"""Independent finite enumeration oracle for ConditionalExpectationGenerator."""
import itertools
import random
import re
import unittest
from fractions import Fraction

from generators.conditional_expectation_generator import (
    QUERIES, ConditionalExpectationGenerator,
)
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def table_rows(body):
    rows = [(int(x), int(y), Fraction(p)) for x, y, p in
            re.findall(r"P\(X=(-?\d+),Y=(\d+)\)=(-?\d+(?:/\d+)?)", body)]
    assert len(rows) == 4 and sum((p for _, _, p in rows), Fraction()) == 1
    return rows


def conditional(rows, y_value):
    selected = [(x, p) for x, y, p in rows if y == y_value]
    marginal = sum((p for _, p in selected), Fraction())
    mean = sum((x * p for x, p in selected), Fraction()) / marginal
    variance = sum(((Fraction(x) - mean) ** 2 * p for x, p in selected),
                   Fraction()) / marginal
    return marginal, mean, variance


def n_rows(body):
    rows = [(int(n), Fraction(p)) for n, p in
            re.findall(r"P\(N=(\d+)\)=(-?\d+(?:/\d+)?)", body)]
    assert len(rows) == 4 and sum((p for _, p in rows), Fraction()) == 1
    return rows


def random_sum_distribution(rows, p):
    distribution = {}
    for n, pn in rows:
        for bits in itertools.product((0, 1), repeat=n):
            weight = pn
            for bit in bits:
                weight *= p if bit else 1 - p
            total = sum(bits)
            distribution[total] = distribution.get(total, Fraction()) + weight
    return distribution


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("from_table", "tower_check", "conditional_variance",
                   "total_variance_check"):
        rows = table_rows(body)
        p0, mean0, var0 = conditional(rows, 0)
        p1, mean1, var1 = conditional(rows, 1)
        overall_mean = sum((x * p for x, _, p in rows), Fraction())
        overall_var = sum(((Fraction(x) - overall_mean) ** 2 * p
                           for x, _, p in rows), Fraction())
        if variant == "from_table":
            target = int(re.search(r"Target: E\[X given Y=(\d+)\]", body).group(1))
            mean = mean0 if target == 0 else mean1
            answer = f"E[X given Y={target}] = {ptext(mean)}"
        elif variant == "conditional_variance":
            target = int(re.search(r"given Y=(\d+)\.", body).group(1))
            mean, variance = (mean0, var0) if target == 0 else (mean1, var1)
            answer = (f"E[X given Y={target}] = {ptext(mean)}; "
                      f"Var(X given Y={target}) = {ptext(variance)}")
        elif variant == "tower_check":
            answer = (f"E[X given Y=0] = {ptext(mean0)}; "
                      f"E[X given Y=1] = {ptext(mean1)}; "
                      f"E[X] = {ptext(p0 * mean0 + p1 * mean1)}")
        else:
            within = p0 * var0 + p1 * var1
            between = p0 * (mean0 - overall_mean) ** 2 + p1 * (mean1 - overall_mean) ** 2
            answer = (f"Var(X) = {ptext(overall_var)}; "
                      f"E[Var(X given Y)] = {ptext(within)}; "
                      f"Var(E[X given Y]) = {ptext(between)}")
    elif variant == "two_stage_experiment":
        faces = int(re.search(r"fair (\d+)-sided die", body).group(1))
        expectation = Fraction()
        for n in range(1, faces + 1):
            for bits in itertools.product((0, 1), repeat=n):
                expectation += Fraction(1, faces) * Fraction(1, 2) ** n * sum(bits)
        answer = f"E[H] = {ptext(expectation)}"
    else:
        rows = n_rows(body)
        p = Fraction(re.search(r"Bernoulli\((\d+(?:/\d+)?)\)", body).group(1))
        distribution = random_sum_distribution(rows, p)
        mean = sum((value * probability for value, probability in distribution.items()),
                   Fraction())
        if variant == "random_sum_mean":
            answer = f"E[S] = {ptext(mean)}"
        else:
            variance = sum(((Fraction(value) - mean) ** 2 * probability
                            for value, probability in distribution.items()), Fraction())
            answer = f"Var(S) = {ptext(variance)}"
    return {"variant": variant, "query": query, "answer": answer}


class ConditionalExpectationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(418063)

    def test_output_contract(self):
        example = ConditionalExpectationGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ConditionalExpectationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_square_steps_are_exact(self):
        generator = ConditionalExpectationGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]))

    def test_total_variance_components_sum_to_direct_variance(self):
        generator = ConditionalExpectationGenerator("total_variance_check")
        for _ in range(150):
            example = generator.generate()
            values = [Fraction(value) for value in
                      re.findall(r"= (-?\d+(?:/\d+)?)", example["final_answer"])]
            self.assertEqual(values[0], values[1] + values[2])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ConditionalExpectationGenerator.VARIANTS:
            generator = ConditionalExpectationGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_conditional_expectation_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ConditionalExpectationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ConditionalExpectationGenerator()
        for _ in range(250):
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
