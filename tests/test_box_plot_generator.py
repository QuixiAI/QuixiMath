"""Independent fixed-column box-plot oracle for BoxPlotGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.box_plot_generator import QUERIES, BoxPlotGenerator
from helpers import DELIM
from tests import stats_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_plots(body):
    lines = body.splitlines()
    start = next(index for index, line in enumerate(lines)
                 if line.startswith("Scale: "))
    end = start + 2
    while end < len(lines) and re.match(r"^(?:Plot|A|B):", lines[end]):
        end += 1
    return stats_oracle.parse_box_plot("\n".join(lines[start:end]))


def shape(summary):
    minimum, q1, median, q3, maximum = summary
    left_whisker, right_whisker = q1 - minimum, maximum - q3
    if left_whisker != right_whisker:
        if right_whisker > left_whisker:
            return ("right-skewed",
                    f"right whisker {right_whisker} > left whisker {left_whisker}")
        return ("left-skewed",
                f"left whisker {left_whisker} > right whisker {right_whisker}")
    left_box, right_box = median - q1, q3 - median
    if right_box > left_box:
        return ("right-skewed",
                f"right box half {right_box} > left box half {left_box}")
    if left_box > right_box:
        return ("left-skewed",
                f"left box half {left_box} > right box half {right_box}")
    return ("symmetric",
            f"whiskers {left_whisker} = {right_whisker}; box halves "
            f"{left_box} = {right_box}")


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "from_description":
        match = re.search(r"min=(\d+), Q1=(\d+), median=(\d+), Q3=(\d+), "
                          r"max=(\d+)", body)
        minimum, q1, median, q3, maximum = map(int, match.groups())
        answer = f"IQR = {q3 - q1}; range = {maximum - minimum}"
    else:
        plots = parse_plots(body)
        labels = [label for label in plots if label != "scale"]
        if variant == "compare_two":
            target = re.search(r"Compare target: (median|IQR)", body).group(1)
            values = {}
            for label in labels:
                row = plots[label]
                values[label] = (row["median"] if target == "median" else
                                 row["q3"] - row["q1"])
            winner = max(values, key=values.get)
            answer = (f"{winner}; {target} {values[winner]} > "
                      f"{min(values.values())}")
        else:
            row = plots[labels[0]]
            summary = (row["min"], row["q1"], row["median"], row["q3"],
                       row["max"])
            if variant == "read_summary":
                answer = (f"min = {summary[0]}, Q1 = {summary[1]}, "
                          f"median = {summary[2]}, Q3 = {summary[3]}, "
                          f"max = {summary[4]}")
            elif variant == "iqr_from_plot":
                answer = str(summary[3] - summary[1])
            elif variant == "percent_region":
                region = re.search(r"Target region: (.+)\.", body).group(1)
                percent = {"Q1 to max": 75, "min to median": 50,
                           "median to max": 50, "Q1 to Q3": 50,
                           "min to Q3": 75}[region]
                answer = f"{percent}%"
            elif variant == "shape":
                label, witness = shape(summary)
                answer = f"{label}; {witness}"
            else:
                answer = "outliers: " + ", ".join(map(str, row["outliers"]))
    return {"variant": variant, "query": query, "answer": answer}


class BoxPlotGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310006)

    def test_output_contract(self):
        example = BoxPlotGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = BoxPlotGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_subtraction_steps_are_exact(self):
        generator = BoxPlotGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_all_shape_outcomes_occur(self):
        generator = BoxPlotGenerator("shape")
        seen = set()
        for _ in range(300):
            seen.add(generator.generate()["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"left-skewed", "right-skewed", "symmetric"})

    def test_outliers_are_outside_whiskers(self):
        generator = BoxPlotGenerator("outliers_marked")
        for _ in range(250):
            example = generator.generate()
            plots = parse_plots(split_query(example["problem"])[0])
            row = plots["Plot"]
            self.assertTrue(row["outliers"])
            self.assertTrue(all(value < row["min"] or value > row["max"]
                                for value in row["outliers"]))

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in BoxPlotGenerator.VARIANTS:
            generator = BoxPlotGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_box_plot_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BoxPlotGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = BoxPlotGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            algebra_text = "\n".join(
                line for line in rendered.splitlines()
                if not line.startswith(("Scale:", "       +", "Plot:",
                                        "A:", "B:")))
            self.assertNotRegex(algebra_text, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
