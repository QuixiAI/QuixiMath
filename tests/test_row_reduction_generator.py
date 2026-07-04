import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.row_reduction_generator import RowReductionGenerator
from helpers import DELIM


def solve(aug):
    """Independent Fraction Gaussian elimination with pivoting."""
    n = len(aug)
    m = [[Fraction(v) for v in row] for row in aug]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        m[col] = [v / m[col][col] for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [m[r][t] - f * m[col][t] for t in range(n + 1)]
    return [m[i][n] for i in range(n)]


def oracle_answer(example):
    mm = re.search(r"augmented matrix (\[\[.+\]\])",
                   example["problem"])
    aug = ast.literal_eval(mm.group(1))
    sol = solve(aug)
    names = ["x", "y", "z"][:len(aug)]
    assert all(v.denominator == 1 for v in sol)
    return ", ".join(f"{nm} = {v.numerator}"
                     for nm, v in zip(names, sol))


class TestRowReductionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RowReductionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: independent Fraction Gaussian elimination."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_row_ops_are_integer_and_correct_count(self):
        for _ in range(200):
            result = self.gen.generate()
            n = 3 if "z = " in result["final_answer"] else 2
            row_ops = [s for s in result["steps"]
                       if s.startswith(f"ROW_OP{DELIM}")]
            self.assertEqual(len(row_ops), n * (n - 1) // 2)
            for s in row_ops:
                new_row = s.split(DELIM)[2]
                for v in new_row.strip("[]").split(", "):
                    int(v)  # raises if not integer

    def test_triangular_form_recorded(self):
        for _ in range(100):
            result = self.gen.generate()
            self.assertTrue(any("triangular form" in s
                                for s in result["steps"]))

    def test_back_substitution_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)

    def test_both_sizes_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"row_reduction_two",
                               "row_reduction_three"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RowReductionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
