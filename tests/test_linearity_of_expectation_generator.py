"""Independent exhaustive oracle for LinearityOfExpectationGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.linearity_of_expectation_generator import (
    QUERIES, LinearityOfExpectationGenerator,
)
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def average(values, weights=None):
    if weights is None:
        return Fraction(sum(values), len(values))
    return sum((Fraction(value) * weight for value, weight in zip(values, weights)),
               Fraction())


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "fixed_points":
        match = re.search(r"permutation of 1 through (\d+)", body)
        size = int(match.group(1))
        counts = [sum(index + 1 == value for index, value in enumerate(perm))
                  for perm in itertools.permutations(range(1, size + 1))]
        value = average(counts)
        answer = f"{size} × 1/{size} = {ptext(value)}"
    elif variant == "distinct_values":
        match = re.search(r"(\d+) independent fair (\d+)-sided dice", body)
        rolls, faces = map(int, match.groups())
        counts = [len(set(outcome))
                  for outcome in itertools.product(range(1, faces + 1), repeat=rolls)]
        value, answer = average(counts), None
    elif variant == "empty_bins":
        match = re.search(r"(\d+) labelled balls .* into (\d+) labelled bins", body)
        balls, bins = map(int, match.groups())
        counts = [bins - len(set(outcome))
                  for outcome in itertools.product(range(bins), repeat=balls)]
        value, answer = average(counts), None
    elif variant == "heads_different_coins":
        match = re.search(r"(\d+) independent coins with head probabilities (.+)\. Let", body)
        count, data = int(match.group(1)), match.group(2)
        probabilities = [Fraction(value) for value in
                         re.findall(r"p\d+=(\d+(?:/\d+)?)", data)]
        assert len(probabilities) == count
        values, weights = [], []
        for outcome in itertools.product((0, 1), repeat=count):
            weight = Fraction(1)
            for bit, probability in zip(outcome, probabilities):
                weight *= probability if bit else 1 - probability
            values.append(sum(outcome))
            weights.append(weight)
        value, answer = average(values, weights), None
    elif variant == "sum_dice":
        match = re.search(r"dice with side counts ([\d, ]+)\. Let", body)
        sides = tuple(map(int, match.group(1).split(", ")))
        values = [sum(outcome) for outcome in
                  itertools.product(*(range(1, side + 1) for side in sides))]
        value, answer = average(values), None
    elif variant == "adjacent_same_color":
        match = re.search(r"sequence of length (\d+) that uses (\d+) colors", body)
        length, colors = map(int, match.groups())
        values = [sum(first == second for first, second in zip(outcome, outcome[1:]))
                  for outcome in itertools.product(range(colors), repeat=length)]
        value, answer = average(values), None
    else:
        match = re.search(r"(\d+) people who independently choose .* from (\d+) labelled", body)
        people, dates = map(int, match.groups())
        values = []
        for outcome in itertools.product(range(dates), repeat=people):
            values.append(sum(outcome[a] == outcome[b]
                              for a, b in itertools.combinations(range(people), 2)))
        value = average(values)
        answer = f"E[Y] = {ptext(value)}"
    if answer is None:
        answer = ptext(value)
    return {"variant": variant, "query": query, "answer": answer,
            "value": value}


class LinearityOfExpectationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(174206)

    def test_output_contract(self):
        example = LinearityOfExpectationGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = LinearityOfExpectationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_combination_steps_are_exact(self):
        generator = LinearityOfExpectationGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"\((\d+(?:/\d+)?)\)\^(\d+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))

    def test_fixed_point_constant_answer_is_composite(self):
        generator = LinearityOfExpectationGenerator("fixed_points")
        for _ in range(100):
            answer = generator.generate()["final_answer"]
            self.assertRegex(answer, r"^[3-6] × 1/[3-6] = 1$")

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in LinearityOfExpectationGenerator.VARIANTS:
            generator = LinearityOfExpectationGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_linearity_expectation_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LinearityOfExpectationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LinearityOfExpectationGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
