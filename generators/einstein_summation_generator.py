import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.matrix_ops_generator import mat


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def rnd_matrix(size=2, lo=-5, hi=5):
    return [[random.randint(lo, hi) for _ in range(size)] for _ in range(size)]


class EinsteinSummationGenerator(ProblemGenerator):
    """
    Numeric Einstein-summation bookkeeping for contractions and symmetrizing.

    Variants:
    - contraction: C_ik = A_ij B_jk.
    - trace: T_ii.
    - symmetrize: S_ij = (T_ij + T_ji)/2.

    Op-codes used:
    - EINSTEIN_SETUP / TENSOR_ENTRY / TRACE_ENTRY
    - A / M / D (established/shared): exact arithmetic
    - Z: contracted tensor, trace, or symmetrized tensor
    """

    VARIANTS = ["contraction", "trace", "symmetrize"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "contraction":
            problem, steps, answer = self._generate_contraction()
        elif variant == "trace":
            problem, steps, answer = self._generate_trace()
        else:
            problem, steps, answer = self._generate_symmetrize()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"einstein_summation_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_contraction(self):
        A = rnd_matrix()
        B = rnd_matrix()
        C = [[0, 0], [0, 0]]
        steps = [
            step("EINSTEIN_SETUP", "contract", f"A_ij={mat(A)}",
                 f"B_jk={mat(B)}"),
        ]
        for i in range(2):
            for k in range(2):
                p1 = A[i][0] * B[0][k]
                p2 = A[i][1] * B[1][k]
                C[i][k] = p1 + p2
                steps.extend([
                    step("M", A[i][0], B[0][k], p1),
                    step("M", A[i][1], B[1][k], p2),
                    step("A", p1, p2, C[i][k]),
                    step("TENSOR_ENTRY", f"C_{i + 1}{k + 1}", C[i][k]),
                ])
        answer = f"C_ik = {mat(C)}"
        problem = (
            f"Given A_ij={mat(A)} and B_jk={mat(B)}, compute "
            "C_ik=A_ij B_jk using Einstein summation."
        )
        return problem, steps, answer

    def _generate_trace(self):
        T = rnd_matrix(3, -6, 6)
        diagonal = [T[i][i] for i in range(3)]
        partial = diagonal[0] + diagonal[1]
        trace_value = partial + diagonal[2]
        steps = [
            step("EINSTEIN_SETUP", "trace", f"T_ij={mat(T)}"),
        ]
        for i, value in enumerate(diagonal, start=1):
            steps.append(step("TRACE_ENTRY", f"T_{i}{i}", value))
        steps.extend([
            step("A", diagonal[0], diagonal[1], partial),
            step("A", partial, diagonal[2], trace_value),
        ])
        answer = f"T_ii = {trace_value}"
        problem = f"Given T_ij={mat(T)}, compute the contraction T_ii."
        return problem, steps, answer

    def _generate_symmetrize(self):
        T = rnd_matrix()
        S = [[Fraction(0) for _ in range(2)] for _ in range(2)]
        steps = [
            step("EINSTEIN_SETUP", "symmetrize", f"T_ij={mat(T)}"),
        ]
        for i in range(2):
            for j in range(2):
                total = T[i][j] + T[j][i]
                value = Fraction(total, 2)
                S[i][j] = value
                steps.extend([
                    step("A", T[i][j], T[j][i], total),
                    step("D", total, 2, fraction_text(value)),
                    step("TENSOR_ENTRY", f"S_{i + 1}{j + 1}",
                         fraction_text(value)),
                ])
        answer = f"S_ij = {matrix_text(S)}"
        problem = (
            f"Given T_ij={mat(T)}, compute S_ij=(T_ij+T_ji)/2."
        )
        return problem, steps, answer
