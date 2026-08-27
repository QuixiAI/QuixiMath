import random
from fractions import Fraction
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


PYTHAG_LIMIT = 24
NON_UNIT_DEN = 16
NON_UNIT_NUM = 16
INT_BOUND = 12

PHRASINGS = [
    "Check whether M={matrix} is a member of {group}.",
    "Does M={matrix} belong to {group}? Verify the defining conditions.",
    "Decide whether the matrix M={matrix} lies in the group {group}.",
    "Test M={matrix} for membership in {group}.",
    "Is M={matrix} an element of {group}? Check the group conditions.",
]

LABELS = {
    "so2": ("R", "R^T", "R^T R"),
    "o2": ("R", "R^T", "R^T R"),
    "su2": ("U", "U^dagger", "U^dagger U"),
    "sl2z": ("M", "M^T", "M^T M"),
    "gl2z": ("M", "M^T", "M^T M"),
}


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(M):
    return ("[[" + ",".join(fraction_text(v) for v in M[0]) + "],["
            + ",".join(fraction_text(v) for v in M[1]) + "]]")


def pythagorean_pairs(limit):
    """Exact rational points on the unit circle from primitive (m, n)."""
    pairs = []
    for m in range(2, limit + 1):
        for n in range(1, m):
            if gcd(m, n) != 1 or (m - n) % 2 == 0:
                continue
            hyp = m * m + n * n
            pairs.append((Fraction(m * m - n * n, hyp),
                          Fraction(2 * m * n, hyp)))
    return pairs


UNIT_PAIRS = pythagorean_pairs(PYTHAG_LIMIT)


def primitive_columns(bound):
    return [(p, q)
            for p in range(-bound, bound + 1)
            for q in range(-bound, bound + 1)
            if gcd(abs(p), abs(q)) == 1]


def unimodular_matrices(bound):
    cols = primitive_columns(bound)
    return [[[p, r], [q, s]]
            for (p, q) in cols
            for (r, s) in cols
            if p * s - q * r in (1, -1)]


UNIMODULAR = unimodular_matrices(INT_BOUND)


def random_unit_entries():
    """Random (c, s) with c^2 + s^2 = 1 exactly, all four sign quadrants."""
    c, s = random.choice(UNIT_PAIRS)
    if random.choice([True, False]):
        c, s = s, c
    if random.choice([True, False]):
        c = -c
    if random.choice([True, False]):
        s = -s
    return c, s


def random_rotation_entries():
    """Backwards-compatible helper: exact rational cosine/sine pair."""
    return random_unit_entries()


def random_off_circle_entries():
    """Random rational (a, b) that is NOT on the unit circle."""
    while True:
        r = random.randint(2, NON_UNIT_DEN)
        p = random.randint(-NON_UNIT_NUM, NON_UNIT_NUM)
        q = random.randint(-NON_UNIT_NUM, NON_UNIT_NUM)
        if p == 0 and q == 0:
            continue
        a = Fraction(p, r)
        b = Fraction(q, r)
        if a * a + b * b == 1:
            continue
        return a, b


def random_integer_matrix(det_kind):
    """Integer 2x2 matrix with det 1, det -1, or |det| not 1."""
    if det_kind in ("plus", "minus"):
        want = 1 if det_kind == "plus" else -1
        while True:
            M = random.choice(UNIMODULAR)
            if M[0][0] * M[1][1] - M[0][1] * M[1][0] == want:
                return [[Fraction(v) for v in row] for row in M]
    while True:
        M = [[random.randint(-INT_BOUND, INT_BOUND) for _ in range(2)]
             for _ in range(2)]
        if M[0][0] * M[1][1] - M[0][1] * M[1][0] not in (1, -1):
            return [[Fraction(v) for v in row] for row in M]


class MatrixGroupCheckGenerator(ProblemGenerator):
    """
    Matrix group membership checks with exact rational / integer arithmetic.

    Variants:
    - so2: is M a rotation (M^T M = I and det M = 1)?
    - su2: same test written with the unitary labels U^dagger U.
    - o2: orthogonal test only (det M = 1 or -1 both qualify).
    - sl2z: integer entries with det M = 1.
    - gl2z: integer entries with det M = 1 or -1.

    Matrices are built backward: rotation and reflection shapes on exact
    rational points of the unit circle (Pythagorean parameterisation), rational
    pairs deliberately off the circle, and integer matrices with a chosen
    determinant. Membership is genuinely yes or no, so the verdict has to be
    earned rather than guessed.

    Op-codes used:
    - MATRIX_GROUP_SETUP / CHECK
    - E / A / M / S (established/shared): exact arithmetic
    - Z: membership verdict
    """

    VARIANTS = ["so2", "su2", "o2", "sl2z", "gl2z"]
    CIRCLE_VARIANTS = ("so2", "su2", "o2")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        group = self.variant or random.choice(self.VARIANTS)
        if group in self.CIRCLE_VARIANTS:
            steps, answer, matrix = self._circle_problem(group)
        else:
            steps, answer, matrix = self._integer_problem(group)
        steps.append(step("Z", answer))
        problem = random.choice(PHRASINGS).format(matrix=matrix,
                                                  group=group.upper())
        return dict(
            problem_id=jid(),
            operation=f"matrix_group_check_{group}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _circle_problem(self, group):
        symbol, adjoint_label, product_label = LABELS[group]
        on_circle = random.random() < 0.55
        a, b = random_unit_entries() if on_circle else (
            random_off_circle_entries())
        shape = random.choice(["rotation", "reflection"])
        if shape == "rotation":
            M = [[a, -b], [b, a]]
        else:
            M = [[a, b], [b, -a]]
        a_sq = M[0][0] ** 2
        b_sq = M[1][0] ** 2
        norm = a_sq + b_sq
        left = M[0][0] * M[1][1]
        right = M[0][1] * M[1][0]
        det = left - right

        orthogonal = norm == 1
        if group == "o2":
            member = orthogonal
        else:
            member = orthogonal and det == 1
        norm_text = "I" if norm == 1 else f"({fraction_text(norm)})I"
        detail = (f"{product_label} = {norm_text}, "
                  f"det = {fraction_text(det)}")
        answer = (f"{group.upper()} member {'yes' if member else 'no'}; "
                  f"{detail}")

        matrix = matrix_text(M)
        steps = [
            step("MATRIX_GROUP_SETUP", group.upper(), f"M={matrix}"),
            step("E", fraction_text(M[0][0]), 2, fraction_text(a_sq)),
            step("E", fraction_text(M[1][0]), 2, fraction_text(b_sq)),
            step("A", fraction_text(a_sq), fraction_text(b_sq),
                 fraction_text(norm)),
            step("CHECK", product_label, norm_text,
                 "metric preserved" if orthogonal else "columns not unit"),
            step("M", fraction_text(M[0][0]), fraction_text(M[1][1]),
                 fraction_text(left)),
            step("M", fraction_text(M[0][1]), fraction_text(M[1][0]),
                 fraction_text(right)),
            step("S", fraction_text(left), fraction_text(right),
                 fraction_text(det)),
            step("CHECK", f"det {symbol}", fraction_text(det),
                 "special" if det == 1 else "not special"),
        ]
        return steps, answer, matrix

    def _integer_problem(self, group):
        symbol = LABELS[group][0]
        det_kind = random.choice(["plus", "minus", "other", "other"])
        M = random_integer_matrix(det_kind)
        left = M[0][0] * M[1][1]
        right = M[0][1] * M[1][0]
        det = left - right
        member = det == 1 if group == "sl2z" else det in (1, -1)
        detail = f"integer entries, det = {fraction_text(det)}"
        answer = (f"{group.upper()} member {'yes' if member else 'no'}; "
                  f"{detail}")

        matrix = matrix_text(M)
        steps = [
            step("MATRIX_GROUP_SETUP", group.upper(), f"M={matrix}"),
            step("CHECK", "entries", "all integers", "lattice condition"),
            step("M", fraction_text(M[0][0]), fraction_text(M[1][1]),
                 fraction_text(left)),
            step("M", fraction_text(M[0][1]), fraction_text(M[1][0]),
                 fraction_text(right)),
            step("S", fraction_text(left), fraction_text(right),
                 fraction_text(det)),
            step("CHECK", f"det {symbol}", fraction_text(det),
                 "unimodular" if det in (1, -1) else "not unimodular"),
        ]
        return steps, answer, matrix
