import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def factor_txt(root):
    if root == 0:
        return "y"
    return f"(y - {root})" if root > 0 else f"(y + {abs(root)})"


def f_txt(leading, roots):
    body = "".join(factor_txt(root) for root in roots)
    return body if leading > 0 else f"-{body}"


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def eval_poly(leading, roots, y):
    value = Fraction(leading)
    for root in roots:
        value *= y - root
    return value


def sign_word(value):
    return "positive" if value > 0 else "negative"


def arrow(value):
    return "up" if value > 0 else "down"


def interval_txt(index, roots):
    if index == 0:
        return f"(-inf, {roots[0]})"
    if index == len(roots):
        return f"({roots[-1]}, inf)"
    return f"({roots[index - 1]}, {roots[index]})"


def test_point(index, roots):
    if index == 0:
        return Fraction(roots[0] - 1)
    if index == len(roots):
        return Fraction(roots[-1] + 1)
    return Fraction(roots[index - 1] + roots[index], 2)


def classify(left_sign, right_sign):
    if left_sign > 0 and right_sign < 0:
        return "stable"
    if left_sign < 0 and right_sign > 0:
        return "unstable"
    return "semistable"


def answer_txt(roots, classes):
    pieces = [f"y={root} {cls}" for root, cls in zip(roots, classes)]
    return "equilibria: " + "; ".join(pieces)


class StabilityGenerator(ProblemGenerator):
    """
    Equilibria and stability for autonomous ODEs dy/dt = f(y).

    Variant:
    - factored_polynomial: f(y) has two or three simple integer roots

    Op-codes used:
    - ODE_SETUP (established): autonomous equation and task
    - EQUILIBRIA: roots of f(y)=0
    - SIGN_TEST: interval test values and signs
    - STABILITY: classify each equilibrium from neighboring signs
    - Z: composite stability classification
    """

    VARIANTS = ["factored_polynomial"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        count = random.choice([2, 3])
        roots = sorted(random.sample(range(-5, 6), count))
        leading = random.choice([-1, 1])
        signs = []
        steps = [
            step("ODE_SETUP", f"dy/dt = {f_txt(leading, roots)}",
                 "equilibria and stability"),
            step("EQUILIBRIA", "f(y) = 0",
                 ", ".join(f"y={root}" for root in roots)),
        ]
        for index in range(len(roots) + 1):
            point = test_point(index, roots)
            value = eval_poly(leading, roots, point)
            signs.append(1 if value > 0 else -1)
            steps.append(step("SIGN_TEST", interval_txt(index, roots),
                              f"y = {fmt_frac(point)}",
                              f"f(y) = {fmt_frac(value)} ({sign_word(value)})",
                              arrow(value)))
        classes = []
        for index, root in enumerate(roots):
            cls = classify(signs[index], signs[index + 1])
            classes.append(cls)
            steps.append(step("STABILITY", f"y={root}",
                              f"left {arrow(signs[index])}, "
                              f"right {arrow(signs[index + 1])}",
                              cls))
        answer = answer_txt(roots, classes)
        steps.append(step("Z", answer))
        problem = (
            f"For dy/dt = {f_txt(leading, roots)}, find equilibria and "
            f"classify stability by sign analysis."
        )
        return dict(
            problem_id=jid(),
            operation="stability_factored_polynomial",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
