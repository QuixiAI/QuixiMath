import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.polar_parametric_generator import PolarParametricGenerator
from helpers import DELIM


def exact_to_float(txt):
    """'2√3', '-√2', '5', '0' -> float."""
    t = txt.strip()
    sign = -1.0 if t.startswith("-") else 1.0
    t = t.lstrip("-")
    m = re.fullmatch(r"(\d*)√(\d+)", t)
    if m:
        return sign * int(m.group(1) or 1) * math.sqrt(int(m.group(2)))
    return sign * float(t)


def eq_residual(eq, x, y):
    """Residual of an equation string at (x, y)."""
    lhs, rhs = eq.split(" = ")
    s = f"({lhs}) - ({rhs})"
    s = s.replace("^", "**")
    s = re.sub(r"(\d)([xy(])", r"\1*\2", s)
    s = re.sub(r"\)\(", ")*(", s)
    return eval(s, {"x": x, "y": y})


def oracle_check(example):
    p = example["problem"]
    a = example["final_answer"]
    m = re.fullmatch(r"Convert the polar point \((\d+), (\d+)°\) to "
                     r"rectangular coordinates\. Give exact values\.", p)
    if m:
        r, th = int(m.group(1)), math.radians(int(m.group(2)))
        xs, ys = a.strip("()").split(", ")
        return (abs(exact_to_float(xs) - r * math.cos(th)) < 1e-9 and
                abs(exact_to_float(ys) - r * math.sin(th)) < 1e-9)
    m = re.fullmatch(r"Convert the point \((-?\d+), (-?\d+)\) to polar "
                     r"coordinates.*", p)
    if m:
        x, y = int(m.group(1)), int(m.group(2))
        rs, ths = a.strip("()").split(", ")
        r = exact_to_float(rs)
        th = math.radians(float(ths.rstrip("°")))
        return (abs(r * math.cos(th) - x) < 1e-9 and
                abs(r * math.sin(th) - y) < 1e-9)
    m = re.fullmatch(r"Convert the polar equation r = (\d+)( cos θ)? to "
                     r"rectangular form\.", p)
    if m:
        k = int(m.group(1))
        for t in (0.3, 0.8, 1.9, 2.6):
            r = k * math.cos(t) if m.group(2) else k
            x, y = r * math.cos(t), r * math.sin(t)
            if abs(eq_residual(a, x, y)) > 1e-9:
                return False
        return True
    m = re.fullmatch(r"Eliminate the parameter: x = (.+), y = (.+)\.", p)
    assert m, p
    xd, yd = m.group(1), m.group(2)
    mm = re.fullmatch(r"(\d+) cos t", xd)
    if mm:
        k = int(mm.group(1))
        for t in (0.4, 1.3, 2.8):
            if abs(eq_residual(a, k * math.cos(t),
                               k * math.sin(t))) > 1e-9:
                return False
        return True
    mx = re.fullmatch(r"t ([+-]) (\d+)", xd)
    my = re.fullmatch(r"(-?\d+)t(?: ([+-]) (\d+))?", yd)
    xa = int(mx.group(2)) * (1 if mx.group(1) == "+" else -1)
    b = int(my.group(1))
    c = int(my.group(3) or 0) * (1 if (my.group(2) or "+") == "+" else -1)
    for t in (-2, 0, 3):
        x = t + xa
        y = b * t + c
        if abs(eq_residual(a, x, y)) > 1e-9:
            return False
    return True


class TestPolarParametricGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PolarParametricGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_verification(self):
        """A9 oracle: every conversion verified numerically."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_polar_points_use_table_lookups(self):
        gen = PolarParametricGenerator("polar_point")
        for _ in range(100):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("TABLE_LOOKUP"), 2)

    def test_cos_circle_completes_square(self):
        gen = PolarParametricGenerator("polar_equation")
        found = False
        for _ in range(100):
            result = gen.generate()
            if "cos" in result["problem"]:
                found = True
                ops = [s.split(DELIM)[0] for s in result["steps"]]
                self.assertIn("COMPLETE_SQUARE", ops)
        self.assertTrue(found)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PolarParametricGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
