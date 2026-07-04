import random

from base_generator import ProblemGenerator
from helpers import step, jid


TRIG = {
    0: ("1", "0"),
    30: ("sqrt3/2", "1/2"),
    45: ("sqrt2/2", "sqrt2/2"),
    60: ("1/2", "sqrt3/2"),
    90: ("0", "1"),
    120: ("-1/2", "sqrt3/2"),
    135: ("-sqrt2/2", "sqrt2/2"),
    150: ("-sqrt3/2", "1/2"),
    180: ("-1", "0"),
    210: ("-sqrt3/2", "-1/2"),
    225: ("-sqrt2/2", "-sqrt2/2"),
    240: ("-1/2", "-sqrt3/2"),
    270: ("0", "-1"),
    300: ("1/2", "-sqrt3/2"),
    315: ("sqrt2/2", "-sqrt2/2"),
    330: ("sqrt3/2", "-1/2"),
}


def scale_trig(radius, value):
    if value == "0":
        return "0"
    if value == "1":
        return str(radius)
    if value == "-1":
        return str(-radius)
    sign = "-" if value.startswith("-") else ""
    core = value.lstrip("-")
    if core == "1/2":
        return f"{sign}{radius // 2}" if radius % 2 == 0 else \
            f"{sign}{radius}/2"
    root = "sqrt2" if "sqrt2" in core else "sqrt3"
    if radius == 1:
        body = f"{root}/2"
    elif radius % 2 == 0:
        factor = radius // 2
        body = root if factor == 1 else f"{factor}{root}"
    else:
        body = f"{radius}{root}/2"
    return f"{sign}{body}"


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


def roots_text(radius, angles):
    prefix = "" if radius == 1 else f"{radius} "
    return ", ".join(f"{prefix}cis({angle} deg)" for angle in angles)


class DeMoivreGenerator(ProblemGenerator):
    """
    De Moivre powers, roots of unity, and roots of arbitrary complex numbers.

    Variants:
    - power: (r cis theta)^n
    - roots_unity: all n-th roots of 1
    - arbitrary_roots: all n-th roots of R cis theta

    Op-codes used:
    - DEMOIVRE_SETUP / DEMOIVRE_POWER: theorem setup and power result
    - ROOT / ROOT_ANGLE: root radius and argument list
    - TABLE_LOOKUP / SCALE_EXACT / RECT_FORM: exact rectangular conversion
    - E / M / A / D / MOD_REDUCE (established/shared): exact arithmetic
    - Z: final polar or rectangular result
    """

    VARIANTS = ["power", "roots_unity", "arbitrary_roots"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "power":
            problem, steps, answer = self._generate_power()
        elif variant == "roots_unity":
            problem, steps, answer = self._generate_roots_unity()
        else:
            problem, steps, answer = self._generate_arbitrary_roots()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"de_moivre_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_power(self):
        radius = random.randint(2, 7)
        theta = random.choice(list(TRIG))
        exponent = random.randint(2, 5)
        radius_power = radius ** exponent
        raw_angle = theta * exponent
        angle = raw_angle % 360
        cos_text, sin_text = TRIG[angle]
        real = scale_trig(radius_power, cos_text)
        imag = scale_trig(radius_power, sin_text)
        rect = cx_exact(real, imag)
        steps = [
            step("DEMOIVRE_SETUP", "power", f"r={radius}",
                 f"theta={theta} deg", f"n={exponent}"),
            step("E", radius, exponent, radius_power),
            step("M", theta, exponent, raw_angle),
            step("MOD_REDUCE", raw_angle, "mod 360", angle),
            step("DEMOIVRE_POWER", f"{radius_power} cis({angle} deg)"),
            step("TABLE_LOOKUP", f"cos {angle} deg", cos_text),
            step("TABLE_LOOKUP", f"sin {angle} deg", sin_text),
            step("SCALE_EXACT", f"{radius_power}*cos", real),
            step("SCALE_EXACT", f"{radius_power}*sin", imag),
            step("RECT_FORM", rect),
        ]
        answer = (
            f"polar = {radius_power} cis({angle} deg); "
            f"rectangular = {rect}"
        )
        problem = (
            f"Use De Moivre's theorem to compute "
            f"({radius} cis({theta} deg))^{exponent}."
        )
        return problem, steps, answer

    def _generate_roots_unity(self):
        n = random.choice([3, 4, 6, 8, 12])
        steps = [step("DEMOIVRE_SETUP", "roots_of_unity", f"n={n}")]
        angles = []
        for k in range(n):
            raw = 360 * k
            angle = raw // n
            steps.append(step("M", 360, k, raw))
            steps.append(step("D", raw, n, angle))
            steps.append(step("ROOT_ANGLE", f"k={k}", f"{angle} deg"))
            steps.append(step("ROOT", f"cis({angle} deg)"))
            angles.append(angle)
        answer = f"roots = {roots_text(1, angles)}"
        problem = f"Find all {n}-th roots of unity in polar form."
        return problem, steps, answer

    def _generate_arbitrary_roots(self):
        n = random.choice([2, 3, 4])
        rho = random.randint(2, 5)
        if n == 3:
            base_angle = random.choice([0, 30, 60, 90])
        else:
            base_angle = random.choice([0, 45, 90, 135])
        radius = rho ** n
        theta = (n * base_angle) % 360
        steps = [
            step("DEMOIVRE_SETUP", "arbitrary_roots", f"R={radius}",
                 f"theta={theta} deg", f"n={n}"),
            step("ROOT", radius, n, rho),
        ]
        angles = []
        for k in range(n):
            turn = 360 * k
            raw = theta + turn
            angle = raw // n
            steps.append(step("M", 360, k, turn))
            steps.append(step("A", theta, turn, raw))
            steps.append(step("D", raw, n, angle))
            steps.append(step("ROOT_ANGLE", f"k={k}", f"{angle} deg"))
            steps.append(step("ROOT", f"{rho} cis({angle} deg)"))
            angles.append(angle)
        answer = f"roots = {roots_text(rho, angles)}"
        problem = (
            f"Find all {n}-th roots of z = {radius} cis({theta} deg)."
        )
        return problem, steps, answer
