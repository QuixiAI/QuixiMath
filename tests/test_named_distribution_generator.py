"""Prompt-only oracle for NamedDistributionGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.named_distribution_generator import QUERIES, NamedDistributionGenerator
from helpers import DELIM


VALUE = r"(?:\d+\.\d{4}|\d+/\d+)"


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
    if variant == "poisson":
        lam = int(re.search(r"Poisson with lambda=(\d+)", body).group(1))
        supplied = Fraction(re.search(rf"Supplied value: e\^\(-\d+\) = ({VALUE})", body).group(1))
        k = int(re.search(r"Target: P\(X=(\d+)\)", body).group(1))
        value = supplied * lam ** k / math.factorial(k)
        answer = f"P(X={k}) = {float(value):.4f}"
    elif variant == "exponential":
        supplied = Fraction(re.search(rf"e\^\(-lambda\*t\) = ({VALUE})", body).group(1))
        answer = f"P(X<t) = {float(1 - supplied):.4f}"
    elif variant == "uniform":
        match = re.search(r"Uniform\((-?\d+),(-?\d+)\).*Target: "
                          r"P\((-?\d+)<X<(-?\d+)\)", body)
        low, high, left, right = map(int, match.groups())
        probability = Fraction(right - left, high - low)
        mean = Fraction(low + high, 2)
        variance = Fraction((high - low) ** 2, 12)
        answer = (f"P = {ptext(probability)}; mean = {ptext(mean)}; "
                  f"variance = {ptext(variance)}")
    elif variant == "normal":
        match = re.search(r"Normal\(mu=(-?\d+), sigma=(\d+)\).*"
                          rf"Phi\((-?\d+)\) = ({VALUE}).*P\(X<(-?\d+)\)", body)
        mu, sigma, z, supplied, x_value = match.groups()
        assert (int(x_value) - int(mu)) / int(sigma) == int(z)
        answer = f"P(X<{x_value}) = {float(Fraction(supplied)):.4f}"
    elif variant == "exponential_memoryless":
        match = re.search(rf"e\^\(-lambda\*s\) = ({VALUE}); "
                          rf"e\^\(-lambda\*t\) = ({VALUE})", body)
        first, second = map(Fraction, match.groups())
        joint = first * second
        conditional = joint / first
        assert conditional == second
        value = f"{float(conditional):.4f}"
        answer = f"P(X > s+t given X > s) = {value} = P(X > t)"
    else:
        lam = Fraction(re.search(r"Poisson with lambda=(\d+(?:/\d+)?)", body).group(1))
        floor_value = lam.numerator // lam.denominator
        if lam.denominator == 1:
            answer = f"modes = {floor_value - 1} and {floor_value}"
        else:
            answer = f"mode = {floor_value}"
    return {"variant": variant, "query": query, "answer": answer}


class NamedDistributionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240765)

    def test_output_contract(self):
        example = NamedDistributionGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = NamedDistributionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_factorial_and_power_steps_are_exact(self):
        generator = NamedDistributionGenerator()
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
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (-?\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))
                elif fields[0] == "ROUND":
                    self.assertEqual(f"{float(Fraction(fields[1])):.4f}", fields[3])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in NamedDistributionGenerator.VARIANTS:
            generator = NamedDistributionGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"named_distribution_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_supplied_parser_accepts_decimal_and_fraction_forms(self):
        self.assertEqual(Fraction("0.1353"), Fraction(1353, 10000))
        self.assertEqual(Fraction("1353/10000"), Fraction(1353, 10000))
        self.assertRegex("0.1353", rf"^{VALUE}$")
        self.assertRegex("1353/10000", rf"^{VALUE}$")

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NamedDistributionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = NamedDistributionGenerator()
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
