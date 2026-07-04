import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_coeff(coeff, body):
    if coeff == 1:
        return body
    return f"{coeff}*{body}"


def mul_expr(coeff, body):
    return body if coeff == 1 else f"{coeff}*{body}"


def square_coeff_expr(coeff, body):
    return body if coeff == 1 else f"{coeff}^2*{body}"


class CentroidGenerator(ProblemGenerator):
    """
    Centroids of plane regions using area and moment integrals.

    Variants:
    - line_region:      region under y = m*x
    - parabola_region:  region under y = k*x^2

    Op-codes used:
    - CENTROID_SETUP: region and target
    - AREA_INT: area integral
    - MOMENT_Y: integral for M_y = int x dA
    - MOMENT_X: integral for M_x = int y dA
    - CENTROID_COORD: divide moments by area
    - Z: centroid
    """

    VARIANTS = ["line_region", "parabola_region"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "line_region":
            slope = random.randint(1, 8)
            width = random.randint(2, 18)
            y_txt = fmt_coeff(slope, "x")
            area = Fraction(slope * width * width, 2)
            moment_y = Fraction(slope * width ** 3, 3)
            moment_x = Fraction(slope * slope * width ** 3, 6)
            xbar = moment_y / area
            ybar = moment_x / area
            steps = [
                step("CENTROID_SETUP", f"0 <= y <= {y_txt}",
                     f"0 <= x <= {width}", "centroid"),
                step("AREA_INT", "A = int y dx",
                     mul_expr(slope, f"{width}^2/2"), fmt_frac(area)),
                step("MOMENT_Y", "M_y = int x*y dx",
                     mul_expr(slope, f"{width}^3/3"),
                     fmt_frac(moment_y)),
                step("MOMENT_X", "M_x = 1/2 int y^2 dx",
                     square_coeff_expr(slope, f"{width}^3/6"),
                     fmt_frac(moment_x)),
                step("CENTROID_COORD", "xbar = M_y/A",
                     f"({fmt_frac(moment_y)})/({fmt_frac(area)})",
                     fmt_frac(xbar)),
                step("CENTROID_COORD", "ybar = M_x/A",
                     f"({fmt_frac(moment_x)})/({fmt_frac(area)})",
                     fmt_frac(ybar)),
            ]
            answer = f"centroid ({fmt_frac(xbar)}, {fmt_frac(ybar)})"
            problem = (
                f"Find the centroid of the region under y = {y_txt} "
                f"from x = 0 to x = {width} using moments."
            )
        else:
            coeff = random.randint(1, 8)
            width = random.randint(2, 12)
            y_txt = fmt_coeff(coeff, "x^2")
            area = Fraction(coeff * width ** 3, 3)
            moment_y = Fraction(coeff * width ** 4, 4)
            moment_x = Fraction(coeff * coeff * width ** 5, 10)
            xbar = moment_y / area
            ybar = moment_x / area
            steps = [
                step("CENTROID_SETUP", f"0 <= y <= {y_txt}",
                     f"0 <= x <= {width}", "centroid"),
                step("AREA_INT", "A = int y dx",
                     mul_expr(coeff, f"{width}^3/3"), fmt_frac(area)),
                step("MOMENT_Y", "M_y = int x*y dx",
                     mul_expr(coeff, f"{width}^4/4"),
                     fmt_frac(moment_y)),
                step("MOMENT_X", "M_x = 1/2 int y^2 dx",
                     square_coeff_expr(coeff, f"{width}^5/10"),
                     fmt_frac(moment_x)),
                step("CENTROID_COORD", "xbar = M_y/A",
                     f"({fmt_frac(moment_y)})/({fmt_frac(area)})",
                     fmt_frac(xbar)),
                step("CENTROID_COORD", "ybar = M_x/A",
                     f"({fmt_frac(moment_x)})/({fmt_frac(area)})",
                     fmt_frac(ybar)),
            ]
            answer = f"centroid ({fmt_frac(xbar)}, {fmt_frac(ybar)})"
            problem = (
                f"Find the centroid of the region under y = {y_txt} "
                f"from x = 0 to x = {width} using moments."
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"centroid_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
