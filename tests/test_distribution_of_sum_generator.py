"""Independent product-space oracle for DistributionOfSumGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.distribution_of_sum_generator import QUERIES, DistributionOfSumGenerator
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


def parse_pmf(body, label):
    rows = [(int(value), Fraction(p)) for value, p in
            re.findall(rf"P\({label}=(\d+)\)=(-?\d+(?:/\d+)?)", body)]
    assert rows and sum((p for _, p in rows), Fraction()) == 1
    return dict(rows)


def product_distribution(x_pmf, y_pmf, function):
    output = {}
    for x, px in x_pmf.items():
        for y, py in y_pmf.items():
            value = function(x, y)
            output[value] = output.get(value, Fraction()) + px * py
    return output


def answer_pmf(label, pmf):
    return "; ".join(f"P({label}={value}) = {ptext(probability)}"
                     for value, probability in sorted(pmf.items()))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("convolution_pmf", "single_value", "max_of_two", "min_of_two"):
        x_pmf, y_pmf = parse_pmf(body, "X"), parse_pmf(body, "Y")
        if variant in ("convolution_pmf", "single_value"):
            output = product_distribution(x_pmf, y_pmf, lambda x, y: x + y)
            if variant == "single_value":
                target = int(re.search(r"Target: P\(S=(\d+)\)", body).group(1))
                answer = ptext(output[target])
            else:
                answer = answer_pmf("S", output)
        else:
            function = max if variant == "max_of_two" else min
            output = product_distribution(x_pmf, y_pmf, function)
            answer = answer_pmf("M", output)
    elif variant == "weighted_dice_sum":
        match = re.search(
            r"fair (\d+)- and (\d+)-sided dice X and Y\. Let W=(\d+)X\+(\d+)Y\. "
            r"Target: P\(W=(\d+)\)", body)
        sides_x, sides_y, a, b, target = map(int, match.groups())
        pairs = tuple(itertools.product(range(1, sides_x + 1),
                                        range(1, sides_y + 1)))
        answer = ptext(Fraction(sum(a * x + b * y == target for x, y in pairs),
                                len(pairs)))
    elif variant == "sum_binomial_rule":
        match = re.search(
            r"X~Binomial\((\d+),(\d+(?:/\d+)?)\) and Y~Binomial\((\d+),\2\)\. "
            r"Let S=X\+Y\. Target: P\(S=(\d+)\)", body)
        n1, p_text, n2, k = match.groups()
        n, p, k = int(n1) + int(n2), Fraction(p_text), int(k)
        probability = Fraction(math.comb(n, k)) * p ** k * (1 - p) ** (n - k)
        answer = f"Binomial({n}, {ptext(p)}); P(S={k}) = {ptext(probability)}"
    else:
        match = re.search(r"X~Poisson\((\d+)\) and Y~Poisson\((\d+)\)", body)
        total = int(match.group(1)) + int(match.group(2))
        answer = f"Poisson({total}); mean {total}; variance {total}"
    return {"variant": variant, "query": query, "answer": answer}


class DistributionOfSumGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(502841)

    def test_output_contract(self):
        example = DistributionOfSumGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = DistributionOfSumGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_combination_steps_are_exact(self):
        generator = DistributionOfSumGenerator()
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
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"\((\d+(?:/\d+)?)\)\^(\d+)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))

    def test_output_pmfs_sum_to_one(self):
        for variant in ("convolution_pmf", "max_of_two", "min_of_two"):
            generator = DistributionOfSumGenerator(variant)
            for _ in range(120):
                example = generator.generate()
                probabilities = [Fraction(value) for value in
                                 re.findall(r"= (-?\d+(?:/\d+)?)",
                                            example["final_answer"])]
                self.assertEqual(sum(probabilities, Fraction()), 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in DistributionOfSumGenerator.VARIANTS:
            generator = DistributionOfSumGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_distribution_sum_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DistributionOfSumGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = DistributionOfSumGenerator()
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
