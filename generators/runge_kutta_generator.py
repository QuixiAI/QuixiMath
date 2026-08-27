import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.euler_method_generator import f_txt, f_sub


COEFFICIENTS = list(range(-3, 4))
CONSTANTS = list(range(-5, 6))
STEP_SIZES = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 5)]
START_X = [Fraction(v, 2) for v in range(-6, 7)]
START_Y = [Fraction(v, 2) for v in range(-10, 21) if v != 0]
VARIABLE_PAIRS = [
    ("x", "y"), ("t", "y"), ("t", "P"), ("t", "v"), ("x", "u"),
    ("t", "N"), ("t", "Q"), ("s", "w"), ("x", "w"), ("t", "M"),
]
NAMES = [
    "Aisha", "Ben", "Cleo", "Diego", "Emi", "Farah", "Grace", "Hugo",
    "Imani", "Jonas", "Kavya", "Liam", "Maya", "Noah", "Omar", "Priya",
    "Quinn", "Rosa", "Samir", "Tara", "Uma", "Vera", "Wes", "Ximena",
]
SETTINGS = [
    "numerical methods class", "the computing lab", "study hall",
    "a differential-equations workshop", "the library", "a review session",
    "the applied-math seminar", "a tutoring session", "the learning center",
    "an engineering methods class", "the problem-solving circle",
    "an exam-prep group",
]
PROBLEM_TEMPLATES = [
    "At {place}, {name} uses {method} on ODE [{ode}; {ic}]. With step size "
    "h = {h}, approximate {goal} after one step.",
    "{name} is working in {place}. For ODE [{ode}; {ic}], take one {method} "
    "step of size h = {h} and estimate {goal}.",
    "During {place}, {name} studies ODE [{ode}; {ic}]. Apply {method} with "
    "h = {h} to approximate {goal}.",
    "A worksheet for {name} at {place} gives ODE [{ode}; {ic}]. Use {method} "
    "and step size h = {h} to find the one-step approximation to {goal}.",
    "For a calculation in {place}, {name} starts with ODE [{ode}; {ic}]. "
    "Using {method} at h = {h}, approximate {goal}.",
    "{name} checks a numerical solution during {place}: ODE [{ode}; {ic}]. "
    "Take one step with {method}, h = {h}, and report {goal}.",
]


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
    One-step RK2 midpoint and classical RK4 tables for
    d(dep)/d(indep) = a·indep + b·dep + c.

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
        for _ in range(500):
            a, b, c = self._coefficients()
            h = random.choice(STEP_SIZES)
            x0 = random.choice(START_X)
            y0 = random.choice(START_Y)
            if self._friendly(variant, a, b, c, h, x0, y0):
                break
        else:  # pragma: no cover - defensive total fallback
            a, b, c = 1, 1, 0
            h, x0, y0 = Fraction(1, 2), Fraction(0), Fraction(2)
        indep, dep = random.choice(VARIABLE_PAIRS)
        if variant == "rk2":
            problem, steps, answer = self._generate_rk2(
                a, b, c, h, x0, y0, indep, dep)
        else:
            problem, steps, answer = self._generate_rk4(
                a, b, c, h, x0, y0, indep, dep)
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
            a, b = random.choice(COEFFICIENTS), random.choice(COEFFICIENTS)
            c = random.choice(CONSTANTS)
            if (a, b, c) != (0, 0, 0):
                return a, b, c

    @staticmethod
    def _friendly(variant, a, b, c, h, x0, y0):
        """Reject tables whose exact fractions become unpleasant by hand."""
        def f(x, y):
            return a * x + b * y + c

        k1 = f(x0, y0)
        if variant == "rk2":
            x_mid, y_mid = x0 + h / 2, y0 + h * k1 / 2
            k2 = f(x_mid, y_mid)
            values = (k1, x_mid, y_mid, k2, h * k2, y0 + h * k2)
        else:
            x_half = x0 + h / 2
            y2 = y0 + h * k1 / 2
            k2 = f(x_half, y2)
            y3 = y0 + h * k2 / 2
            k3 = f(x_half, y3)
            x_full = x0 + h
            y4 = y0 + h * k3
            k4 = f(x_full, y4)
            weighted = k1 + 2 * k2 + 2 * k3 + k4
            values = (k1, x_half, y2, k2, y3, k3, x_full, y4, k4,
                      weighted, h * weighted / 6,
                      y0 + h * weighted / 6)
        return all(abs(value) <= 200 and value.denominator <= 4096
                   and abs(value.numerator) <= 50000 for value in values)

    @staticmethod
    def _problem(method, a, b, c, h, x0, y0, indep, dep):
        target = x0 + h
        fields = dict(
            name=random.choice(NAMES), place=random.choice(SETTINGS),
            method=method,
            ode=f"d{dep}/d{indep} = {f_txt(a, b, c, indep, dep)}",
            ic=f"{dep}({fraction_text(x0)}) = {fraction_text(y0)}",
            h=fraction_text(h),
            goal=f"{dep}({fraction_text(target)})",
        )
        return random.choice(PROBLEM_TEMPLATES).format(**fields)

    def _eval_stage(self, steps, label, a, b, c, x_value, y_value,
                    indep, dep):
        k = a * x_value + b * y_value + c
        steps.append(step("RK_STAGE", label,
                          f"{indep}={fraction_text(x_value)}",
                          f"{dep}={fraction_text(y_value)}"))
        steps.append(step("EVAL", f"f({fraction_text(x_value)},"
                          f"{fraction_text(y_value)})",
                          f"{f_sub(a, b, c, fraction_text(x_value), fraction_text(y_value))}"
                          f" = {fraction_text(k)}"))
        return k

    def _generate_rk2(self, a, b, c, h, x0, y0, indep, dep):
        half_h = h / 2
        steps = [
            step("ODE_SETUP", f"d{dep}/d{indep} = {f_txt(a, b, c, indep, dep)}, "
                 f"{dep}({fraction_text(x0)}) = {fraction_text(y0)}",
                 f"RK2 midpoint, h = {fraction_text(h)}"),
        ]
        k1 = self._eval_stage(steps, "k1", a, b, c, x0, y0, indep, dep)
        steps.append(step("D", fraction_text(h), 2, fraction_text(half_h)))
        k1_half = half_h * k1
        steps.append(step("M", fraction_text(half_h), fraction_text(k1),
                          fraction_text(k1_half)))
        x_mid = x0 + half_h
        y_mid = y0 + k1_half
        steps.append(step("A", fraction_text(x0), fraction_text(half_h),
                          fraction_text(x_mid)))
        add_or_sub_step(steps, y0, k1_half, y_mid)
        k2 = self._eval_stage(steps, "k2", a, b, c, x_mid, y_mid,
                              indep, dep)
        increment = h * k2
        y1 = y0 + increment
        steps.append(step("M", fraction_text(h), fraction_text(k2),
                          fraction_text(increment)))
        add_or_sub_step(steps, y0, increment, y1)
        answer = fraction_text(y1)
        problem = self._problem("RK2 midpoint", a, b, c, h, x0, y0,
                                indep, dep)
        return problem, steps, answer

    def _generate_rk4(self, a, b, c, h, x0, y0, indep, dep):
        half_h = h / 2
        steps = [
            step("ODE_SETUP", f"d{dep}/d{indep} = {f_txt(a, b, c, indep, dep)}, "
                 f"{dep}({fraction_text(x0)}) = {fraction_text(y0)}",
                 f"RK4, h = {fraction_text(h)}"),
        ]
        steps.append(step("D", fraction_text(h), 2, fraction_text(half_h)))
        k1 = self._eval_stage(steps, "k1", a, b, c, x0, y0, indep, dep)
        x_half = x0 + half_h
        steps.append(step("A", fraction_text(x0), fraction_text(half_h),
                          fraction_text(x_half)))
        y_k2 = y0 + half_h * k1
        steps.append(step("M", fraction_text(half_h), fraction_text(k1),
                          fraction_text(half_h * k1)))
        add_or_sub_step(steps, y0, half_h * k1, y_k2)
        k2 = self._eval_stage(steps, "k2", a, b, c, x_half, y_k2,
                              indep, dep)
        y_k3 = y0 + half_h * k2
        steps.append(step("M", fraction_text(half_h), fraction_text(k2),
                          fraction_text(half_h * k2)))
        add_or_sub_step(steps, y0, half_h * k2, y_k3)
        k3 = self._eval_stage(steps, "k3", a, b, c, x_half, y_k3,
                              indep, dep)
        x_full = x0 + h
        steps.append(step("A", fraction_text(x0), fraction_text(h),
                          fraction_text(x_full)))
        y_k4 = y0 + h * k3
        steps.append(step("M", fraction_text(h), fraction_text(k3),
                          fraction_text(h * k3)))
        add_or_sub_step(steps, y0, h * k3, y_k4)
        k4 = self._eval_stage(steps, "k4", a, b, c, x_full, y_k4,
                              indep, dep)
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
        problem = self._problem("RK4", a, b, c, h, x0, y0, indep, dep)
        return problem, steps, answer
