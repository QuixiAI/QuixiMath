import random

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.base_conversion_generator import DIGITS, to_base, from_base


def digit_value(ch):
    return DIGITS.index(ch)


class BaseArithmeticGenerator(ProblemGenerator):
    """
    Column arithmetic in base 2, 8, and 16. Addition works right-to-left with
    in-base carries; multiplication uses a one-digit multiplier and carries
    through each column.

    Variants:
    - addition:       add two base-b numerals
    - multiplication: multiply a base-b numeral by one base-b digit

    Op-codes used:
    - BASE_ARITH_SETUP: operation and base
    - BASE_ADD_COL: one addition column with carry-in and carry-out
    - BASE_MUL_COL: one multiplication column with carry-in and carry-out
    - BASE_CARRY: remaining carry emitted as a digit
    - REVERSE (established): reverse collected result digits
    - CHECK (established): decimal cross-check
    - Z: result in the requested base
    """

    VARIANTS = ["addition", "multiplication"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _add_digits(a_text, b_text, base):
        width = max(len(a_text), len(b_text))
        a_rev = a_text.rjust(width, "0")[::-1]
        b_rev = b_text.rjust(width, "0")[::-1]
        carry = 0
        out = []
        steps = []
        for pos, (a_ch, b_ch) in enumerate(zip(a_rev, b_rev)):
            total = digit_value(a_ch) + digit_value(b_ch) + carry
            digit = total % base
            new_carry = total // base
            out.append(DIGITS[digit])
            steps.append(step("BASE_ADD_COL", f"col {pos}",
                              f"{a_ch} + {b_ch} + carry {carry}",
                              f"{total} -> digit {DIGITS[digit]}, carry {new_carry}"))
            carry = new_carry
        while carry:
            digit = carry % base
            new_carry = carry // base
            out.append(DIGITS[digit])
            steps.append(step("BASE_CARRY", f"carry {carry}",
                              f"digit {DIGITS[digit]}, carry {new_carry}"))
            carry = new_carry
        answer = "".join(reversed(out))
        steps.append(step("REVERSE", ",".join(out), answer))
        return steps, answer

    @staticmethod
    def _multiply_digit(a_text, multiplier_text, base):
        multiplier = digit_value(multiplier_text)
        carry = 0
        out = []
        steps = []
        for pos, a_ch in enumerate(reversed(a_text)):
            total = digit_value(a_ch) * multiplier + carry
            digit = total % base
            new_carry = total // base
            out.append(DIGITS[digit])
            steps.append(step("BASE_MUL_COL", f"col {pos}",
                              f"{a_ch} * {multiplier_text} + carry {carry}",
                              f"{total} -> digit {DIGITS[digit]}, carry {new_carry}"))
            carry = new_carry
        while carry:
            digit = carry % base
            new_carry = carry // base
            out.append(DIGITS[digit])
            steps.append(step("BASE_CARRY", f"carry {carry}",
                              f"digit {DIGITS[digit]}, carry {new_carry}"))
            carry = new_carry
        answer = "".join(reversed(out))
        steps.append(step("REVERSE", ",".join(out), answer))
        return steps, answer

    def _addition(self):
        base = random.choice([2, 8, 16])
        hi = {2: 255, 8: 2047, 16: 4095}[base]
        a = random.randint(1, hi)
        b = random.randint(1, hi)
        a_text = to_base(a, base)
        b_text = to_base(b, base)
        col_steps, result_text = self._add_digits(a_text, b_text, base)
        answer = f"{result_text}_{base}"
        steps = [
            step("BASE_ARITH_SETUP", f"base {base}", f"{a_text} + {b_text}"),
            *col_steps,
            step("CHECK", f"{a} + {b}", a + b, result_text),
            step("Z", answer),
        ]
        problem = f"In base {base}, add {a_text}_{base} + {b_text}_{base}."
        return "addition", problem, steps, answer

    def _multiplication(self):
        base = random.choice([8, 16])
        hi = {8: 511, 16: 4095}[base]
        a = random.randint(2, hi)
        multiplier = random.randint(2, base - 1)
        a_text = to_base(a, base)
        multiplier_text = DIGITS[multiplier]
        col_steps, result_text = self._multiply_digit(a_text, multiplier_text, base)
        answer = f"{result_text}_{base}"
        steps = [
            step("BASE_ARITH_SETUP", f"base {base}",
                 f"{a_text} * {multiplier_text}"),
            *col_steps,
            step("CHECK", f"{a} * {multiplier}", a * multiplier, result_text),
            step("Z", answer),
        ]
        problem = (
            f"In base {base}, multiply {a_text}_{base} by "
            f"{multiplier_text}_{base}."
        )
        return "multiplication", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "addition":
            op_suffix, problem, steps, answer = self._addition()
        else:
            op_suffix, problem, steps, answer = self._multiplication()

        return dict(
            problem_id=jid(),
            operation=f"base_arithmetic_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
