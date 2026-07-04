import random

from base_generator import ProblemGenerator
from helpers import step, jid


POLYS = ["1011", "1101", "10011", "11001", "11101"]


def bits_text(bits):
    return "".join(str(bit) for bit in bits)


def parse_bits(text):
    return [int(ch) for ch in text]


def xor_window(window, poly):
    return [a ^ b for a, b in zip(window, poly)]


def crc_divide(bits, poly_bits, emit_steps=False):
    work = list(bits)
    degree = len(poly_bits) - 1
    steps = []
    for idx in range(len(bits) - degree):
        if work[idx] == 0:
            if emit_steps:
                steps.append(step("CRC_SKIP", f"i={idx}",
                                  "leading bit 0"))
            continue
        before = work[idx:idx + len(poly_bits)]
        after = xor_window(before, poly_bits)
        work[idx:idx + len(poly_bits)] = after
        if emit_steps:
            steps.append(step("CRC_XOR", f"i={idx}",
                              f"{bits_text(before)} xor {bits_text(poly_bits)}",
                              bits_text(after)))
    return work[-degree:], steps


class CRCGenerator(ProblemGenerator):
    """
    CRC remainder computation by polynomial long division over GF(2).

    Op-codes used:
    - CRC_SETUP / CRC_XOR / CRC_SKIP / CRC_REMAINDER / CRC_CHECK
    - Z: remainder and transmitted codeword
    """

    def generate(self) -> dict:
        poly = random.choice(POLYS)
        degree = len(poly) - 1
        data_len = random.randint(4, 9)
        data_bits = [1] + [random.randint(0, 1) for _ in range(data_len - 1)]
        poly_bits = parse_bits(poly)
        augmented = data_bits + [0] * degree
        remainder, division_steps = crc_divide(
            augmented, poly_bits, emit_steps=True
        )
        codeword = data_bits + remainder
        check_remainder, _ = crc_divide(codeword, poly_bits, emit_steps=False)
        steps = [
            step("CRC_SETUP", f"data={bits_text(data_bits)}",
                 f"poly={poly}", f"augmented={bits_text(augmented)}"),
        ]
        steps.extend(division_steps)
        steps.append(step("CRC_REMAINDER", bits_text(remainder)))
        steps.append(step("CRC_CHECK", f"codeword={bits_text(codeword)}",
                          f"remainder={bits_text(check_remainder)}",
                          "valid" if all(bit == 0 for bit in check_remainder)
                          else "invalid"))
        answer = (
            f"remainder={bits_text(remainder)}; "
            f"codeword={bits_text(codeword)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Compute the CRC remainder for data {bits_text(data_bits)} using "
            f"generator polynomial {poly}. Append {degree} zeros before "
            "division."
        )
        return dict(
            problem_id=jid(),
            operation="crc_remainder",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
