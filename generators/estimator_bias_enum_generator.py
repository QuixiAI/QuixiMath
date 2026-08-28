"""Exact finite-population enumeration of estimator bias and variance.

Variants: ``variance_n_bias``, ``variance_n_minus_1_unbiased``,
``mean_unbiased``, ``max_estimator_bias``, ``range_estimator``, and
``without_replacement``. Replacement variants enumerate at most 16 ordered
samples; without-replacement variants enumerate at most 10 combinations.
Population moments, every sample statistic, expectations, biases, and the
finite-population correction are exact ``Fraction`` arithmetic. Range cases
use four-point populations whose population variance is a rational square.
Op-codes: ``SUM``, ``MEAN_DIV``, ``DEV_ROW``, ``SAMPLE_ENUM``, ``BIAS``,
``FPC``, ``CHECK``, ``S``, ``D``, ``M``, ``ROOT``, and ``Z``.
"""
import itertools
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import exact


STATISTICS = True

LOCATIONS = (
    "north archive", "south archive", "river lab", "lake lab",
    "maple office", "oak office", "pine center", "cedar center",
    "amber campus", "birch campus", "granite clinic", "harbor clinic",
)
STUDIES = (
    "calibration study", "quality review", "sampling audit",
    "measurement study", "estimator trial", "variance review",
    "field survey", "process audit", "reliability study",
    "design review", "method comparison", "pilot analysis",
)

RANGE_POPULATIONS = (
    (1, 2, 5, 10), (1, 4, 5, 8), (1, 6, 9, 10),
    (2, 3, 6, 11), (2, 5, 6, 9), (2, 7, 10, 11),
    (3, 4, 7, 12), (3, 6, 7, 10), (3, 8, 11, 12),
    (4, 7, 8, 11), (5, 8, 9, 12),
)

QUERIES = {
    "variance_n_bias": (
        "Find E[σ̂²], compare it with σ², and state the bias.",
        "Enumerate the denominator-n variance estimator and measure its bias.",
        "Does σ̂² target the population variance without bias? Show the exact values.",
        "Compute the expectation, target, and bias of σ̂².",
    ),
    "variance_n_minus_1_unbiased": (
        "Find E[s²], compare it with σ², and state the bias.",
        "Enumerate the denominator-(n - 1) sample variance.",
        "Verify exactly whether s² is unbiased for the population variance.",
        "Compute the expectation, target, and bias of s².",
    ),
    "mean_unbiased": (
        "Find E[x̄], compare it with μ, and state the bias.",
        "Enumerate the sample mean and check its expected value.",
        "Verify exactly whether x̄ is unbiased for the population mean.",
        "Compute the expectation, target, and bias of x̄.",
    ),
    "max_estimator_bias": (
        "Find E[max], compare it with endpoint N, and state the bias.",
        "Enumerate the sample maximum as an estimator of N.",
        "Compute the exact bias of the maximum-based endpoint estimator.",
        "Report E[max], its target, and its bias.",
    ),
    "range_estimator": (
        "Find E[range], compare it with σ, and state the bias.",
        "Enumerate max - min as an estimator of the population standard deviation.",
        "Compute the range estimator's exact expectation and bias.",
        "Report E[range], σ, and their difference.",
    ),
    "without_replacement": (
        "Find E[x̄], its bias, and Var(x̄), then verify the finite-population correction.",
        "Enumerate the without-replacement sample mean and check its variance formula.",
        "Use all simple random samples to verify unbiasedness and the FPC.",
        "Compute the sample mean's expectation, bias, and exact variance.",
    ),
}


def _site():
    record = f"enum {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(STUDIES)} ({record})")


def _population(size=None):
    size = size or random.choice((3, 4))
    return tuple(sorted(random.sample(range(1, 13), size)))


def _mean(values):
    return sum((Fraction(value) for value in values), Fraction(0)) / len(values)


def _variance(values, denominator=None):
    center = _mean(values)
    denominator = len(values) if denominator is None else denominator
    return sum((Fraction(value) - center) ** 2 for value in values) / denominator


def _sample_label(sample):
    return "(" + ", ".join(map(str, sample)) + ")"


def _population_steps(population, include_root=False):
    total = sum(population)
    mean = _mean(population)
    squares = [(Fraction(value) - mean) ** 2 for value in population]
    ss = sum(squares, Fraction(0))
    variance = ss / len(population)
    steps = [step("SUM", " + ".join(map(str, population)), total),
             step("MEAN_DIV", total, len(population), exact(mean))]
    for value, square in zip(population, squares):
        steps.append(step("DEV_ROW", value,
                          f"{value} - {exact(mean)}", exact(square)))
    steps.extend([step("SUM", " + ".join(exact(value) for value in squares),
                       exact(ss)),
                  step("D", exact(ss), len(population), exact(variance))])
    if include_root:
        # RANGE_POPULATIONS guarantee numerator and denominator are squares.
        sigma = Fraction(math.isqrt(variance.numerator),
                         math.isqrt(variance.denominator))
        if sigma * sigma != variance:
            raise ValueError(f"range population variance {variance} is not square")
        steps.append(step("ROOT", exact(variance), exact(sigma)))
    return steps, mean, variance


class EstimatorBiasEnumGenerator(ProblemGenerator):
    """Generate exact estimator-bias enumerations with bounded row counts.

    The module docstring lists all variants, op-codes, and exactness / capacity
    constructions. Samples shown in ``SAMPLE_ENUM`` are the complete sample
    space under the procedure stated in the problem.
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
                "operation": f"statistics_estimator_bias_enum_{variant}",
                "problem": problem, "steps": steps,
                "final_answer": answer}

    def _replacement(self, variant):
        if variant == "max_estimator_bias":
            endpoint = random.choice((3, 4))
            population = tuple(range(1, endpoint + 1))
        elif variant == "range_estimator":
            population = random.choice(RANGE_POPULATIONS)
        else:
            population = _population()
        sample_size = 2
        include_root = variant == "range_estimator"
        steps, population_mean, population_variance = _population_steps(
            population, include_root=include_root)
        samples = list(itertools.product(population, repeat=sample_size))

        if variant == "variance_n_bias":
            symbol = "σ̂²"
            statistics = [_variance(sample) for sample in samples]
            target = population_variance
            problem_detail = "σ̂² = Σ(x - x̄)²/n"
            target_name = "σ²"
        elif variant == "variance_n_minus_1_unbiased":
            symbol = "s²"
            statistics = [_variance(sample, sample_size - 1)
                          for sample in samples]
            target = population_variance
            problem_detail = "s² = Σ(x - x̄)²/(n - 1)"
            target_name = "σ²"
        elif variant == "mean_unbiased":
            symbol = "x̄"
            statistics = [_mean(sample) for sample in samples]
            target = population_mean
            problem_detail = "use x̄ to estimate μ"
            target_name = "μ"
        elif variant == "max_estimator_bias":
            symbol = "max"
            statistics = [Fraction(max(sample)) for sample in samples]
            target = Fraction(max(population))
            problem_detail = "use the sample maximum to estimate endpoint N"
            target_name = "N"
        else:
            symbol = "range"
            statistics = [Fraction(max(sample) - min(sample))
                          for sample in samples]
            sigma = Fraction(math.isqrt(population_variance.numerator),
                             math.isqrt(population_variance.denominator))
            target = sigma
            problem_detail = "use max - min to estimate population σ"
            target_name = "σ"

        for sample, statistic in zip(samples, statistics):
            if symbol in ("σ̂²", "s²"):
                detail = (f"x̄ = {exact(_mean(sample))}, "
                          f"{symbol} = {exact(statistic)}")
            else:
                detail = f"{symbol} = {exact(statistic)}"
            steps.append(step("SAMPLE_ENUM", _sample_label(sample), detail))
        statistic_sum = sum(statistics, Fraction(0))
        expectation = statistic_sum / len(samples)
        bias = expectation - target
        steps.extend([
            step("SUM", " + ".join(exact(value) for value in statistics),
                 exact(statistic_sum)),
            step("D", exact(statistic_sum), len(samples), exact(expectation)),
            step("BIAS", f"E[{symbol}] = {exact(expectation)}",
                 f"{target_name} = {exact(target)}", exact(bias)),
        ])
        if variant == "variance_n_bias":
            factor_num = sample_size - 1
            factor = Fraction(factor_num, sample_size)
            steps.extend([
                step("S", sample_size, 1, sample_size - 1),
                step("D", factor_num, sample_size, exact(factor)),
                step("M", exact(population_variance), exact(factor),
                     exact(population_variance * factor)),
                step("CHECK", "variance identity",
                     f"{exact(population_variance)} × {exact(factor)}",
                     exact(expectation)),
            ])
        elif variant == "variance_n_minus_1_unbiased":
            steps.append(step("CHECK", "unbiased sample-variance identity",
                              f"E[s²] = σ² = {exact(population_variance)}",
                              exact(expectation)))
        else:
            steps.append(step("CHECK", "complete equally likely sample space",
                              len(samples), f"E[{symbol}] = {exact(expectation)}"))

        bias_text = ("0 (unbiased)" if bias == 0 else exact(bias))
        answer = (f"E[{symbol}] = {exact(expectation)}; "
                  f"{target_name} = {exact(target)}; bias = {bias_text}")
        roster = ", ".join(map(str, population))
        problem = (f"At the {_site()}, population = {{{roster}}}; treat its "
                   f"members as equally likely. For ordered samples of size "
                   f"n = {sample_size} with replacement, {problem_detail}.\n"
                   f"{random.choice(QUERIES[variant])}")
        return self._result(variant, problem, steps, answer)

    def _without_replacement(self):
        size, sample_size = random.choice(((3, 2), (3, 3), (4, 2), (5, 2)))
        population = _population(size)
        steps, population_mean, population_variance = _population_steps(population)
        samples = list(itertools.combinations(population, sample_size))
        means = [_mean(sample) for sample in samples]
        for sample, mean in zip(samples, means):
            steps.append(step("SAMPLE_ENUM", _sample_label(sample),
                              f"x̄ = {exact(mean)}"))
        mean_sum = sum(means, Fraction(0))
        expectation = mean_sum / len(samples)
        deviations = [(mean - expectation) ** 2 for mean in means]
        variance = sum(deviations, Fraction(0)) / len(samples)
        bias = expectation - population_mean
        base = population_variance / sample_size
        factor_num = len(population) - sample_size
        factor_den = len(population) - 1
        factor = Fraction(factor_num, factor_den)
        steps.extend([
            step("SUM", " + ".join(exact(value) for value in means),
                 exact(mean_sum)),
            step("D", exact(mean_sum), len(samples), exact(expectation)),
            step("BIAS", f"E[x̄] = {exact(expectation)}",
                 f"μ = {exact(population_mean)}", exact(bias)),
            step("SUM", " + ".join(exact(value) for value in deviations),
                 exact(sum(deviations, Fraction(0)))),
            step("D", exact(sum(deviations, Fraction(0))), len(samples),
                 exact(variance)),
            step("FPC", "Var(x̄) = σ²/n × (N-n)/(N-1)"),
            step("D", exact(population_variance), sample_size, exact(base)),
            step("S", len(population), sample_size, factor_num),
            step("S", len(population), 1, factor_den),
            step("D", factor_num, factor_den, exact(factor)),
            step("M", exact(base), exact(factor), exact(base * factor)),
            step("CHECK", "finite-population correction",
                 f"{exact(base)} × {exact(factor)}", exact(variance)),
        ])
        answer = (f"E[x̄] = {exact(expectation)}; bias = {exact(bias)}; "
                  f"Var(x̄) = {exact(variance)}")
        roster = ", ".join(map(str, population))
        problem = (f"At the {_site()}, population = {{{roster}}}. Enumerate "
                   f"all unordered simple random samples of size n = "
                   f"{sample_size} without replacement. Use x̄ to estimate μ "
                   f"and verify Var(x̄) = σ²/n × (N-n)/(N-1).\n"
                   f"{random.choice(QUERIES['without_replacement'])}")
        return self._result("without_replacement", problem, steps, answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "without_replacement":
            return self._without_replacement()
        return self._replacement(variant)
