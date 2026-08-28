"""Independent Cartesian-product oracle for SampleSpaceListGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.sample_space_list_generator import QUERIES, SampleSpaceListGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_roster(text):
    return tuple(int(item) for item in text[1:-1].split(", "))


def probability_text(favorable, total):
    value = Fraction(favorable, total)
    return str(value.numerator) if value.denominator == 1 else str(value)


def joined(items):
    return ", ".join(map(str, items))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    body = re.sub(r"^At the [a-z ]+, ", "", body)
    if variant in ("list_and_count", "event_probability"):
        match = re.fullmatch(
            r"A coin is flipped and a spinner with sectors (\{[^{}]+\}) is "
            r"spun\. Outcomes put H before T and write the spinner label "
            r"second\.(?: Event A is heads and an (odd|even) spinner label\.)?",
            body)
        assert match is not None, body
        sectors = parse_roster(match.group(1))
        outcomes = tuple(f"{coin}{sector}" for coin in ("H", "T")
                         for sector in sectors)
        if variant == "list_and_count":
            answer = f"{joined(outcomes)}; {len(outcomes)} outcomes"
            favorable = None
        else:
            parity = 1 if match.group(2) == "odd" else 0
            favorable = tuple(f"H{sector}" for sector in sectors
                              if sector % 2 == parity)
            answer = (f"{joined(outcomes)}; {len(outcomes)} outcomes; "
                      f"{probability_text(len(favorable), len(outcomes))}")
    elif variant == "two_coins":
        match = re.fullmatch(
            r"The ([a-z]+) coin is flipped, then the ([a-z]+) coin\. Event A "
            r"is (exactly one head|at least one head|matching faces); outcome "
            r"strings record that order\.", body)
        assert match is not None, body
        outcomes = ("HH", "HT", "TH", "TT")
        case = match.group(3)
        favorable = tuple(outcome for outcome in outcomes
                          if ((outcome.count("H") == 1) if case == "exactly one head"
                              else ("H" in outcome) if case == "at least one head"
                              else outcome[0] == outcome[1]))
        answer = (f"{joined(outcomes)}; 4 outcomes; "
                  f"{probability_text(len(favorable), 4)}")
    elif variant == "two_spinners":
        match = re.fullmatch(
            r"Spinner 1 sectors are (\{[^{}]+\}); spinner 2 sectors are "
            r"(\{[^{}]+\})\. Event A is that the pair sum is (even|odd)\. "
            r"Pairs list spinner 1 first\.", body)
        assert match is not None, body
        first, second = parse_roster(match.group(1)), parse_roster(match.group(2))
        pairs = tuple(itertools.product(first, second))
        outcomes = tuple(f"({a}, {b})" for a, b in pairs)
        parity = 0 if match.group(3) == "even" else 1
        favorable = tuple(pair for pair in pairs if sum(pair) % 2 == parity)
        answer = (f"{joined(outcomes)}; {len(outcomes)} outcomes; "
                  f"{probability_text(len(favorable), len(outcomes))}")
    else:
        match = re.fullmatch(
            r"Digit cards are (\{[^{}]+\})\. Draw two without replacement "
            r"to form a two-digit number\. Event A is that the two-digit "
            r"number is greater than (\d+)\.", body)
        assert match is not None, body
        digits, threshold = parse_roster(match.group(1)), int(match.group(2))
        outcomes = tuple(10 * a + b for a in digits for b in digits if a != b)
        favorable = tuple(number for number in outcomes if number > threshold)
        answer = (f"{joined(outcomes)}; {len(outcomes)} outcomes; "
                  f"{probability_text(len(favorable), len(outcomes))}")
    return {"variant": variant, "query": query, "answer": answer,
            "outcomes": outcomes, "favorable": favorable}


class SampleSpaceListGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(577215)

    def test_output_contract(self):
        example = SampleSpaceListGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SampleSpaceListGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_sample_space_and_event_steps_are_exact(self):
        generator = SampleSpaceListGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            sample = next(raw.split(DELIM) for raw in example["steps"]
                          if raw.startswith("SAMPLE_SPACE" + DELIM))
            self.assertEqual(int(sample[3]), len(parts["outcomes"]))
            if parts["favorable"] is not None:
                event = next(raw.split(DELIM) for raw in example["steps"]
                             if raw.startswith("EVENT" + DELIM))
                self.assertEqual(int(event[3]), len(parts["favorable"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SampleSpaceListGenerator.VARIANTS:
            generator = SampleSpaceListGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_sample_space_list_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SampleSpaceListGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SampleSpaceListGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
