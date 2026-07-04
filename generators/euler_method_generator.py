import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def f_txt(a, b):
    """ax + by with unit coefficients and zero terms cleaned up."""
    xt = "" if a == 0 else ("x" if a == 1 else
                            "-x" if a == -1 else f"{a}x")
    if b == 0:
        return xt
    yt = "y" if abs(b) == 1 else f"{abs(b)}y"
    if not xt:
        return yt if b > 0 else f"-{yt}"
    return f"{xt} + {yt}" if b > 0 else f"{xt} - {yt}"


def f_sub(a, b, xv, yv):
    """ax + by with the values substituted and parenthesized."""
    def term(c, v):
        if c == 1:
            return f"({v})"
        if c == -1:
            return f"-({v})"
        return f"{c}({v})"
    if a == 0:
        return term(b, yv)
    if b == 0:
        return term(a, xv)
    out = term(a, xv)
    out += f" + {term(abs(b), yv)}" if b > 0 else f" - {term(abs(b), yv)}"
    return out


class EulerMethodGenerator(ProblemGenerator):
    """
    Euler's method for dy/dx = ax + by as a pure scratchpad table:
    each row records x and y, then the slope is evaluated explicitly,
    scaled by h, and added on. Step sizes are terminating decimals so
    every value in the table is exact.

    Variants:
    - two_step / three_step: the number of Euler updates

    Op-codes used:
    - ODE_SETUP (established): the equation, IC, and the method
    - TABLE_ENTRY (established): one row of the Euler table
    - EVAL / M / A / S (established): slope, h·k, and the update
    - Z: the approximation for y at the target x
    """

    VARIANTS = ["two_step", "three_step"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = 2 if variant == "two_step" else 3
        h = Fraction(random.choice(["0.1", "0.2", "0.5"]))
        while True:
            a, b = random.randint(-2, 2), random.randint(-2, 2)
            if (a, b) != (0, 0):
                break
        y0 = random.randint(1, 5)
        target = h * n

        steps = [
            step("ODE_SETUP", f"dy/dx = {f_txt(a, b)}, y(0) = {y0}",
                 f"Euler's method with h = {dec(h)}"),
            step("TABLE_ENTRY", "x = 0", f"y = {y0}"),
        ]
        x, y = Fraction(0), Fraction(y0)
        for _ in range(n):
            k = a * x + b * y
            hk = h * k
            steps.append(step("EVAL", f"f({dec(x)}, {dec(y)})",
                              f"{f_sub(a, b, dec(x), dec(y))} = {dec(k)}"))
            steps.append(step("M", dec(h), dec(k), dec(hk)))
            x2, y2 = x + h, y + hk
            if hk > 0:
                steps.append(step("A", dec(y), dec(hk), dec(y2)))
            elif hk < 0:
                steps.append(step("S", dec(y), dec(-hk), dec(y2)))
            steps.append(step("TABLE_ENTRY", f"x = {dec(x2)}",
                              f"y = {dec(y2)}"))
            x, y = x2, y2
        answer = dec(y)
        steps.append(step("Z", answer))

        problem = (f"Use Euler's method with step size h = {dec(h)} to "
                   f"approximate y({dec(target)}) for "
                   f"dy/dx = {f_txt(a, b)} with y(0) = {y0}.")
        return dict(
            problem_id=jid(),
            operation=f"euler_method_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
