"""Exact bias-variance decomposition and mean-squared-error calculations.

Variants: ``mse_from_parts``, ``mse_scaled_mean``, ``compare_two``,
``optimal_shrinkage``, and ``enumerated_mse``. Scaled-mean cases construct
``Var(xbar)=sigma^2/n`` exactly and use rational shrinkage coefficients;
the enumerated case lists every one of at most 16 ordered samples from
``{1,...,N}``. No rounding is used. Op-codes: ``MSE_DECOMP``, ``MSE_ROW``,
``SAMPLE_ENUM``, ``BIAS``, ``CHECK``, ``SUM``, ``S``, ``D``, ``M``, ``E``,
``A``, and ``Z``.
"""
import itertools
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact


STATISTICS = True

COEFFICIENTS = (
    Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5),
    Fraction(5, 4), Fraction(4, 3), Fraction(3, 2), Fraction(5, 3),
)
LOCATIONS = (
    "north lab", "south lab", "river office", "lake office",
    "maple center", "oak center", "pine archive", "cedar archive",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "risk study", "calibration review", "estimator audit",
    "shrinkage trial", "method comparison", "sampling review",
    "quality study", "forecast audit", "measurement review",
    "variance study", "pilot analysis", "reliability review",
)

QUERIES = {
    "mse_from_parts": (
        "Use MSE = Var + bias² to find the exact mean squared error.",
        "Combine the supplied variance and squared bias.",
        "Report the bias, variance, and MSE of T.",
        "Compute the estimator's exact mean squared error.",
    ),
    "mse_scaled_mean": (
        "Find the bias, variance, and MSE of T.",
        "Apply the bias-variance decomposition to the scaled sample mean.",
        "Compute E[T], bias(T), Var(T), and MSE(T).",
        "Report the exact performance of this shrinkage estimator.",
    ),
    "compare_two": (
        "Choose the estimator with smaller MSE and show the exact comparison.",
        "Compare T1 and T2 by mean squared error.",
        "Which scaled mean has lower MSE?",
        "Compute both MSE values and select the better estimator.",
    ),
    "optimal_shrinkage": (
        "Find c* and the resulting minimum MSE.",
        "Minimize the scaled-mean MSE over c.",
        "Use c* = μ²/(μ² + σ²/n) and evaluate its MSE.",
        "Report the exact optimal shrinkage coefficient and MSE.",
    ),
    "enumerated_mse": (
        "Enumerate the sample maximum and find its bias, variance, and MSE.",
        "Compute E[(T - N)²] exactly from the full sample space.",
        "Evaluate the maximum estimator by both definitions of MSE.",
        "Report bias(T), Var(T), and MSE(T).",
    ),
}


def _site():
    record = f"mse {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _scaled_parts(mu, sigma2, n, coefficient):
    var_mean = Fraction(sigma2, n)
    expectation = coefficient * mu
    bias = expectation - mu
    variance = coefficient ** 2 * var_mean
    mse = variance + bias ** 2
    return {"var_mean": var_mean, "expectation": expectation,
            "bias": bias, "variance": variance, "mse": mse}


def _scaled_steps(label, mu, sigma2, n, coefficient, parts):
    coefficient_text = str(coefficient)
    steps = [
        step("D", sigma2, n, exact(parts["var_mean"])),
        step("M", coefficient_text, mu, exact(parts["expectation"])),
        step("S", exact(parts["expectation"]), mu, exact(parts["bias"])),
        step("BIAS", f"E[{label}] = {exact(parts['expectation'])}",
             f"θ = {mu}", exact(parts["bias"])),
        step("E", coefficient_text, 2, exact(coefficient ** 2)),
        step("M", exact(coefficient ** 2), exact(parts["var_mean"]),
             exact(parts["variance"])),
        step("MSE_DECOMP", f"MSE({label}) = Var({label}) + bias({label})²"),
        step("E", exact(parts["bias"]), 2, exact(parts["bias"] ** 2)),
        step("A", exact(parts["variance"]), exact(parts["bias"] ** 2),
             exact(parts["mse"])),
        step("MSE_ROW", label, f"bias = {exact(parts['bias'])}",
             f"Var = {exact(parts['variance'])}",
             f"MSE = {exact(parts['mse'])}"),
    ]
    return steps


class MSEDecompositionGenerator(ProblemGenerator):
    """Generate exact MSE decompositions and estimator comparisons.

    The module docstring lists variants, op-codes, and the rational / bounded
    enumeration constructions that keep every result exact.
    """

    VARIANTS = tuple(QUERIES)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _result(variant, problem, steps, answer):
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_mse_decomposition_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _from_parts(self):
        bias = random.choice((Fraction(-4), Fraction(-3), Fraction(-2),
                              Fraction(-3, 2), Fraction(-1), Fraction(1, 2),
                              Fraction(1), Fraction(3, 2), Fraction(2),
                              Fraction(3)))
        variance = random.choice((Fraction(1, 4), Fraction(1, 2), Fraction(1),
                                  Fraction(3, 2), Fraction(2), Fraction(5, 2),
                                  Fraction(3), Fraction(4), Fraction(5)))
        squared = bias ** 2
        mse = variance + squared
        steps = [step("MSE_DECOMP", "MSE(T) = Var(T) + bias(T)²"),
                 step("E", exact(bias), 2, exact(squared)),
                 step("A", exact(variance), exact(squared), exact(mse)),
                 step("CHECK", "nonnegative MSE", f"{exact(mse)} ≥ 0")]
        answer = (f"bias = {exact(bias)}; Var = {exact(variance)}; "
                  f"MSE = {exact(mse)}")
        problem = (f"At the {_site()}, an estimator T has bias = "
                   f"{exact(bias)} and Var(T) = {exact(variance)}.\n"
                   f"{random.choice(QUERIES['mse_from_parts'])}")
        return self._result("mse_from_parts", problem, steps, answer)

    @staticmethod
    def _parameters():
        n = random.choice((2, 3, 4, 5, 6, 8, 10))
        mu = random.randint(3, 20)
        variance_mean = random.randint(1, 10)
        sigma2 = n * variance_mean
        return mu, sigma2, n

    def _scaled_mean(self):
        mu, sigma2, n = self._parameters()
        coefficient = random.choice(COEFFICIENTS)
        parts = _scaled_parts(mu, sigma2, n, coefficient)
        steps = _scaled_steps("T", mu, sigma2, n, coefficient, parts)
        steps.append(step("CHECK", "direct MSE",
                          f"{exact(parts['variance'])} + "
                          f"{exact(parts['bias'] ** 2)}",
                          exact(parts["mse"])))
        answer = (f"bias = {exact(parts['bias'])}; "
                  f"Var = {exact(parts['variance'])}; "
                  f"MSE = {exact(parts['mse'])}")
        problem = (f"At the {_site()}, x̄ is the mean of n = {n} observations "
                   f"with μ = {mu} and σ² = {sigma2}. For T = "
                   f"({coefficient})·x̄, evaluate its performance.\n"
                   f"{random.choice(QUERIES['mse_scaled_mean'])}")
        return self._result("mse_scaled_mean", problem, steps, answer)

    def _compare(self):
        mu, sigma2, n = self._parameters()
        while True:
            first, second = random.sample(COEFFICIENTS, 2)
            first_parts = _scaled_parts(mu, sigma2, n, first)
            second_parts = _scaled_parts(mu, sigma2, n, second)
            if first_parts["mse"] != second_parts["mse"]:
                break
        steps = _scaled_steps("T1", mu, sigma2, n, first, first_parts)
        steps.extend(_scaled_steps("T2", mu, sigma2, n, second, second_parts))
        if first_parts["mse"] < second_parts["mse"]:
            winner, low, high = "T1", first_parts["mse"], second_parts["mse"]
        else:
            winner, low, high = "T2", second_parts["mse"], first_parts["mse"]
        steps.append(step("CHECK", "smaller MSE",
                          f"{exact(low)} < {exact(high)}", winner))
        answer = f"{winner}; MSE {exact(low)} < {exact(high)}"
        problem = (f"At the {_site()}, μ = {mu}, σ² = {sigma2}, and n = {n}. "
                   f"Compare T1 = ({first})·x̄ with T2 = ({second})·x̄.\n"
                   f"{random.choice(QUERIES['compare_two'])}")
        return self._result("compare_two", problem, steps, answer)

    def _optimal(self):
        mu, sigma2, n = self._parameters()
        variance_mean = Fraction(sigma2, n)
        mu_squared = Fraction(mu ** 2)
        denominator = mu_squared + variance_mean
        coefficient = mu_squared / denominator
        parts = _scaled_parts(mu, sigma2, n, coefficient)
        steps = [step("D", sigma2, n, exact(variance_mean)),
                 step("E", mu, 2, mu_squared),
                 step("A", mu_squared, exact(variance_mean), exact(denominator)),
                 step("D", mu_squared, exact(denominator), exact(coefficient))]
        steps.extend(_scaled_steps("T(c*)", mu, sigma2, n,
                                   coefficient, parts))
        steps.append(step("CHECK", "minimum-MSE identity",
                          f"μ²·Var(x̄)/(μ² + Var(x̄))",
                          exact(parts["mse"])))
        answer = (f"c* = {exact(coefficient)}; "
                  f"MSE(c*) = {exact(parts['mse'])}")
        problem = (f"At the {_site()}, x̄ has μ = {mu}, σ² = {sigma2}, and "
                   f"n = {n}. For T_c = c·x̄, use the supplied identity "
                   f"c* = μ²/(μ² + σ²/n).\n"
                   f"{random.choice(QUERIES['optimal_shrinkage'])}")
        return self._result("optimal_shrinkage", problem, steps, answer)

    def _enumerated(self):
        endpoint = random.choice((3, 4))
        population = tuple(range(1, endpoint + 1))
        samples = list(itertools.product(population, repeat=2))
        statistics = [Fraction(max(sample)) for sample in samples]
        errors = [value - endpoint for value in statistics]
        squared_errors = [value ** 2 for value in errors]
        expectation = sum(statistics, Fraction(0)) / len(samples)
        bias = expectation - endpoint
        deviations = [(value - expectation) ** 2 for value in statistics]
        variance = sum(deviations, Fraction(0)) / len(samples)
        mse = sum(squared_errors, Fraction(0)) / len(samples)
        steps = []
        for sample, statistic, error, squared in zip(
                samples, statistics, errors, squared_errors):
            steps.append(step("SAMPLE_ENUM",
                              "(" + ", ".join(map(str, sample)) + ")",
                              f"T = {exact(statistic)}",
                              f"T - N = {exact(error)}",
                              f"(T - N)² = {exact(squared)}"))
        statistic_sum = sum(statistics, Fraction(0))
        squared_sum = sum(squared_errors, Fraction(0))
        deviation_sum = sum(deviations, Fraction(0))
        steps.extend([
            step("SUM", " + ".join(exact(value) for value in statistics),
                 exact(statistic_sum)),
            step("D", exact(statistic_sum), len(samples), exact(expectation)),
            step("S", exact(expectation), endpoint, exact(bias)),
            step("BIAS", f"E[T] = {exact(expectation)}", f"N = {endpoint}",
                 exact(bias)),
            step("SUM", " + ".join(exact(value) for value in deviations),
                 exact(deviation_sum)),
            step("D", exact(deviation_sum), len(samples), exact(variance)),
            step("SUM", " + ".join(exact(value) for value in squared_errors),
                 exact(squared_sum)),
            step("D", exact(squared_sum), len(samples), exact(mse)),
            step("MSE_DECOMP", "MSE(T) = Var(T) + bias(T)²"),
            step("E", exact(bias), 2, exact(bias ** 2)),
            step("A", exact(variance), exact(bias ** 2), exact(mse)),
            step("CHECK", "enumeration equals decomposition",
                 exact(mse), exact(variance + bias ** 2)),
        ])
        answer = (f"bias = {exact(bias)}; Var = {exact(variance)}; "
                  f"MSE = {exact(mse)}")
        problem = (f"At the {_site()}, draw an ordered sample of size 2 with "
                   f"replacement from population {{1, ..., N}} with N = "
                   f"{endpoint}. Let T be the sample maximum as an estimator "
                   f"of N.\n{random.choice(QUERIES['enumerated_mse'])}")
        return self._result("enumerated_mse", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "mse_from_parts":
            return self._from_parts()
        if variant == "mse_scaled_mean":
            return self._scaled_mean()
        if variant == "compare_two":
            return self._compare()
        if variant == "optimal_shrinkage":
            return self._optimal()
        return self._enumerated()
