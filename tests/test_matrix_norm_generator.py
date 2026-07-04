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

from generators.matrix_norm_generator import MatrixNormGenerator
from helpers import DELIM


VECTOR_RE = re.compile(
    r"For vector v=(\([^)]+\)), compute the L1, L2, and Linf norms\."
)
FROB_RE = re.compile(
    r"For matrix A=(\[\[.*?\]\]), compute the Frobenius norm\."
)
SPECTRAL_RE = re.compile(
    r"For diagonal matrix A=(\[\[.*?\]\]), compute the spectral norm and "
    r"2-norm condition number\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def expected_vector(problem):
    vector = list(ast.literal_eval(VECTOR_RE.fullmatch(problem).group(1)))
    abs_values = [abs(value) for value in vector]
    l1 = sum(abs_values)
    linf = max(abs_values)
    square0 = vector[0] ** 2
    square1 = vector[1] ** 2
    square_sum = square0 + square1
    l2 = math.isqrt(square_sum)
    steps = [make_step("NORM_SETUP", f"v={vector_text(vector)}",
                       "vector norms")]
    for value, abs_value in zip(vector, abs_values):
        steps.append(make_step("ABS", value, abs_value))
    steps.extend([
        make_step("A", abs_values[0], abs_values[1], l1),
        make_step("E", vector[0], 2, square0),
        make_step("E", vector[1], 2, square1),
        make_step("A", square0, square1, square_sum),
        make_step("ROOT", f"sqrt({square_sum})", l2),
        make_step("MAX", f"{abs_values[0]},{abs_values[1]}", linf),
    ])
    answer = f"L1={l1}; L2={l2}; Linf={linf}"
    return steps, answer


def expected_frobenius(problem):
    matrix = ast.literal_eval(FROB_RE.fullmatch(problem).group(1))
    steps = [
        make_step("NORM_SETUP", f"A={matrix_text(matrix)}",
                  "Frobenius norm"),
    ]
    running = 0
    for row in matrix:
        for value in row:
            square = value ** 2
            new_running = running + square
            steps.append(make_step("E", value, 2, square))
            steps.append(make_step("A", running, square, new_running))
            running = new_running
    root = math.isqrt(running)
    steps.append(make_step("ROOT", f"sqrt({running})", root))
    answer = f"Frobenius={root}"
    return steps, answer


def expected_spectral(problem):
    matrix = ast.literal_eval(SPECTRAL_RE.fullmatch(problem).group(1))
    first = matrix[0][0]
    second = matrix[1][1]
    first_sq = first ** 2
    second_sq = second ** 2
    lambda_max = max(first_sq, second_sq)
    lambda_min = min(first_sq, second_sq)
    sigma_max = math.isqrt(lambda_max)
    sigma_min = math.isqrt(lambda_min)
    cond = Fraction(sigma_max, sigma_min)
    steps = [
        make_step("NORM_SETUP", f"A={matrix_text(matrix)}",
                  "spectral norm and condition"),
        make_step("E", first, 2, first_sq),
        make_step("E", second, 2, second_sq),
        make_step("EIGENVALUES", "A^T A", f"{first_sq},{second_sq}"),
        make_step("MAX", f"{first_sq},{second_sq}", lambda_max),
        make_step("MIN", f"{first_sq},{second_sq}", lambda_min),
        make_step("ROOT", f"sqrt({lambda_max})", sigma_max),
        make_step("ROOT", f"sqrt({lambda_min})", sigma_min),
        make_step("D", sigma_max, sigma_min, fraction_text(cond)),
    ]
    answer = f"spectral={sigma_max}; cond={fraction_text(cond)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if VECTOR_RE.fullmatch(problem):
        steps, answer = expected_vector(problem)
    elif FROB_RE.fullmatch(problem):
        steps, answer = expected_frobenius(problem)
    elif SPECTRAL_RE.fullmatch(problem):
        steps, answer = expected_spectral(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMatrixNormGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MatrixNormGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
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

    def test_variants_are_available(self):
        for variant in MatrixNormGenerator.VARIANTS:
            result = MatrixNormGenerator(variant).generate()
            self.assertEqual(result["operation"], f"matrix_norm_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MatrixNormGenerator("bogus")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
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
