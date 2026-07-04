import random

from base_generator import ProblemGenerator
from helpers import step, jid


DIGITS = "0123456789ABCDEF"


def to_base(n, base):
    if n == 0:
        return "0"
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    return "".join(reversed(out))


def from_base(text, base):
    total = 0
    for ch in text:
        total = total * base + DIGITS.index(ch)
    return total


class BaseConversionGenerator(ProblemGenerator):
    """
    Binary and hexadecimal conversions by place value and repeated division,
    plus 8-bit two's complement representation for negative integers.

    Variants:
    - binary_to_decimal
    - decimal_to_binary
    - hex_to_decimal
    - decimal_to_hex
    - twos_complement

    Op-codes used:
    - BASE_SETUP: conversion and target
    - PLACE_VALUE: one digit's base-power contribution
    - DIVMOD: quotient and remainder in repeated division
    - REVERSE: reverse collected remainders into the representation
    - TWOS_SETUP: width and offset for two's complement
    - A (established): running sum or offset addition
    - Z: converted representation
    """

    VARIANTS = ["binary_to_decimal", "decimal_to_binary",
                "hex_to_decimal", "decimal_to_hex", "twos_complement"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _place_steps(text, base):
        steps = []
        running = 0
        chars = list(reversed(text))
        for pos, ch in enumerate(chars):
            digit = DIGITS.index(ch)
            value = digit * (base ** pos)
            steps.append(step("PLACE_VALUE", f"{ch} * {base}^{pos}", value))
            if pos == 0:
                running = value
            else:
                steps.append(step("A", running, value, running + value))
                running += value
        return steps, running

    @staticmethod
    def _division_steps(n, base):
        steps = []
        remainders = []
        cur = n
        if cur == 0:
            steps.append(step("DIVMOD", 0, base, 0, "r=0"))
            remainders.append(0)
        while cur:
            q, r = divmod(cur, base)
            steps.append(step("DIVMOD", cur, base, q, f"r={r}"))
            remainders.append(r)
            cur = q
        digits = "".join(DIGITS[r] for r in reversed(remainders))
        steps.append(step("REVERSE", ",".join(DIGITS[r] for r in remainders),
                          digits))
        return steps, digits

    def _binary_to_decimal(self):
        n = random.randint(1, 255)
        text = to_base(n, 2)
        place_steps, answer = self._place_steps(text, 2)
        steps = [
            step("BASE_SETUP", f"{text}_2", "decimal"),
            *place_steps,
            step("Z", str(answer)),
        ]
        problem = f"Convert binary {text}_2 to decimal."
        return "binary_to_decimal", problem, steps, str(answer)

    def _decimal_to_binary(self):
        n = random.randint(1, 255)
        div_steps, answer = self._division_steps(n, 2)
        steps = [
            step("BASE_SETUP", f"{n}_10", "binary"),
            *div_steps,
            step("Z", answer),
        ]
        problem = f"Convert decimal {n} to binary."
        return "decimal_to_binary", problem, steps, answer

    def _hex_to_decimal(self):
        n = random.randint(16, 4095)
        text = to_base(n, 16)
        place_steps, answer = self._place_steps(text, 16)
        steps = [
            step("BASE_SETUP", f"{text}_16", "decimal"),
            *place_steps,
            step("Z", str(answer)),
        ]
        problem = f"Convert hexadecimal {text}_16 to decimal."
        return "hex_to_decimal", problem, steps, str(answer)

    def _decimal_to_hex(self):
        n = random.randint(16, 4095)
        div_steps, answer = self._division_steps(n, 16)
        steps = [
            step("BASE_SETUP", f"{n}_10", "hexadecimal"),
            *div_steps,
            step("Z", answer),
        ]
        problem = f"Convert decimal {n} to hexadecimal."
        return "decimal_to_hex", problem, steps, answer

    def _twos_complement(self):
        value = -random.randint(1, 128)
        encoded = 256 + value
        div_steps, bits = self._division_steps(encoded, 2)
        bits = bits.rjust(8, "0")
        if div_steps[-1].startswith("REVERSE"):
            parts = div_steps[-1].split("|")
            div_steps[-1] = step("REVERSE", parts[1], bits)
        steps = [
            step("TWOS_SETUP", "8-bit two's complement", "offset = 2^8 = 256"),
            step("A", 256, value, encoded),
            *div_steps,
            step("Z", bits),
        ]
        problem = f"Represent {value} in 8-bit two's complement."
        return "twos_complement", problem, steps, bits

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "binary_to_decimal":
            op_suffix, problem, steps, answer = self._binary_to_decimal()
        elif variant == "decimal_to_binary":
            op_suffix, problem, steps, answer = self._decimal_to_binary()
        elif variant == "hex_to_decimal":
            op_suffix, problem, steps, answer = self._hex_to_decimal()
        elif variant == "decimal_to_hex":
            op_suffix, problem, steps, answer = self._decimal_to_hex()
        else:
            op_suffix, problem, steps, answer = self._twos_complement()

        return dict(
            problem_id=jid(),
            operation=f"base_conversion_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
