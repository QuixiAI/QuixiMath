import random
from base_generator import ProblemGenerator
from helpers import step, jid


def lin(a, b, var):
    """Renders ax + b sign-aware, hiding unit coefficients."""
    head = {1: var, -1: f"-{var}"}.get(a, f"{a}{var}")
    if b == 0:
        return head
    return f"{head} + {b}" if b > 0 else f"{head} - {-b}"


class InverseFunctionGenerator(ProblemGenerator):
    """
    Finds an inverse function by the algebraic method: write y = f(x),
    swap x and y, solve for y. Every record ends with an A1-style
    composition check that f(f⁻¹(x)) collapses back to x.

    Variants:
    - linear:      f(x) = ax + b   -> f⁻¹(x) = (x - b)/a
    - divide_form: f(x) = (x + b)/c -> f⁻¹(x) = cx - b
    - cube:        f(x) = x^3 + c  -> f⁻¹(x) = ∛(x - c)

    Op-codes used:
    - FUNC_SETUP: the function and the goal (established)
    - REWRITE: y = f(x), and the final inverse statement (established)
    - SWAP_VARS: exchange x and y to invert (equation after the swap)
    - EQ_OP_BOTH: solve for y (established: op, value, new_left, new_right)
    - CBRT: take the cube root of both sides (established)
    - CHECK: compose f with the claimed inverse and collapse to x
      (established: method, work, expected)
    - Z: the inverse rule as a bare expression
    """

    VARIANTS = ["linear", "divide_form", "cube"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        fname = random.choice(["f", "g", "h"])
        var = "x"

        if variant == "linear":
            a = random.choice([v for v in range(-5, 6)
                               if v not in (-1, 0, 1)])
            b = random.choice([v for v in range(-9, 10) if v != 0])
            rule = lin(a, b, var)
            inner = lin(1, -b, var)            # x - b
            answer = f"({inner})/{a}" if a > 0 else f"({inner})/({a})"
            head = f"{a}y"
            steps = [
                step("FUNC_SETUP", f"{fname}({var}) = {rule}", "inverse"),
                step("REWRITE", f"y = {rule}"),
                step("SWAP_VARS", f"{var} = {lin(a, b, 'y')}"),
                step("EQ_OP_BOTH", "subtract" if b > 0 else "add", abs(b),
                     inner, head),
                step("EQ_OP_BOTH", "divide", a, answer, "y"),
                step("REWRITE", f"{fname}⁻¹({var}) = {answer}"),
                step("CHECK", "compose",
                     f"{fname}({fname}⁻¹({var})) = "
                     f"{a}({answer}) "
                     f"{'+' if b > 0 else '-'} {abs(b)} = "
                     f"{inner} {'+' if b > 0 else '-'} {abs(b)}", var),
                step("Z", answer),
            ]
        elif variant == "divide_form":
            c = random.randint(2, 5)
            b = random.choice([v for v in range(-9, 10) if v != 0])
            inner = lin(1, b, var)             # x + b
            rule = f"({inner})/{c}"
            answer = lin(c, -b, var)           # cx - b
            steps = [
                step("FUNC_SETUP", f"{fname}({var}) = {rule}", "inverse"),
                step("REWRITE", f"y = {rule}"),
                step("SWAP_VARS", f"{var} = ({lin(1, b, 'y')})/{c}"),
                step("EQ_OP_BOTH", "multiply", c, f"{c}{var}",
                     lin(1, b, "y")),
                step("EQ_OP_BOTH", "subtract" if b > 0 else "add", abs(b),
                     answer, "y"),
                step("REWRITE", f"{fname}⁻¹({var}) = {answer}"),
                step("CHECK", "compose",
                     f"{fname}({fname}⁻¹({var})) = "
                     f"(({answer}) {'+' if b > 0 else '-'} {abs(b)})/{c} = "
                     f"{c}{var}/{c}", var),
                step("Z", answer),
            ]
        else:
            c = random.choice([v for v in range(-9, 10) if v != 0])
            rule = f"{var}^3 {'+' if c > 0 else '-'} {abs(c)}"
            inner = lin(1, -c, var)            # x - c
            answer = f"∛({inner})"
            steps = [
                step("FUNC_SETUP", f"{fname}({var}) = {rule}", "inverse"),
                step("REWRITE", f"y = {rule}"),
                step("SWAP_VARS",
                     f"{var} = y^3 {'+' if c > 0 else '-'} {abs(c)}"),
                step("EQ_OP_BOTH", "subtract" if c > 0 else "add", abs(c),
                     inner, "y^3"),
                step("CBRT", "y^3", "y"),
                step("REWRITE", f"{fname}⁻¹({var}) = {answer}"),
                step("CHECK", "compose",
                     f"{fname}({fname}⁻¹({var})) = (∛({inner}))^3 "
                     f"{'+' if c > 0 else '-'} {abs(c)} = "
                     f"{inner} {'+' if c > 0 else '-'} {abs(c)}", var),
                step("Z", answer),
            ]

        return dict(
            problem_id=jid(),
            operation="inverse_function",
            problem=f"Find the inverse of {fname}({var}) = {rule}.",
            steps=steps,
            final_answer=answer,
        )
