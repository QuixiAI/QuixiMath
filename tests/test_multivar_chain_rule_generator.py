import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.multivar_chain_rule_generator import MultivarChainRuleGenerator
from helpers import DELIM


def exact(fr):
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d != 1:
        return str(fr)
    sign = "-" if fr < 0 else ""
    num = abs(fr.numerator)
    den = fr.denominator
    whole = num // den
    rem = num % den
    if rem == 0:
        return f"{sign}{whole}"
    digits = []
    while rem:
        rem *= 10
        digits.append(str(rem // den))
        rem %= den
    return f"{sign}{whole}.{''.join(digits)}"


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_poly(expr):
    terms = []
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
        terms.append((coeff, mx, ny))
    return terms


def partial_values(expr, x0, y0):
    fx = 0
    fy = 0
    for c, mx, ny in parse_poly(expr):
        if mx:
            fx += c * mx * (x0 ** (mx - 1)) * (y0 ** ny)
        if ny:
            fy += c * ny * (x0 ** mx) * (y0 ** (ny - 1))
    return fx, fy


def parse_linear_value(expr, values):
    total = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        value = 1
        for factor in raw.split("*"):
            if re.fullmatch(r"\d+", factor):
                coeff *= int(factor)
            elif factor in values:
                value *= values[factor]
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        total += coeff * value
    return total


def linear_coeff(expr, var):
    total = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        variables = []
        for factor in raw.split("*"):
            if re.fullmatch(r"\d+", factor):
                coeff *= int(factor)
            elif factor in {"s", "t"}:
                variables.append(factor)
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        if variables == [var]:
            total += coeff
    return total


def oracle_answer(example):
    problem = example["problem"]
    if "Find dz/dt" in problem:
        poly, x_expr, y_expr, t0 = re.fullmatch(
            r"Let z = f\(x,y\) = (.+), where x = (.+) and y = (.+)\. "
            r"Find dz/dt at t = (-?\d+)\.",
            problem,
        ).groups()
        t0 = int(t0)
        x0 = parse_linear_value(x_expr, {"t": t0})
        y0 = parse_linear_value(y_expr, {"t": t0})
        fx, fy = partial_values(poly, x0, y0)
        return str(fx * linear_coeff(x_expr, "t") +
                   fy * linear_coeff(y_expr, "t"))
    if "Find dz/ds" in problem:
        poly, x_expr, y_expr, s0, t0 = re.fullmatch(
            r"Let z = f\(x,y\) = (.+), where x = (.+) and y = (.+)\. "
            r"Find dz/ds at \(s, t\) = \((-?\d+), (-?\d+)\)\.",
            problem,
        ).groups()
        s0 = int(s0)
        t0 = int(t0)
        x0 = parse_linear_value(x_expr, {"s": s0, "t": t0})
        y0 = parse_linear_value(y_expr, {"s": s0, "t": t0})
        fx, fy = partial_values(poly, x0, y0)
        return str(fx * linear_coeff(x_expr, "s") +
                   fy * linear_coeff(y_expr, "s"))
    poly, x0, y0, dx, dy = re.fullmatch(
        r"For f\(x,y\) = (.+), estimate df at \((-?\d+), (-?\d+)\) "
        r"when dx = ([-\d/]+) and dy = ([-\d/]+)\.",
        problem,
    ).groups()
    fx, fy = partial_values(poly, int(x0), int(y0))
    return exact(Fraction(fx) * Fraction(dx) + Fraction(fy) * Fraction(dy))


def safe_eval_arith(expr):
    return Fraction(eval(expr, {"__builtins__": {}}, {}))


def parse_factor(text):
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return Fraction(text)


def eval_product_sum(expr):
    total = Fraction(0)
    for raw in expr.split(" + "):
        left, right = raw.split("*")
        total += parse_factor(left) * parse_factor(right)
    return total


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"CHAIN_VALUE", "EVAL_PARTIAL"}:
            if safe_eval_arith(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] in {"CHAIN_SUM", "DIFF_SUM"}:
            if eval_product_sum(parts[2]) != Fraction(parts[3]):
                return False
    return True


class TestMultivarChainRuleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MultivarChainRuleGenerator()

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

    def test_chain_variants_have_chain_sum(self):
        for variant in ("path_derivative", "partial_s"):
            gen = MultivarChainRuleGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"CHAIN_SUM{DELIM}")
                                    for s in result["steps"]))

    def test_total_diff_has_diff_sum(self):
        gen = MultivarChainRuleGenerator("total_diff")
        for _ in range(50):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"DIFF_SUM{DELIM}")
                                for s in result["steps"]))

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
            MultivarChainRuleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
