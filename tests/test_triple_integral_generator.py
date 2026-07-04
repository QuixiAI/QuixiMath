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

from generators.triple_integral_generator import TripleIntegralGenerator
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


def oracle_answer(example):
    problem = example["problem"]
    if "cylindrical" in problem:
        integrand, radius_sq, height = re.fullmatch(
            r"Convert to cylindrical and evaluate the triple integral "
            r"of (z|\d+\*z) over the solid x\^2 \+ y\^2 <= (\d+), "
            r"0 <= z <= (\d+)\.",
            problem,
        ).groups()
        coeff = 1 if integrand == "z" else int(integrand.split("*")[0])
        radius = math.isqrt(int(radius_sq))
        height = int(height)
        value = Fraction(coeff * height * height * radius * radius, 2)
        return f"value {fmt_pi(value)}"
    coeff, radius_sq = re.fullmatch(
        r"Convert to spherical and evaluate the triple integral of (\d+) "
        r"over the ball x\^2 \+ y\^2 \+ z\^2 <= (\d+)\.",
        problem,
    ).groups()
    coeff = int(coeff)
    radius = math.isqrt(int(radius_sq))
    value = Fraction(coeff * 4 * radius ** 3, 3)
    return f"value {fmt_pi(value)}"


def eval_fraction_expr(expr):
    expr = expr.replace("^", "**")
    expr = re.sub(r"\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def coeff_from_pi(text):
    if text == "pi":
        return Fraction(1)
    if text == "-pi":
        return Fraction(-1)
    return Fraction(text[:-3])


def eval_pi_product(expr):
    assert expr.endswith("*pi")
    expr = expr[:-3]
    total = Fraction(1)
    for factor in expr.split("*"):
        total *= Fraction(factor)
    return total


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"INNER_EVAL", "MIDDLE_EVAL"} and re.search(r"\d", parts[2]):
            if eval_fraction_expr(parts[2].split(" = ")[-1]) != Fraction(parts[3]):
                return False
        elif parts[0] == "TRIPLE_EVAL":
            if eval_pi_product(parts[2]) != coeff_from_pi(parts[3]):
                return False
    return True


class TestTripleIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TripleIntegralGenerator()

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
        cases = {
            "cylindrical": "Convert to cylindrical",
            "spherical": "Convert to spherical",
        }
        for variant, phrase in cases.items():
            gen = TripleIntegralGenerator(variant)
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
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            TripleIntegralGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
