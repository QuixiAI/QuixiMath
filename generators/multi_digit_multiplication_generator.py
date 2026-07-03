import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sig1(n):
    """Rounds a positive integer to one significant figure (half-up)."""
    k = 10 ** (len(str(n)) - 1)
    return ((n + k // 2) // k) * k


class MultiDigitMultiplicationGenerator(ProblemGenerator):
    """Generates standard column-form multi-digit integer multiplication.

    With estimate=True (see DESIGN.md "Derived Record Formats"), the steps
    open with an ESTIMATE (round each factor to one significant figure) and
    close with an ESTIMATE_CHECK comparing the exact product against it.
    """

    def __init__(self, estimate: bool = False):
        self.estimate = estimate
        if estimate:
            self.op_symbol = "estimate"

    def generate(self) -> dict:
        operation = ("multi_digit_multiplication_estimated" if self.estimate
                     else "multi_digit_multiplication")
        # Choose 2–5 digit numbers to keep partials manageable
        top = random.randint(10, 99999)
        bottom = random.randint(10, 99999)

        # Place the larger number on top for more familiar layout
        if bottom > top:
            top, bottom = bottom, top

        top_str = str(top)
        bottom_str = str(bottom)
        problem = f"{top_str} * {bottom_str}"

        steps = []
        steps.append(step("MUL_SETUP", top_str, bottom_str))

        est = None
        if self.estimate:
            r_top, r_bottom = sig1(top), sig1(bottom)
            est = r_top * r_bottom
            steps.append(step("ESTIMATE",
                              f"{top} × {bottom} ≈ {r_top} × {r_bottom}", est))

        partials = []
        for idx, digit_char in enumerate(reversed(bottom_str)):
            digit = int(digit_char)
            partial = digit * top
            shifted = partial * (10 ** idx)
            steps.append(step("MUL_PARTIAL", digit, top_str, str(shifted)))
            partials.append(shifted)

        total = sum(partials)
        partial_expr = " + ".join(str(p) for p in partials)
        steps.append(step("ADD_PARTIALS", partial_expr, str(total)))
        if self.estimate:
            steps.append(step("ESTIMATE_CHECK", est, total,
                              f"{total} ≈ {est} ✓"))
        steps.append(step("Z", str(total)))

        result = dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=str(total),
        )
        if self.estimate:
            result["grade_level"] = "middle"
            result["difficulty"] = 3
        return result
