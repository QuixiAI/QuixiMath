"""Independent full-enumeration oracle for sampling distributions."""
import itertools
import random
import re
import unittest
from collections import Counter
from fractions import Fraction

from generators.sampling_distribution_enum_generator import (
    QUERIES,
    SamplingDistributionEnumGenerator,
)
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
    d = value.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    if d != 1:
        return str(value)
    places = 1
    while (value * 10 ** places).denominator != 1:
        places += 1
    scaled = int(abs(value) * 10 ** places)
    digits = str(scaled).rjust(places + 1, "0")
    sign = "-" if value < 0 else ""
    return (sign + digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def text_list(pairs):
    return "; ".join(f"{key}: {value}" for key, value in pairs)


def sample_label(sample):
    return "{" + ", ".join(map(str, sample)) + "}"


def parsed_case(body):
    binary = "binary population values" in body
    label = "binary population values" if binary else "population values"
    population = list(map(int, re.search(
        rf"{label} are: ([0-9, ]+)\.", body).group(1).split(", ")))
    sample_size = int(re.search(r"Sampling plan: n = (\d+)", body).group(1))
    replacement = "with replacement" in body
    if replacement:
        samples = list(itertools.product(population, repeat=sample_size))
    elif binary:
        samples = [tuple(population[i] for i in indexes)
                   for indexes in itertools.combinations(
                       range(len(population)), sample_size)]
    else:
        samples = list(itertools.combinations(population, sample_size))
    stats = [Fraction(sum(sample), sample_size) for sample in samples]
    return population, sample_size, replacement, samples, stats, Counter(stats)


def distribution_answer(counts, total):
    return text_list((exact_text(value), ptext(Fraction(count, total)))
                     for value, count in sorted(counts.items()))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    population, n, replacement, samples, stats, counts = parsed_case(body)
    total = len(samples)
    if variant == "list_means":
        answer = text_list((sample_label(sample), exact_text(value))
                           for sample, value in zip(samples, stats))
    elif variant in ("distribution_table", "proportion_phat"):
        answer = distribution_answer(counts, total)
    elif variant == "mean_of_xbar":
        expected = sum(value * Fraction(count, total)
                       for value, count in counts.items())
        population_mean = Fraction(sum(population), len(population))
        assert expected == population_mean
        answer = (f"{exact_text(expected)}; equals μ = "
                  f"{exact_text(population_mean)}")
    elif variant == "variance_of_xbar":
        expected = sum(value * Fraction(count, total)
                       for value, count in counts.items())
        variance = sum((value - expected) ** 2 * Fraction(count, total)
                       for value, count in counts.items())
        pop_mean = Fraction(sum(population), len(population))
        pop_variance = sum((value - pop_mean) ** 2
                           for value in population) / len(population)
        base = pop_variance / n
        if replacement:
            identity = base
            formula = f"σ²/n = {exact_text(base)}"
        else:
            correction = Fraction(len(population) - n, len(population) - 1)
            identity = base * correction
            formula = (f"σ²/n · (N-n)/(N-1) = {exact_text(base)} · "
                       f"{exact_text(correction)} = {exact_text(identity)}")
        assert variance == identity
        answer = f"{exact_text(variance)}; {formula}"
    else:
        threshold = Fraction(re.search(
            r"Event: x̄ ≥ (\d+(?:\.\d+)?(?:/\d+)?)", body)
                             .group(1))
        qualifying = sum(value >= threshold for value in stats)
        answer = ptext(Fraction(qualifying, total))
    return {"variant": variant, "query": query, "answer": answer,
            "samples": samples, "stats": stats, "counts": counts,
            "total": total}


class SamplingDistributionEnumGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(310020)

    def test_output_contract(self):
        example = SamplingDistributionEnumGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_600_answers_by_full_enumeration(self):
        generator = SamplingDistributionEnumGenerator()
        for _ in range(600):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_enumeration_rows_are_complete_and_capped_at_twenty(self):
        generator = SamplingDistributionEnumGenerator()
        for _ in range(400):
            example = generator.generate()
            parts = oracle_parts(example)
            rows = [raw for raw in example["steps"]
                    if raw.startswith(f"SAMPLE_ENUM{DELIM}")]
            self.assertEqual(len(rows), parts["total"])
            self.assertLessEqual(len(rows), 20)

    def test_arithmetic_steps_are_exact(self):
        generator = SamplingDistributionEnumGenerator()
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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]), raw)

    def test_distribution_rows_sum_to_one(self):
        for variant in ("distribution_table", "mean_of_xbar",
                        "variance_of_xbar", "prob_event", "proportion_phat"):
            generator = SamplingDistributionEnumGenerator(variant)
            for _ in range(150):
                example = generator.generate()
                rows = [raw.split(DELIM) for raw in example["steps"]
                        if raw.startswith(f"DIST_ROW{DELIM}")]
                self.assertEqual(sum(Fraction(row[3]) for row in rows), 1)

    def test_replacement_prompts_use_ordered_sequences(self):
        generator = SamplingDistributionEnumGenerator()
        seen = 0
        for _ in range(400):
            example = generator.generate()
            if "ordered draws with replacement" not in example["problem"]:
                continue
            seen += 1
            parts = oracle_parts(example)
            population_size = int(round(parts["total"] ** 0.5))
            self.assertEqual(parts["total"], population_size ** 2)
        self.assertGreater(seen, 50)

    def test_both_sampling_methods_are_reachable(self):
        generator = SamplingDistributionEnumGenerator()
        seen = set()
        for _ in range(300):
            problem = generator.generate()["problem"]
            seen.add("with" if "with replacement" in problem else "without")
        self.assertEqual(seen, {"with", "without"})

    def test_variance_identity_is_supplied_in_problem(self):
        generator = SamplingDistributionEnumGenerator("variance_of_xbar")
        seen = set()
        for _ in range(200):
            problem = generator.generate()["problem"]
            self.assertIn("σ² is the population variance (divide by N)", problem)
            if "with replacement" in problem:
                self.assertIn("Var(x̄) = σ²/n", problem)
                seen.add("with")
            else:
                self.assertIn("Var(x̄) = (σ²/n) · (N-n)/(N-1)", problem)
                seen.add("without")
        self.assertEqual(seen, {"with", "without"})

    def test_all_variants_and_four_phrasings_are_reachable(self):
        for variant in SamplingDistributionEnumGenerator.VARIANTS:
            generator = SamplingDistributionEnumGenerator(variant)
            seen = set()
            for _ in range(300):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"statistics_sampling_distribution_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SamplingDistributionEnumGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SamplingDistributionEnumGenerator()
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
