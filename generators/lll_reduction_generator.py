import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


BASES = [
    ((4, 1), (7, 2)),
    ((3, 1), (8, 3)),
    ((5, 2), (9, 4)),
    ((6, 1), (11, 2)),
]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def sub(u, k, v):
    return (u[0] - k * v[0], u[1] - k * v[1])


def norm2(v):
    return dot(v, v)


def round_fraction(fr):
    if fr >= 0:
        return (fr.numerator + fr.denominator // 2) // fr.denominator
    return -round_fraction(-fr)


def basis_text(b1, b2):
    return f"[({b1[0]},{b1[1]}),({b2[0]},{b2[1]})]"


class LLLReductionGenerator(ProblemGenerator):
    """
    Two-dimensional LLL/Gauss lattice basis reduction.

    Op-codes used:
    - LLL_SETUP / DOT / NORM2 / MU / SIZE_REDUCE / SWAP / LLL_DONE
    - Z: reduced basis
    """

    def generate(self) -> dict:
        b1, b2 = random.choice(BASES)
        original = (b1, b2)
        steps = [step("LLL_SETUP", basis_text(b1, b2))]
        while True:
            numerator = dot(b2, b1)
            denominator = norm2(b1)
            mu = Fraction(numerator, denominator)
            k = round_fraction(mu)
            steps.append(step("DOT", f"b2.b1", numerator))
            steps.append(step("NORM2", "b1", denominator))
            steps.append(step("MU", str(mu), f"round={k}"))
            if k:
                old = b2
                b2 = sub(b2, k, b1)
                coeff = str(k) if k >= 0 else f"({k})"
                steps.append(step("SIZE_REDUCE", f"b2={old}",
                                  f"b2-{coeff}b1={b2}"))
                continue
            if norm2(b2) < norm2(b1):
                steps.append(step("SWAP", f"norm b2={norm2(b2)}",
                                  f"norm b1={norm2(b1)}"))
                b1, b2 = b2, b1
                continue
            break
        steps.append(step("LLL_DONE", basis_text(b1, b2)))
        answer = f"reduced basis = {basis_text(b1, b2)}"
        problem = (
            f"Use two-dimensional LLL (Gauss reduction) on basis "
            f"{basis_text(*original)}. Round mu to the nearest integer."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="lll_reduction_2d",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
