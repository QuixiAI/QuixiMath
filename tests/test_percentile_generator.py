"""Independent exact oracle for PercentileGenerator prompts."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.percentile_generator import QUERIES, PercentileGenerator
from helpers import DELIM


CONTEXT_RANGES = {
    "quiz scores": (5, 20),
    "plant heights": (8, 40),
    "commute times": (15, 60),
    "battery lifetimes": (6, 40),
    "package weights": (200, 600),
    "daily sales": (20, 90),
    "daily rainfall": (2, 30),
    "ages": (8, 60),
    "shoe sizes": (5, 13),
    "points per game": (4, 30),
    "reading minutes": (10, 60),
    "pencil lengths": (2, 8),
}


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_data(body):
    values = re.search(r"distinct [a-z -]+ are: ([0-9, ]+)\.", body).group(1)
    return list(map(int, values.split(", ")))


def parse_context(body):
    match = re.search(r"distinct ([a-z -]+) are:", body)
    return match.group(1)


def nearest_position(size, percentile):
    return math.ceil(Fraction(size * percentile, 100))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    values = parse_data(body)
    ordered = sorted(values)
    if variant in ("percentile_rank", "interpret"):
        target = int(re.search(r"Target value: (\d+)\.", body).group(1))
        below = sum(value < target for value in values)
        percent = Fraction(100 * below, len(values))
        assert percent.denominator == 1
        if variant == "percentile_rank":
            answer = f"{percent.numerator}%"
        else:
            answer = (f"above {percent.numerator}% of the group; rank "
                      f"{below + 1} of {len(values)}")
    elif variant == "value_at_percentile":
        percentile = int(re.search(r"Requested percentile: (\d+)%", body)
                         .group(1))
        answer = str(ordered[nearest_position(len(values), percentile) - 1])
    elif variant == "quartiles_by_rank":
        q1 = ordered[nearest_position(len(values), 25) - 1]
        q3 = ordered[nearest_position(len(values), 75) - 1]
        answer = f"Q1 = {q1}; Q3 = {q3}"
    else:
        lower, upper = map(int, re.search(
            r"Lower percentile: (\d+)%\. Upper percentile: (\d+)%", body
        ).groups())
        first = nearest_position(len(values), lower)
        last = nearest_position(len(values), upper)
        answer = str(last - first + 1)
    return {"variant": variant, "query": query, "answer": answer}


class PercentileGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310013)

    def test_output_contract(self):
        example = PercentileGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PercentileGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_ceil_steps_are_exact(self):
        generator = PercentileGenerator()
        for _ in range(450):
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
                elif fields[0] == "CEIL":
                    value = Fraction(fields[1])
                    expected = -((-value.numerator) // value.denominator)
                    self.assertEqual(int(fields[2]), expected, raw)

    def test_data_are_distinct_and_sorted_step_is_complete(self):
        generator = PercentileGenerator()
        for _ in range(300):
            example = generator.generate()
            values = parse_data(split_query(example["problem"])[0])
            self.assertEqual(len(values), len(set(values)))
            sort = next(raw for raw in example["steps"]
                        if raw.startswith(f"SORT{DELIM}"))
            self.assertEqual(list(map(int, sort.split(DELIM)[1].split(","))),
                             sorted(values))

    def test_values_stay_within_the_stated_context_range(self):
        generator = PercentileGenerator()
        for _ in range(500):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            values = parse_data(body)
            low, high = CONTEXT_RANGES[parse_context(body)]
            self.assertTrue(all(low <= value <= high for value in values))

    def test_percentile_ranks_are_whole_percents(self):
        for variant in ("percentile_rank", "interpret"):
            generator = PercentileGenerator(variant)
            for _ in range(250):
                example = generator.generate()
                body = split_query(example["problem"])[0]
                values = parse_data(body)
                target = int(re.search(r"Target value: (\d+)", body).group(1))
                percent = Fraction(100 * sum(value < target for value in values),
                                   len(values))
                self.assertEqual(percent.denominator, 1)

    def test_rule_is_stated_for_every_variant(self):
        for variant in PercentileGenerator.VARIANTS:
            generator = PercentileGenerator(variant)
            for _ in range(50):
                example = generator.generate()
                self.assertRegex(example["problem"],
                                 r"(?:Percentile-rank|Nearest-rank) rule:")
                self.assertTrue(any(raw.startswith(f"RULE{DELIM}")
                                    for raw in example["steps"]))

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in PercentileGenerator.VARIANTS:
            generator = PercentileGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_percentile_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PercentileGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PercentileGenerator()
        for _ in range(300):
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
