import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


# Hand-friendly slope-field coefficients: integers and halves.
COEF_CHOICES = [Fraction(v) for v in
                ("-3", "-2", "-1.5", "-1", "-0.5", "0",
                 "0.5", "1", "1.5", "2", "3")]
CONST_CHOICES = [Fraction(v) for v in
                 ("-5", "-4", "-3", "-2", "-1", "-0.5", "0", "0.5",
                  "1", "1.5", "2", "2.5", "3", "4", "5")]
H_CHOICES = [Fraction(v) for v in ("0.1", "0.2", "0.25", "0.4", "0.5")]
X0_CHOICES = [Fraction(v) for v in
              ("0", "0", "0", "1", "2", "3", "-1", "-2",
               "0.5", "1.5", "2.5", "-0.5")]
Y0_CHOICES = [Fraction(v) for v in
              ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
               "-1", "-2", "-3", "-4", "-5",
               "0.5", "1.5", "2.5", "3.5", "-1.5", "-2.5")]
# (independent, dependent) letter pairs; both single letters so the
# right-hand side never collides with an English word.
VAR_PAIRS = [("x", "y"), ("t", "y"), ("t", "P"), ("t", "v"), ("x", "u"),
             ("t", "N"), ("t", "Q"), ("s", "w"), ("x", "w"), ("t", "M")]

MAX_DP = 4          # decimal places any table value may show
MAX_MAG = 400       # magnitude any table value may reach


def _dp(fr):
    """Number of decimal places in the exact decimal render of ``fr``."""
    s = dec(fr)
    return len(s.split(".")[1]) if "." in s else 0


def _term(coef, var):
    """Render abs(coef)·var with unit coefficients cleaned up."""
    mag = abs(coef)
    if var is None:
        return dec(mag)
    if mag == 1:
        return var
    return f"{dec(mag)}{var}"


def f_txt(a, b, c, indep="x", dep="y"):
    """a·indep + b·dep + c with unit coefficients and zero terms cleaned."""
    out = ""
    for coef, var in ((a, indep), (b, dep), (c, None)):
        if coef == 0:
            continue
        body = _term(coef, var)
        if not out:
            out = body if coef > 0 else f"-{body}"
        else:
            out += f" + {body}" if coef > 0 else f" - {body}"
    return out or "0"


def f_sub(a, b, c, xv, yv):
    """The right-hand side with the current values substituted in."""
    def sub(coef, val):
        mag = abs(coef)
        if val is None:
            return dec(mag)
        if mag == 1:
            return f"({val})"
        return f"{dec(mag)}({val})"

    out = ""
    for coef, val in ((a, xv), (b, yv), (c, None)):
        if coef == 0:
            continue
        body = sub(coef, val)
        if not out:
            out = body if coef > 0 else f"-{body}"
        else:
            out += f" + {body}" if coef > 0 else f" - {body}"
    return out or "0"


def euler_table(a, b, c, h, x0, y0, n):
    """Exact Euler run.  Returns rows ``(x, y, k, hk, x2, y2)`` or ``None``
    when some value in the table would be too wide to work by hand."""
    rows = []
    x, y = x0, y0
    if _dp(x) > MAX_DP or _dp(y) > MAX_DP:
        return None
    for _ in range(n):
        k = a * x + b * y + c
        hk = h * k
        x2, y2 = x + h, y + hk
        for val in (k, hk, x2, y2):
            if _dp(val) > MAX_DP or abs(val) > MAX_MAG:
                return None
        rows.append((x, y, k, hk, x2, y2))
        x, y = x2, y2
    return rows


class EulerMethodGenerator(ProblemGenerator):
    """
    Euler's method for dy/dx = ax + by + c as a pure scratchpad table:
    each row records x and y, then the slope is evaluated explicitly,
    scaled by h, and added on.  Step sizes, coefficients, and initial
    conditions are terminating decimals and the table is rejected unless
    every entry stays short, so every value is exact and hand-writable.

    Variants:
    - two_step / three_step / four_step: the number of Euler updates

    Widened axes: slope coefficients (integers and halves) plus a constant
    term, non-zero starting abscissa, decimal initial values, five step
    sizes, ten independent/dependent variable letter pairs, and five
    problem phrasings.

    Op-codes used:
    - ODE_SETUP (established): the equation, IC, and the method
    - TABLE_ENTRY (established): one row of the Euler table
    - EVAL / M / A / S (established): slope, h·k, and the update
    - Z: the approximation for y at the target x
    """

    VARIANTS = ["two_step", "three_step", "four_step"]
    STEPS_FOR = {"two_step": 2, "three_step": 3, "four_step": 4}

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        n = self.STEPS_FOR[variant]

        rows = None
        for _ in range(500):
            a = random.choice(COEF_CHOICES)
            b = random.choice(COEF_CHOICES)
            if a == 0 and b == 0:
                continue
            c = random.choice(CONST_CHOICES)
            h = random.choice(H_CHOICES)
            x0 = random.choice(X0_CHOICES)
            y0 = random.choice(Y0_CHOICES)
            rows = euler_table(a, b, c, h, x0, y0, n)
            if rows is not None:
                break
        if rows is None:  # pragma: no cover - fallback keeps generate total
            a, b, c = Fraction(1), Fraction(0), Fraction(0)
            h, x0, y0 = Fraction(1, 2), Fraction(0), Fraction(2)
            rows = euler_table(a, b, c, h, x0, y0, n)

        indep, dep = random.choice(VAR_PAIRS)
        rhs = f_txt(a, b, c, indep, dep)
        deriv = f"d{dep}/d{indep}"
        target = x0 + h * n

        steps = [
            step("ODE_SETUP", f"{deriv} = {rhs}, {dep}({dec(x0)}) = {dec(y0)}",
                 f"Euler's method with h = {dec(h)}",
                 f"{n} steps to {indep} = {dec(target)}"),
            step("TABLE_ENTRY", f"{indep} = {dec(x0)}", f"{dep} = {dec(y0)}"),
        ]
        for x, y, k, hk, x2, y2 in rows:
            steps.append(step("EVAL", f"f({dec(x)}, {dec(y)})",
                              f"{f_sub(a, b, c, dec(x), dec(y))} = {dec(k)}"))
            steps.append(step("M", dec(h), dec(k), dec(hk)))
            if hk > 0:
                steps.append(step("A", dec(y), dec(hk), dec(y2)))
            elif hk < 0:
                steps.append(step("S", dec(y), dec(-hk), dec(y2)))
            steps.append(step("TABLE_ENTRY", f"{indep} = {dec(x2)}",
                              f"{dep} = {dec(y2)}"))
        answer = dec(rows[-1][5])
        steps.append(step("Z", answer))

        ic = f"{dep}({dec(x0)}) = {dec(y0)}"
        goal = f"{dep}({dec(target)})"
        phrasings = [
            (f"Use Euler's method with step size h = {dec(h)} to "
             f"approximate {goal} for {deriv} = {rhs} with {ic}."),
            (f"Starting from {ic}, apply Euler's method to {deriv} = {rhs} "
             f"with step size h = {dec(h)} and estimate {goal}."),
            (f"Approximate {goal} using {n} steps of Euler's method on "
             f"{deriv} = {rhs}, given {ic} and step size h = {dec(h)}."),
            (f"The initial value problem {deriv} = {rhs}, {ic} is solved "
             f"numerically. Take {n} Euler steps of size h = {dec(h)} and "
             f"report the approximation to {goal}."),
            (f"Euler's method with h = {dec(h)} is applied to "
             f"{deriv} = {rhs} from {ic}. What approximation does it give "
             f"for {goal}?"),
        ]
        problem = random.choice(phrasings)

        return dict(
            problem_id=jid(),
            operation=f"euler_method_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
