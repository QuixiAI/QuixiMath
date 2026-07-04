import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.crc_generator import CRCGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute the CRC remainder for data ([01]+) using generator polynomial "
    r"([01]+)\. Append (\d+) zeros before division\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_bits(text):
    return [int(ch) for ch in text]


def bits_text(bits):
    return "".join(str(bit) for bit in bits)


def xor_window(window, poly):
    return [a ^ b for a, b in zip(window, poly)]


def crc_divide(bits, poly_bits, emit_steps=False):
    work = list(bits)
    degree = len(poly_bits) - 1
    steps = []
    for idx in range(len(bits) - degree):
        if work[idx] == 0:
            if emit_steps:
                steps.append(make_step("CRC_SKIP", f"i={idx}",
                                       "leading bit 0"))
            continue
        before = work[idx:idx + len(poly_bits)]
        after = xor_window(before, poly_bits)
        work[idx:idx + len(poly_bits)] = after
        if emit_steps:
            steps.append(make_step("CRC_XOR", f"i={idx}",
                                   f"{bits_text(before)} xor {bits_text(poly_bits)}",
                                   bits_text(after)))
    return work[-degree:], steps


def expected_flow(example):
    data_raw, poly_raw, degree_raw = (
        PROBLEM_RE.fullmatch(example["problem"]).groups()
    )
    degree = int(degree_raw)
    data_bits = parse_bits(data_raw)
    poly_bits = parse_bits(poly_raw)
    augmented = data_bits + [0] * degree
    remainder, division_steps = crc_divide(
        augmented, poly_bits, emit_steps=True
    )
    codeword = data_bits + remainder
    check_remainder, _ = crc_divide(codeword, poly_bits, emit_steps=False)
    steps = [
        make_step("CRC_SETUP", f"data={bits_text(data_bits)}",
                  f"poly={poly_raw}", f"augmented={bits_text(augmented)}"),
    ]
    steps.extend(division_steps)
    steps.append(make_step("CRC_REMAINDER", bits_text(remainder)))
    steps.append(make_step("CRC_CHECK", f"codeword={bits_text(codeword)}",
                           f"remainder={bits_text(check_remainder)}",
                           "valid" if all(bit == 0 for bit in check_remainder)
                           else "invalid"))
    answer = f"remainder={bits_text(remainder)}; codeword={bits_text(codeword)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCRCGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CRCGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "crc_remainder")
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

    def test_xor_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CRC_XOR":
                    before_raw, poly_raw = fields[2].split(" xor ")
                    expected = bits_text(xor_window(parse_bits(before_raw),
                                                    parse_bits(poly_raw)))
                    self.assertEqual(fields[3], expected, raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
