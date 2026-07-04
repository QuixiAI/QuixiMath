import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.segment_partition_generator import SegmentPartitionGenerator
from helpers import DELIM


def oracle_answer(example):
    m = re.fullmatch(r"Point P divides the segment from "
                     r"A\((-?\d+), (-?\d+)\) to B\((-?\d+), (-?\d+)\) in "
                     r"the ratio (\d+):(\d+) \(measured from A\)\. "
                     r"Find P\.", example["problem"])
    assert m, example["problem"]
    x1, y1, x2, y2, mm, nn = (int(v) for v in m.groups())
    t = Fraction(mm, mm + nn)
    px = x1 + t * (x2 - x1)
    py = y1 + t * (y2 - y1)
    assert px.denominator == 1 and py.denominator == 1
    return f"({px.numerator}, {py.numerator})"


class TestSegmentPartitionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SegmentPartitionGenerator()

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

    def test_point_lies_between_endpoints(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.search(r"A\((-?\d+), (-?\d+)\) to B\((-?\d+), (-?\d+)\)",
                          result["problem"])
            x1, y1, x2, y2 = (int(v) for v in m.groups())
            px, py = (int(v) for v in
                      re.findall(r"-?\d+", result["final_answer"]))
            self.assertTrue(min(x1, x2) < px < max(x1, x2) or x1 == x2)
            self.assertTrue(min(y1, y2) < py < max(y1, y2) or y1 == y2)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)


if __name__ == "__main__":
    unittest.main()
