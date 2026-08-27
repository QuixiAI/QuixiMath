"""Independent line parser and rule-schema oracle for natural deduction."""
import random
import re
import unittest

from generators.natural_deduction_generator import QUERIES, NaturalDeductionGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_lines(text):
    lines = []
    for raw in text.split("; "):
        match = re.fullmatch(r"(\d+)\. (.+) \[(.+)\]", raw)
        assert match is not None, raw
        number = int(match.group(1))
        formula = None if match.group(2) == "____" else oracle.parse_formula(
            match.group(2))
        lines.append((number, formula, match.group(3)))
    assert [line[0] for line in lines] == list(range(1, len(lines) + 1))
    return lines


def apply_rule(rule, citations, formulas, displayed=None):
    indices = [int(value) for value in citations.split(",") if value]
    if rule == "∧I":
        assert len(indices) == 2
        return ("and", formulas[indices[0]], formulas[indices[1]])
    if rule in ("∧E₁", "∧E₂"):
        assert len(indices) == 1
        conjunction = formulas[indices[0]]
        assert conjunction[0] == "and"
        return conjunction[1 if rule == "∧E₁" else 2]
    if rule == "→E":
        assert len(indices) == 2
        first, second = formulas[indices[0]], formulas[indices[1]]
        if first[0] == "imp" and first[1] == second:
            return first[2]
        assert second[0] == "imp" and second[1] == first
        return second[2]
    if rule == "∨I":
        assert len(indices) == 1 and displayed is not None
        assert displayed[0] == "or"
        assert formulas[indices[0]] in displayed[1:]
        return displayed
    raise AssertionError((rule, citations))


def forced_chain(premises):
    lines = list(premises)
    derived = []
    while True:
        selected = None
        for source_number, formula in enumerate(lines, 1):
            if formula[0] == "and":
                for rule, child in (("∧E₁", formula[1]), ("∧E₂", formula[2])):
                    if child not in lines:
                        selected = (child, rule, str(source_number))
                        break
                if selected:
                    break
            if formula[0] == "imp":
                for antecedent_number, antecedent in enumerate(lines, 1):
                    if antecedent == formula[1] and formula[2] not in lines:
                        selected = (formula[2], "→E",
                                    f"{source_number},{antecedent_number}")
                        break
                if selected:
                    break
        if selected is None:
            return derived
        formula, rule, citations = selected
        lines.append(formula)
        derived.append((len(lines), formula, rule, citations))


def render(node):
    return oracle.render(node)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "forward_chain":
        match = re.fullmatch(
            r"Premises in line order: (.+)\. Policy: (.+)\.", body)
        assert match is not None, body
        premise_parts = match.group(1).split("; ")
        premises = []
        for expected, raw in enumerate(premise_parts, 1):
            line = re.fullmatch(r"(\d+)\. (.+)", raw)
            assert line is not None and int(line.group(1)) == expected
            premises.append(oracle.parse_formula(line.group(2)))
        derived = forced_chain(premises)
        answer = "; ".join(f"{number}: {render(formula)}"
                           for number, formula, _, _ in derived)
        return {"variant": variant, "query": query, "premises": premises,
                "derived": derived, "answer": answer}

    prefix = "Fitch derivation: " if variant == "conditional_proof" else "Derivation: "
    assert body.startswith(prefix), body
    rest = body[len(prefix):]
    if variant == "conditional_proof":
        suffix = ". Lines 2–3 form one subproof."
        assert rest.endswith(suffix), rest
        rest = rest[:-len(suffix)]
    else:
        assert rest.endswith("."), rest
        rest = rest[:-1]
    lines = parse_lines(rest)
    formulas = {number: formula for number, formula, _ in lines}

    if variant == "justify":
        expected = {3: "∧I 1,2", 4: "∨I 3", 6: "→E 5,4"}
        for number, rule_text in expected.items():
            rule, _, citations = rule_text.partition(" ")
            self_formula = formulas[number]
            self_result = apply_rule(rule, citations, formulas, self_formula)
            assert self_result == self_formula
        answer = "; ".join(f"{number}: {expected[number]}"
                           for number in (3, 4, 6))
    elif variant == "missing_line":
        missing = next(number for number, formula, _ in lines if formula is None)
        rule_text = lines[missing - 1][2]
        rule, _, citations = rule_text.partition(" ")
        formula = apply_rule(rule, citations, formulas)
        formulas[missing] = formula
        answer = f"line {missing}: {render(formula)}"
    else:
        assert lines[1][2] == "____" and lines[2][2] == "____"
        assert lines[3][2] == "____"
        if formulas[3][0] == "and":
            assert formulas[3] == ("and", formulas[1], formulas[2])
            third = "∧I 1,2"
        else:
            assert formulas[1][0] == "imp" and formulas[1][1] == formulas[2]
            assert formulas[1][2] == formulas[3]
            third = "→E 1,2"
        assert formulas[4] == ("imp", formulas[2], formulas[3])
        answer = f"2: assumption; 3: {third}; 4: →I 2–3"
    return {"variant": variant, "query": query, "lines": lines,
            "formulas": formulas, "answer": answer}


class NaturalDeductionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(911287)

    def test_output_contract(self):
        example = NaturalDeductionGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = NaturalDeductionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_every_apply_step_matches_its_cited_rule_schema(self):
        generator = NaturalDeductionGenerator()
        for _ in range(300):
            example = generator.generate()
            formulas = {}
            next_number = 1
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "PREMISE":
                    number = int(fields[1])
                    formulas[number] = oracle.parse_formula(fields[2])
                    next_number = max(next_number, number + 1)
                elif fields[0] == "SUBPROOF_OPEN":
                    formulas[next_number] = oracle.parse_formula(fields[2])
                    next_number += 1
                elif fields[0] == "APPLY":
                    displayed = oracle.parse_formula(fields[3])
                    result = apply_rule(fields[1], fields[2], formulas, displayed)
                    self.assertEqual(result, displayed)
                    formulas[next_number] = displayed
                    next_number += 1
                elif fields[0] == "SUBPROOF_CLOSE":
                    displayed = oracle.parse_formula(fields[3])
                    self.assertEqual(displayed,
                                     ("imp", formulas[2], formulas[3]))
                    formulas[next_number] = displayed
                    next_number += 1

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in NaturalDeductionGenerator.VARIANTS:
            generator = NaturalDeductionGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"natural_deduction_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NaturalDeductionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = NaturalDeductionGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
