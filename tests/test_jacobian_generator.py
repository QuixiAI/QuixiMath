import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.jacobian_generator import JacobianGenerator
from helpers import DELIM


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear(expr):
    coeffs = {"u": 0, "v": 0}
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
            raise AssertionError(f"constant term not expected in {expr!r}")
        coeffs[var] += coeff
    return coeffs["u"], coeffs["v"]


def transform_coeffs(problem):
    if problem.startswith("For"):
        x_txt, y_txt = re.fullmatch(
            r"For the change of variables x = (.+), y = (.+), compute "
            r"the Jacobian determinant d\(x,y\)/d\(u,v\)\.",
            problem,
        ).groups()
    else:
        x_txt, y_txt, _, _ = re.fullmatch(
            r"Use x = (.+), y = (.+) to find the area of the image of "
            r"0 <= u <= (\d+), 0 <= v <= (\d+)\.",
            problem,
        ).groups()
    a, b = parse_linear(x_txt)
    c, d = parse_linear(y_txt)
    return a, b, c, d


def oracle_answer(example):
    problem = example["problem"]
    a, b, c, d = transform_coeffs(problem)
    det = a * d - b * c
    if problem.startswith("For"):
        return f"Jacobian determinant {det}"
    _, _, u_max, v_max = re.fullmatch(
        r"Use x = (.+), y = (.+) to find the area of the image of "
        r"0 <= u <= (\d+), 0 <= v <= (\d+)\.",
        problem,
    ).groups()
    area = abs(det) * int(u_max) * int(v_max)
    return f"image area {area}"


def eval_arith(expr):
    return Fraction(eval(expr, {"__builtins__": {}, "abs": abs}, {}))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "JAC_DET":
            if eval_arith(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "AREA_SCALE":
            if eval_arith(parts[2]) != Fraction(parts[3]):
                return False
    return True


class TestJacobianGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = JacobianGenerator()

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

    def test_variant_outputs(self):
        cases = {
            "determinant": "Jacobian determinant",
            "area_scale": "image area",
        }
        for variant, phrase in cases.items():
            gen = JacobianGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(phrase, result["final_answer"])

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
            JacobianGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
