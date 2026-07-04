import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class GaussianCurvatureGenerator(ProblemGenerator):
    """
    Gaussian curvature for hand-friendly surfaces.

    Variants:
    - sphere: K = 1/R^2.
    - saddle: graph z = (a/2)x^2 - (b/2)y^2 at the origin, using
      K = (f_xx f_yy - f_xy^2)/(1 + f_x^2 + f_y^2)^2.

    Op-codes used:
    - GAUSSIAN_CURVATURE_SETUP / FORMULA / DERIV / CHECK
    - E / M / S / A / D (established/shared): exact arithmetic
    - Z: exact curvature
    """

    VARIANTS = ["sphere", "saddle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "sphere":
            problem, steps, answer = self._generate_sphere()
        else:
            problem, steps, answer = self._generate_saddle()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"gaussian_curvature_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_sphere(self):
        radius = random.randint(2, 160)
        radius_sq = radius * radius
        curvature = Fraction(1, radius_sq)
        steps = [
            step("GAUSSIAN_CURVATURE_SETUP", "sphere", f"R={radius}"),
            step("FORMULA", "K = 1/R^2"),
            step("E", radius, 2, radius_sq),
            step("D", 1, radius_sq, fraction_text(curvature)),
            step("CHECK", "positive curvature", fraction_text(curvature),
                 "sphere"),
        ]
        answer = f"K = {fraction_text(curvature)}"
        problem = (
            f"Find the Gaussian curvature of a sphere of radius {radius}."
        )
        return problem, steps, answer

    def _generate_saddle(self):
        a = random.randint(1, 24)
        b = random.randint(1, 24)
        f_xx = a
        f_yy = -b
        f_xy = 0
        numerator_left = f_xx * f_yy
        numerator_right = f_xy ** 2
        numerator = numerator_left - numerator_right
        grad_sum = 1
        denominator = grad_sum ** 2
        curvature = Fraction(numerator, denominator)
        steps = [
            step("GAUSSIAN_CURVATURE_SETUP", "saddle",
                 f"z=({a}x^2-{b}y^2)/2", "point=(0,0)"),
            step("FORMULA",
                 "K=(f_xx f_yy - f_xy^2)/(1+f_x^2+f_y^2)^2"),
            step("DERIV", "f_x=0, f_y=0", f"f_xx={f_xx}",
                 f"f_yy={f_yy}, f_xy={f_xy}"),
            step("M", f_xx, f_yy, numerator_left),
            step("E", f_xy, 2, numerator_right),
            step("S", numerator_left, numerator_right, numerator),
            step("A", 1, 0, grad_sum),
            step("E", grad_sum, 2, denominator),
            step("D", numerator, denominator, fraction_text(curvature)),
            step("CHECK", "negative curvature", fraction_text(curvature),
                 "saddle"),
        ]
        answer = f"K = {fraction_text(curvature)}"
        problem = (
            f"For the saddle surface z=({a}x^2-{b}y^2)/2, find "
            f"the Gaussian curvature at the origin using the graph "
            f"curvature formula."
        )
        return problem, steps, answer
