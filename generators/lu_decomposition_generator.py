import random

from base_generator import ProblemGenerator
from helpers import step, jid


def matmul(L, U):
    return [
        [sum(L[i][k] * U[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def fmt_matrix(M):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]"
                           for row in M) + "]"


def fmt_num(n):
    return f"({n})" if n < 0 else str(n)


def ratio_expr(n, d):
    return f"{fmt_num(n)}/{fmt_num(d)}"


def product_expr(a, b):
    return f"{fmt_num(a)}*{fmt_num(b)}"


def subtract_products_expr(base, *pairs):
    expr = fmt_num(base)
    for a, b in pairs:
        expr += f" - {product_expr(a, b)}"
    return expr


class LUDecompositionGenerator(ProblemGenerator):
    """
    3x3 LU decomposition with a unit lower-triangular L using Doolittle's
    method and no pivoting.

    Op-codes used:
    - LU_SETUP: matrix and method
    - LU_ENTRY: compute an entry of L or U
    - LU_RESULT: assembled L and U
    - CHECK (established): multiply L*U back to A
    - Z: final L and U
    """

    @staticmethod
    def _factors():
        l21 = random.randint(-4, 4)
        l31 = random.randint(-4, 4)
        l32 = random.randint(-4, 4)
        u11 = random.choice([v for v in range(-5, 6) if v != 0])
        u22 = random.choice([v for v in range(-5, 6) if v != 0])
        u33 = random.choice([v for v in range(-5, 6) if v != 0])
        u12 = random.randint(-5, 5)
        u13 = random.randint(-5, 5)
        u23 = random.randint(-5, 5)
        L = [[1, 0, 0], [l21, 1, 0], [l31, l32, 1]]
        U = [[u11, u12, u13], [0, u22, u23], [0, 0, u33]]
        return L, U, matmul(L, U)

    def generate(self) -> dict:
        L, U, A = self._factors()
        l21 = L[1][0]
        l31 = L[2][0]
        l32 = L[2][1]
        u11, u12, u13 = U[0]
        u22, u23 = U[1][1], U[1][2]
        u33 = U[2][2]

        steps = [
            step("LU_SETUP", f"A = {fmt_matrix(A)}", "unit lower L"),
            step("LU_ENTRY", "u11", f"a11 = {A[0][0]}", u11),
            step("LU_ENTRY", "u12", f"a12 = {A[0][1]}", u12),
            step("LU_ENTRY", "u13", f"a13 = {A[0][2]}", u13),
            step("LU_ENTRY", "l21", ratio_expr(A[1][0], u11), l21),
            step("LU_ENTRY", "l31", ratio_expr(A[2][0], u11), l31),
            step("LU_ENTRY", "u22",
                 subtract_products_expr(A[1][1], (l21, u12)), u22),
            step("LU_ENTRY", "u23",
                 subtract_products_expr(A[1][2], (l21, u13)), u23),
            step("LU_ENTRY", "l32",
                 f"({subtract_products_expr(A[2][1], (l31, u12))})"
                 f"/{fmt_num(u22)}", l32),
            step("LU_ENTRY", "u33",
                 subtract_products_expr(A[2][2], (l31, u13), (l32, u23)),
                 u33),
            step("LU_RESULT", "L", fmt_matrix(L)),
            step("LU_RESULT", "U", fmt_matrix(U)),
            step("CHECK", "L*U", fmt_matrix(A), "matches A"),
        ]
        answer = f"L={fmt_matrix(L)}; U={fmt_matrix(U)}"
        steps.append(step("Z", answer))
        problem = (
            f"Find an LU decomposition A = L*U with unit lower triangular "
            f"L for A = {fmt_matrix(A)}."
        )

        return dict(
            problem_id=jid(),
            operation="lu_decomposition",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
