import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.special_right_triangle_generator import (
    SpecialRightTriangleGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"A 45-45-90 triangle has legs of length (\d+)\. "
                     r"Find the hypotenuse\. Give an exact answer\.", p)
    if m:
        return f"{m.group(1)}√2"
    m = re.fullmatch(r"A 45-45-90 triangle has hypotenuse (\d+)\. Find "
                     r"the length of each leg\. Give an exact answer\.",
                     p)
    if m:
        h = int(m.group(1))
        assert h % 2 == 0
        return f"{h // 2}√2"
    m = re.fullmatch(r"The shorter leg of a 30-60-90 triangle is "
                     r"(\d+)\. Find the longer leg and the hypotenuse\. "
                     r"Give exact answers\.", p)
    if m:
        s = int(m.group(1))
        return f"longer leg = {s}√3; hypotenuse = {2 * s}"
    m = re.fullmatch(r"The hypotenuse of a 30-60-90 triangle is (\d+)\. "
                     r"Find both legs\. Give exact answers\.", p)
    if m:
        h = int(m.group(1))
        assert h % 2 == 0
        return f"shorter leg = {h // 2}; longer leg = {h // 2}√3"
    m = re.fullmatch(r"The longer leg of a 30-60-90 triangle is "
                     r"(\d+)√3\. Find the shorter leg and the "
                     r"hypotenuse\. Give exact answers\.", p)
    assert m, p
    k = int(m.group(1))
    return f"shorter leg = {k}; hypotenuse = {2 * k}"


class TestSpecialRightTriangleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SpecialRightTriangleGenerator()

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

    def test_ratios_always_cited(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
                                for s in result["steps"]))

    def test_rationalize_appears_for_45_hyp(self):
        gen = SpecialRightTriangleGenerator("45_from_hyp")
        for _ in range(50):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"RATIONALIZE{DELIM}")
                                for s in result["steps"]))

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SpecialRightTriangleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
