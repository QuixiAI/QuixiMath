import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.radical_multiply_generator import (
    RadicalMultiplyGenerator,
    rad,
    split_square,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently multiplies and simplifies from the problem text."""
    expr = example["problem"].split(": ", 1)[1]

    m = re.fullmatch(r"\((\d*)√(\d+)\)\^2", expr)
    if m:  # square
        a = int(m.group(1) or 1)
        return str(a * a * int(m.group(2)))

    m = re.fullmatch(r"√(\d+)\((\d+) \+ (\d+)√(\d+)\)", expr)
    if m:  # distribute (shared radical by construction)
        root, b, c, root2 = (int(v) for v in m.groups())
        assert root == root2
        return f"{c * root} + {rad(b, root)}"

    m = re.fullmatch(r"\((\d+) \+ √(\d+)\)\((\d+) \+ √(\d+)\)", expr)
    if m:  # binomial
        a, r1, b, r2 = (int(v) for v in m.groups())
        assert r1 == r2
        return f"{a * b + r1} + {rad(a + b, r1)}"

    m = re.fullmatch(r"(\d*)√(\d+) · (\d*)√(\d+)", expr)
    assert m, expr
    a = int(m.group(1) or 1)
    mm = int(m.group(2))
    b = int(m.group(3) or 1)
    nn = int(m.group(4))
    s, f = split_square(mm * nn)
    return rad(a * b * s, f)


class TestRadicalMultiplyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadicalMultiplyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "radical_multiply")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: multiply and simplify independently; the radicand in
        the answer must be square-free."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])
            m = re.search(r"√(\d+)", result["final_answer"])
            if m:
                s, _ = split_square(int(m.group(1)))
                self.assertEqual(s, 1, "answer radicand not square-free")

    def test_numeric_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M" and f[1].isdigit() and f[2].isdigit():
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "SQUARE_FACTOR":
                    mm = re.fullmatch(r"(\d+) × (\d+)", f[2])
                    self.assertEqual(int(mm.group(1)) * int(mm.group(2)),
                                     int(f[1]), s)

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            p = self.gen.generate()["problem"]
            if ")^2" in p:
                kinds.add("square")
            elif p.count("(") == 2:
                kinds.add("binomial")
            elif "(" in p:
                kinds.add("distribute")
            else:
                kinds.add("product")
        self.assertEqual(kinds, {"square", "binomial", "distribute",
                                 "product"})

    def test_fixed_variant_constructor(self):
        gen = RadicalMultiplyGenerator("square")
        for _ in range(10):
            self.assertIn(")^2", gen.generate()["problem"])
        with self.assertRaises(ValueError):
            RadicalMultiplyGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
