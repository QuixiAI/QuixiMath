import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.regular_polygon_area_generator import (
    RegularPolygonAreaGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM

SIDES = {"pentagon": 5, "hexagon": 6, "heptagon": 7, "octagon": 8,
         "nonagon": 9, "decagon": 10}


def oracle_answer(example):
    """Recomputes (1/2)·a·P exactly from the problem text."""
    m = re.fullmatch(r"A regular (\w+) has side length (\d+) and apothem "
                     r"([\d.]+)\. Find its area\.", example["problem"])
    assert m, example["problem"]
    n = SIDES[m.group(1)]
    s = int(m.group(2))
    a = Fraction(m.group(3))
    return f"{dec(a * n * s / 2)} square units"


class TestRegularPolygonAreaGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RegularPolygonAreaGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute the area exactly."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_apothem_is_realistic(self):
        """Given apothem within half a unit of the true apothem."""
        import math
        for _ in range(300):
            result = self.gen.generate()
            m = re.fullmatch(r"A regular (\w+) has side length (\d+) and "
                             r"apothem ([\d.]+)\. Find its area\.",
                             result["problem"])
            n, s, a = SIDES[m.group(1)], int(m.group(2)), float(m.group(3))
            true_a = s / (2 * math.tan(math.pi / n))
            self.assertLessEqual(abs(a - true_a), 0.5, result["problem"])

    def test_step_arithmetic_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(Fraction(f[1]) * Fraction(f[2]),
                                     Fraction(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(Fraction(f[1]) / Fraction(f[2]),
                                     Fraction(f[3]), s)


if __name__ == "__main__":
    unittest.main()
