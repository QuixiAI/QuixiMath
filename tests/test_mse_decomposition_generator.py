"""Independent exact oracles for MSEDecompositionGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.mse_decomposition_generator import (
    QUERIES, MSEDecompositionGenerator,
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


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def scaled(mu, sigma2, n, coefficient):
    var_mean = Fraction(sigma2, n)
    expectation = coefficient * mu
    bias = expectation - mu
    variance = coefficient ** 2 * var_mean
    return {"var_mean": var_mean, "expectation": expectation,
            "bias": bias, "variance": variance,
            "mse": variance + bias ** 2}


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    parts = {"body": body, "variant": variant, "query": query}
    if variant == "mse_from_parts":
        bias, variance = map(Fraction, re.search(
            r"has bias = ([-\d./]+) and Var\(T\) = ([-\d./]+)\.",
            body).groups())
        mse = variance + bias ** 2
        parts.update(bias=bias, variance=variance, mse=mse,
                     answer=f"bias = {exact(bias)}; Var = {exact(variance)}; "
                            f"MSE = {exact(mse)}")
    elif variant == "mse_scaled_mean":
        n, mu, sigma2, coefficient = re.search(
            r"n = (\d+) observations with μ = (\d+) and σ² = (\d+)\. "
            r"For T = \(([-\d/]+)\)·x̄", body).groups()
        n, mu, sigma2 = int(n), int(mu), int(sigma2)
        coefficient = Fraction(coefficient)
        result = scaled(mu, sigma2, n, coefficient)
        parts.update(mu=mu, sigma2=sigma2, n=n, coefficient=coefficient,
                     **result,
                     answer=f"bias = {exact(result['bias'])}; "
                            f"Var = {exact(result['variance'])}; "
                            f"MSE = {exact(result['mse'])}")
    elif variant == "compare_two":
        mu, sigma2, n, first, second = re.search(
            r"μ = (\d+), σ² = (\d+), and n = (\d+)\. Compare T1 = "
            r"\(([-\d/]+)\)·x̄ with T2 = \(([-\d/]+)\)·x̄\.", body).groups()
        mu, sigma2, n = int(mu), int(sigma2), int(n)
        first, second = Fraction(first), Fraction(second)
        first_parts = scaled(mu, sigma2, n, first)
        second_parts = scaled(mu, sigma2, n, second)
        assert first_parts["mse"] != second_parts["mse"]
        if first_parts["mse"] < second_parts["mse"]:
            winner, low, high = "T1", first_parts["mse"], second_parts["mse"]
        else:
            winner, low, high = "T2", second_parts["mse"], first_parts["mse"]
        parts.update(mu=mu, sigma2=sigma2, n=n, first=first, second=second,
                     first_parts=first_parts, second_parts=second_parts,
                     winner=winner, low=low, high=high,
                     answer=f"{winner}; MSE {exact(low)} < {exact(high)}")
    elif variant == "optimal_shrinkage":
        mu, sigma2, n = map(int, re.search(
            r"x̄ has μ = (\d+), σ² = (\d+), and n = (\d+)\.",
            body).groups())
        var_mean = Fraction(sigma2, n)
        coefficient = Fraction(mu ** 2, 1) / (mu ** 2 + var_mean)
        result = scaled(mu, sigma2, n, coefficient)
        parts.update(mu=mu, sigma2=sigma2, n=n, coefficient=coefficient,
                     **result,
                     answer=f"c* = {exact(coefficient)}; "
                            f"MSE(c*) = {exact(result['mse'])}")
    else:
        endpoint = int(re.search(r"with N = (\d+)\.", body).group(1))
        samples = list(itertools.product(range(1, endpoint + 1), repeat=2))
        statistics = [Fraction(max(sample)) for sample in samples]
        expectation = sum(statistics, Fraction(0)) / len(samples)
        bias = expectation - endpoint
        variance = sum((value - expectation) ** 2 for value in statistics) / len(samples)
        mse = sum((value - endpoint) ** 2 for value in statistics) / len(samples)
        parts.update(endpoint=endpoint, samples=samples, statistics=statistics,
                     expectation=expectation, bias=bias, variance=variance,
                     mse=mse,
                     answer=f"bias = {exact(bias)}; Var = {exact(variance)}; "
                            f"MSE = {exact(mse)}")
    return parts


class MSEDecompositionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(842016)

    def test_output_contract(self):
        example = MSEDecompositionGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = MSEDecompositionGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_generic_arithmetic_steps_are_exact(self):
        generator = MSEDecompositionGenerator()
        for _ in range(700):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "SUM":
                    values = [Fraction(value) for value in fields[1].split(" + ")]
                    self.assertEqual(sum(values, Fraction(0)),
                                     Fraction(fields[2]), raw)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_from_parts_uses_supplied_bias_and_variance(self):
        generator = MSEDecompositionGenerator("mse_from_parts")
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertEqual(parts["mse"],
                             parts["variance"] + parts["bias"] ** 2)
            self.assertIn("MSE(T) = Var(T) + bias(T)²",
                          DELIM.join(example["steps"]))

    def test_scaled_mean_rows_match_closed_form(self):
        generator = MSEDecompositionGenerator("mse_scaled_mean")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            row = next(raw.split(DELIM) for raw in example["steps"]
                       if raw.startswith(f"MSE_ROW{DELIM}"))
            self.assertEqual(row, ["MSE_ROW", "T",
                                   f"bias = {exact(parts['bias'])}",
                                   f"Var = {exact(parts['variance'])}",
                                   f"MSE = {exact(parts['mse'])}"])

    def test_compare_two_computes_both_and_both_winners_occur(self):
        generator = MSEDecompositionGenerator("compare_two")
        winners = set()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            winners.add(parts["winner"])
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"MSE_ROW{DELIM}")]
            self.assertEqual([row[1] for row in rows], ["T1", "T2"])
            check = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"CHECK{DELIM}smaller MSE"))
            left, right = map(Fraction, check[2].split(" < "))
            self.assertLess(left, right)
            self.assertEqual(check[3], parts["winner"])
        self.assertEqual(winners, {"T1", "T2"})

    def test_optimal_coefficient_and_minimum_identity(self):
        generator = MSEDecompositionGenerator("optimal_shrinkage")
        for _ in range(300):
            parts = oracle_parts(generator.generate())
            expected_c = Fraction(parts["mu"] ** 2, 1) / (
                parts["mu"] ** 2 + parts["var_mean"])
            expected_mse = (parts["mu"] ** 2 * parts["var_mean"] /
                            (parts["mu"] ** 2 + parts["var_mean"]))
            self.assertEqual(parts["coefficient"], expected_c)
            self.assertEqual(parts["mse"], expected_mse)

    def test_enumerated_max_rows_and_direct_mse(self):
        generator = MSEDecompositionGenerator("enumerated_mse")
        seen_endpoints = set()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_endpoints.add(parts["endpoint"])
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"SAMPLE_ENUM{DELIM}")]
            self.assertEqual(len(rows), parts["endpoint"] ** 2)
            self.assertLessEqual(len(rows), 16)
            for row, sample, statistic in zip(
                    rows, parts["samples"], parts["statistics"]):
                error = statistic - parts["endpoint"]
                self.assertEqual(row[1],
                                 "(" + ", ".join(map(str, sample)) + ")")
                self.assertEqual(row[2], f"T = {exact(statistic)}")
                self.assertEqual(row[3], f"T - N = {exact(error)}")
                self.assertEqual(row[4], f"(T - N)² = {exact(error ** 2)}")
            self.assertEqual(parts["mse"],
                             parts["variance"] + parts["bias"] ** 2)
        self.assertEqual(seen_endpoints, {3, 4})

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in MSEDecompositionGenerator.VARIANTS:
            generator = MSEDecompositionGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_mse_decomposition_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MSEDecompositionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MSEDecompositionGenerator()
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
