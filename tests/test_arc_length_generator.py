import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.arc_length_generator import ArcLengthGenerator
from helpers import DELIM


def to_py(expr):
    s = expr
    s = re.sub(r"e\^\((-?\w+)\)", r"math.exp(\1)", s)
    s = re.sub(r"e\^(-?\w+)", r"math.exp(\1)", s)
    s = re.sub(r"\be\b", "math.e", s)
    s = s.replace("^", "**")
    s = re.sub(r"(\d)x", r"\1*x", s)
    s = re.sub(r"\)x", ")*x", s)
    return s


def answer_value(ans):
    if re.fullmatch(r"-?\d+(/\d+)?", ans):
        return float(Fraction(ans))
    return eval(to_py(ans), {"math": math})


def oracle_check(example):
    """A9 oracle: polyline length of the curve from the problem."""
    m = re.fullmatch(r"Find the arc length of y = (.+) on "
                     r"\[(-?\d+), (-?\d+)\]\.", example["problem"])
    f = eval("lambda x: " + to_py(m.group(1)), {"math": math})
    a, b = int(m.group(2)), int(m.group(3))
    n = 4000
    total = 0.0
    for i in range(n):
        x1 = a + (b - a) * i / n
        x2 = a + (b - a) * (i + 1) / n
        total += math.hypot(x2 - x1, f(x2) - f(x1))
    want = answer_value(example["final_answer"])
    return abs(total - want) < 1e-3 * max(1.0, want)


class TestArcLengthGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ArcLengthGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_polyline_length(self):
        """A9 oracle: numeric polyline length matches every answer."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_formula_and_speed_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"ARCLEN_FORMULA{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"INTEG_SETUP{DELIM}")
                                for s in result["steps"]))

    def test_classic_17_12(self):
        """The textbook 17/12 case must be reproducible."""
        gen = ArcLengthGenerator("cubic_reciprocal")
        seen = set()
        for _ in range(300):
            r = gen.generate()
            if "x^3/6" in r["problem"] and "[1, 2]" in r["problem"]:
                seen.add(r["final_answer"])
        self.assertEqual(seen, {"17/12"})

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1x", "--", r"\+ -", r"/1x", r"\^1\b"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ArcLengthGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
