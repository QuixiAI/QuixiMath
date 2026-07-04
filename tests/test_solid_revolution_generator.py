import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.solid_revolution_generator import SolidRevolutionGenerator
from generators.arc_sector_generator import pi_txt
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Find the volume when the region under "
                     r"y = (\d*)x on \[0, (\d+)\] is rotated about the "
                     r"x-axis.*", p)
    if m:
        k = int(m.group(1) or 1)
        a = int(m.group(2))
        return pi_txt(Fraction(k * k * a ** 3, 3))
    m = re.fullmatch(r"Find the volume when the region between "
                     r"y = (\d*)x and y = \d*x\^2 on \[0, 1\].*", p)
    if m:
        k = int(m.group(1) or 1)
        return pi_txt(Fraction(2 * k * k, 15))
    m = re.fullmatch(r"Use the shell method to find the volume when "
                     r"the region under y = x\((\d+) - x\) on "
                     r"\[0, \1\].*", p)
    if m:
        a = int(m.group(1))
        return pi_txt(Fraction(a ** 4, 6))
    m = re.fullmatch(r"The base of a solid is the region under "
                     r"y = (\d+) - x on \[0, \1\]\..*", p)
    assert m, p
    c = int(m.group(1))
    return str(Fraction(c ** 3, 3))


class TestSolidRevolutionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SolidRevolutionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: closed-form volumes recomputed exactly."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_pi_absent_only_for_cross_sections(self):
        for _ in range(300):
            result = self.gen.generate()
            if "cross_section" in result["operation"]:
                self.assertNotIn("π", result["final_answer"])
            else:
                self.assertIn("π", result["final_answer"])

    def test_formula_always_stated(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"VOL_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SolidRevolutionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
