import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def random_exp_value():
    while True:
        numerator = random.randint(2, 36)
        denominator = random.randint(1, 24)
        if numerator > denominator and math.gcd(numerator, denominator) == 1:
            return Fraction(numerator, denominator)


class HyperbolicFunctionGenerator(ProblemGenerator):
    """
    Evaluate sinh, cosh, and tanh from supplied exact e^x and e^-x
    values, then verify cosh^2(x) - sinh^2(x) = 1.

    Op-codes used:
    - HYPERBOLIC_SETUP / FORMULA / CHECK
    - A / S / D / E (established/shared): exact fraction arithmetic
    - Z: all three hyperbolic function values
    """

    def generate(self) -> dict:
        exp_x = random_exp_value()
        exp_neg_x = Fraction(1, 1) / exp_x
        diff = exp_x - exp_neg_x
        sinh_x = diff / 2
        total = exp_x + exp_neg_x
        cosh_x = total / 2
        tanh_x = sinh_x / cosh_x
        cosh_sq = cosh_x ** 2
        sinh_sq = sinh_x ** 2
        identity = cosh_sq - sinh_sq
        steps = [
            step("HYPERBOLIC_SETUP", f"e^x={fraction_text(exp_x)}",
                 f"e^(-x)={fraction_text(exp_neg_x)}"),
            step("FORMULA", "sinh x = (e^x - e^(-x))/2"),
            step("S", fraction_text(exp_x), fraction_text(exp_neg_x),
                 fraction_text(diff)),
            step("D", fraction_text(diff), 2, fraction_text(sinh_x)),
            step("FORMULA", "cosh x = (e^x + e^(-x))/2"),
            step("A", fraction_text(exp_x), fraction_text(exp_neg_x),
                 fraction_text(total)),
            step("D", fraction_text(total), 2, fraction_text(cosh_x)),
            step("FORMULA", "tanh x = sinh x / cosh x"),
            step("D", fraction_text(sinh_x), fraction_text(cosh_x),
                 fraction_text(tanh_x)),
            step("E", fraction_text(cosh_x), 2, fraction_text(cosh_sq)),
            step("E", fraction_text(sinh_x), 2, fraction_text(sinh_sq)),
            step("S", fraction_text(cosh_sq), fraction_text(sinh_sq),
                 fraction_text(identity)),
            step("CHECK", "cosh^2 x - sinh^2 x", fraction_text(identity),
                 "identity holds"),
        ]
        answer = (
            f"sinh x = {fraction_text(sinh_x)}, "
            f"cosh x = {fraction_text(cosh_x)}, "
            f"tanh x = {fraction_text(tanh_x)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Given e^x = {fraction_text(exp_x)} and e^(-x) = "
            f"{fraction_text(exp_neg_x)}, compute sinh x, cosh x, "
            f"and tanh x."
        )
        return dict(
            problem_id=jid(),
            operation="hyperbolic_function_eval",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
