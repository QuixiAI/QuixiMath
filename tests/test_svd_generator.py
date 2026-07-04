import ast
import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.svd_generator import SVDGenerator
from helpers import DELIM


ROOT2 = "√2"
S = f"1/{ROOT2}"
VEC_PLUS = f"[{S}, {S}]"
VEC_MINUS = f"[{S}, -{S}]"
ORTHO_MATRIX = f"[[{S}, {S}], [{S}, -{S}]]"


def parse_problem_matrix(problem):
    (matrix_txt,) = re.fullmatch(
        r"Find an SVD A = U\*Sigma\*V\^T for A = (\[\[.*\]\]) "
        r"using A\^T A\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def ata_for(A):
    return [
        [sum(A[k][i] * A[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def over_root2(n):
    if n == 1:
        return S
    if n == -1:
        return f"-{S}"
    if n < 0:
        return f"-{-n}/{ROOT2}"
    return f"{n}/{ROOT2}"


def scaled_vec(n, signs):
    return "[" + ", ".join(over_root2(n * sign) for sign in signs) + "]"


def svd_parts(A):
    a, b = A[0]
    sigma1 = a + b
    sigma2 = a - b
    Sigma = [[sigma1, 0], [0, sigma2]]
    return sigma1, sigma2, Sigma


def oracle_answer(example):
    A = parse_problem_matrix(example["problem"])
    _, _, Sigma = svd_parts(A)
    return f"U={ORTHO_MATRIX}; Sigma={fmt_matrix(Sigma)}; V^T={ORTHO_MATRIX}"


def reconstructed_from_sigmas(sigma1, sigma2):
    return [
        [(sigma1 + sigma2) // 2, (sigma1 - sigma2) // 2],
        [(sigma1 - sigma2) // 2, (sigma1 + sigma2) // 2],
    ]


def check_step_arithmetic(example):
    A = parse_problem_matrix(example["problem"])
    a, b = A[0]
    sigma1, sigma2, Sigma = svd_parts(A)
    expected = {
        f"λ1 = {sigma1 * sigma1}": (sigma1 * sigma1, VEC_PLUS),
        f"λ2 = {sigma2 * sigma2}": (sigma2 * sigma2, VEC_MINUS),
    }
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "ATA":
            if ast.literal_eval(parts[2]) != ata_for(A):
                return False
        elif parts[0] == "EIGENVALUE":
            label = parts[1]
            if label not in expected:
                return False
            lam, _ = expected[label]
            if label == f"λ1 = {lam}" and parts[2] != f"from ({a} + {b})^2":
                return False
            if label == f"λ2 = {lam}" and parts[2] != f"from ({a} - {b})^2":
                return False
        elif parts[0] == "EIGENVECTOR":
            if parts[2] != expected[parts[1]][1]:
                return False
        elif parts[0] == "ROOT":
            radicand = int(parts[1].removeprefix("√"))
            root = int(parts[2])
            if root * root != radicand:
                return False
        elif parts[0] == "AV_VECTOR":
            if parts[1] == "A*v1" and parts[2] != scaled_vec(
                    sigma1, [1, 1]):
                return False
            if parts[1] == "A*v2" and parts[2] != scaled_vec(
                    sigma2, [1, -1]):
                return False
        elif parts[0] == "U_VECTOR":
            if parts[1] == "u1 = A*v1/σ1" and parts[2] != VEC_PLUS:
                return False
            if parts[1] == "u2 = A*v2/σ2" and parts[2] != VEC_MINUS:
                return False
        elif parts[0] == "CHECK":
            if ast.literal_eval(parts[2]) != reconstructed_from_sigmas(
                    sigma1, sigma2):
                return False
            if parts[3] != "matches A":
                return False
        elif parts[0] == "Z":
            if fmt_matrix(Sigma) not in parts[1]:
                return False
    return True


class TestSVDGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SVDGenerator()

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

    def test_singular_values_match_ata_eigenvalues(self):
        for _ in range(300):
            result = self.gen.generate()
            A = parse_problem_matrix(result["problem"])
            sigma1, sigma2, _ = svd_parts(A)
            ata = ata_for(A)
            trace = ata[0][0] + ata[1][1]
            det = ata[0][0] * ata[1][1] - ata[0][1] * ata[1][0]
            disc = trace * trace - 4 * det
            root = math.isqrt(disc)
            eigenvalues = sorted([(trace - root) // 2,
                                  (trace + root) // 2], reverse=True)
            self.assertEqual(eigenvalues, [sigma1 ** 2, sigma2 ** 2])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ -|--")
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
