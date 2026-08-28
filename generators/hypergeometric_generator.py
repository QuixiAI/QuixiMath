"""Compute exact without-replacement probabilities and moments.

Variants: ``exact_k``, ``at_least_one``, ``at_most``, ``mean``,
``variance``, and ``three_types``. Op-codes: ``HYPERGEO_SETUP``,
``HYPERGEO_FORMULA``, ``HYPERGEO_TERM``, ``NCR``, ``FRAC_BUILD``,
``COMPLEMENT``, ``M``, ``A``, ``S``, ``D``, ``CHECK``, and ``Z``.
Populations have at most 12 labelled items, so every test oracle can enumerate
the sample subsets exactly; context, batch, parameter, target, and five
phrasing choices provide a large problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
CONTEXTS = (
    ("box", "good bulbs", "defective bulbs"),
    ("crate", "ripe peaches", "unripe peaches"),
    ("batch", "working sensors", "faulty sensors"),
    ("shelf", "new books", "used books"),
    ("case", "charged batteries", "empty batteries"),
    ("tray", "plain tiles", "patterned tiles"),
    ("basket", "red apples", "green apples"),
    ("packet", "signed cards", "unsigned cards"),
    ("rack", "local jerseys", "visitor jerseys"),
    ("drawer", "metal tokens", "wooden tokens"),
)
BATCHES = ("amber", "birch", "cedar", "delta", "ember", "forest",
           "granite", "harbor", "indigo", "jade", "kestrel", "lunar",
           "maple", "nova", "onyx", "pearl", "quartz", "river", "solar",
           "topaz", "umber", "violet", "willow", "zephyr")
COLOR_SETS = (("red", "blue", "green"), ("amber", "teal", "white"),
              ("orange", "purple", "yellow"), ("black", "silver", "gold"),
              ("coral", "navy", "lime"), ("rose", "cyan", "gray"))
QUERIES = {
    "exact_k": (
        "Find the exact probability of the displayed count.",
        "Use the hypergeometric formula for exactly the target number.",
        "Count favorable samples and divide by all samples.",
        "What is the exact without-replacement probability?",
        "Evaluate the requested point probability for X.",
    ),
    "at_least_one": (
        "Find the probability of at least one target item.",
        "Use the complement of drawing no target items.",
        "Compute one minus the all-nontarget sample probability.",
        "What is the exact chance that the sample contains a target?",
        "Apply the hypergeometric complement shortcut.",
    ),
    "at_most": (
        "Find the probability of at most the displayed number of target items.",
        "Add every feasible hypergeometric term through the target count.",
        "Compute the requested cumulative probability exactly.",
        "What is the exact value of the lower-tail probability?",
        "Sum the without-replacement point probabilities up to the cutoff.",
    ),
    "mean": (
        "Find the exact expected value of X.",
        "Use the hypergeometric mean formula.",
        "How many target items are expected in the sample?",
        "Compute E[X] for this without-replacement count.",
        "Determine the mean number of target items drawn.",
    ),
    "variance": (
        "Find the exact variance of X.",
        "Use the hypergeometric variance with its finite-population correction.",
        "Compute Var(X) for this without-replacement count.",
        "What is the exact spread of the target-item count?",
        "Apply np(1 − p)(N − n)/(N − 1).",
    ),
    "three_types": (
        "Find the exact probability of the displayed three-color counts.",
        "Use the multivariate hypergeometric counting ratio.",
        "Count samples with all three requested color totals.",
        "What is the exact probability of this color composition?",
        "Multiply the three favorable combination counts and divide by all samples.",
    ),
}


def _two_type_parameters(variant):
    while True:
        total = random.randint(6, 12)
        target_total = random.randint(2, total - 2)
        other_total = total - target_total
        if variant == "at_least_one":
            sample = random.randint(2, other_total)
        else:
            sample = random.randint(2, total - 2)
        lower = max(0, sample - other_total)
        upper = min(target_total, sample)
        if variant == "at_most" and lower < upper:
            cutoff = random.randint(lower, upper - 1)
            return total, target_total, sample, cutoff
        if variant == "exact_k":
            return total, target_total, sample, random.randint(lower, upper)
        if variant not in ("exact_k", "at_most"):
            return total, target_total, sample, None


def _pmf_value(total, target_total, sample, count):
    other_total = total - target_total
    if not (0 <= count <= target_total and 0 <= sample - count <= other_total):
        return Fraction()
    return Fraction(math.comb(target_total, count)
                    * math.comb(other_total, sample - count),
                    math.comb(total, sample))


def _pmf_steps(total, target_total, sample, count):
    other_total = total - target_total
    first = math.comb(target_total, count)
    second = math.comb(other_total, sample - count)
    favorable = first * second
    all_samples = math.comb(total, sample)
    value = Fraction(favorable, all_samples)
    return [
        step("NCR", f"C({target_total}, {count})", first),
        step("NCR", f"C({other_total}, {sample - count})", second),
        step("M", first, second, favorable),
        step("NCR", f"C({total}, {sample})", all_samples),
        step("FRAC_BUILD", f"{favorable}/{all_samples}", prob_txt(value)),
        step("HYPERGEO_TERM", f"X = {count}", prob_txt(value)),
    ], value


def _two_type_prefix(total, target_total, sample, context, batch, target):
    container, target_plural, other_plural = context
    return (f"In the {batch} lot, a {container} has {target_total} "
            f"{target_plural} and {total - target_total} {other_plural}. "
            f"A sample of {sample} items is drawn uniformly without replacement. "
            f"Let X be the number of {target_plural} drawn. Target: {target}.")


class HypergeometricGenerator(ProblemGenerator):
    """Generate exact hypergeometric probabilities and moments."""

    VARIANTS = ("exact_k", "at_least_one", "at_most", "mean", "variance",
                "three_types")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _two_type(variant):
        total, target_total, sample, cutoff = _two_type_parameters(variant)
        context = random.choice(CONTEXTS)
        batch = random.choice(BATCHES)
        setup_goal = {
            "exact_k": f"P(X = {cutoff})",
            "at_least_one": "P(X ≥ 1)",
            "at_most": f"P(X ≤ {cutoff})",
            "mean": "E[X]",
            "variance": "Var(X)",
        }[variant]
        prefix = _two_type_prefix(total, target_total, sample, context, batch,
                                  setup_goal)
        steps = [step("HYPERGEO_SETUP",
                      f"N = {total}, K = {target_total}, n = {sample}",
                      setup_goal)]
        if variant == "exact_k":
            steps.append(step("HYPERGEO_FORMULA",
                              "P(X = k) = C(K,k)·C(N − K,n − k)/C(N,n)"))
            extra, value = _pmf_steps(total, target_total, sample, cutoff)
            steps.extend(extra)
            answer = prob_txt(value)
        elif variant == "at_least_one":
            other_total = total - target_total
            no_target = math.comb(other_total, sample)
            all_samples = math.comb(total, sample)
            p_none = Fraction(no_target, all_samples)
            value = 1 - p_none
            steps.extend([
                step("COMPLEMENT", "P(X ≥ 1) = 1 − P(X = 0)"),
                step("NCR", f"C({other_total}, {sample})", no_target),
                step("NCR", f"C({total}, {sample})", all_samples),
                step("FRAC_BUILD", f"{no_target}/{all_samples}",
                     prob_txt(p_none)),
                step("S", 1, prob_txt(p_none), prob_txt(value)),
            ])
            answer = prob_txt(value)
        elif variant == "at_most":
            lower = max(0, sample - (total - target_total))
            steps.append(step("HYPERGEO_FORMULA",
                              "P(X ≤ k) = Σ C(K,i)·C(N − K,n − i)/C(N,n)"))
            terms = []
            for count in range(lower, cutoff + 1):
                extra, value = _pmf_steps(total, target_total, sample, count)
                steps.extend(extra)
                terms.append(value)
            additions, value = _sum_exact(terms)
            steps.extend(additions)
            steps.append(step("CHECK", f"summed X = {lower} through {cutoff}",
                              prob_txt(value)))
            answer = prob_txt(value)
        elif variant == "mean":
            product = sample * target_total
            value = Fraction(product, total)
            steps.extend([
                step("HYPERGEO_FORMULA", "E[X] = nK/N"),
                step("M", sample, target_total, product),
                step("D", product, total, prob_txt(value)),
            ])
            answer = f"E[X] = {prob_txt(value)}"
        else:
            other_total = total - target_total
            p = Fraction(target_total, total)
            q = Fraction(other_total, total)
            remaining = total - sample
            population_gap = total - 1
            fpc = Fraction(remaining, population_gap)
            np_value = sample * p
            npq = np_value * q
            value = npq * fpc
            steps.extend([
                step("HYPERGEO_FORMULA",
                     "Var(X) = n(K/N)(1 − K/N)(N − n)/(N − 1)"),
                step("D", target_total, total, prob_txt(p)),
                step("S", 1, prob_txt(p), prob_txt(q)),
                step("S", total, sample, remaining),
                step("S", total, 1, population_gap),
                step("D", remaining, population_gap, prob_txt(fpc)),
                step("M", sample, prob_txt(p), prob_txt(np_value)),
                step("M", prob_txt(np_value), prob_txt(q), prob_txt(npq)),
                step("M", prob_txt(npq), prob_txt(fpc), prob_txt(value)),
            ])
            answer = f"Var(X) = {prob_txt(value)}"
        return prefix, steps, answer

    @staticmethod
    def _three_types():
        colors = random.choice(COLOR_SETS)
        counts = tuple(random.randint(2, 4) for _ in colors)
        total = sum(counts)
        sample = random.randint(3, min(6, total - 1))
        while True:
            selected = random.sample(
                [(index, item) for index, count in enumerate(counts)
                 for item in range(count)], sample)
            targets = tuple(sum(index == color_index for index, _ in selected)
                            for color_index in range(3))
            if all(targets):
                break
        batch = random.choice(BATCHES)
        inventory = "; ".join(f"{count} {color} marbles"
                              for color, count in zip(colors, counts))
        goal = ", ".join(f"{target} {color}"
                         for color, target in zip(colors, targets))
        prefix = (f"In the {batch} lot, a bag has {inventory}. A sample "
                  f"of {sample} marbles is drawn uniformly without replacement. "
                  f"Target counts: {goal}.")
        favorable_parts = [math.comb(count, target)
                           for count, target in zip(counts, targets)]
        favorable = 1
        steps = [step("HYPERGEO_SETUP", f"N = {total}, n = {sample}", goal),
                 step("HYPERGEO_FORMULA",
                      "P(counts) = product of type combinations/C(N,n)")]
        for count, target, value in zip(counts, targets, favorable_parts):
            steps.append(step("NCR", f"C({count}, {target})", value))
            steps.append(step("M", favorable, value, favorable * value))
            favorable *= value
        all_samples = math.comb(total, sample)
        probability = Fraction(favorable, all_samples)
        steps.extend([
            step("NCR", f"C({total}, {sample})", all_samples),
            step("FRAC_BUILD", f"{favorable}/{all_samples}",
                 prob_txt(probability)),
            step("CHECK", "target counts sum to sample",
                 " + ".join(map(str, targets)), sample),
        ])
        return prefix, steps, prob_txt(probability)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "three_types":
            prefix, steps, answer = self._three_types()
        else:
            prefix, steps, answer = self._two_type(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_hypergeometric_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}


def _sum_exact(values):
    steps = []
    running = values[0]
    for value in values[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(value),
                          prob_txt(running + value)))
        running += value
    return steps, running
