"""Exhaustive weighted-sequence oracle for MultinomialProbabilityGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.multinomial_probability_generator import (
    QUERIES, MultinomialProbabilityGenerator,
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


def parse_trial(body, variant):
    if variant == "bag_with_replacement":
        match = re.search(
            r"a bag contains (\d+) ([^,]+) tokens?, (\d+) ([^,]+) tokens?, "
            r"and (\d+) (.+?) tokens?\. .+? makes (\d+) draws with replacement",
            body)
        assert match, body
        raw = tuple(int(match.group(index)) for index in (1, 3, 5))
        total = sum(raw)
        probabilities = tuple(Fraction(value, total) for value in raw)
        n = int(match.group(7))
    else:
        n = int(re.search(r"runs (\d+) independent trials", body).group(1))
        probability_match = re.search(
            r"p_A=(\d+(?:/\d+)?), B \(.+?\) with probability "
            r"p_B=(\d+(?:/\d+)?), and C \(.+?\) with probability "
            r"p_C=(\d+(?:/\d+)?)", body)
        assert probability_match, body
        probabilities = tuple(Fraction(value) for value in probability_match.groups())
    assert sum(probabilities, Fraction()) == 1
    return n, probabilities


def weighted_rows(n, probabilities):
    for sequence in itertools.product(range(3), repeat=n):
        weight = Fraction(1)
        for outcome in sequence:
            weight *= probabilities[outcome]
        counts = tuple(sequence.count(outcome) for outcome in range(3))
        yield sequence, counts, weight


def target_counts(body):
    match = re.search(r"P\(X_A=(\d+), X_B=(\d+), X_C=(\d+)\)", body)
    assert match, body
    return tuple(map(int, match.groups()))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    n, probabilities = parse_trial(body, variant)
    rows = list(weighted_rows(n, probabilities))
    if variant in ("exact_counts", "bag_with_replacement"):
        counts = target_counts(body)
        value = sum((weight for _, observed, weight in rows if observed == counts),
                    Fraction())
        answer = ptext(value)
    elif variant == "marginal_is_binomial":
        k = int(re.search(r"P\(X_A=(\d+)\)", body).group(1))
        value = sum((weight for _, counts, weight in rows if counts[0] == k),
                    Fraction())
        answer = (f"X_A ~ Binomial({n}, {ptext(probabilities[0])}); "
                  f"P(X_A={k}) = {ptext(value)}")
    elif variant == "mean_cov":
        mean_a = sum((counts[0] * weight for _, counts, weight in rows), Fraction())
        second_a = sum((counts[0] ** 2 * weight for _, counts, weight in rows),
                       Fraction())
        mean_b = sum((counts[1] * weight for _, counts, weight in rows), Fraction())
        cross = sum((counts[0] * counts[1] * weight
                     for _, counts, weight in rows), Fraction())
        variance = second_a - mean_a ** 2
        covariance = cross - mean_a * mean_b
        answer = (f"E[X_A] = {ptext(mean_a)}; Var(X_A) = {ptext(variance)}; "
                  f"Cov(X_A,X_B) = {ptext(covariance)}")
    else:
        sequence_text = re.search(r"Specified sequence: ([ABC,]+)\.", body).group(1)
        target = tuple("ABC".index(symbol) for symbol in sequence_text.split(","))
        counts = tuple(target.count(outcome) for outcome in range(3))
        sequence_probability = next(weight for sequence, _, weight in rows
                                    if sequence == target)
        count_probability = sum((weight for _, observed, weight in rows
                                 if observed == counts), Fraction())
        answer = (f"specified sequence = {ptext(sequence_probability)}; "
                  f"matching counts = {ptext(count_probability)}")
    return {"variant": variant, "query": query, "answer": answer}


class MultinomialProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240762)

    def test_output_contract(self):
        example = MultinomialProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MultinomialProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_factorial_combination_and_power_steps_are_exact(self):
        generator = MultinomialProbabilityGenerator()
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
                elif fields[0] == "FACT":
                    self.assertEqual(math.factorial(int(fields[1])), int(fields[2]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in MultinomialProbabilityGenerator.VARIANTS:
            generator = MultinomialProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_multinomial_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MultinomialProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MultinomialProbabilityGenerator()
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
