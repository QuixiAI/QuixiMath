"""Independent exact-arithmetic oracle for TIntervalGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.t_interval_generator import QUERIES, TIntervalGenerator
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


def exact_root(value):
    value = Fraction(value)
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Fraction(numerator, denominator)


def sample_sd(values):
    values = [Fraction(value) for value in values]
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return mean, exact_root(variance)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    t_text, df = re.search(r"use t\* = (\d+\.\d{3}) \(df = (\d+)\)", body).groups()
    t_star, df = Fraction(t_text), int(df)
    if variant in ("mean_t_ci", "mean_t_margin"):
        n, mean, sample_s = map(int, re.search(
            r"sample has n = (\d+), x̄ = (\d+), and sample s = (\d+)", body
        ).groups())
        root_n = math.isqrt(n)
        assert root_n * root_n == n and df == n - 1
        se = Fraction(sample_s, root_n)
        margin = t_star * se
        answer = (exact_text(margin) if variant == "mean_t_margin" else
                  f"({exact_text(mean - margin)}, {exact_text(mean + margin)})")
        case = {"n": n, "se": se}
    elif variant == "paired_from_data":
        before_text, after_text = re.search(
            r"before: ([0-9, -]+)\. after: ([0-9, -]+)\. For", body).groups()
        before = [int(value) for value in before_text.split(", ")]
        after = [int(value) for value in after_text.split(", ")]
        assert len(before) == len(after) and df == len(before) - 1
        differences = [a - b for a, b in zip(after, before)]
        mean, sd = sample_sd(differences)
        root_n = math.isqrt(len(differences))
        se = sd / root_n
        margin = t_star * se
        answer = f"({exact_text(mean - margin)}, {exact_text(mean + margin)})"
        case = {"n": len(before), "differences": differences, "se": se}
    elif variant in ("paired_from_summary", "paired_t_stat"):
        n, mean_text, sd_text = re.search(
            r"have n = (\d+), d̄ = (-?\d+(?:\.\d+)?(?:/\d+)?), and sample "
            r"sd = (\d+(?:\.\d+)?(?:/\d+)?)", body).groups()
        n, mean, sd = int(n), Fraction(mean_text), Fraction(sd_text)
        root_n = math.isqrt(n)
        assert root_n * root_n == n and df == n - 1
        se = sd / root_n
        if variant == "paired_t_stat":
            answer = exact_text(mean / se)
        else:
            margin = t_star * se
            answer = f"({exact_text(mean - margin)}, {exact_text(mean + margin)})"
        case = {"n": n, "se": se}
    else:
        groups = re.search(
            r"sample 1 has n1 = (\d+), x̄1 = (-?\d+(?:\.\d+)?), s1 = (\d+); "
            r"sample 2 has n2 = (\d+), x̄2 = (-?\d+(?:\.\d+)?), s2 = (\d+)",
            body).groups()
        n1, mean1, s1, n2, mean2, s2 = (
            int(groups[0]), Fraction(groups[1]), int(groups[2]),
            int(groups[3]), Fraction(groups[4]), int(groups[5]))
        assert df == n1 + n2 - 2
        pooled_variance = Fraction((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2,
                                   df)
        pooled_sd = exact_root(pooled_variance)
        se = pooled_sd * exact_root(Fraction(1, n1) + Fraction(1, n2))
        difference = mean1 - mean2
        if variant == "pooled_t_ci":
            margin = t_star * se
            answer = (f"({exact_text(difference - margin)}, "
                      f"{exact_text(difference + margin)})")
        else:
            statistic = difference / se
            reject = abs(statistic) > t_star
            relation = ">" if reject else "≤"
            label = "reject H0" if reject else "fail to reject H0"
            answer = (f"{label} ({exact_text(abs(statistic))} {relation} "
                      f"{t_text})")
        case = {"n": n1, "se": se, "pooled_sd": pooled_sd}
    return {"variant": variant, "query": query, "answer": answer,
            "t_text": t_text, "df": df, "case": case}


class TIntervalGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(881023)

    def test_output_contract(self):
        example = TIntervalGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = TIntervalGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_roots_and_lookups_are_exact(self):
        generator = TIntervalGenerator()
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]), raw)
                elif fields[0] == "LOOKUP_SUPPLIED":
                    self.assertIn(fields[2], example["problem"])

    def test_raw_pair_differences_and_deviation_rows_are_exact(self):
        generator = TIntervalGenerator("paired_from_data")
        seen_sizes = set()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            differences = parts["case"]["differences"]
            seen_sizes.add(len(differences))
            pair_rows = [raw.split(DELIM) for raw in example["steps"]
                         if raw.startswith(f"PAIR_DIFF{DELIM}")]
            self.assertEqual([int(row[1]) - int(row[2]) for row in pair_rows],
                             differences)
            mean = Fraction(sum(differences), len(differences))
            dev_rows = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"DEV_ROW{DELIM}")]
            for row in dev_rows:
                self.assertEqual(Fraction(row[1]) - mean, Fraction(row[2]))
                self.assertEqual(Fraction(row[2]) ** 2, Fraction(row[3]))
        self.assertEqual(seen_sizes, {4, 16})

    def test_every_lookup_prints_value_and_df(self):
        for variant in ("mean_t_ci", "mean_t_margin", "paired_from_data",
                        "paired_from_summary", "pooled_t_stat", "pooled_t_ci"):
            generator = TIntervalGenerator(variant)
            for _ in range(120):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertIn(f"t* = {parts['t_text']} (df = {parts['df']})",
                              example["problem"])
                for raw in example["steps"]:
                    if raw.startswith(f"LOOKUP_SUPPLIED{DELIM}"):
                        self.assertIn(parts["t_text"], raw)

    def test_pooled_decision_reaches_both_outcomes(self):
        generator = TIntervalGenerator("pooled_t_stat")
        labels = {generator.generate()["final_answer"].split(" (")[0]
                  for _ in range(500)}
        self.assertEqual(labels, {"reject H0", "fail to reject H0"})

    def test_all_confidence_levels_are_reachable(self):
        generator = TIntervalGenerator("mean_t_ci")
        seen = set()
        for _ in range(500):
            problem = generator.generate()["problem"]
            seen.add(int(re.search(r"For a (\d+)% procedure", problem).group(1)))
        self.assertEqual(seen, {90, 95, 99})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in TIntervalGenerator.VARIANTS:
            generator = TIntervalGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_t_interval_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TIntervalGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TIntervalGenerator()
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
