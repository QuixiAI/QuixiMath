import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


DILATION_FACTORS = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 5),
                    Fraction(4, 5)]


def fraction_text(value):
    return str(Fraction(value))


class SchwarzschildGenerator(ProblemGenerator):
    """
    Schwarzschild radius and time-dilation plug-ins with supplied constants.

    Variants:
    - radius: r_s = 2GM/c^2.
    - time_dilation: sqrt(1 - r_s/r), constructed to be exact.

    Op-codes used:
    - SCHWARZSCHILD_SETUP / ROOT
    - M / E / D / S (established/shared): exact arithmetic
    - Z: radius or dilation factor
    """

    VARIANTS = ["radius", "time_dilation"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "radius":
            problem, steps, answer = self._generate_radius()
        else:
            problem, steps, answer = self._generate_time_dilation()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"schwarzschild_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_radius(self):
        G = random.randint(1, 12)
        c = random.randint(1, 6)
        factor = random.randint(1, 20)
        M = factor * c * c
        numerator_left = 2 * G
        numerator = numerator_left * M
        c_sq = c ** 2
        radius = Fraction(numerator, c_sq)
        steps = [
            step("SCHWARZSCHILD_SETUP", "radius", f"G={G}",
                 f"M={M}", f"c={c}"),
            step("M", 2, G, numerator_left),
            step("M", numerator_left, M, numerator),
            step("E", c, 2, c_sq),
            step("D", numerator, c_sq, fraction_text(radius)),
        ]
        answer = f"r_s = {fraction_text(radius)}"
        problem = (
            f"Given G={G}, M={M}, and c={c}, compute the Schwarzschild "
            "radius r_s=2GM/c^2."
        )
        return problem, steps, answer

    def _generate_time_dilation(self):
        factor = random.choice(DILATION_FACTORS)
        denom = factor.denominator ** 2 - factor.numerator ** 2
        scale = random.randint(1, 30)
        r_s = scale * denom
        radius = Fraction(r_s * factor.denominator ** 2, denom)
        ratio = Fraction(r_s, radius)
        inside = 1 - ratio
        steps = [
            step("SCHWARZSCHILD_SETUP", "time_dilation",
                 f"r_s={r_s}", f"r={fraction_text(radius)}"),
            step("D", r_s, fraction_text(radius), fraction_text(ratio)),
            step("S", 1, fraction_text(ratio), fraction_text(inside)),
            step("ROOT", f"sqrt({fraction_text(inside)})",
                 fraction_text(factor)),
        ]
        answer = f"time dilation factor = {fraction_text(factor)}"
        problem = (
            f"Given Schwarzschild radius r_s={r_s} and radius "
            f"r={fraction_text(radius)}, compute the time dilation factor "
            "sqrt(1 - r_s/r)."
        )
        return problem, steps, answer
