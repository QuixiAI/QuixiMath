import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.nets_surface_area_generator import NetsSurfaceAreaGenerator
from helpers import DELIM


def oracle_answer(example):
    """Recomputes total surface area from the face list alone."""
    m = re.fullmatch(r"A net consists of: (.+)\. All lengths are in the "
                     r"same unit\. Find the total surface area\.",
                     example["problem"])
    assert m, example["problem"]
    faces = m.group(1)

    mm = re.fullmatch(r"6 squares (\d+) by \1", faces)
    if mm:
        s = int(mm.group(1))
        return f"{6 * s * s} square units"
    mm = re.fullmatch(r"2 rectangles (\d+) by (\d+); 2 rectangles "
                      r"(\d+) by (\d+); 2 rectangles (\d+) by (\d+)",
                      faces)
    if mm:
        v = [int(x) for x in mm.groups()]
        total = 2 * (v[0] * v[1] + v[2] * v[3] + v[4] * v[5])
        return f"{total} square units"
    mm = re.fullmatch(r"2 right triangles with legs (\d+) and (\d+); "
                      r"rectangles (\d+) by (\d+), (\d+) by \4, and "
                      r"(\d+) by \4", faces)
    if mm:
        a, b = int(mm.group(1)), int(mm.group(2))
        L = int(mm.group(4))
        s1, s2, s3 = int(mm.group(3)), int(mm.group(5)), int(mm.group(6))
        total = a * b + (s1 + s2 + s3) * L
        return f"{total} square units"
    mm = re.fullmatch(r"1 square (\d+) by \1; 4 triangles with base \1 "
                      r"and height (\d+)", faces)
    assert mm, faces
    s, slant = int(mm.group(1)), int(mm.group(2))
    return f"{s * s + 2 * s * slant} square units"


class TestNetsSurfaceAreaGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = NetsSurfaceAreaGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute the surface area from the face list."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            p = self.gen.generate()["problem"]
            if "6 squares" in p:
                kinds.add("cube")
            elif "2 rectangles" in p:
                kinds.add("rect")
            elif "right triangles" in p:
                kinds.add("tri")
            else:
                kinds.add("pyr")
        self.assertEqual(kinds, {"cube", "rect", "tri", "pyr"})


if __name__ == "__main__":
    unittest.main()
