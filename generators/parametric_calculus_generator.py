import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt
from generators.integration_by_parts_generator import cm


POLAR_ANGLE_FACTORS = sorted({
    Fraction(numerator, denominator)
    for denominator in range(1, 31)
    for numerator in range(1, 2 * denominator + 1)
})
POLAR_PHASE_FACTORS = sorted({
    Fraction(numerator, denominator)
    for denominator in range(1, 31)
    for numerator in range(0, 2 * denominator)
})


def poly_t(terms):
    """Render nonzero (coefficient, body) terms with clean signs."""
    pieces = []
    for coefficient, body in terms:
        if coefficient == 0:
            continue
        term = cm(abs(coefficient), body) if body else str(abs(coefficient))
        if not pieces:
            pieces.append(term if coefficient > 0 else f"-{term}")
        else:
            pieces.append(f"+ {term}" if coefficient > 0 else f"- {term}")
    return " ".join(pieces) if pieces else "0"


def signed_int(value):
    if value == 0:
        return ""
    return f" + {value}" if value > 0 else f" - {-value}"


def angle_text(value):
    """Render an exact multiple of pi, including zero and negatives."""
    value = Fraction(value)
    if value == 0:
        return "0"
    if value < 0:
        return f"-{pi_txt(-value)}"
    return pi_txt(value)


def coefficient_text(value, body):
    """Render a rational coefficient times a symbolic body."""
    value = Fraction(value)
    if value.denominator == 1:
        return cm(value.numerator, body)
    return f"({value}){body}"


def lin_t(a, b):
    """at + b in the parameter t."""
    at = cm(a, "t")
    if b == 0:
        return at
    return f"{at} + {b}" if b > 0 else f"{at} - {-b}"


def quad_t(a, b):
    """at^2 + b in the parameter t."""
    at = cm(a, "t^2")
    if b == 0:
        return at
    return f"{at} + {b}" if b > 0 else f"{at} - {-b}"


class ParametricCalculusGenerator(ProblemGenerator):
    """
    Parametric derivatives and arc length, and polar area, all exact.
    Arc-length curves are built so the speed is a perfect square:
    x = 3mt^2, y = mt^3 - 3mt gives speed 3m(t^2 + 1). Polar circles
    r = c·cos(θ - φ) use the half-angle identity and land on πc²/4.

    Variants:
    - dydx: dy/dx = (dy/dt)/(dx/dt) at an integer t
    - arc_length: ∫ of the perfect-square speed over [s, T]
    - polar_sector: A = (1/2)∫ r² dθ for constant r
    - polar_circle: r = 2a·cos(θ) via cos² half-angle identity

    Op-codes used:
    - PARAM_SETUP / POLAR_SETUP / THEOREM / IDENT_SUB (established)
    - POLAR_AREA_FORMULA: A = (1/2) ∫ r^2 dθ
    - ARCLEN_FORMULA: L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt
    - EVAL / SUBST / REWRITE / INTEG_SETUP / ANTIDERIV / M / S / D
      (established)
    - Z: the exact slope, length, or area
    """

    VARIANTS = ["dydx", "arc_length", "polar_sector", "polar_circle"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "dydx":
            while True:
                x_quad = random.randint(1, 9)
                x_linear = random.randint(-12, 12)
                x_constant = random.randint(-20, 20)
                y_cubic = random.randint(1, 8)
                y_linear = random.randint(-12, 12)
                y_constant = random.randint(-20, 20)
                t0 = random.randint(-8, 8)
                xv = 2 * x_quad * t0 + x_linear
                if xv != 0:
                    break
            x_txt = poly_t([
                (x_quad, "t^2"), (x_linear, "t"), (x_constant, ""),
            ])
            y_txt = poly_t([
                (y_cubic, "t^3"), (y_linear, "t"), (y_constant, ""),
            ])
            dx_txt = poly_t([(2 * x_quad, "t"), (x_linear, "")])
            dy_txt = poly_t([(3 * y_cubic, "t^2"), (y_linear, "")])
            yv = 3 * y_cubic * t0 * t0 + y_linear
            ans = Fraction(yv, xv)
            steps = [
                step("PARAM_SETUP", f"x = {x_txt}, y = {y_txt}",
                     f"find dy/dx at t = {t0}"),
                step("THEOREM", "parametric derivative",
                     "dy/dx = (dy/dt)/(dx/dt)"),
                step("EVAL", "dx/dt", dx_txt),
                step("EVAL", "dy/dt", dy_txt),
                step("SUBST", "t", t0,
                     f"dx/dt = {2 * x_quad}({t0})"
                     f"{signed_int(x_linear)} = {xv}"),
                step("SUBST", "t", t0,
                     f"dy/dt = {3 * y_cubic}({t0})^2"
                     f"{signed_int(y_linear)} = {yv}"),
                step("D", yv, xv, str(ans)),
            ]
            answer = str(ans)
            problem = (f"A curve is given by x = {x_txt}, y = {y_txt}. "
                       f"Find dy/dx at t = {t0}.")
        elif variant == "arc_length":
            m = random.randint(1, 20)
            s = random.randint(0, 9)
            T = s + random.randint(1, 10)
            quad_shift = random.randint(-10, 10)
            cubic_shift = random.randint(-10, 10)
            swap = random.random() < 0.5
            quad = poly_t([(3 * m, "t^2"), (quad_shift, "")])
            cub = poly_t([
                (m, "t^3"), (-3 * m, "t"), (cubic_shift, ""),
            ])
            x_txt, y_txt = (cub, quad) if swap else (quad, cub)
            dquad = cm(6 * m, "t")
            dcub = quad_t(3 * m, -3 * m)
            d1, d2 = (dcub, dquad) if swap else (dquad, dcub)
            sq_quad = f"({dquad})^2 = {cm(36 * m * m, 't^2')}"
            sq_cub = (f"({dcub})^2 = {cm(9 * m * m, 't^4')} - "
                      f"{cm(18 * m * m, 't^2')} + {9 * m * m}")
            speed = quad_t(3 * m, 3 * m)
            anti = f"{cm(m, 't^3')} + {cm(3 * m, 't')}"

            def at(t):
                return m * t ** 3 + 3 * m * t

            def at_txt(t):
                return (f"{cm(m, f'({t})^3')} + {cm(3 * m, f'({t})')}"
                        f" = {at(t)}")
            L = at(T) - at(s)
            steps = [
                step("PARAM_SETUP", f"x = {x_txt}, y = {y_txt}",
                     f"arc length for {s} ≤ t ≤ {T}"),
                step("ARCLEN_FORMULA",
                     "L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt"),
                step("EVAL", "dx/dt", d1),
                step("EVAL", "dy/dt", d2),
                step("EVAL", sq_quad if not swap else sq_cub),
                step("EVAL", sq_cub if not swap else sq_quad),
                step("EVAL",
                     f"({d1})^2 + ({d2})^2 = {cm(9 * m * m, 't^4')} + "
                     f"{cm(18 * m * m, 't^2')} + {9 * m * m}"),
                step("REWRITE",
                     f"{cm(9 * m * m, 't^4')} + {cm(18 * m * m, 't^2')} "
                     f"+ {9 * m * m} = ({speed})^2"),
                step("EVAL", f"√(({speed})^2) = {speed}"),
                step("INTEG_SETUP",
                     f"∫ from {s} to {T} of ({speed}) dt", "arc length"),
                step("ANTIDERIV", f"({speed}) dt", anti),
                step("SUBST", "t", T, at_txt(T)),
                step("SUBST", "t", s, at_txt(s)),
                step("S", at(T), at(s), L),
            ]
            answer = str(L)
            problem = (f"Find the arc length of the curve x = {x_txt}, "
                       f"y = {y_txt} for {s} ≤ t ≤ {T}.")
        elif variant == "polar_sector":
            a = random.randint(2, 80)
            th = random.choice(POLAR_ANGLE_FACTORS)
            th_txt = pi_txt(th)
            r2 = a * a
            outer = pi_txt(r2 * th)
            area = pi_txt(r2 * th / 2)
            steps = [
                step("POLAR_SETUP", f"r = {a} for 0 ≤ θ ≤ {th_txt}",
                     "area swept"),
                step("POLAR_AREA_FORMULA", "A = (1/2) ∫ r^2 dθ"),
                step("EVAL", "r^2", r2),
                step("ANTIDERIV", f"{r2} dθ", f"{r2}θ"),
                step("SUBST", "θ", th_txt,
                     f"{r2}({th_txt}) - {r2}(0) = {outer}"),
                step("M", "1/2", outer, area),
            ]
            answer = area
            problem = (f"Find the area swept by the polar curve r = {a} "
                       f"for 0 ≤ θ ≤ {th_txt}.")
        else:
            c = random.randint(2, 80)
            phase = random.choice(POLAR_PHASE_FACTORS)
            shifted_theta = ("θ" if phase == 0 else
                             f"θ - {angle_text(phase)}")
            lower = phase - Fraction(1, 2)
            upper = phase + Fraction(1, 2)
            lower_txt = angle_text(lower)
            upper_txt = angle_text(upper)
            r_txt = cm(c, f"cos({shifted_theta})")
            r2c = c * c
            half = Fraction(r2c, 2)
            quarter = Fraction(r2c, 4)
            sc = Fraction(quarter, 2)
            half_txt = str(half)
            quarter_integrand = coefficient_text(
                quarter, f"(1 + cos(2({shifted_theta})))")
            anti = (f"{coefficient_text(quarter, 'θ')} + "
                    f"{coefficient_text(sc, f'sin(2({shifted_theta}))')}")
            upper_value = angle_text(quarter * upper)
            lower_value = angle_text(quarter * lower)
            area = angle_text(quarter)
            steps = [
                step("POLAR_SETUP",
                     f"r = {r_txt} for {lower_txt} ≤ θ ≤ {upper_txt}",
                     "enclosed area"),
                step("POLAR_AREA_FORMULA", "A = (1/2) ∫ r^2 dθ"),
                step("EVAL", "r^2", f"{r2c}cos^2({shifted_theta})"),
                step("M", "1/2", r2c, half_txt),
                step("IDENT_SUB", f"u = {shifted_theta}",
                     "cos^2(u) = (1 + cos(2u))/2"),
                step("M", half_txt, "1/2", str(quarter)),
                step("REWRITE", f"A = ∫ {quarter_integrand} dθ"),
                step("ANTIDERIV", f"{quarter_integrand} dθ", anti),
                step("EVAL", "sin(π) = 0, sin(-π) = 0"),
                step("SUBST", "θ", upper_txt,
                     f"{coefficient_text(quarter, f'({upper_txt})')} + "
                     f"{coefficient_text(sc, 'sin(π)')} = {upper_value}"),
                step("SUBST", "θ", lower_txt,
                     f"{coefficient_text(quarter, f'({lower_txt})')} + "
                     f"{coefficient_text(sc, 'sin(-π)')} = {lower_value}"),
                step("S", upper_value, lower_value, area),
            ]
            answer = area
            problem = (f"Find the area enclosed by the polar curve "
                       f"r = {r_txt} for {lower_txt} ≤ θ ≤ {upper_txt}.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"parametric_calculus_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
