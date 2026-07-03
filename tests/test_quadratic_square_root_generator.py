import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quadratic_square_root_generator import (
    QuadraticSquareRootGenerator,
    SQUARE_FREE,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently solves the equation from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)

    m = re.fullmatch(rf"\({var} ([+-]) (\d+)\)\^2 = (\d+)", expr)
    if m:  # shifted
        h = int(m.group(2)) * (-1 if m.group(1) == "+" else 1)
        k = int(m.group(3))
        r = int(k ** 0.5)
        assert r * r == k
        lo, hi = sorted((h - r, h + r))
        return f"{var} = {lo} or {var} = {hi}"

    m = re.fullmatch(rf"(\d*){var}\^2 = (\d+)", expr)
    if not m:
        m2 = re.fullmatch(rf"(\d+){var}\^2 - (\d+) = 0", expr)
        assert m2, expr
        a, rhs = int(m2.group(1)), int(m2.group(2))
    else:
        a, rhs = int(m.group(1) or 1), int(m.group(2))
    assert rhs % a == 0
    k = rhs // a
    r = int(k ** 0.5)
    if r * r == k:
        return f"{var} = {-r} or {var} = {r}"
    assert k in SQUARE_FREE, k
    return f"{var} = -√{k} or {var} = √{k}"


class TestQuadraticSquareRootGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuadraticSquareRootGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "quadratic_by_square_roots")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve from the problem text; answers ascending."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_plus_minus_and_root_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            codes = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertIn("SQRT_BOTH_SIDES", codes)
            self.assertIn("PLUS_MINUS", codes)
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "ROOT":
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)
                elif f[0] == "PLUS_MINUS":
                    self.assertIn("±", f[1], s)
                    self.assertIn(" or ", f[2], s)
                elif f[0] == "CHECK":
                    lhs_val = f[2].rsplit("= ", 1)[1]
                    self.assertEqual(lhs_val, f[3], s)

    def test_check_substitutions_true(self):
        """Integer-case CHECK works must be arithmetically true."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "CHECK" or "√" in f[2]:
                    continue
                m = re.fullmatch(
                    r"\(?\(?(-?\d+)\)?(?: ([+-]) (\d+))?\)?\^2 = (\d+)", f[2])
                self.assertIsNotNone(m, s)
                base = int(m.group(1))
                if m.group(2):
                    off = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
                    base += off
                self.assertEqual(base * base, int(m.group(4)), s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            result = self.gen.generate()
            p = result["problem"]
            if "√" in result["final_answer"]:
                kinds.add("irrational")
            elif "(" in p:
                kinds.add("shifted")
            elif re.search(r"\d[xyn]\^2", p):
                kinds.add("scaled")
            else:
                kinds.add("simple")
        self.assertEqual(kinds, {"irrational", "shifted", "scaled", "simple"})

    def test_fixed_variant_constructor(self):
        gen = QuadraticSquareRootGenerator("shifted")
        for _ in range(10):
            self.assertIn("(", gen.generate()["problem"])
        with self.assertRaises(ValueError):
            QuadraticSquareRootGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
