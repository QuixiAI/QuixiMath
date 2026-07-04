import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kraft_inequality_generator import KraftInequalityGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Kraft's inequality for a binary prefix code with requested lengths "
    r"(.+)\. Decide whether the lengths are feasible; if feasible, give "
    r"canonical codewords\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_lengths(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    pairs = []
    for piece in match.group(1).split(", "):
        symbol, length = piece.split("=")
        pairs.append((symbol, int(length)))
    return pairs


def lengths_text(pairs):
    return ", ".join(f"{symbol}={length}" for symbol, length in pairs)


def kraft_sum(lengths):
    return sum((Fraction(1, 2 ** length) for length in lengths), Fraction(0))


def canonical_codes(pairs):
    ordered = sorted(pairs, key=lambda item: (item[1], item[0]))
    code = 0
    previous_length = 0
    codes = {}
    trace = []
    for symbol, length in ordered:
        shift = length - previous_length
        shifted = code << shift
        trace.append((symbol, length, code, shift, shifted))
        codes[symbol] = format(shifted, f"0{length}b")
        code = shifted + 1
        previous_length = length
    return ordered, codes, trace


def codes_text(symbols, codes):
    return ",".join(f"{symbol}:{codes[symbol]}" for symbol in symbols)


def expected_flow(example):
    pairs = parse_lengths(example["problem"])
    symbols = [symbol for symbol, _ in pairs]
    total = kraft_sum(length for _, length in pairs)
    steps = [
        make_step("KRAFT_SETUP", lengths_text(pairs), "binary prefix code"),
        make_step("KRAFT_FORMULA", "sum 2^-l_i <= 1"),
    ]
    running = Fraction(0)
    for symbol, length in pairs:
        denominator = 2 ** length
        term = Fraction(1, denominator)
        steps.append(make_step("E", 2, length, denominator))
        steps.append(make_step("D", 1, denominator, fraction_text(term)))
        steps.append(make_step("KRAFT_TERM", symbol, f"l={length}",
                               fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running

    if total <= 1:
        status = "feasible_complete" if total == 1 else "feasible_incomplete"
        slack = 1 - total
        steps.append(make_step("KRAFT_CHECK", f"sum={fraction_text(total)}",
                               "<=1", "feasible"))
        steps.append(make_step("S", 1, fraction_text(total),
                               fraction_text(slack)))
        steps.append(make_step("KRAFT_CLASSIFY",
                               f"slack={fraction_text(slack)}",
                               "complete" if slack == 0 else "incomplete"))
        ordered, codes, trace = canonical_codes(pairs)
        steps.append(make_step("CANONICAL_ORDER", lengths_text(ordered)))
        for symbol, length, code, shift, shifted in trace:
            steps.append(make_step("CANONICAL_SHIFT", f"code={code}",
                                   f"left={shift}", shifted))
            steps.append(make_step("CODEWORD", symbol, f"l={length}",
                                   codes[symbol]))
            steps.append(make_step("A", shifted, 1, shifted + 1))
        answer = (
            f"Kraft={fraction_text(total)}; status={status}; "
            f"slack={fraction_text(slack)}; "
            f"codes={codes_text(symbols, codes)}"
        )
    else:
        excess = total - 1
        steps.append(make_step("KRAFT_CHECK", f"sum={fraction_text(total)}",
                               ">1", "infeasible"))
        steps.append(make_step("S", fraction_text(total), 1,
                               fraction_text(excess)))
        steps.append(make_step("KRAFT_CLASSIFY",
                               f"excess={fraction_text(excess)}",
                               "no prefix code"))
        answer = (
            f"Kraft={fraction_text(total)}; status=infeasible; "
            f"excess={fraction_text(excess)}"
        )

    steps.append(make_step("Z", answer))
    return steps, answer


def parse_answer_codes(answer):
    marker = "; codes="
    if marker not in answer:
        return {}
    raw = answer.split(marker, 1)[1]
    codes = {}
    for piece in raw.split(","):
        symbol, code = piece.split(":")
        codes[symbol] = code
    return codes


def assert_prefix_free(testcase, codes):
    values = list(codes.values())
    for idx, left in enumerate(values):
        for jdx, right in enumerate(values):
            if idx == jdx:
                continue
            testcase.assertFalse(right.startswith(left), (left, right))


class TestKraftInequalityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = KraftInequalityGenerator()

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
        for variant in KraftInequalityGenerator.VARIANTS:
            result = KraftInequalityGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"kraft_inequality_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            KraftInequalityGenerator("bogus")

    def test_arithmetic_steps_and_prefix_codes(self):
        for _ in range(300):
            result = self.gen.generate()
            pairs = dict(parse_lengths(result["problem"]))
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "CANONICAL_SHIFT":
                    code = int(fields[1].split("=")[1])
                    shift = int(fields[2].split("=")[1])
                    self.assertEqual(code << shift, int(fields[3]),
                                     raw_step)
            codes = parse_answer_codes(result["final_answer"])
            if codes:
                self.assertEqual(set(codes), set(pairs))
                for symbol, code in codes.items():
                    self.assertEqual(len(code), pairs[symbol], symbol)
                assert_prefix_free(self, codes)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
