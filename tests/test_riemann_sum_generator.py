import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.riemann_sum_generator import RiemannSumGenerator
from generators.exponential_model_generator import dec
from tests.test_derivative_power_rule_generator import parse_terms
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"Approximate ∫ from (-?\d+) to (-?\d+) of "
                     r"\((.+)\) dx using the (.+) with n = 4\.",
                     example["problem"])
    assert m, example["problem"]
    a, b = int(m.group(1)), int(m.group(2))
    terms = parse_terms(m.group(3))
    method = m.group(4)

    def f(x):
        return sum(c * x ** n for c, n in terms)
    n = 4
    dx = (b - a) // n
    if "left" in method:
        total = sum(f(a + i * dx) for i in range(n)) * dx
        return str(total)
    if "right" in method:
        total = sum(f(a + (i + 1) * dx) for i in range(n)) * dx
        return str(total)
    if "midpoint" in method:
        total = sum(f(a + i * dx + dx // 2) for i in range(n)) * dx
        return str(total)
    vals = [f(a + i * dx) for i in range(n + 1)]
    total = Fraction(dx, 2) * (vals[0] + 2 * sum(vals[1:-1]) + vals[-1])
    return dec(total)


class TestRiemannSumGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RiemannSumGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute each rule from scratch."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_table_has_expected_row_count(self):
        for _ in range(300):
            result = self.gen.generate()
            fevals = [s for s in result["steps"]
                      if s.startswith(f"EVAL{DELIM}f(")]
            if "trapezoid" in result["operation"]:
                self.assertEqual(len(fevals), 5)
            else:
                self.assertEqual(len(fevals), 4)

    def test_trapezoid_doubles_interior(self):
        gen = RiemannSumGenerator("trapezoid")
        for _ in range(100):
            result = gen.generate()
            doubles = [s for s in result["steps"]
                       if s.startswith(f"M{DELIM}2{DELIM}")]
            self.assertEqual(len(doubles), 3)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(Fraction(f[1]) * Fraction(f[2]),
                                     Fraction(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RiemannSumGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
