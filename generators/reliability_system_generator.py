"""Compute exact reliability of independent component systems.

Variants: ``series``, ``parallel``, ``both``, ``mixed``,
``at_least_one_distinct``, and ``exactly_one``. Op-codes:
``COMPLEMENT``, ``M``, ``S``, ``A``, ``SUM``, ``RELIABILITY``, and ``Z``.
Random component names, exact working probabilities, sizes, and five
phrasings give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
COMPONENTS = ("alarm", "battery", "controller", "fan", "filter", "fuse",
              "motor", "panel", "pump", "relay", "router", "sensor",
              "server", "switch", "valve", "wire", "compressor", "drive",
              "gateway", "inverter", "module", "transmitter")
PROBABILITY_BANK = (
    Fraction(1, 5), Fraction(1, 4), Fraction(3, 10), Fraction(1, 3),
    Fraction(3, 8), Fraction(2, 5), Fraction(1, 2), Fraction(3, 5),
    Fraction(5, 8), Fraction(2, 3), Fraction(7, 10), Fraction(3, 4),
    Fraction(4, 5), Fraction(5, 6), Fraction(7, 8), Fraction(9, 10),
)
QUERIES = {
    "series": (
        "Find the probability the system works when all components are in series.",
        "Multiply the component reliabilities for the series-system chance.",
        "What is the exact reliability when every listed component must work?",
        "Use independence to compute the all-components-working probability.",
        "Determine the working probability of the series connection.",
    ),
    "parallel": (
        "Find the probability the system works when all components are in parallel.",
        "Use the all-fail complement to compute the parallel reliability.",
        "What is the exact chance that at least one parallel component works?",
        "Compute one minus the probability that every component fails.",
        "Determine the working probability of the parallel connection.",
    ),
    "both": (
        "Find the reliability if the components are in series and if they are in parallel.",
        "Report the exact series probability followed by the parallel probability.",
        "Compute both all-work and at-least-one-works system reliabilities.",
        "Compare the series and parallel working chances for these components.",
        "Give both standard connection reliabilities in exact form.",
    ),
    "mixed": (
        "Find the reliability of the displayed mixed connection.",
        "Compute the parallel block first, then multiply through the series stages.",
        "What is the exact working probability of this series-parallel system?",
        "Use independence for the parallel pair and the remaining series components.",
        "Determine the mixed-system reliability from its block structure.",
    ),
    "at_least_one_distinct": (
        "Find the probability that at least one component works.",
        "Use the complement of all distinct components failing.",
        "What is the exact chance of one or more working components?",
        "Multiply the unequal failure probabilities, then subtract from 1.",
        "Determine the at-least-one reliability for the listed components.",
    ),
    "exactly_one": (
        "Find the probability that exactly one component works.",
        "Add the mutually exclusive cases with one success and all other failures.",
        "What is the exact chance of a single working component?",
        "Compute every one-worker path and sum the path probabilities.",
        "Determine the exactly-one reliability from the independent states.",
    ),
}


def _product_steps(values):
    values = list(values)
    running = values[0]
    steps = []
    for value in values[1:]:
        steps.append(step("M", prob_txt(running), prob_txt(value),
                          prob_txt(running * value)))
        running *= value
    return steps, running


def _failure_steps(names, probabilities):
    failures = []
    steps = []
    for name, probability in zip(names, probabilities):
        failure = 1 - probability
        steps.append(step("COMPLEMENT",
                          f"P({name} fails) = 1 − P({name} works)",
                          f"1 − {prob_txt(probability)}", prob_txt(failure)))
        failures.append(failure)
    return steps, failures


def _series_flow(names, probabilities, label="series"):
    steps, value = _product_steps(probabilities)
    rule = " × ".join(prob_txt(p) for p in probabilities)
    steps.append(step("RELIABILITY", label, rule, prob_txt(value)))
    return steps, value


def _parallel_flow(names, probabilities, label="parallel"):
    steps, failures = _failure_steps(names, probabilities)
    product_steps, all_fail = _product_steps(failures)
    steps.extend(product_steps)
    value = 1 - all_fail
    steps.append(step("S", 1, prob_txt(all_fail), prob_txt(value)))
    rule = "1 − " + " × ".join(prob_txt(q) for q in failures)
    steps.append(step("RELIABILITY", label, rule, prob_txt(value)))
    return steps, value


class ReliabilitySystemGenerator(ProblemGenerator):
    """Generate exact series, parallel, and mixed reliability exercises."""

    VARIANTS = ("series", "parallel", "both", "mixed",
                "at_least_one_distinct", "exactly_one")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _components(variant):
        n = random.randint(3, 5)
        names = tuple(random.sample(COMPONENTS, n))
        if variant == "parallel":
            probability = random.choice(PROBABILITY_BANK)
            probabilities = (probability,) * n
        else:
            probabilities = tuple(random.sample(PROBABILITY_BANK, n))
        given = "; ".join(f"{name}={prob_txt(probability)}"
                          for name, probability in zip(names, probabilities))
        prefix = ("Components have independent working states. Working "
                  f"probabilities: {given}.")
        if variant == "mixed":
            prefix += (f" Design: {names[0]} and {names[1]} form a parallel "
                       "block; that block is in series with "
                       f"{', '.join(names[2:])}.")
        return names, probabilities, prefix

    @classmethod
    def _generate_variant(cls, variant):
        names, probabilities, prefix = cls._components(variant)
        if variant == "series":
            steps, value = _series_flow(names, probabilities)
            answer = prob_txt(value)
        elif variant in ("parallel", "at_least_one_distinct"):
            steps, value = _parallel_flow(names, probabilities,
                                          "parallel" if variant == "parallel"
                                          else "at least one")
            answer = prob_txt(value)
        elif variant == "both":
            series_steps, series = _series_flow(names, probabilities)
            parallel_steps, parallel = _parallel_flow(names, probabilities)
            steps = series_steps + parallel_steps
            answer = (f"series {prob_txt(series)}; "
                      f"parallel {prob_txt(parallel)}")
        elif variant == "mixed":
            parallel_steps, block = _parallel_flow(names[:2], probabilities[:2],
                                                    "parallel block")
            remaining = (block,) + probabilities[2:]
            product_steps, value = _product_steps(remaining)
            steps = parallel_steps + product_steps
            rule = " × ".join([prob_txt(block),
                               *(prob_txt(p) for p in probabilities[2:])])
            steps.append(step("RELIABILITY", "mixed system", rule,
                              prob_txt(value)))
            answer = prob_txt(value)
        else:
            failure_steps, failures = _failure_steps(names, probabilities)
            steps = failure_steps
            terms = []
            for index, name in enumerate(names):
                factors = [probabilities[j] if j == index else failures[j]
                           for j in range(len(names))]
                product_steps, value = _product_steps(factors)
                steps.extend(product_steps)
                steps.append(step("RELIABILITY", f"only {name}",
                                  " × ".join(prob_txt(f) for f in factors),
                                  prob_txt(value)))
                terms.append(value)
            running = terms[0]
            for value in terms[1:]:
                steps.append(step("A", prob_txt(running), prob_txt(value),
                                  prob_txt(running + value)))
                running += value
            steps.append(step("SUM", " + ".join(prob_txt(v) for v in terms),
                              prob_txt(running)))
            answer = prob_txt(running)
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        prefix, steps, answer = self._generate_variant(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_reliability_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
