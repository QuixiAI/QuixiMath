import random

from base_generator import ProblemGenerator
from helpers import step, jid


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


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


def fx_formula(a, c, d):
    return fmt_linear([(2 * a, "x"), (c, "y"), (d, "")])


def fy_formula(b, c, e):
    return fmt_linear([(2 * b, "y"), (c, "x"), (e, "")])


class HessianClassifyGenerator(ProblemGenerator):
    """
    Critical points of quadratic two-variable functions classified by the
    second-partials / Hessian determinant test.

    Variants:
    - local_min: positive definite Hessian
    - local_max: negative definite Hessian
    - saddle:    indefinite Hessian

    Op-codes used:
    - HESSIAN_SETUP: function and task
    - PARTIAL_RESULT (established): f_x and f_y formulas
    - CRIT_EQS: set the first partials equal to zero
    - CRIT_SOLVE: Cramer's-rule arithmetic for the critical point
    - CHECK (established): verify the gradient is zero at the point
    - SECOND_PARTIAL: f_xx, f_xy, and f_yy values
    - HESSIAN_DET: determinant D = f_xx*f_yy - f_xy^2
    - HESSIAN_TEST: second-partials test conclusion
    - Z: classified critical point
    """

    VARIANTS = ["local_min", "local_max", "saddle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _hessian_coeffs(variant):
        while True:
            if variant == "local_min":
                a = random.randint(1, 5)
                b = random.randint(1, 5)
                c = random.randint(-4, 4)
            elif variant == "local_max":
                a = random.randint(-5, -1)
                b = random.randint(-5, -1)
                c = random.randint(-4, 4)
            else:
                a = random.choice([v for v in range(-5, 6) if v != 0])
                b = random.choice([v for v in range(-5, 6) if v != 0])
                c = random.randint(-6, 6)
            det = 4 * a * b - c * c
            if variant in {"local_min", "local_max"} and det > 0:
                return a, b, c, det
            if variant == "saddle" and det < 0:
                return a, b, c, det

    @staticmethod
    def _classification(det, f_xx):
        if det < 0:
            return "saddle point"
        return "local minimum" if f_xx > 0 else "local maximum"

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b, c, det = self._hessian_coeffs(variant)
        x0 = random.randint(-4, 4)
        y0 = random.randint(-4, 4)
        f_xx = 2 * a
        f_xy = c
        f_yy = 2 * b
        d = -(f_xx * x0 + f_xy * y0)
        e = -(f_xy * x0 + f_yy * y0)
        f_txt = fmt_formula(a, b, c, d, e)
        fx_txt = fx_formula(a, c, d)
        fy_txt = fy_formula(b, c, e)
        rhs_x = -d
        rhs_y = -e
        x_num = rhs_x * f_yy - f_xy * rhs_y
        y_num = f_xx * rhs_y - rhs_x * f_xy
        classification = self._classification(det, f_xx)
        answer = f"critical point ({x0}, {y0}): {classification}"

        steps = [
            step("HESSIAN_SETUP", f"f(x,y) = {f_txt}",
                 "find and classify the critical point"),
            step("PARTIAL_RESULT", "f_x", fx_txt),
            step("PARTIAL_RESULT", "f_y", fy_txt),
            step("CRIT_EQS", "f_x = 0", f"{fx_txt} = 0"),
            step("CRIT_EQS", "f_y = 0", f"{fy_txt} = 0"),
            step("CRIT_SOLVE", "det",
                 f"{factor_text(f_xx)}*{factor_text(f_yy)} - "
                 f"{factor_text(f_xy)}^2", det),
            step("CRIT_SOLVE", "x",
                 f"{factor_text(x_num)}/{factor_text(det)}", x0),
            step("CRIT_SOLVE", "y",
                 f"{factor_text(y_num)}/{factor_text(det)}", y0),
            step("CHECK", f"gradient at ({x0}, {y0})",
                 "f_x = 0, f_y = 0", "critical point"),
            step("SECOND_PARTIAL", "f_xx", f_xx),
            step("SECOND_PARTIAL", "f_xy", f_xy),
            step("SECOND_PARTIAL", "f_yy", f_yy),
            step("HESSIAN_DET", "D = f_xx*f_yy - f_xy^2",
                 f"{factor_text(f_xx)}*{factor_text(f_yy)} - "
                 f"{factor_text(f_xy)}^2", det),
            step("HESSIAN_TEST", f"D = {det}",
                 f"f_xx = {f_xx}", classification),
            step("Z", answer),
        ]
        problem = (
            f"For f(x,y) = {f_txt}, find the critical point and classify "
            f"it using the Hessian test."
        )

        return dict(
            problem_id=jid(),
            operation=f"hessian_classify_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
