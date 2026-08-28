"""Independent supplied-table oracle for PValueGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.p_value_generator import QUERIES, PValueGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exact_root(value):
    value = Fraction(value)
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def parse_case(body):
    prefix, table_line = body.splitlines()
    tail = re.search(r"\((right|left|two)-tailed\)", prefix).group(1)
    table = {Fraction(z): Fraction(value) for z, value in re.findall(
        r"z=(\d+\.\d{2}): (0\.\d{4})", table_line)}
    direct = re.search(r"Data: z = (-?\d+\.\d{2})", prefix)
    if direct:
        z = Fraction(direct.group(1))
        kind = "direct"
    elif "one-proportion" in prefix:
        n, successes = map(int, re.search(
            r"Data: n = (\d+), successes = (\d+)", prefix).groups())
        null = Fraction(re.search(r"H0: p = (\d+(?:/\d+)?)", prefix).group(1))
        se = exact_root(null * (1 - null) / n)
        z = (Fraction(successes, n) - null) / se
        kind = "proportion"
    else:
        null = int(re.search(r"H0: μ = (\d+)", prefix).group(1))
        n, xbar, sigma = re.search(
            r"Data: n = (\d+), x̄ = (\d+(?:\.\d+)?), population σ = (\d+)",
            prefix).groups()
        n, xbar, sigma = int(n), Fraction(xbar), int(sigma)
        root_n = math.isqrt(n)
        assert root_n * root_n == n
        z = (xbar - null) / Fraction(sigma, root_n)
        kind = "mean"
    return {"prefix": prefix, "tail": tail, "z": z, "table": table,
            "kind": kind}


def pvalue(case):
    magnitude = abs(case["z"])
    assert magnitude in case["table"], (magnitude, case["table"])
    upper = 1 - case["table"][magnitude]
    return 2 * upper if case["tail"] == "two" else upper


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    case = parse_case(body)
    value = pvalue(case)
    if variant == "decision_alpha":
        alpha_text = re.search(r"decide at α = (\d+(?:\.\d+)?)",
                               case["prefix"]).group(1)
        alpha = Fraction(alpha_text)
        if value < alpha:
            answer = f"reject H0 (p = {float(value):.4f} < {alpha_text})"
        else:
            answer = (f"fail to reject H0 (p = {float(value):.4f} "
                      f"≥ {alpha_text})")
    elif variant == "compare_alphas":
        assert Fraction(1, 100) <= value < Fraction(1, 20)
        answer = f"reject at 0.05, fail at 0.01; p = {float(value):.4f}"
    else:
        answer = f"{float(value):.4f}"
    return {"variant": variant, "query": query, "answer": answer,
            "value": value, **case}


class PValueGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(631027)

    def test_output_contract(self):
        example = PValueGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = PValueGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_data_variants_recompute_the_printed_z_independently(self):
        for variant, kind in (("from_prop_data", "proportion"),
                              ("from_mean_data", "mean")):
            generator = PValueGenerator(variant)
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["kind"], kind)
                z_rows = [raw.split(DELIM) for raw in example["steps"]
                          if raw.startswith(f"D{DELIM}")]
                self.assertEqual(Fraction(z_rows[-1][3]), parts["z"])

    def test_arithmetic_roots_and_lookups_are_exact(self):
        generator = PValueGenerator()
        for _ in range(500):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]), raw)
                elif fields[0] == "TABLE_LOOKUP":
                    self.assertIn(fields[2], example["problem"])

    def test_each_table_has_one_needed_row_and_two_decoys(self):
        generator = PValueGenerator()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertEqual(len(parts["table"]), 3)
            self.assertIn(abs(parts["z"]), parts["table"])
            lookups = [raw for raw in example["steps"]
                       if raw.startswith(f"TABLE_LOOKUP{DELIM}")]
            self.assertEqual(len(lookups), 1)

    def test_decision_variant_reaches_both_conclusions(self):
        generator = PValueGenerator("decision_alpha")
        labels = {generator.generate()["final_answer"].split(" (")[0]
                  for _ in range(500)}
        self.assertEqual(labels, {"reject H0", "fail to reject H0"})

    def test_compare_alphas_always_straddles_the_p_value(self):
        generator = PValueGenerator("compare_alphas")
        for _ in range(400):
            parts = oracle_parts(generator.generate())
            self.assertGreaterEqual(parts["value"], Fraction(1, 100))
            self.assertLess(parts["value"], Fraction(1, 20))

    def test_direct_variants_cover_the_full_z_magnitude_grid(self):
        generator = PValueGenerator("right_tail")
        seen = {oracle_parts(generator.generate())["z"] for _ in range(1800)}
        self.assertEqual(seen, {Fraction(k, 10) for k in range(5, 35)})

    def test_data_variants_reach_all_three_tail_rules(self):
        for variant in ("from_prop_data", "from_mean_data"):
            generator = PValueGenerator(variant)
            seen = {oracle_parts(generator.generate())["tail"]
                    for _ in range(400)}
            self.assertEqual(seen, {"right", "left", "two"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in PValueGenerator.VARIANTS:
            generator = PValueGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_p_value_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PValueGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PValueGenerator()
        for _ in range(400):
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
