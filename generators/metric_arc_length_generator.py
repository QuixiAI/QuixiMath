import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


THETA_CHOICES = [
    Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
    Fraction(2, 3), Fraction(3, 4), Fraction(1, 1),
]


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


class MetricArcLengthGenerator(ProblemGenerator):
    """
    Arc length from a metric along simple polar-coordinate paths.

    Variants:
    - radial: theta constant, ds = dr.
    - circle: r constant, ds = r dtheta.

    Op-codes used:
    - METRIC_ARC_SETUP / METRIC_RESTRICT / INTEGRAL_SETUP
    - E / S / ROOT / M (established/shared): exact arithmetic
    - Z: exact length
    """

    VARIANTS = ["radial", "circle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "radial":
            problem, steps, answer = self._generate_radial()
        else:
            problem, steps, answer = self._generate_circle()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"metric_arc_length_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_radial(self):
        start = random.randint(1, 30)
        length = random.randint(1, 30)
        end = start + length
        theta0 = random.choice([0, 30, 45, 60, 90, 120])
        steps = [
            step("METRIC_ARC_SETUP", "polar metric",
                 "ds^2=dr^2+r^2 dtheta^2",
                 f"theta={theta0} deg, r:{start}->{end}"),
            step("METRIC_RESTRICT", "dtheta=0", "ds^2=dr^2"),
            step("INTEGRAL_SETUP", "L = integral from r0 to r1 of 1 dr"),
            step("S", end, start, length),
            step("M", 1, length, length),
        ]
        answer = f"length = {length}"
        problem = (
            f"In polar coordinates with metric ds^2=dr^2+r^2 dtheta^2, "
            f"find the length of the path theta={theta0} deg from "
            f"r={start} to r={end}."
        )
        return problem, steps, answer

    def _generate_circle(self):
        radius = random.randint(2, 30)
        theta = random.choice(THETA_CHOICES)
        radius_sq = radius * radius
        theta_text = pi_text(theta)
        length_coeff = radius * theta
        steps = [
            step("METRIC_ARC_SETUP", "polar metric",
                 "ds^2=dr^2+r^2 dtheta^2",
                 f"r={radius}, theta:0->{theta_text}"),
            step("METRIC_RESTRICT", "dr=0", "ds^2=r^2 dtheta^2"),
            step("E", radius, 2, radius_sq),
            step("ROOT", radius_sq, radius),
            step("INTEGRAL_SETUP",
                 f"L = integral from 0 to {theta_text} of {radius} dtheta"),
            step("M", radius, theta, length_coeff),
        ]
        answer = f"length = {pi_text(length_coeff)}"
        problem = (
            f"In polar coordinates with metric ds^2=dr^2+r^2 dtheta^2, "
            f"find the length of the path r={radius} from theta=0 "
            f"to theta={theta_text}."
        )
        return problem, steps, answer
