"""Independent prompt-only oracle for HistogramConstructGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.histogram_construct_generator import (
    QUERIES,
    HistogramConstructGenerator,
)
from helpers import DELIM
from tests import stats_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for template in queries:
            pattern = re.escape(template)
            pattern = pattern.replace(r"\{value\}", r"(?P<value>\d+)")
            pattern = pattern.replace(r"\{first\}", r"(?P<first>\d+-\d+)")
            pattern = pattern.replace(r"\{last\}", r"(?P<last>\d+-\d+)")
            pattern = pattern.replace(r"\{target\}", r"(?P<target>\d+-\d+)")
            match = re.search(r"\n" + pattern + r"$", problem)
            if match:
                return (problem[:match.start()], variant, template,
                        match.groupdict())
    raise AssertionError(problem)


def _bin_map(body):
    line = next(line for line in body.splitlines()
                if line.startswith("Histogram bins: "))
    parsed = stats_oracle.parse_bins(line)
    return {f"{lo}-{hi}": count for (lo, hi), count in parsed}


def _raw_bins(body):
    values = list(map(int, re.search(r"raw [a-z ]+: ([0-9, ]+)\.", body)
                      .group(1).split(", ")))
    width, start = map(int, re.search(
        r"bins of width (\d+) starting at (\d+)", body).groups())
    indexes = [(value - start) // width for value in values]
    bins = {}
    for index in range(min(indexes), max(indexes) + 1):
        low = start + index * width
        bins[f"{low}-{low + width - 1}"] = indexes.count(index)
    return values, bins


def oracle_parts(example):
    body, variant, query, fields = split_query(example["problem"])
    if variant == "bin_counts":
        _, bins = _raw_bins(body)
        answer = "; ".join(f"{label}: {count}"
                           for label, count in bins.items())
    else:
        bins = _bin_map(body)
        labels = list(bins)
        counts = list(bins.values())
        if variant == "bin_of_value":
            value = int(fields["value"])
            answer = next(label for label in labels
                          if int(label.split("-")[0]) <= value
                          <= int(label.split("-")[1]))
        elif variant == "count_between":
            first, last = labels.index(fields["first"]), labels.index(fields["last"])
            answer = str(sum(counts[first:last + 1]))
        elif variant == "relative_bin":
            answer = str(Fraction(bins[fields["target"]], sum(counts)))
        else:
            top = max(counts)
            assert counts.count(top) == 1
            peak = counts.index(top)
            left, right = sum(counts[:peak]), sum(counts[peak + 1:])
            if right > left:
                answer = (f"right-skewed; peak in {labels[peak]}, "
                          f"tail to {labels[-1]}")
            elif left > right:
                answer = (f"left-skewed; peak in {labels[peak]}, "
                          f"tail to {labels[0]}")
            else:
                answer = (f"symmetric; peak in {labels[peak]}, equal side "
                          f"counts {left} = {right}")
    return {"variant": variant, "query": query, "answer": answer}


class HistogramConstructGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310007)

    def test_output_contract(self):
        example = HistogramConstructGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = HistogramConstructGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = HistogramConstructGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_construction_assigns_every_value_once(self):
        generator = HistogramConstructGenerator("bin_counts")
        for _ in range(200):
            example = generator.generate()
            values, bins = _raw_bins(split_query(example["problem"])[0])
            assignments = [raw for raw in example["steps"]
                           if raw.startswith(f"BIN_ASSIGN{DELIM}")]
            self.assertEqual(len(assignments), len(values))
            self.assertEqual(sum(bins.values()), len(values))

    def test_all_shape_outcomes_occur(self):
        generator = HistogramConstructGenerator("shape")
        seen = set()
        for _ in range(400):
            seen.add(generator.generate()["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"left-skewed", "right-skewed", "symmetric"})

    def test_bins_are_contiguous_equal_width_and_inclusive(self):
        generator = HistogramConstructGenerator()
        for _ in range(300):
            example = generator.generate()
            body, variant, _, _ = split_query(example["problem"])
            if variant == "bin_counts":
                values, bins = _raw_bins(body)
                self.assertTrue(values)
                labels = list(bins)
            else:
                bins = _bin_map(body)
                labels = list(bins)
            ranges = [tuple(map(int, label.split("-"))) for label in labels]
            widths = [high - low + 1 for low, high in ranges]
            self.assertEqual(len(set(widths)), 1)
            self.assertIn(widths[0], (5, 10, 20))
            self.assertTrue(all(right[0] == left[1] + 1
                                for left, right in zip(ranges, ranges[1:])))

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in HistogramConstructGenerator.VARIANTS:
            generator = HistogramConstructGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(
                    example["operation"],
                    f"statistics_histogram_construct_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HistogramConstructGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = HistogramConstructGenerator()
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
