import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.entropy_generator import EntropyGenerator
from helpers import DELIM


DIST_RE = re.compile(
    r"Compute Shannon entropy in bits for distribution P=\[([^]]+)\]\."
)
INFO_RE = re.compile(
    r"An event has probability p=([^ ]+)\. Find its information content "
    r"in bits\."
)
COUNTS_RE = re.compile(
    r"A source emits symbols with counts \[([^]]+)\] out of total (\d+)\. "
    r"Find entropy in bits\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


def entropy_terms(probabilities):
    rows = []
    running = Fraction(0)
    for probability in probabilities:
        self_information = -log2_power(probability)
        term = probability * self_information
        new_running = running + term
        rows.append((probability, self_information, term,
                     running, new_running))
        running = new_running
    return rows, running


def log2_power(probability):
    value = Fraction(probability)
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    if value != 1:
        raise AssertionError(f"not a power of two: {probability}")
    return exponent


def expected_distribution(problem):
    probabilities = [
        Fraction(piece) for piece in DIST_RE.fullmatch(problem).group(1).split(",")
    ]
    rows, entropy = entropy_terms(probabilities)
    steps = [
        make_step("ENTROPY_SETUP",
                  f"P={list_text([fraction_text(p) for p in probabilities])}",
                  "H=-sum p log2(p)"),
    ]
    for probability, self_information, term, running, new_running in rows:
        steps.append(make_step("LOG2", fraction_text(probability),
                               -self_information))
        steps.append(make_step("M", fraction_text(probability),
                               self_information, fraction_text(term)))
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
    answer = f"H={fraction_text(entropy)} {bit_unit(entropy)}"
    return steps, answer


def expected_information(problem):
    probability = Fraction(INFO_RE.fullmatch(problem).group(1))
    log_value = log2_power(probability)
    information = -log_value
    steps = [
        make_step("INFO_SETUP", f"p={fraction_text(probability)}",
                  "I=-log2(p)"),
        make_step("LOG2", fraction_text(probability), log_value),
        make_step("S", 0, log_value, information),
    ]
    answer = f"I={information} {bit_unit(information)}"
    return steps, answer


def expected_counts(problem):
    counts_raw, total_raw = COUNTS_RE.fullmatch(problem).groups()
    counts = [int(piece) for piece in counts_raw.split(",")]
    total = int(total_raw)
    probabilities = [Fraction(count, total) for count in counts]
    rows, entropy = entropy_terms(probabilities)
    steps = [
        make_step("ENTROPY_SETUP",
                  f"counts={list_text(counts)}, total={total}",
                  "H=-sum p log2(p)"),
    ]
    for count, row in zip(counts, rows):
        probability, self_information, term, running, new_running = row
        steps.append(make_step("D", count, total, fraction_text(probability)))
        steps.append(make_step("LOG2", fraction_text(probability),
                               -self_information))
        steps.append(make_step("M", fraction_text(probability),
                               self_information, fraction_text(term)))
        steps.append(make_step("A", fraction_text(running),
                               fraction_text(term),
                               fraction_text(new_running)))
    answer = f"H={fraction_text(entropy)} {bit_unit(entropy)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if DIST_RE.fullmatch(problem):
        steps, answer = expected_distribution(problem)
    elif INFO_RE.fullmatch(problem):
        steps, answer = expected_information(problem)
    elif COUNTS_RE.fullmatch(problem):
        steps, answer = expected_counts(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestEntropyGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = EntropyGenerator()

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

    def test_variants_are_available(self):
        for variant in EntropyGenerator.VARIANTS:
            result = EntropyGenerator(variant).generate()
            self.assertEqual(result["operation"], f"entropy_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EntropyGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
