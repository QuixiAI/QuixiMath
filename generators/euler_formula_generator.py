import random

from base_generator import ProblemGenerator
from helpers import step, jid


ANGLE_DATA = {
    0: ("0", "1", "0"),
    45: ("pi/4", "sqrt2/2", "sqrt2/2"),
    90: ("pi/2", "0", "1"),
    135: ("3pi/4", "-sqrt2/2", "sqrt2/2"),
    180: ("pi", "-1", "0"),
    225: ("5pi/4", "-sqrt2/2", "-sqrt2/2"),
    270: ("3pi/2", "0", "-1"),
    315: ("7pi/4", "sqrt2/2", "-sqrt2/2"),
}


def cx_int(real, imag):
    if imag == 0:
        return str(real)
    if imag == 1:
        imag_text = "i"
    elif imag == -1:
        imag_text = "-i"
    else:
        imag_text = f"{imag}i"
    if real == 0:
        return imag_text
    if imag > 0:
        return f"{real} + {imag_text}"
    return f"{real} - {imag_text.lstrip('-')}"


def cx_exact(real, imag):
    if imag == "0":
        return real
    imag_abs = imag.lstrip("-")
    imag_part = "i" if imag_abs == "1" else f"{imag_abs}i"
    if real == "0":
        return f"-{imag_part}" if imag.startswith("-") else imag_part
    if imag.startswith("-"):
        return f"{real} - {imag_part}"
    return f"{real} + {imag_part}"


def radius_text(a, b):
    if a == 0:
        return str(abs(b))
    if b == 0:
        return str(abs(a))
    scale = abs(a)
    return "sqrt2" if scale == 1 else f"{scale}sqrt2"


def scale_trig(radius, trig_value):
    if trig_value == "0":
        return "0"
    if trig_value == "1":
        return str(radius)
    if trig_value == "-1":
        return str(-radius)
    sign = "-" if trig_value.startswith("-") else ""
    # The non-axis values are +/-sqrt2/2 and radius is chosen even.
    factor = radius // 2
    body = "sqrt2" if factor == 1 else f"{factor}sqrt2"
    return f"{sign}{body}"


class EulerFormulaGenerator(ProblemGenerator):
    """
    Euler's formula conversions among rectangular, polar, and exponential
    complex forms, including Euler's identity.

    Variants:
    - rect_to_forms: a+bi -> r cis(theta) -> r e^(i theta)
    - polar_to_forms: r cis(theta) -> a+bi -> r e^(i theta)
    - identity: e^(i*pi)+1 = 0

    Op-codes used:
    - EULER_SETUP / EULER_FORMULA: formula and conversion context
    - ARGUMENT / POLAR_FORM / RECT_FORM / EXP_FORM: form conversions
    - TABLE_LOOKUP / SCALE_EXACT / ROOT_SIMPLIFY / REWRITE: exact values
    - E / A (established/shared): modulus and identity arithmetic
    - Z: final converted form
    """

    VARIANTS = ["rect_to_forms", "polar_to_forms", "identity"]

    RECT_POINTS = (
        [(scale, 0, 0) for scale in range(1, 13)] +
        [(0, scale, 90) for scale in range(1, 13)] +
        [(-scale, 0, 180) for scale in range(1, 13)] +
        [(0, -scale, 270) for scale in range(1, 13)] +
        [(scale, scale, 45) for scale in range(1, 13)] +
        [(-scale, scale, 135) for scale in range(1, 13)] +
        [(-scale, -scale, 225) for scale in range(1, 13)] +
        [(scale, -scale, 315) for scale in range(1, 13)]
    )

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rect_to_forms":
            problem, steps, answer = self._generate_rect_to_forms()
        elif variant == "polar_to_forms":
            problem, steps, answer = self._generate_polar_to_forms()
        else:
            problem, steps, answer = self._generate_identity()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"euler_formula_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_rect_to_forms(self):
        real, imag, angle = random.choice(self.RECT_POINTS)
        theta_rad = ANGLE_DATA[angle][0]
        r_text = radius_text(real, imag)
        square_sum = real * real + imag * imag
        z_text = cx_int(real, imag)
        steps = [
            step("EULER_SETUP", "rectangular to polar/exponential",
                 f"z={z_text}"),
            step("E", real, 2, real * real),
            step("E", imag, 2, imag * imag),
            step("A", real * real, imag * imag, square_sum),
            step("ROOT_SIMPLIFY", f"sqrt({square_sum})", r_text),
            step("ARGUMENT", f"({real},{imag})", f"{angle} deg"),
            step("POLAR_FORM", f"{r_text} cis({angle} deg)"),
            step("EXP_FORM", f"{r_text} e^(i*{theta_rad})"),
        ]
        answer = (
            f"polar = {r_text} cis({angle} deg); "
            f"exponential = {r_text} e^(i*{theta_rad})"
        )
        problem = f"Convert z = {z_text} to polar and exponential form."
        return problem, steps, answer

    def _generate_polar_to_forms(self):
        angle = random.choice(list(ANGLE_DATA))
        theta_rad, cos_text, sin_text = ANGLE_DATA[angle]
        if "sqrt2/2" in cos_text or "sqrt2/2" in sin_text:
            radius = random.choice(list(range(2, 31, 2)))
        else:
            radius = random.randint(1, 30)
        real = scale_trig(radius, cos_text)
        imag = scale_trig(radius, sin_text)
        rect = cx_exact(real, imag)
        steps = [
            step("EULER_SETUP", "polar to rectangular/exponential",
                 f"r={radius}", f"theta={angle} deg"),
            step("EULER_FORMULA", "e^(i theta)=cos theta+i sin theta"),
            step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
            step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
            step("SCALE_EXACT", f"{radius}*cos", real),
            step("SCALE_EXACT", f"{radius}*sin", imag),
            step("RECT_FORM", rect),
            step("EXP_FORM", f"{radius} e^(i*{theta_rad})"),
        ]
        answer = (
            f"rectangular = {rect}; "
            f"exponential = {radius} e^(i*{theta_rad})"
        )
        problem = (
            f"Convert z = {radius} cis({angle} deg) to rectangular and "
            "exponential form."
        )
        return problem, steps, answer

    def _generate_identity(self):
        steps = [
            step("EULER_SETUP", "Euler identity", "theta=pi"),
            step("EULER_FORMULA", "e^(i theta)=cos theta+i sin theta"),
            step("TABLE_LOOKUP", "cos pi", "-1"),
            step("TABLE_LOOKUP", "sin pi", "0"),
            step("REWRITE", "e^(i*pi)=-1+0i", "-1"),
            step("A", -1, 1, 0),
        ]
        answer = "0"
        problem = "Use Euler's formula to evaluate e^(i*pi)+1."
        return problem, steps, answer
