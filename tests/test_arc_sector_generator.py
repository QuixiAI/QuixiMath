import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.arc_sector_generator import ArcSectorGenerator, pi_txt
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"A circle has radius (\d+)\. Find the length of "
                     r"the arc cut off by a central angle of (\d+)°\. "
                     r"Give the exact answer in terms of π\.", p)
    if m:
        r, theta = int(m.group(1)), int(m.group(2))
        return pi_txt(Fraction(theta, 360) * 2 * r)
    m = re.fullmatch(r"A circle has radius (\d+)\. Find the area of the "
                     r"sector with central angle (\d+)°\. Give the "
                     r"exact answer in terms of π\.", p)
    assert m, p
    r, theta = int(m.group(1)), int(m.group(2))
    return pi_txt(Fraction(theta, 360) * r * r)


class TestArcSectorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ArcSectorGenerator()

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

    def test_angle_fraction_reduced(self):
        for _ in range(300):
            result = self.gen.generate()
            fr = next(s for s in result["steps"]
                      if s.startswith(f"FRAC_REDUCE{DELIM}"))
            f = fr.split(DELIM)
            theta = int(f[1].split("/")[0])
            self.assertEqual(Fraction(theta, 360), Fraction(f[2]), fr)

    def test_step_arithmetic_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(Fraction(f[1]) * Fraction(f[2]),
                                     Fraction(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)

    def test_fraction_pi_answers_occur(self):
        kinds = set()
        for _ in range(200):
            kinds.add("/" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"arc_measure", "sector_measure"})


if __name__ == "__main__":
    unittest.main()
