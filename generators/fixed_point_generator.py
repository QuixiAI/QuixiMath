import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def signed_fraction(value):
    fr = Fraction(value)
    if fr >= 0:
        return f"+{fraction_text(fr)}"
    return fraction_text(fr)


def linear_text(a_coeff, b_coeff):
    return f"{fraction_text(a_coeff)}*x{signed_fraction(b_coeff)}"


class FixedPointGenerator(ProblemGenerator):
    """
    Fixed-point iteration for affine contractions g(x)=a*x+b.

    Since g'(x)=a, the convergence check is the exact comparison abs(a)<1.

    Op-codes used:
    - FIXED_POINT_SETUP: g(x), starting value, and iteration count
    - DERIVATIVE: derivative of the affine map
    - ABS / COMPARE: contraction check
    - FIXED_POINT_UPDATE: record x_i -> x_{i+1}
    - M / A (established/shared): exact iteration arithmetic
    - Z: final iterate
    """

    VARIANTS = ["affine"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        a_coeff = self._random_contraction()
        b_coeff = Fraction(random.randint(-8, 8), random.randint(1, 6))
        if b_coeff == 0:
            b_coeff = Fraction(1, 1)
        x_value = Fraction(random.randint(-5, 5), random.randint(1, 4))
        start_x = x_value
        iterations = random.randint(3, 4)
        g_text = linear_text(a_coeff, b_coeff)
        abs_a = abs(a_coeff)
        steps = [
            step("FIXED_POINT_SETUP", f"g(x)={g_text}",
                 f"x0={fraction_text(x_value)}",
                 f"iterations={iterations}"),
            step("DERIVATIVE", "g'(x)", fraction_text(a_coeff)),
            step("ABS", fraction_text(a_coeff), fraction_text(abs_a)),
            step("COMPARE", fraction_text(abs_a), "< 1", "converges"),
        ]
        for index in range(1, iterations + 1):
            ax = a_coeff * x_value
            next_x = ax + b_coeff
            steps.extend([
                step("M", fraction_text(a_coeff), fraction_text(x_value),
                     fraction_text(ax)),
                step("A", fraction_text(ax), fraction_text(b_coeff),
                     fraction_text(next_x)),
                step("FIXED_POINT_UPDATE", index,
                     f"x_{index - 1}={fraction_text(x_value)}",
                     f"x_{index}={fraction_text(next_x)}"),
            ])
            x_value = next_x
        answer = f"x_{iterations} = {fraction_text(x_value)}"
        steps.append(step("Z", answer))
        problem = (
            f"Use fixed-point iteration x=g(x) with g(x)={g_text} from "
            f"x0={fraction_text(start_x)} for "
            f"{iterations} iterations. First check abs(g')<1."
        )
        return dict(
            problem_id=jid(),
            operation="fixed_point_affine",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _random_contraction(self):
        numerator = random.choice([n for n in range(-5, 6) if n != 0])
        denominator = random.randint(abs(numerator) + 1, abs(numerator) + 8)
        return Fraction(numerator, denominator)
