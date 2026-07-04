import random
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
        theta = random.choice(list(TRIG_TXT))
        r = random.choice([2, 4, 6, 8, 10, 12])
        ct, st = TRIG_TXT[theta]
        x, y = scaled(ct, r), scaled(st, r)
        steps = [
            step("POLAR_SETUP", f"(r, θ) = ({r}, {theta}°)",
                 "rectangular coordinates"),
            step("POLAR_FORMULA", "x = r cos θ, y = r sin θ"),
            step("TABLE_LOOKUP", f"cos {theta}°", ct),
            step("TABLE_LOOKUP", f"sin {theta}°", st),
            step("REWRITE", f"x = {r} · ({ct}) = {x}"),
            step("REWRITE", f"y = {r} · ({st}) = {y}"),
        ]
        answer = f"({x}, {y})"
        steps.append(step("Z", answer))
        return self._pack("polar_to_rect_point",
                          f"Convert the polar point ({r}, {theta}°) to "
                          f"rectangular coordinates. Give exact values.",
                          steps, answer)

    def _rect_point(self):
        a = random.randint(2, 9)
        kind = random.choice(["diag", "axis"])
        if kind == "axis":
            theta = random.choice([0, 90, 180, 270])
            x, y = {0: (a, 0), 90: (0, a), 180: (-a, 0),
                    270: (0, -a)}[theta]
            r_txt = str(a)
            steps = [
                step("POLAR_SETUP", f"(x, y) = ({x}, {y})",
                     "polar (r ≥ 0, 0° ≤ θ < 360°)"),
                step("POLAR_FORMULA", "r = √(x^2 + y^2), point on an "
                     "axis"),
                step("EVAL", "r", a),
                step("QUADRANT", f"({x}, {y})", f"θ = {theta}°"),
            ]
        else:
            theta = random.choice([45, 135, 225, 315])
            sx = 1 if theta in (45, 315) else -1
            sy = 1 if theta in (45, 135) else -1
            x, y = sx * a, sy * a
            r_txt = f"{a}√2"
            steps = [
                step("POLAR_SETUP", f"(x, y) = ({x}, {y})",
                     "polar (r ≥ 0, 0° ≤ θ < 360°)"),
                step("POLAR_FORMULA", "r = √(x^2 + y^2), tan θ = y/x"),
                step("E", x, 2, x * x),
                step("E", y, 2, y * y),
                step("A", x * x, y * y, 2 * a * a),
                step("ROOT_SIMPLIFY", f"√{2 * a * a} = {r_txt}"),
                step("D", y, x, y // x),
                step("TABLE_LOOKUP", "tan 45°", "1"),
                step("QUADRANT", f"({x}, {y})", f"θ = {theta}°"),
            ]
        answer = f"({r_txt}, {theta}°)"
        steps.append(step("Z", answer))
        return self._pack("rect_to_polar_point",
                          f"Convert the point ({x}, {y}) to polar "
                          f"coordinates with r ≥ 0 and 0° ≤ θ < 360°. "
                          f"Give exact values.", steps, answer)

    def _polar_equation(self):
        if random.random() < 0.5:
            k = random.randint(2, 9)
            answer = f"x^2 + y^2 = {k * k}"
            steps = [
                step("POLAR_SETUP", f"r = {k}", "rectangular equation"),
                step("SUBST", "r", "√(x^2 + y^2)",
                     f"√(x^2 + y^2) = {k}"),
                step("E", k, 2, k * k),
                step("REWRITE", answer),
            ]
            problem = (f"Convert the polar equation r = {k} to "
                       f"rectangular form.")
        else:
            a = random.randint(2, 6)
            answer = f"(x - {a})^2 + y^2 = {a * a}"
            steps = [
                step("POLAR_SETUP", f"r = {2 * a} cos θ",
                     "rectangular equation"),
                step("EQ_OP_BOTH", "multiply", "r", "r^2",
                     f"{2 * a} r cos θ"),
                step("SUBST", "r^2", "x^2 + y^2",
                     f"x^2 + y^2 = {2 * a} r cos θ"),
                step("SUBST", "r cos θ", "x",
                     f"x^2 + y^2 = {2 * a}x"),
                step("MOVE_TERM", f"{2 * a}x to the left",
                     f"x^2 - {2 * a}x + y^2 = 0"),
                step("COMPLETE_SQUARE", f"half of -{2 * a} = -{a}",
                     f"(-{a})^2 = {a * a}"),
                step("REWRITE", answer),
            ]
            problem = (f"Convert the polar equation r = {2 * a} cos θ "
                       f"to rectangular form.")
        steps.append(step("Z", answer))
        return self._pack("polar_eq_to_rect", problem, steps, answer)

    def _parametric(self):
        if random.random() < 0.55:
            a = random.choice([v for v in range(-5, 6) if v != 0])
            b = random.choice([v for v in range(-4, 5)
                               if v not in (-1, 0, 1)])
            c = random.randint(-6, 6)
            const = b * a + c
            # x = t - a  ->  t = x + a
            xdef = f"t {'-' if a > 0 else '+'} {abs(a)}"
            ydef = (f"{b}t {'+' if c >= 0 else '-'} {abs(c)}"
                    if c else f"{b}t")
            t_expr = f"x {'+' if a > 0 else '-'} {abs(a)}"
            dist = f"{b}x {'+' if b * a > 0 else '-'} {abs(b * a)}"
            ans_const = const
            answer = (f"y = {b}x {'+' if ans_const > 0 else '-'} "
                      f"{abs(ans_const)}" if ans_const
                      else f"y = {b}x")
            steps = [
                step("PARAM_SETUP", f"x = {xdef}, y = {ydef}",
                     "eliminate t"),
                step("REWRITE", f"t = {t_expr}"),
                step("SUBST", "t", t_expr,
                     f"y = {b}({t_expr})"
                     f"{' + ' + str(c) if c > 0 else ''}"
                     f"{' - ' + str(-c) if c < 0 else ''}"),
                step("DIST", b, t_expr, dist),
            ]
            if c:
                steps.append(step("A", b * a, c, const))
            steps.append(step("REWRITE", answer))
            problem = (f"Eliminate the parameter: x = {xdef}, "
                       f"y = {ydef}.")
        else:
            a = random.randint(2, 9)
            answer = f"x^2 + y^2 = {a * a}"
            steps = [
                step("PARAM_SETUP", f"x = {a} cos t, y = {a} sin t",
                     "eliminate t"),
                step("THEOREM", "Pythagorean identity",
                     "cos^2 t + sin^2 t = 1"),
                step("REWRITE", f"(x/{a})^2 + (y/{a})^2 = 1"),
                step("E", a, 2, a * a),
                step("REWRITE", answer),
            ]
            problem = (f"Eliminate the parameter: x = {a} cos t, "
                       f"y = {a} sin t.")
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
