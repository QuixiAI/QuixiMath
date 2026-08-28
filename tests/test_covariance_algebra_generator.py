"""Independent exact oracle for CovarianceAlgebraGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.covariance_algebra_generator import (
    QUERIES, CovarianceAlgebraGenerator,
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


def parse_moments(body):
    match = re.search(
        r"Var\(X\) = (-?\d+(?:/\d+)?), Var\(Y\) = (-?\d+(?:/\d+)?), and "
        r"Cov\(X,Y\) = (-?\d+(?:/\d+)?)", body)
    assert match is not None, body
    return tuple(Fraction(value) for value in match.groups())


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "var_sum_independent":
        values = [Fraction(value) for value in
                  re.findall(r"Var\(X\d+\)=(-?\d+(?:/\d+)?)", body)]
        answer = ptext(sum(values, Fraction()))
    elif variant == "cov_from_table_3x3":
        rows = [(int(x), int(y), Fraction(p)) for x, y, p in
                re.findall(r"P\(X=(\d+),Y=(\d+)\)=(-?\d+(?:/\d+)?)", body)]
        assert len(rows) == 9 and sum((p for _, _, p in rows), Fraction()) == 1
        ex = sum((x * p for x, _, p in rows), Fraction())
        ey = sum((y * p for _, y, p in rows), Fraction())
        exy = sum((x * y * p for x, y, p in rows), Fraction())
        answer = ptext(exy - ex * ey)
    else:
        vx, vy, covariance = parse_moments(body)
        if variant == "var_linear_combo":
            match = re.search(r"Coefficients are a=(-?\d+), b=(-?\d+)", body)
            a, b = map(int, match.groups())
            answer = ptext(a * a * vx + b * b * vy + 2 * a * b * covariance)
        elif variant == "cov_bilinear":
            match = re.search(
                r"Coefficients are a=(-?\d+), b=(-?\d+), c=(-?\d+), d=(-?\d+)",
                body)
            a, b, c, d = map(int, match.groups())
            answer = ptext(a * c * vx + b * d * vy
                           + (a * d + b * c) * covariance)
        elif variant == "corr_from_cov":
            sx, sy = math.isqrt(vx.numerator), math.isqrt(vy.numerator)
            assert vx.denominator == vy.denominator == 1
            assert sx * sx == vx and sy * sy == vy
            answer = ptext(covariance / (sx * sy))
        elif variant == "var_difference":
            answer = ptext(vx + vy - 2 * covariance)
        else:
            answer = ptext(vx + covariance)
    return {"variant": variant, "query": query, "answer": answer}


class CovarianceAlgebraGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(731504)

    def test_output_contract(self):
        example = CovarianceAlgebraGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CovarianceAlgebraGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_power_and_root_steps_are_exact(self):
        generator = CovarianceAlgebraGenerator()
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

    def test_variance_variants_are_nonnegative(self):
        for variant in ("var_linear_combo", "var_sum_independent",
                        "var_difference"):
            generator = CovarianceAlgebraGenerator(variant)
            for _ in range(150):
                self.assertGreaterEqual(Fraction(generator.generate()["final_answer"]), 0)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CovarianceAlgebraGenerator.VARIANTS:
            generator = CovarianceAlgebraGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_covariance_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CovarianceAlgebraGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CovarianceAlgebraGenerator()
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
