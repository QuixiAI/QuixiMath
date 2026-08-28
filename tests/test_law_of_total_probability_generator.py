"""Independent partition-enumeration oracle for LawOfTotalProbabilityGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.law_of_total_probability_generator import (
    QUERIES, LawOfTotalProbabilityGenerator,
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


def parse_data(text):
    rows = []
    for item in text.split("; "):
        match = re.fullmatch(
            r"([a-z]+) prior=(\d+(?:/\d+)?) and P\(([a-z ]+) given \1\)="
            r"(\d+(?:/\d+)?)", item)
        assert match is not None, item
        rows.append((match.group(1), Fraction(match.group(2)),
                     Fraction(match.group(4))))
    return rows


def weighted_sum(rows):
    return sum((prior * rate for _, prior, rate in rows), Fraction())


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("two_causes", "three_causes"):
        match = re.fullmatch(
            r"(Suppliers|Servers) ([a-z, ]+) form the full source partition\. "
            r"Data: (.+)\. Event B is a (defect|failure)\.", body)
        assert match is not None, body
        rows = parse_data(match.group(3))
        expected_count = 2 if variant == "two_causes" else 3
        assert len(rows) == expected_count
        value = weighted_sum(rows)
    elif variant == "urn_choice":
        match = re.fullmatch(
            r"Choose one urn with priors (.+)\. Contents: (.+)\. Draw one ball\. "
            r"Target color: ([a-z]+)\.", body)
        assert match is not None, body
        priors = {name: Fraction(value) for name, value in
                  (item.split("=") for item in match.group(1).split("; "))}
        target = match.group(3)
        rows = []
        for item in match.group(2).split("; "):
            inventory = re.fullmatch(
                r"([a-z]+) has (\d+) ([a-z]+) and (\d+) ([a-z]+)", item)
            assert inventory is not None, item
            name, first_count, first_color, second_count, second_color = inventory.groups()
            counts = {first_color: int(first_count), second_color: int(second_count)}
            rows.append((name, priors[name], Fraction(counts[target], sum(counts.values()))))
        value = weighted_sum(rows)
    elif variant == "two_stage_draw":
        match = re.fullmatch(
            r"A bag has (\d+) ([a-z]+) and (\d+) ([a-z]+) balls\. Draw two "
            r"without replacement\. Target color: ([a-z]+)\.", body)
        assert match is not None, body
        first_count, first_color = int(match.group(1)), match.group(2)
        second_count, second_color, target = int(match.group(3)), match.group(4), match.group(5)
        items = [(first_color, index) for index in range(first_count)]
        items += [(second_color, index) for index in range(second_count)]
        outcomes = tuple(itertools.permutations(items, 2))
        value = Fraction(sum(second[0] == target for _, second in outcomes), len(outcomes))
        rows = []
    else:
        match = re.fullmatch(
            r"At ([A-Za-z]+), sunny, cloudy, and rainy form the full weather "
            r"partition\. Data: (.+)\. Event B is a delayed commute\.", body)
        assert match is not None, body
        rows = parse_data(match.group(2))
        value = weighted_sum(rows)
    if rows:
        self_total = sum((prior for _, prior, _ in rows), Fraction())
        assert self_total == 1
    return {"variant": variant, "query": query, "answer": ptext(value),
            "value": value}


class LawOfTotalProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(331662)

    def test_output_contract(self):
        example = LawOfTotalProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LawOfTotalProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_term_and_arithmetic_steps_are_exact(self):
        generator = LawOfTotalProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "TOTAL_PROB_TERM":
                    factors = [Fraction(item) for item in fields[2].split(" × ")]
                    self.assertEqual(factors[0] * factors[1], Fraction(fields[3]))

    def test_second_draw_matches_initial_color_fraction(self):
        generator = LawOfTotalProbabilityGenerator("two_stage_draw")
        for _ in range(200):
            example = generator.generate()
            match = re.search(r"A bag has (\d+) ([a-z]+) and (\d+)", example["problem"])
            self.assertIsNotNone(match)
            expected = Fraction(int(match.group(1)),
                                int(match.group(1)) + int(match.group(3)))
            self.assertEqual(Fraction(example["final_answer"]), expected)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in LawOfTotalProbabilityGenerator.VARIANTS:
            generator = LawOfTotalProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"probability_total_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LawOfTotalProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LawOfTotalProbabilityGenerator()
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
