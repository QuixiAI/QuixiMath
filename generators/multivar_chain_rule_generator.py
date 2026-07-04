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


def fmt_formula(a, b, c, d, e):
    return fmt_linear([
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ])


def fmt_eval_sum(raw_terms):
    pieces = []
    for coeff, value in raw_terms:
        term_value = coeff if value is None else coeff * value
        if term_value == 0:
            continue
        if value is None:
            text = factor_text(coeff)
        elif coeff == 1:
            text = factor_text(value)
        else:
            text = f"{factor_text(coeff)}*{factor_text(value)}"
        pieces.append(text)
    return " + ".join(pieces) if pieces else "0"


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


def product_sum_text(left_a, right_a, left_b, right_b):
    return (
        f"{factor_text(left_a)}*{factor_text(right_a)} + "
        f"{factor_text(left_b)}*{factor_text(right_b)}"
    )


def fx_formula(a, c, d):
    return fmt_linear([(2 * a, "x"), (c, "y"), (d, "")])


def fy_formula(b, c, e):
    return fmt_linear([(2 * b, "y"), (c, "x"), (e, "")])


class MultivarChainRuleGenerator(ProblemGenerator):
    """
    Multivariable chain rule and total differential computations for
    quadratic functions f(x,y).

    Variants:
    - path_derivative: z=f(x,y), x(t), y(t); find dz/dt
    - partial_s:       z=f(x,y), x(s,t), y(s,t); find dz/ds
    - total_diff:      compute df = f_x dx + f_y dy at a point

    Op-codes used:
    - MV_CHAIN_SETUP: function, substitutions, and target
    - DERIV_RULE (established): chain-rule or total-differential formula
    - PARTIAL_RESULT (established): f_x and f_y formulas
    - CHAIN_VALUE: substitute parameter values into x and y
    - EVAL_PARTIAL (established): substitute x,y into a partial derivative
    - CHAIN_RATE: derivative of a parameterized variable
    - CHAIN_SUM: assemble the chain-rule sum
    - DIFF_SETUP: function, point, and differentials
    - DIFF_SUM: assemble the total differential
    - Z: final numeric derivative or differential
    """

    VARIANTS = ["path_derivative", "partial_s", "total_diff"]
    SMALL_DELTAS = [
        Fraction(1, 2),
        Fraction(-1, 2),
        Fraction(1, 4),
        Fraction(-1, 4),
        Fraction(2, 5),
        Fraction(-2, 5),
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
        )

    @staticmethod
    def _values(a, b, c, d, e, x0, y0):
        fx = 2 * a * x0 + c * y0 + d
        fy = 2 * b * y0 + c * x0 + e
        return fx, fy

    @staticmethod
    def _base_steps(fx_txt, fy_txt, a, b, c, d, e, x0, y0):
        fx, fy = MultivarChainRuleGenerator._values(a, b, c, d, e, x0, y0)
        return [
            step("PARTIAL_RESULT", "f_x", fx_txt),
            step("PARTIAL_RESULT", "f_y", fy_txt),
            step("EVAL_PARTIAL", "f_x",
                 fmt_eval_sum([(2 * a, x0), (c, y0), (d, None)]), fx),
            step("EVAL_PARTIAL", "f_y",
                 fmt_eval_sum([(2 * b, y0), (c, x0), (e, None)]), fy),
        ], fx, fy

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b, c, d, e = self._params()
        f_txt = fmt_formula(a, b, c, d, e)
        fx_txt = fx_formula(a, c, d)
        fy_txt = fy_formula(b, c, e)

        if variant == "path_derivative":
            mx = random.choice([v for v in range(-4, 5) if v != 0])
            my = random.choice([v for v in range(-4, 5) if v != 0])
            bx = random.randint(-6, 6)
            by = random.randint(-6, 6)
            t0 = random.randint(-3, 3)
            x_txt = fmt_linear([(mx, "t"), (bx, "")])
            y_txt = fmt_linear([(my, "t"), (by, "")])
            x0 = mx * t0 + bx
            y0 = my * t0 + by
            partial_steps, fx, fy = self._base_steps(
                fx_txt, fy_txt, a, b, c, d, e, x0, y0)
            answer = fx * mx + fy * my
            steps = [
                step("MV_CHAIN_SETUP", f"z = f(x,y) = {f_txt}",
                     f"x = {x_txt}, y = {y_txt}", f"t = {t0}"),
                step("DERIV_RULE", "single-parameter chain rule",
                     "dz/dt = f_x*dx/dt + f_y*dy/dt"),
                step("CHAIN_VALUE", f"x({t0})",
                     fmt_eval_sum([(mx, t0), (bx, None)]), x0),
                step("CHAIN_VALUE", f"y({t0})",
                     fmt_eval_sum([(my, t0), (by, None)]), y0),
            ] + partial_steps + [
                step("CHAIN_RATE", "dx/dt", mx),
                step("CHAIN_RATE", "dy/dt", my),
                step("CHAIN_SUM", "f_x*dx/dt + f_y*dy/dt",
                     product_sum_text(fx, mx, fy, my), answer),
            ]
            problem = (
                f"Let z = f(x,y) = {f_txt}, where x = {x_txt} and "
                f"y = {y_txt}. Find dz/dt at t = {t0}."
            )
        elif variant == "partial_s":
            xs = random.choice([v for v in range(-4, 5) if v != 0])
            xt = random.choice([v for v in range(-3, 4) if v != 0])
            ys = random.choice([v for v in range(-4, 5) if v != 0])
            yt = random.choice([v for v in range(-3, 4) if v != 0])
            bx = random.randint(-5, 5)
            by = random.randint(-5, 5)
            s0 = random.randint(-2, 3)
            t0 = random.randint(-2, 3)
            x_txt = fmt_linear([(xs, "s"), (xt, "t"), (bx, "")])
            y_txt = fmt_linear([(ys, "s"), (yt, "t"), (by, "")])
            x0 = xs * s0 + xt * t0 + bx
            y0 = ys * s0 + yt * t0 + by
            partial_steps, fx, fy = self._base_steps(
                fx_txt, fy_txt, a, b, c, d, e, x0, y0)
            answer = fx * xs + fy * ys
            steps = [
                step("MV_CHAIN_SETUP", f"z = f(x,y) = {f_txt}",
                     f"x = {x_txt}, y = {y_txt}",
                     f"(s,t) = ({s0}, {t0})"),
                step("DERIV_RULE", "partial chain rule",
                     "dz/ds = f_x*x_s + f_y*y_s"),
                step("CHAIN_VALUE", f"x({s0},{t0})",
                     fmt_eval_sum([(xs, s0), (xt, t0), (bx, None)]), x0),
                step("CHAIN_VALUE", f"y({s0},{t0})",
                     fmt_eval_sum([(ys, s0), (yt, t0), (by, None)]), y0),
            ] + partial_steps + [
                step("CHAIN_RATE", "x_s", xs),
                step("CHAIN_RATE", "y_s", ys),
                step("CHAIN_SUM", "f_x*x_s + f_y*y_s",
                     product_sum_text(fx, xs, fy, ys), answer),
            ]
            problem = (
                f"Let z = f(x,y) = {f_txt}, where x = {x_txt} and "
                f"y = {y_txt}. Find dz/ds at (s, t) = ({s0}, {t0})."
            )
        else:
            x0 = random.randint(-3, 4)
            y0 = random.randint(-3, 4)
            dx = random.choice(self.SMALL_DELTAS)
            dy = random.choice(self.SMALL_DELTAS)
            partial_steps, fx, fy = self._base_steps(
                fx_txt, fy_txt, a, b, c, d, e, x0, y0)
            value = Fraction(fx) * dx + Fraction(fy) * dy
            answer = exact(value)
            steps = [
                step("DIFF_SETUP", f"f(x,y) = {f_txt}",
                     f"point ({x0}, {y0})", f"dx={dx}, dy={dy}"),
                step("DERIV_RULE", "total differential",
                     "df = f_x*dx + f_y*dy"),
            ] + partial_steps + [
                step("DIFF_SUM", "f_x*dx + f_y*dy",
                     product_sum_text(fx, dx, fy, dy), answer),
            ]
            problem = (
                f"For f(x,y) = {f_txt}, estimate df at ({x0}, {y0}) "
                f"when dx = {dx} and dy = {dy}."
            )

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"multivar_chain_rule_{variant}",
            problem=problem,
            steps=steps,
            final_answer=str(answer),
        )
