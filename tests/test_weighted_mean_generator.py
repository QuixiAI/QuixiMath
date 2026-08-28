"""Independent exact oracle for WeightedMeanGenerator prompts."""
import random
import re
import unittest
from fractions import Fraction

from generators.weighted_mean_generator import QUERIES, WeightedMeanGenerator
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
    numerator = abs(value.numerator) * 10 ** places // value.denominator
    if places == 0:
        return f"{sign}{numerator}"
    digits = str(numerator).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def money_text(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def _mean(values, weights):
    return (sum(Fraction(value) * weight
                for value, weight in zip(values, weights))
            / sum(weights, Fraction(0)))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "weights":
        pairs = [(int(value), Fraction(weight)) for value, weight in
                 re.findall(r"\((\d+), (\d+)\)", body)]
        answer = exact_text(_mean([v for v, _ in pairs],
                                  [w for _, w in pairs]))
    elif variant == "percent_weights":
        rows = [(int(score), Fraction(int(percent), 100)) for score, percent in
                re.findall(r"=([0-9]+) at ([0-9]+)%", body)]
        answer = exact_text(_mean([v for v, _ in rows],
                                  [w for _, w in rows]))
    elif variant == "frequency_table_mean":
        table = re.search(r"frequency\): (.+)\.$", body).group(1)
        pairs = [(int(value), Fraction(frequency)) for value, frequency in
                 re.findall(r"(\d+): (\d+)", table)]
        answer = exact_text(_mean([v for v, _ in pairs],
                                  [w for _, w in pairs]))
    elif variant == "price_per_unit":
        pairs = [(Fraction(price), Fraction(amount)) for price, amount in
                 re.findall(r"\(\$(\d+\.\d{2}) per kg, (\d+) kg\)", body)]
        answer = f"{money_text(_mean([v for v, _ in pairs],
                                      [w for _, w in pairs]))} per kg"
    else:
        pairs = [(int(value), Fraction(weight)) for value, weight in
                 re.findall(r"\((\d+), (\d+)\)", body)]
        missing = int(re.search(r"Missing entry: value (\d+)", body).group(1))
        target = int(re.search(r"Target weighted mean: (\d+)", body).group(1))
        known_total = sum(Fraction(value) * weight for value, weight in pairs)
        known_weight = sum((weight for _, weight in pairs), Fraction(0))
        wanted = (target * known_weight - known_total) / (missing - target)
        assert wanted.denominator == 1 and wanted > 0
        answer = str(wanted.numerator)
    return {"variant": variant, "query": query, "answer": answer}


class WeightedMeanGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310009)

    def test_output_contract(self):
        example = WeightedMeanGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = WeightedMeanGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_and_weight_rows_are_exact(self):
        generator = WeightedMeanGenerator()
        for _ in range(400):
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
                elif fields[0] == "WEIGHT_ROW":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "PERCENT_TO_DEC":
                    self.assertEqual(Fraction(int(fields[1][:-1]), 100),
                                     Fraction(fields[2]), raw)

    def test_check_steps_are_exact_where_numeric(self):
        generator = WeightedMeanGenerator()
        for _ in range(350):
            example = generator.generate()
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[:2] == ["CHECK", "weighted mean"]:
                    numerator, denominator = fields[2].split("/")
                    self.assertEqual(Fraction(numerator) / Fraction(denominator),
                                     Fraction(fields[3]), raw)
                elif fields[:2] == ["CHECK", "percent weights sum"]:
                    self.assertEqual(fields[2:], ["100%", "1"])
                elif fields[:2] == ["CHECK", "substitute"]:
                    match = re.fullmatch(
                        r"\((\d+) \+ (\d+)·(\d+)\)/\((\d+) \+ (\d+)\)",
                        fields[2],
                    )
                    a, b, w1, c, w2 = map(int, match.groups())
                    self.assertEqual(w1, w2)
                    self.assertEqual(Fraction(a + b * w1, c + w2),
                                     Fraction(fields[3]), raw)

    def test_frequency_values_are_distinct(self):
        generator = WeightedMeanGenerator("frequency_table_mean")
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            table = re.search(r"frequency\): (.+)\.$", body).group(1)
            values = [int(value) for value, _ in
                      re.findall(r"(\d+): (\d+)", table)]
            self.assertEqual(len(values), len(set(values)))
            self.assertEqual(values, sorted(values))

    def test_percent_weights_sum_to_100(self):
        generator = WeightedMeanGenerator("percent_weights")
        for _ in range(250):
            body = split_query(generator.generate()["problem"])[0]
            percents = [int(value) for value in re.findall(r"at (\d+)%", body)]
            self.assertEqual(sum(percents), 100)

    def test_missing_weights_are_positive_integers(self):
        generator = WeightedMeanGenerator("missing_weight")
        for _ in range(250):
            example = generator.generate()
            self.assertGreater(int(example["final_answer"]), 0)
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"])

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in WeightedMeanGenerator.VARIANTS:
            generator = WeightedMeanGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_weighted_mean_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            WeightedMeanGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = WeightedMeanGenerator()
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
