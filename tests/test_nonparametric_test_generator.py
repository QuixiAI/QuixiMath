"""Independent exact oracles for NonparametricTestGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.nonparametric_test_generator import (
    QUERIES, NonparametricTestGenerator,
)
from helpers import DELIM


def number(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value)
    return str(float(value)).rstrip("0").rstrip(".")


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


def binomial_upper(n, k):
    return sum((Fraction(math.comb(n, value), 2 ** n)
                for value in range(k, n + 1)), Fraction(0))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant.startswith("sign_test"):
        pairs = [tuple(map(int, match)) for match in re.findall(
            r"\((\d+), (\d+)\)", body)]
        differences = [after - before for before, after in pairs]
        assert all(differences)
        plus = sum(value > 0 for value in differences)
        n = len(differences)
        if variant == "sign_test_two_sided":
            pvalue = 2 * binomial_upper(n, max(plus, n - plus))
        else:
            pvalue = binomial_upper(n, plus)
        if variant == "sign_test_decision":
            alpha_text = re.search(
                r"Use α = (\d+(?:\.\d+)?)", body).group(1)
            alpha = Fraction(alpha_text)
            reject = pvalue < alpha
            label = "reject H0" if reject else "fail to reject H0"
            relation = "<" if reject else "≥"
            answer = (f"{label} ({probability(pvalue)} {relation} "
                      f"{alpha_text})")
        else:
            answer = probability(pvalue)
        return {"answer": answer, "variant": variant, "query": query,
                "pairs": pairs, "differences": differences, "plus": plus,
                "n": n, "pvalue": pvalue, "body": body}

    if variant == "permutation_pvalue":
        first, second = re.search(
            r"group A = ([\d, ]+) and group B = ([\d, ]+)\. The statistic",
            body).groups()
        group_a = tuple(map(int, first.split(", ")))
        group_b = tuple(map(int, second.split(", ")))
        size = len(group_a)
        values = group_a + group_b
        observed = Fraction(sum(group_a) - sum(group_b), size)
        differences = []
        for combination in itertools.combinations(range(2 * size), size):
            left = [values[index] for index in combination]
            right = [values[index] for index in range(2 * size)
                     if index not in combination]
            differences.append(Fraction(sum(left) - sum(right), size))
        extreme = sum(value >= observed for value in differences)
        pvalue = Fraction(extreme, len(differences))
        return {"answer": probability(pvalue), "variant": variant,
                "query": query, "group_a": group_a, "group_b": group_b,
                "observed": observed, "differences": differences,
                "pvalue": pvalue, "body": body}

    if variant == "bootstrap_percentile_ci":
        stats_text, low, high = re.search(
            r"20 supplied bootstrap statistics are ([\d., ]+)\. Form the "
            r"(\d+)th-to-(\d+)th percentile", body).groups()
        values = [Fraction(value) for value in stats_text.split(", ")]
        low, high = int(low), int(high)
        ordered = sorted(values)
        low_pos = math.ceil(low * len(values) / 100)
        high_pos = math.ceil(high * len(values) / 100)
        lower, upper = ordered[low_pos - 1], ordered[high_pos - 1]
        return {"answer": f"({number(lower)}, {number(upper)})",
                "variant": variant, "query": query, "values": values,
                "positions": (low_pos, high_pos), "body": body}

    first, second = re.search(
        r"group A = ([\d, ]+) and group B = ([\d, ]+)\.", body).groups()
    group_a = tuple(map(int, first.split(", ")))
    group_b = tuple(map(int, second.split(", ")))
    ordered = sorted(group_a + group_b)
    ranks = {value: rank for rank, value in enumerate(ordered, 1)}
    rank_sum = sum(ranks[value] for value in group_a)
    return {"answer": str(rank_sum), "variant": variant, "query": query,
            "group_a": group_a, "group_b": group_b, "ranks": ranks,
            "body": body}


class NonparametricTestGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(936102)

    def test_output_contract(self):
        example = NonparametricTestGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_problem_text(self):
        generator = NonparametricTestGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_sign_rows_binomial_coefficients_and_arithmetic(self):
        for variant in ("sign_test_pvalue", "sign_test_two_sided",
                        "sign_test_decision"):
            generator = NonparametricTestGenerator(variant)
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                sign_rows = [raw.split(DELIM) for raw in example["steps"]
                             if raw.startswith(f"SIGN_ROW{DELIM}")]
                self.assertEqual(len(sign_rows), parts["n"])
                self.assertEqual(sum(row[3] == "+" for row in sign_rows),
                                 parts["plus"])
                for raw in example["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] == "NCR":
                        n, k = map(int, re.fullmatch(
                            r"C\((\d+),(\d+)\)", fields[1]).groups())
                        self.assertEqual(math.comb(n, k), int(fields[2]), raw)
                    elif fields[0] == "A":
                        self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "M":
                        self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                         Fraction(fields[3]), raw)

    def test_sign_n_bank_and_decision_outcomes(self):
        generator = NonparametricTestGenerator("sign_test_pvalue")
        seen_n = {oracle_parts(generator.generate())["n"] for _ in range(900)}
        self.assertEqual(seen_n, set(range(6, 13)))
        generator = NonparametricTestGenerator("sign_test_decision")
        labels = {generator.generate()["final_answer"].split(" (")[0]
                  for _ in range(900)}
        self.assertEqual(labels, {"reject H0", "fail to reject H0"})

    def test_permutation_enumerates_all_six_or_twenty_splits(self):
        generator = NonparametricTestGenerator("permutation_pvalue")
        seen = set()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw for raw in example["steps"]
                    if raw.startswith(f"PERM_ROW{DELIM}")]
            expected = math.comb(2 * len(parts["group_a"]), len(parts["group_a"]))
            self.assertEqual(len(rows), expected)
            self.assertEqual(len(parts["differences"]), expected)
            seen.add(expected)
        self.assertEqual(seen, {6, 20})

    def test_bootstrap_nearest_ranks_and_rule(self):
        generator = NonparametricTestGenerator("bootstrap_percentile_ci")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertEqual(len(parts["values"]), 20)
            self.assertIn("Nearest-rank rule", example["problem"])
            positions = [int(raw.split(DELIM)[2]) for raw in example["steps"]
                         if raw.startswith(f"CEIL{DELIM}")]
            self.assertEqual(tuple(positions), parts["positions"])

    def test_rank_sum_has_no_ties_and_rows_match_ranks(self):
        generator = NonparametricTestGenerator("rank_sum_stat")
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            values = parts["group_a"] + parts["group_b"]
            self.assertEqual(len(values), len(set(values)))
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"RANK_ROW{DELIM}")]
            self.assertEqual(len(rows), len(values))
            for _, value, rank, group in rows:
                value, rank = int(value), int(rank)
                self.assertEqual(parts["ranks"][value], rank)
                self.assertEqual(group, "A" if value in parts["group_a"] else "B")

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in NonparametricTestGenerator.VARIANTS:
            generator = NonparametricTestGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_nonparametric_test_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NonparametricTestGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = NonparametricTestGenerator()
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
