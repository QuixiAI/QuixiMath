import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def frac_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def linear_text(coef, const):
    parts = []
    if coef != 0:
        if coef == 1:
            parts.append("z")
        elif coef == -1:
            parts.append("-z")
        else:
            parts.append(f"{coef}z")
    if const != 0:
        if not parts:
            parts.append(str(const))
        else:
            parts.append(f"+ {const}" if const > 0 else f"- {-const}")
    return " ".join(parts) if parts else "0"


def transform_text(a, b, c, d):
    return f"({linear_text(a, b)})/({linear_text(c, d)})"


class MobiusTransformGenerator(ProblemGenerator):
    """
    Mobius transformation images, fixed points, and cross-ratios.

    Variants:
    - image: evaluate T(z0)
    - fixed_points: solve z = T(z) as a quadratic
    - cross_ratio: compute [z1,z2;z3,z4]

    Op-codes used:
    - MOBIUS_SETUP / IMAGE: transformation setup and point image
    - FIXED_EQ / QUADRATIC / FIXED_POINT: fixed-point equation
    - CROSS_RATIO_SETUP / CROSS_RATIO: cross-ratio computation
    - E / M / A / S / F (established/shared): exact arithmetic
    - CHECK: fixed-point substitution
    - Z: final value
    """

    VARIANTS = ["image", "fixed_points", "cross_ratio"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "image":
            problem, steps, answer = self._generate_image()
        elif variant == "fixed_points":
            problem, steps, answer = self._generate_fixed_points()
        else:
            problem, steps, answer = self._generate_cross_ratio()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"mobius_transform_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_image(self):
        while True:
            a, b, c, d = [random.randint(-5, 5) for _ in range(4)]
            z0 = random.randint(-6, 6)
            if a * d - b * c != 0 and c * z0 + d != 0:
                break
        az = a * z0
        numerator = az + b
        cz = c * z0
        denominator = cz + d
        value = Fraction(numerator, denominator)
        steps = [
            step("MOBIUS_SETUP", f"T(z)={transform_text(a, b, c, d)}",
                 f"z0={z0}"),
            step("M", a, z0, az),
            step("A", az, b, numerator),
            step("M", c, z0, cz),
            step("A", cz, d, denominator),
            step("F", numerator, denominator, frac_text(value)),
            step("IMAGE", f"T({z0})", frac_text(value)),
        ]
        answer = f"T({z0}) = {frac_text(value)}"
        problem = (
            f"For T(z) = {transform_text(a, b, c, d)}, compute T({z0})."
        )
        return problem, steps, answer

    def _generate_fixed_points(self):
        c = random.randint(1, 3)
        r1, r2 = random.sample([v for v in range(-5, 6) if v != 0], 2)
        r1, r2 = sorted((r1, r2))
        a = 0
        d = -c * (r1 + r2)
        b = -c * r1 * r2
        middle = d - a
        const = -b
        steps = [
            step("MOBIUS_SETUP", f"T(z)={transform_text(a, b, c, d)}",
                 "fixed points"),
            step("FIXED_EQ", "z=(az+b)/(cz+d)"),
            step("EXPAND", "c z^2 + (d-a)z - b = 0"),
            step("S", d, a, middle),
            step("S", 0, b, const),
            step("QUADRATIC", c, middle, const),
        ]
        for root in (r1, r2):
            square = root * root
            term1 = c * square
            term2 = middle * root
            partial = term1 + term2
            total = partial + const
            steps.extend([
                step("E", root, 2, square),
                step("M", c, square, term1),
                step("M", middle, root, term2),
                step("A", term1, term2, partial),
                step("A", partial, const, total),
                step("CHECK", f"root {root}", total),
                step("FIXED_POINT", root),
            ])
        answer = f"fixed points = {{{r1}, {r2}}}"
        problem = (
            f"For T(z) = {transform_text(a, b, c, d)}, find the fixed "
            "points."
        )
        return problem, steps, answer

    def _generate_cross_ratio(self):
        z1, z2, z3, z4 = random.sample(range(-8, 9), 4)
        a = z1 - z3
        b = z2 - z4
        c = z1 - z4
        d = z2 - z3
        numerator = a * b
        denominator = c * d
        value = Fraction(numerator, denominator)
        steps = [
            step("CROSS_RATIO_SETUP", f"z1={z1}", f"z2={z2}",
                 f"z3={z3}", f"z4={z4}"),
            step("S", z1, z3, a),
            step("S", z2, z4, b),
            step("M", a, b, numerator),
            step("S", z1, z4, c),
            step("S", z2, z3, d),
            step("M", c, d, denominator),
            step("F", numerator, denominator, frac_text(value)),
            step("CROSS_RATIO", frac_text(value)),
        ]
        answer = f"cross_ratio = {frac_text(value)}"
        problem = (
            f"Compute the cross-ratio [z1,z2;z3,z4] for z1={z1}, "
            f"z2={z2}, z3={z3}, z4={z4}."
        )
        return problem, steps, answer
