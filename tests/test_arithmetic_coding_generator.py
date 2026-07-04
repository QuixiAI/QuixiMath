import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.arithmetic_coding_generator import ArithmeticCodingGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Arithmetic-code message ([A-D]+) using symbol probabilities (.+)\. "
    r"Find the final interval and midpoint code\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def distribution_text(symbols, probabilities):
    return ", ".join(
        f"{symbol}={fraction_text(probability)}"
        for symbol, probability in zip(symbols, probabilities)
    )


def interval_text(low, high):
    return f"[{fraction_text(low)},{fraction_text(high)})"


def parse_problem(problem):
    message, raw_distribution = PROBLEM_RE.fullmatch(problem).groups()
    symbols = []
    probabilities = []
    for piece in raw_distribution.split(", "):
        symbol, probability = piece.split("=")
        symbols.append(symbol)
        probabilities.append(Fraction(probability))
    return message, symbols, probabilities


def cumulative_intervals(symbols, probabilities):
    running = Fraction(0)
    intervals = {}
    for symbol, probability in zip(symbols, probabilities):
        high = running + probability
        intervals[symbol] = (running, high)
        running = high
    return intervals


def expected_flow(example):
    message, symbols, probabilities = parse_problem(example["problem"])
    intervals = cumulative_intervals(symbols, probabilities)
    steps = [
        make_step("ARITH_SETUP", distribution_text(symbols, probabilities),
                  f"message={message}"),
    ]
    for symbol in symbols:
        low, high = intervals[symbol]
        steps.append(make_step("CUM_INTERVAL", symbol,
                               interval_text(low, high)))
    low = Fraction(0)
    high = Fraction(1)
    for symbol in message:
        sym_low, sym_high = intervals[symbol]
        width = high - low
        low_offset = width * sym_low
        high_offset = width * sym_high
        new_low = low + low_offset
        new_high = low + high_offset
        steps.extend([
            make_step("ARITH_SYMBOL", symbol,
                      f"cum={interval_text(sym_low, sym_high)}"),
            make_step("S", fraction_text(high), fraction_text(low),
                      fraction_text(width)),
            make_step("M", fraction_text(width), fraction_text(sym_low),
                      fraction_text(low_offset)),
            make_step("A", fraction_text(low), fraction_text(low_offset),
                      fraction_text(new_low)),
            make_step("M", fraction_text(width), fraction_text(sym_high),
                      fraction_text(high_offset)),
            make_step("A", fraction_text(low), fraction_text(high_offset),
                      fraction_text(new_high)),
            make_step("ARITH_INTERVAL", interval_text(new_low, new_high)),
        ])
        low, high = new_low, new_high
    endpoint_sum = low + high
    code = endpoint_sum / 2
    steps.append(make_step("A", fraction_text(low), fraction_text(high),
                           fraction_text(endpoint_sum)))
    steps.append(make_step("D", fraction_text(endpoint_sum), 2,
                           fraction_text(code)))
    answer = f"interval={interval_text(low, high)}; code={fraction_text(code)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestArithmeticCodingGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ArithmeticCodingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "arithmetic_coding")
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

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
