import ast
import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.low_rank_approx_generator import LowRankApproxGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For diagonal matrix A=(\[\[.*?\]\]), compute the rank-1 truncated "
    r"SVD approximation and Frobenius reconstruction error\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    matrix = ast.literal_eval(match.group(1))
    first = matrix[0][0]
    second = matrix[1][1]
    first_sq = first ** 2
    second_sq = second ** 2
    if first >= second:
        kept = "sigma1"
        approx = [[first, 0], [0, 0]]
        discarded = second
        relation = ">="
    else:
        kept = "sigma2"
        approx = [[0, 0], [0, second]]
        discarded = first
        relation = "<"
    steps = [
        make_step("LOWRANK_SETUP", f"A={matrix_text(matrix)}", "rank=1"),
        make_step("E", first, 2, first_sq),
        make_step("E", second, 2, second_sq),
        make_step("EIGENVALUES", "A^T A", f"{first_sq},{second_sq}"),
        make_step("ROOT", f"sqrt({first_sq})", first),
        make_step("SINGULAR_VALUE", "sigma1", first),
        make_step("ROOT", f"sqrt({second_sq})", second),
        make_step("SINGULAR_VALUE", "sigma2", second),
        make_step("CHECK", "sigma1 vs sigma2",
                  f"{first} {relation} {second}", f"keep={kept}"),
        make_step("TRUNCATE", "rank=1", f"discard={discarded}"),
    ]
    residual_squares = []
    for row in range(2):
        for col in range(2):
            residual = matrix[row][col] - approx[row][col]
            square = residual ** 2
            steps.append(make_step("APPROX_ENTRY", f"({row + 1},{col + 1})",
                                   approx[row][col]))
            steps.append(make_step("S", matrix[row][col], approx[row][col],
                                   residual))
            steps.append(make_step("E", residual, 2, square))
            residual_squares.append(square)
    running = 0
    for square in residual_squares:
        new_running = running + square
        steps.append(make_step("A", running, square, new_running))
        running = new_running
    steps.append(make_step("ROOT", f"sqrt({running})", discarded))
    answer = f"A_rank1={matrix_text(approx)}; error={discarded}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLowRankApproxGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LowRankApproxGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "low_rank_svd_rank1")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    radicand = int(fields[1][5:-1])
                    self.assertEqual(math.isqrt(radicand), int(fields[2]),
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
