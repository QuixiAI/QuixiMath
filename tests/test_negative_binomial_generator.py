"""Weighted-sequence and first-step oracle for NegativeBinomialGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.negative_binomial_generator import QUERIES, NegativeBinomialGenerator
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


def sequence_weight(bits, p):
    weight = Fraction(1)
    for bit in bits:
        weight *= p if bit else 1 - p
    return weight


def waiting_moments(r, p):
    means = [Fraction() for _ in range(r + 1)]
    seconds = [Fraction() for _ in range(r + 1)]
    q = 1 - p
    for successes in reversed(range(r)):
        means[successes] = (1 + p * means[successes + 1]) / p
        continuation_mean = p * means[successes + 1] + q * means[successes]
        seconds[successes] = (1 + 2 * continuation_mean
                              + p * seconds[successes + 1]) / p
    return means[0], seconds[0] - means[0] ** 2


def exact_trial_probability(r, n, p):
    total = Fraction()
    for prefix in itertools.product((0, 1), repeat=n - 1):
        bits = prefix + (1,)
        if sum(prefix) == r - 1:
            total += sequence_weight(bits, p)
    return total


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    p = Fraction(re.search(r"p=(\d+(?:/\d+)?)", body).group(1))
    if variant == "geometric_special_case":
        n = int(re.search(r"P\(N=(\d+)\)", body).group(1))
        probability = exact_trial_probability(1, n, p)
        mean, _ = waiting_moments(1, p)
        answer = f"P(N={n}) = {ptext(probability)}; E[N] = {ptext(mean)}"
    else:
        r = int(re.search(r"the (\d+)(?:th|st|nd|rd) success", body).group(1))
        if variant == "exact_trial":
            n = int(re.search(r"P\(N=(\d+)\)", body).group(1))
            answer = ptext(exact_trial_probability(r, n, p))
        elif variant == "at_most_trials":
            n = int(re.search(r"P\(N≤(\d+)\)", body).group(1))
            total = Fraction()
            for bits in itertools.product((0, 1), repeat=n):
                if sum(bits) >= r:
                    total += sequence_weight(bits, p)
            answer = ptext(total)
        elif variant == "failures_form":
            failures = int(re.search(r"P\(F=(\d+)\)", body).group(1))
            answer = ptext(exact_trial_probability(r, r + failures, p))
        else:
            mean, variance = waiting_moments(r, p)
            answer = ptext(mean if variant == "mean" else variance)
    return {"variant": variant, "query": query, "answer": answer}


class NegativeBinomialGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240761)

    def test_output_contract(self):
        example = NegativeBinomialGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = NegativeBinomialGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_combination_steps_are_exact(self):
        generator = NegativeBinomialGenerator()
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
                    match = re.fullmatch(r"base (\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in NegativeBinomialGenerator.VARIANTS:
            generator = NegativeBinomialGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_negative_binomial_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NegativeBinomialGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = NegativeBinomialGenerator()
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
