import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hessian_classify_generator import HessianClassifyGenerator
from helpers import DELIM


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_poly(expr):
    coeffs = {}
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        mx = 0
        ny = 0
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor == "x":
                mx += 1
            elif factor == "y":
                ny += 1
            elif factor == "x^2":
                mx += 2
            elif factor == "y^2":
                ny += 2
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        coeffs[(mx, ny)] = coeffs.get((mx, ny), 0) + coeff
    return coeffs


def coefficients(expr):
    coeffs = parse_poly(expr)
    return (
        coeffs.get((2, 0), 0),
        coeffs.get((0, 2), 0),
        coeffs.get((1, 1), 0),
        coeffs.get((1, 0), 0),
        coeffs.get((0, 1), 0),
    )


def classify(det, f_xx):
    if det < 0:
        return "saddle point"
    return "local minimum" if f_xx > 0 else "local maximum"


def solve_from_poly(expr):
    a, b, c, d, e = coefficients(expr)
    f_xx = 2 * a
    f_xy = c
    f_yy = 2 * b
    det = f_xx * f_yy - f_xy * f_xy
    rhs_x = -d
    rhs_y = -e
    x0 = Fraction(rhs_x * f_yy - f_xy * rhs_y, det)
    y0 = Fraction(f_xx * rhs_y - rhs_x * f_xy, det)
    return x0, y0, det, f_xx, f_xy, f_yy


def oracle_answer(example):
    problem = example["problem"]
    expr = re.fullmatch(
        r"For f\(x,y\) = (.+), find the critical point and classify "
        r"it using the Hessian test\.",
        problem,
    ).group(1)
    x0, y0, det, f_xx, _, _ = solve_from_poly(expr)
    assert x0.denominator == 1 and y0.denominator == 1
    return (f"critical point ({x0.numerator}, {y0.numerator}): "
            f"{classify(det, f_xx)}")


def parse_factor(text):
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return Fraction(text)


def eval_det_expr(expr):
    left, square = expr.split(" - ")
    a, b = left.split("*")
    return parse_factor(a) * parse_factor(b) - parse_factor(square[:-2]) ** 2


def eval_ratio(expr):
    top, bottom = expr.split("/")
    return parse_factor(top) / parse_factor(bottom)


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"CRIT_SOLVE", "HESSIAN_DET"}:
            if parts[1] in {"det", "D = f_xx*f_yy - f_xy^2"}:
                if eval_det_expr(parts[2]) != Fraction(parts[3]):
                    return False
            elif parts[1] in {"x", "y"}:
                if eval_ratio(parts[2]) != Fraction(parts[3]):
                    return False
        elif parts[0] == "HESSIAN_TEST":
            det = int(parts[1].split(" = ")[1])
            f_xx = int(parts[2].split(" = ")[1])
            if classify(det, f_xx) != parts[3]:
                return False
        elif parts[0] == "CHECK" and parts[3] != "critical point":
            return False
    return True


class TestHessianClassifyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HessianClassifyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_each_variant_classification(self):
        expected = {
            "local_min": "local minimum",
            "local_max": "local maximum",
            "saddle": "saddle point",
        }
        for variant, label in expected.items():
            gen = HessianClassifyGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(label, result["final_answer"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            HessianClassifyGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
