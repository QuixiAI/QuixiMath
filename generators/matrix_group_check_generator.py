import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_rotation_entries():
    m = random.randint(2, 20)
    n = random.randint(1, m - 1)
    c = Fraction(m * m - n * n, m * m + n * n)
    s = Fraction(2 * m * n, m * m + n * n)
    if random.choice([True, False]):
        c, s = s, c
    return c, s


class MatrixGroupCheckGenerator(ProblemGenerator):
    """
    Matrix group membership checks for exact 2x2 rotation matrices.

    Variants:
    - so2: verify R^T R = I and det R = 1.
    - su2: verify U^dagger U = I and det U = 1 for the same real
      unitary form.

    Op-codes used:
    - MATRIX_GROUP_SETUP / CHECK
    - E / A / M / S (established/shared): exact arithmetic
    - Z: membership verdict
    """

    VARIANTS = ["so2", "su2"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        group = self.variant or random.choice(self.VARIANTS)
        c, s = random_rotation_entries()
        neg_s = -s
        c_sq = c ** 2
        s_sq = s ** 2
        norm = c_sq + s_sq
        det_left = c * c
        det_right = neg_s * s
        det = det_left - det_right
        matrix = (
            f"[[{fraction_text(c)},{fraction_text(neg_s)}],"
            f"[{fraction_text(s)},{fraction_text(c)}]]"
        )
        matrix_symbol = "R" if group == "so2" else "U"
        adjoint_label = "R^T" if group == "so2" else "U^dagger"
        product_label = "R^T R" if group == "so2" else "U^dagger U"
        steps = [
            step("MATRIX_GROUP_SETUP", group.upper(), f"M={matrix}"),
            step("E", fraction_text(c), 2, fraction_text(c_sq)),
            step("E", fraction_text(s), 2, fraction_text(s_sq)),
            step("A", fraction_text(c_sq), fraction_text(s_sq),
                 fraction_text(norm)),
            step("CHECK", product_label, "I", "metric preserved"),
            step("M", fraction_text(c), fraction_text(c),
                 fraction_text(det_left)),
            step("M", fraction_text(neg_s), fraction_text(s),
                 fraction_text(det_right)),
            step("S", fraction_text(det_left), fraction_text(det_right),
                 fraction_text(det)),
            step("CHECK", "det M", fraction_text(det), "special"),
        ]
        answer = (
            f"{group.upper()} member yes; "
            f"{adjoint_label} {matrix_symbol} = I, det = 1"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Check whether M={matrix} is a member of {group.upper()}."
        )
        return dict(
            problem_id=jid(),
            operation=f"matrix_group_check_{group}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
