"""Independent exact oracle for AlternativeMeansGenerator prompts."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.alternative_means_generator import QUERIES, AlternativeMeansGenerator
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
    scaled = abs(value.numerator) * 10 ** places // value.denominator
    sign = "-" if value < 0 else ""
    if places == 0:
        return f"{sign}{scaled}"
    digits = str(scaled).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}".rstrip("0").rstrip(".")


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def _values(body):
    text = re.search(r"(?:are|values): ([-0-9, ]+)\.", body).group(1)
    return list(map(int, text.split(", ")))


def _perfect_root(product, size):
    candidate = 1
    while candidate ** size < product:
        candidate += 1
    assert candidate ** size == product
    return candidate


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "midrange":
        values = _values(body)
        answer = exact_text(Fraction(min(values) + max(values), 2))
    elif variant == "trimmed_mean":
        values = _values(body)
        percent = int(re.search(r"lowest (\d+)%", body).group(1))
        drop = len(values) * percent // 100
        kept = sorted(values)[drop:len(values) - drop]
        answer = exact_text(Fraction(sum(kept), len(kept)))
    elif variant == "harmonic_mean":
        values = _values(body)
        reciprocal_sum = sum((Fraction(1, value) for value in values),
                             Fraction(0))
        answer = exact_text(Fraction(len(values), 1) / reciprocal_sum)
    elif variant == "geometric_mean_data":
        values = _values(body)
        answer = str(_perfect_root(math.prod(values), len(values)))
    elif "equal distances" in body:
        first, second = map(int, re.search(
            r"at (\d+) mph and (\d+) mph", body).groups())
        value = Fraction(2 * first * second, first + second)
        answer = f"harmonic; {exact_text(value)} mph"
    else:
        first, second = map(Fraction, re.search(
            r"growth factors ([0-9.]+) and ([0-9.]+)", body).groups())
        product = first * second
        numerator_root = math.isqrt(product.numerator)
        denominator_root = math.isqrt(product.denominator)
        assert numerator_root ** 2 == product.numerator
        assert denominator_root ** 2 == product.denominator
        root = Fraction(numerator_root, denominator_root)
        answer = f"geometric; factor {exact_text(root)}"
    return {"variant": variant, "query": query, "answer": answer}


class AlternativeMeansGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310011)

    def test_output_contract(self):
        example = AlternativeMeansGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = AlternativeMeansGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = AlternativeMeansGenerator()
        root_powers = {"√": 2, "∛": 3, "∜": 4}
        for _ in range(450):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "ROOT":
                    symbol = fields[1][0]
                    radicand = Fraction(fields[1][1:])
                    self.assertEqual(Fraction(fields[2]) ** root_powers[symbol],
                                     radicand, raw)

    def test_reciprocal_and_lcd_steps_are_exact(self):
        generator = AlternativeMeansGenerator("harmonic_mean")
        for _ in range(300):
            example = generator.generate()
            denominators = []
            common = None
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "RECIP_ROW":
                    denominators.append(int(fields[1]))
                    self.assertEqual(Fraction(1, int(fields[1])),
                                     Fraction(fields[2]), raw)
                elif fields[0] == "L":
                    common = int(fields[2])
                    self.assertEqual(common,
                                     math.lcm(*map(int, fields[1].split(","))))
                elif fields[0] == "C":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
            self.assertEqual(common, math.lcm(*denominators))

    def test_trim_rule_drops_the_stated_count_from_each_end(self):
        generator = AlternativeMeansGenerator("trimmed_mean")
        for _ in range(250):
            example = generator.generate()
            body = split_query(example["problem"])[0]
            values = _values(body)
            percent = int(re.search(r"lowest (\d+)%", body).group(1))
            drop = len(values) * percent // 100
            rule = next(raw for raw in example["steps"]
                        if raw.startswith(f"RULE{DELIM}"))
            self.assertIn(f"drop {drop} low, {drop} high", rule)
            trim = next(raw for raw in example["steps"]
                        if raw.startswith(f"TRIM{DELIM}"))
            self.assertTrue(trim.endswith(f"{len(values) - 2 * drop} kept"))

    def test_geometric_products_are_perfect_powers(self):
        generator = AlternativeMeansGenerator("geometric_mean_data")
        for _ in range(250):
            example = generator.generate()
            values = _values(split_query(example["problem"])[0])
            mean = int(example["final_answer"])
            self.assertEqual(math.prod(values), mean ** len(values))

    def test_both_method_choices_occur(self):
        generator = AlternativeMeansGenerator("which_mean")
        seen = set()
        for _ in range(300):
            seen.add(generator.generate()["final_answer"].split(";", 1)[0])
        self.assertEqual(seen, {"harmonic", "geometric"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in AlternativeMeansGenerator.VARIANTS:
            generator = AlternativeMeansGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_alternative_means_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            AlternativeMeansGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = AlternativeMeansGenerator()
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
