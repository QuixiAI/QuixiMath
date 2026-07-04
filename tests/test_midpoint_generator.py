import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.midpoint_generator import MidpointGenerator
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Find the midpoint of the segment from "
                     r"\((-?\d+), (-?\d+)\) to \((-?\d+), (-?\d+)\)\.", p)
    if m:
        x1, y1, x2, y2 = (int(v) for v in m.groups())
        assert (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0
        return f"({(x1 + x2) // 2}, {(y1 + y2) // 2})"
    m = re.fullmatch(r"The midpoint of a segment is \((-?\d+), (-?\d+)\) "
                     r"and one endpoint is \((-?\d+), (-?\d+)\)\. Find "
                     r"the other endpoint\.", p)
    assert m, p
    mx, my, x1, y1 = (int(v) for v in m.groups())
    return f"({2 * mx - x1}, {2 * my - y1})"


class TestMidpointGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MidpointGenerator()

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

    def test_step_arithmetic(self):
        for _ in range(400):
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

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"midpoint_midpoint", "midpoint_endpoint"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            MidpointGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
