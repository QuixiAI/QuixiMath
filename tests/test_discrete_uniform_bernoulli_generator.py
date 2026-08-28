"""Definitional-sum oracle for DiscreteUniformBernoulliGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.discrete_uniform_bernoulli_generator import (
    QUERIES, DiscreteUniformBernoulliGenerator,
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
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def moments(values):
    probability = Fraction(1, len(values))
    mean = sum((Fraction(value) * probability for value in values), Fraction())
    variance = sum(((Fraction(value) - mean) ** 2 * probability for value in values),
                   Fraction())
    return mean, variance


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "uniform_interval_prob":
        match = re.fullmatch(
            r"X is discrete uniform on the integers (-?\d+) through (-?\d+)\. "
            r"Target interval: (-?\d+) through (-?\d+)\.", body)
        assert match is not None, body
        start, end, left, right = map(int, match.groups())
        support = tuple(range(start, end + 1))
        value = Fraction(sum(left <= x <= right for x in support), len(support))
        answer = ptext(value)
    elif variant in ("uniform_moments", "uniform_shift"):
        match = re.fullmatch(
            r"X is discrete uniform on the integers (-?\d+) through (-?\d+)\."
            r"(?: Define Y = X ([+−]) (\d+)\.)?", body)
        assert match is not None, body
        start, end = int(match.group(1)), int(match.group(2))
        values = tuple(range(start, end + 1))
        if variant == "uniform_shift":
            shift = int(match.group(4)) * (1 if match.group(3) == "+" else -1)
            values = tuple(value + shift for value in values)
            mean, variance = moments(values)
            answer = f"E[Y] = {ptext(mean)}; Var(Y) = {ptext(variance)}"
        else:
            mean, variance = moments(values)
            answer = f"E[X] = {ptext(mean)}; Var(X) = {ptext(variance)}"
        value = mean
    elif variant == "bernoulli_moments":
        match = re.fullmatch(
            r"For the ([a-z]+), X is 1 on success and 0 on failure\. The "
            r"success probability is (\d+(?:/\d+)?)\.", body)
        assert match is not None, body
        probability = Fraction(match.group(2))
        mean = probability
        variance = ((0 - mean) ** 2 * (1 - probability) +
                    (1 - mean) ** 2 * probability)
        answer = f"E[X] = {ptext(mean)}; Var(X) = {ptext(variance)}"
        value = mean
    else:
        match = re.fullmatch(
            r"A fair ([a-z]+) (\d+)-sided die with faces 1 through \2 is "
            r"rolled\. I=1 when (.+), and I=0 otherwise\.", body)
        assert match is not None, body
        sides, description = int(match.group(2)), match.group(3)
        outcomes = tuple(range(1, sides + 1))
        if description == "the roll is even":
            event = [x for x in outcomes if x % 2 == 0]
        elif "at least" in description:
            cutoff = int(description.rsplit(" ", 1)[1])
            event = [x for x in outcomes if x >= cutoff]
        else:
            divisor = int(description.rsplit(" ", 1)[1])
            event = [x for x in outcomes if x % divisor == 0]
        value = Fraction(len(event), sides)
        answer = f"E[I] = {ptext(value)}"
    return {"variant": variant, "query": query, "answer": answer, "value": value}


class DiscreteUniformBernoulliGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(346410)

    def test_output_contract(self):
        example = DiscreteUniformBernoulliGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = DiscreteUniformBernoulliGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = DiscreteUniformBernoulliGenerator()
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in DiscreteUniformBernoulliGenerator.VARIANTS:
            generator = DiscreteUniformBernoulliGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_discrete_uniform_bernoulli_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DiscreteUniformBernoulliGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DiscreteUniformBernoulliGenerator()
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
