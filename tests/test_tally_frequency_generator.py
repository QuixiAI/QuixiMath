"""Independent raw-recount and tally-decoding oracle."""
import random
import re
import unittest
from collections import Counter
from fractions import Fraction

from generators.tally_frequency_generator import QUERIES, TallyFrequencyGenerator
from helpers import DELIM
from tests import stats_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for template in queries:
            pattern = re.escape(template)
            pattern = pattern.replace(
                r"\{target\}", r"(?P<target>[A-Za-z]+)")
            pattern = pattern.replace(
                r"\{high\}", r"(?P<high>[A-Za-z]+)")
            pattern = pattern.replace(
                r"\{low\}", r"(?P<low>[A-Za-z]+)")
            match = re.search(r"\n" + pattern + r"$", problem)
            if match:
                return problem[:match.start()], variant, template, match.groupdict()
    raise AssertionError(problem)


def text_list(counts):
    return "; ".join(f"{key}: {value}" for key, value in sorted(counts.items()))


def oracle_parts(example):
    body, variant, query, fields = split_query(example["problem"])
    if variant == "raw_to_table":
        raw = re.search(r"Raw responses: ([A-Za-z, ]+)\.$", body).group(1)
        counts = Counter(raw.split(", "))
        answer = text_list(counts)
    else:
        table_start = body.index("Tally table for ")
        tally_rows = "\n".join(body[table_start:].splitlines()[1:])
        counts = stats_oracle.parse_tally(tally_rows)
        if variant == "tally_to_count":
            target = fields["target"]
            answer = str(counts[target])
        elif variant == "table_total":
            answer = str(sum(counts.values()))
        elif variant == "most_least":
            high = max(counts.values())
            low = min(counts.values())
            assert list(counts.values()).count(high) == 1
            assert list(counts.values()).count(low) == 1
            most = next(key for key, value in counts.items() if value == high)
            least = next(key for key, value in counts.items() if value == low)
            answer = f"most: {most} ({high}); least: {least} ({low})"
        else:
            high, low = fields["high"], fields["low"]
            answer = str(counts[high] - counts[low])
    return {"variant": variant, "query": query, "answer": answer}


class TallyFrequencyGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310001)

    def test_output_contract(self):
        example = TallyFrequencyGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = TallyFrequencyGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = TallyFrequencyGenerator()
        for _ in range(300):
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

    def test_tally_rows_use_exact_group_of_five_grammar(self):
        generator = TallyFrequencyGenerator()
        for _ in range(250):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "TALLY_ROW":
                    marks = fields[2]
                    count = int(fields[3])
                    groups = marks.split()
                    self.assertTrue(all(group == "////\\" for group in groups[:-1]))
                    decoded = 5 * sum(group == "////\\" for group in groups)
                    decoded += sum(len(group) for group in groups if group != "////\\")
                    self.assertEqual(decoded, count, raw)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in TallyFrequencyGenerator.VARIANTS:
            generator = TallyFrequencyGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_tally_frequency_{variant}")
                seen.add(parts["query"])
            self.assertEqual(len(seen), 4)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TallyFrequencyGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = TallyFrequencyGenerator()
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
