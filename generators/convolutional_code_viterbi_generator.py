import random

from base_generator import ProblemGenerator
from helpers import step, jid


MESSAGES = ["101", "110", "011", "100"]


def bits_text(bits):
    return "".join(str(bit) for bit in bits)


def encode_bits(bits):
    state = 0
    encoded = []
    for bit in bits:
        encoded.extend([bit ^ state, bit])
        state = bit
    return encoded


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def all_messages(length):
    return [[int(ch) for ch in format(i, f"0{length}b")]
            for i in range(2 ** length)]


class ConvolutionalCodeViterbiGenerator(ProblemGenerator):
    """
    Encode and decode a tiny rate-1/2 convolutional code by Viterbi search.

    The code has one memory bit: output is (u xor previous, u), initial
    previous bit 0.

    Op-codes used:
    - CONV_SETUP / CONV_ENCODE_STEP / VITERBI_CAND / VITERBI_PICK
    - CHECK
    - Z: encoded bits, decoded bits, and Hamming distance
    """

    def generate(self) -> dict:
        message = [int(ch) for ch in random.choice(MESSAGES)]
        encoded = encode_bits(message)
        received = encoded[:]
        flip_pos = random.randrange(len(received))
        received[flip_pos] ^= 1
        steps = [
            step("CONV_SETUP", "output=(u xor prev,u)",
                 f"message={bits_text(message)}", "prev0=0"),
        ]
        prev = 0
        for idx, bit in enumerate(message, start=1):
            pair = [bit ^ prev, bit]
            steps.append(step("CONV_ENCODE_STEP", f"i={idx}",
                              f"prev={prev},u={bit}", bits_text(pair)))
            prev = bit
        steps.append(step("CONV_RECEIVED", bits_text(received),
                          f"flipped position {flip_pos + 1}"))

        best = None
        for candidate in all_messages(len(message)):
            cand_code = encode_bits(candidate)
            dist = hamming(cand_code, received)
            steps.append(step("VITERBI_CAND", bits_text(candidate),
                              bits_text(cand_code), f"distance={dist}"))
            key = (dist, bits_text(candidate))
            if best is None or key < best[0]:
                best = (key, candidate, cand_code, dist)
                steps.append(step("VITERBI_PICK", bits_text(candidate),
                                  f"distance={dist}"))
        _, decoded, _, distance = best
        steps.append(step("CHECK", bits_text(decoded), bits_text(message),
                          "matches original" if decoded == message else "differs"))
        answer = (
            f"encoded={bits_text(encoded)}; decoded={bits_text(decoded)}; "
            f"distance={distance}"
        )
        problem = (
            "Use the rate-1/2 convolutional code output=(u xor previous,u) "
            f"with initial previous bit 0. Encode message {bits_text(message)}. "
            f"Then Viterbi-decode received bits {bits_text(received)} by "
            "minimum Hamming distance, breaking ties lexicographically."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="convolutional_code_viterbi",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
