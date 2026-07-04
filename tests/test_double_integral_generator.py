import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.double_integral_generator import DoubleIntegralGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_pi(coeff):
    coeff = Fraction(coeff)
    if coeff == 1:
        return "pi"
    if coeff == -1:
        return "-pi"
    return f"{fmt_frac(coeff)}*pi"


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear(expr):
    coeffs = {"x": 0, "y": 0}
    const = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        var = None
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor in coeffs:
                var = factor
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        if var is None:
            const += coeff
        else:
            coeffs[var] += coeff
    return coeffs["x"], coeffs["y"], const


def oracle_answer(example):
    problem = example["problem"]
    if problem.startswith("Evaluate"):
        a, b, c, d, integrand = re.fullmatch(
            r"Evaluate the iterated integral int_x=(\d+)\.\.(\d+) "
            r"int_y=(\d+)\.\.(\d+) \((.+)\) dy dx\.",
            problem,
        ).groups()
        a, b, c, d = map(int, (a, b, c, d))
        p, q, r = parse_linear(integrand)
        value = (
            Fraction(p * (b * b - a * a) * (d - c), 2) +
            Fraction(q * (d * d - c * c) * (b - a), 2) +
            Fraction(r * (b - a) * (d - c))
        )
        return f"value {fmt_frac(value)}"
    if problem.startswith("Reverse"):
        width, slope, const = re.fullmatch(
            r"Reverse the order and evaluate int_x=0\.\.(\d+) "
            r"int_y=0\.\.(\d+)\*x (\d+) dy dx\.",
            problem,
        ).groups()
        width = int(width)
        slope = int(slope)
        const = int(const)
        height = slope * width
        value = Fraction(const * slope * width * width, 2)
        return (f"reversed y:0..{height}, x:y/{slope}..{width}; "
                f"value {fmt_frac(value)}")

    region, radius_sq = re.fullmatch(
        r"Convert to polar and evaluate the double integral of x\^2 \+ "
        r"y\^2 over the (first-quadrant|upper-half|full) disk "
        r"x\^2 \+ y\^2 <= (\d+)\.",
        problem,
    ).groups()
    angle = {
        "first-quadrant": Fraction(1, 2),
        "upper-half": Fraction(1),
        "full": Fraction(2),
    }[region]
    radius_sq = int(radius_sq)
    radius_fourth = radius_sq * radius_sq
    value = angle * Fraction(radius_fourth, 4)
    return f"value {fmt_pi(value)}"


def eval_fraction_expr(expr):
    expr = expr.replace("^", "**")
    expr = re.sub(r"\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "OUTER_EVAL":
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "INNER_EVAL" and parts[1].startswith("r="):
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
    return True


class TestDoubleIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DoubleIntegralGenerator()

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

    def test_variant_markers(self):
        expected = {
            "rectangle_iterated": "Evaluate the iterated",
            "reverse_triangle": "Reverse the order",
            "polar_sector": "Convert to polar",
        }
        for variant, phrase in expected.items():
            gen = DoubleIntegralGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertIn(phrase, result["problem"])

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
            DoubleIntegralGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
