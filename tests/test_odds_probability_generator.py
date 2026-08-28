"""Independent odds/probability conversion oracle."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.odds_probability_generator import OddsProbabilityGenerator, QUERIES
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


def odds_for(value):
    left, right = value, 1 - value
    a = left.numerator * right.denominator
    b = right.numerator * left.denominator
    divisor = math.gcd(a, b)
    return f"{a // divisor}:{b // divisor}"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("prob_to_odds_for", "prob_to_odds_against",
                   "odds_of_complement"):
        match = re.fullmatch(r"For event A \(.+\), P\(A\) = (.+)\.", body)
        assert match is not None, body
        value = Fraction(match.group(1))
        if variant == "prob_to_odds_for":
            answer = odds_for(value)
        else:
            answer = odds_for(1 - value)
    elif variant == "odds_to_prob":
        match = re.fullmatch(r"The odds in favor of event A are (\d+):(\d+)\.", body)
        assert match is not None, body
        first, second = map(int, match.groups())
        answer = ptext(Fraction(first, first + second))
    else:
        match = re.fullmatch(
            r"Observed outcome counts are ([a-z]+)=(\d+); ([a-z]+)=(\d+)\. "
            r"Focus outcome: \1\.", body)
        assert match is not None, body
        first, second = int(match.group(2)), int(match.group(4))
        divisor = math.gcd(first, second)
        answer = f"{first // divisor}:{second // divisor}"
    return {"variant": variant, "query": query, "answer": answer}


class OddsProbabilityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(173205)

    def test_output_contract(self):
        example = OddsProbabilityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = OddsProbabilityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_odds_are_reduced_and_probability_steps_are_exact(self):
        generator = OddsProbabilityGenerator()
        for _ in range(300):
            example = generator.generate()
            answer = example["final_answer"]
            if ":" in answer:
                first, second = map(int, answer.split(":"))
                self.assertEqual(math.gcd(first, second), 1)
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "PROB_SETUP":
                    self.assertEqual(Fraction(int(fields[1]), int(fields[2])),
                                     Fraction(answer))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in OddsProbabilityGenerator.VARIANTS:
            generator = OddsProbabilityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"probability_odds_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            OddsProbabilityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = OddsProbabilityGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
