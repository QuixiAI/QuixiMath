"""Exact conjugate Bayesian updates and posterior predictions.

Variants: ``beta_binomial``, ``normal_normal``, ``gamma_poisson``,
``beta_map``, ``beta_predictive``, and ``normal_predictive_mean``.  Gamma
models always state the rate parameterization, Beta MAP samples guarantee an
interior mode, and all normal precisions are rational.
Op-codes: ``BAYES_UPDATE_SETUP``, ``COUNT``, ``SUM``, ``PRIOR_PRECISION``,
``DATA_PRECISION``, ``POST_PRECISION``, ``POSTERIOR_PARAM``, ``MAP_ESTIMATE``,
``POSTERIOR_PREDICTIVE``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


STATISTICS = True


def fraction_text(value):
    return str(Fraction(value))


def data_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def sum_expr(values):
    return " + ".join(str(v) for v in values)


class BayesianUpdateGenerator(ProblemGenerator):
    """
    Mechanical conjugate Bayesian parameter updates.

    Variants:
    - beta_binomial: Beta(alpha,beta) prior with binomial data
    - normal_normal: known-variance normal data and normal prior on mu
    - gamma_poisson: Gamma shape/rate prior with Poisson data
    - beta_map: interior posterior mode after binomial data
    - beta_predictive: posterior predictive success probability
    - normal_predictive_mean: posterior predictive mean and variance

    Op-codes used:
    - BAYES_UPDATE_SETUP: prior, likelihood family, and data
    - COUNT / SUM: sufficient statistics
    - PRIOR_PRECISION / DATA_PRECISION / POST_PRECISION: normal-normal weights
    - POSTERIOR_PARAM: updated parameter value
    - MAP_ESTIMATE / POSTERIOR_PREDICTIVE: requested posterior summary
    - A / S / D / CHECK (established/shared): exact arithmetic
    - Z: posterior family and parameters
    """

    VARIANTS = ["beta_binomial", "normal_normal", "gamma_poisson",
                "beta_map", "beta_predictive", "normal_predictive_mean"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {
            "beta_binomial": self._generate_beta_binomial,
            "normal_normal": self._generate_normal_normal,
            "gamma_poisson": self._generate_gamma_poisson,
            "beta_map": self._generate_beta_map,
            "beta_predictive": self._generate_beta_predictive,
            "normal_predictive_mean": self._generate_normal_predictive,
        }
        problem, steps, answer = methods[variant]()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"bayesian_update_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_beta_binomial(self):
        alpha = random.randint(1, 12)
        beta = random.randint(1, 12)
        n = random.randint(4, 30)
        successes = random.randint(0, n)
        failures = n - successes
        post_alpha = alpha + successes
        post_beta = beta + failures
        post_total = post_alpha + post_beta
        post_mean = Fraction(post_alpha, post_total)
        steps = [
            step("BAYES_UPDATE_SETUP", "beta_binomial",
                 f"prior=Beta({alpha},{beta})",
                 f"successes={successes}, trials={n}"),
            step("S", n, successes, failures),
            step("POSTERIOR_PARAM", "alpha' = alpha + successes"),
            step("A", alpha, successes, post_alpha),
            step("POSTERIOR_PARAM", "beta' = beta + failures"),
            step("A", beta, failures, post_beta),
            step("A", post_alpha, post_beta, post_total),
            step("D", post_alpha, post_total, fraction_text(post_mean)),
        ]
        answer = (
            f"posterior=Beta({post_alpha},{post_beta}); "
            f"posterior_mean={fraction_text(post_mean)}"
        )
        problem = (
            f"Start with a Beta({alpha},{beta}) prior for Bernoulli p. "
            f"After {successes} successes in {n} trials, compute the "
            "conjugate posterior parameters and posterior mean."
        )
        return problem, steps, answer

    def _generate_normal_normal(self):
        n = random.randint(3, 8)
        values = [random.randint(-8, 12) for _ in range(n)]
        sigma_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9, 10])
        mu0 = random.randint(-6, 8)
        tau_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9, 10])
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
            step("BAYES_UPDATE_SETUP", "normal_normal",
                 f"prior=Normal({mu0},{tau_sq})",
                 f"sigma^2={sigma_sq}"),
            step("BAYES_UPDATE_SETUP", "data", data_text(values)),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("PRIOR_PRECISION", "1/tau^2"),
            step("D", 1, tau_sq, fraction_text(prior_precision)),
            step("DATA_PRECISION", "n/sigma^2"),
            step("D", n, sigma_sq, fraction_text(data_precision)),
            step("POST_PRECISION", "prior precision + data precision"),
            step("A", fraction_text(prior_precision),
                 fraction_text(data_precision),
                 fraction_text(post_precision)),
            step("D", mu0, tau_sq, fraction_text(prior_weighted)),
            step("D", total, sigma_sq, fraction_text(data_weighted)),
            step("A", fraction_text(prior_weighted),
                 fraction_text(data_weighted),
                 fraction_text(weighted_total)),
            step("D", fraction_text(weighted_total),
                 fraction_text(post_precision), fraction_text(post_mean)),
            step("D", 1, fraction_text(post_precision),
                 fraction_text(post_variance)),
        ]
        answer = (
            f"posterior=Normal(mean={fraction_text(post_mean)}, "
            f"variance={fraction_text(post_variance)})"
        )
        problem = (
            f"For data {data_text(values)} from Normal(mu, sigma^2={sigma_sq}) "
            f"with prior mu~Normal({mu0}, tau^2={tau_sq}), compute the "
            "conjugate posterior mean and variance."
        )
        return problem, steps, answer

    def _generate_gamma_poisson(self):
        alpha = random.randint(1, 12)
        beta = random.randint(1, 12)
        n = random.randint(3, 8)
        values = [random.randint(0, 9) for _ in range(n)]
        total = sum(values)
        post_alpha = alpha + total
        post_beta = beta + n
        post_mean = Fraction(post_alpha, post_beta)
        steps = [
            step("BAYES_UPDATE_SETUP", "gamma_poisson",
                 f"prior=Gamma(shape={alpha},rate={beta})",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("POSTERIOR_PARAM", "shape'=alpha+sum x_i"),
            step("A", alpha, total, post_alpha),
            step("POSTERIOR_PARAM", "rate'=beta+n"),
            step("A", beta, n, post_beta),
            step("D", post_alpha, post_beta, fraction_text(post_mean)),
            step("CHECK", f"shape'={post_alpha}>0", f"rate'={post_beta}>0"),
        ]
        answer = (f"posterior=Gamma({post_alpha},{post_beta}) rate; "
                  f"posterior_mean={fraction_text(post_mean)}")
        problem = (
            f"A Poisson rate lambda has prior Gamma(alpha={alpha}, "
            f"beta={beta}), using the shape-rate parameterization. Given "
            f"counts {data_text(values)}, find the conjugate posterior and "
            "its mean."
        )
        return problem, steps, answer

    def _generate_beta_map(self):
        alpha = random.randint(2, 12)
        beta = random.randint(2, 12)
        n = random.randint(4, 30)
        successes = random.randint(0, n)
        failures = n - successes
        post_alpha = alpha + successes
        post_beta = beta + failures
        alpha_minus = post_alpha - 1
        beta_minus = post_beta - 1
        denominator = alpha_minus + beta_minus
        estimate = Fraction(alpha_minus, denominator)
        steps = [
            step("BAYES_UPDATE_SETUP", "beta_map",
                 f"prior=Beta({alpha},{beta})",
                 f"successes={successes}, trials={n}"),
            step("S", n, successes, failures),
            step("A", alpha, successes, post_alpha),
            step("A", beta, failures, post_beta),
            step("POSTERIOR_PARAM", f"Beta({post_alpha},{post_beta})"),
            step("S", post_alpha, 1, alpha_minus),
            step("S", post_beta, 1, beta_minus),
            step("A", alpha_minus, beta_minus, denominator),
            step("D", alpha_minus, denominator, fraction_text(estimate)),
            step("MAP_ESTIMATE", "(alpha'-1)/(alpha'+beta'-2)",
                 fraction_text(estimate)),
            step("CHECK", f"alpha'={post_alpha}>1", f"beta'={post_beta}>1"),
        ]
        answer = (f"posterior=Beta({post_alpha},{post_beta}); "
                  f"MAP={fraction_text(estimate)}")
        problem = (
            f"Start with a Beta({alpha},{beta}) prior for Bernoulli p. After "
            f"{successes} successes in {n} trials, find the posterior and "
            "its interior MAP estimate."
        )
        return problem, steps, answer

    def _generate_beta_predictive(self):
        alpha = random.randint(1, 12)
        beta = random.randint(1, 12)
        n = random.randint(4, 30)
        successes = random.randint(0, n)
        failures = n - successes
        post_alpha = alpha + successes
        post_beta = beta + failures
        post_total = post_alpha + post_beta
        predictive = Fraction(post_alpha, post_total)
        steps = [
            step("BAYES_UPDATE_SETUP", "beta_predictive",
                 f"prior=Beta({alpha},{beta})",
                 f"successes={successes}, trials={n}"),
            step("S", n, successes, failures),
            step("A", alpha, successes, post_alpha),
            step("A", beta, failures, post_beta),
            step("POSTERIOR_PARAM", f"Beta({post_alpha},{post_beta})"),
            step("A", post_alpha, post_beta, post_total),
            step("D", post_alpha, post_total, fraction_text(predictive)),
            step("POSTERIOR_PREDICTIVE", "P(next success)=alpha'/(alpha'+beta')",
                 fraction_text(predictive)),
            step("CHECK", f"0<={fraction_text(predictive)}<=1",
                 "valid probability"),
        ]
        answer = (f"posterior=Beta({post_alpha},{post_beta}); "
                  f"P(next success)={fraction_text(predictive)}")
        problem = (
            f"Start with a Beta({alpha},{beta}) prior for Bernoulli p. After "
            f"{successes} successes in {n} trials, find the posterior and "
            "the posterior predictive probability of success on the next "
            "trial."
        )
        return problem, steps, answer

    def _generate_normal_predictive(self):
        n = random.randint(3, 8)
        values = [random.randint(-8, 12) for _ in range(n)]
        sigma_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9, 10])
        mu0 = random.randint(-6, 8)
        tau_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9, 10])
        total = sum(values)
        prior_precision = Fraction(1, tau_sq)
        data_precision = Fraction(n, sigma_sq)
        post_precision = prior_precision + data_precision
        prior_weighted = Fraction(mu0, tau_sq)
        data_weighted = Fraction(total, sigma_sq)
        weighted_total = prior_weighted + data_weighted
        post_mean = weighted_total / post_precision
        post_variance = Fraction(1, 1) / post_precision
        predictive_variance = post_variance + sigma_sq
        steps = [
            step("BAYES_UPDATE_SETUP", "normal_predictive",
                 f"prior=Normal({mu0},{tau_sq})", f"sigma^2={sigma_sq}"),
            step("BAYES_UPDATE_SETUP", "data", data_text(values)),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("PRIOR_PRECISION", "1/tau^2"),
            step("D", 1, tau_sq, fraction_text(prior_precision)),
            step("DATA_PRECISION", "n/sigma^2"),
            step("D", n, sigma_sq, fraction_text(data_precision)),
            step("POST_PRECISION", "prior precision + data precision"),
            step("A", fraction_text(prior_precision),
                 fraction_text(data_precision), fraction_text(post_precision)),
            step("D", mu0, tau_sq, fraction_text(prior_weighted)),
            step("D", total, sigma_sq, fraction_text(data_weighted)),
            step("A", fraction_text(prior_weighted),
                 fraction_text(data_weighted), fraction_text(weighted_total)),
            step("D", fraction_text(weighted_total),
                 fraction_text(post_precision), fraction_text(post_mean)),
            step("D", 1, fraction_text(post_precision),
                 fraction_text(post_variance)),
            step("A", fraction_text(post_variance), sigma_sq,
                 fraction_text(predictive_variance)),
            step("POSTERIOR_PREDICTIVE", "Normal",
                 f"mean={fraction_text(post_mean)}",
                 f"variance={fraction_text(predictive_variance)}"),
            step("CHECK", f"predictive variance={fraction_text(predictive_variance)}>0"),
        ]
        answer = (f"posterior_mean={fraction_text(post_mean)}; "
                  f"posterior_variance={fraction_text(post_variance)}; "
                  f"predictive_mean={fraction_text(post_mean)}; "
                  f"predictive_variance={fraction_text(predictive_variance)}")
        problem = (
            f"For data {data_text(values)} from Normal(mu, sigma^2={sigma_sq}) "
            f"with prior mu~Normal({mu0}, tau^2={tau_sq}), find the posterior "
            "mean and variance, then the mean and variance of the posterior "
            "predictive distribution for one new observation."
        )
        return problem, steps, answer
