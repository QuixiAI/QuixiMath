import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def pi_txt(fr):
    """Exact multiple of π: '6π', '49π/8', 'π/3'."""
    if fr.denominator == 1:
        return "π" if fr == 1 else f"{fr.numerator}π"
    head = "π" if fr.numerator == 1 else f"{fr.numerator}π"
    return f"{head}/{fr.denominator}"


class ArcSectorGenerator(ProblemGenerator):
    """
    Arc length and sector area, kept exact in terms of π: reduce the
    angle fraction θ/360 first, then apply it to 2πr or πr².

    Op-codes used:
    - ARC_SETUP: radius, central angle, and the goal (given, goal)
    - ARC_FORMULA / SECTOR_FORMULA: the formula (established shape)
    - FRAC_REDUCE: θ/360 in lowest terms (established)
    - M / E: the arithmetic, exact fractions (established)
    - Z: exact answer like '6π' or '49π/8'
    """

    VARIANTS = ["arc", "sector"]
    ANGLES = [30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        r = random.randint(2, 12)
        theta = random.choice(self.ANGLES)
        frac = Fraction(theta, 360)

        steps = [step("ARC_SETUP", f"circle r = {r}, central angle "
                      f"{theta}°",
                      "arc length" if variant == "arc" else "sector area"),
                 step("ARC_FORMULA" if variant == "arc"
                      else "SECTOR_FORMULA",
                      "L = (θ/360)·2πr" if variant == "arc"
                      else "A = (θ/360)·πr^2"),
                 step("FRAC_REDUCE", f"{theta}/360", frac)]

        if variant == "arc":
            steps.append(step("M", 2, r, 2 * r))
            value = frac * 2 * r
            steps.append(step("M", frac, 2 * r, value))
            answer = pi_txt(value)
            problem = (f"A circle has radius {r}. Find the length of "
                       f"the arc cut off by a central angle of {theta}°. "
                       f"Give the exact answer in terms of π.")
        else:
            steps.append(step("E", r, 2, r * r))
            value = frac * r * r
            steps.append(step("M", frac, r * r, value))
            answer = pi_txt(value)
            problem = (f"A circle has radius {r}. Find the area of the "
                       f"sector with central angle {theta}°. Give the "
                       f"exact answer in terms of π.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"{variant}_measure",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
