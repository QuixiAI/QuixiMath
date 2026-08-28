"""Prompt-text oracle for RandomDigitSimulationGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.random_digit_simulation_generator import (
    QUERIES, RandomDigitSimulationGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def _scan(blocks, success_digits, threshold):
    counts = [sum(int(digit) < success_digits for digit in block)
              for block in blocks]
    return counts, sum(count >= threshold for count in counts)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "two_digit_blocks":
        match = re.fullmatch(
            r"An event has probability (\d+(?:/\d+)?)\. Use two-digit blocks "
            r"00 through 99: blocks 00–(\d{2}) represent success and blocks "
            r"(\d{2})–99 represent failure\. Random blocks: ([0-9 ]+)\.", body)
        assert match is not None, body
        probability = Fraction(match.group(1))
        success_end, failure_start = int(match.group(2)), int(match.group(3))
        assert success_end + 1 == failure_start
        assert probability == Fraction(failure_start, 100)
        blocks = match.group(4).split()
        counts = [int(block) < failure_start for block in blocks]
        successful = sum(counts)
        estimate = Fraction(successful, len(blocks))
        answer = ptext(estimate)
        threshold, success_digits = None, failure_start
    elif variant == "assign_digits":
        match = re.fullmatch(
            r"An attempt succeeds with probability (\d+(?:/\d+)?)\. Use the "
            r"convention that the smallest digits starting at 0 represent "
            r"success\. Each block of (\d+) digits is one trial of \2 attempts\. "
            r"Random digits: ([0-9 ]+)\. Event: at least (\d+) successes\.", body)
        assert match is not None, body
        probability = Fraction(match.group(1))
        success_digits = int(probability * 10)
        assert Fraction(success_digits, 10) == probability
        shots, blocks, threshold = int(match.group(2)), match.group(3).split(), int(match.group(4))
        assert all(len(block) == shots for block in blocks)
        counts, successful = _scan(blocks, success_digits, threshold)
        estimate = Fraction(successful, len(blocks))
        answer = (f"0–{success_digits - 1} success, {success_digits}–9 failure; "
                  f"{ptext(estimate)}")
    else:
        match = re.fullmatch(
            r"A free throw succeeds with probability (\d+(?:/\d+)?)\. Digits "
            r"0–(\d) mean make and digits (\d)–9 mean miss\. Each block of "
            r"(\d+) digits is one game of \4 shots\. Random digits: ([0-9 ]+)\. "
            r"Event: at least (\d+) makes\.", body)
        assert match is not None, body
        probability = Fraction(match.group(1))
        success_end, failure_start = int(match.group(2)), int(match.group(3))
        assert success_end + 1 == failure_start
        success_digits = failure_start
        assert probability == Fraction(success_digits, 10)
        shots, blocks, threshold = int(match.group(4)), match.group(5).split(), int(match.group(6))
        assert all(len(block) == shots for block in blocks)
        counts, successful = _scan(blocks, success_digits, threshold)
        estimate = Fraction(successful, len(blocks))
        if variant == "compare_to_theoretical":
            theoretical = sum(
                (Fraction(math.comb(shots, k)) * probability ** k *
                 (1 - probability) ** (shots - k)
                 for k in range(threshold, shots + 1)), Fraction())
            answer = (f"estimate {ptext(estimate)}; theoretical "
                      f"{ptext(theoretical)}")
        else:
            theoretical = None
            answer = ptext(estimate)
    return {"variant": variant, "query": query, "answer": answer,
            "blocks": blocks, "counts": counts, "successful": successful,
            "estimate": estimate, "threshold": threshold,
            "shots": None if variant == "two_digit_blocks" else shots,
            "success_digits": success_digits,
            "theoretical": theoretical if variant == "compare_to_theoretical" else None}


class RandomDigitSimulationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(173205)

    def test_output_contract(self):
        example = RandomDigitSimulationGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RandomDigitSimulationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_digit_scans_counts_and_fraction_steps_match_prompt(self):
        generator = RandomDigitSimulationGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            scans = [raw.split(DELIM) for raw in example["steps"]
                     if raw.startswith("DIGIT_SCAN" + DELIM)]
            self.assertEqual([fields[1] for fields in scans], parts["blocks"])
            if parts["variant"] == "two_digit_blocks":
                expected_readings = [f"value {int(block)}" for block in parts["blocks"]]
                expected_verdicts = ["yes" if count else "no" for count in parts["counts"]]
            else:
                expected_readings = [f"makes {count}" for count in parts["counts"]]
                expected_verdicts = ["yes" if count >= parts["threshold"] else "no"
                                     for count in parts["counts"]]
            self.assertEqual([fields[2] for fields in scans], expected_readings)
            self.assertEqual([fields[3] for fields in scans], expected_verdicts)
            count_step = next(raw.split(DELIM) for raw in example["steps"]
                              if raw.startswith("COUNT" + DELIM))
            setup_step = next(raw.split(DELIM) for raw in example["steps"]
                              if raw.startswith("PROB_SETUP" + DELIM))
            self.assertEqual(int(count_step[2]), parts["successful"])
            self.assertEqual(Fraction(int(setup_step[1]), int(setup_step[2])),
                             parts["estimate"])
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                    self.assertEqual(fields[2], ptext(Fraction(fields[2])))

    def test_theoretical_terms_form_the_independent_binomial_sum(self):
        generator = RandomDigitSimulationGenerator("compare_to_theoretical")
        for _ in range(200):
            example = generator.generate()
            parts = oracle_parts(example)
            term_steps = [raw.split(DELIM) for raw in example["steps"]
                          if raw.startswith("TERM" + DELIM)]
            p = Fraction(parts["success_digits"], 10)
            expected = []
            for makes in range(parts["threshold"], parts["shots"] + 1):
                value = (math.comb(parts["shots"], makes) * p ** makes *
                         (1 - p) ** (parts["shots"] - makes))
                expected.append((f"{makes} makes", value))
            self.assertEqual([(fields[1], Fraction(fields[3]))
                              for fields in term_steps], expected)
            self.assertEqual(sum((value for _, value in expected), Fraction()),
                             parts["theoretical"])
            sum_step = next(raw.split(DELIM) for raw in example["steps"]
                            if raw.startswith("SUM" + DELIM))
            self.assertEqual(sum((Fraction(item) for item in sum_step[1].split(" + ")),
                                 Fraction()), Fraction(sum_step[2]))
            self.assertEqual(Fraction(sum_step[2]), parts["theoretical"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RandomDigitSimulationGenerator.VARIANTS:
            generator = RandomDigitSimulationGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_random_digit_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RandomDigitSimulationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RandomDigitSimulationGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"\^0\b|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
