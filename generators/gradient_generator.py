import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def exact(fr):
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


def fmt_formula(a, b, c, d, e):
    raw_terms = [
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ]
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        prefix = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        if not pieces:
            pieces.append(prefix if coeff > 0 else f"-{prefix}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + prefix)
    return " ".join(pieces) if pieces else "0"


def fx_formula(a, c, d):
    return fmt_linear([(2 * a, "x"), (c, "y"), (d, "")])


def fy_formula(b, c, e):
    return fmt_linear([(2 * b, "y"), (c, "x"), (e, "")])


def fmt_linear(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        if body:
            text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        else:
            text = str(abs(coeff))
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def fmt_eval_sum(raw_terms):
    pieces = []
    for coeff, value in raw_terms:
        term_value = coeff if value is None else coeff * value
        if term_value == 0:
            continue
        if value is None:
            text = str(abs(coeff))
        elif abs(coeff) == 1:
            text = str(value)
        else:
            text = f"{abs(coeff)}*{value}"
        if not pieces:
            pieces.append(text if term_value > 0 else f"-{text}")
        else:
            pieces.append(("+ " if term_value > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


def tangent_plane(z0, fx, fy, x0, y0):
    pieces = [f"z = {z0}"]
    for coeff, body in ((fx, f"(x - {x0})"), (fy, f"(y - {y0})")):
        if coeff == 0:
            continue
        term = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        pieces.append(("+ " if coeff > 0 else "- ") + term)
    return " ".join(pieces)


class GradientGenerator(ProblemGenerator):
    """
    Gradient, directional derivative, and tangent plane computations for
    quadratic functions f(x,y).

    Variants:
    - gradient:    compute ∇f(a,b)
    - directional: compute ∇f(a,b) · u for a supplied unit vector
    - tangent:     tangent plane to z = f(x,y) at (a,b)

    Op-codes used:
    - GRAD_SETUP: function, point, and target
    - PARTIAL_RESULT (established): f_x and f_y formulas
    - EVAL_PARTIAL: substitute the point into a partial derivative
    - DOT: directional derivative dot product
    - TANGENT_PLANE: assemble tangent plane
    - CHECK (established): point lies on the tangent plane
    - Z: final gradient, directional derivative, or plane
    """

    VARIANTS = ["gradient", "directional", "tangent"]
    UNIT_DIRECTIONS = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(-3, 5), Fraction(4, 5)),
        (Fraction(5, 13), Fraction(12, 13)),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _params():
        return (
            random.randint(1, 5),
            random.randint(1, 5),
            random.randint(-4, 4),
            random.randint(-6, 6),
            random.randint(-6, 6),
            random.randint(0, 4),
            random.randint(0, 4),
        )

    @staticmethod
    def _values(a, b, c, d, e, x0, y0):
        fx = 2 * a * x0 + c * y0 + d
        fy = 2 * b * y0 + c * x0 + e
        z0 = a * x0 * x0 + b * y0 * y0 + c * x0 * y0 + d * x0 + e * y0
        return fx, fy, z0

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b, c, d, e, x0, y0 = self._params()
        f_txt = fmt_formula(a, b, c, d, e)
        fx_txt = fx_formula(a, c, d)
        fy_txt = fy_formula(b, c, e)
        fx, fy, z0 = self._values(a, b, c, d, e, x0, y0)

        steps = [
            step("GRAD_SETUP", f"f(x,y) = {f_txt}",
                 f"point ({x0}, {y0})", variant),
            step("PARTIAL_RESULT", "f_x", fx_txt),
            step("PARTIAL_RESULT", "f_y", fy_txt),
            step("EVAL_PARTIAL", "f_x",
                 fmt_eval_sum([(2 * a, x0), (c, y0), (d, None)]), fx),
            step("EVAL_PARTIAL", "f_y",
                 fmt_eval_sum([(2 * b, y0), (c, x0), (e, None)]), fy),
        ]

        if variant == "gradient":
            answer = f"({fx}, {fy})"
            problem = (
                f"For f(x,y) = {f_txt}, find grad f at ({x0}, {y0})."
            )
        elif variant == "directional":
            ux, uy = random.choice(self.UNIT_DIRECTIONS)
            value = Fraction(fx) * ux + Fraction(fy) * uy
            answer = exact(value)
            steps.append(step("DOT", f"({fx}, {fy}) · ({ux}, {uy})",
                              f"{factor_text(fx)}*{factor_text(ux)} + "
                              f"{factor_text(fy)}*{factor_text(uy)}",
                              answer))
            problem = (
                f"For f(x,y) = {f_txt}, find the directional derivative "
                f"at ({x0}, {y0}) in direction u = ({ux}, {uy})."
            )
        else:
            plane = tangent_plane(z0, fx, fy, x0, y0)
            answer = plane
            steps.append(step("TANGENT_PLANE", "z = z0 + fx(x-a) + fy(y-b)",
                              plane))
            steps.append(step("CHECK", f"at ({x0}, {y0})",
                              f"z = {z0}", "passes through point"))
            problem = (
                f"Find the tangent plane to z = f(x,y) for f(x,y) = "
                f"{f_txt} at ({x0}, {y0})."
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"gradient_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
