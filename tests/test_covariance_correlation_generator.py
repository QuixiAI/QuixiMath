"""Independent prompt-only oracle for CovarianceCorrelationGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.covariance_correlation_generator import (
    QUERIES,
    CovarianceCorrelationGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        return str(value)
    places = max(twos, fives)
    scaled = value.numerator * 2 ** (places - twos) * 5 ** (places - fives)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return (sign + digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")


def raw_covariance(body, sample):
    xs = list(map(int, re.search(r"x values: ([0-9, -]+)\.", body)
                  .group(1).split(", ")))
    ys = list(map(int, re.search(r"y values: ([0-9, -]+)\.", body)
                  .group(1).split(", ")))
    assert len(xs) == len(ys)
    n = len(xs)
    x_mean, y_mean = Fraction(sum(xs), n), Fraction(sum(ys), n)
    product_sum = sum((x - x_mean) * (y - y_mean)
                      for x, y in zip(xs, ys))
    return product_sum / (n - 1 if sample else n), xs, ys


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("sample_covariance", "population_covariance",
                   "covariance_sign"):
        covariance, xs, ys = raw_covariance(
            body, variant != "population_covariance")
        if variant == "covariance_sign":
            label = "positive" if covariance > 0 else "negative"
            answer = f"{label}; cov = {exact_text(covariance)}"
        else:
            answer = exact_text(covariance)
    elif variant == "r_from_summaries":
        covariance, sx, sy = re.search(
            r"covariance = (-?[0-9./]+); sx = (\d+); sy = (\d+)", body
        ).groups()
        value = Fraction(covariance) / (int(sx) * int(sy))
        assert abs(value) <= 1
        answer = exact_text(value)
        xs = ys = None
    elif variant == "r_from_z_products":
        pairs = [(int(a), int(b)) for a, b in
                 re.findall(r"\((-?\d+), (-?\d+)\)", body)]
        value = Fraction(sum(a * b for a, b in pairs), len(pairs) - 1)
        assert abs(value) <= 1
        answer = exact_text(value)
        xs = ys = None
    else:
        value = Fraction(re.search(r"correlation between x and y is r = "
                                   r"(-?\d+(?:\.\d+)?(?:/\d+)?)",
                                   body).group(1))
        k = Fraction(re.search(r"positive-scale unit conversion with k = "
                               r"(\d+(?:\.\d+)?(?:/\d+)?)",
                               body).group(1))
        assert k > 0
        answer = f"unchanged; r = {exact_text(value)}"
        xs = ys = None
    return {"variant": variant, "query": query, "answer": answer,
            "xs": xs, "ys": ys}


class CovarianceCorrelationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310017)

    def test_output_contract(self):
        example = CovarianceCorrelationGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_800_answers_from_problem_text(self):
        generator = CovarianceCorrelationGenerator()
        for _ in range(800):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_product_rows_are_exact(self):
        generator = CovarianceCorrelationGenerator()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
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
                elif fields[0] in ("D", "MEAN_DIV"):
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ZPROD_ROW":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "REG_ROW":
                    dx = Fraction(fields[1].split("=", 1)[1])
                    dy = Fraction(fields[2].split("=", 1)[1])
                    product = Fraction(fields[3].split("=", 1)[1])
                    self.assertEqual(dx * dy, product, raw)

    def test_raw_rows_cover_every_prompt_pair(self):
        for variant in ("sample_covariance", "population_covariance",
                        "covariance_sign"):
            generator = CovarianceCorrelationGenerator(variant)
            for _ in range(200):
                example = generator.generate()
                parts = oracle_parts(example)
                rows = [raw for raw in example["steps"]
                        if raw.startswith(f"REG_ROW{DELIM}")]
                self.assertEqual(len(rows), len(parts["xs"]))

    def test_z_score_vectors_are_standardized_samples(self):
        generator = CovarianceCorrelationGenerator("r_from_z_products")
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            pairs = [(int(a), int(b)) for a, b in
                     re.findall(r"\((-?\d+), (-?\d+)\)", body)]
            for values in zip(*pairs):
                self.assertEqual(sum(values), 0)
                self.assertEqual(sum(value * value for value in values),
                                 len(values) - 1)

    def test_positive_unit_change_preserves_r_on_concrete_data(self):
        xs = [1, 2, 4, 7, 9]
        ys = [8, 3, 6, 2, 1]

        def correlation_data(a, b):
            n = len(a)
            am, bm = Fraction(sum(a), n), Fraction(sum(b), n)
            cov = sum((x - am) * (y - bm) for x, y in zip(a, b))
            va = sum((x - am) ** 2 for x in a)
            vb = sum((y - bm) ** 2 for y in b)
            return cov, va, vb

        base = correlation_data(xs, ys)
        for k, c in ((2, 5), (Fraction(2, 5), 0),
                     (Fraction(9, 5), 32)):
            transformed = [k * y + c for y in ys]
            changed = correlation_data(xs, transformed)
            self.assertEqual(changed[0] ** 2 * base[1] * base[2],
                             base[0] ** 2 * changed[1] * changed[2])
            self.assertEqual(changed[0] > 0, base[0] > 0)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in CovarianceCorrelationGenerator.VARIANTS:
            generator = CovarianceCorrelationGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_covariance_correlation_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CovarianceCorrelationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CovarianceCorrelationGenerator()
        for _ in range(350):
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
