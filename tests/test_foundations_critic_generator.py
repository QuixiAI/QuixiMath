"""Independent critic oracle for FoundationsCriticGenerator."""
import re
import unittest
import random

from generators.foundations_critic_generator import (
    FoundationsCriticGenerator, QUERIES,
)
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_roster(text):
    return set() if text == "∅" else set(oracle.parse_roster(text))


def proof_rule(formulas):
    if len(formulas) == 3:
        first, second, result = formulas
        if first[0] == "imp" and first[1] == second and first[2] == result:
            return "MP 1,2"
        if result == ("and", first, second):
            return "∧I 1,2"
    if len(formulas) == 2:
        first, result = formulas
        if first[0] == "and" and first[1] == result:
            return "∧E 1"
        if result[0] == "or" and result[1] == first:
            return "∨I 1"
    raise AssertionError(formulas)


def derived_formula(premises, justification):
    if justification == "MP 1,2":
        assert premises[0][0] == "imp" and premises[0][1] == premises[1]
        return premises[0][2]
    if justification == "∧I 1,2":
        return ("and", premises[0], premises[1])
    if justification == "∧E 1":
        return premises[0][1]
    if justification == "∨I 1":
        # The displayed target is blank, so the second disjunct is encoded in
        # the problem's canonical rule instance only through its CHECK trace.
        raise AssertionError("∨I missing-line instances are not self-contained")
    raise AssertionError(justification)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "truth_table_error":
        header, *shown = body.splitlines()
        match = re.fullmatch(
            r"A worked truth table has one wrong row; the final classification "
            r"follows the displayed column\. Formula: (.+)\. Variable order: "
            r"([a-z](?:, [a-z])*)\; T rows precede F rows\.", header)
        assert match is not None, header
        formula = oracle.parse_formula(match.group(1))
        names = tuple(match.group(2).split(", "))
        rows = oracle.truth_rows(formula, names)
        bad = None
        values = []
        for index, (assignment, value) in enumerate(rows, 1):
            row = re.fullmatch(rf"{index}\) row (.+) gives ([TF])", shown[index - 1])
            assert row is not None
            displayed = row.group(2) == "T"
            values.append(value)
            if displayed != value:
                assert bad is None
                bad = index
        assert shown[-1].endswith("classification: contingent")
        assert bad is not None
        column = "".join("T" if value else "F" for value in values)
        classification = oracle.classify(formula)
        answer = f"step {bad}; column {column}; {classification}"
        case = classification
    elif variant == "membership_table_error":
        header, *shown = body.splitlines()
        match = re.fullmatch(
            r"A worked membership table has one wrong entry; the final verdict "
            r"follows the displayed columns\. Identity: A ∩ \(B ∪ C\) = "
            r"\(A ∩ B\) ∪ \(A ∩ C\)\. U=(.+); A=(.+); B=(.+); C=(.+)\.",
            header)
        assert match is not None, header
        universe, a_set, b_set, c_set = map(parse_roster, match.groups())
        left = a_set & (b_set | c_set)
        right = (a_set & b_set) | (a_set & c_set)
        assert left == right
        bad = None
        for index, value in enumerate(sorted(universe), 1):
            row = re.fullmatch(
                rf"{index}\) x={value}: left ([TF]); right ([TF])",
                shown[index - 1])
            assert row is not None
            displayed = (row.group(1) == "T", row.group(2) == "T")
            correct = (value in left, value in right)
            if displayed != correct:
                assert bad is None
                bad = index
        assert bad is not None
        answer = f"step {bad}; identity; columns match"
        case = "membership"
    else:
        header, *shown = body.splitlines()
        assert header == "Natural-deduction proof with one blank."
        parsed = []
        blank_line = None
        blank_annotation = None
        for expected, line in enumerate(shown, 1):
            match = re.fullmatch(r"(\d+)\) (.+) \[(.+)\]", line)
            assert match is not None, line
            assert int(match.group(1)) == expected
            formula_text, annotation = match.group(2), match.group(3)
            if formula_text == "____" or annotation == "____":
                blank_line = expected
                blank_annotation = annotation
            parsed.append(None if formula_text == "____"
                          else oracle.parse_formula(formula_text))
        assert blank_line is not None
        if variant == "missing_justification":
            missing = proof_rule(parsed)
            case = missing.split()[0]
        else:
            justification = blank_annotation
            if justification == "∨I 1":
                # The independent oracle can recover a ∨I target only if its
                # second disjunct is stated; the generator excludes this case.
                raise AssertionError(example["problem"])
            missing_ast = derived_formula(parsed[:-1], justification)
            missing = oracle.render(missing_ast)
            case = justification.split()[0]
        answer = f"step {blank_line}; {missing}"
    return {"variant": variant, "query": query, "answer": answer,
            "case": case}


class FoundationsCriticGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(316227)

    def test_output_contract(self):
        example = FoundationsCriticGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = FoundationsCriticGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in FoundationsCriticGenerator.VARIANTS:
            generator = FoundationsCriticGenerator(variant)
            seen_queries = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"foundations_critic_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FoundationsCriticGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FoundationsCriticGenerator()
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
