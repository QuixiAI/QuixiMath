import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.function_inner_product_generator import FunctionInnerProductGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute the inner product of (sin|cos)\((\d+)x\) and "
    r"(sin|cos)\((\d+)x\) on \[0,2pi\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "family1": match.group(1),
        "m": int(match.group(2)),
        "family2": match.group(3),
        "n": int(match.group(4)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    f = f"{parts['family1']}({parts['m']}x)"
    g = f"{parts['family2']}({parts['n']}x)"
    steps = [
        make_step("INNER_PRODUCT_SETUP", "interval=[0,2pi]",
                  f"f={f}", f"g={g}"),
    ]
    if parts["family1"] == parts["family2"]:
        family = parts["family1"]
        if parts["m"] == parts["n"]:
            steps += [
                make_step("IDENTITY", f"{family}^2({parts['m']}x)",
                          "average term integrates to 1/2"),
                make_step("INTEGRAL", "integral 1 dx on [0,2pi]",
                          "2pi"),
                make_step("INTEGRAL",
                          f"oscillating term for {family}^2", 0),
                make_step("D", 2, 2, 1),
                make_step("CHECK", "same frequency", "nonzero norm"),
            ]
            answer = "inner product = pi"
        else:
            diff = abs(parts["m"] - parts["n"])
            total = parts["m"] + parts["n"]
            sign = "-" if family == "sin" else "+"
            steps += [
                make_step("IDENTITY", f"{f}*{g}",
                          f"1/2(cos({diff}x) {sign} cos({total}x))"),
                make_step("INTEGRAL",
                          f"integral cos({diff}x) on [0,2pi]", 0),
                make_step("INTEGRAL",
                          f"integral cos({total}x) on [0,2pi]", 0),
            ]
            steps.append(make_step("S" if family == "sin" else "A",
                                   0, 0, 0))
            steps += [
                make_step("D", 0, 2, 0),
                make_step("CHECK", "different frequencies", "orthogonal"),
            ]
            answer = "inner product = 0"
    else:
        total = parts["m"] + parts["n"]
        diff = abs(parts["m"] - parts["n"])
        steps += [
            make_step("IDENTITY", f"{f}*{g}",
                      f"1/2(sin({total}x) + sin({diff}x))"),
            make_step("INTEGRAL", f"integral sin({total}x) on [0,2pi]",
                      0),
            make_step("INTEGRAL", f"integral sin({diff}x) on [0,2pi]",
                      0),
            make_step("A", 0, 0, 0),
            make_step("D", 0, 2, 0),
            make_step("CHECK", "sin-cos family", "orthogonal"),
        ]
        answer = "inner product = 0"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFunctionInnerProductGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FunctionInnerProductGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_answer_matches_orthogonality_rule(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if (parts["family1"] == parts["family2"] and
                    parts["m"] == parts["n"]):
                expected = "inner product = pi"
            else:
                expected = "inner product = 0"
            self.assertEqual(result["final_answer"], expected)

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("same_family", "cross_family"):
            gen = FunctionInnerProductGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"function_inner_product_{variant}")

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FunctionInnerProductGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
