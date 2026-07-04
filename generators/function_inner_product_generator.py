import random

from base_generator import ProblemGenerator
from helpers import step, jid


FAMILIES = ["sin", "cos"]


class FunctionInnerProductGenerator(ProblemGenerator):
    """
    Function-space inner products for the sin/cos family on [0, 2pi].

    Variants:
    - same_family: sin-sin or cos-cos, giving pi when frequencies match
      and 0 when they differ.
    - cross_family: sin-cos orthogonality, always 0.

    Op-codes used:
    - INNER_PRODUCT_SETUP / IDENTITY / INTEGRAL / CHECK
    - A / S / D (established/shared): coefficient arithmetic
    - Z: exact inner product
    """

    VARIANTS = ["same_family", "cross_family"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "same_family":
            problem, steps, answer = self._generate_same_family()
        else:
            problem, steps, answer = self._generate_cross_family()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"function_inner_product_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_same_family(self):
        family = random.choice(FAMILIES)
        m = random.randint(1, 50)
        if random.random() < 0.4:
            n = m
        else:
            n = random.choice([value for value in range(1, 51)
                               if value != m])
        f = f"{family}({m}x)"
        g = f"{family}({n}x)"
        steps = [
            step("INNER_PRODUCT_SETUP", "interval=[0,2pi]",
                 f"f={f}", f"g={g}"),
        ]
        if m == n:
            steps += [
                step("IDENTITY", f"{family}^2({m}x)",
                     f"average term integrates to 1/2"),
                step("INTEGRAL", "integral 1 dx on [0,2pi]", "2pi"),
                step("INTEGRAL", f"oscillating term for {family}^2", 0),
                step("D", 2, 2, 1),
                step("CHECK", "same frequency", "nonzero norm"),
            ]
            value = "pi"
        else:
            diff = abs(m - n)
            total = m + n
            sign = "-" if family == "sin" else "+"
            steps += [
                step("IDENTITY", f"{f}*{g}",
                     f"1/2(cos({diff}x) {sign} cos({total}x))"),
                step("INTEGRAL", f"integral cos({diff}x) on [0,2pi]", 0),
                step("INTEGRAL", f"integral cos({total}x) on [0,2pi]", 0),
            ]
            if family == "sin":
                steps.append(step("S", 0, 0, 0))
            else:
                steps.append(step("A", 0, 0, 0))
            steps += [
                step("D", 0, 2, 0),
                step("CHECK", "different frequencies", "orthogonal"),
            ]
            value = "0"
        answer = f"inner product = {value}"
        problem = (
            f"Compute the inner product of {f} and {g} on [0,2pi]."
        )
        return problem, steps, answer

    def _generate_cross_family(self):
        m = random.randint(1, 50)
        n = random.randint(1, 50)
        f = f"sin({m}x)"
        g = f"cos({n}x)"
        total = m + n
        diff = abs(m - n)
        steps = [
            step("INNER_PRODUCT_SETUP", "interval=[0,2pi]",
                 f"f={f}", f"g={g}"),
            step("IDENTITY", f"{f}*{g}",
                 f"1/2(sin({total}x) + sin({diff}x))"),
            step("INTEGRAL", f"integral sin({total}x) on [0,2pi]", 0),
            step("INTEGRAL", f"integral sin({diff}x) on [0,2pi]", 0),
            step("A", 0, 0, 0),
            step("D", 0, 2, 0),
            step("CHECK", "sin-cos family", "orthogonal"),
        ]
        answer = "inner product = 0"
        problem = (
            f"Compute the inner product of {f} and {g} on [0,2pi]."
        )
        return problem, steps, answer
