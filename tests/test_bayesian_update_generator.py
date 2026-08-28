"""Independent problem-text oracles for BayesianUpdateGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.bayesian_update_generator import (
    STATISTICS,
    BayesianUpdateGenerator,
)
from helpers import DELIM


BETA_RE = re.compile(
    r"Start with a Beta\((\d+),(\d+)\) prior for Bernoulli p\. After "
    r"(\d+) successes in (\d+) trials,"
)
NORMAL_RE = re.compile(
    r"For data \[([-0-9,]+)\] from Normal\(mu, sigma\^2=(\d+)\) with "
    r"prior mu~Normal\((-?\d+), tau\^2=(\d+)\),"
)
GAMMA_RE = re.compile(
    r"A Poisson rate lambda has prior Gamma\(alpha=(\d+), beta=(\d+)\), "
    r"using the shape-rate parameterization\. Given counts "
    r"\[([0-9,]+)\],"
)


def exact(value):
    return str(Fraction(value))


def parse_ints(raw):
    return [int(part) for part in raw.split(",")]


def normal_posterior(problem):
    match = NORMAL_RE.match(problem)
    if not match:
        raise AssertionError(f"cannot parse normal problem: {problem}")
    values = parse_ints(match.group(1))
    sigma_sq = int(match.group(2))
    mu0 = int(match.group(3))
    tau_sq = int(match.group(4))
    prior_precision = Fraction(1, tau_sq)
    data_precision = Fraction(len(values), sigma_sq)
    post_precision = prior_precision + data_precision
    weighted_total = Fraction(mu0, tau_sq) + Fraction(sum(values), sigma_sq)
    post_mean = weighted_total / post_precision
    post_variance = Fraction(1, 1) / post_precision
    return post_mean, post_variance, sigma_sq


def oracle(problem):
    gamma_match = GAMMA_RE.match(problem)
    if gamma_match:
        alpha = int(gamma_match.group(1))
        beta = int(gamma_match.group(2))
        values = parse_ints(gamma_match.group(3))
        post_alpha = alpha + sum(values)
        post_beta = beta + len(values)
        return (f"posterior=Gamma({post_alpha},{post_beta}) rate; "
                f"posterior_mean={exact(Fraction(post_alpha, post_beta))}")

    beta_match = BETA_RE.match(problem)
    if beta_match:
        alpha, beta, successes, n = map(int, beta_match.groups())
        failures = n - successes
        post_alpha = alpha + successes
        post_beta = beta + failures
        if "interior MAP estimate" in problem:
            estimate = Fraction(post_alpha - 1,
                                post_alpha + post_beta - 2)
            return (f"posterior=Beta({post_alpha},{post_beta}); "
                    f"MAP={exact(estimate)}")
        posterior_mean = Fraction(post_alpha, post_alpha + post_beta)
        if "posterior predictive probability" in problem:
            return (f"posterior=Beta({post_alpha},{post_beta}); "
                    f"P(next success)={exact(posterior_mean)}")
        return (f"posterior=Beta({post_alpha},{post_beta}); "
                f"posterior_mean={exact(posterior_mean)}")

    post_mean, post_variance, sigma_sq = normal_posterior(problem)
    if "posterior predictive distribution" in problem:
        predictive_variance = post_variance + sigma_sq
        return (f"posterior_mean={exact(post_mean)}; "
                f"posterior_variance={exact(post_variance)}; "
                f"predictive_mean={exact(post_mean)}; "
                f"predictive_variance={exact(predictive_variance)}")
    return (f"posterior=Normal(mean={exact(post_mean)}, "
            f"variance={exact(post_variance)})")


def assert_arithmetic(testcase, raw_step):
    fields = raw_step.split(DELIM)
    code = fields[0]
    if code == "A":
        testcase.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "S":
        testcase.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "D":
        testcase.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                             Fraction(fields[3]), raw_step)
    elif code == "SUM":
        terms = [Fraction(term.strip()) for term in fields[2].split("+")]
        testcase.assertEqual(sum(terms, Fraction()),
                             Fraction(fields[3]), raw_step)


class TestBayesianUpdateGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BayesianUpdateGenerator()

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
        random.seed(4227)
        seen = set()
        for _ in range(1000):
            result = self.gen.generate()
            seen.add(result["operation"])
            self.assertEqual(result["final_answer"], oracle(result["problem"]),
                             result["problem"])
        self.assertEqual(
            seen,
            {f"bayesian_update_{variant}"
             for variant in BayesianUpdateGenerator.VARIANTS},
        )

    def test_all_variants_and_invalid_variant(self):
        for variant in BayesianUpdateGenerator.VARIANTS:
            result = BayesianUpdateGenerator(variant).generate()
            self.assertEqual(result["operation"], f"bayesian_update_{variant}")
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
        with self.assertRaises(ValueError):
            BayesianUpdateGenerator("bogus")

    def test_emitted_arithmetic(self):
        random.seed(887)
        for _ in range(600):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                assert_arithmetic(self, raw_step)

    def test_gamma_rate_parameterization_and_update(self):
        gen = BayesianUpdateGenerator("gamma_poisson")
        for _ in range(150):
            result = gen.generate()
            self.assertIn("shape-rate parameterization", result["problem"])
            self.assertRegex(result["final_answer"],
                             r"posterior=Gamma\(\d+,\d+\) rate")

    def test_beta_map_is_interior_and_uses_mode_formula(self):
        gen = BayesianUpdateGenerator("beta_map")
        for _ in range(150):
            result = gen.generate()
            match = re.search(r"posterior=Beta\((\d+),(\d+)\); MAP=([^;]+)$",
                              result["final_answer"])
            post_alpha, post_beta = int(match.group(1)), int(match.group(2))
            estimate = Fraction(match.group(3))
            self.assertGreater(post_alpha, 1)
            self.assertGreater(post_beta, 1)
            self.assertEqual(estimate,
                             Fraction(post_alpha - 1,
                                      post_alpha + post_beta - 2))
            self.assertGreater(estimate, 0)
            self.assertLess(estimate, 1)

    def test_beta_predictive_is_probability(self):
        gen = BayesianUpdateGenerator("beta_predictive")
        for _ in range(150):
            result = gen.generate()
            probability = Fraction(result["final_answer"].rsplit("=", 1)[1])
            self.assertGreaterEqual(probability, 0)
            self.assertLessEqual(probability, 1)

    def test_normal_predictive_identity(self):
        gen = BayesianUpdateGenerator("normal_predictive_mean")
        for _ in range(150):
            result = gen.generate()
            post_mean, post_variance, sigma_sq = normal_posterior(
                result["problem"]
            )
            answer = result["final_answer"]
            predictive_mean = Fraction(
                re.search(r"predictive_mean=([^;]+)", answer).group(1)
            )
            predictive_variance = Fraction(
                re.search(r"predictive_variance=([^;]+)$", answer).group(1)
            )
            self.assertEqual(predictive_mean, post_mean)
            self.assertEqual(predictive_variance, post_variance + sigma_sq)

    def test_pipe_and_render_safety(self):
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
