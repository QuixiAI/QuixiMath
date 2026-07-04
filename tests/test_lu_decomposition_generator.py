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

from generators.lu_decomposition_generator import LUDecompositionGenerator
from helpers import DELIM


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def parse_problem_matrix(problem):
    (matrix_txt,) = re.fullmatch(
        r"Find an LU decomposition A = L\*U with unit lower triangular "
        r"L for A = (\[\[.*\]\])\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def matmul(L, U):
    return [
        [sum(L[i][k] * U[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def integral(value):
    value = Fraction(value)
    if value.denominator != 1:
        raise AssertionError(f"expected integer entry, got {value}")
    return value.numerator


def oracle_factors(A):
    A = [[Fraction(v) for v in row] for row in A]
    u11, u12, u13 = A[0]
    l21 = A[1][0] / u11
    l31 = A[2][0] / u11
    u22 = A[1][1] - l21 * u12
    u23 = A[1][2] - l21 * u13
    l32 = (A[2][1] - l31 * u12) / u22
    u33 = A[2][2] - l31 * u13 - l32 * u23
    L = [
        [1, 0, 0],
        [integral(l21), 1, 0],
        [integral(l31), integral(l32), 1],
    ]
    U = [
        [integral(u11), integral(u12), integral(u13)],
        [0, integral(u22), integral(u23)],
        [0, 0, integral(u33)],
    ]
    return L, U


def oracle_answer(example):
    L, U = oracle_factors(parse_problem_matrix(example["problem"]))
    return f"L={fmt_matrix(L)}; U={fmt_matrix(U)}"


def eval_fraction_expr(expr):
    if " = " in expr:
        expr = expr.split(" = ", 1)[1]
    expr = re.sub(r"(?<![A-Za-z])-?\d+",
                  lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def check_step_arithmetic(example):
    L = U = None
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "LU_ENTRY":
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "LU_RESULT" and parts[1] == "L":
            L = ast.literal_eval(parts[2])
        elif parts[0] == "LU_RESULT" and parts[1] == "U":
            U = ast.literal_eval(parts[2])
        elif parts[0] == "CHECK":
            if matmul(L, U) != ast.literal_eval(parts[2]):
                return False
    return True


class TestLUDecompositionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LUDecompositionGenerator()

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

    def test_reconstructs_problem_matrix(self):
        for _ in range(300):
            result = self.gen.generate()
            answer = result["final_answer"]
            l_txt, u_txt = re.fullmatch(
                r"L=(\[\[.*\]\]); U=(\[\[.*\]\])",
                answer,
            ).groups()
            self.assertEqual(matmul(ast.literal_eval(l_txt),
                                    ast.literal_eval(u_txt)),
                             parse_problem_matrix(result["problem"]))

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"--|\+ 0|(?<!\d)1x")
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


if __name__ == "__main__":
    unittest.main()
