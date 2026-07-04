import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gradient_generator import GradientGenerator, exact
from helpers import DELIM


def parse_terms(expr):
    expr = expr.replace(" - ", " + -")
    terms = []
    for raw in expr.split(" + "):
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


def values(expr, x0, y0):
    fx = 0
    fy = 0
    z = 0
    for c, mx, ny in parse_terms(expr):
        z += c * (x0 ** mx) * (y0 ** ny)
        if mx:
            fx += c * mx * (x0 ** (mx - 1)) * (y0 ** ny)
        if ny:
            fy += c * ny * (x0 ** mx) * (y0 ** (ny - 1))
    return fx, fy, z


def fmt_plane(z0, fx, fy, x0, y0):
    pieces = [f"z = {z0}"]
    for coeff, body in ((fx, f"(x - {x0})"), (fy, f"(y - {y0})")):
        if coeff == 0:
            continue
        term = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        pieces.append(("+ " if coeff > 0 else "- ") + term)
    return " ".join(pieces)


def oracle_answer(example):
    problem = example["problem"]
    if "directional derivative" in problem:
        expr, x0, y0, ux, uy = re.fullmatch(
            r"For f\(x,y\) = (.+), find the directional derivative at "
            r"\((\d+), (\d+)\) in direction u = \(([-\d/]+), ([-\d/]+)\)\.",
            problem,
        ).groups()
        fx, fy, _ = values(expr, int(x0), int(y0))
        return exact(Fraction(fx) * Fraction(ux) + Fraction(fy) * Fraction(uy))
    if "tangent plane" in problem:
        expr, x0, y0 = re.fullmatch(
            r"Find the tangent plane to z = f\(x,y\) for f\(x,y\) = "
            r"(.+) at \((\d+), (\d+)\)\.",
            problem,
        ).groups()
        x0 = int(x0)
        y0 = int(y0)
        fx, fy, z0 = values(expr, x0, y0)
        return fmt_plane(z0, fx, fy, x0, y0)
    expr, x0, y0 = re.fullmatch(
        r"For f\(x,y\) = (.+), find grad f at \((\d+), (\d+)\)\.",
        problem,
    ).groups()
    fx, fy, _ = values(expr, int(x0), int(y0))
    return f"({fx}, {fy})"


def safe_eval_arith(expr):
    self = None
    del self
    return Fraction(eval(expr, {"__builtins__": {}}, {}))


def eval_dot(expr):
    total = Fraction(0)
    for raw in expr.split(" + "):
        left, right = raw.split("*")
        total += Fraction(left.strip("()")) * Fraction(right.strip("()"))
    return total


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "EVAL_PARTIAL":
            if safe_eval_arith(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "DOT":
            if eval_dot(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "CHECK" and parts[3] == "passes through point":
            if not parts[2].startswith("z = "):
                return False
    return True


class TestGradientGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GradientGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
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

    def test_tangent_has_point_check(self):
        gen = GradientGenerator("tangent")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.endswith("passes through point")
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
            GradientGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
