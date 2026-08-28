"""Independent inclusive-bin oracle for GroupedDataGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.grouped_data_generator import QUERIES, GroupedDataGenerator
from helpers import DELIM
from tests import stats_oracle


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
    scaled = abs(value.numerator) * 10 ** places // value.denominator
    sign = "-" if value < 0 else ""
    if places == 0:
        return f"{sign}{scaled}"
    digits = str(scaled).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def percent_text(value):
    return exact_text(Fraction(value) * 100) + "%"


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_table(body):
    line = next(line for line in body.splitlines()
                if line.startswith("Grouped frequencies: "))
    rows = stats_oracle.parse_bins(line)
    labels = [f"{low}-{high}" for (low, high), _ in rows]
    ranges = [interval for interval, _ in rows]
    frequencies = [frequency for _, frequency in rows]
    return labels, ranges, frequencies


def median_class(frequencies):
    halfway = Fraction(sum(frequencies), 2)
    cumulative = 0
    for index, frequency in enumerate(frequencies):
        before = cumulative
        cumulative += frequency
        if cumulative >= halfway:
            return index, before, cumulative, halfway
    raise AssertionError(frequencies)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    labels, ranges, frequencies = parse_table(body)
    total = sum(frequencies)
    if variant == "mean_from_midpoints":
        midpoints = [Fraction(low + high, 2) for low, high in ranges]
        answer = exact_text(sum(midpoint * frequency
                                for midpoint, frequency in
                                zip(midpoints, frequencies)) / total)
    elif variant == "modal_class":
        top = max(frequencies)
        assert frequencies.count(top) == 1
        index = frequencies.index(top)
        answer = f"{labels[index]}; frequency {top}"
    elif variant == "median_class":
        index, _, cumulative, halfway = median_class(frequencies)
        answer = (f"{labels[index]}; cumulative {cumulative} ≥ "
                  f"{exact_text(halfway)}")
    elif variant == "estimated_median":
        index, before, _, halfway = median_class(frequencies)
        low, high = ranges[index]
        width = high - low + 1
        estimate = (Fraction(low)
                    + (halfway - before) / frequencies[index] * width)
        answer = exact_text(estimate)
    else:
        target = re.search(r"Target class: (\d+-\d+)\.", body).group(1)
        index = labels.index(target)
        answer = (f"total {total}; {target}: "
                  f"{percent_text(Fraction(frequencies[index], total))}")
    return {"variant": variant, "query": query, "answer": answer}


class GroupedDataGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310012)

    def test_output_contract(self):
        example = GroupedDataGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = GroupedDataGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_midpoint_rows_are_exact(self):
        generator = GroupedDataGenerator()
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
                elif fields[0] == "MID_ROW":
                    label = fields[1]
                    low, high = map(int, label.split("-"))
                    self.assertEqual(Fraction(fields[2]),
                                     Fraction(low + high, 2), raw)
                    body = split_query(example["problem"])[0]
                    labels, _, frequencies = parse_table(body)
                    frequency = frequencies[labels.index(label)]
                    self.assertEqual(Fraction(fields[2]) * frequency,
                                     Fraction(fields[3]), raw)

    def test_cumulative_rows_match_display(self):
        for variant in ("median_class", "estimated_median"):
            generator = GroupedDataGenerator(variant)
            for _ in range(250):
                example = generator.generate()
                labels, _, frequencies = parse_table(
                    split_query(example["problem"])[0])
                running = 0
                for raw in example["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] == "CUM_ROW":
                        index = labels.index(fields[1])
                        running = sum(frequencies[:index + 1])
                        self.assertEqual(int(fields[2]), running, raw)

    def test_modal_class_is_unique(self):
        generator = GroupedDataGenerator("modal_class")
        for _ in range(250):
            _, _, frequencies = parse_table(
                split_query(generator.generate()["problem"])[0])
            self.assertEqual(frequencies.count(max(frequencies)), 1)

    def test_estimated_median_rule_is_stated_and_answer_terminates(self):
        generator = GroupedDataGenerator("estimated_median")
        for _ in range(250):
            example = generator.generate()
            self.assertIn("Estimated-median rule:", example["problem"])
            self.assertNotIn("/", example["final_answer"])
            rule = next(raw for raw in example["steps"]
                        if raw.startswith(f"RULE{DELIM}"))
            self.assertIn("n/2 - CF before", rule)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in GroupedDataGenerator.VARIANTS:
            generator = GroupedDataGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_grouped_data_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GroupedDataGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = GroupedDataGenerator()
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
