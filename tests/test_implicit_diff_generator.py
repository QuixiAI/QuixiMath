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

from generators.implicit_diff_generator import ImplicitDiffGenerator
from helpers import DELIM


def numeric_slope(y_of_x, x):
    h = 1e-6
    return (y_of_x(x + h) - y_of_x(x - h)) / (2 * h)


def oracle_check(example):
    """Compare the claimed dy/dx against a numeric slope on the curve."""
    p = example["problem"]
    ans = example["final_answer"].replace("dy/dx = ", "")

    m = re.fullmatch(r"Find dy/dx for x\^2 \+ y\^2 = (\d+) at the "
                     r"point \((-?\d+), (-?\d+)\)\.", p)
    if m:
        r2, x0, y0 = (int(v) for v in m.groups())
        assert x0 * x0 + y0 * y0 == r2
        return Fraction(ans) == Fraction(-x0, y0)
    m = re.fullmatch(r"Find dy/dx for x\^2 \+ y\^2 = (\d+)\.", p)
    if m:
        r2 = int(m.group(1))
        x = 0.4 * math.sqrt(r2)

        def y_of_x(t):
            return math.sqrt(r2 - t * t)
        y = y_of_x(x)
        assert ans == "-x/y"
        return abs(numeric_slope(y_of_x, x) - (-x / y)) < 1e-4
    m = re.fullmatch(r"Find dy/dx for x\^3 \+ y\^3 = (\d+)\.", p)
    if m:
        c = int(m.group(1))
        x = 0.7

        def y_of_x(t):
            return (c - t ** 3) ** (1 / 3)
        y = y_of_x(x)
        assert ans == "-x^2/y^2"
        return abs(numeric_slope(y_of_x, x) - (-x * x / (y * y))) < 1e-4
    m = re.fullmatch(r"Find dy/dx for xy = (-?\d+)\.", p)
    if m:
        c = int(m.group(1))
        x = 1.3

        def y_of_x(t):
            return c / t
        y = y_of_x(x)
        assert ans == "-y/x"
        return abs(numeric_slope(y_of_x, x) - (-y / x)) < 1e-4
    m = re.fullmatch(r"Find dy/dx for x\^2 \+ xy \+ y\^2 = (\d+)\.", p)
    assert m, p
    c = int(m.group(1))
    x = 0.6

    def y_of_x(t):
        return (-t + math.sqrt(4 * c - 3 * t * t)) / 2
    y = y_of_x(x)
    assert ans == "-(2x + y)/(x + 2y)"
    claimed = -(2 * x + y) / (x + 2 * y)
    return abs(numeric_slope(y_of_x, x) - claimed) < 1e-4


class TestImplicitDiffGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ImplicitDiffGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_curve_slope(self):
        """A9 oracle: slope measured on the actual curve."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_chain_factor_named_for_y_terms(self):
        for _ in range(200):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "IMPLICIT_DIFF" and "of y" in f[1]:
                    self.assertIn("y'", f[2], s)

    def test_at_point_values_reduced(self):
        gen = ImplicitDiffGenerator("circle")
        for _ in range(200):
            result = gen.generate()
            m = re.search(r"= (-?\d+)/(\d+)$", result["final_answer"])
            if m:
                n, d = int(m.group(1)), int(m.group(2))
                self.assertEqual(math.gcd(abs(n), d), 1,
                                 result["final_answer"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ImplicitDiffGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
