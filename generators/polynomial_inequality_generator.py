import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


REL = ["<", "≤", ">", "≥"]


def fmt_num(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fac(root):
    if root == 0:
        return "x"
    return f"(x - {root})" if root > 0 else f"(x + {-root})"


def poly_quad(r1, r2):
    b = -(r1 + r2)
    c = r1 * r2
    parts = ["x^2"]
    if b:
        parts.append(f"+ {b}x" if b > 0 else f"- {-b}x")
    if c:
        parts.append(f"+ {c}" if c > 0 else f"- {-c}")
    return " ".join(parts)


def interval_piece(left, right, include_left=False, include_right=False):
    lbr = "[" if include_left else "("
    rbr = "]" if include_right else ")"
    ltxt = "-∞" if left is None else fmt_num(left)
    rtxt = "∞" if right is None else fmt_num(right)
    if left is None:
        lbr = "("
    if right is None:
        rbr = ")"
    return f"{lbr}{ltxt}, {rtxt}{rbr}"


def interval_answer(accepted, closed_points, open_points):
    pieces = []
    for left, right in accepted:
        include_left = left in closed_points and left not in open_points
        include_right = right in closed_points and right not in open_points
        pieces.append(interval_piece(left, right, include_left, include_right))
    return " ∪ ".join(pieces) if pieces else "No solution"


def test_point(left, right):
    if left is None:
        return Fraction(right) - 1
    if right is None:
        return Fraction(left) + 1
    return (Fraction(left) + Fraction(right)) / 2


def relation_ok(value, rel):
    return {
        "<": value < 0,
        "≤": value <= 0,
        ">": value > 0,
        "≥": value >= 0,
    }[rel]


class PolynomialInequalityGenerator(ProblemGenerator):
    """
    Polynomial and rational inequalities solved by sign charts.

    Variants:
    - factored_quadratic: solve a factored quadratic inequality.
    - expanded_quadratic: factor a quadratic first, then solve.
    - cubic: solve a cubic with three integer zeros.
    - rational: solve a linear-over-linear rational inequality, excluding
      the pole even for non-strict inequalities.

    Op-codes used:
    - INEQ_SETUP: expression and relation
    - FACTOR / ZERO_PRODUCT: zeros or critical values
    - SIGN_CHART / TRY / ACCEPT / REJECT: interval testing
    - CHECK: pole exclusion for rational inequalities
    - Z: canonical interval notation
    """

    VARIANTS = ["factored_quadratic", "expanded_quadratic", "cubic",
                "rational"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        rel = random.choice(REL)
        if variant == "factored_quadratic":
            r1, r2 = sorted(random.sample(range(-8, 9), 2))
            expr = f"{fac(r1)}{fac(r2)}"
            factored = expr
            intervals, accepted = self._poly_intervals([r1, r2], rel)
            closed = {r1, r2} if rel in ("≤", "≥") else set()
            answer = interval_answer(accepted, closed, set())
            steps = self._poly_steps(expr, factored, [r1, r2], rel,
                                     intervals, accepted)
            problem = f"Solve {expr} {rel} 0. Give the answer in interval notation."
        elif variant == "expanded_quadratic":
            r1, r2 = sorted(random.sample(range(-8, 9), 2))
            expr = poly_quad(r1, r2)
            factored = f"{fac(r1)}{fac(r2)}"
            intervals, accepted = self._poly_intervals([r1, r2], rel)
            closed = {r1, r2} if rel in ("≤", "≥") else set()
            answer = interval_answer(accepted, closed, set())
            steps = self._poly_steps(expr, factored, [r1, r2], rel,
                                     intervals, accepted)
            problem = f"Solve {expr} {rel} 0. Give the answer in interval notation."
        elif variant == "cubic":
            roots = sorted(random.sample(range(-6, 7), 3))
            expr = "".join(fac(r) for r in roots)
            intervals, accepted = self._poly_intervals(roots, rel)
            closed = set(roots) if rel in ("≤", "≥") else set()
            answer = interval_answer(accepted, closed, set())
            steps = self._poly_steps(expr, expr, roots, rel, intervals,
                                     accepted)
            problem = f"Solve {expr} {rel} 0. Give the answer in interval notation."
        else:
            zero, pole = random.sample(range(-8, 9), 2)
            expr = f"{fac(zero)}/{fac(pole)}"
            intervals, accepted = self._rational_intervals(zero, pole, rel)
            closed = {zero} if rel in ("≤", "≥") else set()
            answer = interval_answer(accepted, closed, {pole})
            steps = [
                step("INEQ_SETUP", f"{expr} {rel} 0"),
                step("ZERO_PRODUCT", f"{fac(zero)} = 0", f"x = {zero}"),
                step("CHECK", f"{fac(pole)} = 0", f"x = {pole}",
                     "excluded pole"),
                step("SIGN_CHART", "critical values",
                     ", ".join(fmt_num(v) for v in sorted([zero, pole]))),
            ]
            steps += self._chart_steps(expr, rel, intervals, accepted)
            problem = f"Solve {expr} {rel} 0. Give the answer in interval notation."

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"polynomial_inequality_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    @staticmethod
    def _poly_value(x, roots):
        out = Fraction(1)
        for root in roots:
            out *= x - root
        return out

    def _poly_intervals(self, roots, rel):
        bounds = [None] + sorted(roots) + [None]
        intervals = list(zip(bounds[:-1], bounds[1:]))
        accepted = []
        for left, right in intervals:
            x = test_point(left, right)
            if relation_ok(self._poly_value(x, roots), rel):
                accepted.append((left, right))
        return intervals, accepted

    @staticmethod
    def _rational_intervals(zero, pole, rel):
        pts = sorted([zero, pole])
        bounds = [None] + pts + [None]
        intervals = list(zip(bounds[:-1], bounds[1:]))
        accepted = []
        for left, right in intervals:
            x = test_point(left, right)
            value = (x - zero) / (x - pole)
            if relation_ok(value, rel):
                accepted.append((left, right))
        return intervals, accepted

    def _poly_steps(self, expr, factored, roots, rel, intervals, accepted):
        steps = [step("INEQ_SETUP", f"{expr} {rel} 0")]
        if expr != factored:
            steps.append(step("FACTOR", expr, factored))
        steps.append(step("ZERO_PRODUCT", factored,
                          " or ".join(f"x = {r}" for r in roots)))
        steps.append(step("SIGN_CHART", "zeros",
                          ", ".join(str(r) for r in roots)))
        steps += self._chart_steps(factored, rel, intervals, accepted)
        return steps

    @staticmethod
    def _chart_steps(expr, rel, intervals, accepted):
        steps = []
        for left, right in intervals:
            x = test_point(left, right)
            label = interval_piece(left, right)
            verdict = "accept" if (left, right) in accepted else "reject"
            steps.append(step("TRY", label, f"x = {fmt_num(x)}"))
            steps.append(step("ACCEPT" if verdict == "accept" else "REJECT",
                              label, f"{expr} {rel} 0 is {verdict}"))
        return steps
