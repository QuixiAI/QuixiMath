import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


def digit_groups(n):
    text = str(n)
    if len(text) % 2:
        text = "0" + text
    return [int(text[i:i + 2]) for i in range(0, len(text), 2)]


class ManualSquareRootGenerator(ProblemGenerator):
    """
    By-hand square root procedures: the classic digit-by-digit paired-groups
    algorithm for perfect squares, and one divide-and-average iteration.

    Variants:
    - digit_by_digit: exact integer square root by paired groups
    - divide_average: next estimate = (x + N/x)/2

    Op-codes used:
    - SQRT_SETUP: radicand and grouping or estimate
    - BRING_DOWN: bring down the next two-digit group
    - SQRT_TRIAL: trial digit product and accept/reject cue
    - SQRT_DIGIT: append the accepted digit to the root
    - A / S / D / CHECK (established): arithmetic and verification
    - Z: exact square root or next estimate
    """

    VARIANTS = ["digit_by_digit", "divide_average"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _digit_by_digit(self):
        root_answer = random.randint(10, 999)
        n = root_answer * root_answer
        groups = digit_groups(n)
        steps = [
            step("SQRT_SETUP", f"N = {n}",
                 f"groups {', '.join(f'{g:02d}' for g in groups)}"),
        ]
        current = 0
        root = 0
        for idx, group in enumerate(groups):
            before = current
            current = current * 100 + group
            if idx == 0:
                steps.append(step("BRING_DOWN", f"group {group:02d}",
                                  f"current = {current}"))
            else:
                steps.append(step("BRING_DOWN",
                                  f"{before}*100 + {group:02d}",
                                  f"current = {current}"))
            base = 20 * root
            digit = 0
            product = 0
            for candidate in range(10):
                trial = (base + candidate) * candidate
                if trial <= current:
                    digit = candidate
                    product = trial
                else:
                    break
            steps.append(step("SQRT_TRIAL", f"x = {digit}",
                              f"({base} + {digit})*{digit} = {product}",
                              "fits"))
            if digit < 9:
                reject_product = (base + digit + 1) * (digit + 1)
                steps.append(step("SQRT_TRIAL", f"x = {digit + 1}",
                                  f"({base} + {digit + 1})*{digit + 1} = {reject_product}",
                                  "too large"))
            steps.append(step("S", current, product, current - product))
            current -= product
            root = root * 10 + digit
            steps.append(step("SQRT_DIGIT", digit, f"root = {root}"))
        steps.append(step("CHECK", f"{root}^2", root * root, n))
        steps.append(step("Z", str(root)))
        problem = f"Find sqrt({n}) using the digit-by-digit square root algorithm."
        return "digit_by_digit", problem, steps, str(root)

    def _divide_average(self):
        n = random.randint(20, 500)
        estimate = random.randint(2, 30)
        quotient = Fraction(n, estimate)
        total = Fraction(estimate) + quotient
        next_estimate = total / 2
        answer = exact(next_estimate)
        steps = [
            step("SQRT_SETUP", f"N = {n}", f"x0 = {estimate}"),
            step("D", n, estimate, exact(quotient)),
            step("A", estimate, exact(quotient), exact(total)),
            step("D", exact(total), 2, answer),
            step("CHECK", "divide-and-average",
                 "(x + N/x)/2", answer),
            step("Z", answer),
        ]
        problem = (
            f"Use one divide-and-average step to estimate sqrt({n}) "
            f"starting from x0 = {estimate}. What is the next estimate?"
        )
        return "divide_average", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "digit_by_digit":
            op_suffix, problem, steps, answer = self._digit_by_digit()
        else:
            op_suffix, problem, steps, answer = self._divide_average()

        return dict(
            problem_id=jid(),
            operation=f"manual_square_root_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
