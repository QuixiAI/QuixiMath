"""Independent keyed-display oracle for StemAndLeafGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.stem_and_leaf_generator import QUERIES, StemAndLeafGenerator
from helpers import DELIM
from tests import stats_oracle


def ntext(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator == 1:
        return f"{float(value):.10f}".rstrip("0").rstrip(".")
    return str(value)


def split_query(problem):
    number = r"-?\d+(?:\.\d+|/\d+)?"
    for variant, queries in QUERIES.items():
        for template in queries:
            pattern = re.escape(template)
            pattern = pattern.replace(r"\{stem\}", r"(?P<stem>\d+)")
            pattern = pattern.replace(r"\{lower\}", rf"(?P<lower>{number})")
            pattern = pattern.replace(r"\{upper\}", rf"(?P<upper>{number})")
            match = re.search(r"\n" + pattern + r"$", problem)
            if match:
                return problem[:match.start()], variant, template, match.groupdict()
    raise AssertionError(problem)


def plot_values(body):
    lines = body.splitlines()
    start = next(index for index, line in enumerate(lines)
                 if "∣" in line and "Leaves" in line)
    return stats_oracle.parse_stem_leaf("\n".join(lines[start:]))


def stem_list(values):
    pairs = [divmod(int(value), 10) for value in sorted(values)]
    rows = {stem: [] for stem in range(pairs[0][0], pairs[-1][0] + 1)}
    for stem, leaf in pairs:
        rows[stem].append(leaf)
    return "; ".join(f"{stem}: " + (" ".join(map(str, leaves)) or "none")
                     for stem, leaves in rows.items())


def oracle_parts(example):
    body, variant, query, fields = split_query(example["problem"])
    if variant == "construct":
        raw = re.search(r"raw [a-z ]+ are: ([0-9, ]+)\. Use tens", body).group(1)
        values = list(map(Fraction, raw.split(", ")))
        answer = stem_list(values)
    else:
        values = plot_values(body)
        if variant in ("list_values", "decimal_key"):
            answer = ", ".join(ntext(value) for value in values)
        elif variant == "count_in_stem":
            stem = int(fields["stem"])
            decimal = any(value.denominator != 1 for value in values)
            place = 1 if decimal else 10
            answer = str(sum(int(value / place) == stem for value in values))
        elif variant == "median_from_plot":
            middle = len(values) // 2
            median = (values[middle] if len(values) % 2 else
                      (values[middle - 1] + values[middle]) / 2)
            answer = ntext(median)
        elif variant == "range_from_plot":
            answer = ntext(values[-1] - values[0])
        else:
            lower, upper = Fraction(fields["lower"]), Fraction(fields["upper"])
            answer = str(sum(lower <= value <= upper for value in values))
    return {"variant": variant, "query": query, "answer": answer}


class StemAndLeafGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310004)

    def test_output_contract(self):
        example = StemAndLeafGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = StemAndLeafGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = StemAndLeafGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "MEAN_DIV":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_display_has_key_sorted_leaves_and_contiguous_stems(self):
        generator = StemAndLeafGenerator("list_values")
        saw_empty = False
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            values = plot_values(body)
            self.assertEqual(values, sorted(values))
            rows = [line for line in body.splitlines()
                    if "∣" in line and "Leaves" not in line and not line.startswith("Key:")]
            saw_empty |= any(not line.split("∣", 1)[1].strip() for line in rows)
            self.assertEqual(sum(len(line.split("∣", 1)[1].split()) for line in rows),
                             len(values))
        self.assertTrue(saw_empty)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in StemAndLeafGenerator.VARIANTS:
            generator = StemAndLeafGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_stem_and_leaf_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StemAndLeafGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = StemAndLeafGenerator()
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
