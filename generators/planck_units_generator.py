import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class PlanckUnitsGenerator(ProblemGenerator):
    """
    Planck length, time, and mass from supplied hbar, G, and c.

    Constants are constructed as hbar=a^2, G=b^2, c=d^2 so the square roots
    are exact:
    l_P=sqrt(hbar G/c^3), t_P=sqrt(hbar G/c^5), m_P=sqrt(hbar c/G).

    Op-codes used:
    - PLANCK_SETUP / ROOT
    - E / M / D (established/shared): exact arithmetic
    - Z: requested Planck unit
    """

    VARIANTS = ["length", "time", "mass"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        d = random.randint(1, 6)
        hbar = a ** 2
        G = b ** 2
        c = d ** 2
        if variant == "length":
            power = 3
            formula = "sqrt(hbar*G/c^3)"
            answer_name = "l_P"
            root_value = Fraction(a * b, d ** 3)
        elif variant == "time":
            power = 5
            formula = "sqrt(hbar*G/c^5)"
            answer_name = "t_P"
            root_value = Fraction(a * b, d ** 5)
        else:
            power = 1
            formula = "sqrt(hbar*c/G)"
            answer_name = "m_P"
            root_value = Fraction(a * d, b)
        c_power = c ** power
        numerator = hbar * (G if variant != "mass" else c)
        radicand = Fraction(numerator, c_power if variant != "mass" else G)
        steps = [
            step("PLANCK_SETUP", variant, f"hbar={hbar}", f"G={G}",
                 f"c={c}"),
            step("M", hbar, G if variant != "mass" else c, numerator),
            step("E", c if variant != "mass" else G, power,
                 c_power if variant != "mass" else G ** power),
            step("D", numerator, c_power if variant != "mass" else G,
                 fraction_text(radicand)),
            step("ROOT", f"sqrt({fraction_text(radicand)})",
                 fraction_text(root_value)),
        ]
        answer = f"{answer_name} = {fraction_text(root_value)}"
        steps.append(step("Z", answer))
        problem = (
            f"Given hbar={hbar}, G={G}, and c={c}, compute the Planck "
            f"{variant} {formula}."
        )
        return dict(
            problem_id=jid(),
            operation=f"planck_units_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
