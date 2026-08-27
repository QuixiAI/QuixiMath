"""Independent A9 checks for SetBuilderRosterGenerator."""
import math
import random
import re
import unittest

from generators.set_builder_roster_generator import QUERIES, SetBuilderRosterGenerator
from helpers import DELIM
from tests import foundations_oracle as set_oracle


def parse_problem(example):
    problem = example["problem"]
    all_queries = QUERIES["list"] + QUERIES["cardinality"]
    query = next((item for item in all_queries if problem.endswith(f" {item}")), None)
    assert query is not None, problem
    body = problem[:-(len(query) + 1)]
    match = re.fullmatch(r"Set S = (\{x ∈ ℤ : .+\})\.", body)
    assert match is not None, body
    expression = match.group(1)
    accepted = set_oracle.eval_set_builder(expression)
    result_roster = set_oracle.roster_text(accepted).replace("-", "−")
    cardinality = query in QUERIES["cardinality"]
    answer = (f"card(S) = {len(accepted)}; S = {result_roster}"
              if cardinality else result_roster)
    condition = set_oracle.parse_set_builder(expression)[2]
    if cardinality:
        variant = "cardinality"
    elif " and (" in condition:
        variant = "compound_condition"
    elif "prime" in condition or "perfect square" in condition:
        variant = "squares_primes"
    elif condition.count(" and "):
        variant = "parity_divisibility"
    else:
        variant = "integer_range"
    return {"expression": expression, "condition": condition,
            "accepted": accepted, "answer": answer, "variant": variant,
            "query": query}


def signed_int(text):
    return int(text.replace("−", "-"))


class SetBuilderRosterGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(216091)

    def test_output_contract(self):
        example = SetBuilderRosterGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetBuilderRosterGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], parse_problem(example)["answer"],
                             example["problem"])

    def test_trial_and_predicate_arithmetic_steps(self):
        generator = SetBuilderRosterGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = parse_problem(example)
            tried = []
            accepted_steps = []
            rejected_steps = []
            roster_step = None
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "DIV_CHECK":
                    value, divisor = int(fields[1]), int(fields[2])
                    self.assertIn(f"remainder {value % divisor}", fields[3])
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "CMP":
                    left, right = int(fields[1]), int(fields[2])
                    relation = "<" if left < right else ("=" if left == right else ">")
                    self.assertIn(fields[3], (relation, "≥"))
                    if fields[3] == "≥":
                        self.assertGreaterEqual(left, right)
                elif fields[0] == "TRY":
                    value = signed_int(fields[1].split(" = ")[1])
                    tried.append(value)
                    expected = value in parts["accepted"]
                    self.assertEqual(fields[3], "true" if expected else "false")
                elif fields[0] == "ACCEPT":
                    accepted_steps.append(signed_int(fields[1].split(" = ")[1]))
                elif fields[0] == "REJECT":
                    rejected_steps.append(signed_int(fields[1].split(" = ")[1]))
                elif fields[0] == "ROSTER":
                    roster_step = fields[2]
                elif fields[0] == "COUNT":
                    self.assertEqual(fields[1:], ["S", str(len(parts["accepted"]))])
            self.assertEqual(accepted_steps,
                             [value for value in tried if value in parts["accepted"]])
            self.assertEqual(rejected_steps,
                             [value for value in tried if value not in parts["accepted"]])
            self.assertEqual(roster_step,
                             set_oracle.roster_text(parts["accepted"]).replace("-", "−"))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SetBuilderRosterGenerator.VARIANTS:
            generator = SetBuilderRosterGenerator(variant)
            seen = set()
            for _ in range(500):
                example = generator.generate()
                parts = parse_problem(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"set_builder_roster_{variant}")
                seen.add(parts["query"])
            expected = (set(QUERIES["cardinality"]) if variant == "cardinality"
                        else set(QUERIES["list"]))
            self.assertEqual(seen, expected)

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            SetBuilderRosterGenerator("bogus")

    def test_pipe_safety_canonical_answer_and_render_sanity(self):
        generator = SetBuilderRosterGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = parse_problem(example)
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            self.assertEqual(set_oracle.eval_set_builder(parts["expression"]),
                             parts["accepted"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
