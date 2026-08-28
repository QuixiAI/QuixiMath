"""Independent branch-enumeration oracle for TreeDiagramProbabilityGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.tree_diagram_probability_generator import (
    QUERIES, TreeDiagramProbabilityGenerator,
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
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_roster(text):
    return tuple(int(item) for item in text[1:-1].split(", "))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("different_colors", "same_color", "with_replacement"):
        match = re.fullmatch(
            r"A bag has (\d+) ([a-z]+) and (\d+) ([a-z]+) marbles\. Draw "
            r"two (with replacement|without replacement)\. Use A for \2 and "
            r"B for \4\. Event A: the two colors (differ|match)\.", body)
        assert match is not None, body
        a, b = int(match.group(1)), int(match.group(3))
        replacement = match.group(5) == "with replacement"
        favorable = set()
        branches = {}
        total = a + b
        for first, first_n in (("A", a), ("B", b)):
            for second, second_n in (("A", a), ("B", b)):
                numerator = second_n if replacement else second_n - (first == second)
                branches[first + second] = (Fraction(first_n, total) *
                                             Fraction(numerator, total if replacement else total - 1))
        if match.group(6) == "differ":
            favorable = {"AB", "BA"}
        else:
            favorable = {"AA", "BB"}
        value = sum((branches[label] for label in favorable), Fraction())
    elif variant == "exactly_one":
        match = re.fullmatch(
            r"Two independent stages have success counts (\d+)/(\d+) and "
            r"(\d+)/(\d+)\. Event A: exactly one stage succeeds\. Use S for "
            r"success and F for failure\.", body)
        assert match is not None, body
        a, b, c, d = map(int, match.groups())
        p, q = Fraction(a, b), Fraction(c, d)
        value = p * (1 - q) + (1 - p) * q
    elif variant == "three_coins_exactly_two_heads":
        match = re.fullmatch(
            r"Flip the ([a-z]+), ([a-z]+), and ([a-z]+) coins in that order\. "
            r"Event A: exactly two heads\.", body)
        assert match is not None, body
        outcomes = tuple(itertools.product("HT", repeat=3))
        value = Fraction(sum(bits.count("H") == 2 for bits in outcomes), len(outcomes))
    else:
        match = re.fullmatch(
            r"Spin equal sectors (\{[^{}]+\}), then flip a fair coin\. Event "
            r"A: a (odd|even) sector and heads\. Branch labels write sector "
            r"then coin face\.", body)
        assert match is not None, body
        sectors = parse_roster(match.group(1))
        parity = 1 if match.group(2) == "odd" else 0
        value = Fraction(sum(sector % 2 == parity for sector in sectors),
                         2 * len(sectors))
    return {"variant": variant, "query": query, "answer": ptext(value),
            "value": value}


class TreeDiagramProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(264575)

    def test_output_contract(self):
        example = TreeDiagramProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = TreeDiagramProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_branch_products_and_sums_are_exact(self):
        generator = TreeDiagramProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "TREE_BRANCH":
                    factors = [Fraction(item) for item in fields[2].split(" × ")]
                    product = Fraction(1)
                    for factor in factors:
                        product *= factor
                    self.assertEqual(product, Fraction(fields[3]))
                elif fields[0] == "BRANCH_SUM":
                    values = [Fraction(item) for item in fields[2].split(" + ")]
                    self.assertEqual(sum(values, Fraction()), Fraction(fields[3]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in TreeDiagramProbabilityGenerator.VARIANTS:
            generator = TreeDiagramProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_tree_diagram_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TreeDiagramProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TreeDiagramProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
