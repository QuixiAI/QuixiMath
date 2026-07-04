import random

from base_generator import ProblemGenerator
from helpers import step, jid


def xor_bits(bits):
    result = 0
    for bit in bits:
        result ^= bit
    return result


def bits_text(bits):
    return "".join(str(bit) for bit in bits)


def xor_text(bits, result):
    return " xor ".join(str(bit) for bit in bits) + f"={result}"


def encode_data(data_bits):
    d1, d2, d3, d4 = data_bits
    p1 = xor_bits([d1, d2, d4])
    p2 = xor_bits([d1, d3, d4])
    p4 = xor_bits([d2, d3, d4])
    return [p1, p2, d1, p4, d2, d3, d4]


def syndrome_bits(word):
    s1 = xor_bits([word[0], word[2], word[4], word[6]])
    s2 = xor_bits([word[1], word[2], word[5], word[6]])
    s4 = xor_bits([word[3], word[4], word[5], word[6]])
    return s1, s2, s4


def syndrome_value(word):
    s1, s2, s4 = syndrome_bits(word)
    return s1 + 2 * s2 + 4 * s4


def flip_bit(word, position):
    corrected = list(word)
    if position:
        idx = position - 1
        corrected[idx] = 1 - corrected[idx]
    return corrected


def data_from_code(word):
    return [word[2], word[4], word[5], word[6]]


class HammingCodeGenerator(ProblemGenerator):
    """
    Hamming(7,4) encoding, syndrome computation, and single-error correction.

    Variants:
    - encode: place data bits and compute even parities.
    - syndrome: compute syndrome and error position from a received word.
    - correct: compute syndrome, correct one bit, and recover data bits.

    Op-codes used:
    - HAMMING_SETUP / HAMMING_PLACE / PARITY_CALC / CODEWORD
    - HAMMING_RECEIVED / SYNDROME_CALC / SYNDROME_VALUE / CORRECT_BIT
    - RECOVER_DATA / CHECK
    - Z: encoded word, syndrome, or corrected data
    """

    VARIANTS = ["encode", "syndrome", "correct"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        data_bits = [random.randint(0, 1) for _ in range(4)]
        codeword = encode_data(data_bits)
        if variant == "encode":
            problem, steps, answer = self._generate_encode(data_bits, codeword)
        else:
            error_position = random.randint(1, 7)
            received = flip_bit(codeword, error_position)
            if variant == "syndrome":
                problem, steps, answer = self._generate_syndrome(received)
            else:
                problem, steps, answer = self._generate_correct(received)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"hamming_code_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _encode_steps(self, data_bits, codeword):
        d1, d2, d3, d4 = data_bits
        p1, p2, _, p4, _, _, _ = codeword
        return [
            step("HAMMING_SETUP", f"data={bits_text(data_bits)}",
                 "even parity"),
            step("HAMMING_PLACE", "positions 1,2,3,4,5,6,7",
                 "p1,p2,d1,p4,d2,d3,d4"),
            step("PARITY_CALC", "p1=d1 xor d2 xor d4",
                 xor_text([d1, d2, d4], p1)),
            step("PARITY_CALC", "p2=d1 xor d3 xor d4",
                 xor_text([d1, d3, d4], p2)),
            step("PARITY_CALC", "p4=d2 xor d3 xor d4",
                 xor_text([d2, d3, d4], p4)),
            step("CODEWORD", bits_text(codeword)),
        ]

    def _generate_encode(self, data_bits, codeword):
        steps = self._encode_steps(data_bits, codeword)
        answer = f"code={bits_text(codeword)}"
        problem = (
            f"Encode data bits d={bits_text(data_bits)} using Hamming(7,4) "
            "with even parity."
        )
        return problem, steps, answer

    def _syndrome_steps(self, received):
        s1, s2, s4 = syndrome_bits(received)
        position = syndrome_value(received)
        return [
            step("HAMMING_RECEIVED", f"r={bits_text(received)}"),
            step("SYNDROME_CALC", "s1=b1 xor b3 xor b5 xor b7",
                 xor_text([received[0], received[2], received[4], received[6]], s1)),
            step("SYNDROME_CALC", "s2=b2 xor b3 xor b6 xor b7",
                 xor_text([received[1], received[2], received[5], received[6]], s2)),
            step("SYNDROME_CALC", "s4=b4 xor b5 xor b6 xor b7",
                 xor_text([received[3], received[4], received[5], received[6]], s4)),
            step("SYNDROME_VALUE", f"s1={s1}, s2={s2}, s4={s4}",
                 f"position={position}"),
        ]

    def _generate_syndrome(self, received):
        steps = self._syndrome_steps(received)
        position = syndrome_value(received)
        answer = f"syndrome={position}; error_position={position}"
        problem = (
            "A Hamming(7,4) even-parity word is received as "
            f"r={bits_text(received)}. Compute the syndrome and error "
            "position."
        )
        return problem, steps, answer

    def _generate_correct(self, received):
        steps = self._syndrome_steps(received)
        position = syndrome_value(received)
        corrected = flip_bit(received, position)
        if position:
            old = received[position - 1]
            new = corrected[position - 1]
            steps.append(step("CORRECT_BIT", f"position={position}",
                              f"{old}->{new}", f"corrected={bits_text(corrected)}"))
        else:
            steps.append(step("CORRECT_BIT", "position=0", "no change",
                              f"corrected={bits_text(corrected)}"))
        data_bits = data_from_code(corrected)
        steps.append(step("RECOVER_DATA", "positions 3,5,6,7",
                          bits_text(data_bits)))
        check = syndrome_value(corrected)
        steps.append(step("CHECK", f"syndrome(corrected)={check}",
                          "valid" if check == 0 else "invalid"))
        answer = (
            f"syndrome={position}; corrected={bits_text(corrected)}; "
            f"data={bits_text(data_bits)}"
        )
        problem = (
            "A Hamming(7,4) even-parity word is received as "
            f"r={bits_text(received)}. Compute the syndrome, correct the "
            "word, and recover data bits."
        )
        return problem, steps, answer
