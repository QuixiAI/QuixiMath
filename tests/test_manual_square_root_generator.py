import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.manual_square_root_generator import (
    ManualSquareRootGenerator, exact,
)
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the square-root result from the prompt."""
    problem = example["problem"]
    m = re.search(r"Find sqrt\((\d+)\)", problem)
    if m:
        return str(math.isqrt(int(m.group(1))))
    n, estimate = (int(v) for v in re.search(
        r"estimate sqrt\((\d+)\) starting from x0 = (\d+)",
        problem,
    ).groups())
    return exact((Fraction(estimate) + Fraction(n, estimate)) / 2)


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "SQRT_TRIAL":
            base, digit, digit_again, product = (int(v) for v in re.fullmatch(
                r"\((\d+) \+ (\d+)\)\*(\d+) = (\d+)", parts[2]
            ).groups())
            if digit != digit_again or (base + digit) * digit != product:
                return False
        elif code == "S":
            if Fraction(parts[1]) - Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif code == "A":
            if exact(Fraction(parts[1]) + Fraction(parts[2])) != parts[3]:
                return False
        elif code == "D":
            if exact(Fraction(parts[1]) / Fraction(parts[2])) != parts[3]:
                return False
        elif code == "CHECK" and len(parts) == 4 and parts[1].endswith("^2"):
            root = int(parts[1][:-2])
            if root * root != int(parts[2]) or int(parts[2]) != int(parts[3]):
                return False
    return True


class TestManualSquareRootGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ManualSquareRootGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_digit_variant_has_trials_and_check(self):
        gen = ManualSquareRootGenerator("digit_by_digit")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"SQRT_TRIAL{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"CHECK{DELIM}")
                                for s in result["steps"]))

    def test_divide_average_has_formula_check(self):
        gen = ManualSquareRootGenerator("divide_average")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any("(x + N/x)/2" in s for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(50):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ManualSquareRootGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
