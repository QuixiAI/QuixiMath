import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.area_between_curves_generator import (
    AreaBetweenCurvesGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    p_txt = example["problem"]
    m = re.fullmatch(r"Find the area between y = x\^2 and "
                     r"y = (\d+) - x\^2\.", p_txt)
    if m:
        import math
        c = int(m.group(1))
        k = math.isqrt(c // 2)
        assert 2 * k * k == c
        return str(Fraction(8 * k ** 3, 3))
    m = re.fullmatch(r"Find the area between y = x\^2 and "
                     r"y = (.+)\.", p_txt)
    assert m, p_txt
    line = m.group(1)
    mm = re.fullmatch(r"(-?\d*)x(?: ([+-]) (\d+))?|(-?\d+)", line)
    if mm.group(4) is not None:
        slope, inter = 0, int(mm.group(4))
    else:
        g = mm.group(1)
        slope = int(g + "1") if g in ("", "-") else int(g)
        inter = int(mm.group(3) or 0) * \
            (1 if (mm.group(2) or "+") == "+" else -1)
    # intersections: x² - slope·x - inter = 0
    roots = sorted(t for t in range(-30, 31)
                   if t * t - slope * t - inter == 0)
    assert len(roots) == 2
    p, q = roots
    return str(Fraction((q - p) ** 3, 6))


class TestAreaBetweenCurvesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AreaBetweenCurvesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: (q - p)³/6 for secants; (8/3)k³ for the pair."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_area_is_positive(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertGreater(Fraction(result["final_answer"]), 0)

    def test_top_curve_checked(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"CHECK{DELIM}midpoint")
                                for s in result["steps"]))

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            AreaBetweenCurvesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
