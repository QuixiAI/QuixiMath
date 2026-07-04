import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.related_rates_generator import RelatedRatesGenerator
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"The radius of a circle grows at (\d+) cm/s\. How "
                     r"fast is the area increasing when the radius is "
                     r"(\d+) cm\? Give an exact answer\.", p)
    if m:
        k, r0 = int(m.group(1)), int(m.group(2))
        return f"dA/dt = {2 * r0 * k}π cm²/s"
    m = re.fullmatch(r"A (\d+) ft ladder leans against a wall\. The "
                     r"base slides away from the wall at (\d+) ft/s\. "
                     r"How fast is the top sliding down when the base "
                     r"is (\d+) ft from the wall\?", p)
    if m:
        L, k, x0 = (int(v) for v in m.groups())
        y2 = L * L - x0 * x0
        import math
        y0 = math.isqrt(y2)
        assert y0 * y0 == y2
        return f"dy/dt = {Fraction(-x0 * k, y0)} ft/s"
    m = re.fullmatch(r"Each edge of a cube grows at (\d+) cm/s\. How "
                     r"fast is the volume increasing when the edge is "
                     r"(\d+) cm\?", p)
    if m:
        k, s0 = int(m.group(1)), int(m.group(2))
        return f"dV/dt = {3 * s0 * s0 * k} cm³/s"
    m = re.fullmatch(r"Water pours into a conical tank \(radius equals "
                     r"half the depth\) at (\d+) m³/min\. How fast is "
                     r"the depth rising when the water is (\d+) m "
                     r"deep\? Give an exact answer\.", p)
    assert m, p
    k, h0 = int(m.group(1)), int(m.group(2))
    rate = Fraction(4 * k, h0 * h0)
    rtxt = (f"{rate}/π" if rate.denominator == 1
            else f"{rate.numerator}/({rate.denominator}π)")
    return f"dh/dt = {rtxt} m/min"


class TestRelatedRatesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RelatedRatesGenerator()

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

    def test_relation_differentiated_in_t(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"IMPLICIT_DIFF{DELIM}")
                                and "d/dt" in s
                                for s in result["steps"]))

    def test_ladder_rate_is_negative(self):
        gen = RelatedRatesGenerator("ladder")
        for _ in range(100):
            result = gen.generate()
            m = re.search(r"= (-\d+(?:/\d+)?) ft/s",
                          result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])

    def test_answers_have_units(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertRegex(result["final_answer"],
                             r"(cm²/s|ft/s|cm³/s|m/min)$")

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RelatedRatesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
