import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search
from generators.domain_range_generator import lin
from generators.polynomial_long_division_generator import poly_txt


class AreaBetweenCurvesGenerator(ProblemGenerator):
    """
    Area between curves with integer intersections by construction:
    set the curves equal, factor to find the bounds, check which
    curve is on top at the midpoint, integrate the difference with
    exact fractions.

    Variants:
    - line_parabola: y = x² vs the secant line through (p, p²), (q, q²)
    - parabola_pair: y = x² vs y = 2k² - x², symmetric about 0

    Op-codes used:
    - AREA_SETUP / EQ_SETUP / MOVE_TERM / FACTOR_PAIR_GOAL / TRY /
      REJECT / ACCEPT / ZERO_PRODUCT (established)
    - CHECK: midpoint comparison to pick the top curve (established)
    - REWRITE / INTEG_RULE / ANTIDERIV / SUBST / EVAL / S
      (established, exact fractions)
    - Z: the exact area
    """

    VARIANTS = ["line_parabola", "parabola_pair"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "line_parabola":
            while True:
                p = random.randint(-6, 5)
                q = p + random.randint(1, 6)
                if p != 0 and q != 0:
                    break
            m = p + q
            b = -p * q
            line = lin(m, b, "x") if m != 0 else str(b)
            area = Fraction((q - p) ** 3, 6)
            mid = Fraction(p + q, 2)
            line_mid = m * mid + b
            para_mid = mid * mid
            steps = [
                step("AREA_SETUP", f"y = x^2 and y = {line}",
                     "area between the curves"),
                step("EQ_SETUP", f"x^2 = {line}", "find intersections"),
                step("MOVE_TERM", "everything to the left",
                     f"{poly_txt([1, -m, -b], 'x')} = 0"),
            ]
            mm, nn = pair_search(steps, p * q, -(p + q))
            f1, f2 = binomial("x", mm), binomial("x", nn)
            steps.append(step("ZERO_PRODUCT", f"{f1}{f2} = 0",
                              f"x = {p} or x = {q}"))
            steps.append(step("CHECK", f"midpoint x = {mid}",
                              f"line = {line_mid}, parabola = "
                              f"{para_mid}", "line is on top"))
            steps.append(step("REWRITE",
                              f"A = ∫ from {p} to {q} of "
                              f"({line} - x^2) dx"))
            F_txt = (f"F(x) = {Fraction(m, 2)}x^2 + {b}x - (1/3)x^3"
                     .replace("+ -", "- "))
            steps.append(step("ANTIDERIV", f"{line} - x^2", F_txt))

            def F(x):
                return Fraction(m, 2) * x * x + b * x - \
                    Fraction(x ** 3, 3)
            steps.append(step("EVAL", f"F({q})", F(q)))
            steps.append(step("EVAL", f"F({p})", F(p)))
            steps.append(step("S", F(q), F(p), area))
            answer = str(area)
            problem = (f"Find the area between y = x^2 and "
                       f"y = {line}.")
        else:
            k = random.randint(1, 7)
            c = 2 * k * k
            area = Fraction(8 * k ** 3, 3)
            steps = [
                step("AREA_SETUP", f"y = x^2 and y = {c} - x^2",
                     "area between the curves"),
                step("EQ_SETUP", f"x^2 = {c} - x^2",
                     "find intersections"),
                step("EQ_OP_BOTH", "add", "x^2", "2x^2", c),
                step("EQ_OP_BOTH", "divide", 2, "x^2", k * k),
                step("REWRITE", f"x = ±{k}"),
                step("CHECK", "midpoint x = 0",
                     f"upper = {c}, lower = 0",
                     f"{c} - x^2 is on top"),
                step("REWRITE",
                     f"A = ∫ from {-k} to {k} of "
                     f"({c} - 2x^2) dx"),
                step("ANTIDERIV", f"{c} - 2x^2",
                     f"F(x) = {c}x - (2/3)x^3"),
            ]

            def F(x):
                return c * x - Fraction(2 * x ** 3, 3)
            steps.append(step("EVAL", f"F({k})", F(k)))
            steps.append(step("EVAL", f"F({-k})", F(-k)))
            steps.append(step("S", F(k), F(-k), area))
            answer = str(area)
            problem = (f"Find the area between y = x^2 and "
                       f"y = {c} - x^2.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"area_between_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
