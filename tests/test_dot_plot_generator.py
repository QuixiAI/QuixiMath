"""Independent dot-row parsing oracle for DotPlotGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.dot_plot_generator import QUERIES, DotPlotGenerator
from helpers import DELIM
from tests import stats_oracle


def ntext(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    if value.denominator in (2, 4, 5, 8, 10):
        text = f"{float(value):.8f}".rstrip("0").rstrip(".")
        return text
    return str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for template in queries:
            pattern = re.escape(template)
            pattern = pattern.replace(r"\{target\}", r"(?P<target>-?\d+)")
            pattern = pattern.replace(r"\{threshold\}", r"(?P<threshold>-?\d+)")
            pattern = pattern.replace(r"\{relation\}", r"(?P<relation>above|below)")
            match = re.search(r"\n" + pattern + r"$", problem)
            if match:
                return problem[:match.start()], variant, template, match.groupdict()
    raise AssertionError(problem)


def display_counts(body):
    rows = [line for line in body.splitlines() if "∣" in line]
    return stats_oracle.parse_dot_plot("\n".join(rows))


def oracle_parts(example):
    body, variant, query, fields = split_query(example["problem"])
    if variant == "construct":
        raw = re.search(r"raw [a-z ]+ are: ([0-9, ]+)\.$", body).group(1)
        values = list(map(int, raw.split(", ")))
        counts = {value: values.count(value)
                  for value in range(min(values), max(values) + 1)}
        answer = "; ".join(f"{value}: {count}"
                           for value, count in counts.items())
    else:
        counts = display_counts(body)
        values = [value for value in counts for _ in range(counts[value])]
        if variant == "read_count":
            answer = str(counts[int(fields["target"])])
        elif variant == "count_above_below":
            threshold = int(fields["threshold"])
            if fields["relation"] == "above":
                answer = str(sum(count for value, count in counts.items()
                                 if value > threshold))
            else:
                answer = str(sum(count for value, count in counts.items()
                                 if value < threshold))
        elif variant == "most_common":
            top = max(counts.values())
            assert list(counts.values()).count(top) == 1
            mode = next(value for value, count in counts.items() if count == top)
            answer = f"{mode} ({top} observations)"
        elif variant == "range_from_plot":
            answer = str(max(values) - min(values))
        elif variant == "total_from_plot":
            answer = str(sum(values))
        else:
            ordered = sorted(values)
            middle = len(ordered) // 2
            median = (Fraction(ordered[middle]) if len(ordered) % 2 else
                      Fraction(ordered[middle - 1] + ordered[middle], 2))
            answer = ntext(median)
    return {"variant": variant, "query": query, "answer": answer}


class DotPlotGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310002)

    def test_output_contract(self):
        example = DotPlotGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = DotPlotGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = DotPlotGenerator()
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
                elif fields[0] == "MEAN_DIV":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_display_rows_are_contiguous_and_include_gaps(self):
        generator = DotPlotGenerator("read_count")
        saw_gap = False
        for _ in range(250):
            counts = display_counts(split_query(generator.generate()["problem"])[0])
            self.assertEqual(list(counts), list(range(min(counts), max(counts) + 1)))
            saw_gap |= 0 in counts.values()
        self.assertTrue(saw_gap)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in DotPlotGenerator.VARIANTS:
            generator = DotPlotGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_dot_plot_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DotPlotGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DotPlotGenerator()
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
