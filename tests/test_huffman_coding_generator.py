import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.huffman_coding_generator import HuffmanCodingGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Build a Huffman code for symbols with probabilities (.+)\. Report "
    r"code lengths, expected length L, entropy H, and Kraft sum\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def parse_distribution(problem):
    raw = PROBLEM_RE.fullmatch(problem).group(1)
    symbols = []
    probabilities = []
    for piece in raw.split(", "):
        symbol, probability = piece.split("=")
        symbols.append(symbol)
        probabilities.append(Fraction(probability))
    return symbols, probabilities


def distribution_text(symbols, probabilities):
    return ", ".join(
        f"{symbol}={fraction_text(probability)}"
        for symbol, probability in zip(symbols, probabilities)
    )


def label(symbols):
    return "".join(sorted(symbols))


def node_text(node_label, weight):
    return f"{node_label}:{fraction_text(weight)}"


def huffman_trace(symbols, probabilities):
    nodes = [
        (probability, symbol, (symbol,))
        for symbol, probability in zip(symbols, probabilities)
    ]
    lengths = {symbol: 0 for symbol in symbols}
    merge_steps = []
    while len(nodes) > 1:
        nodes.sort(key=lambda item: (item[0], item[1]))
        left_weight, left_label, left_symbols = nodes.pop(0)
        right_weight, right_label, right_symbols = nodes.pop(0)
        merged_symbols = tuple(sorted(left_symbols + right_symbols))
        merged_label = label(merged_symbols)
        merged_weight = left_weight + right_weight
        for symbol in merged_symbols:
            lengths[symbol] += 1
        merge_steps.append(
            make_step("HUFFMAN_MERGE",
                      f"{node_text(left_label, left_weight)} + "
                      f"{node_text(right_label, right_weight)}",
                      node_text(merged_label, merged_weight))
        )
        nodes.append((merged_weight, merged_label, merged_symbols))
    return merge_steps, lengths


def append_expected_length(steps, symbols, probabilities, lengths):
    steps.append(make_step("HUFFMAN_FORMULA", "L=sum p_i*l_i"))
    running = Fraction(0)
    for symbol, probability in zip(symbols, probabilities):
        term = probability * lengths[symbol]
        steps.append(make_step("M", fraction_text(probability),
                               lengths[symbol], fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    return running


def append_entropy(steps, probabilities):
    steps.append(make_step("ENTROPY_SETUP", "H", "-sum p log2(p)"))
    running = Fraction(0)
    for probability in probabilities:
        exponent = probability.denominator.bit_length() - 1
        term = probability * exponent
        steps.append(make_step("LOG2", fraction_text(probability),
                               -exponent))
        steps.append(make_step("M", fraction_text(probability), exponent,
                               fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    return running


def append_kraft(steps, symbols, lengths):
    steps.append(make_step("KRAFT_FORMULA", "sum 2^-l_i"))
    running = Fraction(0)
    for symbol in symbols:
        denominator = 2 ** lengths[symbol]
        term = Fraction(1, denominator)
        steps.append(make_step("E", 2, lengths[symbol], denominator))
        steps.append(make_step("D", 1, denominator, fraction_text(term)))
        new_running = running + term
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
        running = new_running
    return running


def expected_flow(example):
    symbols, probabilities = parse_distribution(example["problem"])
    steps = [
        make_step("HUFFMAN_SETUP", distribution_text(symbols, probabilities)),
    ]
    merge_steps, lengths = huffman_trace(symbols, probabilities)
    steps.extend(merge_steps)
    for symbol in symbols:
        steps.append(make_step("CODE_LENGTH", symbol, f"l={lengths[symbol]}"))
    expected_length = append_expected_length(
        steps, symbols, probabilities, lengths
    )
    entropy = append_entropy(steps, probabilities)
    kraft = append_kraft(steps, symbols, lengths)
    steps.append(make_step("KRAFT_CHECK", f"sum={fraction_text(kraft)}",
                           "complete" if kraft == 1 else "incomplete"))
    length_text = ",".join(
        f"{symbol}:{lengths[symbol]}" for symbol in symbols
    )
    answer = (
        f"lengths={length_text}; "
        f"L={fraction_text(expected_length)} {bit_unit(expected_length)}; "
        f"H={fraction_text(entropy)} {bit_unit(entropy)}; "
        f"Kraft={fraction_text(kraft)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestHuffmanCodingGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = HuffmanCodingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "huffman_coding")
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
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
