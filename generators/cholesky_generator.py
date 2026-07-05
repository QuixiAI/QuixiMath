import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(row) for row in zip(*A)]


class CholeskyGenerator(ProblemGenerator):
    """
    Cholesky factorization of 3x3 positive-definite matrices constructed
    as A = L L^T from an integer lower-triangular L.

    Op-codes used:
    - CHOL_SETUP / CHOLESKY_ENTRY / CHECK
    - S / M / D / ROOT (established)
    - Z: lower-triangular factor L
    """

    def generate(self) -> dict:
        l11 = random.randint(1, 5)
        l22 = random.randint(1, 5)
        l33 = random.randint(1, 5)
        l21 = random.randint(-4, 4)
        l31 = random.randint(-4, 4)
        l32 = random.randint(-4, 4)
        L = [[l11, 0, 0], [l21, l22, 0], [l31, l32, l33]]
        A = matmul(L, transpose(L))
        steps = [
            step("CHOL_SETUP", f"A = {fmt_matrix(A)}", "A = L L^T"),
            step("ROOT", f"√{A[0][0]}", l11),
            step("CHOLESKY_ENTRY", "l11", l11),
            step("D", A[1][0], l11, l21),
            step("CHOLESKY_ENTRY", "l21", l21),
            step("D", A[2][0], l11, l31),
            step("CHOLESKY_ENTRY", "l31", l31),
            step("S", A[1][1], l21 * l21, l22 * l22),
            step("ROOT", f"√{l22 * l22}", l22),
            step("CHOLESKY_ENTRY", "l22", l22),
            step("S", A[2][1], l31 * l21, l32 * l22),
            step("D", l32 * l22, l22, l32),
            step("CHOLESKY_ENTRY", "l32", l32),
            step("S", A[2][2], l31 * l31 + l32 * l32, l33 * l33),
            step("ROOT", f"√{l33 * l33}", l33),
            step("CHOLESKY_ENTRY", "l33", l33),
            step("CHECK", "L*L^T", fmt_matrix(A), "matches A"),
        ]
        answer = f"L={fmt_matrix(L)}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="cholesky",
            problem=f"Find the Cholesky factor A = L*L^T for A = {fmt_matrix(A)}.",
            steps=steps,
            final_answer=answer,
        )
