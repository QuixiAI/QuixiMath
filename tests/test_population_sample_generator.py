"""Independent population/sample arithmetic oracle."""
import random
import re
import unittest
from fractions import Fraction

from generators.population_sample_generator import QUERIES, PopulationSampleGenerator
from helpers import DELIM


def ntext(value):
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
    if denominator == 1:
        places = max(twos, fives)
        scaled = abs(value.numerator) * 10 ** places // value.denominator
        digits = str(scaled).rjust(places + 1, "0")
        text = (digits if places == 0 else
                f"{digits[:-places]}.{digits[-places:]}")
        text = text.rstrip("0").rstrip(".")
        return ("-" if value < 0 else "") + text
    return str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "capture_recapture":
        match = re.search(r"marks M=(\d+) ([a-z]+).*captures C=(\d+) [a-z]+; "
                          r"R=(\d+)", body)
        marked, animal, captured, recaptured = match.groups()
        estimate = Fraction(int(marked) * int(captured), int(recaptured))
        assert estimate.denominator == 1
        answer = f"estimated population: {estimate.numerator} {animal}"
    elif variant == "parameter_vs_statistic":
        match = re.search(r"complete census of (\d+) ([a-z]+).*finds (\d+) that "
                          r"[a-z ]+\. A random sample of (\d+) [a-z]+ finds "
                          r"(\d+) that", body)
        population, group, census_count, sample, observed = match.groups()
        parameter = Fraction(int(census_count), int(population))
        statistic = Fraction(int(observed), int(sample))
        answer = f"parameter: {ntext(parameter)}; statistic: {ntext(statistic)}"
    elif variant == "identify":
        match = re.search(r"population is all (\d+) ([a-z]+).*random sample "
                          r"contains (\d+) [a-z]+; (\d+) ", body)
        population, group, sample, observed = match.groups()
        statistic = Fraction(int(observed), int(sample))
        answer = (f"population: {population} {group}; sample: {sample} {group}; "
                  f"statistic: {ntext(statistic)}")
    else:
        match = re.search(r"contains (\d+) ([a-z]+)\. In a random sample of "
                          r"(\d+) [a-z]+, (\d+) ", body)
        population, group, sample, observed = match.groups()
        estimate = Fraction(int(observed), int(sample)) * int(population)
        answer = f"estimated count: {ntext(estimate)} {group}"
    return {"variant": variant, "query": query, "answer": answer}


class PopulationSampleGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310005)

    def test_output_contract(self):
        example = PopulationSampleGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PopulationSampleGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = PopulationSampleGenerator()
        for _ in range(350):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_capture_recapture_is_integral(self):
        generator = PopulationSampleGenerator("capture_recapture")
        for _ in range(250):
            example = generator.generate()
            match = re.search(r"M=(\d+).*C=(\d+).*R=(\d+)", example["problem"])
            marked, captured, recaptured = map(int, match.groups())
            self.assertEqual((marked * captured) % recaptured, 0)

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in PopulationSampleGenerator.VARIANTS:
            generator = PopulationSampleGenerator(variant)
            seen = set()
            for _ in range(260):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_population_sample_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PopulationSampleGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PopulationSampleGenerator()
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
