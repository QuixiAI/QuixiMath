import random

from base_generator import ProblemGenerator
from helpers import step, jid


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


class LowRankApproxGenerator(ProblemGenerator):
    """
    Rank-1 truncated SVD approximation and Frobenius reconstruction error.

    Diagonal 2x2 matrices make the singular values exact: they are the absolute
    diagonal entries. The rank-1 approximation keeps the larger singular
    component and the Frobenius error is the discarded singular value.

    Op-codes used:
    - LOWRANK_SETUP / EIGENVALUES / SINGULAR_VALUE / TRUNCATE / APPROX_ENTRY
    - CHECK (established): choose the larger singular value
    - S / E / A / ROOT (established/shared): residual and Frobenius arithmetic
    - Z: rank-1 approximation and error
    """

    def generate(self) -> dict:
        first = random.randint(1, 20)
        second = random.choice([value for value in range(1, 21)
                                if value != first])
        matrix = [[first, 0], [0, second]]
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
            step("LOWRANK_SETUP", f"A={matrix_text(matrix)}", "rank=1"),
            step("E", first, 2, first_sq),
            step("E", second, 2, second_sq),
            step("EIGENVALUES", "A^T A", f"{first_sq},{second_sq}"),
            step("ROOT", f"sqrt({first_sq})", first),
            step("SINGULAR_VALUE", "sigma1", first),
            step("ROOT", f"sqrt({second_sq})", second),
            step("SINGULAR_VALUE", "sigma2", second),
            step("CHECK", "sigma1 vs sigma2",
                 f"{first} {relation} {second}", f"keep={kept}"),
            step("TRUNCATE", "rank=1", f"discard={discarded}"),
        ]
        residual_squares = []
        for row in range(2):
            for col in range(2):
                residual = matrix[row][col] - approx[row][col]
                square = residual ** 2
                steps.append(step("APPROX_ENTRY", f"({row + 1},{col + 1})",
                                  approx[row][col]))
                steps.append(step("S", matrix[row][col], approx[row][col],
                                  residual))
                steps.append(step("E", residual, 2, square))
                residual_squares.append(square)
        running = 0
        for square in residual_squares:
            new_running = running + square
            steps.append(step("A", running, square, new_running))
            running = new_running
        steps.append(step("ROOT", f"sqrt({running})", discarded))
        answer = f"A_rank1={matrix_text(approx)}; error={discarded}"
        steps.append(step("Z", answer))
        problem = (
            f"For diagonal matrix A={matrix_text(matrix)}, compute the rank-1 "
            "truncated SVD approximation and Frobenius reconstruction error."
        )
        return dict(
            problem_id=jid(),
            operation="low_rank_svd_rank1",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
