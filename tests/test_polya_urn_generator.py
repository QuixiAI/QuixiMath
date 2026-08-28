"""Recursive urn-state oracle for PolyaUrnGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.polya_urn_generator import QUERIES, PolyaUrnGenerator
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


def parse_setup(body):
    return tuple(map(int, re.search(r"r=(\d+) red and b=(\d+) blue.+c=(\d+)",
                                    body).groups()))


def sequence_probability(red, blue, reinforcement, sequence):
    probability = Fraction(1)
    for color in sequence:
        total = red + blue
        if color == "R":
            probability *= Fraction(red, total)
            red += reinforcement
        else:
            probability *= Fraction(blue, total)
            blue += reinforcement
    return probability


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    red, blue, reinforcement = parse_setup(body)
    target = re.search(r"Target: (.+)\.$", body).group(1)
    if variant in ("sequence_probability", "reinforcement_c"):
        sequence = re.fullmatch(r"P\(sequence ([RB, ]+)\)", target).group(1).split(", ")
        probability = sequence_probability(red, blue, reinforcement, sequence)
        answer = f"P({', '.join(sequence)}) = {ptext(probability)}"
    elif variant == "exchangeability_check":
        match = re.fullmatch(r"compare P\(([RB, ]+)\) and P\(([RB, ]+)\)", target)
        first, second = (value.split(", ") for value in match.groups())
        first_probability = sequence_probability(red, blue, reinforcement, first)
        second_probability = sequence_probability(red, blue, reinforcement, second)
        answer = (f"P({', '.join(first)}) = {ptext(first_probability)}; "
                  f"P({', '.join(second)}) = {ptext(second_probability)}; "
                  f"equal (exchangeable)")
    elif variant == "kth_draw_marginal":
        draw = int(re.fullmatch(r"P\(draw (\d+) is R\)", target).group(1))
        probability = sum((sequence_probability(red, blue, reinforcement, sequence)
                           for sequence in itertools.product(("R", "B"), repeat=draw)
                           if sequence[-1] == "R"), Fraction())
        answer = f"P(draw {draw} is R) = {ptext(probability)}"
    elif variant == "count_after_n":
        red_draws, draws = map(int, re.fullmatch(
            r"P\(exactly (\d+) red draws among n=(\d+)\)", target).groups())
        probability = sum((sequence_probability(red, blue, reinforcement, sequence)
                           for sequence in itertools.product(("R", "B"), repeat=draws)
                           if sequence.count("R") == red_draws), Fraction())
        answer = f"P({red_draws} red draws in {draws}) = {ptext(probability)}"
    else:
        draws = int(re.fullmatch(r"expected red fraction after n=(\d+) draws", target).group(1))
        expected = Fraction()
        for sequence in itertools.product(("R", "B"), repeat=draws):
            weight = sequence_probability(red, blue, reinforcement, sequence)
            final_red = red + reinforcement * sequence.count("R")
            final_total = red + blue + reinforcement * draws
            expected += weight * Fraction(final_red, final_total)
        answer = f"expected red fraction after {draws} draws = {ptext(expected)}"
    return {"variant": variant, "query": query, "answer": answer}


class PolyaUrnGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240772)

    def test_output_contract(self):
        example = PolyaUrnGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PolyaUrnGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_combination_steps_are_exact(self):
        generator = PolyaUrnGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))

    def test_plan_exchangeability_example(self):
        first = sequence_probability(2, 1, 1, ("R", "B", "R"))
        second = sequence_probability(2, 1, 1, ("B", "R", "R"))
        self.assertEqual(first, Fraction(1, 10))
        self.assertEqual(second, Fraction(1, 10))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in PolyaUrnGenerator.VARIANTS:
            generator = PolyaUrnGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_polya_urn_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PolyaUrnGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PolyaUrnGenerator()
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
