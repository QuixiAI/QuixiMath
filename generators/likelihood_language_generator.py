"""Translate exact finite probabilities into likelihood language.

Variants: ``classify``, ``compare_two_events``, ``order_events``, and
``certain_impossible``. Op-codes: ``COUNT``, ``SUM``, ``PROB_SETUP``, ``F``,
``LIKELIHOOD``, ``CMP``, ``CHECK``, and ``Z``. Random outcome labels, counts,
experiments, and five phrasings per variant give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
OUTCOMES = (
    "amber", "blue", "coral", "green", "indigo", "lime", "orange",
    "pink", "purple", "red", "silver", "teal", "white", "yellow",
)
EXPERIMENTS = (
    "one draw from a bag",
    "one spin of an equal-area spinner",
    "one tile chosen from a box",
    "one token selected from a jar",
)

QUERIES = {
    "classify": (
        "Classify the focus event on the stated likelihood scale.",
        "Give the likelihood word and its exact probability.",
        "Determine whether the focus event is impossible, unlikely, an even chance, likely, or certain.",
        "Use the displayed scale to describe the event and report its probability.",
        "Translate the exact event chance into the required likelihood language.",
    ),
    "compare_two_events": (
        "State which focus event is more likely and compare their exact probabilities.",
        "Compare the two named outcomes using reduced fractions.",
        "Decide which of the two events has the greater chance.",
        "Give a verbal comparison followed by the exact probability inequality.",
        "Use the counts to compare the two focus events.",
    ),
    "order_events": (
        "Order the three outcomes from least to most likely.",
        "Rank the named events by increasing probability.",
        "List the outcomes in ascending likelihood order.",
        "Use their common total to order the three event chances.",
        "Arrange the focus outcomes from smallest chance to largest chance.",
    ),
    "certain_impossible": (
        "Classify the focus event as impossible or certain and give its probability.",
        "Decide which endpoint of the likelihood scale applies.",
        "Give the exact endpoint probability and its likelihood word.",
        "Use the complete outcome list to classify the focus event.",
        "Determine whether the event can never happen or must happen.",
    ),
}


def likelihood(value):
    if value == 0:
        return "impossible"
    if value < Fraction(1, 2):
        return "unlikely"
    if value == Fraction(1, 2):
        return "even chance"
    if value < 1:
        return "likely"
    return "certain"


def counts_text(labels, counts):
    return "; ".join(f"{label}={count}" for label, count in zip(labels, counts))


def experiment_prefix(labels, counts):
    return (f"Experiment: {random.choice(EXPERIMENTS)}. Outcome counts: "
            f"{counts_text(labels, counts)}. All individual outcomes are "
            "equally likely. Scale: 0 impossible; between 0 and 1/2 "
            "unlikely; 1/2 even chance; between 1/2 and 1 likely; 1 "
            "certain.")


class LikelihoodLanguageGenerator(ProblemGenerator):
    """Generate exact likelihood classification and comparison exercises."""

    VARIANTS = ("classify", "compare_two_events", "order_events",
                "certain_impossible")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _base(self, distinct=False):
        labels = tuple(sorted(random.sample(OUTCOMES, 3)))
        if distinct:
            counts = tuple(random.sample(range(1, 61), 3))
        else:
            counts = tuple(random.randint(1, 60) for _ in labels)
        total = sum(counts)
        prefix = experiment_prefix(labels, counts)
        return labels, counts, total, prefix

    def _classify(self):
        labels = tuple(sorted(random.sample(OUTCOMES, 3)))
        index = random.randrange(3)
        other_counts = [random.randint(1, 30) for _ in range(2)]
        other_total = sum(other_counts)
        desired = random.choice(("unlikely", "even chance", "likely"))
        if desired == "unlikely":
            focus_count = random.randint(1, max(1, other_total - 1))
        elif desired == "even chance":
            focus_count = other_total
        else:
            focus_count = other_total + random.randint(1, 30)
        built = iter(other_counts)
        counts = tuple(focus_count if position == index else next(built)
                       for position in range(3))
        total = sum(counts)
        prefix = experiment_prefix(labels, counts)
        label, count = labels[index], counts[index]
        value = Fraction(count, total)
        value_text = prob_txt(value)
        category = likelihood(value)
        if category != desired:
            raise AssertionError("likelihood construction failed")
        problem = (f"{prefix} Focus event: outcome {label}. "
                   f"{random.choice(QUERIES['classify'])}")
        steps = [step("COUNT", label, count),
                 step("SUM", " + ".join(map(str, counts)), total),
                 step("PROB_SETUP", count, total)]
        if value.denominator != total:
            steps.append(step("F", f"{count}/{total}", value_text))
        steps.append(step("LIKELIHOOD", value_text, category))
        return problem, steps, f"{category}; {value_text}"

    def _compare(self):
        labels, counts, total, prefix = self._base(distinct=True)
        first, second = random.sample(range(3), 2)
        left, right = labels[first], labels[second]
        left_value = Fraction(counts[first], total)
        right_value = Fraction(counts[second], total)
        if left_value > right_value:
            winner, loser = left, right
            high, low = left_value, right_value
        else:
            winner, loser = right, left
            high, low = right_value, left_value
        answer = (f"{winner} is more likely than {loser}; "
                  f"{prob_txt(high)} > {prob_txt(low)}")
        problem = (f"{prefix} Focus events: outcome {left} and outcome "
                   f"{right}. {random.choice(QUERIES['compare_two_events'])}")
        steps = [step("COUNT", left, counts[first]),
                 step("COUNT", right, counts[second]),
                 step("SUM", " + ".join(map(str, counts)), total),
                 step("CMP", f"P({left})={prob_txt(left_value)}",
                      f"P({right})={prob_txt(right_value)}", answer)]
        return problem, steps, answer

    def _order(self):
        labels, counts, total, prefix = self._base(distinct=True)
        ordered = sorted(range(3), key=lambda index: counts[index])
        answer = ", ".join(labels[index] for index in ordered)
        problem = (f"{prefix} Focus events: outcomes {', '.join(labels)}. "
                   f"{random.choice(QUERIES['order_events'])}")
        steps = [step("COUNT", label, count)
                 for label, count in zip(labels, counts)]
        steps.append(step("SUM", " + ".join(map(str, counts)), total))
        steps.append(step("CMP", "least to most", answer))
        return problem, steps, answer

    def _endpoint(self):
        labels, counts, total, prefix = self._base()
        impossible = random.choice((True, False))
        if impossible:
            absent = random.choice([name for name in OUTCOMES if name not in labels])
            focus = f"outcome {absent}"
            category, value_text, favorable = "impossible", "0", 0
        else:
            focus = "one of the three listed outcomes"
            category, value_text, favorable = "certain", "1", total
        problem = (f"{prefix} Focus event: {focus}. "
                   f"{random.choice(QUERIES['certain_impossible'])}")
        steps = [step("SUM", " + ".join(map(str, counts)), total),
                 step("PROB_SETUP", favorable, total),
                 step("LIKELIHOOD", value_text, category),
                 step("CHECK", focus, category)]
        return problem, steps, f"{category}; {value_text}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "classify":
            problem, steps, answer = self._classify()
        elif variant == "compare_two_events":
            problem, steps, answer = self._compare()
        elif variant == "order_events":
            problem, steps, answer = self._order()
        else:
            problem, steps, answer = self._endpoint()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"probability_likelihood_language_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
