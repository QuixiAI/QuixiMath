import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hypercube_counting_generator import (
    HypercubeCountingGenerator,
)
from generators.geometric_mean_generator import sqrt_txt
from helpers import DELIM

PIECE_K = {"vertices": 0, "edges": 1, "square faces": 2,
           "cubic cells": 3}


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"How many (.+) does a (\d+)-dimensional hypercube "
                     r"have\?", p)
    if m:
        k, n = PIECE_K[m.group(1)], int(m.group(2))
        return str(math.comb(n, k) * 2 ** (n - k))
    m = re.fullmatch(r"Find the distance between P\((.+)\) and "
                     r"Q\((.+)\) in 4-dimensional space\.", p)
    if m:
        pv = [int(v) for v in m.group(1).split(", ")]
        qv = [int(v) for v in m.group(2).split(", ")]
        total = sum((qv[i] - pv[i]) ** 2 for i in range(4))
        return f"d = {sqrt_txt(total)}"
    m = re.fullmatch(r"Find the length of the main diagonal of a "
                     r"(\d+)-dimensional cube with side length (\d+)\. "
                     r"Give an exact answer\.", p)
    assert m, p
    n, s = int(m.group(1)), int(m.group(2))
    r = math.isqrt(n)
    return str(s * r) if r * r == n else f"{s}√{n}"


class TestHypercubeCountingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HypercubeCountingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: math.comb counts and exact 4D distances."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_tesseract_sanity(self):
        """The 4-cube: 16 vertices, 32 edges, 24 squares, 8 cells."""
        expected = {0: 16, 1: 32, 2: 24, 3: 8}
        for k, want in expected.items():
            self.assertEqual(math.comb(4, k) * 2 ** (4 - k), want)

    def test_ncr_steps_correct(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "NCR":
                    m = re.fullmatch(r"C\((\d+),(\d+)\)", f[1])
                    self.assertEqual(
                        math.comb(int(m.group(1)), int(m.group(2))),
                        int(f[2]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_4d_diagonal_is_rational(self):
        gen = HypercubeCountingGenerator("diagonal")
        for _ in range(100):
            result = gen.generate()
            if "a 4-dimensional cube" in result["problem"]:
                self.assertNotIn("√", result["final_answer"],
                                 result["problem"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)


if __name__ == "__main__":
    unittest.main()
