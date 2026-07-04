import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.euler_method_generator import f_txt, f_sub


def fraction_text(value):
    return str(Fraction(value))


def add_or_sub_step(steps, left, delta, result):
    if delta >= 0:
        steps.append(step("A", fraction_text(left), fraction_text(delta),
                          fraction_text(result)))
    else:
        steps.append(step("S", fraction_text(left), fraction_text(-delta),
                          fraction_text(result)))


class RungeKuttaGenerator(ProblemGenerator):
    """
    One-step RK2 midpoint and classical RK4 tables for dy/dx = ax + by.

    Op-codes used:
    - ODE_SETUP: equation, initial value, method, and step size
    - RK_STAGE: one Runge-Kutta stage point
    - RK_COMBINE: weighted RK4 stage sum
    - EVAL / M / D / A / S (established/shared): exact stage arithmetic
    - Z: one-step approximation
    """

    VARIANTS = ["rk2", "rk4"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a, b = self._coefficients()
        h = random.choice([Fraction(1, 2), Fraction(1, 4)])
        y0 = Fraction(random.randint(1, 5), 1)
        if variant == "rk2":
            problem, steps, answer = self._generate_rk2(a, b, h, y0)
        else:
            problem, steps, answer = self._generate_rk4(a, b, h, y0)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"runge_kutta_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _coefficients(self):
        while True:
            a, b = random.randint(-2, 2), random.randint(-2, 2)
            if (a, b) != (0, 0):
                return a, b

    def _eval_stage(self, steps, label, a, b, x_value, y_value):
        k = a * x_value + b * y_value
        steps.append(step("RK_STAGE", label, f"x={fraction_text(x_value)}",
                          f"y={fraction_text(y_value)}"))
        steps.append(step("EVAL", f"f({fraction_text(x_value)},"
                          f"{fraction_text(y_value)})",
                          f"{f_sub(a, b, fraction_text(x_value), fraction_text(y_value))}"
                          f" = {fraction_text(k)}"))
        return k

    def _generate_rk2(self, a, b, h, y0):
        x0 = Fraction(0)
        half_h = h / 2
        steps = [
            step("ODE_SETUP", f"dy/dx = {f_txt(a, b)}, y(0) = "
                 f"{fraction_text(y0)}", f"RK2 midpoint, h = {fraction_text(h)}"),
        ]
        k1 = self._eval_stage(steps, "k1", a, b, x0, y0)
        steps.append(step("D", fraction_text(h), 2, fraction_text(half_h)))
        k1_half = half_h * k1
        steps.append(step("M", fraction_text(half_h), fraction_text(k1),
                          fraction_text(k1_half)))
        x_mid = x0 + half_h
        y_mid = y0 + k1_half
        steps.append(step("A", fraction_text(x0), fraction_text(half_h),
                          fraction_text(x_mid)))
        add_or_sub_step(steps, y0, k1_half, y_mid)
        k2 = self._eval_stage(steps, "k2", a, b, x_mid, y_mid)
        increment = h * k2
        y1 = y0 + increment
        steps.append(step("M", fraction_text(h), fraction_text(k2),
                          fraction_text(increment)))
        add_or_sub_step(steps, y0, increment, y1)
        answer = fraction_text(y1)
        problem = (
            f"Use RK2 midpoint with step size h = {fraction_text(h)} to "
            f"approximate y({fraction_text(h)}) for dy/dx = {f_txt(a, b)} "
            f"with y(0) = {fraction_text(y0)}."
        )
        return problem, steps, answer

    def _generate_rk4(self, a, b, h, y0):
        x0 = Fraction(0)
        half_h = h / 2
        steps = [
            step("ODE_SETUP", f"dy/dx = {f_txt(a, b)}, y(0) = "
                 f"{fraction_text(y0)}", f"RK4, h = {fraction_text(h)}"),
        ]
        steps.append(step("D", fraction_text(h), 2, fraction_text(half_h)))
        k1 = self._eval_stage(steps, "k1", a, b, x0, y0)
        x_half = x0 + half_h
        steps.append(step("A", fraction_text(x0), fraction_text(half_h),
                          fraction_text(x_half)))
        y_k2 = y0 + half_h * k1
        steps.append(step("M", fraction_text(half_h), fraction_text(k1),
                          fraction_text(half_h * k1)))
        add_or_sub_step(steps, y0, half_h * k1, y_k2)
        k2 = self._eval_stage(steps, "k2", a, b, x_half, y_k2)
        y_k3 = y0 + half_h * k2
        steps.append(step("M", fraction_text(half_h), fraction_text(k2),
                          fraction_text(half_h * k2)))
        add_or_sub_step(steps, y0, half_h * k2, y_k3)
        k3 = self._eval_stage(steps, "k3", a, b, x_half, y_k3)
        x_full = x0 + h
        steps.append(step("A", fraction_text(x0), fraction_text(h),
                          fraction_text(x_full)))
        y_k4 = y0 + h * k3
        steps.append(step("M", fraction_text(h), fraction_text(k3),
                          fraction_text(h * k3)))
        add_or_sub_step(steps, y0, h * k3, y_k4)
        k4 = self._eval_stage(steps, "k4", a, b, x_full, y_k4)
        two_k2 = 2 * k2
        two_k3 = 2 * k3
        sum1 = k1 + two_k2
        sum2 = sum1 + two_k3
        weighted = sum2 + k4
        h_over_6 = h / 6
        increment = h_over_6 * weighted
        y1 = y0 + increment
        steps.extend([
            step("M", 2, fraction_text(k2), fraction_text(two_k2)),
            step("M", 2, fraction_text(k3), fraction_text(two_k3)),
            step("A", fraction_text(k1), fraction_text(two_k2),
                 fraction_text(sum1)),
            step("A", fraction_text(sum1), fraction_text(two_k3),
                 fraction_text(sum2)),
            step("A", fraction_text(sum2), fraction_text(k4),
                 fraction_text(weighted)),
            step("RK_COMBINE", "k1+2k2+2k3+k4", fraction_text(weighted)),
            step("D", fraction_text(h), 6, fraction_text(h_over_6)),
            step("M", fraction_text(h_over_6), fraction_text(weighted),
                 fraction_text(increment)),
        ])
        add_or_sub_step(steps, y0, increment, y1)
        answer = fraction_text(y1)
        problem = (
            f"Use RK4 with step size h = {fraction_text(h)} to approximate "
            f"y({fraction_text(h)}) for dy/dx = {f_txt(a, b)} with "
            f"y(0) = {fraction_text(y0)}."
        )
        return problem, steps, answer
