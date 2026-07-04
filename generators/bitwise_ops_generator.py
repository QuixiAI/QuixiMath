import random

from base_generator import ProblemGenerator
from helpers import step, jid


OPS = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


def bits(n, width=4):
    return format(n, f"0{width}b")


class BitwiseOpsGenerator(ProblemGenerator):
    """
    Bitwise AND, OR, and XOR as truth tables and 4-bit masking operations.
    Masking traces compute each bit independently, then reassemble the result.

    Variants:
    - truth_table: complete the two-input truth table for AND, OR, or XOR
    - mask:        apply a 4-bit mask with AND, OR, or XOR

    Op-codes used:
    - BIT_SETUP: operation and target
    - BIT_RULE: operation meaning
    - BIT_ROW: one truth-table or mask bit row
    - REVERSE (established): reassemble low-to-high result bits
    - CHECK (established): decimal cross-check
    - Z: final truth table or masked value
    """

    VARIANTS = ["truth_table", "mask"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _rule(op):
        return {
            "AND": "1 only when both bits are 1",
            "OR": "1 when at least one bit is 1",
            "XOR": "1 when exactly one bit is 1",
        }[op]

    def _truth_table(self):
        op = random.choice(list(OPS))
        rows = [(0, 0), (0, 1), (1, 0), (1, 1)]
        outputs = []
        steps = [
            step("BIT_SETUP", f"truth table for {op}", "all 2-bit inputs"),
            step("BIT_RULE", op, self._rule(op)),
        ]
        for a, b in rows:
            out = OPS[op](a, b)
            outputs.append(f"{a}{b}->{out}")
            steps.append(step("BIT_ROW", f"{a} {op} {b}", out))
        answer = ", ".join(outputs)
        steps.append(step("Z", answer))
        problem = f"Complete the truth table for bitwise {op}."
        return "truth_table", problem, steps, answer

    def _mask(self):
        op = random.choice(list(OPS))
        value = random.randint(0, 15)
        mask = random.randint(0, 15)
        result = OPS[op](value, mask)
        value_bits = bits(value)
        mask_bits = bits(mask)
        low_result_bits = []
        steps = [
            step("BIT_SETUP", f"{value_bits} {op} {mask_bits}", "4-bit mask"),
            step("BIT_RULE", op, self._rule(op)),
        ]
        for pos, (a_ch, b_ch) in enumerate(zip(reversed(value_bits),
                                               reversed(mask_bits))):
            out = OPS[op](int(a_ch), int(b_ch))
            low_result_bits.append(str(out))
            steps.append(step("BIT_ROW", f"bit {pos}",
                              f"{a_ch} {op} {b_ch}", out))
        result_bits = bits(result)
        steps.append(step("REVERSE", ",".join(low_result_bits), result_bits))
        steps.append(step("CHECK", f"{value} {op} {mask}", result,
                          result_bits))
        answer = f"{result_bits}_2 = {result}"
        steps.append(step("Z", answer))
        problem = (
            f"Apply bitwise {op} to 4-bit value {value_bits}_2 with mask "
            f"{mask_bits}_2. Give the binary and decimal result."
        )
        return "mask", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "truth_table":
            op_suffix, problem, steps, answer = self._truth_table()
        else:
            op_suffix, problem, steps, answer = self._mask()

        return dict(
            problem_id=jid(),
            operation=f"bitwise_ops_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
