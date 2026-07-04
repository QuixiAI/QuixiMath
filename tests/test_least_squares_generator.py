import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.least_squares_generator import LeastSquaresGenerator
from helpers import DELIM


def parse_points(problem):
    raw = re.findall(r"\((-?\d+), (-?\d+)\)", problem)
    return [(int(x), int(y)) for x, y in raw]


def line_txt(a, b):
    if b == 0:
        return f"ŷ = {a}"
    mag = "x" if abs(b) == 1 else f"{abs(b)}x"
    if a == 0:
        return f"ŷ = {mag}" if b > 0 else f"ŷ = -{mag}"
    return f"ŷ = {a} + {mag}" if b > 0 else f"ŷ = {a} - {mag}"


def design_matrix(xs):
    return [[1, x] for x in xs]


def mat2_solve(A, b):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [
        Fraction(b[0] * A[1][1] - A[0][1] * b[1], det),
        Fraction(A[0][0] * b[1] - b[0] * A[1][0], det),
    ]


def normal_parts(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    X = design_matrix(xs)
    xtx = [
        [sum(row[i] * row[j] for row in X) for j in range(2)]
        for i in range(2)
    ]
    xty = [sum(row[i] * y for row, y in zip(X, ys)) for i in range(2)]
    beta = mat2_solve(xtx, xty)
    yhat = [beta[0] + beta[1] * x for x in xs]
    residual = [Fraction(y) - yh for y, yh in zip(ys, yhat)]
    return X, xs, ys, xtx, xty, beta, yhat, residual


def fmt_value(value):
    value = Fraction(value)
    return value.numerator if value.denominator == 1 else str(value)


def fmt_list(values):
    return "[" + ", ".join(str(fmt_value(v)) for v in values) + "]"


def fmt_matrix(M):
    return "[" + ", ".join(fmt_list(row) for row in M) + "]"


def oracle_answer(example):
    _, _, _, _, _, beta, yhat, residual = normal_parts(
        parse_points(example["problem"])
    )
    assert all(v.denominator == 1 for v in beta + yhat + residual)
    a, b = (v.numerator for v in beta)
    return (f"{line_txt(a, b)}; projection {fmt_list(yhat)}; "
            f"residual {fmt_list(residual)}")


def check_step_arithmetic(example):
    points = parse_points(example["problem"])
    X, _, ys, xtx, xty, beta, yhat, residual = normal_parts(points)
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "DESIGN_MATRIX":
            if parts[1] != f"X = {fmt_matrix(X)}":
                return False
            if parts[2] != f"y = {fmt_list(ys)}":
                return False
        elif parts[0] == "NORMAL_EQ" and parts[1] == "X^T X":
            if parts[2] != fmt_matrix(xtx):
                return False
        elif parts[0] == "NORMAL_EQ" and parts[1] == "X^T y":
            if parts[2] != fmt_list(xty):
                return False
        elif parts[0] == "D":
            if Fraction(parts[1]) / Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "LS_LINE":
            a, b = (v.numerator for v in beta)
            if parts[1] != f"a = {a}, b = {b}":
                return False
            if parts[2] != line_txt(a, b):
                return False
        elif parts[0] == "PROJECTION":
            if ast.literal_eval(parts[2]) != [int(v) for v in yhat]:
                return False
        elif parts[0] == "RESIDUAL":
            if ast.literal_eval(parts[2]) != [int(v) for v in residual]:
                return False
        elif parts[0] == "CHECK":
            check = [
                sum(row[col] * residual[i] for i, row in enumerate(X))
                for col in range(2)
            ]
            if ast.literal_eval(parts[2]) != [int(v) for v in check]:
                return False
            if parts[3] != "orthogonal":
                return False
    return True


class TestLeastSquaresGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LeastSquaresGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_residual_is_orthogonal_to_design_columns(self):
        for _ in range(300):
            result = self.gen.generate()
            X, _, _, _, _, _, _, residual = normal_parts(
                parse_points(result["problem"])
            )
            for col in range(2):
                self.assertEqual(
                    sum(row[col] * residual[i] for i, row in enumerate(X)),
                    0,
                )

    def test_variants_have_expected_point_count(self):
        for variant, count in (("three_point_line", 3),
                               ("four_point_line", 4)):
            gen = LeastSquaresGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(len(parse_points(result["problem"])), count)

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1x|\+ -|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"least_squares_three_point_line",
                               "least_squares_four_point_line"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LeastSquaresGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
