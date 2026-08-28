"""Problem-text oracles for every MethodOfMomentsGenerator variant."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.method_of_moments_generator import (
    STATISTICS,
    MethodOfMomentsGenerator,
)
from helpers import DELIM


DATA_RE = re.compile(r"data \[(-?\d+(?:,-?\d+)*)\]")


def exact(value):
    return str(Fraction(value))


def values_from_problem(problem):
    match = DATA_RE.search(problem)
    if not match:
        raise AssertionError(f"cannot parse data from: {problem}")
    return [int(part) for part in match.group(1).split(",")]


def moments(problem):
    values = values_from_problem(problem)
    n = len(values)
    mean = Fraction(sum(values), n)
    second = Fraction(sum(value * value for value in values), n)
    return values, mean, second


def oracle(problem):
    values, mean, second = moments(problem)
    if "Poisson(lambda)" in problem:
        return f"xbar={exact(mean)}; lambda_hat={exact(mean)}"
    if "Exponential(lambda)" in problem:
        estimate = Fraction(len(values), sum(values))
        return f"xbar={exact(mean)}; lambda_hat={exact(estimate)}"
    if "Uniform(0,theta)" in problem:
        return f"xbar={exact(mean)}; theta_hat={exact(2 * mean)}"

    variance = second - mean * mean
    if problem.startswith("For normal data"):
        return (f"xbar={exact(mean)}; m2={exact(second)}; "
                f"mu_hat={exact(mean)}; sigma2_hat={exact(variance)}")
    if "Gamma(alpha,beta)" in problem:
        alpha = mean * mean / variance
        beta = mean / variance
        return (f"xbar={exact(mean)}; m2={exact(second)}; "
                f"alpha_hat={exact(alpha)}; beta_hat={exact(beta)}")
    if "Uniform(a,b)" in problem:
        radicand = 3 * variance
        numerator_root = math.isqrt(radicand.numerator)
        denominator_root = math.isqrt(radicand.denominator)
        if (numerator_root * numerator_root != radicand.numerator or
                denominator_root * denominator_root != radicand.denominator):
            raise AssertionError(f"non-square endpoint radicand: {radicand}")
        radius = Fraction(numerator_root, denominator_root)
        return (f"xbar={exact(mean)}; m2={exact(second)}; "
                f"a_hat={exact(mean - radius)}; "
                f"b_hat={exact(mean + radius)}")
    raise AssertionError(f"unrecognized problem: {problem}")


def assert_arithmetic(testcase, raw_step):
    fields = raw_step.split(DELIM)
    code = fields[0]
    if code == "A":
        testcase.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "S":
        testcase.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "M":
        testcase.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "D":
        testcase.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "E":
        testcase.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "ROOT":
        testcase.assertEqual(Fraction(fields[2]) ** 2,
                             Fraction(fields[1]), raw_step)
    elif code == "SUM":
        terms = [Fraction(term.strip()) for term in fields[2].split("+")]
        testcase.assertEqual(sum(terms, Fraction()),
                             Fraction(fields[3]), raw_step)


class TestMethodOfMomentsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MethodOfMomentsGenerator()

    def test_statistics_marker(self):
        self.assertIs(STATISTICS, True)

    def test_output_contract(self):
        result = self.gen.generate()
        self.assertEqual(
            set(result),
            {"problem_id", "operation", "problem", "steps", "final_answer"},
        )
        self.assertEqual(result["steps"][-1],
                         f"Z{DELIM}{result['final_answer']}")

    def test_oracle_recomputes_answer_from_problem_text(self):
        random.seed(7319)
        seen = set()
        for _ in range(1000):
            result = self.gen.generate()
            seen.add(result["operation"])
            self.assertEqual(result["final_answer"], oracle(result["problem"]),
                             result["problem"])
        self.assertEqual(
            seen,
            {f"method_of_moments_{variant}"
             for variant in MethodOfMomentsGenerator.VARIANTS},
        )

    def test_all_variants_and_invalid_variant(self):
        for variant in MethodOfMomentsGenerator.VARIANTS:
            result = MethodOfMomentsGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"method_of_moments_{variant}")
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
        with self.assertRaises(ValueError):
            MethodOfMomentsGenerator("bogus")

    def test_emitted_arithmetic(self):
        random.seed(992)
        for _ in range(500):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                assert_arithmetic(self, raw_step)

    def test_sample_moments_match_problem_data(self):
        for variant in ("normal_two_param", "gamma_two_param", "uniform_a_b"):
            gen = MethodOfMomentsGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                _, mean, second = moments(result["problem"])
                sample_moments = {
                    fields[1]: fields[2]
                    for fields in (step_text.split(DELIM)
                                   for step_text in result["steps"])
                    if fields[0] == "SAMPLE_MOMENT"
                }
                self.assertEqual(Fraction(sample_moments["xbar"]), mean)
                self.assertEqual(
                    Fraction(sample_moments["m2=(1/n)sum x_i^2"]), second
                )

    def test_two_parameter_estimates_have_valid_domains(self):
        for variant in ("normal_two_param", "gamma_two_param", "uniform_a_b"):
            gen = MethodOfMomentsGenerator(variant)
            for _ in range(150):
                result = gen.generate()
                _, mean, second = moments(result["problem"])
                variance = second - mean * mean
                self.assertGreater(variance, 0)
                if variant == "gamma_two_param":
                    self.assertGreater(mean * mean / variance, 0)
                    self.assertGreater(mean / variance, 0)
                elif variant == "uniform_a_b":
                    answer = result["final_answer"]
                    a_hat = Fraction(re.search(r"a_hat=([^;]+)", answer).group(1))
                    b_hat = Fraction(re.search(r"b_hat=([^;]+)", answer).group(1))
                    self.assertLess(a_hat, b_hat)

    def test_uniform_endpoint_exactness_patterns(self):
        gen = MethodOfMomentsGenerator("uniform_a_b")
        observed_variances = set()
        for _ in range(300):
            result = gen.generate()
            _, mean, second = moments(result["problem"])
            variance = second - mean * mean
            observed_variances.add(variance)
            root = math.isqrt((3 * variance).numerator)
            self.assertEqual(root * root, (3 * variance).numerator)
            self.assertEqual((3 * variance).denominator, 1)
        self.assertEqual(observed_variances, {Fraction(3), Fraction(12)})

    def test_rate_parameterization_is_stated(self):
        for _ in range(100):
            result = MethodOfMomentsGenerator("gamma_two_param").generate()
            self.assertIn("beta is the rate parameter", result["problem"])

    def test_pipe_and_render_safety(self):
        # ``+ 0`` is legitimate here when a sampled Poisson observation is 0.
        bad_patterns = (r"\b1x\b", r"\b-1x\b", r"\^1\b", r"--")
        for _ in range(500):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["final_answer"])
            rendered = result["problem"] + " " + " ".join(result["steps"])
            for pattern in bad_patterns:
                self.assertIsNone(re.search(pattern, rendered), rendered)
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
