import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


COEFFS = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
PAIRS = [
    ("E12", "E23"),
    ("E23", "E31"),
    ("E31", "E12"),
    ("E23", "E12"),
    ("E31", "E23"),
    ("E12", "E31"),
]


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


class BCHGenerator(ProblemGenerator):
    """
    Baker-Campbell-Hausdorff for nilpotent 3x3 elementary matrices.

    The selected pairs satisfy [A,[A,B]]=[B,[A,B]]=0, so
    log(e^A e^B) = A + B + 1/2[A,B] exactly.

    Op-codes used:
    - BCH_SETUP / MATRIX_EXP / MATRIX_PRODUCT / MATRIX_SUB
    - MATRIX_SCALE / MATRIX_ADD / BCH_FORM / CHECK
    - Z: exact truncated logarithm
    """

    def generate(self) -> dict:
        left, right = random.choice(PAIRS)
        a = random.choice(COEFFS)
        b = random.choice(COEFFS)
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
            step("BCH_SETUP", f"A={scaled_label(a, left)}",
                 f"B={scaled_label(b, right)}", "order=2"),
            step("MATRIX_EXP", "e^A", "I + A", matrix_text(exp_A)),
            step("MATRIX_EXP", "e^B", "I + B", matrix_text(exp_B)),
            step("MATRIX_PRODUCT", "e^A e^B", matrix_text(exp_product)),
            step("MATRIX_PRODUCT", "AB", matrix_text(AB)),
            step("MATRIX_PRODUCT", "BA", matrix_text(BA)),
            step("MATRIX_SUB", "AB - BA", matrix_text(comm)),
            step("MATRIX_SCALE", "1/2[A,B]", matrix_text(half_comm)),
            step("MATRIX_ADD", "A+B", matrix_text(A_plus_B)),
            step("BCH_FORM", "A+B+1/2[A,B]", matrix_text(bch)),
            step("CHECK", "[A,[A,B]] and [B,[A,B]]", "0", "truncates"),
        ]
        answer = f"log(e^A e^B) = {matrix_text(bch)}"
        steps.append(step("Z", answer))
        problem = (
            f"For nilpotent 3x3 matrices A={scaled_label(a, left)} and "
            f"B={scaled_label(b, right)}, where Eij has a 1 in row i and "
            "column j, use BCH to second order to compute log(e^A e^B)."
        )
        return dict(
            problem_id=jid(),
            operation="bch_nilpotent_second_order",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
