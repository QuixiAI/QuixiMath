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

from generators.parametric_calculus_generator import (
    ParametricCalculusGenerator,
)
from helpers import DELIM


def to_t(expr):
    s = expr.replace("^", "**")
    return eval("lambda t: " + re.sub(r"(\d)t", r"\1*t", s))


def pi_val(s):
    m = re.fullmatch(r"(-?\d*)π(?:/(\d+))?", s)
    if not m:
        return None
    head = m.group(1)
    num = -1 if head == "-" else 1 if head == "" else int(head)
    return num * math.pi / int(m.group(2) or 1)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    h = 1e-6
    m = re.fullmatch(r"A curve is given by x = (.+), y = (.+)\. "
                     r"Find dy/dx at t = (-?\d+)\.", p)
    if m:
        fx, fy = to_t(m.group(1)), to_t(m.group(2))
        t0 = int(m.group(3))
        dx = (fx(t0 + h) - fx(t0 - h)) / (2 * h)
        dy = (fy(t0 + h) - fy(t0 - h)) / (2 * h)
        return abs(dy / dx - float(Fraction(ans))) < 1e-4
    m = re.fullmatch(r"Find the arc length of the curve x = (.+), "
                     r"y = (.+) for (\d+) ≤ t ≤ (\d+)\.", p)
    if m:
        fx, fy = to_t(m.group(1)), to_t(m.group(2))
        s, T = int(m.group(3)), int(m.group(4))
        n = 4000
        length = 0.0
        for i in range(n):
            t1 = s + (T - s) * i / n
            t2 = s + (T - s) * (i + 1) / n
            length += math.hypot(fx(t2) - fx(t1), fy(t2) - fy(t1))
        return abs(length - int(ans)) < 1e-3 * max(1, int(ans))
    m = re.fullmatch(r"Find the area swept by the polar curve r = (\d+) "
                     r"for 0 ≤ θ ≤ (\S+)\.", p)
    if m:
        a, th = int(m.group(1)), pi_val(m.group(2))
        return abs(0.5 * a * a * th - pi_val(ans)) < 1e-9
    m = re.fullmatch(r"Find the area enclosed by the polar curve "
                     r"r = (\d+)cos\(θ\) for -π/2 ≤ θ ≤ π/2\.", p)
    assert m, p
    c = int(m.group(1))
    n = 4000
    total = 0.0
    for i in range(n):
        th = -math.pi / 2 + math.pi * (i + 0.5) / n
        total += 0.5 * (c * math.cos(th)) ** 2 * (math.pi / n)
    return abs(total - pi_val(ans)) < 1e-4


class TestParametricCalculusGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ParametricCalculusGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: numeric slope/length/area recomputation."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_formula_steps_present(self):
        for v, code in (("arc_length", "ARCLEN_FORMULA"),
                        ("polar_sector", "POLAR_AREA_FORMULA"),
                        ("polar_circle", "POLAR_AREA_FORMULA"),
                        ("dydx", "THEOREM")):
            gen = ParametricCalculusGenerator(v)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"{code}{DELIM}")
                                    for s in result["steps"]))

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1t", r"(?<!\d)1cos", r"(?<!\d)1θ",
                        r"(?<!\d)1\(", "--", r"\+ -", r"\^1\b"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ParametricCalculusGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
