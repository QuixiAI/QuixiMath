import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.cramers_rule_generator import CramersRuleGenerator
from helpers import DELIM


def parse_eq(txt):
    """'3x + 2y = 8' -> (a, b, e)."""
    m = re.fullmatch(r"(-?\d*)x ([+-]) (\d*)y = (-?\d+)", txt)
    assert m, txt
    a = int(m.group(1) + "1") if m.group(1) in ("", "-") \
        else int(m.group(1))
    b = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    return a, b, int(m.group(4))


def oracle_answer(example):
    m = re.fullmatch(r"Solve the system using Cramer's rule: "
                     r"(.+); (.+)\.", example["problem"])
    a, b, e = parse_eq(m.group(1))
    c, d, f = parse_eq(m.group(2))
    D = a * d - b * c
    x = Fraction(e * d - b * f, D)
    y = Fraction(a * f - e * c, D)
    assert x.denominator == 1 and y.denominator == 1
    return f"x = {x.numerator}, y = {y.numerator}"


class TestCramersRuleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CramersRuleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve the system independently."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_solution_satisfies_both_equations(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.fullmatch(r"Solve the system using Cramer's rule: "
                             r"(.+); (.+)\.", result["problem"])
            a, b, e = parse_eq(m.group(1))
            c, d, f = parse_eq(m.group(2))
            mm = re.fullmatch(r"x = (-?\d+), y = (-?\d+)",
                              result["final_answer"])
            x, y = int(mm.group(1)), int(mm.group(2))
            self.assertEqual(a * x + b * y, e)
            self.assertEqual(c * x + d * y, f)

    def test_nonzero_check_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any("≠ 0" in s for s in result["steps"]
                                if s.startswith(f"CHECK{DELIM}")))

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)


if __name__ == "__main__":
    unittest.main()
