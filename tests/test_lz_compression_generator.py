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

TEXT_RE = re.compile(r"\"([a-z]+)\"")
LZ77_TOKEN_RE = re.compile(r"\((\d+),(\d+),([a-z]|\$)\)")
LZ78_TOKEN_RE = re.compile(r"\((\d+),([a-z]|\$)\)")


def parse_problem(problem):
    """Return (kind, payload) parsed from the problem text alone."""
    if "Each token is" in problem:
        if "LZ77" in problem:
            return "lz77_decode", [
                (int(a), int(b), c)
                for a, b, c in LZ77_TOKEN_RE.findall(problem)
            ]
        return "lz78_decode", [
            (int(a), b) for a, b in LZ78_TOKEN_RE.findall(problem)
        ]
    match = TEXT_RE.search(problem)
    assert match is not None, problem
    kind = "lz77" if "LZ77" in problem else "lz78"
    return kind, match.group(1)


def lz77_independent(text):
    """LZ77 by explicit substring search (not the generator's incremental
    character loop): longest non-overlapping match, largest start on ties."""
    tokens = []
    pos = 0
    while pos < len(text):
        best_len = 0
        best_start = None
        for length in range(min(len(text) - pos, pos), 0, -1):
            cands = [s for s in range(pos - length + 1)
                     if text[s:s + length] == text[pos:pos + length]]
            if cands:
                best_len = length
                best_start = max(cands)
                break
        offset = pos - best_start if best_len else 0
        next_char = (text[pos + best_len] if pos + best_len < len(text)
                     else "$")
        tokens.append((offset, best_len, next_char))
        pos += best_len + (0 if next_char == "$" else 1)
        if next_char == "$":
            break
    return tokens


def lz78_independent(text):
    """LZ78 by longest-dictionary-prefix slicing rather than the generator's
    incremental extension loop."""
    phrases = {}
    tokens = []
    pos = 0
    while pos < len(text):
        best_phrase = ""
        for length in range(len(text) - pos, 0, -1):
            cand = text[pos:pos + length]
            if cand in phrases:
                best_phrase = cand
                break
        idx = phrases.get(best_phrase, 0)
        end = pos + len(best_phrase)
        next_char = text[end] if end < len(text) else "$"
        tokens.append((idx, next_char))
        if next_char == "$":
            break
        phrases[best_phrase + next_char] = len(phrases) + 1
        pos = end + 1
    return tokens


def decode77(tokens):
    out = ""
    for offset, length, ch in tokens:
        if length:
            start = len(out) - offset
            out += out[start:start + length]
        if ch != "$":
            out += ch
    return out


def decode78(tokens):
    phrases = {0: ""}
    out = ""
    for idx, ch in tokens:
        phrase = phrases[idx] + ("" if ch == "$" else ch)
        out += phrase
        if ch != "$":
            phrases[len(phrases)] = phrase
    return out


def oracle(problem):
    kind, payload = parse_problem(problem)
    if kind == "lz77":
        tokens = lz77_independent(payload)
        assert decode77(tokens) == payload, problem
        return "LZ77 = " + ", ".join(f"({a},{b},{c})" for a, b, c in tokens)
    if kind == "lz78":
        tokens = lz78_independent(payload)
        assert decode78(tokens) == payload, problem
        return "LZ78 = " + ", ".join(f"({a},{b})" for a, b in tokens)
    if kind == "lz77_decode":
        text = decode77(payload)
        assert lz77_independent(text) == payload, problem
        return f"text = {text}"
    text = decode78(payload)
    assert lz78_independent(text) == payload, problem
    return f"text = {text}"


def check_steps(case, result):
    steps = result["steps"]
    fields = [s.split("|") for s in steps]
    kind, payload = parse_problem(result["problem"])
    case.assertEqual(fields[0][0], "LZ_SETUP")
    if kind in ("lz77", "lz78"):
        case.assertEqual(fields[0][2], payload)
        emit = "LZ77_EMIT" if kind == "lz77" else "LZ78_EMIT"
        emitted = [f[1] for f in fields if f[0] == emit]
        case.assertEqual(", ".join(emitted),
                         result["final_answer"].split(" = ", 1)[1])
    if kind == "lz77":
        text = payload
        # Every LZ77_SEARCH length is the true match length at that start.
        for f in fields:
            if f[0] != "LZ77_SEARCH":
                continue
            pos = int(f[1].split()[1])
            start = int(f[2].split()[1])
            length = int(f[3].split()[1])
            expect = 0
            while (pos + expect < len(text) and start + expect < pos and
                   text[start + expect] == text[pos + expect]):
                expect += 1
            case.assertEqual(length, expect, f)
    if kind == "lz78":
        indices = [int(f[1]) for f in fields if f[0] == "LZ78_DICT"]
        case.assertEqual(indices, list(range(len(indices))))
    if kind in ("lz77_decode", "lz78_decode"):
        final = result["final_answer"].split(" = ", 1)[1]
        outs = [f[-1].split("out = ")[1] for f in fields
                if f[0] in ("LZ77_EXPAND", "LZ78_APPEND")]
        case.assertTrue(outs)
        case.assertEqual(outs[-1], final)
        for earlier, later in zip(outs, outs[1:]):
            case.assertTrue(later.startswith(earlier), (earlier, later))
        for out in outs:
            case.assertTrue(final.startswith(out), (out, final))
    for f in fields:
        if f[0] == "CHECK":
            case.assertEqual(f[2].split(" = ", 1)[1], f[3].split(" = ", 1)[1],
                             f)


class TestLZCompressionGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = LZCompressionGenerator()
        saw = set()
        openings = set()
        problems = set()
        payloads = set()
        for _ in range(400):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]),
                             result["problem"])
            check_steps(self, result)
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 2)[0])
            problems.add(result["problem"])
            payloads.add(str(parse_problem(result["problem"])[1]))
        self.assertEqual(saw, {f"lz_compression_{v}"
                               for v in LZCompressionGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 4)
        self.assertGreaterEqual(len(problems), 380)
        self.assertGreaterEqual(len(payloads), 350)

    def test_each_variant_fixed(self):
        random.seed(7)
        for variant in LZCompressionGenerator.VARIANTS:
            gen = LZCompressionGenerator(variant)
            for _ in range(60):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"lz_compression_{variant}")
                self.assertEqual(result["final_answer"],
                                 oracle(result["problem"]), result["problem"])
                check_steps(self, result)

    def test_round_trip_property(self):
        random.seed(11)
        gen = LZCompressionGenerator("lz78")
        for _ in range(50):
            result = gen.generate()
            _, text = parse_problem(result["problem"])
            tokens = [(int(a), b) for a, b in
                      LZ78_TOKEN_RE.findall(result["final_answer"])]
            self.assertEqual(decode78(tokens), text)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            LZCompressionGenerator("bad")


if __name__ == "__main__":
    unittest.main()
