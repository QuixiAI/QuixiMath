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
    m = re.search(r"The radius of a circle grows at (\d+) "
                  r"(cm|m|ft|in)/(s|min)\. How fast is the area increasing "
                  r"when the radius is (\d+) \2\? Give an exact answer\.$", p)
    if m:
        k, unit, time, r0 = (int(m.group(1)), m.group(2), m.group(3),
                             int(m.group(4)))
        return f"dA/dt = {2 * r0 * k}π {unit}²/{time}"
    m = re.search(r"A (\d+) (cm|m|ft|in) ladder leans against a wall\. The "
                  r"base slides away from the wall at (\d+) \2/(s|min)\. "
                  r"How fast is the top sliding down when the base is "
                  r"(\d+) \2 from the wall\?$", p)
    if m:
        L, unit, k, time, x0 = (int(m.group(1)), m.group(2),
                                 int(m.group(3)), m.group(4), int(m.group(5)))
        y2 = L * L - x0 * x0
        import math
        y0 = math.isqrt(y2)
        assert y0 * y0 == y2
        return f"dy/dt = {Fraction(-x0 * k, y0)} {unit}/{time}"
    m = re.search(r"Each edge of a cube grows at (\d+) "
                  r"(cm|m|ft|in)/(s|min)\. How fast is the volume increasing "
                  r"when the edge is (\d+) \2\?$", p)
    if m:
        k, unit, time, s0 = (int(m.group(1)), m.group(2), m.group(3),
                             int(m.group(4)))
        return f"dV/dt = {3 * s0 * s0 * k} {unit}³/{time}"
    m = re.search(r"Water pours into a conical tank \(radius equals half the "
                  r"depth\) at (\d+) (cm|m|ft|in)³/(s|min)\. How fast is the "
                  r"depth rising when the water is (\d+) \2 deep\? Give an "
                  r"exact answer\.$", p)
    assert m, p
    k, unit, time, h0 = (int(m.group(1)), m.group(2), m.group(3),
                          int(m.group(4)))
    rate = Fraction(4 * k, h0 * h0)
    rtxt = (f"{rate}/π" if rate.denominator == 1
            else f"{rate.numerator}/({rate.denominator}π)")
    return f"dh/dt = {rtxt} {unit}/{time}"


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
            m = re.search(r"= (-\d+(?:/\d+)?) (?:cm|m|ft|in)/(?:s|min)",
                          result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])

    def test_answers_have_units(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertRegex(result["final_answer"],
                             r"(cm|m|ft|in)(²|³)?/(s|min)$")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)

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
