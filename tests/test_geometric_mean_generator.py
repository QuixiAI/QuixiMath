import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_mean_generator import (
    GeometricMeanGenerator,
    sqrt_txt,
)
from helpers import DELIM


def oracle_answer(example):
    """Reapplies the geometric mean relations from the text alone."""
    p_txt = example["problem"]
    m = re.fullmatch(r"In a right triangle, the altitude to the "
                     r"hypotenuse splits it into segments of length "
                     r"(\d+) and (\d+)\. Find the altitude h\.", p_txt)
    if m:
        p, q = int(m.group(1)), int(m.group(2))
        return f"h = {sqrt_txt(p * q)}"
    m = re.fullmatch(r"In a right triangle, the altitude to the "
                     r"hypotenuse splits it into segments p = (\d+) and "
                     r"q = (\d+)\. Find the leg adjacent to the segment "
                     r"of length \1\.", p_txt)
    if m:
        p, q = int(m.group(1)), int(m.group(2))
        return f"leg = {sqrt_txt(p * (p + q))}"
    m = re.fullmatch(r"The altitude to the hypotenuse of a right "
                     r"triangle has length (\d+), and it splits the "
                     r"hypotenuse into two segments, one of length "
                     r"(\d+)\. Find the other segment q\.", p_txt)
    assert m, p_txt
    h, p = int(m.group(1)), int(m.group(2))
    assert (h * h) % p == 0
    return f"q = {h * h // p}"


class TestGeometricMeanGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricMeanGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: reapply the relations independently."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_radicals_are_fully_simplified(self):
        for _ in range(400):
            result = self.gen.generate()
            m = re.search(r"(?:(\d+))?√(\d+)", result["final_answer"])
            if m:
                inside = int(m.group(2))
                for f in range(2, int(math.isqrt(inside)) + 1):
                    self.assertNotEqual(inside % (f * f), 0,
                                        result["final_answer"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_integer_and_radical_answers_occur(self):
        kinds = set()
        for _ in range(200):
            kinds.add("√" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"geometric_mean_altitude",
                               "geometric_mean_leg",
                               "geometric_mean_find_segment"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricMeanGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
