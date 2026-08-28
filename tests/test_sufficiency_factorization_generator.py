"""Independent factorization oracles for SufficiencyFactorizationGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.sufficiency_factorization_generator import (
    QUERIES, SufficiencyFactorizationGenerator,
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


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_data(text):
    return tuple(map(int, re.search(r"\[([\d, ]+)\]", text).group(1).split(", ")))


def family_from_body(body):
    if "Bernoulli(p)" in body:
        return "bernoulli", None
    if "Poisson(λ)" in body:
        return "poisson", None
    if "Exponential(rate λ)" in body:
        return "exponential", None
    if "Geometric(p)" in body:
        return "geometric", None
    if "Normal(μ, known σ²" in body:
        variance = int(re.search(r"known σ² = (\d+)", body).group(1))
        return "normal_mu", variance
    if "Uniform(0, θ)" in body:
        return "uniform", None
    return "normal_two", None


def evaluated_factor(family, data, variance=None):
    n = len(data)
    total = sum(data)
    if family == "bernoulli":
        return f"p^{total}(1-p)^{n - total}", "1"
    if family == "poisson":
        product = math.prod(math.factorial(value) for value in data)
        return f"λ^{total} e^(-{n}λ)", exact(Fraction(1, product))
    if family == "exponential":
        return f"λ^{n} e^(-{total}λ)", "1"
    if family == "geometric":
        return f"p^{n}(1-p)^{total - n}", "1"
    if family == "normal_mu":
        sum_squares = sum(value ** 2 for value in data)
        return (f"exp[μ·{total}/{variance} - {n}μ²/(2·{variance})]",
                f"(2π·{variance})^(-{n}/2) "
                f"exp[-{sum_squares}/(2·{variance})]")
    maximum = max(data)
    return f"θ^(-{n}) 1({maximum} ≤ θ)", "1"


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "ratio_check":
        first_text, second_text = re.search(
            r"samples are x = \[([\d, ]+)\] and y = \[([\d, ]+)\]",
            body).groups()
        first = tuple(map(int, first_text.split(", ")))
        second = tuple(map(int, second_text.split(", ")))
        first_t, second_t = sum(first), sum(second)
        assert first_t == second_t
        return {"body": body, "variant": variant, "query": query,
                "first": first, "second": second, "statistic": first_t,
                "answer": f"ratio = 1; T(x) = T(y) = {first_t}"}

    family, variance = family_from_body(body)
    data = parse_data(body)
    statistic = stats_oracle.sufficient_statistic(family, data)
    if variant == "identify_T":
        if family == "uniform":
            answer = f"T = max x_i = {int(statistic)}"
        elif family == "normal_two":
            answer = (f"T = (Σx_i, Σx_i²) = "
                      f"({int(statistic[0])}, {int(statistic[1])})")
        else:
            answer = f"T = Σx_i = {int(statistic)}"
    elif variant == "two_dimensional":
        total, sum_squares = map(int, statistic)
        n = len(data)
        g = (f"(2πσ²)^(-{n}/2) exp[-({sum_squares} - "
             f"2μ·{total} + {n}μ²)/(2σ²)]")
        answer = (f"T = (Σx_i, Σx_i²) = ({total}, {sum_squares}); "
                  f"g = {g}; h = 1")
    else:
        g, h = evaluated_factor(family, data, variance)
        if family == "uniform":
            t_text = f"T = max x_i = {int(statistic)}"
        else:
            t_text = f"T = Σx_i = {int(statistic)}"
        answer = f"{t_text}; g = {g}; h = {h}"
    return {"body": body, "variant": variant, "query": query,
            "family": family, "variance": variance, "data": data,
            "statistic": statistic, "answer": answer}


class SufficiencyFactorizationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(407126)

    def test_output_contract(self):
        example = SufficiencyFactorizationGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = SufficiencyFactorizationGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_identify_variant_covers_all_seven_family_statistics(self):
        generator = SufficiencyFactorizationGenerator("identify_T")
        seen = set()
        for _ in range(900):
            example = generator.generate()
            parts = oracle_parts(example)
            seen.add(parts["family"])
            sufficient = next(raw.split(DELIM) for raw in example["steps"]
                              if raw.startswith(f"SUFFICIENT{DELIM}"))
            if parts["family"] == "normal_two":
                expected = f"({int(parts['statistic'][0])}, {int(parts['statistic'][1])})"
            else:
                expected = str(int(parts["statistic"]))
            self.assertEqual(sufficient[2], expected)
        self.assertEqual(seen, {"bernoulli", "poisson", "exponential",
                                "geometric", "normal_mu", "uniform",
                                "normal_two"})

    def test_factor_variant_covers_six_one_parameter_families(self):
        generator = SufficiencyFactorizationGenerator("factor_and_evaluate")
        seen = set()
        for _ in range(900):
            example = generator.generate()
            parts = oracle_parts(example)
            seen.add(parts["family"])
            factors = [raw.split(DELIM) for raw in example["steps"]
                       if raw.startswith(f"LIKELIHOOD_FACTOR{DELIM}")]
            self.assertEqual(len(factors), 2)
            g, h = evaluated_factor(parts["family"], parts["data"],
                                    parts["variance"])
            self.assertEqual(factors[-1][1:], [f"g = {g}", f"h = {h}"])
        self.assertEqual(seen, {"bernoulli", "poisson", "exponential",
                                "geometric", "normal_mu", "uniform"})

    def test_poisson_factorial_product_is_explicit_and_exact(self):
        generator = SufficiencyFactorizationGenerator("factor_and_evaluate")
        checked = 0
        while checked < 180:
            example = generator.generate()
            parts = oracle_parts(example)
            if parts["family"] != "poisson":
                continue
            checked += 1
            factorials = [raw.split(DELIM) for raw in example["steps"]
                          if raw.startswith(f"FACTORIAL{DELIM}")]
            self.assertEqual(len(factorials), len(parts["data"]))
            for fields, value in zip(factorials, parts["data"]):
                self.assertEqual(int(fields[1]), value)
                self.assertEqual(int(fields[2]), math.factorial(value))
            products = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"M{DELIM}")]
            self.assertEqual(len(products), len(parts["data"]))
            self.assertEqual(int(products[-1][3]),
                             math.prod(math.factorial(v) for v in parts["data"]))

    def test_two_dimensional_sums_and_squares_are_explicit(self):
        generator = SufficiencyFactorizationGenerator("two_dimensional")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"E{DELIM}")]
            self.assertEqual(len(rows), len(parts["data"]))
            for fields, value in zip(rows, parts["data"]):
                self.assertEqual(int(fields[1]), value)
                self.assertEqual(int(fields[1]) ** int(fields[2]),
                                 int(fields[3]))
            self.assertEqual(parts["statistic"],
                             (sum(parts["data"]),
                              sum(value ** 2 for value in parts["data"])))

    def test_ratio_check_uses_distinct_samples_with_same_T(self):
        generator = SufficiencyFactorizationGenerator("ratio_check")
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertNotEqual(parts["first"], parts["second"])
            self.assertEqual(sum(parts["first"]), sum(parts["second"]))
            ratio = next(raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"LIKELIHOOD_RATIO{DELIM}"))
            self.assertEqual(ratio[2], "1")
            self.assertNotIn("p", ratio[2])

    def test_generic_arithmetic_steps_recompute(self):
        generator = SufficiencyFactorizationGenerator()
        for _ in range(600):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "SUM":
                    values = [int(value) for value in fields[1].split(" + ")]
                    self.assertEqual(sum(values), int(fields[2]), raw)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw)

    def test_all_variants_and_four_queries_are_reachable(self):
        for variant in SufficiencyFactorizationGenerator.VARIANTS:
            generator = SufficiencyFactorizationGenerator(variant)
            seen = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(example["operation"],
                                 f"statistics_sufficiency_factorization_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SufficiencyFactorizationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SufficiencyFactorizationGenerator()
        for _ in range(500):
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
