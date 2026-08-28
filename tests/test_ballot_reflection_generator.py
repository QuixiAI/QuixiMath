"""Exhaustive ballot-order and plus/minus path oracle."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.ballot_reflection_generator import QUERIES, BallotReflectionGenerator
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


def walk_paths(n):
    for increments in itertools.product((-1, 1), repeat=n):
        partials = [0]
        for increment in increments:
            partials.append(partials[-1] + increment)
        yield partials


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "ballot_probability":
        a, b = map(int, re.search(r"A has a=(\d+).+B has b=(\d+)", body).groups())
        total = favorable = 0
        for a_positions in itertools.combinations(range(a + b), a):
            a_set = set(a_positions)
            lead = 0
            valid = True
            for index in range(a + b):
                lead += 1 if index in a_set else -1
                valid &= lead > 0
            total += 1
            favorable += valid
        answer = ptext(Fraction(favorable, total))
    else:
        n = int(re.search(r"takes n=(\d+) steps", body).group(1)
                if "takes n=" in body else
                re.search(r"occurs at n=(\d+)", body).group(1))
        paths = list(walk_paths(n))
        if variant == "paths_touching_level":
            endpoint, depth = map(int, re.search(
                r"ends at S_n=(-?\d+) and touches level -(\d+)", body).groups())
            favorable = sum(path[-1] == endpoint and -depth in path for path in paths)
        elif variant == "first_return":
            favorable = sum(path[-1] == 0 and all(value != 0 for value in path[1:-1])
                             for path in paths)
        elif variant == "max_at_least":
            level = int(re.search(r"level a=(\d+)", body).group(1))
            favorable = sum(max(path) >= level for path in paths)
        elif variant == "stay_nonnegative":
            favorable = sum(min(path) >= 0 for path in paths)
        else:
            favorable = sum(min(path) >= 0 and path[-1] == 0 for path in paths)
        answer = ptext(Fraction(favorable, 2 ** n))
    return {"variant": variant, "query": query, "answer": answer}


class BallotReflectionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240771)

    def test_output_contract(self):
        example = BallotReflectionGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = BallotReflectionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_combination_and_power_steps_are_exact(self):
        generator = BallotReflectionGenerator()
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base 2, exponent (\d+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(2 ** int(match.group(1)), int(fields[2]))

    def test_plan_examples(self):
        self.assertEqual(Fraction(5 - 2, 5 + 2), Fraction(3, 7))
        paths = list(walk_paths(6))
        self.assertEqual(sum(path[-1] == 2 and -1 in path for path in paths), 6)
        paths = list(walk_paths(4))
        favorable = sum(path[-1] == 0 and all(value != 0 for value in path[1:-1])
                        for path in paths)
        self.assertEqual(Fraction(favorable, 16), Fraction(1, 8))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in BallotReflectionGenerator.VARIANTS:
            generator = BallotReflectionGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_ballot_reflection_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BallotReflectionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = BallotReflectionGenerator()
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
