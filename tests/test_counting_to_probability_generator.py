"""Brute-force oracle for CountingToProbabilityGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.counting_to_probability_generator import (
    QUERIES, CountingToProbabilityGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_roster(text):
    return tuple(item.strip() for item in text[1:-1].split(", "))


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "first_letter":
        match = re.fullmatch(
            r"The distinct letters of codeword ([A-Z]+) are arranged uniformly at random\.", body)
        assert match is not None, body
        items = tuple(match.group(1))
        assert len(set(items)) == len(items)
        outcomes = tuple(itertools.permutations(items))
        favorable = sum(outcome[0] in "AEIOU" for outcome in outcomes)
    elif variant == "no_repeats_code":
        match = re.fullmatch(
            r"A code of length (\d+) is selected uniformly from all strings over "
            r"symbols (\{[^{}]+\}); repetition is allowed in the full space\.", body)
        assert match is not None, body
        length, items = int(match.group(1)), parse_roster(match.group(2))
        outcomes = tuple(itertools.product(items, repeat=length))
        favorable = sum(len(set(outcome)) == length for outcome in outcomes)
    elif variant == "friends_adjacent":
        match = re.fullmatch(
            r"The people (\{[^{}]+\}) line up uniformly at random\. The named "
            r"friends are ([A-Za-z]+) and ([A-Za-z]+)\.", body)
        assert match is not None, body
        items = parse_roster(match.group(1))
        first, second = match.group(2), match.group(3)
        outcomes = tuple(itertools.permutations(items))
        favorable = sum(abs(outcome.index(first) - outcome.index(second)) == 1
                         for outcome in outcomes)
    elif variant == "specific_position":
        match = re.fullmatch(
            r"The distinct symbols (\{[^{}]+\}) are arranged uniformly at random\. "
            r"Target: ([A-Z]) in position (\d+)\.", body)
        assert match is not None, body
        items = parse_roster(match.group(1))
        target, position = match.group(2), int(match.group(3)) - 1
        outcomes = tuple(itertools.permutations(items))
        favorable = sum(outcome[position] == target for outcome in outcomes)
    else:
        match = re.fullmatch(
            r"The distinct numbered cards (\{[^{}]+\}) are arranged uniformly at "
            r"random in a row\.", body)
        assert match is not None, body
        items = tuple(map(int, parse_roster(match.group(1))))
        outcomes = tuple(itertools.permutations(items))
        favorable = sum(outcome[-1] % 2 == 0 for outcome in outcomes)
    value = Fraction(favorable, len(outcomes))
    return {"variant": variant, "query": query, "answer": ptext(value),
            "value": value, "favorable": favorable, "total": len(outcomes)}


class CountingToProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(264575)

    def test_output_contract(self):
        example = CountingToProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CountingToProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_counting_and_arithmetic_steps_are_exact(self):
        generator = CountingToProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            running_fcp = None
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "FACT":
                    self.assertEqual(math.factorial(int(fields[1])), int(fields[2]))
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]), int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]), int(fields[3]))
                elif fields[0] == "FCP":
                    choices, current = int(fields[2]), int(fields[3])
                    if fields[1].startswith("position "):
                        expected = choices if running_fcp is None else running_fcp * choices
                        self.assertEqual(current, expected)
                        running_fcp = current
                    else:
                        self.assertEqual(choices, current)
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                    self.assertEqual(fields[2], ptext(Fraction(fields[2])))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CountingToProbabilityGenerator.VARIANTS:
            generator = CountingToProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"probability_counting_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CountingToProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CountingToProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
