import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.arc_sector_generator import pi_txt
from generators.integration_by_parts_generator import cm


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
    r = 2a·cos(θ) use the half-angle identity and land on πa².

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
            c = random.randint(-4, 4)
            d = random.choice([v for v in range(-5, 6) if v != 0])
            t0 = random.choice([-2, -1, 1, 2, 3])
            if 2 * t0 + c == 0:
                t0 = t0 + 1 if 2 * (t0 + 1) + c != 0 else t0 - 1
            x_txt = ("t^2" if c == 0 else
                     f"t^2 + {cm(c, 't')}" if c > 0 else
                     f"t^2 - {cm(-c, 't')}")
            y_txt = (f"t^3 + {cm(d, 't')}" if d > 0 else
                     f"t^3 - {cm(-d, 't')}")
            xv = 2 * t0 + c
            yv = 3 * t0 * t0 + d
            ans = Fraction(yv, xv)
            steps = [
                step("PARAM_SETUP", f"x = {x_txt}, y = {y_txt}",
                     f"find dy/dx at t = {t0}"),
                step("THEOREM", "parametric derivative",
                     "dy/dx = (dy/dt)/(dx/dt)"),
                step("EVAL", "dx/dt", lin_t(2, c)),
                step("EVAL", "dy/dt", quad_t(3, d)),
                step("SUBST", "t", t0,
                     f"dx/dt = 2({t0}){'' if c == 0 else f' + {c}' if c > 0 else f' - {-c}'} = {xv}"),
                step("SUBST", "t", t0,
                     f"dy/dt = 3({t0})^2{'' if d == 0 else f' + {d}' if d > 0 else f' - {-d}'} = {yv}"),
                step("D", yv, xv, str(ans)),
            ]
            answer = str(ans)
            problem = (f"A curve is given by x = {x_txt}, y = {y_txt}. "
                       f"Find dy/dx at t = {t0}.")
        elif variant == "arc_length":
            m = random.randint(1, 8)
            s, T = random.choice([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
            swap = random.random() < 0.5
            quad = cm(3 * m, "t^2")
            cub = f"{cm(m, 't^3')} - {cm(3 * m, 't')}"
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
            a = random.randint(2, 9)
            num, den = random.choice([(1, 6), (1, 4), (1, 3), (1, 2),
                                      (1, 1)])
            th = Fraction(num, den)
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
            a = random.randint(1, 5)
            r2c = 4 * a * a
            half = 2 * a * a
            quarter = a * a
            sc = Fraction(quarter, 2)
            sc_txt = str(sc) if sc.denominator == 1 else f"({sc})"
            q_paren = "" if quarter == 1 else str(quarter)
            end = pi_txt(Fraction(quarter, 2))
            steps = [
                step("POLAR_SETUP",
                     f"r = {cm(2 * a, 'cos(θ)')} for -π/2 ≤ θ ≤ π/2",
                     "enclosed area"),
                step("POLAR_AREA_FORMULA", "A = (1/2) ∫ r^2 dθ"),
                step("EVAL", "r^2", f"{r2c}cos^2(θ)"),
                step("M", "1/2", r2c, half),
                step("IDENT_SUB", "cos^2(θ) = (1 + cos(2θ))/2"),
                step("M", half, "1/2", quarter),
                step("REWRITE", f"A = ∫ {q_paren}(1 + cos(2θ)) dθ"),
                step("ANTIDERIV", f"{q_paren}(1 + cos(2θ)) dθ",
                     f"{cm(quarter, 'θ')} + {sc_txt}sin(2θ)"),
                step("EVAL", "sin(π) = 0, sin(-π) = 0"),
                step("SUBST", "θ", "π/2",
                     f"{q_paren}(π/2) + {sc_txt}sin(π) = {end}"),
                step("SUBST", "θ", "-π/2",
                     f"{q_paren}(-π/2) + {sc_txt}sin(-π) = -{end}"),
                step("S", end, f"-{end}", pi_txt(Fraction(quarter))),
            ]
            answer = pi_txt(Fraction(quarter))
            problem = (f"Find the area enclosed by the polar curve "
                       f"r = {cm(2 * a, 'cos(θ)')} for "
                       f"-π/2 ≤ θ ≤ π/2.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"parametric_calculus_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
