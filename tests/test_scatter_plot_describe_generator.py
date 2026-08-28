"""Independent prompt-only oracle for ScatterPlotDescribeGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.scatter_plot_describe_generator import (
    QUERIES,
    ScatterPlotDescribeGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_points(text):
    return [(int(x), int(y))
            for x, y in re.findall(r"\((-?\d+), (-?\d+)\)", text)]


def agreement_count(points):
    n = len(points)
    x_mean = Fraction(sum(x for x, _ in points), n)
    y_mean = Fraction(sum(y for _, y in points), n)
    assert all(Fraction(x) != x_mean and Fraction(y) != y_mean
               for x, y in points)
    return sum((Fraction(x) - x_mean) * (Fraction(y) - y_mean) > 0
               for x, y in points)


def parse_line(body):
    intercept, sign, coefficient = re.search(
        r"Supplied line: ŷ = (-?\d+) ([+−]) (\d*)x", body
    ).groups()
    slope = int(coefficient) if coefficient else 1
    if sign == "−":
        slope = -slope
    return int(intercept), slope


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("direction", "no_association"):
        points = parse_points(body)
        agreements = agreement_count(points)
        n = len(points)
        if agreements > n / 2:
            answer = f"positive; {agreements} of {n} points agree in sign"
        elif agreements < n / 2:
            disagrees = n - agreements
            answer = (f"negative; {disagrees} of {n} points disagree in "
                      f"sign")
        else:
            answer = (f"no association; {agreements} of {n} points agree "
                      f"in sign")
    elif variant == "stronger_of_two":
        a_text, b_text = re.search(
            r"set A points are: (.+)\.\nSet B points are: (.+)\.\n"
            r"Quadrant-count rule:", body,
        ).groups()
        a_points, b_points = parse_points(a_text), parse_points(b_text)
        a_count, b_count = agreement_count(a_points), agreement_count(b_points)
        a_fraction = Fraction(a_count, len(a_points))
        b_fraction = Fraction(b_count, len(b_points))
        assert a_fraction != b_fraction
        if a_fraction > b_fraction:
            answer = (f"A; agreement {a_count}/{len(a_points)} > "
                      f"{b_count}/{len(b_points)}")
        else:
            answer = (f"B; agreement {b_count}/{len(b_points)} > "
                      f"{a_count}/{len(a_points)}")
    else:
        points = parse_points(body.split("Supplied line:")[0])
        intercept, slope = parse_line(body)
        residuals = [(abs(y - (intercept + slope * x)), x, y,
                      y - (intercept + slope * x)) for x, y in points]
        largest = max(value[0] for value in residuals)
        assert sum(value[0] == largest for value in residuals) == 1
        _, x, y, residual = max(residuals)
        answer = f"({x}, {y}); residual {residual}"
    return {"variant": variant, "query": query, "answer": answer}


class ScatterPlotDescribeGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310015)

    def test_output_contract(self):
        example = ScatterPlotDescribeGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_800_answers_from_problem_text(self):
        generator = ScatterPlotDescribeGenerator()
        for _ in range(800):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ScatterPlotDescribeGenerator()
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
                elif fields[0] in ("D", "MEAN_DIV"):
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ABS":
                    self.assertEqual(abs(Fraction(fields[1])),
                                     Fraction(fields[2]), raw)

    def test_quadrant_rows_match_prompt_points_and_mean_lines(self):
        for variant in ("direction", "no_association", "stronger_of_two"):
            generator = ScatterPlotDescribeGenerator(variant)
            for _ in range(200):
                example = generator.generate()
                body = split_query(example["problem"])[0]
                if variant == "stronger_of_two":
                    chunks = re.search(
                        r"set A points are: (.+)\.\nSet B points are: (.+)\.\n",
                        body,
                    ).groups()
                    groups = {"A": parse_points(chunks[0]),
                              "B": parse_points(chunks[1])}
                else:
                    groups = {"": parse_points(body)}
                rows = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"QUADRANT_ROW{DELIM}")]
                self.assertEqual(len(rows), sum(map(len, groups.values())))
                for label, points in groups.items():
                    x_mean = Fraction(sum(x for x, _ in points), len(points))
                    y_mean = Fraction(sum(y for _, y in points), len(points))
                    for x, y in points:
                        point_label = f"{label} ({x}, {y})".strip()
                        row = next(fields for fields in rows
                                   if fields[1] == point_label)
                        expected_signs = ("+" if x > x_mean else "−") + "," + (
                            "+" if y > y_mean else "−")
                        self.assertEqual(row[2], expected_signs)
                        expected = "agree" if (x - x_mean) * (y - y_mean) > 0 else "disagree"
                        self.assertEqual(row[3], expected)

    def test_no_association_is_exactly_half(self):
        generator = ScatterPlotDescribeGenerator("no_association")
        for _ in range(250):
            example = generator.generate()
            points = parse_points(split_query(example["problem"])[0])
            self.assertEqual(agreement_count(points) * 2, len(points))

    def test_direction_reaches_positive_and_negative_majorities(self):
        generator = ScatterPlotDescribeGenerator("direction")
        seen = set()
        for _ in range(300):
            example = generator.generate()
            seen.add(example["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"positive", "negative"})

    def test_stronger_comparison_uses_two_positive_patterns(self):
        generator = ScatterPlotDescribeGenerator("stronger_of_two")
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            a_text, b_text = re.search(
                r"set A points are: (.+)\.\nSet B points are: (.+)\.\n",
                body,
            ).groups()
            for points in (parse_points(a_text), parse_points(b_text)):
                self.assertGreater(agreement_count(points), len(points) / 2)

    def test_outlier_is_uniquely_largest_absolute_residual(self):
        generator = ScatterPlotDescribeGenerator("identify_outlier")
        for _ in range(250):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            points = parse_points(body.split("Supplied line:")[0])
            intercept, slope = parse_line(body)
            magnitudes = [abs(y - intercept - slope * x) for x, y in points]
            self.assertEqual(magnitudes.count(max(magnitudes)), 1)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in ScatterPlotDescribeGenerator.VARIANTS:
            generator = ScatterPlotDescribeGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_scatter_describe_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ScatterPlotDescribeGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ScatterPlotDescribeGenerator()
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
