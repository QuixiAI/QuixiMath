import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sub(n):
    """A substituted input is always parenthesized: 2(3) + 5, (-2)^2."""
    return f"({n})"


class FunctionTableGenerator(ProblemGenerator):
    """
    Builds a value table from a rule: evaluate f at each listed input.

    Variants:
    - linear:      f(x) = ax + b   at four consecutive integers spanning 0
    - quadratic:   f(x) = ax^2 + c at four consecutive integers spanning 0
    - exponential: f(x) = a · b^x  at x = 0, 1, 2, 3

    Every row is worked in full: substitute, chain the arithmetic, then
    record the row with TABLE_ENTRY. The final answer is the completed
    f(x) row in input order.

    Op-codes used:
    - FUNC_SETUP: the rule and the inputs to evaluate (rule, input list)
    - SUBST: substitute one input (variable, value, resulting expression)
    - E / M / A: the arithmetic (established meanings)
    - TABLE_ENTRY: record one completed table row (entry, value)
    - Z: final answer
    """

    VARIANTS = ["linear", "quadratic", "exponential"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        fname = random.choice(["f", "g", "h"])
        var = random.choice(["x", "x", "t"])

        if variant == "exponential":
            a = random.randint(1, 9)
            base = random.choice([2, 3, 4, 5])
            xs = [0, 1, 2, 3]
            rule = (f"{fname}({var}) = {base}^{var}" if a == 1
                    else f"{fname}({var}) = {a} · {base}^{var}")
        else:
            start = random.choice([-3, -2, -1])
            xs = list(range(start, start + 4))
            b = random.choice([v for v in range(-9, 10) if v != 0])
            b_txt = f"+ {b}" if b > 0 else f"- {-b}"
            if variant == "linear":
                a = random.choice(
                    [v for v in range(-5, 6) if v not in (-1, 0, 1)])
                rule = f"{fname}({var}) = {a}{var} {b_txt}"
            else:
                a = random.choice([v for v in range(-3, 4) if v != 0])
                a_txt = {1: "", -1: "-"}.get(a, str(a))
                rule = f"{fname}({var}) = {a_txt}{var}^2 {b_txt}"

        x_list = ", ".join(str(x) for x in xs)
        steps = [step("FUNC_SETUP", rule, f"{var} = {x_list}")]
        values = []

        for k in xs:
            if variant == "linear":
                value = a * k + b
                steps.append(step("SUBST", var, k, f"{a}{sub(k)} {b_txt}"))
                steps.append(step("M", a, k, a * k))
                steps.append(step("A", a * k, b, value))
            elif variant == "quadratic":
                sq = k * k
                t1 = a * sq
                value = t1 + b
                prefix = {1: "", -1: "-"}.get(a, str(a))
                steps.append(step("SUBST", var, k,
                                  f"{prefix}{sub(k)}^2 {b_txt}"))
                steps.append(step("E", sub(k), 2, sq))
                if a != 1:
                    steps.append(step("M", a, sq, t1))
                steps.append(step("A", t1, b, value))
            else:
                power = base ** k
                value = a * power
                expr = (f"{base}^{k}" if a == 1
                        else f"{a} · {base}^{k}")
                steps.append(step("SUBST", var, k, expr))
                steps.append(step("E", base, k, power))
                if a != 1:
                    steps.append(step("M", a, power, value))
            steps.append(step("TABLE_ENTRY", f"{fname}({k})", value))
            values.append(value)

        answer = ", ".join(str(v) for v in values)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="function_table",
            problem=(f"Complete the table for {rule} at {var} = {x_list}. "
                     f"Give the {fname}({var}) values in order."),
            steps=steps,
            final_answer=answer,
        )
