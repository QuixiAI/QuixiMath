import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    coeff = Fraction(value)
    if coeff.denominator == 1:
        return f"{coeff.numerator}/π"
    return f"{coeff.numerator}/({coeff.denominator}π)"


class HawkingGenerator(ProblemGenerator):
    """
    Hawking temperature and Bekenstein-Hawking entropy evaluations.

    Constants are supplied in the problem and kept symbolic/exact. Temperature
    reduces the rational coefficient before attaching the remaining 1/π.

    Op-codes used:
    - HAWKING_SETUP: variant, formula, and supplied constants
    - PI_DEN: attach a symbolic π in the denominator
    - E / M / D (established/shared): exact arithmetic
    - Z: requested black-hole thermodynamics quantity
    """

    VARIANTS = ["temperature", "entropy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "temperature":
            problem, steps, answer = self._generate_temperature()
        else:
            problem, steps, answer = self._generate_entropy()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hawking_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_temperature(self):
        hbar = random.randint(1, 12)
        c = random.randint(1, 6)
        G = random.randint(1, 12)
        M = random.randint(1, 18)
        k_b = random.randint(1, 12)
        c_cubed = c ** 3
        numerator = hbar * c_cubed
        den_8g = 8 * G
        den_8gm = den_8g * M
        denominator = den_8gm * k_b
        coeff = Fraction(numerator, denominator)
        value = over_pi_text(coeff)
        constants = f"hbar={hbar},c={c},G={G},M={M},k_B={k_b}"
        steps = [
            step("HAWKING_SETUP", "temperature",
                 "T_H=hbar*c^3/(8π*G*M*k_B)", constants),
            step("E", c, 3, c_cubed),
            step("M", hbar, c_cubed, numerator),
            step("M", 8, G, den_8g),
            step("M", den_8g, M, den_8gm),
            step("M", den_8gm, k_b, denominator),
            step("D", numerator, denominator, fraction_text(coeff)),
            step("PI_DEN", fraction_text(coeff), "π", value),
        ]
        answer = f"T_H = {value}"
        problem = (
            f"Given hbar={hbar}, c={c}, G={G}, M={M}, and k_B={k_b}, "
            "compute the Hawking temperature "
            "T_H=hbar*c^3/(8π*G*M*k_B)."
        )
        return problem, steps, answer

    def _generate_entropy(self):
        k_b = random.randint(1, 12)
        c = random.randint(1, 6)
        area = random.randint(4, 80)
        hbar = random.randint(1, 12)
        G = random.randint(1, 12)
        c_cubed = c ** 3
        left = k_b * c_cubed
        numerator = left * area
        den_4hbar = 4 * hbar
        denominator = den_4hbar * G
        entropy = Fraction(numerator, denominator)
        constants = f"k_B={k_b},c={c},A={area},hbar={hbar},G={G}"
        steps = [
            step("HAWKING_SETUP", "entropy",
                 "S_BH=k_B*c^3*A/(4*hbar*G)", constants),
            step("E", c, 3, c_cubed),
            step("M", k_b, c_cubed, left),
            step("M", left, area, numerator),
            step("M", 4, hbar, den_4hbar),
            step("M", den_4hbar, G, denominator),
            step("D", numerator, denominator, fraction_text(entropy)),
        ]
        answer = f"S_BH = {fraction_text(entropy)}"
        problem = (
            f"Given k_B={k_b}, c={c}, A={area}, hbar={hbar}, and G={G}, "
            "compute the Bekenstein-Hawking entropy "
            "S_BH=k_B*c^3*A/(4*hbar*G)."
        )
        return problem, steps, answer
