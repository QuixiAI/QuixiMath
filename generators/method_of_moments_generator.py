"""Exact one- and two-parameter method-of-moments estimators.

Variants: ``poisson``, ``exponential``, ``uniform_zero_theta``,
``normal_two_param``, ``gamma_two_param``, and ``uniform_a_b``.  Integer
samples keep every sample moment rational; the two-sided uniform samples use
zero-sum deviation patterns for which ``3(m2-xbar^2)`` is a perfect square.
Op-codes: ``MOM_SETUP``, ``COUNT``, ``SUM``, ``SAMPLE_MOMENT``,
``MOM_EQUATION``, ``REWRITE``, ``E``, ``A``, ``S``, ``M``, ``D``, ``ROOT``,
``CHECK``, and ``Z``.
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


class MethodOfMomentsGenerator(ProblemGenerator):
    """
    Exact first- and second-moment method-of-moments estimators.

    Variants:
    - poisson: E[X]=lambda
    - exponential: E[X]=1/lambda
    - uniform_zero_theta: E[X]=theta/2
    - normal_two_param: match the first two raw moments
    - gamma_two_param: match mean and variance (beta is a rate)
    - uniform_a_b: recover both endpoints from mean and variance

    Op-codes used:
    - MOM_SETUP: model, parameter, and data
    - COUNT / SUM: sample size and total
    - SAMPLE_MOMENT: sample mean
    - MOM_EQUATION: population moment matched to sample moment
    - REWRITE: solved estimating equation
    - E / A / S / D / M / ROOT (established/shared): exact arithmetic
    - CHECK: domain check
    - Z: sample moment and estimator
    """

    VARIANTS = ["poisson", "exponential", "uniform_zero_theta",
                "normal_two_param", "gamma_two_param", "uniform_a_b"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {
            "poisson": self._generate_poisson,
            "exponential": self._generate_exponential,
            "uniform_zero_theta": self._generate_uniform,
            "normal_two_param": self._generate_normal_two_param,
            "gamma_two_param": self._generate_gamma_two_param,
            "uniform_a_b": self._generate_uniform_a_b,
        }
        problem, steps, answer = methods[variant]()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"method_of_moments_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _summary_steps(self, model, parameter, values):
        n = len(values)
        total = sum(values)
        mean = Fraction(total, n)
        steps = [
            step("MOM_SETUP", model, f"parameter={parameter}",
                 f"data={data_text(values)}"),
            step("COUNT", "n", n),
            step("SUM", "sum x_i", sum_expr(values), total),
            step("D", total, n, fraction_text(mean)),
            step("SAMPLE_MOMENT", "xbar", fraction_text(mean)),
        ]
        return n, total, mean, steps

    def _two_moment_steps(self, model, parameter, values):
        n, total, mean, steps = self._summary_steps(model, parameter, values)
        squares = [value * value for value in values]
        square_total = sum(squares)
        second_moment = Fraction(square_total, n)
        steps.extend([
            step("SUM", "sum x_i^2", sum_expr(squares), square_total),
            step("D", square_total, n, fraction_text(second_moment)),
            step("SAMPLE_MOMENT", "m2=(1/n)sum x_i^2",
                 fraction_text(second_moment)),
        ])
        return n, total, mean, second_moment, steps

    def _generate_poisson(self):
        n = random.randint(3, 10)
        values = [random.randint(0, 9) for _ in range(n)]
        if sum(values) == 0:
            values[random.randrange(n)] = random.randint(1, 9)
        _, _, mean, steps = self._summary_steps("poisson", "lambda", values)
        lambda_hat = mean
        steps += [
            step("MOM_EQUATION", "E[X]=lambda", "xbar=lambda"),
            step("REWRITE", f"lambda_hat={fraction_text(lambda_hat)}"),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>=0",
                 "valid Poisson parameter"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from a Poisson(lambda) model, "
            "use the first moment equation to find the method-of-moments "
            "estimator lambda_hat."
        )
        return problem, steps, answer

    def _generate_exponential(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 12) for _ in range(n)]
        _, total, mean, steps = self._summary_steps(
            "exponential", "lambda", values
        )
        lambda_hat = Fraction(n, total)
        steps += [
            step("MOM_EQUATION", "E[X]=1/lambda", "xbar=1/lambda"),
            step("REWRITE", "lambda_hat=1/xbar"),
            step("D", n, total, fraction_text(lambda_hat)),
            step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                 "valid rate parameter"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"lambda_hat={fraction_text(lambda_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from an Exponential(lambda) "
            "model, use E[X]=1/lambda to find the method-of-moments "
            "estimator lambda_hat."
        )
        return problem, steps, answer

    def _generate_uniform(self):
        n = random.randint(3, 10)
        values = [random.randint(1, 20) for _ in range(n)]
        _, _, mean, steps = self._summary_steps(
            "uniform_zero_theta", "theta", values
        )
        theta_hat = 2 * mean
        steps += [
            step("MOM_EQUATION", "E[X]=theta/2", "xbar=theta/2"),
            step("REWRITE", "theta_hat=2*xbar"),
            step("M", 2, fraction_text(mean), fraction_text(theta_hat)),
            step("CHECK", f"theta_hat={fraction_text(theta_hat)}>0",
                 "valid upper endpoint"),
        ]
        answer = (
            f"xbar={fraction_text(mean)}; "
            f"theta_hat={fraction_text(theta_hat)}"
        )
        problem = (
            f"For data {data_text(values)} from a Uniform(0,theta) model, "
            "use E[X]=theta/2 to find the method-of-moments estimator "
            "theta_hat."
        )
        return problem, steps, answer

    def _generate_normal_two_param(self):
        n = random.randint(4, 9)
        values = [random.randint(1, 20) for _ in range(n)]
        while len(set(values)) == 1:
            values = [random.randint(1, 20) for _ in range(n)]
        _, _, mean, second_moment, steps = self._two_moment_steps(
            "normal", "mu,sigma^2", values
        )
        mean_square = mean ** 2
        variance = second_moment - mean_square
        steps.extend([
            step("MOM_EQUATION", "E[X]=mu", "xbar=mu"),
            step("MOM_EQUATION", "E[X^2]=mu^2+sigma^2",
                 "m2=mu^2+sigma^2"),
            step("REWRITE", f"mu_hat={fraction_text(mean)}"),
            step("E", fraction_text(mean), 2, fraction_text(mean_square)),
            step("S", fraction_text(second_moment),
                 fraction_text(mean_square), fraction_text(variance)),
            step("REWRITE", f"sigma2_hat={fraction_text(variance)}"),
            step("CHECK", f"sigma2_hat={fraction_text(variance)}>0",
                 "valid variance parameter"),
        ])
        answer = (f"xbar={fraction_text(mean)}; "
                  f"m2={fraction_text(second_moment)}; "
                  f"mu_hat={fraction_text(mean)}; "
                  f"sigma2_hat={fraction_text(variance)}")
        problem = (
            f"For normal data {data_text(values)} with both mu and sigma^2 "
            "unknown, match the first two raw moments to find the "
            "method-of-moments estimates mu_hat and sigma2_hat."
        )
        return problem, steps, answer

    def _generate_gamma_two_param(self):
        n = random.randint(4, 9)
        values = [random.randint(1, 14) for _ in range(n)]
        while len(set(values)) == 1:
            values = [random.randint(1, 14) for _ in range(n)]
        _, _, mean, second_moment, steps = self._two_moment_steps(
            "gamma_rate", "alpha,beta", values
        )
        mean_square = mean ** 2
        variance = second_moment - mean_square
        alpha_hat = mean_square / variance
        beta_hat = mean / variance
        steps.extend([
            step("MOM_EQUATION", "E[X]=alpha/beta",
                 "xbar=alpha/beta"),
            step("MOM_EQUATION", "Var(X)=alpha/beta^2",
                 "m2-xbar^2=alpha/beta^2"),
            step("E", fraction_text(mean), 2, fraction_text(mean_square)),
            step("S", fraction_text(second_moment),
                 fraction_text(mean_square), fraction_text(variance)),
            step("D", fraction_text(mean_square), fraction_text(variance),
                 fraction_text(alpha_hat)),
            step("D", fraction_text(mean), fraction_text(variance),
                 fraction_text(beta_hat)),
            step("REWRITE", f"alpha_hat={fraction_text(alpha_hat)}",
                 f"beta_hat={fraction_text(beta_hat)}"),
            step("CHECK", f"alpha_hat={fraction_text(alpha_hat)}>0",
                 f"beta_hat={fraction_text(beta_hat)}>0"),
        ])
        answer = (f"xbar={fraction_text(mean)}; "
                  f"m2={fraction_text(second_moment)}; "
                  f"alpha_hat={fraction_text(alpha_hat)}; "
                  f"beta_hat={fraction_text(beta_hat)}")
        problem = (
            f"For Gamma(alpha,beta) data {data_text(values)}, where beta is "
            "the rate parameter, match the sample mean and second raw moment "
            "to find the method-of-moments estimates alpha_hat and beta_hat."
        )
        return problem, steps, answer

    def _generate_uniform_a_b(self):
        deviations = random.choice([
            [-2, -2, -1, 1, 2, 2],
            [-4, -4, -2, 2, 4, 4],
        ])
        center = random.randint(6, 40)
        values = [center + deviation for deviation in deviations]
        random.shuffle(values)
        _, _, mean, second_moment, steps = self._two_moment_steps(
            "uniform_a_b", "a,b", values
        )
        mean_square = mean ** 2
        variance = second_moment - mean_square
        three_variance = 3 * variance
        radius = Fraction(3 if max(deviations) == 2 else 6)
        a_hat = mean - radius
        b_hat = mean + radius
        steps.extend([
            step("MOM_EQUATION", "E[X]=(a+b)/2", "xbar=(a+b)/2"),
            step("MOM_EQUATION", "Var(X)=(b-a)^2/12",
                 "m2-xbar^2=(b-a)^2/12"),
            step("E", fraction_text(mean), 2, fraction_text(mean_square)),
            step("S", fraction_text(second_moment),
                 fraction_text(mean_square), fraction_text(variance)),
            step("M", 3, fraction_text(variance),
                 fraction_text(three_variance)),
            step("ROOT", fraction_text(three_variance),
                 fraction_text(radius)),
            step("REWRITE", "a_hat=xbar-sqrt(3*variance)",
                 "b_hat=xbar+sqrt(3*variance)"),
            step("S", fraction_text(mean), fraction_text(radius),
                 fraction_text(a_hat)),
            step("A", fraction_text(mean), fraction_text(radius),
                 fraction_text(b_hat)),
            step("CHECK", f"a_hat={fraction_text(a_hat)}<"
                 f"b_hat={fraction_text(b_hat)}", "valid endpoints"),
        ])
        answer = (f"xbar={fraction_text(mean)}; "
                  f"m2={fraction_text(second_moment)}; "
                  f"a_hat={fraction_text(a_hat)}; "
                  f"b_hat={fraction_text(b_hat)}")
        problem = (
            f"For data {data_text(values)} from a Uniform(a,b) model, match "
            "the first two raw moments to find the method-of-moments endpoint "
            "estimates a_hat and b_hat."
        )
        return problem, steps, answer
