"""Independent fraction-row parsing oracle for FractionLinePlotGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.fraction_line_plot_generator import (
    QUERIES, FractionLinePlotGenerator,
)
from helpers import DELIM
from tests import stats_oracle


def mixed_text(value):
    value = Fraction(value)
    whole, rem = divmod(value.numerator, value.denominator)
    if rem == 0:
        return str(whole)
    if whole == 0:
        return f"{rem}/{value.denominator}"
    return f"{whole} {rem}/{value.denominator}"


def parse_mixed(text):
    if " " in text:
        whole, fraction = text.split()
        return int(whole) + Fraction(fraction)
    return Fraction(text)


def split_query(problem):
    number = r"\d+(?: \d+/\d+|/\d+)?"
    for variant, queries in QUERIES.items():
        for template in queries:
            pattern = re.escape(template)
            pattern = pattern.replace(r"\{threshold\}",
                                      rf"(?P<threshold>{number})")
            pattern = pattern.replace(r"\{plural\}", r"(?P<plural>[a-z]+)")
            match = re.search(r"\n" + pattern + r"$", problem)
            if match:
                return problem[:match.start()], variant, template, match.groupdict()
    raise AssertionError(problem)


def plot_data(body):
    rows = [line for line in body.splitlines() if "∣" in line]
    counts = stats_oracle.parse_line_plot("\n".join(rows))
    values = [value for value in counts for _ in range(counts[value])]
    return counts, values


def measure_answer(value, body):
    plural = re.search(r"plot of [a-z ]+ in ([a-z]+) ", body).group(1)
    singular = {"inches": "inch", "feet": "foot", "meters": "meter",
                "yards": "yard"}[plural]
    return f"{mixed_text(value)} {singular if value == 1 else plural}"


def oracle_parts(example):
    body, variant, query, fields = split_query(example["problem"])
    counts, values = plot_data(body)
    if variant == "count_at_least":
        threshold = parse_mixed(fields["threshold"])
        answer = str(sum(count for value, count in counts.items()
                         if value >= threshold))
    elif variant == "longest_minus_shortest":
        answer = measure_answer(max(values) - min(values), body)
    elif variant == "total_length":
        answer = measure_answer(sum(values, Fraction()), body)
    else:
        answer = measure_answer(sum(values, Fraction()) / len(values), body)
    return {"variant": variant, "query": query, "answer": answer}


class FractionLinePlotGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310003)

    def test_output_contract(self):
        example = FractionLinePlotGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = FractionLinePlotGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = FractionLinePlotGenerator()
        for _ in range(350):
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

    def test_rows_are_evenly_spaced_and_reduced(self):
        generator = FractionLinePlotGenerator()
        saw_mixed = False
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            counts, _ = plot_data(body)
            keys = list(counts)
            if len(keys) > 1:
                unit = keys[1] - keys[0]
                self.assertTrue(all(right - left == unit
                                    for left, right in zip(keys, keys[1:])))
            saw_mixed |= any(value > 1 and value.denominator > 1 for value in keys)
        self.assertTrue(saw_mixed)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in FractionLinePlotGenerator.VARIANTS:
            generator = FractionLinePlotGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_fraction_line_plot_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FractionLinePlotGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = FractionLinePlotGenerator()
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
