"""Printed-table oracle for NormalApproxBinomialGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.normal_approx_binomial_generator import (
    QUERIES, NormalApproxBinomialGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_base(body):
    match = re.fullmatch(
        r"At the (.+) in ([A-Za-z]+), X counts (.+) in (\d+) independent trials "
        r"with success probability p = (\d+(?:/\d+)?)\. Target: (.+?)\."
        r"(?: Use a normal approximation with continuity correction\. (Standard .+))?",
        body)
    assert match is not None, body
    table = {z: Fraction(value) for z, value in
             re.findall(r"z=(\d+\.\d{2}): (0\.\d{4})", match.group(7) or "")}
    return int(match.group(4)), Fraction(match.group(5)), match.group(6), table


def cdf_from_table(z, table):
    magnitude = f"{float(abs(z)):.2f}"
    assert magnitude in table, (magnitude, table)
    return table[magnitude] if z >= 0 else 1 - table[magnitude]


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    n, p, goal, table = parse_base(body)
    mean = n * p
    variance = mean * (1 - p)
    sigma = math.isqrt(variance.numerator)
    assert variance.denominator == 1 and sigma * sigma == variance
    if variant == "check_conditions":
        successes, failures = mean, n * (1 - p)
        ok = successes >= 10 and failures >= 10
        rs, rf = ("≥" if successes >= 10 else "<",
                  "≥" if failures >= 10 else "<")
        answer = (f"{'ok' if ok else 'fails'}; np = {successes} {rs} 10, "
                  f"n(1 − p) = {failures} {rf} 10")
    elif variant == "mean_sd":
        answer = f"mean {mean}; sd {sigma}"
    elif variant == "at_most":
        cutoff = int(re.fullmatch(r"P\(X ≤ (\d+)\)", goal).group(1))
        z = (Fraction(2 * cutoff + 1, 2) - mean) / sigma
        answer = f"{float(cdf_from_table(z, table)):.4f}"
    elif variant == "at_least":
        cutoff = int(re.fullmatch(r"P\(X ≥ (\d+)\)", goal).group(1))
        z = (Fraction(2 * cutoff - 1, 2) - mean) / sigma
        answer = f"{float(1 - cdf_from_table(z, table)):.4f}"
    elif variant == "exactly":
        cutoff = int(re.fullmatch(r"P\(X = (\d+)\)", goal).group(1))
        z1 = (Fraction(2 * cutoff - 1, 2) - mean) / sigma
        z2 = (Fraction(2 * cutoff + 1, 2) - mean) / sigma
        answer = f"{float(cdf_from_table(z2, table) - cdf_from_table(z1, table)):.4f}"
    else:
        match = re.fullmatch(r"P\((\d+) ≤ X ≤ (\d+)\)", goal)
        assert match is not None, goal
        lower, upper = map(int, match.groups())
        z1 = (Fraction(2 * lower - 1, 2) - mean) / sigma
        z2 = (Fraction(2 * upper + 1, 2) - mean) / sigma
        answer = f"{float(cdf_from_table(z2, table) - cdf_from_table(z1, table)):.4f}"
    return {"variant": variant, "query": query, "answer": answer,
            "n": n, "p": p, "goal": goal, "table": table}


def exact_binomial_probability(n, p, goal):
    q = 1 - p
    exact_match = re.fullmatch(r"P\(X = (\d+)\)", goal)
    at_most = re.fullmatch(r"P\(X ≤ (\d+)\)", goal)
    at_least = re.fullmatch(r"P\(X ≥ (\d+)\)", goal)
    between = re.fullmatch(r"P\((\d+) ≤ X ≤ (\d+)\)", goal)
    if exact_match:
        indices = (int(exact_match.group(1)),)
    elif at_most:
        indices = range(0, int(at_most.group(1)) + 1)
    elif at_least:
        indices = range(int(at_least.group(1)), n + 1)
    else:
        indices = range(int(between.group(1)), int(between.group(2)) + 1)
    return sum((Fraction(math.comb(n, index)) * p ** index * q ** (n - index)
                for index in indices), Fraction())


class NormalApproxBinomialGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(295041)

    def test_output_contract(self):
        example = NormalApproxBinomialGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text_and_table(self):
        generator = NormalApproxBinomialGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_approximation_is_close_to_exact_binomial(self):
        for variant in ("at_most", "at_least", "exactly", "between"):
            generator = NormalApproxBinomialGenerator(variant)
            for _ in range(15):
                example = generator.generate()
                parts = oracle_parts(example)
                exact_value = exact_binomial_probability(parts["n"], parts["p"],
                                                         parts["goal"])
                self.assertLessEqual(abs(float(exact_value)
                                         - float(example["final_answer"])), 0.02,
                                     example["problem"])

    def test_arithmetic_roots_and_lookups_are_exact_and_supplied(self):
        generator = NormalApproxBinomialGenerator()
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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]))
                elif fields[0] == "TABLE_LOOKUP":
                    z = fields[1][2:-1]
                    self.assertIn(f"z={z}: {fields[2]}", example["problem"])

    def test_condition_variant_reaches_pass_and_fail(self):
        generator = NormalApproxBinomialGenerator("check_conditions")
        seen = set()
        for _ in range(200):
            seen.add(generator.generate()["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"ok", "fails"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in NormalApproxBinomialGenerator.VARIANTS:
            generator = NormalApproxBinomialGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_normal_approx_binomial_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NormalApproxBinomialGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = NormalApproxBinomialGenerator()
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
