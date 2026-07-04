import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hamming_code_generator import HammingCodeGenerator
from helpers import DELIM


ENCODE_RE = re.compile(
    r"Encode data bits d=([01]{4}) using Hamming\(7,4\) with even parity\."
)
SYNDROME_RE = re.compile(
    r"A Hamming\(7,4\) even-parity word is received as r=([01]{7})\. "
    r"Compute the syndrome and error position\."
)
CORRECT_RE = re.compile(
    r"A Hamming\(7,4\) even-parity word is received as r=([01]{7})\. "
    r"Compute the syndrome, correct the word, and recover data bits\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def bits(raw):
    return [int(ch) for ch in raw]


def bits_text(values):
    return "".join(str(bit) for bit in values)


def xor_bits(values):
    out = 0
    for value in values:
        out ^= value
    return out


def xor_text(values, result):
    return " xor ".join(str(bit) for bit in values) + f"={result}"


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
        corrected[position - 1] = 1 - corrected[position - 1]
    return corrected


def data_from_code(word):
    return [word[2], word[4], word[5], word[6]]


def encode_steps(data_bits, codeword):
    d1, d2, d3, d4 = data_bits
    p1, p2, _, p4, _, _, _ = codeword
    return [
        make_step("HAMMING_SETUP", f"data={bits_text(data_bits)}",
                  "even parity"),
        make_step("HAMMING_PLACE", "positions 1,2,3,4,5,6,7",
                  "p1,p2,d1,p4,d2,d3,d4"),
        make_step("PARITY_CALC", "p1=d1 xor d2 xor d4",
                  xor_text([d1, d2, d4], p1)),
        make_step("PARITY_CALC", "p2=d1 xor d3 xor d4",
                  xor_text([d1, d3, d4], p2)),
        make_step("PARITY_CALC", "p4=d2 xor d3 xor d4",
                  xor_text([d2, d3, d4], p4)),
        make_step("CODEWORD", bits_text(codeword)),
    ]


def syndrome_steps(received):
    s1, s2, s4 = syndrome_bits(received)
    position = syndrome_value(received)
    return [
        make_step("HAMMING_RECEIVED", f"r={bits_text(received)}"),
        make_step("SYNDROME_CALC", "s1=b1 xor b3 xor b5 xor b7",
                  xor_text([received[0], received[2], received[4], received[6]], s1)),
        make_step("SYNDROME_CALC", "s2=b2 xor b3 xor b6 xor b7",
                  xor_text([received[1], received[2], received[5], received[6]], s2)),
        make_step("SYNDROME_CALC", "s4=b4 xor b5 xor b6 xor b7",
                  xor_text([received[3], received[4], received[5], received[6]], s4)),
        make_step("SYNDROME_VALUE", f"s1={s1}, s2={s2}, s4={s4}",
                  f"position={position}"),
    ]


def expected_flow(example):
    problem = example["problem"]
    if ENCODE_RE.fullmatch(problem):
        data_bits = bits(ENCODE_RE.fullmatch(problem).group(1))
        codeword = encode_data(data_bits)
        steps = encode_steps(data_bits, codeword)
        answer = f"code={bits_text(codeword)}"
    elif SYNDROME_RE.fullmatch(problem):
        received = bits(SYNDROME_RE.fullmatch(problem).group(1))
        steps = syndrome_steps(received)
        position = syndrome_value(received)
        answer = f"syndrome={position}; error_position={position}"
    elif CORRECT_RE.fullmatch(problem):
        received = bits(CORRECT_RE.fullmatch(problem).group(1))
        steps = syndrome_steps(received)
        position = syndrome_value(received)
        corrected = flip_bit(received, position)
        if position:
            old = received[position - 1]
            new = corrected[position - 1]
            steps.append(make_step("CORRECT_BIT", f"position={position}",
                                   f"{old}->{new}",
                                   f"corrected={bits_text(corrected)}"))
        else:
            steps.append(make_step("CORRECT_BIT", "position=0", "no change",
                                   f"corrected={bits_text(corrected)}"))
        data_bits = data_from_code(corrected)
        steps.append(make_step("RECOVER_DATA", "positions 3,5,6,7",
                               bits_text(data_bits)))
        check = syndrome_value(corrected)
        steps.append(make_step("CHECK", f"syndrome(corrected)={check}",
                               "valid" if check == 0 else "invalid"))
        answer = (
            f"syndrome={position}; corrected={bits_text(corrected)}; "
            f"data={bits_text(data_bits)}"
        )
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestHammingCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = HammingCodeGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_variants_are_available(self):
        for variant in HammingCodeGenerator.VARIANTS:
            result = HammingCodeGenerator(variant).generate()
            self.assertEqual(result["operation"], f"hamming_code_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HammingCodeGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
