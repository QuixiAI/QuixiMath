import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def ln_text(value):
    return f"ln({fraction_text(value)})"


def random_ratio():
    while True:
        numerator = random.randint(2, 30)
        denominator = random.randint(1, 18)
        if numerator > denominator and math.gcd(numerator, denominator) == 1:
            return Fraction(numerator, denominator)


class HyperbolicDistanceGenerator(ProblemGenerator):
    """
    Poincare half-plane and disk distances in exact logarithmic form.

    Variants:
    - half_plane: vertical geodesic distance abs(ln(y2/y1)).
    - disk_radial: radial disk distance ln((1+r)/(1-r)).

    Op-codes used:
    - HYPERBOLIC_DISTANCE_SETUP / FORMULA / LOG_EVAL
    - A / S / D (established/shared): exact fraction arithmetic
    - Z: exact logarithmic distance
    """

    VARIANTS = ["half_plane", "disk_radial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "half_plane":
            problem, steps, answer = self._generate_half_plane()
        else:
            problem, steps, answer = self._generate_disk_radial()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hyperbolic_distance_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_half_plane(self):
        x = random.randint(-6, 6)
        y1 = Fraction(random.randint(1, 20), 1)
        ratio = random_ratio()
        y2 = y1 * ratio
        distance = ln_text(ratio)
        steps = [
            step("HYPERBOLIC_DISTANCE_SETUP", "half-plane",
                 f"P=({x},{fraction_text(y1)})",
                 f"Q=({x},{fraction_text(y2)})"),
            step("FORMULA", "vertical geodesic distance = abs(ln(y_Q/y_P))"),
            step("D", fraction_text(y2), fraction_text(y1),
                 fraction_text(ratio)),
            step("LOG_EVAL", fraction_text(ratio), distance),
        ]
        answer = f"distance = {distance}"
        problem = (
            f"In the Poincare half-plane, P=({x},{fraction_text(y1)}) "
            f"and Q=({x},{fraction_text(y2)}) lie on the same vertical "
            f"geodesic. Use d=abs(ln(y_Q/y_P)) to find the hyperbolic "
            f"distance."
        )
        return problem, steps, answer

    def _generate_disk_radial(self):
        ratio = random_ratio()
        r = (ratio - 1) / (ratio + 1)
        one_plus = 1 + r
        one_minus = 1 - r
        distance = ln_text(ratio)
        steps = [
            step("HYPERBOLIC_DISTANCE_SETUP", "disk",
                 "P=(0,0)", f"Q=({fraction_text(r)},0)"),
            step("FORMULA", "radial disk distance = ln((1+r)/(1-r))"),
            step("A", 1, fraction_text(r), fraction_text(one_plus)),
            step("S", 1, fraction_text(r), fraction_text(one_minus)),
            step("D", fraction_text(one_plus), fraction_text(one_minus),
                 fraction_text(ratio)),
            step("LOG_EVAL", fraction_text(ratio), distance),
        ]
        answer = f"distance = {distance}"
        problem = (
            f"In the Poincare disk, P=(0,0) and Q=({fraction_text(r)},0) "
            f"lie on a diameter. Use d=ln((1+r)/(1-r)) to find the "
            f"hyperbolic distance."
        )
        return problem, steps, answer
