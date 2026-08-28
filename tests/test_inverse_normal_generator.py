"""Independent supplied-table oracle for InverseNormalGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.inverse_normal_generator import QUERIES, InverseNormalGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = "\n" + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    assert denominator == 1
    places = max(twos, fives)
    scaled = value.numerator * 2 ** (places - twos) * 5 ** (places - fives)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return (sign + digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")


def selected_table(body):
    rows = {}
    for percentile, z in re.findall(
            r"(\d+(?:\.\d+)?)th percentile z = (\d+(?:\.\d+)?)", body):
        rows[Fraction(percentile)] = Fraction(z)
    assert len(rows) == 2
    return rows


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    table = selected_table(body)
    if variant == "cutoff_above":
        tail, percentile = map(Fraction, re.search(
            r"Target: top ([0-9.]+)%, whose boundary is the ([0-9.]+)th",
            body,
        ).groups())
        assert tail + percentile == 100
        mean, sigma = map(int, re.search(
            r"mean μ = (\d+) \S+ and standard deviation σ = (\d+)", body
        ).groups())
        answer = exact_text(mean + table[percentile] * sigma)
    elif variant == "cutoff_below":
        tail, z, percentile = re.search(
            r"Target: bottom ([0-9.]+)%; by symmetry use z = −([0-9.]+) "
            r"from the ([0-9.]+)th", body,
        ).groups()
        tail, z, percentile = Fraction(tail), Fraction(z), Fraction(percentile)
        assert z == table[percentile] and tail + percentile == 100
        mean, sigma = map(int, re.search(
            r"mean μ = (\d+) \S+ and standard deviation σ = (\d+)", body
        ).groups())
        answer = exact_text(mean - z * sigma)
    elif variant == "middle_interval":
        middle, z, percentile = re.search(
            r"Target: middle ([0-9.]+)%, bounded by z = ±([0-9.]+) from "
            r"the ([0-9.]+)th", body,
        ).groups()
        middle, z, percentile = (Fraction(middle), Fraction(z),
                                 Fraction(percentile))
        assert middle == 2 * percentile - 100 and z == table[percentile]
        mean, sigma = map(int, re.search(
            r"mean μ = (\d+) \S+ and standard deviation σ = (\d+)", body
        ).groups())
        offset = z * sigma
        answer = f"({exact_text(mean - offset)}, {exact_text(mean + offset)})"
    elif variant == "sigma_from_cutoff":
        mean = int(re.search(r"mean μ = (\d+)", body).group(1))
        percentile, cutoff = re.search(
            r"Their ([0-9.]+)th percentile cutoff is ([0-9.]+)", body
        ).groups()
        percentile, cutoff = Fraction(percentile), Fraction(cutoff)
        sigma = (cutoff - mean) / table[percentile]
        assert sigma.denominator == 1
        answer = str(sigma.numerator)
    else:
        sigma = int(re.search(r"standard deviation σ = (\d+)", body).group(1))
        percentile, cutoff = re.search(
            r"Their ([0-9.]+)th percentile cutoff is ([0-9.]+)", body
        ).groups()
        percentile, cutoff = Fraction(percentile), Fraction(cutoff)
        mean = cutoff - table[percentile] * sigma
        assert mean.denominator == 1
        answer = str(mean.numerator)
    return {"variant": variant, "query": query, "answer": answer,
            "table": table}


class InverseNormalGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310019)

    def test_output_contract(self):
        example = InverseNormalGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_700_answers_from_problem_text(self):
        generator = InverseNormalGenerator()
        for _ in range(700):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = InverseNormalGenerator()
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_each_lookup_has_exactly_one_decoy_and_is_supplied(self):
        generator = InverseNormalGenerator()
        for _ in range(350):
            example = generator.generate()
            parts = oracle_parts(example)
            self.assertEqual(len(parts["table"]), 2)
            lookups = [raw.split(DELIM) for raw in example["steps"]
                       if raw.startswith(f"LOOKUP_SUPPLIED{DELIM}")]
            self.assertEqual(len(lookups), 1)
            self.assertIn(lookups[0][2], example["problem"])

    def test_sigma_bank_always_recovers_an_integer(self):
        generator = InverseNormalGenerator("sigma_from_cutoff")
        for _ in range(300):
            self.assertRegex(generator.generate()["final_answer"], r"^\d+$")

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in InverseNormalGenerator.VARIANTS:
            generator = InverseNormalGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_inverse_normal_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InverseNormalGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = InverseNormalGenerator()
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
