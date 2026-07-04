import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


class RegularPolygonAreaGenerator(ProblemGenerator):
    """
    Area of a regular polygon from its apothem: A = (1/2)·a·P. The
    perimeter is computed first, then the product, then the halving.
    The given apothem is the true value rounded to the nearest half so
    the numbers stay realistic for the named polygon.

    Op-codes used:
    - POLY_SETUP: the polygon, side, and apothem (description, goal)
    - POLY_FORMULA: A = (1/2)·a·P (established *_FORMULA shape)
    - M / D / EVAL: perimeter, product, halving (established)
    - Z: 'A square units' (exact decimal when the apothem is a half)
    """

    NAMES = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
             7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon"}

    def generate(self) -> dict:
        n = random.randint(5, 10)
        s = random.randint(4, 14)
        true_a = s / (2 * math.tan(math.pi / n))
        a = Fraction(round(true_a * 2), 2)  # nearest half, exact
        P = n * s
        area = a * P / 2

        a_txt = dec(a)
        steps = [
            step("POLY_SETUP",
                 f"regular {self.NAMES[n]}: n = {n}, side {s}, "
                 f"apothem {a_txt}", "area"),
            step("POLY_FORMULA", "A = (1/2)·a·P"),
            step("M", n, s, P),
            step("EVAL", "P", P),
            step("M", a_txt, P, dec(a * P)),
            step("D", dec(a * P), 2, dec(area)),
        ]
        answer = f"{dec(area)} square units"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="regular_polygon_area",
            problem=(f"A regular {self.NAMES[n]} has side length {s} and "
                     f"apothem {a_txt}. Find its area."),
            steps=steps,
            final_answer=answer,
        )
