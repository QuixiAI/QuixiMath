"""Independent prompt-only oracle for GeometricDistributionGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.geometric_distribution_generator import (
    QUERIES, GeometricDistributionGenerator,
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


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    p = Fraction(re.search(r"probability p=(\d+/\d+)", body).group(1))
    q = 1 - p
    target = re.search(r"Target: (.+)\.$", body).group(1)
    if variant == "exact_k":
        k = int(re.fullmatch(r"P\(X=(\d+)\)", target).group(1))
        probability = p
        for _ in range(k - 1):
            probability *= q
        answer = ptext(probability)
    elif variant == "at_most":
        k = int(re.fullmatch(r"P\(X≤(\d+)\)", target).group(1))
        fail_all = Fraction(1)
        for _ in range(k):
            fail_all *= q
        answer = ptext(1 - fail_all)
    elif variant == "after_k":
        k = int(re.fullmatch(r"P\(X>(\d+)\)", target).group(1))
        probability = Fraction(1)
        for _ in range(k):
            probability *= q
        answer = ptext(probability)
    elif variant == "mean":
        answer = ptext(Fraction(1, 1) / (1 - q))
    elif variant in ("memoryless_verify", "conditional_tail"):
        match = re.fullmatch(r"P\(X>(\d+) given X>(\d+)\)", target)
        later, earlier = map(int, match.groups())
        probability = q ** later / q ** earlier
        if variant == "memoryless_verify":
            answer = (f"P(X > {later} given X > {earlier}) = "
                      f"{ptext(probability)} = P(X > {later - earlier})")
        else:
            answer = ptext(probability)
    else:
        match = re.fullmatch(r"E\[X-(\d+) given X>(\d+)\]", target)
        self_elapsed, given_elapsed = map(int, match.groups())
        assert self_elapsed == given_elapsed
        answer = (f"E[X - {self_elapsed} given X > {self_elapsed}] = "
                  f"{ptext(1 / p)}")
    return {"variant": variant, "query": query, "answer": answer}


class GeometricDistributionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240764)

    def test_output_contract(self):
        example = GeometricDistributionGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = GeometricDistributionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = GeometricDistributionGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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

    def test_probability_variants_stay_in_unit_interval(self):
        variants = ("exact_k", "at_most", "after_k", "conditional_tail")
        for variant in variants:
            generator = GeometricDistributionGenerator(variant)
            for _ in range(100):
                value = Fraction(generator.generate()["final_answer"])
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in GeometricDistributionGenerator.VARIANTS:
            generator = GeometricDistributionGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"geometric_distribution_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GeometricDistributionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = GeometricDistributionGenerator()
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
