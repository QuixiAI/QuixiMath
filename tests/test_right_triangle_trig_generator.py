import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.right_triangle_trig_generator import (
    RightTriangleTrigGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"In a right triangle, the leg opposite angle A is "
                     r"(\d+), the leg adjacent to A is (\d+), and the "
                     r"hypotenuse is (\d+)\. Write (sin|cos|tan) A as a "
                     r"fraction in lowest terms\.", p)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        assert a * a + b * b == c * c
        fn = m.group(4)
        val = {"sin": Fraction(a, c), "cos": Fraction(b, c),
               "tan": Fraction(a, b)}[fn]
        return f"{fn} A = {val}"
    m = re.fullmatch(r"In a right triangle, one acute angle measures "
                     r"(\d+)° and the (.+) is (\d+)\. Given that "
                     r"(sin|cos|tan) \1° ≈ ([\d.]+), find the (.+)\.", p)
    if m:
        known = int(m.group(3))
        val = Fraction(m.group(5))
        x = known * val
        assert x.denominator == 1
        return str(x.numerator)
    m = re.fullmatch(r"In a right triangle, the (.+) is (\d+) and the "
                     r"(.+) is (\d+)\. Given that (sin|cos|tan) (\d+)° ≈ "
                     r"([\d.]+), find the measure of angle A\.", p)
    assert m, p
    num, den = int(m.group(2)), int(m.group(4))
    assert Fraction(num, den) == Fraction(m.group(7))
    return f"A = {m.group(6)}°"


class TestRightTriangleTrigGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RightTriangleTrigGenerator()

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

    def test_needed_values_always_provided(self):
        """Principle 5: any non-triple problem supplies its trig value."""
        for _ in range(300):
            result = self.gen.generate()
            if "lowest terms" not in result["problem"]:
                self.assertIn("≈", result["problem"])

    def test_ratio_definition_stated(self):
        for _ in range(200):
            result = self.gen.generate()
            tr = next(s for s in result["steps"]
                      if s.startswith(f"TRIG_RATIO{DELIM}"))
            fn = tr.split(DELIM)[1]
            self.assertEqual(
                tr.split(DELIM)[2],
                RightTriangleTrigGenerator.RATIO_DEF[fn], tr)

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
                elif f[0] == "FRAC_REDUCE":
                    n, d = f[1].split("/")
                    self.assertEqual(Fraction(int(n), int(d)),
                                     Fraction(f[2]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RightTriangleTrigGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
