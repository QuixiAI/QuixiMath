"""Exact maximum-likelihood calculations from score or boundary arguments.

Variants: ``bernoulli``, ``exponential``, ``normal_mu``, ``normal_sigma2``,
``poisson``, ``uniform_theta``, ``geometric``, and ``binomial_n_known``.
Normal two-parameter data come from zero-sum deviation patterns with SS/n an
integer; all remaining estimates are exact fractions or an observed boundary.
Op-codes: ``MLE_SETUP``, ``COUNT``, ``SUM``, ``DEV_ROW``, ``MAX``,
``LOG_LIKELIHOOD``, ``DERIVATIVE``, ``SCORE_EQ``, ``REWRITE``,
``BOUNDARY_MLE``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from stats_common import patterns


STATISTICS = True


def fraction_text(value):
    return str(Fraction(value))


def data_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def sum_expr(values):
    return " + ".join(str(v) for v in values)


class MLEGenerator(ProblemGenerator):
    """
    Maximum-likelihood estimates from log-likelihood score equations.

    Variants include the three original score-equation cases plus normal
    mean/variance, Poisson, uniform endpoint, geometric, and known-n binomial.

    Op-codes used:
    - MLE_SETUP: model, parameter, and data
    - COUNT / SUM: sufficient statistics
    - LOG_LIKELIHOOD: log-likelihood up to standard constants
    - DERIVATIVE: score function
    - SCORE_EQ: score equation set to zero
    - REWRITE: simplified estimating equation
    - A / S / D (established/shared): exact arithmetic
    - CHECK: parameter-domain check
    - DEV_ROW / MAX / BOUNDARY_MLE: explicit variance and endpoint work
    - M: total known binomial trials
    - Z: log-likelihood, score, or boundary MLE
    """

    VARIANTS = ["bernoulli", "exponential", "normal_mu", "normal_sigma2",
                "poisson", "uniform_theta", "geometric",
                "binomial_n_known"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {
            "bernoulli": self._generate_bernoulli,
            "exponential": self._generate_exponential,
            "normal_mu": self._generate_normal_mu,
            "normal_sigma2": self._generate_normal_sigma2,
            "poisson": self._generate_poisson,
            "uniform_theta": self._generate_uniform_theta,
            "geometric": self._generate_geometric,
            "binomial_n_known": self._generate_binomial_n_known,
        }
        problem, steps, answer = methods[variant]()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"mle_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_bernoulli(self):
        n = random.randint(5, 18)
        successes = random.randint(1, n - 1)
        values = [1] * successes + [0] * (n - successes)
        random.shuffle(values)
        failures = n - successes
        p_hat = Fraction(successes, n)
        loglik = f"ell(p)={successes}*log(p)+{failures}*log(1-p)"
        score = f"score={successes}/p-{failures}/(1-p)"
        steps = [
            step("MLE_SETUP", "bernoulli", "parameter=p",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("COUNT", "sum x_i", successes),
            step("S", n, successes, failures),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{successes}/p={failures}/(1-p)"),
            step("REWRITE", f"{successes}={n}*p"),
            step("D", successes, n, fraction_text(p_hat)),
            step("CHECK", f"0<={fraction_text(p_hat)}<=1",
                 "valid Bernoulli parameter"),
        ]
        answer = f"{loglik}; {score}; p_hat={fraction_text(p_hat)}"
        problem = (
            f"For Bernoulli data {data_text(values)}, write the "
            "log-likelihood for p, differentiate, and solve for the MLE "
            "p_hat."
        )
        return problem, steps, answer

    def _generate_exponential(self):
        n = random.randint(3, 9)
        values = [random.randint(1, 12) for _ in range(n)]
        total = sum(values)
        lambda_hat = Fraction(n, total)
        loglik = f"ell(lambda)={n}*log(lambda)-{total}*lambda"
        score = f"score={n}/lambda-{total}"
        steps = [
            step("MLE_SETUP", "exponential", "parameter=lambda",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{n}/lambda={total}"),
            step("D", n, total, fraction_text(lambda_hat)),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                 "valid rate parameter"),
        ]
        answer = (
            f"{loglik}; {score}; lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For exponential data {data_text(values)}, write the "
            "log-likelihood for lambda, differentiate, and solve for the "
            "MLE lambda_hat."
        )
        return problem, steps, answer

    def _generate_normal_mu(self):
        n = random.randint(3, 9)
        values = [random.randint(-8, 12) for _ in range(n)]
        sigma_sq = random.choice([1, 2, 3, 4, 5, 6, 8, 9])
        total = sum(values)
        mu_hat = Fraction(total, n)
        loglik = f"ell(mu)=-(1/(2*{sigma_sq}))*sum((x_i-mu)^2)+C"
        score = f"score=({total}-{n}*mu)/{sigma_sq}"
        steps = [
            step("MLE_SETUP", "normal_mu", "parameter=mu",
                 f"sigma^2={sigma_sq}"),
            step("MLE_SETUP", "data", data_text(values)),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{total}-{n}*mu=0"),
            step("REWRITE", f"{total}={n}*mu"),
            step("D", total, n, fraction_text(mu_hat)),
            step("CHECK", "mu_hat can be any real number",
                 fraction_text(mu_hat)),
        ]
        answer = f"{loglik}; {score}; mu_hat={fraction_text(mu_hat)}"
        problem = (
            f"For normal data {data_text(values)} with known "
            f"sigma^2={sigma_sq}, write the log-likelihood for mu, "
            "differentiate, and solve for the MLE mu_hat."
        )
        return problem, steps, answer

    def _generate_normal_sigma2(self):
        n = random.randint(4, 8)
        candidates = []
        for pattern in patterns(n, max_abs=6):
            ss = sum(deviation ** 2 for deviation in pattern)
            if ss % n == 0:
                candidates.append((pattern, ss))
        deviations, ss = random.choice(candidates)
        center = random.randint(max(5, 1 - min(deviations)), 30)
        values = [center + deviation for deviation in deviations]
        random.shuffle(values)
        total = sum(values)
        mu_hat = Fraction(total, n)
        sigma2_hat = Fraction(ss, n)
        steps = [
            step("MLE_SETUP", "normal_sigma2", "parameters=mu,sigma^2",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("D", total, n, fraction_text(mu_hat)),
            step("LOG_LIKELIHOOD",
                 "ell(mu,sigma^2)=-(n/2)log(sigma^2)-SS(mu)/(2sigma^2)+C"),
            step("DERIVATIVE", "score_mu=sum(x_i-mu)/sigma^2"),
            step("SCORE_EQ", f"mu_hat={fraction_text(mu_hat)}"),
        ]
        squares = []
        for value in values:
            deviation = Fraction(value) - mu_hat
            square = deviation ** 2
            squares.append(square)
            steps.append(step("DEV_ROW", value, fraction_text(deviation),
                              fraction_text(square)))
        steps.extend([
            step("SUM", "SS", " + ".join(fraction_text(v) for v in squares), ss),
            step("DERIVATIVE", "score_sigma2=-n/(2sigma^2)+SS/(2sigma^4)"),
            step("SCORE_EQ", "sigma2_hat=SS/n"),
            step("D", ss, n, fraction_text(sigma2_hat)),
            step("CHECK", f"sigma2_hat={fraction_text(sigma2_hat)}>0",
                 "valid variance parameter"),
        ])
        answer = (f"mu_hat={fraction_text(mu_hat)}; SS={ss}; "
                  f"sigma2_hat={fraction_text(sigma2_hat)}")
        problem = (
            f"For normal data {data_text(values)} with both mu and sigma^2 "
            "unknown, find the MLEs mu_hat and sigma2_hat=SS/n."
        )
        return problem, steps, answer

    def _generate_poisson(self):
        n = random.randint(3, 10)
        values = [random.randint(0, 9) for _ in range(n)]
        if sum(values) == 0:
            values[random.randrange(n)] = random.randint(1, 9)
        total = sum(values)
        lambda_hat = Fraction(total, n)
        loglik = f"ell(lambda)={total}*log(lambda)-{n}*lambda+C"
        score = f"score={total}/lambda-{n}"
        steps = [
            step("MLE_SETUP", "poisson", "parameter=lambda",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"{total}/lambda={n}"),
            step("D", total, n, fraction_text(lambda_hat)),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                 "valid Poisson parameter"),
        ]
        answer = f"{loglik}; {score}; lambda_hat={fraction_text(lambda_hat)}"
        problem = (
            f"For Poisson data {data_text(values)}, write the log-likelihood "
            "for lambda, differentiate, and solve for the MLE lambda_hat."
        )
        return problem, steps, answer

    def _generate_uniform_theta(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 20) for _ in range(n)]
        maximum = max(values)
        steps = [
            step("MLE_SETUP", "uniform_zero_theta", "parameter=theta",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("MAX", data_text(values), maximum),
            step("LOG_LIKELIHOOD", "L(theta)=theta^(-n) for theta>=max; 0 otherwise"),
            step("DERIVATIVE", "score=-n/theta has no zero"),
            step("CHECK", "likelihood decreasing in θ", f"θ ≥ {maximum}"),
            step("BOUNDARY_MLE", "smallest allowed theta", maximum),
        ]
        answer = (f"theta_hat = max = {maximum}; "
                  "score equation has no root")
        problem = (
            f"For data {data_text(values)} from Uniform(0,theta), find the "
            "boundary MLE theta_hat and explain why no score root is used."
        )
        return problem, steps, answer

    def _generate_geometric(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 10) for _ in range(n)]
        total = sum(values)
        failures = total - n
        mean = Fraction(total, n)
        p_hat = Fraction(n, total)
        loglik = f"ell(p)={n}*log(p)+{failures}*log(1-p)"
        score = f"score={n}/p-{failures}/(1-p)"
        steps = [
            step("MLE_SETUP", "geometric", "support=1,2,...",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("S", total, n, failures),
            step("D", total, n, fraction_text(mean)),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", "p_hat=1/xbar"),
            step("D", n, total, fraction_text(p_hat)),
            step("CHECK", f"0<{fraction_text(p_hat)}<=1",
                 "valid geometric parameter"),
        ]
        answer = (f"xbar={fraction_text(mean)}; {score}; "
                  f"p_hat={fraction_text(p_hat)}")
        problem = (
            f"For geometric data {data_text(values)} on support 1,2,..., "
            "write the log-likelihood and find the MLE p_hat=1/xbar."
        )
        return problem, steps, answer

    def _generate_binomial_n_known(self):
        observations = random.randint(3, 8)
        trials_each = random.randint(2, 10)
        values = [random.randint(0, trials_each) for _ in range(observations)]
        total_successes = sum(values)
        total_trials = observations * trials_each
        if total_successes in (0, total_trials):
            values[0] = random.randint(1, trials_each - 1)
            total_successes = sum(values)
        failures = total_trials - total_successes
        p_hat = Fraction(total_successes, total_trials)
        loglik = (f"ell(p)={total_successes}*log(p)+"
                  f"{failures}*log(1-p)+C")
        score = f"score={total_successes}/p-{failures}/(1-p)"
        steps = [
            step("MLE_SETUP", "binomial_n_known", f"N={trials_each}",
                 f"data={data_text(values)}"),
            step("COUNT", "observations", observations),
            step("SUM", "total successes", sum_expr(values), total_successes),
            step("M", observations, trials_each, total_trials),
            step("S", total_trials, total_successes, failures),
            step("LOG_LIKELIHOOD", loglik),
            step("DERIVATIVE", score),
            step("SCORE_EQ", f"p_hat={total_successes}/{total_trials}"),
            step("D", total_successes, total_trials, fraction_text(p_hat)),
            step("CHECK", f"0<{fraction_text(p_hat)}<1",
                 "interior binomial parameter"),
        ]
        answer = f"{loglik}; {score}; p_hat={fraction_text(p_hat)}"
        problem = (
            f"For independent Binomial(N={trials_each},p) counts "
            f"{data_text(values)}, with N known, write the log-likelihood "
            "and find the MLE p_hat."
        )
        return problem, steps, answer
