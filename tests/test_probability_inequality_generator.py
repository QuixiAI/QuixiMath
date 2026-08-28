"""Independent formula and pmf oracle for ProbabilityInequalityGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.probability_inequality_generator import (
    QUERIES, ProbabilityInequalityGenerator,
)
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def ceil_fraction(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "markov":
        mean = int(re.search(r"E\[X\]=(\d+)", body).group(1))
        threshold = int(re.search(r"P\(X≥(\d+)\)", body).group(1))
        answer = ptext(Fraction(mean, threshold))
    elif variant in ("chebyshev", "chebyshev_within"):
        match = re.search(r"mean μ=(-?\d+) and variance (\d+)", body)
        mean, variance = map(int, match.groups())
        target = re.search(r"Target: P\(abs\(X−-?\d+\)([≥<])(\d+)\)", body)
        relation, radius = target.group(1), int(target.group(2))
        tail = Fraction(variance, radius * radius)
        answer = ptext(tail if relation == "≥" else 1 - tail)
    elif variant == "chebyshev_find_k":
        coverage = Fraction(re.search(r"≥(\d+(?:/\d+)?)", body).group(1))
        answer = f"k = {math.isqrt((1 / (1 - coverage)).numerator)}"
    elif variant == "boole_union_bound":
        probabilities = [Fraction(value) for value in
                         re.findall(r"P\(A\d+\)=(\d+(?:/\d+)?)", body)]
        answer = ptext(sum(probabilities, Fraction()))
    elif variant == "bonferroni_lower":
        values = [Fraction(value) for value in
                  re.findall(r"P\([AB]\)=(\d+(?:/\d+)?)", body)]
        answer = ptext(values[0] + values[1] - 1)
    elif variant in ("lln_bound", "lln_sample_size"):
        variance = int(re.search(r"variance (\d+)", body).group(1))
        epsilon = Fraction(re.search(r"ε=(\d+(?:/\d+)?)", body).group(1))
        if variant == "lln_bound":
            n = int(re.search(r"sample size n=(\d+)", body).group(1))
            answer = ptext(Fraction(variance, 1) / (n * epsilon ** 2))
        else:
            delta = Fraction(re.search(r"≤(\d+(?:/\d+)?)", body).group(1))
            answer = f"n = {ceil_fraction(Fraction(variance, 1)/(delta*epsilon**2))}"
    else:
        rows = [(int(x), Fraction(p)) for x, p in
                re.findall(r"P\(X=(\d+)\)=(\d+(?:/\d+)?)", body)]
        threshold = int(re.search(r"Target: P\(X≥(\d+)\)", body).group(1))
        mean = sum((x * p for x, p in rows), Fraction())
        exact = sum((p for x, p in rows if x >= threshold), Fraction())
        answer = f"bound {ptext(mean/threshold)}; exact {ptext(exact)}"
    return {"variant": variant, "query": query, "answer": answer}


class ProbabilityInequalityGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(965201)

    def test_output_contract(self):
        example = ProbabilityInequalityGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ProbabilityInequalityGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_ceiling_steps_are_exact(self):
        generator = ProbabilityInequalityGenerator()
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
                elif fields[0] == "CEIL":
                    self.assertEqual(ceil_fraction(Fraction(fields[1])), int(fields[2]))

    def test_compare_exact_never_exceeds_markov_bound(self):
        generator = ProbabilityInequalityGenerator("compare_exact")
        for _ in range(150):
            match = re.fullmatch(r"bound ([0-9/]+); exact ([0-9/]+)",
                                 generator.generate()["final_answer"])
            self.assertLessEqual(Fraction(match.group(2)), Fraction(match.group(1)))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ProbabilityInequalityGenerator.VARIANTS:
            generator = ProbabilityInequalityGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_inequality_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ProbabilityInequalityGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ProbabilityInequalityGenerator()
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
