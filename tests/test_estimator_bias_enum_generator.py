"""Independent enumeration oracles for EstimatorBiasEnumGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.estimator_bias_enum_generator import (
    QUERIES, EstimatorBiasEnumGenerator,
)
from helpers import DELIM


def exact(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value)
    sign = "-" if value < 0 else ""
    numerator = abs(value.numerator)
    denominator = value.denominator
    whole, remainder = divmod(numerator, denominator)
    if remainder == 0:
        return f"{sign}{whole}"
    digits = []
    while remainder:
        remainder *= 10
        digit, remainder = divmod(remainder, denominator)
        digits.append(str(digit))
    return f"{sign}{whole}.{''.join(digits)}"


def mean(values):
    return sum((Fraction(value) for value in values), Fraction(0)) / len(values)


def variance(values, denominator=None):
    center = mean(values)
    denominator = len(values) if denominator is None else denominator
    return sum((Fraction(value) - center) ** 2 for value in values) / denominator


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    population = tuple(map(int, re.search(
        r"population = \{([\d, ]+)\}", body).group(1).split(", ")))
    sample_size = int(re.search(r"size n = (\d+)", body).group(1))
    population_mean = mean(population)
    population_variance = variance(population)
    if variant == "without_replacement":
        samples = list(itertools.combinations(population, sample_size))
        statistics = [mean(sample) for sample in samples]
        expectation = sum(statistics, Fraction(0)) / len(samples)
        deviations = [(value - expectation) ** 2 for value in statistics]
        statistic_variance = sum(deviations, Fraction(0)) / len(samples)
        answer = (f"E[x̄] = {exact(expectation)}; "
                  f"bias = {exact(expectation - population_mean)}; "
                  f"Var(x̄) = {exact(statistic_variance)}")
        return {"answer": answer, "variant": variant, "query": query,
                "body": body, "population": population,
                "sample_size": sample_size, "samples": samples,
                "statistics": statistics, "expectation": expectation,
                "target": population_mean, "bias": expectation - population_mean,
                "statistic_variance": statistic_variance,
                "population_mean": population_mean,
                "population_variance": population_variance}

    samples = list(itertools.product(population, repeat=sample_size))
    if variant == "variance_n_bias":
        symbol, target_name = "σ̂²", "σ²"
        statistics = [variance(sample) for sample in samples]
        target = population_variance
    elif variant == "variance_n_minus_1_unbiased":
        symbol, target_name = "s²", "σ²"
        statistics = [variance(sample, sample_size - 1) for sample in samples]
        target = population_variance
    elif variant == "mean_unbiased":
        symbol, target_name = "x̄", "μ"
        statistics = [mean(sample) for sample in samples]
        target = population_mean
    elif variant == "max_estimator_bias":
        symbol, target_name = "max", "N"
        statistics = [Fraction(max(sample)) for sample in samples]
        target = Fraction(max(population))
    else:
        symbol, target_name = "range", "σ"
        statistics = [Fraction(max(sample) - min(sample)) for sample in samples]
        root_num = math.isqrt(population_variance.numerator)
        root_den = math.isqrt(population_variance.denominator)
        assert root_num * root_num == population_variance.numerator
        assert root_den * root_den == population_variance.denominator
        target = Fraction(root_num, root_den)
    expectation = sum(statistics, Fraction(0)) / len(samples)
    bias = expectation - target
    bias_text = "0 (unbiased)" if bias == 0 else exact(bias)
    answer = (f"E[{symbol}] = {exact(expectation)}; "
              f"{target_name} = {exact(target)}; bias = {bias_text}")
    return {"answer": answer, "variant": variant, "query": query,
            "body": body, "population": population,
            "sample_size": sample_size, "samples": samples,
            "statistics": statistics, "symbol": symbol,
            "expectation": expectation, "target": target, "bias": bias,
            "population_mean": population_mean,
            "population_variance": population_variance}


def sample_detail(parts, sample, statistic):
    symbol = parts["symbol"]
    if symbol in ("σ̂²", "s²"):
        return f"x̄ = {exact(mean(sample))}, {symbol} = {exact(statistic)}"
    return f"{symbol} = {exact(statistic)}"


class EstimatorBiasEnumGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(681504)

    def test_output_contract(self):
        example = EstimatorBiasEnumGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = EstimatorBiasEnumGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_population_moment_steps_are_exact(self):
        generator = EstimatorBiasEnumGenerator()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            dev_rows = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"DEV_ROW{DELIM}")]
            self.assertEqual(len(dev_rows), len(parts["population"]))
            for fields, value in zip(dev_rows, parts["population"]):
                self.assertEqual(int(fields[1]), value)
                left, right = fields[2].split(" - ")
                self.assertEqual(Fraction(left) - Fraction(right),
                                 Fraction(value) - parts["population_mean"])
                self.assertEqual((Fraction(left) - Fraction(right)) ** 2,
                                 Fraction(fields[3]), DELIM.join(fields))

    def test_replacement_sample_rows_are_complete_and_exact(self):
        for variant in EstimatorBiasEnumGenerator.VARIANTS[:-1]:
            generator = EstimatorBiasEnumGenerator(variant)
            for _ in range(120):
                example = generator.generate()
                parts = oracle_parts(example)
                rows = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"SAMPLE_ENUM{DELIM}")]
                self.assertEqual(len(rows), len(parts["samples"]))
                self.assertLessEqual(len(rows), 16)
                for fields, sample, statistic in zip(
                        rows, parts["samples"], parts["statistics"]):
                    self.assertEqual(fields[1],
                                     "(" + ", ".join(map(str, sample)) + ")")
                    self.assertEqual(fields[2],
                                     sample_detail(parts, sample, statistic))

    def test_without_replacement_rows_and_fpc_are_exact(self):
        generator = EstimatorBiasEnumGenerator("without_replacement")
        seen_shapes = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_shapes.add((len(parts["population"]), parts["sample_size"]))
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"SAMPLE_ENUM{DELIM}")]
            self.assertEqual(len(rows), math.comb(
                len(parts["population"]), parts["sample_size"]))
            self.assertLessEqual(len(rows), 10)
            self.assertEqual([row[1] for row in rows], [
                "(" + ", ".join(map(str, sample)) + ")"
                for sample in parts["samples"]])
            n_population = len(parts["population"])
            expected_fpc = Fraction(n_population - parts["sample_size"],
                                    n_population - 1)
            expected = (parts["population_variance"] /
                        parts["sample_size"] * expected_fpc)
            self.assertEqual(parts["statistic_variance"], expected)
            self.assertIn("Var(x̄) = σ²/n × (N-n)/(N-1)",
                          DELIM.join(example["steps"]))
        self.assertEqual(seen_shapes, {(3, 2), (3, 3), (4, 2), (5, 2)})

    def test_all_generic_arithmetic_steps_recompute(self):
        generator = EstimatorBiasEnumGenerator()
        for _ in range(600):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "SUM":
                    terms = [Fraction(value) for value in fields[1].split(" + ")]
                    self.assertEqual(sum(terms, Fraction(0)),
                                     Fraction(fields[2]), raw)
                elif fields[0] in ("MEAN_DIV", "D"):
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) ** 2,
                                     Fraction(fields[1]), raw)

    def test_bias_and_check_steps_match_independent_oracle(self):
        generator = EstimatorBiasEnumGenerator()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            bias = next(raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"BIAS{DELIM}"))
            self.assertEqual(Fraction(bias[3]), parts["bias"])
            checks = [raw.split(DELIM) for raw in example["steps"]
                      if raw.startswith(f"CHECK{DELIM}")]
            self.assertTrue(checks)
            for fields in checks:
                if " × " in fields[2]:
                    left, right = fields[2].split(" × ")
                    self.assertEqual(Fraction(left) * Fraction(right),
                                     Fraction(fields[3]), DELIM.join(fields))

    def test_range_population_sigma_is_exact(self):
        generator = EstimatorBiasEnumGenerator("range_estimator")
        seen_targets = set()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_targets.add(parts["target"])
            self.assertEqual(parts["target"] ** 2,
                             parts["population_variance"])
        self.assertEqual(seen_targets, {Fraction(5, 2), Fraction(7, 2)})

    def test_expected_bias_directions_and_unbiased_cases(self):
        negative = ("variance_n_bias", "max_estimator_bias")
        for variant in negative:
            generator = EstimatorBiasEnumGenerator(variant)
            self.assertTrue(all(oracle_parts(generator.generate())["bias"] < 0
                                for _ in range(200)))
        unbiased = ("variance_n_minus_1_unbiased", "mean_unbiased",
                    "without_replacement")
        for variant in unbiased:
            generator = EstimatorBiasEnumGenerator(variant)
            self.assertTrue(all(oracle_parts(generator.generate())["bias"] == 0
                                for _ in range(200)))

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in EstimatorBiasEnumGenerator.VARIANTS:
            generator = EstimatorBiasEnumGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_estimator_bias_enum_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EstimatorBiasEnumGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = EstimatorBiasEnumGenerator()
        for _ in range(400):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                    example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
