import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lz_compression_generator import LZCompressionGenerator
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def parse_problem(problem):
    method = "lz77" if "LZ77" in problem else "lz78"
    match = re.search(r"(?:string|input|text) ([a-z]+)", problem)
    assert match is not None, problem
    return method, match.group(1)


def lz77(text):
    tokens = []
    pos = 0
    while pos < len(text):
        best_offset = 0
        best_length = 0
        for start in range(pos):
            length = 0
            while (pos + length < len(text) and start + length < pos and
                   text[start + length] == text[pos + length]):
                length += 1
            offset = pos - start
            if length > best_length or (
                length == best_length and length > 0 and offset < best_offset
            ):
                best_offset = offset
                best_length = length
        next_char = text[pos + best_length] if pos + best_length < len(text) else "$"
        tokens.append((best_offset, best_length, next_char))
        pos += best_length + (0 if next_char == "$" else 1)
        if next_char == "$":
            break
    return "LZ77 = " + ", ".join(f"({a},{b},{c})" for a, b, c in tokens)


def lz78(text):
    dictionary = {}
    tokens = []
    pos = 0
    next_index = 1
    while pos < len(text):
        phrase = ""
        idx = 0
        end = pos
        while end < len(text) and phrase + text[end] in dictionary:
            phrase += text[end]
            idx = dictionary[phrase]
            end += 1
        next_char = text[end] if end < len(text) else "$"
        tokens.append((idx, next_char))
        if next_char != "$":
            dictionary[phrase + next_char] = next_index
            next_index += 1
            pos = end + 1
        else:
            break
    return "LZ78 = " + ", ".join(f"({a},{b})" for a, b in tokens)


def oracle(problem):
    method, text = parse_problem(problem)
    return lz77(text) if method == "lz77" else lz78(text)


class TestLZCompressionGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = LZCompressionGenerator()
        saw = set()
        openings = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 2)[0])
        self.assertEqual(saw, {f"lz_compression_{v}"
                               for v in LZCompressionGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            LZCompressionGenerator("bad")


if __name__ == "__main__":
    unittest.main()
