import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.parabola_features_generator import shift


def general_txt(terms):
    """[(coef, 'x^2'), ...] -> '4x^2 + 9y^2 - 8x + 36y + 4 = 0'."""
    parts = []
    for c, sym in terms:
        if c == 0:
            continue
        mag = "" if abs(c) == 1 and sym else str(abs(c))
        body = f"{mag}{sym}" if sym else str(abs(c))
        if not parts:
            parts.append(body if c > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if c > 0 else f"- {body}")
    return " ".join(parts) + " = 0"


class ConicStandardFormGenerator(ProblemGenerator):
    """
    General form -> standard form by completing the square.

    Variants:
    - circle:  x^2 + y^2 + Dx + Ey + F = 0 -> (x-h)^2 + (y-k)^2 = r^2
    - ellipse: Ax^2 + By^2 + Dx + Ey + F = 0 -> factor each group,
      complete inside the parentheses, and add A·(half)^2 - the
      multiply-through - to the right side, then divide to reach 1

    Op-codes used:
    - CONIC_SETUP / MOVE_TERM / REWRITE / FORM_IDENTIFY (established)
    - FACTOR_GROUP: pull the leading coefficient off a group
      (established)
    - COMPLETE_SQUARE: half-and-square, established two-field shape
    - M: the coefficient times the added square (the classic trap)
    - A: accumulate the right side (established)
    - D / E / EVAL: divide through; read the radius (established)
    - Z: the standard-form equation
    """

    VARIANTS = ["circle", "ellipse"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "circle":
            return self._circle()
        return self._ellipse()

    def _circle(self):
        h = random.randint(-5, 5)
        k = random.randint(-5, 5)
        if h == 0 or k == 0:
            return self._circle()
        r = random.randint(2, 9)
        D, E, F = -2 * h, -2 * k, h * h + k * k - r * r
        eq = general_txt([(1, "x^2"), (1, "y^2"), (D, "x"), (E, "y"),
                          (F, "")])
        grouped = (f"x^2 {'-' if D < 0 else '+'} {abs(D)}x + "
                   f"y^2 {'-' if E < 0 else '+'} {abs(E)}y = {-F}")
        sq_x = h * h
        sq_y = k * k
        rhs1 = -F + sq_x
        rhs2 = rhs1 + sq_y
        std = f"{shift('x', h)}^2 + {shift('y', k)}^2 = {r * r}"
        steps = [
            step("CONIC_SETUP", eq, "standard form"),
            step("MOVE_TERM", "constant to the right", grouped),
            step("COMPLETE_SQUARE", f"half of {D} = {-h}",
                 f"({-h})^2 = {sq_x}"),
            step("COMPLETE_SQUARE", f"half of {E} = {-k}",
                 f"({-k})^2 = {sq_y}"),
            step("A", -F, sq_x, rhs1),
            step("A", rhs1, sq_y, rhs2),
            step("REWRITE", std),
            step("E", r, 2, r * r),
            step("EVAL", "r", r),
            step("FORM_IDENTIFY", "circle",
                 f"center ({h}, {k}), radius {r}"),
            step("Z", std),
        ]
        problem = f"Write in standard form: {eq}."
        return self._pack(problem, steps, std, "circle")

    def _ellipse(self):
        m, n = random.sample([2, 3, 4, 5], 2)  # x-denom m^2, y-denom n^2
        h = random.choice([v for v in range(-4, 5) if v != 0])
        k = random.choice([v for v in range(-4, 5) if v != 0])
        A, B = n * n, m * m
        D, E = -2 * A * h, -2 * B * k
        RHS = A * m * m  # = B * n * n = m^2 n^2
        F = A * h * h + B * k * k - RHS
        eq = general_txt([(A, "x^2"), (B, "y^2"), (D, "x"), (E, "y"),
                          (F, "")])
        gx = f"(x^2 {'-' if h > 0 else '+'} {abs(2 * h)}x)"
        gy = f"(y^2 {'-' if k > 0 else '+'} {abs(2 * k)}y)"
        add_x = A * h * h
        add_y = B * k * k
        r1 = -F + add_x
        r2 = r1 + add_y
        std = (f"{shift('x', h)}^2/{m * m} + "
               f"{shift('y', k)}^2/{n * n} = 1")
        factored = (f"{A}{shift('x', h)}^2 + {B}{shift('y', k)}^2 "
                    f"= {RHS}")
        steps = [
            step("CONIC_SETUP", eq, "standard form"),
            step("MOVE_TERM", "constant to the right",
                 f"{A}x^2 {'-' if D < 0 else '+'} {abs(D)}x + "
                 f"{B}y^2 {'-' if E < 0 else '+'} {abs(E)}y = {-F}"),
            step("FACTOR_GROUP", f"{A}x^2 {'-' if D < 0 else '+'} "
                 f"{abs(D)}x", A, gx),
            step("FACTOR_GROUP", f"{B}y^2 {'-' if E < 0 else '+'} "
                 f"{abs(E)}y", B, gy),
            step("COMPLETE_SQUARE", f"half of {-2 * h} = {-h}",
                 f"({-h})^2 = {h * h}"),
            step("M", A, h * h, add_x),
            step("COMPLETE_SQUARE", f"half of {-2 * k} = {-k}",
                 f"({-k})^2 = {k * k}"),
            step("M", B, k * k, add_y),
            step("A", -F, add_x, r1),
            step("A", r1, add_y, r2),
            step("REWRITE", factored),
            step("D", RHS, A, m * m),
            step("D", RHS, B, n * n),
            step("REWRITE", std),
            step("FORM_IDENTIFY", "ellipse",
                 f"center ({h}, {k})"),
            step("Z", std),
        ]
        problem = f"Write in standard form: {eq}."
        return self._pack(problem, steps, std, "ellipse")

    def _pack(self, problem, steps, answer, kind):
        return dict(
            problem_id=jid(),
            operation=f"conic_standard_form_{kind}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
