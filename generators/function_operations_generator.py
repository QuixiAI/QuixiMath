import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sub(n):
    """A substituted input is always parenthesized: 2(3) + 5, (-2)^2."""
    return f"({n})"


class FunctionOperationsGenerator(ProblemGenerator):
    """
    Function arithmetic evaluated at a point: (f + g)(k), (f - g)(k),
    (f · g)(k), (f/g)(k).

    The scratchpad unfolds the notation first - (f + g)(2) = f(2) + g(2) -
    then evaluates each function separately and combines. Quotients that
    do not divide evenly are written as a fraction and reduced.

    Op-codes used:
    - FUNC_SETUP: both definitions and the target (established)
    - FUNC_OP: unfold the operation notation (expression, meaning)
    - SUBST / E / M / A / S / D: the arithmetic (established meanings)
    - EVAL: record a finished evaluation (call, value)
    - REWRITE: form the quotient as a fraction (established, 1 field)
    - FRAC_REDUCE: reduce a numeric fraction to lowest terms (raw, reduced)
    - Z: final answer
    """

    VARIANTS = ["add", "subtract", "multiply", "divide"]
    OP_TXT = {"add": "+", "subtract": "-", "multiply": "·", "divide": "/"}

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _linear():
        a = random.choice([v for v in range(-5, 6) if v not in (-1, 0, 1)])
        b = random.choice([v for v in range(-9, 10) if v != 0])
        return a, b

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        op = self.OP_TXT[variant]
        n1, n2 = random.choice([("f", "g"), ("g", "h"), ("p", "q")])
        var = random.choice(["x", "x", "t"])

        f_quad = random.random() < 0.4
        if f_quad:
            c = random.choice([v for v in range(-9, 10) if v != 0])
            c_txt = f"+ {c}" if c > 0 else f"- {-c}"
            f_rule = f"{var}^2 {c_txt}"
        else:
            fa, fb = self._linear()
            fb_txt = f"+ {fb}" if fb > 0 else f"- {-fb}"
            f_rule = f"{fa}{var} {fb_txt}"

        ga, gb = self._linear()
        gb_txt = f"+ {gb}" if gb > 0 else f"- {-gb}"
        g_rule = f"{ga}{var} {gb_txt}"

        ks = [v for v in range(-6, 7) if v != 0]
        if variant == "divide":
            ks = [k for k in ks if ga * k + gb != 0]
        k = random.choice(ks)

        fv = (k * k + c) if f_quad else (fa * k + fb)
        gv = ga * k + gb

        target = f"({n1} {op} {n2})({k})" if op != "/" \
            else f"({n1}/{n2})({k})"
        unfold = f"{n1}({k}) {op} {n2}({k})" if op != "/" \
            else f"{n1}({k})/{n2}({k})"
        steps = [
            step("FUNC_SETUP",
                 f"{n1}({var}) = {f_rule}; {n2}({var}) = {g_rule}", target),
            step("FUNC_OP", target, unfold),
        ]

        if f_quad:
            steps.append(step("SUBST", var, k, f"{sub(k)}^2 {c_txt}"))
            steps.append(step("E", sub(k), 2, k * k))
            steps.append(step("A", k * k, c, fv))
        else:
            steps.append(step("SUBST", var, k, f"{fa}{sub(k)} {fb_txt}"))
            steps.append(step("M", fa, k, fa * k))
            steps.append(step("A", fa * k, fb, fv))
        steps.append(step("EVAL", f"{n1}({k})", fv))

        steps.append(step("SUBST", var, k, f"{ga}{sub(k)} {gb_txt}"))
        steps.append(step("M", ga, k, ga * k))
        steps.append(step("A", ga * k, gb, gv))
        steps.append(step("EVAL", f"{n2}({k})", gv))

        if variant == "add":
            value = fv + gv
            steps.append(step("A", fv, gv, value))
            answer = str(value)
        elif variant == "subtract":
            value = fv - gv
            steps.append(step("S", fv, gv, value))
            answer = str(value)
        elif variant == "multiply":
            value = fv * gv
            steps.append(step("M", fv, gv, value))
            answer = str(value)
        elif fv % gv == 0:
            value = fv // gv
            steps.append(step("D", fv, gv, value))
            answer = str(value)
        else:
            g = math.gcd(abs(fv), abs(gv))
            num, den = fv // g, gv // g
            if den < 0:
                num, den = -num, -den
            answer = f"{num}/{den}"
            steps.append(step("REWRITE", f"{fv}/{gv}"))
            if (num, den) != (fv, gv):
                steps.append(step("FRAC_REDUCE", f"{fv}/{gv}", answer))

        steps.append(step("Z", answer))
        problem = (f"Given {n1}({var}) = {f_rule} and {n2}({var}) = {g_rule}, "
                   f"find {target}.")
        return dict(
            problem_id=jid(),
            operation=f"function_op_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
