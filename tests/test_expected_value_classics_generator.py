"""Recurrence, sequence, and permutation oracle for classic expectations."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.expected_value_classics_generator import (
    QUERIES, ExpectedValueClassicsGenerator,
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


def coupon_wait(count, start, target):
    waits = [Fraction() for _ in range(count + 1)]
    for collected in reversed(range(target)):
        new_probability = Fraction(count - collected, count)
        # Rearranged first-step equation:
        # E_i = 1 + (i/n)E_i + ((n-i)/n)E_(i+1).
        waits[collected] = (1 + new_probability * waits[collected + 1]) / new_probability
    return waits[start] - waits[target]


def derangements(size):
    return sum(all(permutation[index] != index for index in range(size))
               for permutation in itertools.permutations(range(size)))


def pi_form(coefficient):
    coefficient = Fraction(coefficient)
    if coefficient.denominator == 1:
        return "1/π" if coefficient.numerator == 1 else f"{coefficient.numerator}/π"
    if coefficient.numerator == 1:
        return f"1/({coefficient.denominator}π)"
    return f"{coefficient.numerator}/({coefficient.denominator}π)"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "coupon_collector":
        count = int(re.search(r"n=(\d+) equally likely", body).group(1))
        answer = ptext(coupon_wait(count, 0, count))
    elif variant == "coupon_next":
        count, collected = map(int, re.search(
            r"n=(\d+) equally likely.+, and (\d+) distinct", body).groups())
        answer = ptext(Fraction(count, count - collected))
    elif variant == "coupon_first_k":
        count = int(re.search(r"n=(\d+) equally likely", body).group(1))
        target = int(re.search(r"k=(\d+) distinct", body).group(1))
        answer = ptext(coupon_wait(count, 0, target))
    elif variant == "coupon_all_in_n":
        count = int(re.search(r"Each of n=(\d+) draws", body).group(1))
        favorable = 0
        for sequence in itertools.product(range(count), repeat=count):
            favorable += len(set(sequence)) == count
        answer = ptext(Fraction(favorable, count ** count))
    elif variant in ("matching_at_least_one", "matching_exactly_k"):
        count = int(re.search(r"permutation assigns n=(\d+)", body).group(1))
        fixed_counts = [sum(value == index for index, value in enumerate(permutation))
                        for permutation in itertools.permutations(range(count))]
        if variant == "matching_at_least_one":
            favorable = sum(value >= 1 for value in fixed_counts)
        else:
            fixed = int(re.search(r"exactly k=(\d+) fixed", body).group(1))
            favorable = sum(value == fixed for value in fixed_counts)
        answer = ptext(Fraction(favorable, math.factorial(count)))
    elif variant == "buffon_probability":
        spacing, length = map(int, re.search(r"d=(\d+).+length L=(\d+)", body).groups())
        answer = pi_form(Fraction(2 * length, spacing))
    elif variant == "buffon_pi_estimate":
        trials, crossings = map(int, re.search(r"n=(\d+) drops, crossings=(\d+)",
                                               body).groups())
        answer = f"pi estimate = {ptext(Fraction(2 * trials, crossings))}"
    else:
        cutoff = int(re.search(r"cutoff of m=(\d+) tosses", body).group(1))
        expectation = Fraction()
        for index in range(1, cutoff + 1):
            # Enumerate all H...HT first-tail strings of length index.
            probability = Fraction(1, 2) ** index
            expectation += probability * 2 ** index
        answer = f"expected payout = {ptext(expectation)}"
    return {"variant": variant, "query": query, "answer": answer}


class ExpectedValueClassicsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240769)

    def test_output_contract(self):
        example = ExpectedValueClassicsGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ExpectedValueClassicsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_factorial_combination_and_power_steps_are_exact(self):
        generator = ExpectedValueClassicsGenerator()
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

    def test_plan_examples(self):
        self.assertEqual(coupon_wait(6, 0, 6), Fraction(147, 10))
        self.assertEqual(Fraction(math.factorial(4), 4 ** 4), Fraction(3, 32))
        self.assertEqual(Fraction(math.comb(4, 1) * derangements(3),
                                  math.factorial(4)), Fraction(1, 3))
        self.assertEqual(pi_form(Fraction(2, 3)), "2/(3π)")
        self.assertEqual(Fraction(2 * 100, 64), Fraction(25, 8))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ExpectedValueClassicsGenerator.VARIANTS:
            generator = ExpectedValueClassicsGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_expected_value_classics_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ExpectedValueClassicsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ExpectedValueClassicsGenerator()
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
