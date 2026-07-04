import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_pythagorean_pair():
    m = random.randint(2, 15)
    n = random.randint(1, m - 1)
    p = m * m - n * n
    q = 2 * m * n
    r = m * m + n * n
    if random.choice([True, False]):
        p, q = q, p
    return Fraction(p, r), Fraction(q, r)


class HermitianCheckGenerator(ProblemGenerator):
    """
    Hermitian and unitary verification for 2x2 matrices.

    Variants:
    - hermitian: real symmetric matrix [[a,b],[b,a]], with real
      eigenvalues a+b and a-b.
    - unitary: real rotation matrix from a Pythagorean pair, checking
      U^dagger U = I.

    Op-codes used:
    - MATRIX_SETUP / ADJOINT / CHECK
    - A / S / E / M (established/shared): exact arithmetic
    - Z: verification result
    """

    VARIANTS = ["hermitian", "unitary"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "hermitian":
            problem, steps, answer = self._generate_hermitian()
        else:
            problem, steps, answer = self._generate_unitary()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hermitian_check_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_hermitian(self):
        a = random.randint(-20, 20)
        b = random.randint(-12, 12)
        lam1 = a + b
        lam2 = a - b
        matrix = f"[[{a},{b}],[{b},{a}]]"
        steps = [
            step("MATRIX_SETUP", "hermitian", f"A={matrix}"),
            step("ADJOINT", f"A^dagger={matrix}"),
            step("CHECK", "A = A^dagger", "yes", "Hermitian"),
            step("A", a, b, lam1),
            step("S", a, b, lam2),
            step("CHECK", "eigenvalues real", f"{lam1},{lam2}", "real"),
        ]
        answer = f"Hermitian yes; eigenvalues = {lam1}, {lam2}"
        problem = (
            f"Check whether A={matrix} is Hermitian and find its "
            f"eigenvalues."
        )
        return problem, steps, answer

    def _generate_unitary(self):
        c, s = random_pythagorean_pair()
        neg_s = -s
        c_sq = c ** 2
        s_sq = s ** 2
        norm = c_sq + s_sq
        left_off = c * neg_s
        right_off = s * c
        offdiag = left_off + right_off
        matrix = (
            f"[[{fraction_text(c)},{fraction_text(neg_s)}],"
            f"[{fraction_text(s)},{fraction_text(c)}]]"
        )
        adjoint = (
            f"[[{fraction_text(c)},{fraction_text(s)}],"
            f"[{fraction_text(neg_s)},{fraction_text(c)}]]"
        )
        steps = [
            step("MATRIX_SETUP", "unitary", f"U={matrix}"),
            step("ADJOINT", f"U^dagger={adjoint}"),
            step("E", fraction_text(c), 2, fraction_text(c_sq)),
            step("E", fraction_text(s), 2, fraction_text(s_sq)),
            step("A", fraction_text(c_sq), fraction_text(s_sq),
                 fraction_text(norm)),
            step("M", fraction_text(c), fraction_text(neg_s),
                 fraction_text(left_off)),
            step("M", fraction_text(s), fraction_text(c),
                 fraction_text(right_off)),
            step("A", fraction_text(left_off), fraction_text(right_off),
                 fraction_text(offdiag)),
            step("CHECK", "U^dagger U", "I", "unitary"),
        ]
        answer = "unitary yes; U^dagger U = I"
        problem = f"Check whether U={matrix} is unitary."
        return problem, steps, answer
