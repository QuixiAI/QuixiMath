import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.radical_variable_simplify_generator import (
    RadicalVariableSimplifyGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently simplifies the radical from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)
    m = re.fullmatch(rf"√\((\d*){var}(?:\^(\d+))?\)", expr)
    assert m, expr
    n = int(m.group(1) or 1)
    p = int(m.group(2) or 1)

    s = 1
    for cand in range(1, int(n ** 0.5) + 1):
        if n % (cand * cand) == 0:
            s = cand
    f = n // (s * s)
    k, rem = divmod(p, 2)

    if k == 0:
        outside = str(s)
    elif k == 1:
        outside = f"{s}{var}" if s > 1 else var
    else:
        outside = f"{s}{var}^{k}" if s > 1 else f"{var}^{k}"
    if rem == 0:
        inside = f"√{f}"
    elif f == 1:
        inside = f"√{var}"
    else:
        inside = f"√({f}{var})"
    return inside if (s == 1 and k == 0) else f"{outside}{inside}"


class TestRadicalVariableSimplifyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadicalVariableSimplifyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "simplify_radical_variables")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_simplification(self):
        """A9 oracle: re-simplify from the problem text; the answer must be
        maximal (square-free radicand, largest square pulled out)."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_square_factor_and_root_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "SQUARE_FACTOR" and f[1].isdigit():
                    m = re.fullmatch(r"(\d+) × (\d+)", f[2])
                    self.assertIsNotNone(m, s)
                    self.assertEqual(int(m.group(1)) * int(m.group(2)),
                                     int(f[1]), s)
                    self.assertEqual(m.group(1), f[3], s)
                    r = int(int(f[3]) ** 0.5)
                    self.assertEqual(r * r, int(f[3]), s)
                elif f[0] == "ROOT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)

    def test_check_squares_back_to_radicand(self):
        for _ in range(300):
            result = self.gen.generate()
            radicand = re.search(r"√\((.+)\)",
                                 result["problem"]).group(1)
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            f = check.split(DELIM)
            self.assertTrue(f[2].endswith(f"= {radicand}"), check)
            self.assertEqual(f[3], radicand, check)

    def test_variable_always_present_and_radical_always_remains(self):
        for _ in range(200):
            result = self.gen.generate()
            var = next(v for v in "xyn" if v in result["problem"])
            self.assertIn(var, result["problem"])
            self.assertIn("√", result["final_answer"])


if __name__ == "__main__":
    unittest.main()
