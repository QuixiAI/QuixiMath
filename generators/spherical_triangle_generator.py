import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


ANGLES = [30, 45, 60, 90, 120, 135, 150]


def simplify_sqrt(radicand):
    outside = 1
    factor = 2
    while factor * factor <= radicand:
        square = factor * factor
        while radicand % square == 0:
            outside *= factor
            radicand //= square
        factor += 1
    return outside, radicand


def exact_term(radicand, coefficient):
    coefficient = Fraction(coefficient)
    if coefficient == 0:
        return {}
    outside, squarefree = simplify_sqrt(radicand)
    return {squarefree: coefficient * outside}


def exact_add(left, right):
    result = dict(left)
    for radicand, coefficient in right.items():
        result[radicand] = result.get(radicand, Fraction(0)) + coefficient
        if result[radicand] == 0:
            del result[radicand]
    return result


def exact_mul(left, right):
    result = {}
    for left_rad, left_coef in left.items():
        for right_rad, right_coef in right.items():
            outside, squarefree = simplify_sqrt(left_rad * right_rad)
            coefficient = left_coef * right_coef * outside
            result[squarefree] = result.get(squarefree, Fraction(0)) + \
                coefficient
            if result[squarefree] == 0:
                del result[squarefree]
    return result


def exact_div_monomial(numerator, denominator):
    if len(numerator) != 1 or len(denominator) != 1:
        raise ValueError("division helper expects monomial exact values")
    num_rad, num_coef = next(iter(numerator.items()))
    den_rad, den_coef = next(iter(denominator.items()))
    outside, squarefree = simplify_sqrt(num_rad * den_rad)
    coefficient = num_coef * outside / (den_coef * den_rad)
    return exact_term(squarefree, coefficient)


def fraction_text(value):
    return str(Fraction(value))


def radical_term_text(radicand, coefficient):
    coefficient = Fraction(coefficient)
    sign = "-" if coefficient < 0 else ""
    coefficient = abs(coefficient)
    if radicand == 1:
        return sign + fraction_text(coefficient)
    root = f"sqrt({radicand})"
    if coefficient == 1:
        body = root
    elif coefficient.denominator == 1:
        body = f"{coefficient.numerator}{root}"
    elif coefficient.numerator == 1:
        body = f"{root}/{coefficient.denominator}"
    else:
        body = f"{coefficient.numerator}{root}/{coefficient.denominator}"
    return sign + body


def exact_text(value):
    if not value:
        return "0"
    parts = []
    for radicand in sorted(value):
        coefficient = value[radicand]
        text = radical_term_text(radicand, coefficient)
        if not parts:
            parts.append(text)
        elif text.startswith("-"):
            parts.append(f"- {text[1:]}")
        else:
            parts.append(f"+ {text}")
    return " ".join(parts)


TRIG = {
    30: {"sin": exact_term(1, Fraction(1, 2)),
         "cos": exact_term(3, Fraction(1, 2))},
    45: {"sin": exact_term(2, Fraction(1, 2)),
         "cos": exact_term(2, Fraction(1, 2))},
    60: {"sin": exact_term(3, Fraction(1, 2)),
         "cos": exact_term(1, Fraction(1, 2))},
    90: {"sin": exact_term(1, 1), "cos": {}},
    120: {"sin": exact_term(3, Fraction(1, 2)),
          "cos": exact_term(1, Fraction(-1, 2))},
    135: {"sin": exact_term(2, Fraction(1, 2)),
          "cos": exact_term(2, Fraction(-1, 2))},
    150: {"sin": exact_term(1, Fraction(1, 2)),
          "cos": exact_term(3, Fraction(-1, 2))},
}


class SphericalTriangleGenerator(ProblemGenerator):
    """
    Mechanical spherical-triangle calculations with supplied exact trig
    values.

    Variants:
    - cosines: spherical law of cosines for sides, finding cos(a).
    - sines: spherical law of sines, finding sin(B).

    Op-codes used:
    - SPHERICAL_TRIANGLE_SETUP / SPHERICAL_COSINE_LAW /
      SPHERICAL_SINE_LAW / TRIG_VALUE
    - M / A / D (established/shared): exact radical arithmetic
    - Z: requested trig value
    """

    VARIANTS = ["cosines", "sines"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "cosines":
            problem, steps, answer = self._generate_cosines()
        else:
            problem, steps, answer = self._generate_sines()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"spherical_triangle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_cosines(self):
        b = random.choice(ANGLES)
        c = random.choice(ANGLES)
        angle_a = random.choice(ANGLES)
        cos_b = TRIG[b]["cos"]
        cos_c = TRIG[c]["cos"]
        sin_b = TRIG[b]["sin"]
        sin_c = TRIG[c]["sin"]
        cos_a_angle = TRIG[angle_a]["cos"]
        cos_product = exact_mul(cos_b, cos_c)
        sin_product = exact_mul(sin_b, sin_c)
        mixed_product = exact_mul(sin_product, cos_a_angle)
        target = exact_add(cos_product, mixed_product)
        steps = [
            step("SPHERICAL_TRIANGLE_SETUP",
                 f"b={b} deg, c={c} deg, A={angle_a} deg",
                 "find cos(a)"),
            step("SPHERICAL_COSINE_LAW",
                 "cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)"),
            step("TRIG_VALUE", f"cos(b)={exact_text(cos_b)}",
                 f"cos(c)={exact_text(cos_c)}",
                 f"cos(A)={exact_text(cos_a_angle)}"),
            step("TRIG_VALUE", f"sin(b)={exact_text(sin_b)}",
                 f"sin(c)={exact_text(sin_c)}"),
            step("M", exact_text(cos_b), exact_text(cos_c),
                 exact_text(cos_product)),
            step("M", exact_text(sin_b), exact_text(sin_c),
                 exact_text(sin_product)),
            step("M", exact_text(sin_product), exact_text(cos_a_angle),
                 exact_text(mixed_product)),
            step("A", exact_text(cos_product), exact_text(mixed_product),
                 exact_text(target)),
        ]
        answer = f"cos(a) = {exact_text(target)}"
        problem = (
            f"In a spherical triangle, sides b={b} deg and c={c} deg "
            f"enclose angle A={angle_a} deg. Given "
            f"cos(b)={exact_text(cos_b)}, cos(c)={exact_text(cos_c)}, "
            f"sin(b)={exact_text(sin_b)}, sin(c)={exact_text(sin_c)}, "
            f"and cos(A)={exact_text(cos_a_angle)}, use the spherical "
            f"law of cosines to find cos(a)."
        )
        return problem, steps, answer

    def _generate_sines(self):
        side_a = random.choice(ANGLES)
        side_b = random.choice(ANGLES)
        # A = a keeps the generated cases valid while still requiring the
        # law-of-sines multiplication and division.
        angle_a = side_a
        sin_a = TRIG[side_a]["sin"]
        sin_b = TRIG[side_b]["sin"]
        sin_angle_a = TRIG[angle_a]["sin"]
        product = exact_mul(sin_b, sin_angle_a)
        target = exact_div_monomial(product, sin_a)
        steps = [
            step("SPHERICAL_TRIANGLE_SETUP",
                 f"a={side_a} deg, b={side_b} deg, A={angle_a} deg",
                 "find sin(B)"),
            step("SPHERICAL_SINE_LAW",
                 "sin(A)/sin(a)=sin(B)/sin(b)"),
            step("TRIG_VALUE", f"sin(a)={exact_text(sin_a)}",
                 f"sin(b)={exact_text(sin_b)}",
                 f"sin(A)={exact_text(sin_angle_a)}"),
            step("M", exact_text(sin_b), exact_text(sin_angle_a),
                 exact_text(product)),
            step("D", exact_text(product), exact_text(sin_a),
                 exact_text(target)),
        ]
        answer = f"sin(B) = {exact_text(target)}"
        problem = (
            f"In a spherical triangle, side a={side_a} deg, side b="
            f"{side_b} deg, and angle A={angle_a} deg. Given "
            f"sin(a)={exact_text(sin_a)}, sin(b)={exact_text(sin_b)}, "
            f"and sin(A)={exact_text(sin_angle_a)}, use the spherical "
            f"law of sines to find sin(B)."
        )
        return problem, steps, answer
