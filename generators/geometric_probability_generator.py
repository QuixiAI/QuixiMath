import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


class GeometricProbabilityGenerator(ProblemGenerator):
    """
    Geometric probability as a ratio of measures: interval length to total
    length, rectangle area to total area, or sector angle to full-circle angle.
    All inputs are integers and all final probabilities are exact.

    Variants:
    - interval: probability from a subinterval of a number line
    - rectangle: probability from an area ratio inside a rectangle
    - sector: probability from a circular sector angle ratio

    Op-codes used:
    - GEO_PROB_SETUP: sample space and target event
    - MEASURE_TOTAL: total length, area, or angle measure
    - MEASURE_FAVORABLE: favorable length, area, or angle measure
    - GEO_PROB_FORMULA: probability = favorable measure / total measure
    - FRAC_BUILD / CHECK (established): exact ratio and sanity check
    - Z: the exact probability
    """

    VARIANTS = ["interval", "rectangle", "sector"]
    SECTOR_ANGLES = [30, 45, 60, 72, 90, 120, 135, 144, 180, 216, 240, 270]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _ratio_step(favorable, total):
        value = Fraction(favorable, total)
        return step("FRAC_BUILD", f"{favorable}/{total}", exact(value)), exact(value)

    def _generate_interval(self):
        total = random.randint(10, 60)
        left = random.randint(0, total - 2)
        right = random.randint(left + 1, total)
        favorable = right - left
        frac_step, answer = self._ratio_step(favorable, total)
        steps = [
            step("GEO_PROB_SETUP", f"number line from 0 to {total}",
                 f"lands between {left} and {right}"),
            step("MEASURE_TOTAL", "total length", total),
            step("MEASURE_FAVORABLE", "interval length",
                 f"{right} - {left} = {favorable}"),
            step("GEO_PROB_FORMULA",
                 "probability = favorable length / total length"),
            frac_step,
            step("CHECK", f"{favorable} <= {total}",
                 "probability is at most 1"),
            step("Z", answer),
        ]
        problem = (
            f"A point is chosen uniformly at random on a number line from "
            f"0 to {total}. What is the probability that it lands between "
            f"{left} and {right}? Give an exact answer."
        )
        return "interval", problem, steps, answer

    def _generate_rectangle(self):
        width = random.randint(5, 20)
        height = random.randint(5, 20)
        shade_width = random.randint(1, width)
        shade_height = random.randint(1, height)
        total = width * height
        favorable = shade_width * shade_height
        frac_step, answer = self._ratio_step(favorable, total)
        steps = [
            step("GEO_PROB_SETUP", f"rectangle {width} by {height}",
                 f"shaded rectangle {shade_width} by {shade_height}"),
            step("MEASURE_TOTAL", "whole area",
                 f"{width} * {height} = {total}"),
            step("MEASURE_FAVORABLE", "shaded area",
                 f"{shade_width} * {shade_height} = {favorable}"),
            step("GEO_PROB_FORMULA",
                 "probability = favorable area / total area"),
            frac_step,
            step("CHECK", f"{favorable} <= {total}",
                 "probability is at most 1"),
            step("Z", answer),
        ]
        problem = (
            f"A point is chosen uniformly at random in a {width} by {height} "
            f"rectangle. A shaded rectangle inside it is {shade_width} by "
            f"{shade_height}. What is the probability that the point lands "
            f"in the shaded rectangle? Give an exact answer."
        )
        return "rectangle", problem, steps, answer

    def _generate_sector(self):
        angle = random.choice(self.SECTOR_ANGLES)
        frac_step, answer = self._ratio_step(angle, 360)
        steps = [
            step("GEO_PROB_SETUP", "full circle", f"sector angle {angle}°"),
            step("MEASURE_TOTAL", "full circle angle", 360),
            step("MEASURE_FAVORABLE", "sector angle", angle),
            step("GEO_PROB_FORMULA",
                 "probability = sector angle / 360"),
            frac_step,
            step("CHECK", f"{angle} <= 360",
                 "probability is at most 1"),
            step("Z", answer),
        ]
        problem = (
            f"A point is chosen uniformly at random in a circle. What is "
            f"the probability that it lands in a sector with central angle "
            f"{angle} degrees? Give an exact answer."
        )
        return "sector", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "interval":
            op_suffix, problem, steps, answer = self._generate_interval()
        elif variant == "rectangle":
            op_suffix, problem, steps, answer = self._generate_rectangle()
        else:
            op_suffix, problem, steps, answer = self._generate_sector()

        return dict(
            problem_id=jid(),
            operation=f"geometric_probability_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
