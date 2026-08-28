"""Convert finite pmfs and cdfs and extract intervals, quantiles, and modes.

Variants: ``pmf_to_cdf``, ``cdf_to_pmf``, ``interval_from_cdf``, ``median``,
``quantile``, and ``mode``. Op-codes: ``DIST_SETUP``, ``WEIGHT``,
``CDF_ROW``, ``TABLE_LOOKUP``, ``QUANTILE``, ``A``, ``S``, ``CMP``,
``CHECK``, and ``Z``. Random supports, dyadic weights, and five phrasings
give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
QUERIES = {
    "pmf_to_cdf": (
        "Build the complete cdf table.",
        "Accumulate the pmf masses in support order and report F(x).",
        "Convert the displayed probability mass function into its cdf.",
        "Find every cumulative probability through the largest support value.",
        "Give the exact cdf rows in ascending x order.",
    ),
    "cdf_to_pmf": (
        "Recover the complete pmf table from the cdf.",
        "Take successive cdf differences to find each point mass.",
        "Convert the displayed cumulative distribution into P(X=x) values.",
        "Find every exact probability mass in ascending support order.",
        "Use F(x) minus the previous cdf value to reconstruct the pmf.",
    ),
    "interval_from_cdf": (
        "Find the probability of the displayed half-open interval.",
        "Subtract the two required cdf values to measure the interval.",
        "Use P(a < X ≤ b) = F(b) − F(a).",
        "What is the exact probability between the stated endpoints?",
        "Look up both cumulative values and compute their difference.",
    ),
    "median": (
        "Find the median, defined as the smallest x with F(x) ≥ 1/2.",
        "Build cumulative probabilities until they first reach one half.",
        "Determine the lower median from the finite distribution.",
        "What is the first support value whose cdf is at least 1/2?",
        "Use the exact cdf to identify the distribution median.",
    ),
    "quantile": (
        "Find the displayed quantile using the first-crossing rule.",
        "Locate the smallest support value whose cdf reaches q.",
        "Use the exact cumulative table to determine the requested quantile.",
        "What is the first x with F(x) at least the stated q?",
        "Accumulate the masses and report the q-quantile.",
    ),
    "mode": (
        "Find the mode and its probability mass.",
        "Identify the largest pmf value, breaking ties by support order.",
        "What support value is most likely, and what is its probability?",
        "Compare all point masses and report the first maximizing value.",
        "Determine the exact mode with the stated first-tie convention.",
    ),
}


def _distribution():
    size = random.randint(3, 6)
    support = tuple(sorted(random.sample(range(-30, 61), size)))
    total = 2 ** random.randint(4, 8)
    while total < size:
        total *= 2
    cuts = sorted(random.sample(range(1, total), size - 1))
    counts = [cuts[0]]
    counts.extend(cuts[i] - cuts[i - 1] for i in range(1, len(cuts)))
    counts.append(total - cuts[-1])
    weights = tuple(Fraction(count, total) for count in counts)
    return support, weights


def _pmf_text(support, weights):
    return "; ".join(f"P(X={x}) = {prob_txt(weight)}"
                     for x, weight in zip(support, weights))


def _cdf_values(weights):
    values = []
    running = Fraction()
    for weight in weights:
        running += weight
        values.append(running)
    return tuple(values)


def _cdf_text(support, values):
    return "; ".join(f"F({x}) = {prob_txt(value)}"
                     for x, value in zip(support, values))


def _cdf_steps(support, weights):
    steps = []
    running = weights[0]
    steps.append(step("CDF_ROW", support[0], prob_txt(running)))
    for x, weight in zip(support[1:], weights[1:]):
        steps.append(step("A", prob_txt(running), prob_txt(weight),
                          prob_txt(running + weight)))
        running += weight
        steps.append(step("CDF_ROW", x, prob_txt(running)))
    return steps


class PmfCdfQuantileGenerator(ProblemGenerator):
    """Generate exact finite-distribution conversion and lookup exercises."""

    VARIANTS = ("pmf_to_cdf", "cdf_to_pmf", "interval_from_cdf", "median",
                "quantile", "mode")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _build(variant):
        support, weights = _distribution()
        cdf = _cdf_values(weights)
        if variant in ("cdf_to_pmf", "interval_from_cdf"):
            steps = [step("DIST_SETUP", "finite cdf", _cdf_text(support, cdf))]
        else:
            steps = [step("DIST_SETUP", "finite pmf", _pmf_text(support, weights))]
        if variant == "cdf_to_pmf":
            prefix = f"X has cdf rows: {_cdf_text(support, cdf)}."
            previous = Fraction()
            for x, cumulative in zip(support, cdf):
                weight = cumulative - previous
                steps.extend([step("S", prob_txt(cumulative), prob_txt(previous),
                                   prob_txt(weight)),
                              step("WEIGHT", x, prob_txt(weight))])
                previous = cumulative
            answer = _pmf_text(support, weights)
        elif variant == "interval_from_cdf":
            left_index = random.randint(0, len(support) - 2)
            right_index = random.randint(left_index + 1, len(support) - 1)
            left, right = support[left_index], support[right_index]
            value = cdf[right_index] - cdf[left_index]
            prefix = (f"X has cdf rows: {_cdf_text(support, cdf)}. Target: "
                      f"P({left} < X ≤ {right}).")
            steps.extend([step("TABLE_LOOKUP", f"F({right})", prob_txt(cdf[right_index])),
                          step("TABLE_LOOKUP", f"F({left})", prob_txt(cdf[left_index])),
                          step("S", prob_txt(cdf[right_index]),
                               prob_txt(cdf[left_index]), prob_txt(value))])
            answer = prob_txt(value)
        elif variant in ("median", "quantile"):
            q = Fraction(1, 2) if variant == "median" else random.choice(
                (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)))
            index = next(i for i, value in enumerate(cdf) if value >= q)
            prefix = f"X has pmf: {_pmf_text(support, weights)}."
            if variant == "quantile":
                prefix += f" Quantile level q = {prob_txt(q)}."
            steps.extend(_cdf_steps(support, weights))
            steps.append(step("QUANTILE", prob_txt(q),
                              "first x with F(x) ≥ q", support[index]))
            answer = (f"median {support[index]}" if variant == "median"
                      else f"q={prob_txt(q)} quantile {support[index]}")
        elif variant == "mode":
            maximum = max(weights)
            index = weights.index(maximum)
            tied = weights.count(maximum) > 1
            prefix = (f"X has pmf: {_pmf_text(support, weights)}. If several "
                      "values tie, choose the first in support order.")
            steps.extend(step("WEIGHT", x, prob_txt(weight))
                         for x, weight in zip(support, weights))
            for x, weight in zip(support, weights):
                steps.append(step("CMP", prob_txt(weight), prob_txt(maximum),
                                  "=" if weight == maximum else "<"))
            steps.append(step("CHECK", "first maximum", support[index],
                              prob_txt(maximum)))
            tie_text = " (first among ties)" if tied else ""
            answer = (f"mode {support[index]}{tie_text}; "
                      f"P(X={support[index]}) = {prob_txt(maximum)}")
        else:
            prefix = f"X has pmf: {_pmf_text(support, weights)}."
            steps.extend(_cdf_steps(support, weights))
            answer = _cdf_text(support, cdf)
        steps.append(step("CHECK", "total probability", prob_txt(cdf[-1])))
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        prefix, steps, answer = self._build(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_pmf_cdf_quantile_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
