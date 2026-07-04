import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

# angle label -> exact sine used (given in the problem text)
SIN_VALUES = {30: Fraction(1, 2), 37: Fraction(3, 5),
              53: Fraction(4, 5), 90: Fraction(1), 150: Fraction(1, 2)}


class TriangleAreaSASGenerator(ProblemGenerator):
    """
    Triangle area from two sides and the included angle:
    Area = (1/2)·a·b·sin C, with the sine value given in the problem
    (Principle 5) and the product kept exact. Obtuse included angles
    (150°) appear so the formula is seen to work past 90°.

    Op-codes used:
    - TRI_SETUP: sides, angle, and the given sine (established)
    - TRI_AREA_FORMULA: Area = (1/2)ab sin C
    - M / D: the product and halving, exact (established)
    - Z: 'N square units'
    """

    def generate(self) -> dict:
        C = random.choice(list(SIN_VALUES))
        sv = SIN_VALUES[C]
        a = random.randint(3, 14)
        b = random.randint(3, 14)
        area = Fraction(a * b) * sv / 2
        if (area * 100).denominator != 1:
            return self.generate()

        given = f"sin {C}° = {dec(sv)}"
        steps = [
            step("TRI_SETUP",
                 f"a = {a}, b = {b}, included angle C = {C}°; "
                 f"given {given}", "area"),
            step("TRI_AREA_FORMULA", "Area = (1/2)·a·b·sin C"),
            step("M", a, b, a * b),
            step("M", a * b, dec(sv), dec(a * b * sv)),
            step("D", dec(a * b * sv), 2, dec(area)),
        ]
        answer = f"{dec(area)} square units"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="triangle_area_sas",
            problem=(f"A triangle has sides a = {a} and b = {b} with "
                     f"included angle C = {C}°. Given {given}, find "
                     f"its area."),
            steps=steps,
            final_answer=answer,
        )
