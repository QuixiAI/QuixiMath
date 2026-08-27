import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

PLACES = [
    "surveying class", "architecture studio", "robotics lab",
    "navigation workshop", "engineering classroom", "construction lab",
    "science museum", "technical college", "design studio",
    "field station", "training center", "mapping office", "research lab",
    "observatory", "modeling classroom", "fabrication shop",
    "university lab", "instrument room", "prototype bay", "survey site",
]

CONTEXTS = [
    "At the {place}, a right-triangle calculation is being checked.",
    "During a session at the {place}, the following triangle is studied.",
    "A worksheet from the {place} gives this triangle.",
    "In a model prepared by the {place}, the following data apply.",
    "An exercise used at the {place} asks about this triangle.",
    "The {place} records a new right-triangle measurement.",
    "A review prepared by the {place} includes the following data.",
    "In a lesson at the {place}, this triangle is analyzed.",
]

# angle label, function, exact-arithmetic value (≈ real value)
GIVEN_VALUES = [
    (30, "sin", Fraction(1, 2)),
    (37, "sin", Fraction(3, 5)), (37, "cos", Fraction(4, 5)),
    (37, "tan", Fraction(3, 4)),
    (53, "sin", Fraction(4, 5)), (53, "cos", Fraction(3, 5)),
    (24, "sin", Fraction(2, 5)), (66, "cos", Fraction(2, 5)),
]


def context_text():
    return random.choice(CONTEXTS).format(place=random.choice(PLACES))


def pythagorean_triple():
    """Construct a modest scaled Pythagorean triple with either leg marked."""
    while True:
        outer = random.randint(2, 8)
        inner = random.randint(1, outer - 1)
        if math.gcd(outer, inner) == 1 and (outer - inner) % 2 == 1:
            break
    primitive_hypotenuse = outer * outer + inner * inner
    scale = random.randint(1, max(1, min(8, 150 // primitive_hypotenuse)))
    leg_a = scale * (outer * outer - inner * inner)
    leg_b = scale * 2 * outer * inner
    hypotenuse = scale * primitive_hypotenuse
    if random.choice([False, True]):
        leg_a, leg_b = leg_b, leg_a
    return leg_a, leg_b, hypotenuse


class RightTriangleTrigGenerator(ProblemGenerator):
    """
    SOH-CAH-TOA with every needed trig value supplied in the problem
    (Principle 5 - no calculator).

    Variants:
    - write_ratio: sides from a (possibly scaled) Pythagorean triple;
      write sin/cos/tan of a marked angle in lowest terms
    - find_side:   a given value like sin 37° ≈ 0.6 scales a known side
    - find_angle:  compute the ratio from two sides, then match it
      against a supplied value table

    Op-codes used:
    - TRIG_SETUP: the triangle data and the goal (given, goal)
    - TRIG_RATIO: the SOH-CAH-TOA definition used (function, ratio)
    - FRAC_REDUCE / M / D: the arithmetic, exact (established)
    - TABLE_LOOKUP: match the computed ratio to the given table
      (established)
    - Z: the ratio, side, or angle
    """

    VARIANTS = ["write_ratio", "find_side", "find_angle"]
    RATIO_DEF = {"sin": "opposite/hypotenuse",
                 "cos": "adjacent/hypotenuse",
                 "tan": "opposite/adjacent"}

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        context = context_text()

        if variant == "write_ratio":
            a, b, c = pythagorean_triple()
            fn = random.choice(["sin", "cos", "tan"])
            num, den = {"sin": (a, c), "cos": (b, c),
                        "tan": (a, b)}[fn]
            val = Fraction(num, den)
            steps = [
                step("TRIG_SETUP",
                     f"right triangle: leg opposite A = {a}, leg "
                     f"adjacent to A = {b}, hypotenuse = {c}",
                     f"{fn} A"),
                step("TRIG_RATIO", fn, self.RATIO_DEF[fn]),
                step("REWRITE", f"{fn} A = {num}/{den}"),
            ]
            if (num, den) != (val.numerator, val.denominator):
                steps.append(step("FRAC_REDUCE", f"{num}/{den}", val))
            answer = f"{fn} A = {val}"
            steps.append(step("Z", answer))
            problem = (f"{context} In a right triangle, the leg opposite "
                       f"angle A "
                       f"is {a}, the leg adjacent to A is {b}, and the "
                       f"hypotenuse is {c}. Write {fn} A as a fraction "
                       f"in lowest terms.")
        elif variant == "find_side":
            deg, fn, val = random.choice(GIVEN_VALUES)
            known = val.denominator * random.randint(1, 100)
            x = known * val
            assert x.denominator == 1
            side_names = {"sin": ("opposite side", "hypotenuse"),
                          "cos": ("adjacent side", "hypotenuse"),
                          "tan": ("opposite side", "adjacent side")}
            want, have = side_names[fn]
            steps = [
                step("TRIG_SETUP",
                     f"right triangle, angle {deg}°, {have} = {known}; "
                     f"given {fn} {deg}° ≈ {dec(val)}", f"the {want}"),
                step("TRIG_RATIO", fn, self.RATIO_DEF[fn]),
                step("REWRITE", f"x/{known} = {dec(val)}"),
                step("M", known, dec(val), dec(x)),
            ]
            answer = str(x.numerator)
            steps.append(step("Z", answer))
            problem = (f"{context} In a right triangle, one acute angle "
                       f"measures "
                       f"{deg}° and the {have} is {known}. Given that "
                       f"{fn} {deg}° ≈ {dec(val)}, find the {want}.")
        else:
            deg, fn, val = random.choice(GIVEN_VALUES)
            scale = random.randint(1, 100)
            num = val.numerator * scale
            den = val.denominator * scale
            names = {"sin": ("opposite side", "hypotenuse"),
                     "cos": ("adjacent side", "hypotenuse"),
                     "tan": ("opposite side", "adjacent side")}
            n1, n2 = names[fn]
            steps = [
                step("TRIG_SETUP",
                     f"right triangle: {n1} = {num}, {n2} = {den}; "
                     f"given {fn} {deg}° ≈ {dec(val)}", "angle A"),
                step("TRIG_RATIO", fn, self.RATIO_DEF[fn]),
                step("D", num, den, dec(val)),
                step("TABLE_LOOKUP", f"{fn} {deg}° = {dec(val)}",
                     f"A = {deg}°"),
            ]
            answer = f"A = {deg}°"
            steps.append(step("Z", answer))
            problem = (f"{context} In a right triangle, the {n1} is {num} "
                       f"and the "
                       f"{n2} is {den}. Given that {fn} {deg}° ≈ "
                       f"{dec(val)}, find the measure of angle A.")

        return dict(
            problem_id=jid(),
            operation=f"right_triangle_trig_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
