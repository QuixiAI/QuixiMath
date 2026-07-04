import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bch_generator import BCHGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For nilpotent 3x3 matrices A=([^ ]+) and B=([^,]+), where Eij has "
    r"a 1 in row i and column j, use BCH to second order to compute "
    r"log\(e\^A e\^B\)\."
)
SCALED_LABEL_RE = re.compile(r"(-?)(?:(\d+))?(E\d\d)")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def zero_matrix(size=3):
    return [[Fraction(0) for _ in range(size)] for _ in range(size)]


def identity_matrix(size=3):
    return [
        [Fraction(1 if i == j else 0) for j in range(size)]
        for i in range(size)
    ]


def e_matrix(label, coeff=1):
    row = int(label[1]) - 1
    col = int(label[2]) - 1
    matrix = zero_matrix()
    matrix[row][col] = Fraction(coeff)
    return matrix


def mat_add(A, B):
    return [
        [A[i][j] + B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_sub(A, B):
    return [
        [A[i][j] - B[i][j] for j in range(len(A[0]))]
        for i in range(len(A))
    ]


def mat_scale(A, scalar):
    return [[scalar * value for value in row] for row in A]


def matmul(A, B):
    return [
        [
            sum(A[i][k] * B[k][j] for k in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def scaled_label(coeff, label):
    if coeff == 1:
        return label
    if coeff == -1:
        return f"-{label}"
    return f"{coeff}{label}"


def parse_scaled_label(text):
    match = SCALED_LABEL_RE.fullmatch(text)
    assert match is not None, text
    sign, coeff, label = match.groups()
    value = int(coeff) if coeff else 1
    if sign == "-":
        value = -value
    return value, label


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    a, left = parse_scaled_label(match.group(1))
    b, right = parse_scaled_label(match.group(2))
    return a, left, b, right


def expected_flow(example):
    a, left, b, right = parse_problem(example["problem"])
    A = e_matrix(left, a)
    B = e_matrix(right, b)
    I = identity_matrix()
    exp_A = mat_add(I, A)
    exp_B = mat_add(I, B)
    exp_product = matmul(exp_A, exp_B)
    AB = matmul(A, B)
    BA = matmul(B, A)
    comm = mat_sub(AB, BA)
    half_comm = mat_scale(comm, Fraction(1, 2))
    A_plus_B = mat_add(A, B)
    bch = mat_add(A_plus_B, half_comm)
    steps = [
        make_step("BCH_SETUP", f"A={scaled_label(a, left)}",
                  f"B={scaled_label(b, right)}", "order=2"),
        make_step("MATRIX_EXP", "e^A", "I + A", matrix_text(exp_A)),
        make_step("MATRIX_EXP", "e^B", "I + B", matrix_text(exp_B)),
        make_step("MATRIX_PRODUCT", "e^A e^B", matrix_text(exp_product)),
        make_step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
        make_step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
        make_step("MATRIX_SUB", "AB - BA", matrix_text(comm)),
        make_step("MATRIX_SCALE", "1/2[A,B]", matrix_text(half_comm)),
        make_step("MATRIX_ADD", "A+B", matrix_text(A_plus_B)),
        make_step("BCH_FORM", "A+B+1/2[A,B]", matrix_text(bch)),
        make_step("CHECK", "[A,[A,B]] and [B,[A,B]]", "0", "truncates"),
    ]
    answer = f"log(e^A e^B) = {matrix_text(bch)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBCHGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BCHGenerator()

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

    def test_higher_commutators_vanish(self):
        for _ in range(300):
            result = self.gen.generate()
            a, left, b, right = parse_problem(result["problem"])
            A = e_matrix(left, a)
            B = e_matrix(right, b)
            comm = mat_sub(matmul(A, B), matmul(B, A))
            left_nested = mat_sub(matmul(A, comm), matmul(comm, A))
            right_nested = mat_sub(matmul(B, comm), matmul(comm, B))
            self.assertEqual(left_nested, zero_matrix(), result["problem"])
            self.assertEqual(right_nested, zero_matrix(), result["problem"])

    def test_both_commutator_signs_occur(self):
        random.seed(7)
        signs = set()
        gen = BCHGenerator()
        for _ in range(300):
            a, left, b, right = parse_problem(gen.generate()["problem"])
            comm = mat_sub(matmul(e_matrix(left, a), e_matrix(right, b)),
                           matmul(e_matrix(right, b), e_matrix(left, a)))
            nonzero = [value for row in comm for value in row if value]
            signs.add(1 if nonzero[0] > 0 else -1)
        self.assertEqual(signs, {-1, 1})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
