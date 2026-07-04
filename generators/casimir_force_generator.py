import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def pi_squared_text(value):
    coeff = Fraction(value)
    sign = "-" if coeff < 0 else ""
    coeff = abs(coeff)
    if coeff == 1:
        body = "π^2"
    elif coeff.denominator == 1:
        body = f"{coeff.numerator}π^2"
    elif coeff.numerator == 1:
        body = f"π^2/{coeff.denominator}"
    else:
        body = f"{coeff.numerator}π^2/{coeff.denominator}"
    return sign + body


class CasimirForceGenerator(ProblemGenerator):
    """
    Casimir force per area between parallel conducting plates.

    The formula F/A = -π^2 hbar c/(240 d^4) is evaluated exactly in supplied
    units. Ordinary rational arithmetic is reduced before attaching π^2.

    Op-codes used:
    - CASIMIR_FORCE_SETUP: formula and supplied constants
    - PI2_NUM: attach a symbolic π^2 in the numerator
    - E / M / D / S (established/shared): exact arithmetic
    - Z: exact force per area
    """

    VARIANTS = ["pressure"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or "pressure"
        hbar = random.randint(1, 20)
        c = random.randint(1, 20)
        d = random.randint(1, 8)
        d_fourth = d ** 4
        denominator = 240 * d_fourth
        numerator = hbar * c
        coeff = Fraction(numerator, denominator)
        signed_coeff = -coeff
        value = pi_squared_text(signed_coeff)
        constants = f"hbar={hbar},c={c},d={d}"
        steps = [
            step("CASIMIR_FORCE_SETUP",
                 "F/A=-π^2*hbar*c/(240*d^4)", constants),
            step("E", d, 4, d_fourth),
            step("M", 240, d_fourth, denominator),
            step("M", hbar, c, numerator),
            step("D", numerator, denominator, fraction_text(coeff)),
            step("S", 0, fraction_text(coeff), fraction_text(signed_coeff)),
            step("PI2_NUM", fraction_text(signed_coeff), "π^2", value),
        ]
        answer = f"F/A = {value}"
        steps.append(step("Z", answer))
        problem = (
            f"Given hbar={hbar}, c={c}, and plate separation d={d}, "
            "compute the Casimir force per area "
            "F/A=-π^2*hbar*c/(240*d^4)."
        )
        return dict(
            problem_id=jid(),
            operation=f"casimir_force_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
