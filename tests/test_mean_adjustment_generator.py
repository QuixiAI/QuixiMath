"""Independent exact oracle for MeanAdjustmentGenerator prompts."""
import random
import re
import unittest
from fractions import Fraction

from generators.mean_adjustment_generator import QUERIES, MeanAdjustmentGenerator
from helpers import DELIM


def exact_text(value):
    value = Fraction(value)
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
    sign = "-" if value < 0 else ""
    scaled = abs(value.numerator) * 10 ** places // value.denominator
    if places == 0:
        return f"{sign}{scaled}"
    digits = str(scaled).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return Fraction(ordered[middle])
    return Fraction(ordered[middle - 1] + ordered[middle], 2)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "needed_score":
        count, old_mean, target = map(int, re.search(
            r"(\d+) [a-z ]+ have mean (\d+)\. The target mean after one "
            r"more value is (\d+)", body).groups())
        answer = str(target * (count + 1) - old_mean * count)
    elif variant == "add_value":
        count, old_mean, added = map(int, re.search(
            r"(\d+) [a-z ]+ have mean (\d+)\. Add the value (\d+)",
            body).groups())
        answer = exact_text(Fraction(old_mean * count + added, count + 1))
    elif variant == "remove_value":
        count, old_mean, removed = map(int, re.search(
            r"(\d+) [a-z ]+ have mean (\d+)\. Remove the value (\d+)",
            body).groups())
        answer = exact_text(Fraction(old_mean * count - removed, count - 1))
    elif variant == "combined_groups":
        count1, mean1, count2, mean2 = map(int, re.search(
            r"Group A has (\d+) values with mean (\d+); Group B has (\d+) "
            r"values with mean (\d+)", body).groups())
        answer = exact_text(Fraction(count1 * mean1 + count2 * mean2,
                                     count1 + count2))
    elif variant == "correction":
        count, reported, wrong, correct = map(int, re.search(
            r"mean of (\d+) [a-z ]+ was (\d+), but (\d+) was recorded "
            r"instead of (\d+)", body).groups())
        answer = exact_text(Fraction(reported * count - wrong + correct, count))
    else:
        values = list(map(int, re.search(r"Data values: ([0-9, ]+)\.", body)
                          .group(1).split(", ")))
        outlier = int(re.search(r"outlier (\d+)\.$", body).group(1))
        expanded = values + [outlier]
        answer = (f"mean {exact_text(Fraction(sum(values), len(values)))} → "
                  f"{exact_text(Fraction(sum(expanded), len(expanded)))}; "
                  f"median {exact_text(median(values))} → "
                  f"{exact_text(median(expanded))}")
    return {"variant": variant, "query": query, "answer": answer}


class MeanAdjustmentGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310010)

    def test_output_contract(self):
        example = MeanAdjustmentGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = MeanAdjustmentGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = MeanAdjustmentGenerator()
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

    def test_numeric_check_steps_are_exact(self):
        generator = MeanAdjustmentGenerator()
        for _ in range(350):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "CHECK":
                    continue
                if fields[1] in ("substitute", "updated total and count",
                                 "remaining mean", "combined mean"):
                    expression = fields[2].strip("()")
                    if "+" in expression:
                        numerator, denominator = expression.split("/", 1)
                        left, right = map(int, numerator.strip("()").split(" + "))
                        value = Fraction(left + right, int(denominator))
                    else:
                        numerator, denominator = expression.split("/")
                        value = Fraction(int(numerator), int(denominator))
                    self.assertEqual(value, Fraction(fields[3]), raw)
                elif fields[1] == "corrected total":
                    first, removed, added = map(
                        int, re.fullmatch(r"(\d+) - (\d+) \+ (\d+)",
                                          fields[2]).groups())
                    self.assertEqual(first - removed + added, int(fields[3]))

    def test_needed_score_is_in_valid_range(self):
        generator = MeanAdjustmentGenerator("needed_score")
        for _ in range(250):
            needed = int(generator.generate()["final_answer"])
            self.assertLessEqual(1, needed)
            self.assertLessEqual(needed, 100)

    def test_outlier_both_directions_and_mean_shifts_occur(self):
        generator = MeanAdjustmentGenerator("outlier_effect")
        directions = set()
        shifts = set()
        for _ in range(350):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            direction = re.search(r"Add the (low|high) outlier", body).group(1)
            directions.add(direction)
            before, after = re.search(r"mean ([^ ]+) → ([^;]+);",
                                      example["final_answer"]).groups()
            shifts.add("up" if Fraction(after) > Fraction(before) else "down")
        self.assertEqual(directions, {"low", "high"})
        self.assertEqual(shifts, {"up", "down"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in MeanAdjustmentGenerator.VARIANTS:
            generator = MeanAdjustmentGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_mean_adjustment_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MeanAdjustmentGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = MeanAdjustmentGenerator()
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
