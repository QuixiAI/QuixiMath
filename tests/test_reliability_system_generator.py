"""Independent state-enumeration oracle for ReliabilitySystemGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.reliability_system_generator import QUERIES, ReliabilitySystemGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def weighted_probability(probabilities, predicate):
    total = Fraction()
    for state in itertools.product((False, True), repeat=len(probabilities)):
        weight = Fraction(1)
        for works, probability in zip(state, probabilities):
            weight *= probability if works else 1 - probability
        if predicate(state):
            total += weight
    return total


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(
        r"Components have independent working states\. Working probabilities: "
        r"(.+?)\.(?: Design: ([a-z]+) and ([a-z]+) form a parallel block; "
        r"that block is in series with ([a-z, ]+)\.)?", body)
    assert match is not None, body
    pairs = [item.split("=") for item in match.group(1).split("; ")]
    names = tuple(item[0] for item in pairs)
    probabilities = tuple(Fraction(item[1]) for item in pairs)
    if variant == "series":
        value = weighted_probability(probabilities, all)
        answer = ptext(value)
    elif variant in ("parallel", "at_least_one_distinct"):
        value = weighted_probability(probabilities, any)
        answer = ptext(value)
    elif variant == "both":
        series = weighted_probability(probabilities, all)
        parallel = weighted_probability(probabilities, any)
        value = series
        answer = f"series {ptext(series)}; parallel {ptext(parallel)}"
    elif variant == "mixed":
        assert (match.group(2), match.group(3)) == names[:2]
        assert tuple(match.group(4).split(", ")) == names[2:]
        value = weighted_probability(
            probabilities, lambda state: (state[0] or state[1]) and all(state[2:]))
        answer = ptext(value)
    else:
        value = weighted_probability(probabilities, lambda state: sum(state) == 1)
        answer = ptext(value)
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, "names": names, "probabilities": probabilities}


class ReliabilitySystemGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(300000)

    def test_output_contract(self):
        example = ReliabilitySystemGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ReliabilitySystemGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ReliabilitySystemGenerator()
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
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "COMPLEMENT":
                    probability = Fraction(fields[2].removeprefix("1 − "))
                    self.assertEqual(1 - probability, Fraction(fields[3]))
                elif fields[0] == "SUM":
                    self.assertEqual(sum((Fraction(item) for item in
                                          fields[1].split(" + ")), Fraction()),
                                     Fraction(fields[2]))

    def test_parallel_variant_uses_identical_probabilities(self):
        generator = ReliabilitySystemGenerator("parallel")
        for _ in range(100):
            probabilities = oracle_parts(generator.generate())["probabilities"]
            self.assertEqual(len(set(probabilities)), 1)

    def test_distinct_variants_use_distinct_probabilities(self):
        for variant in ("at_least_one_distinct", "exactly_one", "mixed"):
            generator = ReliabilitySystemGenerator(variant)
            for _ in range(80):
                probabilities = oracle_parts(generator.generate())["probabilities"]
                self.assertEqual(len(set(probabilities)), len(probabilities))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ReliabilitySystemGenerator.VARIANTS:
            generator = ReliabilitySystemGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_reliability_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ReliabilitySystemGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ReliabilitySystemGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
