"""Independent A9 checks for LogicalConnectiveEvalGenerator."""
import math
import random
import re
import unittest

from generators.logical_connective_eval_generator import (
    LogicalConnectiveEvalGenerator,
    QUERIES,
)
from helpers import DELIM
from tests import foundations_oracle as logic_oracle


def is_prime(value):
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def evaluate_statement(statement):
    match = re.fullmatch(r"(\d+) is (even|odd)", statement)
    if match:
        value = int(match.group(1))
        return (value % 2 == 0) if match.group(2) == "even" else (value % 2 == 1)
    match = re.fullmatch(r"(\d+) is (greater than|less than) (\d+)", statement)
    if match:
        left, right = int(match.group(1)), int(match.group(3))
        return left > right if match.group(2) == "greater than" else left < right
    match = re.fullmatch(r"(\d+) is divisible by (\d+)", statement)
    if match:
        return int(match.group(1)) % int(match.group(2)) == 0
    match = re.fullmatch(r"(\d+) is prime", statement)
    if match:
        return is_prime(int(match.group(1)))
    match = re.fullmatch(r"(\d+) has (\d+) digits", statement)
    if match:
        return len(match.group(1)) == int(match.group(2))
    raise AssertionError(statement)


def parse_problem(problem):
    if isinstance(problem, dict):
        problem = problem["problem"]
    query = next((item for item in QUERIES if problem.endswith(f" {item}")), None)
    assert query is not None, problem
    body = problem[:-(len(query) + 1)]
    match = re.fullmatch(r"((?:Let [pqr]: [^.]+\. )+)Evaluate (.+)\.", body)
    assert match is not None, body
    statements = dict(re.findall(r"Let ([pqr]): ([^.]+)\. ", match.group(1)))
    formula = match.group(2)
    assignment = {name: evaluate_statement(statement)
                  for name, statement in statements.items()}
    value = logic_oracle.eval_formula(logic_oracle.parse_formula(formula), assignment)
    answer = "; ".join(
        [f"{name} = {'T' if assignment[name] else 'F'}"
         for name in sorted(statements)]
        + [f"{formula} = {'T' if value else 'F'}"]
    )
    if len(statements) == 3:
        variant = "nested"
    elif formula.startswith("¬"):
        variant = "not"
    else:
        variant = "and_or"
    return {
        "statements": statements,
        "assignment": assignment,
        "formula": formula,
        "value": value,
        "answer": answer,
        "variant": variant,
        "query": query,
    }


class LogicalConnectiveEvalGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(155921)

    def test_output_contract(self):
        example = LogicalConnectiveEvalGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LogicalConnectiveEvalGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], parse_problem(example)["answer"],
                             example["problem"])

    def test_arithmetic_and_connective_steps(self):
        generator = LogicalConnectiveEvalGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = parse_problem(example)
            statement_steps = {}
            connective_count = 0
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "DIV_CHECK":
                    value, divisor = int(fields[1]), int(fields[2])
                    self.assertIn(f"remainder {value % divisor}", fields[3])
                    if "quotient" in fields[3]:
                        self.assertEqual(
                            fields[3],
                            f"quotient {value // divisor}, remainder {value % divisor}",
                        )
                elif fields[0] == "CMP":
                    left, right = int(fields[1]), int(fields[2])
                    expected = "<" if left < right else ">"
                    self.assertEqual(fields[3], expected)
                elif fields[0] == "COUNT":
                    match = re.fullmatch(r"digits of (\d+)", fields[1])
                    self.assertIsNotNone(match)
                    self.assertEqual(int(fields[2]), len(match.group(1)))
                elif fields[0] == "STMT_EVAL":
                    name, statement, value = fields[1:]
                    self.assertEqual(statement, parts["statements"][name])
                    self.assertEqual(value,
                                     "T" if evaluate_statement(statement) else "F")
                    statement_steps[name] = value
                elif fields[0] == "CONNECTIVE":
                    formula, value = fields[1:]
                    actual = logic_oracle.eval_formula(
                        logic_oracle.parse_formula(formula), parts["assignment"]
                    )
                    self.assertEqual(value, "T" if actual else "F")
                    connective_count += 1
            self.assertEqual(set(statement_steps), set(parts["statements"]))
            self.assertGreaterEqual(connective_count, 1)

    def test_all_variants_phrasings_and_truth_outcomes_are_reachable(self):
        for variant in LogicalConnectiveEvalGenerator.VARIANTS:
            generator = LogicalConnectiveEvalGenerator(variant)
            seen_queries = set()
            seen_values = set()
            for _ in range(500):
                example = generator.generate()
                parts = parse_problem(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"logical_connective_eval_{variant}")
                seen_queries.add(parts["query"])
                seen_values.add(parts["value"])
            self.assertEqual(seen_queries, set(QUERIES))
            self.assertEqual(seen_values, {False, True})

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            LogicalConnectiveEvalGenerator("bogus")

    def test_pipe_safety_formula_canonicality_and_render_sanity(self):
        generator = LogicalConnectiveEvalGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = parse_problem(example)
            self.assertTrue(logic_oracle.is_canonical_formula(parts["formula"]))
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
