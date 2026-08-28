"""Independent enumeration oracle for BayesMultipleHypothesesGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.bayes_multiple_hypotheses_generator import (
    QUERIES, BayesMultipleHypothesesGenerator,
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


def parse_priors(text):
    priors = {}
    for item in text.split("; "):
        label, value = item.split("=")
        priors[label] = Fraction(value)
    assert sum(priors.values(), Fraction()) == 1
    return priors


def parse_urn_body(body):
    match = re.fullmatch(
        r"Urns: (.+)\. Priors: (.+)\. One urn is chosen and retained\. "
        r"Draws are with replacement\. Observations: ([a-z, ]+)\. Target: (.+)\.",
        body)
    assert match is not None, body
    inventories = {}
    for item in match.group(1).split("; "):
        row = re.fullmatch(
            r"(U\d+) has (\d+) ([a-z]+) and (\d+) ([a-z]+)", item)
        assert row is not None, item
        label, n1, color1, n2, color2 = row.groups()
        inventories[label] = {color1: int(n1), color2: int(n2)}
    priors = parse_priors(match.group(2))
    observations = tuple(match.group(3).split(", "))
    return inventories, priors, observations, match.group(4)


def enumerated_urn_likelihood(counts, observations):
    scale = math.gcd(*counts.values())
    balls = []
    for color, count in counts.items():
        balls.extend((color, index) for index in range(count // scale))
    outcomes = itertools.product(balls, repeat=len(observations))
    favorable = sum(tuple(ball[0] for ball in outcome) == observations
                    for outcome in outcomes)
    return Fraction(favorable, len(balls) ** len(observations))


def posterior_distribution(priors, likelihoods):
    weights = {label: priors[label] * likelihoods[label] for label in priors}
    evidence = sum(weights.values(), Fraction())
    return {label: value / evidence for label, value in weights.items()}


def reduced_odds(first, second):
    ratio = Fraction(first, second)
    return f"{ratio.numerator}:{ratio.denominator}"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "coin_identification":
        match = re.fullmatch(
            r"Coins: (.+)\. Priors: (.+)\. One coin is chosen and retained\. "
            r"Tosses: ([HT, ]+)\. Target: P\((C\d+) given ([HT, ]+)\)\.",
            body)
        assert match is not None, body
        biases = {}
        for item in match.group(1).split("; "):
            row = re.fullmatch(r"(C\d+) has P\(H\)=(\d+(?:/\d+)?)", item)
            assert row is not None, item
            biases[row.group(1)] = Fraction(row.group(2))
        priors = parse_priors(match.group(2))
        observations = tuple(match.group(3).split(", "))
        assert observations == tuple(match.group(5).split(", "))
        target = match.group(4)
        likelihoods = {}
        for label, bias in biases.items():
            # Enumerate the biased toss tree and retain exactly the stated path.
            total = Fraction()
            for path in itertools.product(("H", "T"), repeat=len(observations)):
                if path != observations:
                    continue
                weight = Fraction(1)
                for symbol in path:
                    weight *= bias if symbol == "H" else 1 - bias
                total += weight
            likelihoods[label] = total
        posteriors = posterior_distribution(priors, likelihoods)
        answer = ptext(posteriors[target])
    else:
        inventories, priors, observations, target_text = parse_urn_body(body)
        likelihoods = {label: enumerated_urn_likelihood(counts, observations)
                       for label, counts in inventories.items()}
        posteriors = posterior_distribution(priors, likelihoods)
        if variant in ("three_hypotheses", "four_hypotheses"):
            target = re.fullmatch(r"P\((U\d+) given [a-z]+\)", target_text)
            assert target is not None, target_text
            answer = ptext(posteriors[target.group(1)])
        elif variant == "all_posteriors":
            assert target_text == f"all posterior probabilities given {observations[0]}"
            answer = "; ".join(
                f"P({label} given {observations[0]}) = {ptext(posteriors[label])}"
                for label in priors)
        elif variant == "posterior_odds":
            odds_match = re.fullmatch(
                r"posterior odds (U\d+):(U\d+) given [a-z]+", target_text)
            assert odds_match is not None, target_text
            first, second = odds_match.groups()
            answer = (f"posterior odds {first}:{second} = "
                      f"{reduced_odds(posteriors[first], posteriors[second])}")
        else:
            target = re.fullmatch(r"P\((U\d+) given [a-z]+, [a-z]+\)",
                                  target_text)
            assert target is not None, target_text
            label = target.group(1)
            first_likelihoods = {
                urn: enumerated_urn_likelihood(counts, observations[:1])
                for urn, counts in inventories.items()
            }
            first = posterior_distribution(priors, first_likelihoods)
            answer = (f"P({label} given {observations[0]}) = {ptext(first[label])}; "
                      f"P({label} given {', '.join(observations)}) = "
                      f"{ptext(posteriors[label])}")
    return {"variant": variant, "query": query, "answer": answer}


class BayesMultipleHypothesesGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(914275)

    def test_output_contract(self):
        example = BayesMultipleHypothesesGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = BayesMultipleHypothesesGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_bayes_terms_are_exact(self):
        generator = BayesMultipleHypothesesGenerator()
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "BAYES_TERM":
                    factors = [Fraction(value) for value in fields[2].split(" × ")]
                    self.assertEqual(factors[0] * factors[1], Fraction(fields[3]))

    def test_each_update_normalizes_all_posteriors(self):
        generator = BayesMultipleHypothesesGenerator()
        for _ in range(250):
            example = generator.generate()
            current = []
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "BAYES_STAGE":
                    current = []
                elif fields[0] == "POSTERIOR":
                    current.append(Fraction(fields[3]))
                elif fields[0] == "CHECK" and fields[1] == "posteriors sum":
                    self.assertEqual(sum(current, Fraction()), 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in BayesMultipleHypothesesGenerator.VARIANTS:
            generator = BayesMultipleHypothesesGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(
                    example["operation"], f"probability_bayes_multiple_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BayesMultipleHypothesesGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = BayesMultipleHypothesesGenerator()
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
