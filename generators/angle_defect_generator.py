import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


ANGLES = [15, 30, 45, 60, 75, 90]
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


class AngleDefectGenerator(ProblemGenerator):
    """
    Hyperbolic triangle area from angle defect:
    area = (180 degrees - A - B - C) in radians times R^2.

    Op-codes used:
    - ANGLE_DEFECT_SETUP / THEOREM: given data and area formula
    - A / S / D / E / M (established/shared): exact arithmetic
    - Z: exact area in terms of pi
    """

    def generate(self) -> dict:
        radius = random.choice(RADII)
        while True:
            a, b, c = [random.choice(ANGLES) for _ in range(3)]
            if a + b + c < 180:
                break
        first_sum = a + b
        angle_sum = first_sum + c
        defect_deg = 180 - angle_sum
        defect_turn = Fraction(defect_deg, 180)
        radius_sq = radius * radius
        area_coeff = defect_turn * radius_sq
        area = pi_text(area_coeff)
        steps = [
            step("ANGLE_DEFECT_SETUP", f"R={radius}",
                 f"angles={a},{b},{c}"),
            step("THEOREM", "hyperbolic angle defect",
                 "area = (180 deg - (A+B+C))/180 * pi * R^2"),
            step("A", a, b, first_sum),
            step("A", first_sum, c, angle_sum),
            step("S", 180, angle_sum, defect_deg),
            step("D", defect_deg, 180, defect_turn),
            step("E", radius, 2, radius_sq),
            step("M", defect_turn, radius_sq, area_coeff),
        ]
        answer = f"area = {area}"
        steps.append(step("Z", answer))
        problem = (
            f"A hyperbolic triangle with curvature radius {radius} has "
            f"angles {a} deg, {b} deg, and {c} deg. Use the angle "
            f"defect formula to find its exact area in terms of pi."
        )
        return dict(
            problem_id=jid(),
            operation="hyperbolic_angle_defect_area",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
