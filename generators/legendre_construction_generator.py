import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class LegendreConstructionGenerator(ProblemGenerator):
    """
    Construct P_2 or P_3 by Gram-Schmidt on {1, x, x^2, x^3}
    over [-1, 1], then scale to the standard Legendre leading
    coefficient.

    Op-codes used:
    - LEGENDRE_SETUP / INTEGRAL / PROJECTION / POLY_SUB / POLY_SCALE
    - D (established/shared): exact projection coefficient
    - Z: constructed Legendre polynomial
    """

    VARIANTS = ["p2", "p3"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "p2":
            problem, steps, answer = self._generate_p2()
        else:
            problem, steps, answer = self._generate_p3()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"legendre_construction_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_p2(self):
        numerator = Fraction(2, 3)
        denominator = Fraction(2)
        projection = numerator / denominator
        steps = [
            step("LEGENDRE_SETUP", "target=P_2",
                 "inner product integral_-1^1 f(x)g(x) dx"),
            step("INTEGRAL", "<1,1>", denominator),
            step("INTEGRAL", "<x^2,1>", numerator),
            step("D", fraction_text(numerator), fraction_text(denominator),
                 fraction_text(projection)),
            step("PROJECTION", "x^2 onto 1", fraction_text(projection)),
            step("POLY_SUB", "x^2", fraction_text(projection),
                 "x^2 - 1/3"),
            step("POLY_SCALE", "x^2 - 1/3", "3/2",
                 "(3x^2 - 1)/2"),
        ]
        answer = "P_2(x) = (3x^2 - 1)/2"
        problem = (
            "Use Gram-Schmidt on {1, x, x^2} over [-1,1] to construct "
            "the Legendre polynomial P_2 with leading coefficient 3/2."
        )
        return problem, steps, answer

    def _generate_p3(self):
        numerator = Fraction(2, 5)
        denominator = Fraction(2, 3)
        projection = numerator / denominator
        steps = [
            step("LEGENDRE_SETUP", "target=P_3",
                 "inner product integral_-1^1 f(x)g(x) dx"),
            step("INTEGRAL", "<x,x>", denominator),
            step("INTEGRAL", "<x^3,x>", numerator),
            step("D", fraction_text(numerator), fraction_text(denominator),
                 fraction_text(projection)),
            step("PROJECTION", "x^3 onto x", fraction_text(projection)),
            step("POLY_SUB", "x^3", "3x/5", "x^3 - 3x/5"),
            step("POLY_SCALE", "x^3 - 3x/5", "5/2",
                 "(5x^3 - 3x)/2"),
        ]
        answer = "P_3(x) = (5x^3 - 3x)/2"
        problem = (
            "Use Gram-Schmidt on {1, x, x^2, x^3} over [-1,1] to "
            "construct the Legendre polynomial P_3 with leading "
            "coefficient 5/2."
        )
        return problem, steps, answer
