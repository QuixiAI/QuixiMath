import random
from fractions import Fraction
from math import gcd
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.geometric_mean_generator import sqrt_txt

# θ -> (cos txt, sin txt, factor as (num_txt_fn)) for exact points
TRIG_TXT = {
    0: ("1", "0"), 90: ("0", "1"), 180: ("-1", "0"), 270: ("0", "-1"),
    30: ("√3/2", "1/2"), 60: ("1/2", "√3/2"), 120: ("-1/2", "√3/2"),
    150: ("-√3/2", "1/2"), 210: ("-√3/2", "-1/2"),
    240: ("-1/2", "-√3/2"), 300: ("1/2", "-√3/2"),
    330: ("√3/2", "-1/2"), 45: ("√2/2", "√2/2"), 135: ("-√2/2", "√2/2"),
    225: ("-√2/2", "-√2/2"), 315: ("√2/2", "-√2/2"),
}


def scaled(txt, r):
    """r times an exact value string: 4·(√3/2) -> '2√3'."""
    if txt == "0":
        return "0"
    sign = "-" if txt.startswith("-") else ""
    t = txt.lstrip("-")
    if t == "1":
        return f"{sign}{r}"
    if t == "1/2":
        return f"{sign}{r // 2}"
    root = int(t[1])  # √2 or √3
    k = r // 2
    return f"{sign}{k}√{root}" if k > 1 else f"{sign}√{root}"


def linear_text(coefficient, body, constant=0):
    """Render coefficient*body + constant without unit coefficients."""
    if coefficient == 1:
        rendered = body
    elif coefficient == -1:
        rendered = f"-{body}"
    else:
        rendered = f"{coefficient}{body}"
    if constant > 0:
        return f"{rendered} + {constant}"
    if constant < 0:
        return f"{rendered} - {-constant}"
    return rendered


def shifted(variable, center):
    """The coordinate variable-center with clean signs."""
    if center > 0:
        return f"{variable} - {center}"
    if center < 0:
        return f"{variable} + {-center}"
    return variable


def squared_shift(variable, center):
    inner = shifted(variable, center)
    return f"{variable}^2" if center == 0 else f"({inner})^2"


def circle_equation(center_x, center_y, radius_squared):
    return (f"{squared_shift('x', center_x)} + "
            f"{squared_shift('y', center_y)} = {radius_squared}")


class PolarParametricGenerator(ProblemGenerator):
    """
    Polar <-> rectangular for points and equations, and parametric ->
    rectangular elimination.

    Variants:
    - polar_point:    (r, θ) -> (x, y) with exact radical coordinates
    - rect_point:     (x, y) on an axis or 45° diagonal -> (r, θ)
    - polar_equation: r = k -> circle at the origin; r = 2a cos θ ->
                      circle (x - a)² + y² = a² via completing the square
    - parametric:     a line by solving for t, or a circle by the
                      Pythagorean identity

    Op-codes used:
    - POLAR_SETUP / PARAM_SETUP: the given and the goal
    - POLAR_FORMULA: the conversion formulas
    - TABLE_LOOKUP / QUADRANT / ROOT_SIMPLIFY / THEOREM (established)
    - SUBST / REWRITE / DIST / MOVE_TERM / COMPLETE_SQUARE /
      EQ_OP_BOTH / E / M / A / D (established)
    - Z: the point or equation
    """

    VARIANTS = ["polar_point", "rect_point", "polar_equation",
                "parametric"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        return getattr(self, f"_{variant}")()

    def _polar_point(self):
        base_theta = random.choice(list(TRIG_TXT))
        turns = random.randint(-100, 100)
        theta = base_theta + 360 * turns
        r = 2 * random.randint(1, 40)
        ct, st = TRIG_TXT[base_theta]
        x, y = scaled(ct, r), scaled(st, r)
        steps = [
            step("POLAR_SETUP", f"(r, θ) = ({r}, {theta}°)",
                 "rectangular coordinates"),
            step("POLAR_FORMULA", "x = r cos θ, y = r sin θ"),
        ]
        if turns:
            steps.append(step(
                "REWRITE", f"{theta}° = {turns}·360° + {base_theta}°",
                f"coterminal angle {base_theta}°",
            ))
        steps.extend([
            step("TABLE_LOOKUP", f"cos {base_theta}°", ct),
            step("TABLE_LOOKUP", f"sin {base_theta}°", st),
            step("REWRITE", f"x = {r} · ({ct}) = {x}"),
            step("REWRITE", f"y = {r} · ({st}) = {y}"),
        ])
        answer = f"({x}, {y})"
        steps.append(step("Z", answer))
        return self._pack("polar_to_rect_point",
                          f"Convert the polar point ({r}, {theta}°) to "
                          f"rectangular coordinates. Give exact values.",
                          steps, answer)

    def _rect_point(self):
        while True:
            m = random.randint(2, 30)
            n = random.randint(1, m - 1)
            if gcd(m, n) == 1 and (m - n) % 2 == 1:
                break
        leg_a = m * m - n * n
        leg_b = 2 * m * n
        if random.random() < 0.5:
            leg_a, leg_b = leg_b, leg_a
        scale = random.randint(1, 20)
        sign_x = random.choice([-1, 1])
        sign_y = random.choice([-1, 1])
        x, y = sign_x * scale * leg_a, sign_y * scale * leg_b
        radius = scale * (m * m + n * n)
        slope = Fraction(abs(y), abs(x))
        reference = f"arctan({slope})"
        if x > 0 and y > 0:
            theta = reference
        elif x < 0 < y:
            theta = f"180° - {reference}"
        elif x < 0 and y < 0:
            theta = f"180° + {reference}"
        else:
            theta = f"360° - {reference}"
        radial_square = x * x + y * y
        steps = [
            step("POLAR_SETUP", f"(x, y) = ({x}, {y})",
                 "polar (r ≥ 0, 0° ≤ θ < 360°)"),
            step("POLAR_FORMULA", "r = √(x^2 + y^2), tan θ = y/x"),
            step("E", x, 2, x * x),
            step("E", y, 2, y * y),
            step("A", x * x, y * y, radial_square),
            step("ROOT_SIMPLIFY", f"√{radial_square} = {radius}"),
            step("D", abs(y), abs(x), str(slope)),
            step("QUADRANT", f"({x}, {y})", f"θ = {theta}"),
        ]
        answer = f"({radius}, {theta})"
        steps.append(step("Z", answer))
        return self._pack("rect_to_polar_point",
                          f"Convert the point ({x}, {y}) to polar "
                          f"coordinates with r ≥ 0 and 0° ≤ θ < 360°. "
                          f"Give exact values.", steps, answer)

    def _polar_equation(self):
        pole_x = random.randint(-20, 20)
        pole_y = random.randint(-20, 20)
        local_x = shifted("x", pole_x)
        local_y = shifted("y", pole_y)
        if random.random() < 0.5:
            k = random.randint(2, 80)
            answer = circle_equation(pole_x, pole_y, k * k)
            steps = [
                step("POLAR_SETUP", f"r = {k}",
                     f"pole=({pole_x}, {pole_y})", "rectangular equation"),
                step("SUBST", "r",
                     f"√({squared_shift('x', pole_x)} + "
                     f"{squared_shift('y', pole_y)})",
                     f"√({squared_shift('x', pole_x)} + "
                     f"{squared_shift('y', pole_y)}) = {k}"),
                step("E", k, 2, k * k),
                step("REWRITE", answer),
            ]
            problem = (f"Convert the polar equation r = {k} to "
                       f"rectangular form when the pole is "
                       f"({pole_x}, {pole_y}).")
        else:
            a = random.randint(2, 40)
            answer = circle_equation(pole_x + a, pole_y, a * a)
            steps = [
                step("POLAR_SETUP", f"r = {2 * a} cos θ",
                     f"pole=({pole_x}, {pole_y})", "rectangular equation"),
                step("EQ_OP_BOTH", "multiply", "r", "r^2",
                     f"{2 * a} r cos θ"),
                step("SUBST", "r^2",
                     f"({local_x})^2 + ({local_y})^2",
                     f"({local_x})^2 + ({local_y})^2 = "
                     f"{2 * a} r cos θ"),
                step("SUBST", "r cos θ", local_x,
                     f"({local_x})^2 + ({local_y})^2 = "
                     f"{2 * a}({local_x})"),
                step("MOVE_TERM", f"{2 * a}({local_x}) to the left",
                     f"({local_x})^2 - {2 * a}({local_x}) + "
                     f"({local_y})^2 = 0"),
                step("COMPLETE_SQUARE", f"half of -{2 * a} = -{a}",
                     f"(-{a})^2 = {a * a}"),
                step("REWRITE", answer),
            ]
            problem = (f"Convert the polar equation r = {2 * a} cos θ "
                       f"to rectangular form when the pole is "
                       f"({pole_x}, {pole_y}).")
        steps.append(step("Z", answer))
        return self._pack("polar_eq_to_rect", problem, steps, answer)

    def _parametric(self):
        if random.random() < 0.55:
            x_coefficient = random.randint(1, 12)
            y_coefficient = random.choice([
                value for value in range(-12, 13) if value != 0
            ])
            x_constant = random.randint(-20, 20)
            y_constant = random.randint(-20, 20)
            xdef = linear_text(x_coefficient, "t", x_constant)
            ydef = linear_text(y_coefficient, "t", y_constant)
            px = x_coefficient * y_coefficient
            pc = x_coefficient * y_constant
            bq = y_coefficient * x_constant
            const = pc - bq
            local_x = shifted("x", x_constant)
            left = linear_text(x_coefficient, "y")
            px_t = linear_text(px, "t")
            pt = linear_text(x_coefficient, "t")
            answer = f"{left} = {linear_text(y_coefficient, 'x', const)}"
            steps = [
                step("PARAM_SETUP", f"x = {xdef}, y = {ydef}",
                     "eliminate t"),
                step("M", x_coefficient, y_coefficient, px),
                step("M", x_coefficient, y_constant, pc),
                step("EQ_OP_BOTH", "multiply", x_coefficient,
                     f"{left} = {linear_text(px, 't', pc)}"),
                step("REWRITE", f"{pt} = {local_x}"),
                step("SUBST", px_t,
                     linear_text(y_coefficient, f"({pt})"),
                     f"{left} = "
                     f"{linear_text(y_coefficient, f'({local_x})', pc)}"),
                step("M", y_coefficient, x_constant, bq),
                step("DIST", y_coefficient, local_x,
                     linear_text(y_coefficient, "x", -bq)),
                step("S", pc, bq, const),
                step("REWRITE", answer),
            ]
            problem = (f"Eliminate the parameter: x = {xdef}, "
                       f"y = {ydef}.")
        else:
            a = random.randint(2, 40)
            center_x = random.randint(-20, 20)
            center_y = random.randint(-20, 20)
            xdef = linear_text(a, "cos t", center_x)
            ydef = linear_text(a, "sin t", center_y)
            answer = circle_equation(center_x, center_y, a * a)
            steps = [
                step("PARAM_SETUP", f"x = {xdef}, y = {ydef}",
                     "eliminate t"),
                step("THEOREM", "Pythagorean identity",
                     "cos^2 t + sin^2 t = 1"),
                step("REWRITE",
                     f"(({shifted('x', center_x)})/{a})^2 + "
                     f"(({shifted('y', center_y)})/{a})^2 = 1"),
                step("E", a, 2, a * a),
                step("REWRITE", answer),
            ]
            problem = (f"Eliminate the parameter: x = {xdef}, "
                       f"y = {ydef}.")
        steps.append(step("Z", answer))
        return self._pack("parametric_to_rect", problem, steps, answer)

    @staticmethod
    def _pack(op, problem, steps, answer):
        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
