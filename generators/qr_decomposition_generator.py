import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_matrix(M):
    return "[" + ", ".join(
        "[" + ", ".join(fmt_frac(v) for v in row) + "]" for row in M
    ) + "]"


def matmul(A, B):
    rows, inner, cols = len(A), len(B), len(B[0])
    return [[sum(Fraction(A[i][k]) * Fraction(B[k][j])
                 for k in range(inner)) for j in range(cols)]
            for i in range(rows)]


class QRDecompositionGenerator(ProblemGenerator):
    """
    QR decompositions by Gram-Schmidt using exact rational Q entries.

    Variants:
    - two: a 2x2 integer matrix built from a 3-4-5 orthonormal frame.
    - three: a 3x3 upper-triangular matrix whose Gram-Schmidt Q is I.

    Op-codes used:
    - QR_SETUP / QR_ENTRY / GS_SUBTRACT / CHECK
    - DOT / ROOT (established)
    - Z: Q and R
    """

    VARIANTS = ["two", "three"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "two":
            a = random.randint(1, 5)
            b = random.randint(-4, 4)
            c = random.randint(1, 5)
            Q = [[Fraction(3, 5), Fraction(-4, 5)],
                 [Fraction(4, 5), Fraction(3, 5)]]
            R = [[5 * a, 5 * b], [0, 5 * c]]
            A = matmul(Q, R)
            steps = [
                step("QR_SETUP", f"A = {fmt_matrix(A)}", "Gram-Schmidt columns"),
                step("ROOT", f"√({3*a}^2 + {4*a}^2)", 5 * a),
                step("QR_ENTRY", "q1", "[3/5, 4/5]"),
                step("DOT", "q1·v2", 5 * b),
                step("GS_SUBTRACT", "v2 - (q1·v2)q1",
                     f"[{-4*c}, {3*c}]"),
                step("ROOT", f"√({-4*c}^2 + {3*c}^2)", 5 * c),
                step("QR_ENTRY", "q2", "[-4/5, 3/5]"),
            ]
        else:
            r11 = random.randint(1, 6)
            r22 = random.randint(1, 6)
            r33 = random.randint(1, 6)
            r12 = random.randint(-5, 5)
            r13 = random.randint(-5, 5)
            r23 = random.randint(-5, 5)
            Q = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            R = [[r11, r12, r13], [0, r22, r23], [0, 0, r33]]
            A = R
            steps = [
                step("QR_SETUP", f"A = {fmt_matrix(A)}", "Gram-Schmidt columns"),
                step("QR_ENTRY", "q1", "[1, 0, 0]"),
                step("GS_SUBTRACT", "v2 - (q1·v2)q1",
                     f"[0, {r22}, 0]"),
                step("QR_ENTRY", "q2", "[0, 1, 0]"),
                step("GS_SUBTRACT", "v3 - projections",
                     f"[0, 0, {r33}]"),
                step("QR_ENTRY", "q3", "[0, 0, 1]"),
            ]
        steps += [
            step("QR_ENTRY", "Q", fmt_matrix(Q)),
            step("QR_ENTRY", "R", fmt_matrix(R)),
            step("CHECK", "Q^T Q", "I", "orthonormal"),
            step("CHECK", "QR", fmt_matrix(A), "matches A"),
        ]
        answer = f"Q={fmt_matrix(Q)}; R={fmt_matrix(R)}"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"qr_decomposition_{variant}",
            problem=f"Find a QR decomposition A = QR for A = {fmt_matrix(A)}.",
            steps=steps,
            final_answer=answer,
        )
