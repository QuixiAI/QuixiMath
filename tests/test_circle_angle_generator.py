import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.circle_angle_generator import CircleAngleGenerator
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"A central angle of (\d+)° and an inscribed angle "
                     r"subtend the same arc\. Find the inscribed angle\.",
                     p)
    if m:
        return f"{int(m.group(1)) // 2}°"
    m = re.fullmatch(r"An inscribed angle measures (\d+)°\. Find the "
                     r"central angle subtending the same arc\.", p)
    if m:
        return f"{2 * int(m.group(1))}°"
    m = re.fullmatch(r"An inscribed angle measures (\d+)°\. Find the "
                     r"measure of its intercepted arc\.", p)
    if m:
        return f"{2 * int(m.group(1))}°"
    m = re.fullmatch(r"A triangle is inscribed in a circle with one side "
                     r"a diameter\. One of its acute angles measures "
                     r"(\d+)°\. Find the other acute angle\.", p)
    assert m, p
    return f"{90 - int(m.group(1))}°"


class TestCircleAngleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CircleAngleGenerator()

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

    def test_theorem_always_cited(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
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
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)


if __name__ == "__main__":
    unittest.main()
