"""Enumerate exact finite sampling distributions of x̄ and p̂.

Variants: ``list_means``, ``distribution_table``, ``mean_of_xbar``,
``variance_of_xbar``, ``prob_event``, and ``proportion_phat``. Without-
replacement prompts enumerate unordered simple random samples; replacement
prompts enumerate ordered draw sequences, so every displayed row is equally
likely. Construction caps enumeration at 20 rows. Random populations,
methods, targets, sites, scenario codes, and four phrasings give unbounded
capacity.
"""
import itertools
import random
from collections import Counter
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt
from stats_common import num_txt, running_sum_steps, text_list


STATISTICS = True
SETTINGS = (
    "amber study", "birch survey", "cedar trial", "delta project",
    "ember lab", "forest audit", "granite program", "harbor test",
    "indigo review", "jade pilot", "kestrel study", "lunar trial",
)
LOCATIONS = (
    "north campus", "south campus", "east annex", "west annex",
    "river center", "lake center", "hill school", "valley school",
    "maple office", "oak office", "pine clinic", "cedar clinic",
)
QUERIES = {
    "list_means": (
        "List every sample and its exact sample mean.",
        "Enumerate the equally likely samples with their x̄ values.",
        "Report the complete sample-to-mean text list.",
        "Find each possible sample mean without aggregating duplicates.",
    ),
    "distribution_table": (
        "Give the exact sampling distribution of x̄.",
        "Aggregate equal sample means into a probability table.",
        "Report every x̄ value with its reduced probability.",
        "Turn the sample enumeration into the distribution of the mean.",
    ),
    "mean_of_xbar": (
        "Find E[x̄] and compare it with the population mean μ.",
        "Compute the mean of the sampling distribution and verify unbiasedness.",
        "What is the expected sample mean, and does it equal μ?",
        "Weight all x̄ values by their probabilities and check the center.",
    ),
    "variance_of_xbar": (
        "Find Var(x̄) and verify the stated finite-population identity.",
        "Compute the sampling variance and compare it with the formula.",
        "What is the exact variance of the sample mean distribution?",
        "Use enumeration and the supplied sampling-variance identity.",
    ),
    "prob_event": (
        "Find the exact probability of the stated x̄ event.",
        "Count qualifying sample means and divide by all samples.",
        "What fraction of the sampling distribution meets the threshold?",
        "Use complete enumeration to evaluate the sample-mean event.",
    ),
    "proportion_phat": (
        "Give the exact sampling distribution of p̂.",
        "Enumerate samples from the binary population and aggregate p̂.",
        "Report every sample-proportion value with its probability.",
        "Build the distribution of the fraction of sampled successes.",
    ),
}


def _site():
    code = f"cohort {random.choice('ABCDEFGH')}{random.randint(10, 99)}"
    return (f"{random.choice(LOCATIONS)} during the "
            f"{random.choice(SETTINGS)} ({code})")


def _sampling_plan(binary=False):
    if random.choice((True, False)):
        size = random.choice((4, 5, 6))
        sample_size = random.choice([n for n in (2, 3)
                                     if 1 <= n < size and
                                     _comb(size, n) <= 20])
        replacement = False
    else:
        size = random.choice((3, 4))
        sample_size = 2
        replacement = True
    if binary and not replacement:
        size = random.choice((4, 5, 6))
        sample_size = random.choice([n for n in (2, 3)
                                     if _comb(size, n) <= 20])
    return size, sample_size, replacement


def _comb(n, k):
    numerator = 1
    denominator = 1
    for value in range(1, k + 1):
        numerator *= n - value + 1
        denominator *= value
    return numerator // denominator


def _samples(population, sample_size, replacement, binary=False):
    if replacement:
        return list(itertools.product(population, repeat=sample_size))
    if binary:
        return [tuple(population[index] for index in indexes)
                for indexes in itertools.combinations(
                    range(len(population)), sample_size)]
    return list(itertools.combinations(population, sample_size))


def _sample_stat(sample):
    return Fraction(sum(sample), len(sample))


def _sample_label(sample):
    return "{" + ", ".join(map(str, sample)) + "}"


def _distribution(samples):
    stats = [_sample_stat(sample) for sample in samples]
    return stats, Counter(stats)


def _enumeration_steps(population, sample_size, replacement, samples, stats,
                       statistic="x̄"):
    method = ("ordered draws, with replacement" if replacement else
              "unordered samples, without replacement")
    steps = [step("STAT_SETUP",
                  "population " + ",".join(map(str, population)),
                  f"n={sample_size}, {method}")]
    for sample, value in zip(samples, stats):
        steps.append(step("SAMPLE_ENUM", _sample_label(sample),
                          f"{statistic}={num_txt(value)}"))
    return steps


def _distribution_steps(counts, total):
    steps = []
    for value in sorted(counts):
        probability = Fraction(counts[value], total)
        steps.append(step("DIST_ROW", num_txt(value),
                          f"{counts[value]}/{total}", prob_txt(probability)))
    return steps


def _distribution_answer(counts, total):
    return text_list((num_txt(value), prob_txt(Fraction(count, total)))
                     for value, count in sorted(counts.items()))


def _ordinary_case():
    size, sample_size, replacement = _sampling_plan()
    population = sorted(random.sample(range(1, 21), size))
    samples = _samples(population, sample_size, replacement)
    stats, counts = _distribution(samples)
    return population, sample_size, replacement, samples, stats, counts


class SamplingDistributionEnumGenerator(ProblemGenerator):
    """Generate exact sampling distributions by complete enumeration."""

    VARIANTS = ("list_means", "distribution_table", "mean_of_xbar",
                "variance_of_xbar", "prob_event", "proportion_phat")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _ordinary(variant):
        (population, sample_size, replacement, samples, stats,
         counts) = _ordinary_case()
        total = len(samples)
        method = ("make ordered draws with replacement; ordered sequences "
                  "are equally likely" if replacement else
                  "choose without replacement; unordered simple random "
                  "samples are equally likely")
        prefix = (f"At the {_site()}, population values are: "
                  f"{', '.join(map(str, population))}. Sampling plan: "
                  f"n = {sample_size}; {method}. There are {total} equally "
                  f"likely samples.")
        if variant == "variance_of_xbar":
            identity_text = ("Var(x̄) = σ²/n" if replacement else
                             "Var(x̄) = (σ²/n) · (N-n)/(N-1)")
            prefix += (" Here σ² is the population variance (divide by N). "
                       f"Use the identity {identity_text}.")
        steps = _enumeration_steps(population, sample_size, replacement,
                                   samples, stats)
        if variant == "list_means":
            answer = text_list((_sample_label(sample), num_txt(value))
                               for sample, value in zip(samples, stats))
            steps.append(step("CHECK", "all samples listed", total,
                              len(samples)))
        else:
            steps.extend(_distribution_steps(counts, total))
            probability_sum = sum(Fraction(count, total)
                                  for count in counts.values())
            steps.append(step("CHECK", "distribution probability sum",
                              " + ".join(prob_txt(Fraction(count, total))
                                         for _, count in sorted(counts.items())),
                              prob_txt(probability_sum)))
            if variant == "distribution_table":
                answer = _distribution_answer(counts, total)
            elif variant == "mean_of_xbar":
                terms = [value * Fraction(count, total)
                         for value, count in sorted(counts.items())]
                for (value, count), term in zip(sorted(counts.items()), terms):
                    steps.append(step("M", num_txt(value),
                                      prob_txt(Fraction(count, total)),
                                      num_txt(term)))
                additions, expected = running_sum_steps(terms)
                steps.extend(additions)
                population_mean = Fraction(sum(population), len(population))
                assert expected == population_mean
                answer = (f"{num_txt(expected)}; equals μ = "
                          f"{num_txt(population_mean)}")
                steps.append(step("CHECK", "E[x̄] = μ", num_txt(expected),
                                  num_txt(population_mean)))
            elif variant == "variance_of_xbar":
                expected = sum(value * Fraction(count, total)
                               for value, count in counts.items())
                terms = []
                for value, count in sorted(counts.items()):
                    deviation = value - expected
                    square = deviation * deviation
                    probability = Fraction(count, total)
                    term = square * probability
                    terms.append(term)
                    steps.extend([step("S", num_txt(value), num_txt(expected),
                                       num_txt(deviation)),
                                  step("E", num_txt(deviation), 2,
                                       num_txt(square)),
                                  step("M", num_txt(square),
                                       prob_txt(probability), num_txt(term)),
                                  step("VAR_ROW",
                                       f"{num_txt(value)} - {num_txt(expected)} = "
                                       f"{num_txt(deviation)}",
                                       f"({num_txt(deviation)})^2 = "
                                       f"{num_txt(square)}",
                                       f"{prob_txt(probability)}·"
                                       f"{num_txt(square)} = {num_txt(term)}")])
                additions, variance = running_sum_steps(terms)
                steps.extend(additions)
                population_mean = Fraction(sum(population), len(population))
                population_variance = sum(
                    (Fraction(value) - population_mean) ** 2
                    for value in population) / len(population)
                base = population_variance / sample_size
                steps.append(step("D", num_txt(population_variance),
                                  sample_size, num_txt(base)))
                if replacement:
                    formula = f"σ²/n = {num_txt(base)}"
                    identity = base
                else:
                    correction = Fraction(len(population) - sample_size,
                                          len(population) - 1)
                    steps.extend([step("D", len(population) - sample_size,
                                       len(population) - 1,
                                       num_txt(correction)),
                                  step("M", num_txt(base),
                                       num_txt(correction),
                                       num_txt(base * correction))])
                    identity = base * correction
                    formula = (f"σ²/n · (N-n)/(N-1) = {num_txt(base)} · "
                               f"{num_txt(correction)} = {num_txt(identity)}")
                assert variance == identity
                answer = f"{num_txt(variance)}; {formula}"
                steps.append(step("CHECK", "enumeration = variance identity",
                                  num_txt(variance), num_txt(identity)))
            else:
                threshold = random.choice(sorted(counts))
                qualifying = sum(count for value, count in counts.items()
                                 if value >= threshold)
                probability = Fraction(qualifying, total)
                prefix += (f" Event: x̄ ≥ {num_txt(threshold)}.")
                steps.extend([step("COUNT", f"x̄ ≥ {num_txt(threshold)}",
                                   f"{qualifying}/{total}"),
                              step("F", f"{qualifying}/{total}",
                                   prob_txt(probability))])
                answer = prob_txt(probability)
        return prefix, steps, answer

    @staticmethod
    def _phat():
        size, sample_size, replacement = _sampling_plan(binary=True)
        successes = random.randint(1, size - 1)
        population = [0] * (size - successes) + [1] * successes
        random.shuffle(population)
        samples = _samples(population, sample_size, replacement, binary=True)
        stats, counts = _distribution(samples)
        total = len(samples)
        method = ("make ordered draws with replacement; ordered sequences "
                  "are equally likely" if replacement else
                  "choose positions without replacement; unordered index "
                  "samples are equally likely")
        prefix = (f"At the {_site()}, binary population values are: "
                  f"{', '.join(map(str, population))}. Sampling plan: n = "
                  f"{sample_size}; {method}. A 1 is a success. There are "
                  f"{total} equally likely samples.")
        steps = _enumeration_steps(population, sample_size, replacement,
                                   samples, stats, statistic="p̂")
        steps.extend(_distribution_steps(counts, total))
        answer = _distribution_answer(counts, total)
        steps.append(step("CHECK", "p̂ distribution probability sum",
                          " + ".join(prob_txt(Fraction(count, total))
                                     for _, count in sorted(counts.items())),
                          1))
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "proportion_phat":
            prefix, steps, answer = self._phat()
        else:
            prefix, steps, answer = self._ordinary(variant)
        problem = f"{prefix}\n{random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"statistics_sampling_distribution_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
