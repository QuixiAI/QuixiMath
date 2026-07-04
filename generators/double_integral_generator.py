import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_pi(coeff):
    coeff = Fraction(coeff)
    if coeff == 1:
        return "pi"
    if coeff == -1:
        return "-pi"
    return f"{fmt_frac(coeff)}*pi"


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


def fmt_signed_products(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


class DoubleIntegralGenerator(ProblemGenerator):
    """
    Double integrals with iterated rectangular bounds, triangular order
    reversal, and polar conversion.

    Variants:
    - rectangle_iterated: evaluate int_x int_y (p*x + q*y + r)
    - reverse_triangle:  reverse a triangular integral and evaluate it
    - polar_sector:      convert x^2 + y^2 over a disk sector to polar

    Op-codes used:
    - DOUBLE_SETUP: integral, bounds, and target
    - INNER_ANTIDERIV: antiderivative for the inner variable
    - INNER_EVAL: substitute inner bounds
    - OUTER_ANTIDERIV: antiderivative for the outer variable
    - OUTER_EVAL: substitute outer bounds
    - REGION_REWRITE: reversed bounds for a region
    - POLAR_CONVERT: Cartesian-to-polar integrand rewrite
    - JACOBIAN: dA = r dr dtheta
    - POLAR_BOUNDS: r and theta ranges
    - POLAR_EVAL: combine radial integral and angular range
    - Z: final value or reversed-order value
    """

    VARIANTS = ["rectangle_iterated", "reverse_triangle", "polar_sector"]
    SECTORS = [
        ("first-quadrant", "0", "pi/2", Fraction(1, 2)),
        ("upper-half", "0", "pi", Fraction(1, 1)),
        ("full", "0", "2*pi", Fraction(2, 1)),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rectangle_iterated":
            a = random.randint(0, 3)
            b = random.randint(a + 1, a + 5)
            c = random.randint(0, 3)
            d = random.randint(c + 1, c + 5)
            p = 2 * random.randint(1, 4)
            q = 2 * random.randint(1, 4)
            r = random.randint(-5, 8)
            integrand = fmt_linear([(p, "x"), (q, "y"), (r, "")])
            inner_y2 = q // 2
            x_coeff = p * (d - c)
            constant = inner_y2 * (d * d - c * c) + r * (d - c)
            outer_x2 = x_coeff // 2
            value = (outer_x2 * (b * b - a * a) +
                     constant * (b - a))
            inner = fmt_linear([(p, "x*y"), (inner_y2, "y^2"), (r, "y")])
            inner_eval = fmt_linear([(x_coeff, "x"), (constant, "")])
            outer = fmt_linear([(outer_x2, "x^2"), (constant, "x")])
            answer = f"value {value}"
            steps = [
                step("DOUBLE_SETUP", f"integrand {integrand}",
                     f"x:{a}..{b}", f"y:{c}..{d}"),
                step("INNER_ANTIDERIV", "dy", inner),
                step("INNER_EVAL", f"y={c}..{d}", inner_eval),
                step("OUTER_ANTIDERIV", "dx", outer),
                step("OUTER_EVAL", f"x={a}..{b}",
                     fmt_signed_products([
                         (outer_x2, f"({b}^2 - {a}^2)"),
                         (constant, f"({b} - {a})"),
                     ]), value),
                step("Z", answer),
            ]
            problem = (
                f"Evaluate the iterated integral int_x={a}..{b} "
                f"int_y={c}..{d} ({integrand}) dy dx."
            )
        elif variant == "reverse_triangle":
            width = random.randint(2, 8)
            slope = random.randint(2, 5)
            height = slope * width
            const = 2 * random.randint(1, 6)
            value = const * slope * width * width // 2
            answer = (
                f"reversed y:0..{height}, x:y/{slope}..{width}; "
                f"value {value}"
            )
            steps = [
                step("DOUBLE_SETUP", f"integrand {const}",
                     f"x:0..{width}", f"y:0..{slope}*x"),
                step("REGION_REWRITE", f"0 <= y <= {height}",
                     f"y/{slope} <= x <= {width}"),
                step("INNER_ANTIDERIV", "dx", f"{const}*x"),
                step("INNER_EVAL", f"x=y/{slope}..{width}",
                     f"{const}*({width} - y/{slope})"),
                step("OUTER_EVAL", f"y=0..{height}",
                     f"{const}*{slope}*{width}^2/2", value),
                step("Z", answer),
            ]
            problem = (
                f"Reverse the order and evaluate int_x=0..{width} "
                f"int_y=0..{slope}*x {const} dy dx."
            )
        else:
            radius = random.randint(2, 6)
            region, theta_lo, theta_hi, angle_coeff = random.choice(
                self.SECTORS)
            radial = Fraction(radius ** 4, 4)
            coeff = angle_coeff * radial
            value = fmt_pi(coeff)
            answer = f"value {value}"
            steps = [
                step("DOUBLE_SETUP", "integrand x^2 + y^2",
                     f"{region} disk radius {radius}"),
                step("POLAR_CONVERT", "x^2 + y^2", "r^2"),
                step("JACOBIAN", "dA", "r dr dtheta"),
                step("POLAR_BOUNDS", "r", f"0..{radius}"),
                step("POLAR_BOUNDS", "theta", f"{theta_lo}..{theta_hi}"),
                step("INNER_ANTIDERIV", "dr", "r^4/4"),
                step("INNER_EVAL", f"r=0..{radius}",
                     f"{radius}^4/4", fmt_frac(radial)),
                step("POLAR_EVAL", "theta range * radial integral",
                     f"{theta_hi} * {fmt_frac(radial)}", value),
                step("Z", answer),
            ]
            problem = (
                f"Convert to polar and evaluate the double integral of "
                f"x^2 + y^2 over the {region} disk x^2 + y^2 <= "
                f"{radius * radius}."
            )

        return dict(
            problem_id=jid(),
            operation=f"double_integral_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
