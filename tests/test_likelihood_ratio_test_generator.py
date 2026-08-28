"""Independent exact oracles for LikelihoodRatioTestGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.likelihood_ratio_test_generator import (
    QUERIES, LikelihoodRatioTestGenerator,
)
from helpers import DELIM
from tests import stats_oracle


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


def probability(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    parts = {"body": body, "variant": variant, "query": query}
    if variant == "np_ratio_bernoulli":
        n, successes, p0, p1 = re.search(
            r"n = (\d+) Bernoulli trials produced S = (\d+) successes\. "
            r"Test simple H0: p = ([\d/]+) against simple H1: p = ([\d/]+)",
            body).groups()
        n, successes = int(n), int(successes)
        p0, p1 = Fraction(p0), Fraction(p1)
        failures = n - successes
        ratio = (p0 ** successes * (1 - p0) ** failures /
                 (p1 ** successes * (1 - p1) ** failures))
        parts.update(n=n, successes=successes, p0=p0, p1=p1,
                     ratio=ratio, answer=probability(ratio))
    elif variant == "np_region":
        n, target = re.search(
            r"Binomial\(n = (\d+), p = 1/2\).*α0 = ([\d/]+)\.",
            body).groups()
        n, target = int(n), Fraction(target)
        tails = {cutoff: stats_oracle.binomial_tail(
            n, cutoff, Fraction(1, 2)) for cutoff in range(n + 1)}
        cutoff = min(value for value in range(n + 1)
                     if tails[value] <= target)
        alpha = tails[cutoff]
        parts.update(n=n, target=target, cutoff=cutoff, alpha=alpha,
                     previous=tails[cutoff - 1],
                     answer=f"c = {cutoff}; α = {probability(alpha)}")
    elif variant == "np_power":
        n, cutoff, parameter = re.search(
            r"n = (\d+) rejects when S ≥ (\d+)\. At the alternative p1 = "
            r"([\d/]+)", body).groups()
        n, cutoff, parameter = int(n), int(cutoff), Fraction(parameter)
        power = stats_oracle.binomial_tail(n, cutoff, parameter)
        parts.update(n=n, cutoff=cutoff, parameter=parameter, power=power,
                     answer=probability(power))
    elif variant == "wilks_normal":
        sigma, n, sample_mean, null_mean, critical = re.search(
            r"σ = (\d+), n = (\d+), and x̄ = (\d+)\. Test H0: μ = "
            r"(\d+).*χ² critical value = ([\d.]+) \(df = 1\)",
            body).groups()
        sigma, n = int(sigma), int(n)
        sample_mean, null_mean = int(sample_mean), int(null_mean)
        critical = Fraction(critical)
        statistic = Fraction(n * (sample_mean - null_mean) ** 2, sigma ** 2)
        reject = statistic > critical
        relation = ">" if reject else "≤"
        verdict = "reject H0" if reject else "fail to reject H0"
        parts.update(sigma=sigma, n=n, sample_mean=sample_mean,
                     null_mean=null_mean, critical=critical,
                     statistic=statistic, verdict=verdict, relation=relation,
                     answer=f"-2 ln Λ = {exact(statistic)}; {verdict} "
                            f"({exact(statistic)} {relation} {exact(critical)})")
    else:
        unrestricted, null = map(int, re.search(
            r"unrestricted model has (\d+) free parameters and its null "
            r"submodel has (\d+) free parameters", body).groups())
        degrees = unrestricted - null
        parts.update(unrestricted=unrestricted, null=null, degrees=degrees,
                     answer=f"df = {degrees}; {unrestricted} - {null}")
    return parts


def expected_tail_rows(n, cutoff, p):
    rows = []
    for successes in range(cutoff, n + 1):
        term = (math.comb(n, successes) * p ** successes *
                (1 - p) ** (n - successes))
        rows.append((successes, term))
    return rows


class LikelihoodRatioTestGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(316825)

    def test_output_contract(self):
        example = LikelihoodRatioTestGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = LikelihoodRatioTestGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_np_ratio_is_exact_and_n_is_bounded(self):
        generator = LikelihoodRatioTestGenerator("np_ratio_bernoulli")
        seen_n = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            seen_n.add(parts["n"])
            self.assertLessEqual(parts["n"], 6)
            division = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"D{DELIM}")][-1]
            self.assertEqual(Fraction(division[1]) / Fraction(division[2]),
                             parts["ratio"])
            self.assertEqual(Fraction(division[3]), parts["ratio"])
        self.assertEqual(seen_n, {3, 4, 5, 6})

    def test_np_region_enumerates_tail_and_proves_smallest_cutoff(self):
        generator = LikelihoodRatioTestGenerator("np_region")
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"TAIL_ROW{DELIM}")]
            expected = expected_tail_rows(parts["n"], parts["cutoff"],
                                          Fraction(1, 2))
            self.assertEqual([(int(row[1]), Fraction(row[2])) for row in rows],
                             expected)
            self.assertLessEqual(parts["alpha"], parts["target"])
            self.assertGreater(parts["previous"], parts["target"])
            self.assertEqual(sum(term for _, term in expected), parts["alpha"])

    def test_np_power_enumerates_exact_alternative_tail(self):
        generator = LikelihoodRatioTestGenerator("np_power")
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"TAIL_ROW{DELIM}")]
            expected = expected_tail_rows(parts["n"], parts["cutoff"],
                                          parts["parameter"])
            self.assertEqual([(int(row[1]), Fraction(row[2])) for row in rows],
                             expected)
            self.assertEqual(sum(term for _, term in expected), parts["power"])

    def test_all_arithmetic_and_combinations_recompute(self):
        generator = LikelihoodRatioTestGenerator()
        for _ in range(700):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "NCR":
                    n, k = map(int, re.fullmatch(
                        r"C\((\d+),(\d+)\)", fields[1]).groups())
                    self.assertEqual(math.comb(n, k), int(fields[2]), raw)
                elif fields[0] == "SUM":
                    terms = [Fraction(value) for value in fields[1].split(" + ")]
                    self.assertEqual(sum(terms, Fraction(0)),
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

    def test_wilks_normal_has_both_verdicts_and_supplied_cutoff(self):
        generator = LikelihoodRatioTestGenerator("wilks_normal")
        verdicts = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            verdicts.add(parts["verdict"])
            lookup = next(raw.split(DELIM) for raw in example["steps"]
                          if raw.startswith(f"LOOKUP_SUPPLIED{DELIM}"))
            self.assertEqual(lookup[2], "3.841")
            self.assertIn("3.841 (df = 1)", example["problem"])
            check = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"CHECK{DELIM}-2 ln Λ"))
            self.assertEqual(check[3], parts["verdict"])
        self.assertEqual(verdicts, {"reject H0", "fail to reject H0"})

    def test_wilks_df_is_parameter_difference(self):
        generator = LikelihoodRatioTestGenerator("wilks_df")
        seen = set()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            seen.add(parts["degrees"])
            self.assertEqual(parts["degrees"],
                             parts["unrestricted"] - parts["null"])
            self.assertGreater(parts["degrees"], 0)
        self.assertEqual(seen, {1, 2, 3, 4})

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in LikelihoodRatioTestGenerator.VARIANTS:
            generator = LikelihoodRatioTestGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_likelihood_ratio_test_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LikelihoodRatioTestGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = LikelihoodRatioTestGenerator()
        for _ in range(500):
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
