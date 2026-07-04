import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class NewtonRaphsonGenerator(ProblemGenerator):
    """
    Newton-Raphson tables for f(x)=x^2-n with exact rational iterates.

    This is the standard square-root Newton iteration:
        x_{k+1} = x_k - (x_k^2-n)/(2x_k).

    Op-codes used:
    - NEWTON_SETUP: function, derivative, starting value, iteration count
    - NEWTON_UPDATE: record the iterate transition
    - M / S / D (established/shared): f, f', correction, and update
    - Z: final iterate
    """

    VARIANTS = ["sqrt"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        n = self._pick_n()
        root_floor = math.isqrt(n)
        x_value = Fraction(random.choice([root_floor, root_floor + 1]), 1)
        start_x = x_value
        iterations = random.randint(2, 3)
        steps = [
            step("NEWTON_SETUP", f"f(x)=x^2-{n}", "f'(x)=2x",
                 f"x0={fraction_text(x_value)},iterations={iterations}"),
        ]
        for index in range(1, iterations + 1):
            x_sq = x_value * x_value
            f_value = x_sq - n
            derivative = 2 * x_value
            correction = f_value / derivative
            next_x = x_value - correction
            steps.extend([
                step("M", fraction_text(x_value), fraction_text(x_value),
                     fraction_text(x_sq)),
                step("S", fraction_text(x_sq), n, fraction_text(f_value)),
                step("M", 2, fraction_text(x_value),
                     fraction_text(derivative)),
                step("D", fraction_text(f_value), fraction_text(derivative),
                     fraction_text(correction)),
                step("S", fraction_text(x_value), fraction_text(correction),
                     fraction_text(next_x)),
                step("NEWTON_UPDATE", index, f"x_{index - 1}="
                     f"{fraction_text(x_value)}", f"x_{index}="
                     f"{fraction_text(next_x)}"),
            ])
            x_value = next_x
        answer = f"x_{iterations} = {fraction_text(x_value)}"
        steps.append(step("Z", answer))
        problem = (
            f"Use Newton-Raphson on f(x)=x^2-{n} with "
            f"x0={fraction_text(start_x)} for "
            f"{iterations} iterations. Give the final iterate."
        )
        return dict(
            problem_id=jid(),
            operation="newton_raphson_sqrt",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _pick_n(self):
        while True:
            n = random.randint(2, 60)
            root = math.isqrt(n)
            if root * root != n:
                return n
