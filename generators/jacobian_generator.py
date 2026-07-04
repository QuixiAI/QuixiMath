import random

from base_generator import ProblemGenerator
from helpers import step, jid


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


def factor_text(value):
    return f"({value})" if value < 0 else str(value)


class JacobianGenerator(ProblemGenerator):
    """
    Jacobian determinants and linear change-of-variables area scaling.

    Variants:
    - determinant: compute d(x,y)/d(u,v)
    - area_scale: use |J| to scale a rectangle in the uv-plane

    Op-codes used:
    - JAC_SETUP: transformation and target
    - PARTIAL_RESULT (established): x_u, x_v, y_u, y_v
    - JAC_MATRIX: assemble the 2x2 derivative matrix
    - JAC_DET: determinant arithmetic
    - AREA_SCALE: multiply uv-area by |J|
    - Z: determinant or scaled area
    """

    VARIANTS = ["determinant", "area_scale"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _matrix():
        while True:
            a = random.choice([v for v in range(-5, 6) if v != 0])
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            d = random.choice([v for v in range(-5, 6) if v != 0])
            det = a * d - b * c
            if det != 0:
                return a, b, c, d, det

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b, c, d, det = self._matrix()
        x_txt = fmt_linear([(a, "u"), (b, "v")])
        y_txt = fmt_linear([(c, "u"), (d, "v")])
        steps = [
            step("JAC_SETUP", f"x = {x_txt}", f"y = {y_txt}",
                 "d(x,y)/d(u,v)"),
            step("PARTIAL_RESULT", "x_u", a),
            step("PARTIAL_RESULT", "x_v", b),
            step("PARTIAL_RESULT", "y_u", c),
            step("PARTIAL_RESULT", "y_v", d),
            step("JAC_MATRIX", "[[x_u, x_v], [y_u, y_v]]",
                 f"[[{a}, {b}], [{c}, {d}]]"),
            step("JAC_DET", "x_u*y_v - x_v*y_u",
                 f"{factor_text(a)}*{factor_text(d)} - "
                 f"{factor_text(b)}*{factor_text(c)}", det),
        ]

        if variant == "determinant":
            answer = f"Jacobian determinant {det}"
            problem = (
                f"For the change of variables x = {x_txt}, y = {y_txt}, "
                f"compute the Jacobian determinant d(x,y)/d(u,v)."
            )
        else:
            u_max = random.randint(2, 9)
            v_max = random.randint(2, 9)
            uv_area = u_max * v_max
            area = abs(det) * uv_area
            steps.extend([
                step("AREA_SCALE", "uv rectangle area",
                     f"{u_max}*{v_max}", uv_area),
                step("AREA_SCALE", "image area",
                     f"abs({det})*{uv_area}", area),
            ])
            answer = f"image area {area}"
            problem = (
                f"Use x = {x_txt}, y = {y_txt} to find the area of the "
                f"image of 0 <= u <= {u_max}, 0 <= v <= {v_max}."
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"jacobian_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
