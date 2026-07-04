import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def sign_text(value):
    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def interval_text(left, right):
    return f"[{fraction_text(left)}, {fraction_text(right)}]"


class BisectionGenerator(ProblemGenerator):
    """
    Bisection tables for f(x)=x^2-n with exact rational midpoints.

    The final answer is the bracket after a fixed number of iterations.

    Op-codes used:
    - BISECTION_SETUP: function, starting interval, and iteration count
    - SIGN: sign of an evaluated function value or product
    - BISECT_UPDATE: interval chosen from the sign product
    - A / D / M / S (established/shared): midpoint and f(x) arithmetic
    - Z: final bracket
    """

    def generate(self) -> dict:
        n = self._pick_n()
        left = Fraction(math.isqrt(n), 1)
        right = left + 1
        iterations = random.randint(3, 5)
        steps = [
            step("BISECTION_SETUP", f"f(x)=x^2-{n}",
                 f"interval={interval_text(left, right)}",
                 f"iterations={iterations}"),
        ]
        f_left = self._eval_steps(steps, "left", left, n)
        self._eval_steps(steps, "right", right, n)
        for index in range(1, iterations + 1):
            total = left + right
            mid = total / 2
            steps.append(step("A", fraction_text(left), fraction_text(right),
                              fraction_text(total)))
            steps.append(step("D", fraction_text(total), 2,
                              fraction_text(mid)))
            f_mid = self._eval_steps(steps, f"mid{index}", mid, n)
            product = f_left * f_mid
            steps.append(step("M", fraction_text(f_left),
                              fraction_text(f_mid), fraction_text(product)))
            steps.append(step("SIGN", f"product_{index}",
                              fraction_text(product), sign_text(product)))
            if product < 0:
                right = mid
                update = interval_text(left, right)
                relation = "product < 0"
            else:
                left = mid
                f_left = f_mid
                update = interval_text(left, right)
                relation = "product > 0"
            steps.append(step("BISECT_UPDATE", index, relation, update))
        answer = f"root in {interval_text(left, right)}"
        steps.append(step("Z", answer))
        problem = (
            f"Use bisection for f(x)=x^2-{n} on "
            f"{interval_text(Fraction(math.isqrt(n), 1), Fraction(math.isqrt(n) + 1, 1))} "
            f"for {iterations} iterations. Give the final bracket."
        )
        return dict(
            problem_id=jid(),
            operation="bisection_interval",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _pick_n(self):
        while True:
            n = random.randint(2, 200)
            root = math.isqrt(n)
            if root * root != n:
                return n

    def _eval_steps(self, steps, label, x_value, n):
        square = x_value * x_value
        value = square - n
        steps.append(step("M", fraction_text(x_value), fraction_text(x_value),
                          fraction_text(square)))
        steps.append(step("S", fraction_text(square), n,
                          fraction_text(value)))
        steps.append(step("SIGN", label, fraction_text(value),
                          sign_text(value)))
        return value
