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

from generators.trig_six_functions_generator import (
    TrigSixFunctionsGenerator,
    SIGNS,
    ROMAN,
)
from helpers import DELIM


def oracle_answer(example):
    """Rebuilds all six functions from the given ratio and quadrant."""
    m = re.fullmatch(r"Given (sin|cos|tan) θ = (-?\d+/\d+|-?\d+) with θ "
                     r"in quadrant (I{1,3}|IV), find all six "
                     r"trigonometric functions of θ\.",
                     example["problem"])
    assert m, example["problem"]
    fn, val, roman = m.group(1), Fraction(m.group(2)), m.group(3)
    q = {v: k for k, v in ROMAN.items()}[roman]
    ss, cs, ts = SIGNS[q]

    num, den = abs(val.numerator), abs(val.denominator)
    if fn == "sin":
        a, c = num, den
        b = math.isqrt(c * c - a * a)
    elif fn == "cos":
        b, c = num, den
        a = math.isqrt(c * c - b * b)
    else:
        a, b = num, den
        c = math.isqrt(a * a + b * b)
    assert a * a + b * b == c * c

    sin_v = Fraction(ss * a, c)
    cos_v = Fraction(cs * b, c)
    tan_v = Fraction(ts * a, b)
    return (f"sin θ = {sin_v}; cos θ = {cos_v}; tan θ = {tan_v}; "
            f"csc θ = {1 / sin_v}; sec θ = {1 / cos_v}; "
            f"cot θ = {1 / tan_v}")


class TestTrigSixFunctionsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TrigSixFunctionsGenerator()

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

    def test_pythagorean_consistency(self):
        """sin² + cos² = 1 and tan = sin/cos in every record."""
        for _ in range(300):
            result = self.gen.generate()
            vals = dict(re.findall(r"(sin|cos|tan) θ = (-?\d+(?:/\d+)?)",
                                   result["final_answer"]))
            s, c, t = (Fraction(vals[k]) for k in ("sin", "cos", "tan"))
            self.assertEqual(s ** 2 + c ** 2, 1)
            self.assertEqual(t, s / c)

    def test_reciprocals_flip(self):
        for _ in range(300):
            result = self.gen.generate()
            f = result["final_answer"]
            m = dict(re.findall(r"(sin|cos|tan|csc|sec|cot) θ = "
                                r"(-?\d+(?:/\d+)?)", f))
            self.assertEqual(Fraction(m["csc"]), 1 / Fraction(m["sin"]))
            self.assertEqual(Fraction(m["sec"]), 1 / Fraction(m["cos"]))
            self.assertEqual(Fraction(m["cot"]), 1 / Fraction(m["tan"]))

    def test_sign_rules_cited_for_derived(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"SIGN_RULE{DELIM}")
                                for s in result["steps"]))

    def test_all_variants_and_quadrants(self):
        seen = set()
        for _ in range(300):
            result = self.gen.generate()
            q = re.search(r"quadrant (\w+),", result["problem"] + ",")
            seen.add((result["operation"],))
        self.assertEqual(len(seen), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TrigSixFunctionsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
