"""Independent labelled-subset oracle for HypergeometricGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.hypergeometric_generator import QUERIES, HypergeometricGenerator
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


def distribution(labels, sample):
    subsets = tuple(itertools.combinations(range(len(labels)), sample))
    counts = [sum(labels[index] == "target" for index in subset)
              for subset in subsets]
    return counts, len(subsets)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "three_types":
        match = re.fullmatch(
            r"In the ([a-z]+) lot, a bag has (.+)\. A sample of (\d+) "
            r"marbles is drawn uniformly without replacement\. Target counts: (.+)\.",
            body)
        assert match is not None, body
        inventory = []
        for item in match.group(2).split("; "):
            row = re.fullmatch(r"(\d+) ([a-z]+) marbles", item)
            assert row is not None, item
            inventory.append((row.group(2), int(row.group(1))))
        sample = int(match.group(3))
        targets = {}
        for item in match.group(4).split(", "):
            row = re.fullmatch(r"(\d+) ([a-z]+)", item)
            assert row is not None, item
            targets[row.group(2)] = int(row.group(1))
        items = [(color, index) for color, count in inventory
                 for index in range(count)]
        subsets = tuple(itertools.combinations(items, sample))
        favorable = 0
        for subset in subsets:
            observed = {color: sum(item[0] == color for item in subset)
                        for color, _ in inventory}
            favorable += observed == targets
        value = Fraction(favorable, len(subsets))
        answer = ptext(value)
    else:
        match = re.fullmatch(
            r"In the ([a-z]+) lot, a ([a-z]+) has (\d+) (.+) and (\d+) (.+)\. "
            r"A sample of (\d+) items is drawn uniformly without replacement\. "
            r"Let X be the number of (.+) drawn\. Target: (.+)\.", body)
        assert match is not None, body
        target_total = int(match.group(3))
        other_total = int(match.group(5))
        sample = int(match.group(7))
        assert match.group(4) == match.group(8)
        labels = ["target"] * target_total + ["other"] * other_total
        counts, denominator = distribution(labels, sample)
        goal = match.group(9)
        if variant == "exact_k":
            cutoff = int(re.fullmatch(r"P\(X = (\d+)\)", goal).group(1))
            value = Fraction(counts.count(cutoff), denominator)
            answer = ptext(value)
        elif variant == "at_least_one":
            assert goal == "P(X ≥ 1)"
            value = Fraction(sum(count >= 1 for count in counts), denominator)
            answer = ptext(value)
        elif variant == "at_most":
            cutoff = int(re.fullmatch(r"P\(X ≤ (\d+)\)", goal).group(1))
            value = Fraction(sum(count <= cutoff for count in counts), denominator)
            answer = ptext(value)
        else:
            probabilities = {
                count: Fraction(counts.count(count), denominator)
                for count in set(counts)
            }
            mean = sum((count * probability
                        for count, probability in probabilities.items()), Fraction())
            if variant == "mean":
                assert goal == "E[X]"
                answer = f"E[X] = {ptext(mean)}"
            else:
                assert goal == "Var(X)"
                variance = sum(((Fraction(count) - mean) ** 2 * probability
                                for count, probability in probabilities.items()),
                               Fraction())
                answer = f"Var(X) = {ptext(variance)}"
    return {"variant": variant, "query": query, "answer": answer,
            "value": value if variant not in ("mean", "variance") else None}


class HypergeometricGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(613408)

    def test_output_contract(self):
        example = HypergeometricGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = HypergeometricGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_combination_steps_are_exact(self):
        generator = HypergeometricGenerator()
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
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "FRAC_BUILD":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))

    def test_probability_variants_stay_in_unit_interval(self):
        for variant in ("exact_k", "at_least_one", "at_most", "three_types"):
            generator = HypergeometricGenerator(variant)
            for _ in range(120):
                value = Fraction(generator.generate()["final_answer"])
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in HypergeometricGenerator.VARIANTS:
            generator = HypergeometricGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_hypergeometric_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HypergeometricGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = HypergeometricGenerator()
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
