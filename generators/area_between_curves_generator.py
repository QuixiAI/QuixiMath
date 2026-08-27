import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search
from generators.domain_range_generator import lin
from generators.polynomial_long_division_generator import poly_txt


# Integer intersection pairs (p, q), p < q, both nonzero so the factor
# pair search always has a nonzero product to sweep.
PAIRS = [(p, q)
         for p in range(-10, 11) if p != 0
         for q in range(p + 1, min(11, p + 10)) if q != 0]

SHIFTS = list(range(-9, 10))       # the parabola's x coefficient
LIFTS = list(range(-12, 13))       # the parabola's constant term

TEMPLATES = [
    "Find the area between y = {f} and y = {g}.",
    "Find the area of the region bounded by the curves y = {f} and "
    "y = {g}.",
    "The curves y = {f} and y = {g} enclose a region. Find its area.",
    "Compute the exact area of the region between y = {f} and y = {g}.",
    "Find the area enclosed by the graphs of y = {f} and y = {g}.",
    "Two curves, y = {f} and y = {g}, intersect at two points. Find the "
    "area of the region between them.",
]


def antideriv_txt(cubic, square, linear):
    """'F(x) = -(1/3)x^3 + (5/2)x^2 - 6x' from exact coefficients."""
    parts = []
    for coef, power in ((cubic, 3), (square, 2), (linear, 1)):
        if coef == 0:
            continue
        magnitude = abs(coef)
        if magnitude == 1:
            body = ""
        elif magnitude.denominator == 1:
            body = str(magnitude.numerator)
        else:
            body = f"({magnitude})"
        term = f"{body}x^{power}" if power > 1 else f"{body}x"
        if not parts:
            parts.append(f"-{term}" if coef < 0 else term)
        else:
            parts.append(f"+ {term}" if coef > 0 else f"- {term}")
    return "F(x) = " + (" ".join(parts) if parts else "0")


class AreaBetweenCurvesGenerator(ProblemGenerator):
    """
    Area between curves with integer intersections by construction:
    set the curves equal, factor to find the bounds, check which
    curve is on top at the midpoint, integrate the difference with
    exact fractions.

    Variants:
    - line_parabola: y = x² + Bx + C vs the secant line through its
      points at x = p and x = q
    - parabola_pair: an upward parabola vs a downward one meeting at
      x = p and x = q

    Op-codes used:
    - AREA_SETUP / EQ_SETUP / MOVE_TERM / FACTOR_PAIR_GOAL / TRY /
      REJECT / ACCEPT / ZERO_PRODUCT / EQ_OP_BOTH (established)
    - CHECK: midpoint comparison to pick the top curve (established)
    - REWRITE / ANTIDERIV / EVAL / S (established, exact fractions)
    - Z: the exact area
    """

    VARIANTS = ["line_parabola", "parabola_pair"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        p, q = random.choice(PAIRS)
        total, product = p + q, p * q
        mid = Fraction(p + q, 2)

        if variant == "line_parabola":
            shift = random.choice(SHIFTS)
            lift = random.choice(LIFTS)
            para = poly_txt([1, shift, lift], "x")
            slope = shift + total
            intercept = lift - product
            line = lin(slope, intercept, "x") if slope != 0 \
                else str(intercept)
            top, bottom = line, para
            area = Fraction((q - p) ** 3, 6)
            cubic = Fraction(-1, 3)
            square = Fraction(total, 2)
            linear = Fraction(-product)
            integrand = poly_txt([-1, total, -product], "x")
            steps = [
                step("AREA_SETUP", f"y = {para} and y = {line}",
                     "area between the curves"),
                step("EQ_SETUP", f"{para} = {line}", "find intersections"),
                step("MOVE_TERM", "everything to the left",
                     f"{poly_txt([1, -total, product], 'x')} = 0"),
            ]
            mm, nn = pair_search(steps, product, -total)
            steps.append(step("ZERO_PRODUCT",
                              f"{binomial('x', mm)}{binomial('x', nn)} = 0",
                              f"x = {p} or x = {q}"))
            line_mid = slope * mid + intercept
            para_mid = mid * mid + shift * mid + lift
            steps.append(step("CHECK", f"midpoint x = {mid}",
                              f"line = {line_mid}, parabola = {para_mid}",
                              "line is on top"))
        else:
            shift = random.choice(SHIFTS)
            lift = random.choice(LIFTS)
            down = poly_txt([-1, shift, lift], "x")
            up_shift = shift - 2 * total
            up_lift = lift + 2 * product
            up = poly_txt([1, up_shift, up_lift], "x")
            top, bottom = down, up
            area = Fraction((q - p) ** 3, 3)
            cubic = Fraction(-2, 3)
            square = Fraction(total)
            linear = Fraction(-2 * product)
            integrand = poly_txt([-2, 2 * total, -2 * product], "x")
            reduced = poly_txt([1, -total, product], "x")
            steps = [
                step("AREA_SETUP", f"y = {up} and y = {down}",
                     "area between the curves"),
                step("EQ_SETUP", f"{up} = {down}", "find intersections"),
                step("MOVE_TERM", "everything to the left",
                     f"{poly_txt([2, -2 * total, 2 * product], 'x')} = 0"),
                step("EQ_OP_BOTH", "divide", 2, reduced, 0),
            ]
            mm, nn = pair_search(steps, product, -total)
            steps.append(step("ZERO_PRODUCT",
                              f"{binomial('x', mm)}{binomial('x', nn)} = 0",
                              f"x = {p} or x = {q}"))
            down_mid = -mid * mid + shift * mid + lift
            up_mid = mid * mid + up_shift * mid + up_lift
            steps.append(step("CHECK", f"midpoint x = {mid}",
                              f"upper = {down_mid}, lower = {up_mid}",
                              f"{down} is on top"))

        steps.append(step("REWRITE",
                          f"A = ∫ from {p} to {q} of ({top} - ({bottom})) dx"))
        steps.append(step("REWRITE",
                          f"A = ∫ from {p} to {q} of ({integrand}) dx"))
        steps.append(step("ANTIDERIV", integrand,
                          antideriv_txt(cubic, square, linear)))

        def evaluate(x):
            return cubic * x ** 3 + square * x * x + linear * x

        steps.append(step("EVAL", f"F({q})", evaluate(q)))
        steps.append(step("EVAL", f"F({p})", evaluate(p)))
        steps.append(step("S", evaluate(q), evaluate(p), area))
        answer = str(area)
        steps.append(step("Z", answer))

        first, second = (top, bottom) if random.random() < 0.5 \
            else (bottom, top)
        problem = random.choice(TEMPLATES).format(f=first, g=second)

        return dict(
            problem_id=jid(),
            operation=f"area_between_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
