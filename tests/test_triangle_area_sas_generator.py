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

from generators.triangle_area_sas_generator import (
    TriangleAreaSASGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"A triangle has sides a = (\d+) and b = (\d+) "
                     r"with included angle C = (\d+)°\. Given sin \3° = "
                     r"([\d.]+), find its area\.", example["problem"])
    assert m, example["problem"]
    a, b, C = int(m.group(1)), int(m.group(2)), int(m.group(3))
    sv = Fraction(m.group(4))
    assert abs(float(sv) - math.sin(math.radians(C))) < 0.02
    return f"{dec(Fraction(a * b) * sv / 2)} square units"


class TestTriangleAreaSASGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TriangleAreaSASGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_obtuse_angles_occur(self):
        found = False
        for _ in range(200):
            if "150°" in self.gen.generate()["problem"]:
                found = True
                break
        self.assertTrue(found)

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
