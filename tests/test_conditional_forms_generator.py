"""Independent A9 checks for ConditionalFormsGenerator."""
import random
import re
import unittest

from generators.conditional_forms_generator import ConditionalFormsGenerator, QUERIES
from helpers import DELIM
from tests import foundations_oracle as logic_oracle


def split_query(problem, variant):
    for query in QUERIES[variant]:
        if problem.endswith(f" {query}"):
            return problem[:-(len(query) + 1)], query
    raise AssertionError(problem)


def transformed(hypothesis, conclusion, form):
    if form == "converse":
        return ("imp", conclusion, hypothesis)
    if form == "inverse":
        return ("imp", ("not", hypothesis), ("not", conclusion))
    return ("imp", ("not", conclusion), ("not", hypothesis))


def negate_english(predicate):
    match = re.fullmatch(r"n is divisible by (\d+)", predicate)
    if match:
        return f"n is not divisible by {match.group(1)}"
    match = re.fullmatch(r"n > (-?\d+)", predicate)
    if match:
        return f"n ≤ {match.group(1)}"
    if predicate == "n is even":
        return "n is odd"
    raise AssertionError(predicate)


def english_result(hypothesis, conclusion, form):
    if form == "converse":
        return f"If {conclusion}, then {hypothesis}."
    if form == "inverse":
        return f"If {negate_english(hypothesis)}, then {negate_english(conclusion)}."
    return f"If {negate_english(conclusion)}, then {negate_english(hypothesis)}."


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("Biconditional: "):
        body, query = split_query(problem, "biconditional_split")
        formula_text = body[len("Biconditional: "):-1]
        node = logic_oracle.parse_formula(formula_text)
        assert node[0] == "iff"
        forward = logic_oracle.render(("imp", node[1], node[2]))
        reverse = logic_oracle.render(("imp", node[2], node[1]))
        return {"variant": "biconditional_split", "answer": f"{forward}; {reverse}",
                "forms": {"forward": forward, "reverse": reverse},
                "parts": (logic_oracle.render(node[1]),
                          logic_oracle.render(node[2])), "query": query}
    if "Consider its converse" in problem:
        body, query = split_query(problem, "truth_with_counterexample")
        match = re.fullmatch(
            r"Conditional: If n is divisible by (\d+), then n is divisible by "
            r"(\d+), for integers n ≥ (\d+)\. Consider its converse and scan "
            r"multiples of \2 in increasing order\.", body
        )
        assert match is not None, body
        stronger, base, lower = map(int, match.groups())
        value = ((lower + base - 1) // base) * base
        trials = []
        while value % stronger == 0:
            trials.append(value)
            value += base
        trials.append(value)
        witness = f"{value} is divisible by {base} but not by {stronger}"
        answer = f"converse: false; counterexample n = {value} ({witness})"
        converse = (f"If n is divisible by {base}, then n is divisible by "
                    f"{stronger}.")
        return {"variant": "truth_with_counterexample", "answer": answer,
                "forms": {"converse": converse}, "trials": trials,
                "parts": (f"n divisible by {stronger}", f"n divisible by {base}"),
                "query": query}
    if problem.startswith("Conditional: If "):
        body, query = split_query(problem, "english")
        match = re.fullmatch(
            r"Conditional: If (.+), then (.+)\. Requested form: "
            r"(converse|inverse|contrapositive)\.", body
        )
        assert match is not None, body
        hypothesis, conclusion, form = match.groups()
        result = english_result(hypothesis, conclusion, form)
        return {"variant": "english", "answer": result,
                "forms": {form: result}, "parts": (hypothesis, conclusion),
                "query": query}

    body, query = split_query(problem, "symbolic")
    match = re.fullmatch(
        r"Conditional: (.+)\. Requested form: (converse|inverse|contrapositive)\.",
        body,
    )
    assert match is not None, body
    node = logic_oracle.parse_formula(match.group(1))
    assert node[0] == "imp"
    result = logic_oracle.render(transformed(node[1], node[2], match.group(2)))
    return {"variant": "symbolic", "answer": result,
            "forms": {match.group(2): result},
            "parts": (logic_oracle.render(node[1]), logic_oracle.render(node[2])),
            "query": query}


class ConditionalFormsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(324161)

    def test_output_contract(self):
        example = ConditionalFormsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ConditionalFormsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_parts_forms_and_counterexample_scan_steps(self):
        generator = ConditionalFormsGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_forms = {}
            seen_trials = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "COND_PARTS":
                    self.assertEqual(tuple(fields[1:]), parts["parts"])
                elif fields[0] == "FORM":
                    seen_forms[fields[1]] = fields[2]
                elif fields[0] == "DIV_CHECK":
                    value, divisor = int(fields[1]), int(fields[2])
                    self.assertIn(f"remainder {value % divisor}", fields[3])
                elif fields[0] == "TRY":
                    seen_trials.append(int(fields[1].split(" = ")[1]))
            self.assertEqual(seen_forms, parts["forms"])
            if parts["variant"] == "truth_with_counterexample":
                self.assertEqual(seen_trials, parts["trials"])
                self.assertLessEqual(len(seen_trials), 12)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ConditionalFormsGenerator.VARIANTS:
            generator = ConditionalFormsGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"conditional_forms_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            ConditionalFormsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ConditionalFormsGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
