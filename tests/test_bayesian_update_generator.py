import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bayesian_update_generator import (
    BayesianUpdateGenerator,
    data_text,
    sum_expr,
)
from helpers import DELIM


BETA_RE = re.compile(
    r"Start with a Beta\((\d+),(\d+)\) prior for Bernoulli p\. After "
    r"(\d+) successes in (\d+) trials, compute the conjugate posterior "
    r"parameters and posterior mean\."
)
NORMAL_RE = re.compile(
    r"For data \[([-0-9,]+)\] from Normal\(mu, sigma\^2=(\d+)\) with "
    r"prior mu~Normal\((-?\d+), tau\^2=(\d+)\), compute the conjugate "
    r"posterior mean and variance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_values(raw):
    return [int(part) for part in raw.split(",")]


def expected_beta(problem):
    alpha, beta, successes, n = (
        int(value) for value in BETA_RE.fullmatch(problem).groups()
    )
    failures = n - successes
    post_alpha = alpha + successes
    post_beta = beta + failures
    post_total = post_alpha + post_beta
    post_mean = Fraction(post_alpha, post_total)
    steps = [
        make_step("BAYES_UPDATE_SETUP", "beta_binomial",
                  f"prior=Beta({alpha},{beta})",
                  f"successes={successes}, trials={n}"),
        make_step("S", n, successes, failures),
        make_step("POSTERIOR_PARAM", "alpha' = alpha + successes"),
        make_step("A", alpha, successes, post_alpha),
        make_step("POSTERIOR_PARAM", "beta' = beta + failures"),
        make_step("A", beta, failures, post_beta),
        make_step("A", post_alpha, post_beta, post_total),
        make_step("D", post_alpha, post_total, fraction_text(post_mean)),
    ]
    answer = (
        f"posterior=Beta({post_alpha},{post_beta}); "
        f"posterior_mean={fraction_text(post_mean)}"
    )
    return steps, answer


def expected_normal(problem):
    match = NORMAL_RE.fullmatch(problem)
    values = parse_values(match.group(1))
    sigma_sq = int(match.group(2))
    mu0 = int(match.group(3))
    tau_sq = int(match.group(4))
    n = len(values)
    total = sum(values)
    prior_precision = Fraction(1, tau_sq)
    data_precision = Fraction(n, sigma_sq)
    post_precision = prior_precision + data_precision
    prior_weighted = Fraction(mu0, tau_sq)
    data_weighted = Fraction(total, sigma_sq)
    weighted_total = prior_weighted + data_weighted
    post_mean = weighted_total / post_precision
    post_variance = Fraction(1, 1) / post_precision
    steps = [
        make_step("BAYES_UPDATE_SETUP", "normal_normal",
                  f"prior=Normal({mu0},{tau_sq})",
                  f"sigma^2={sigma_sq}"),
        make_step("BAYES_UPDATE_SETUP", "data", data_text(values)),
        make_step("COUNT", "n", n),
        make_step("SUM", "sum x_i", sum_expr(values), total),
        make_step("PRIOR_PRECISION", "1/tau^2"),
        make_step("D", 1, tau_sq, fraction_text(prior_precision)),
        make_step("DATA_PRECISION", "n/sigma^2"),
        make_step("D", n, sigma_sq, fraction_text(data_precision)),
        make_step("POST_PRECISION", "prior precision + data precision"),
        make_step("A", fraction_text(prior_precision),
                  fraction_text(data_precision),
                  fraction_text(post_precision)),
        make_step("D", mu0, tau_sq, fraction_text(prior_weighted)),
        make_step("D", total, sigma_sq, fraction_text(data_weighted)),
        make_step("A", fraction_text(prior_weighted),
                  fraction_text(data_weighted),
                  fraction_text(weighted_total)),
        make_step("D", fraction_text(weighted_total),
                  fraction_text(post_precision), fraction_text(post_mean)),
        make_step("D", 1, fraction_text(post_precision),
                  fraction_text(post_variance)),
    ]
    answer = (
        f"posterior=Normal(mean={fraction_text(post_mean)}, "
        f"variance={fraction_text(post_variance)})"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if BETA_RE.fullmatch(problem):
        steps, answer = expected_beta(problem)
    else:
        steps, answer = expected_normal(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBayesianUpdateGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BayesianUpdateGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "SUM":
                    values = [int(v) for v in re.findall(r"-?\d+", fields[2])]
                    self.assertEqual(sum(values), int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in BayesianUpdateGenerator.VARIANTS:
            result = BayesianUpdateGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"bayesian_update_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BayesianUpdateGenerator("bogus")

    def test_posterior_variances_and_means_are_valid(self):
        beta_gen = BayesianUpdateGenerator("beta_binomial")
        for _ in range(100):
            result = beta_gen.generate()
            mean = Fraction(result["final_answer"].rsplit("=", 1)[1])
            self.assertGreaterEqual(mean, 0)
            self.assertLessEqual(mean, 1)
        normal_gen = BayesianUpdateGenerator("normal_normal")
        for _ in range(100):
            result = normal_gen.generate()
            variance = Fraction(re.search(
                r"variance=([^)]+)\)", result["final_answer"]
            ).group(1))
            self.assertGreater(variance, 0)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
