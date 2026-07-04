import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


ANGLES = [30, 45, 60, 75, 90, 105, 120, 135, 150]
RADII = list(range(2, 21))


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


class SphericalExcessGenerator(ProblemGenerator):
    """
    Spherical triangle area by Girard's theorem:
    area = (A + B + C - 180 degrees) in radians times R^2.

    Op-codes used:
    - SPHERICAL_EXCESS_SETUP / THEOREM: given data and Girard's theorem
    - A / S / D / E / M (established/shared): exact arithmetic
    - Z: exact area in terms of pi
    """

    def generate(self) -> dict:
        radius = random.choice(RADII)
        while True:
            a, b, c = [random.choice(ANGLES) for _ in range(3)]
            if a + b + c > 180:
                break
        first_sum = a + b
        angle_sum = first_sum + c
        excess_deg = angle_sum - 180
        excess_turn = Fraction(excess_deg, 180)
        radius_sq = radius * radius
        area_coeff = excess_turn * radius_sq
        area = pi_text(area_coeff)
        steps = [
            step("SPHERICAL_EXCESS_SETUP", f"R={radius}",
                 f"angles={a},{b},{c}"),
            step("THEOREM", "Girard",
                 "area = (A+B+C-180 deg)/180 * pi * R^2"),
            step("A", a, b, first_sum),
            step("A", first_sum, c, angle_sum),
            step("S", angle_sum, 180, excess_deg),
            step("D", excess_deg, 180, excess_turn),
            step("E", radius, 2, radius_sq),
            step("M", excess_turn, radius_sq, area_coeff),
        ]
        answer = f"area = {area}"
        steps.append(step("Z", answer))
        problem = (
            f"A spherical triangle on a sphere of radius {radius} has "
            f"angles {a} deg, {b} deg, and {c} deg. Use Girard's "
            f"theorem to find its exact area in terms of pi."
        )
        return dict(
            problem_id=jid(),
            operation="spherical_excess_area",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
