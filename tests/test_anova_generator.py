"""Independent raw-data oracle for ANOVAGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.anova_generator import ANOVAGenerator, QUERIES
from helpers import DELIM
from tests.stats_oracle import anova


def number(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value)
    sign = "-" if value < 0 else ""
    value = abs(value)
    scale = 1
    while (value * scale).denominator != 1:
        scale *= 10
    digits = str(int(value * scale)).rjust(len(str(scale)), "0")
    if scale == 1:
        return sign + digits
    places = len(str(scale)) - 1
    return sign + f"{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_groups(problem):
    body = re.search(r"raw data \[(.*?)\]\. Use α", problem).group(1)
    labels, groups = [], []
    for chunk in body.split("; "):
        label, values = chunk.split(": ")
        labels.append(label)
        groups.append([Fraction(value) for value in values.split(", ")])
    return labels, groups


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    labels, groups = parse_groups(body)
    result = anova(groups)
    critical_text, df_b, df_w = re.search(
        r"F critical value = ([\d.]+) \(df (\d+), (\d+)\)", body).groups()
    assert result["df"] == (int(df_b), int(df_w))
    if variant == "group_means":
        answer = "; ".join(f"{label}: {number(mean)}"
                           for label, mean in zip(labels, result["group_means"]))
    elif variant == "ss_between":
        answer = number(result["ssb"])
    elif variant == "ss_within":
        answer = number(result["ssw"])
    elif variant == "anova_table":
        answer = (f"SSB = {number(result['ssb'])}; "
                  f"SSW = {number(result['ssw'])}; "
                  f"df = {df_b}, {df_w}; MSB = {number(result['msb'])}; "
                  f"MSW = {number(result['msw'])}; F = {number(result['f'])}")
    elif variant == "f_stat":
        answer = number(result["f"])
    elif variant == "df_only":
        answer = f"df = {df_b}, {df_w}"
    else:
        reject = result["f"] > Fraction(critical_text)
        label = "reject H0" if reject else "fail to reject H0"
        relation = ">" if reject else "≤"
        answer = (f"{label} ({number(result['f'])} {relation} "
                  f"{critical_text})")
    return {"answer": answer, "variant": variant, "query": query,
            "labels": labels, "groups": groups, "critical": critical_text,
            **result}


class ANOVAGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(741903)

    def test_output_contract(self):
        example = ANOVAGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_900_answers_from_raw_problem_data(self):
        generator = ANOVAGenerator()
        for _ in range(900):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_step_arithmetic_and_sst_identity(self):
        generator = ANOVAGenerator()
        for _ in range(500):
            example = generator.generate()
            parts = oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "SUM":
                    terms = [Fraction(value.strip())
                             for value in fields[1].split("+")]
                    self.assertEqual(sum(terms), Fraction(fields[2]), raw)
                elif fields[0] in ("MEAN_DIV", "D"):
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "DEV_ROW":
                    self.assertEqual(Fraction(fields[2]) ** 2,
                                     Fraction(fields[3]), raw)
                elif fields[0] == "SS_BETWEEN":
                    self.assertEqual(Fraction(fields[2]), parts["ssb"], raw)
                elif fields[0] == "SS_WITHIN":
                    self.assertEqual(Fraction(fields[2]), parts["ssw"], raw)
                elif fields[0] == "CHECK" and fields[1] == "SST":
                    total = Fraction(re.search(r"= ([\d./]+)",
                                               fields[2]).group(1))
                    direct = Fraction(re.search(r"= ([\d./]+)",
                                                fields[3]).group(1))
                    self.assertEqual(total, parts["ssb"] + parts["ssw"])
                    self.assertEqual(direct, parts["sst"])
                elif fields[0] == "LOOKUP_SUPPLIED":
                    self.assertIn(fields[2], example["problem"])

    def test_anova_rows_match_each_raw_group(self):
        generator = ANOVAGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw.split(DELIM) for raw in example["steps"]
                    if raw.startswith(f"ANOVA_ROW{DELIM}")]
            self.assertEqual(len(rows), len(parts["groups"]))
            for row, label, mean, group in zip(
                    rows, parts["labels"], parts["group_means"], parts["groups"]):
                ss = sum((value - mean) ** 2 for value in group)
                self.assertEqual(row[1], label)
                self.assertEqual(row[2], f"mean {number(mean)}")
                self.assertEqual(row[3], f"SS {number(ss)}")

    def test_equal_group_sizes_and_full_shape_bank(self):
        generator = ANOVAGenerator()
        seen = set()
        for _ in range(1200):
            groups = oracle_parts(generator.generate())["groups"]
            sizes = {len(group) for group in groups}
            self.assertEqual(len(sizes), 1)
            seen.add((len(groups), len(groups[0])))
        self.assertEqual(seen, {(k, n) for k in (3, 4) for n in (3, 4, 5)})

    def test_f_variants_filter_for_integer_msw(self):
        for variant in ("f_stat", "f_decision"):
            generator = ANOVAGenerator(variant)
            for _ in range(400):
                parts = oracle_parts(generator.generate())
                self.assertEqual(parts["msw"].denominator, 1)

    def test_decision_variant_reaches_both_outcomes(self):
        generator = ANOVAGenerator("f_decision")
        labels = {generator.generate()["final_answer"].split(" (")[0]
                  for _ in range(800)}
        self.assertEqual(labels, {"reject H0", "fail to reject H0"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in ANOVAGenerator.VARIANTS:
            generator = ANOVAGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_anova_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ANOVAGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ANOVAGenerator()
        for _ in range(400):
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
