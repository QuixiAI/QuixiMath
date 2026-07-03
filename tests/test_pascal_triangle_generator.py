import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pascal_triangle_generator import PascalTriangleGenerator
from helpers import DELIM


def oracle_answer(example):
    """Independently computes with math.comb from the text alone."""
    p = example["problem"]
    m = re.fullmatch(r"Build Pascal's triangle down to row (\d+) "
                     r"\(row 0 is 1\)\. Give row \1\.", p)
    if m:
        n = int(m.group(1))
        return ", ".join(str(math.comb(n, k)) for k in range(n + 1))
    m = re.fullmatch(r"Use Pascal's triangle to find (\d+)C(\d+) "
                     r"\(row 0 is 1\)\.", p)
    assert m, p
    return str(math.comb(int(m.group(1)), int(m.group(2))))


class TestPascalTriangleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PascalTriangleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: math.comb recomputes every answer."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_every_row_is_correct_and_built_by_addition(self):
        for _ in range(200):
            result = self.gen.generate()
            rows = {}
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "PASCAL_ROW":
                    rows[int(f[1])] = [int(v) for v in f[2].split(", ")]
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
            for r_num, entries in rows.items():
                self.assertEqual(entries,
                                 [math.comb(r_num, k)
                                  for k in range(r_num + 1)])
            # rows 0..n all present
            self.assertEqual(sorted(rows), list(range(max(rows) + 1)))

    def test_addition_count_matches_interior_entries(self):
        for _ in range(200):
            result = self.gen.generate()
            n = max(int(s.split(DELIM)[1]) for s in result["steps"]
                    if s.startswith(f"PASCAL_ROW{DELIM}"))
            adds = sum(1 for s in result["steps"]
                       if s.startswith(f"A{DELIM}"))
            # interior entries in rows 2..n: sum of (r - 1)
            self.assertEqual(adds, sum(r - 1 for r in range(2, n + 1)))

    def test_ncr_lookup_is_interior(self):
        gen = PascalTriangleGenerator("ncr")
        for _ in range(100):
            result = gen.generate()
            m = re.search(r"(\d+)C(\d+)", result["problem"])
            n, k = int(m.group(1)), int(m.group(2))
            self.assertTrue(1 <= k <= n - 1, result["problem"])

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"pascal_triangle_row",
                               "pascal_triangle_ncr"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PascalTriangleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
