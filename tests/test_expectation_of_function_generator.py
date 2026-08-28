"""Independent finite-sum oracle for ExpectationOfFunctionGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.expectation_of_function_generator import (
    QUERIES, ExpectationOfFunctionGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_pmf(text):
    rows = []
    for item in text.split("; "):
        match = re.fullmatch(r"P\(X=(-?\d+)\) = (\d+(?:/\d+)?)", item)
        assert match is not None, item
        rows.append((int(match.group(1)), Fraction(match.group(2))))
    assert sum((p for _, p in rows), Fraction()) == 1
    return rows


def raw_moments(rows):
    mean = sum((Fraction(x) * p for x, p in rows), Fraction())
    second = sum((Fraction(x * x) * p for x, p in rows), Fraction())
    variance = sum(((Fraction(x) - mean) ** 2 * p for x, p in rows), Fraction())
    return mean, second, variance


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "e_g_x":
        match = re.fullmatch(r"X has pmf: (.+)\. Let g\(x\) = (.+)\.", body)
        assert match is not None, body
        rows, rule = parse_pmf(match.group(1)), match.group(2)
        if rule == "x²":
            function = lambda x: Fraction(x * x)
        elif rule == "1/x":
            function = lambda x: Fraction(1, x)
        elif rule.startswith("abs("):
            inner = rule[4:-1]
            if " − " in inner:
                c = int(inner.split(" − ")[1])
            else:
                c = -int(inner.split(" + ")[1])
            function = lambda x: Fraction(abs(x - c))
        else:
            affine = re.fullmatch(r"(-?\d+)x(?: ([+−]) (\d+))?", rule)
            assert affine is not None, rule
            a = int(affine.group(1))
            b = (int(affine.group(3)) * (1 if affine.group(2) == "+" else -1)
                 if affine.group(2) else 0)
            function = lambda x: Fraction(a * x + b)
        value = sum((function(x) * p for x, p in rows), Fraction())
        answer = f"E[g(X)] = {ptext(value)}"
    else:
        if variant == "linear_mean_var":
            match = re.fullmatch(r"X has pmf: (.+)\. Define Y = (.+)\.", body)
            assert match is not None, body
            rows = parse_pmf(match.group(1))
            expression = match.group(2)
            affine = re.fullmatch(r"([−-]?\d*)X(?: ([+−]) (\d+))?", expression)
            assert affine is not None, expression
            raw_a = affine.group(1)
            a = -1 if raw_a == "−" else 1 if raw_a == "" else int(raw_a)
            b = (int(affine.group(3)) * (1 if affine.group(2) == "+" else -1)
                 if affine.group(2) else 0)
            transformed = [(a * x + b, p) for x, p in rows]
            mean, _, variance = raw_moments(transformed)
            answer = f"E[Y] = {ptext(mean)}; Var(Y) = {ptext(variance)}"
            value = variance
        elif variant == "standardize":
            match = re.fullmatch(r"X has pmf: (.+)\. Standardize x = (-?\d+)\.", body)
            assert match is not None, body
            rows, observation = parse_pmf(match.group(1)), int(match.group(2))
            mean, _, variance = raw_moments(rows)
            sigma = math.isqrt(variance.numerator)
            assert variance.denominator == 1 and sigma * sigma == variance
            z = (Fraction(observation) - mean) / sigma
            answer = f"μ = {ptext(mean)}; σ = {sigma}; z = {ptext(z)}"
            value = z
        else:
            match = re.fullmatch(r"X has pmf: (.+)\.", body)
            assert match is not None, body
            rows = parse_pmf(match.group(1))
            mean, second, variance = raw_moments(rows)
            if variant == "var_shortcut":
                answer = f"E[X²] = {ptext(second)}; Var(X) = {ptext(variance)}"
            else:
                answer = f"shortcut {ptext(variance)}; definition {ptext(variance)}"
            value = variance
    return {"variant": variant, "query": query, "answer": answer, "value": value}


class ExpectationOfFunctionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(374166)

    def test_output_contract(self):
        example = ExpectationOfFunctionGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = ExpectationOfFunctionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = ExpectationOfFunctionGenerator()
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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                     Fraction(fields[1]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in ExpectationOfFunctionGenerator.VARIANTS:
            generator = ExpectationOfFunctionGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_expectation_function_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ExpectationOfFunctionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = ExpectationOfFunctionGenerator()
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
