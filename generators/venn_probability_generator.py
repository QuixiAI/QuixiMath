"""Compute exact probabilities from two- and three-set Venn data.

Variants: ``only_A``, ``neither``, ``union``, ``exactly_one``,
``from_probabilities``, and ``three_set``. Op-codes: ``VENN_REGION``,
``IE_FORMULA``, ``A``, ``S``, ``PROB_SETUP``, ``F``, and ``Z``. Region
counts are constructed backward, and contexts, counts, targets, and five
phrasings give an unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
CONTEXTS = (
    ("campers", "camper", "swim", "hike"),
    ("students", "student", "join music", "play sports"),
    ("visitors", "visitor", "tour the gallery", "enter the garden"),
    ("employees", "employee", "work remotely", "use transit"),
    ("readers", "reader", "choose fiction", "choose history"),
    ("athletes", "athlete", "run", "swim"),
    ("customers", "customer", "buy tea", "buy pastry"),
    ("travelers", "traveler", "check luggage", "choose a window seat"),
)
QUERIES = {
    "only_A": (
        "Find P(A but not B) and P(neither A nor B).",
        "Compute the A-only chance followed by the chance outside both events.",
        "What are the exact probabilities of only A and of neither event?",
        "Use the Venn regions to report A without B, then neither.",
        "Determine both the A-only probability and the probability of neither.",
    ),
    "neither": (
        "Find the probability of neither A nor B.",
        "Compute the chance that the selected item lies outside both events.",
        "What fraction of the population meets neither condition?",
        "Use the union count to determine P(neither A nor B).",
        "Determine the exact probability of being in neither set.",
    ),
    "union": (
        "Find P(A ∪ B).",
        "Compute the probability that at least one event occurs.",
        "What is the exact chance of A or B?",
        "Use the three inside regions to determine the union probability.",
        "Find the measure of the union of A and B.",
    ),
    "exactly_one": (
        "Find the probability that exactly one of A and B occurs.",
        "Add the two non-overlapping only-regions and divide by the total.",
        "What is the exact chance of A only or B only?",
        "Compute the probability of belonging to exactly one set.",
        "Determine the exclusive-one-event probability from the Venn regions.",
    ),
    "from_probabilities": (
        "Find P(A ∪ B) and P(Aᶜ ∩ Bᶜ).",
        "Use inclusion-exclusion to report the union and neither probabilities.",
        "Compute the exact measures of at least one event and of neither event.",
        "Determine P(A or B), then its complement.",
        "Report the union probability followed by the outside-both probability.",
    ),
    "three_set": (
        "Find P(A ∪ B ∪ C) and the probability of none of the three events.",
        "Apply three-set inclusion-exclusion, then compute the outside region.",
        "Report the exact union probability and its none-of-the-events complement.",
        "Use all singles, pair intersections, and the triple intersection.",
        "Determine the measure inside at least one set and the measure outside all sets.",
    ),
}


def _probability_steps(numerator, denominator):
    value = Fraction(numerator, denominator)
    raw = f"{numerator}/{denominator}"
    steps = [step("PROB_SETUP", numerator, denominator)]
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, value


class VennProbabilityGenerator(ProblemGenerator):
    """Generate exact Venn-region probability exercises."""

    VARIANTS = ("only_A", "neither", "union", "exactly_one",
                "from_probabilities", "three_set")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _two_set(variant):
        plural, singular, action_a, action_b = random.choice(CONTEXTS)
        only_a, both, only_b, neither = (random.randint(1, 70) for _ in range(4))
        total = only_a + both + only_b + neither
        count_a, count_b = only_a + both, only_b + both
        union_count = only_a + both + only_b
        prefix = (f"Of {total} {plural}, {count_a} {action_a}, {count_b} "
                  f"{action_b}, and {both} do both. Let A mean '{action_a}' "
                  f"and B mean '{action_b}'. One {singular} is chosen uniformly.")
        steps = [
            step("VENN_REGION", "A ∩ B", both),
            step("S", count_a, both, only_a),
            step("VENN_REGION", "A only", only_a),
            step("S", count_b, both, only_b),
            step("VENN_REGION", "B only", only_b),
            step("A", only_a, both, only_a + both),
            step("A", only_a + both, only_b, union_count),
            step("VENN_REGION", "A ∪ B", union_count),
            step("S", total, union_count, neither),
            step("VENN_REGION", "neither", neither),
        ]
        if variant == "only_A":
            first_steps, first = _probability_steps(only_a, total)
            second_steps, second = _probability_steps(neither, total)
            steps.extend(first_steps + second_steps)
            answer = f"{prob_txt(first)}; {prob_txt(second)}"
        elif variant == "neither":
            extra, value = _probability_steps(neither, total)
            steps.extend(extra)
            answer = prob_txt(value)
        elif variant == "union":
            extra, value = _probability_steps(union_count, total)
            steps.extend(extra)
            answer = prob_txt(value)
        else:
            exactly_one = only_a + only_b
            steps.append(step("A", only_a, only_b, exactly_one))
            steps.append(step("VENN_REGION", "exactly one", exactly_one))
            extra, value = _probability_steps(exactly_one, total)
            steps.extend(extra)
            answer = prob_txt(value)
        return prefix, steps, answer

    @staticmethod
    def _from_probabilities():
        total = random.randint(12, 140)
        cuts = sorted(random.sample(range(1, total), 3))
        only_a, both, only_b, neither = (
            cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2])
        p_a = Fraction(only_a + both, total)
        p_b = Fraction(only_b + both, total)
        p_both = Fraction(both, total)
        union = p_a + p_b - p_both
        outside = 1 - union
        prefix = (f"Events A and B satisfy P(A) = {prob_txt(p_a)}, P(B) = "
                  f"{prob_txt(p_b)}, and P(A ∩ B) = {prob_txt(p_both)}.")
        summed = p_a + p_b
        steps = [
            step("VENN_REGION", "A ∩ B", prob_txt(p_both)),
            step("IE_FORMULA", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)"),
            step("A", prob_txt(p_a), prob_txt(p_b), prob_txt(summed)),
            step("S", prob_txt(summed), prob_txt(p_both), prob_txt(union)),
            step("VENN_REGION", "A ∪ B", prob_txt(union)),
            step("S", 1, prob_txt(union), prob_txt(outside)),
            step("VENN_REGION", "Aᶜ ∩ Bᶜ", prob_txt(outside)),
        ]
        answer = (f"P(A ∪ B) = {prob_txt(union)}; "
                  f"P(Aᶜ ∩ Bᶜ) = {prob_txt(outside)}")
        return prefix, steps, answer

    @staticmethod
    def _three_set():
        only_a, only_b, only_c = (random.randint(1, 50) for _ in range(3))
        ab_only, ac_only, bc_only = (random.randint(1, 40) for _ in range(3))
        abc, none = random.randint(1, 30), random.randint(1, 60)
        a = only_a + ab_only + ac_only + abc
        b = only_b + ab_only + bc_only + abc
        c = only_c + ac_only + bc_only + abc
        ab, ac, bc = ab_only + abc, ac_only + abc, bc_only + abc
        union = a + b + c - ab - ac - bc + abc
        total = union + none
        prefix = (f"A population has {total} items with card(A) = {a}, card(B) = "
                  f"{b}, card(C) = {c}, card(A ∩ B) = {ab}, card(A ∩ C) = "
                  f"{ac}, card(B ∩ C) = {bc}, and card(A ∩ B ∩ C) = {abc}. "
                  "One item is chosen uniformly.")
        s1, s2 = a + b, a + b + c
        s3, s4, s5 = s2 - ab, s2 - ab - ac, s2 - ab - ac - bc
        steps = [
            step("VENN_REGION", "A ∩ B ∩ C", abc),
            step("IE_FORMULA", "card(A ∪ B ∪ C) = singles − pairs + triple"),
            step("A", a, b, s1),
            step("A", s1, c, s2),
            step("S", s2, ab, s3),
            step("S", s3, ac, s4),
            step("S", s4, bc, s5),
            step("A", s5, abc, union),
            step("VENN_REGION", "A ∪ B ∪ C", union),
            step("S", total, union, none),
            step("VENN_REGION", "none", none),
        ]
        union_steps, p_union = _probability_steps(union, total)
        none_steps, p_none = _probability_steps(none, total)
        steps.extend(union_steps + none_steps)
        answer = (f"P(A ∪ B ∪ C) = {prob_txt(p_union)}; "
                  f"P(none) = {prob_txt(p_none)}")
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "from_probabilities":
            prefix, steps, answer = self._from_probabilities()
        elif variant == "three_set":
            prefix, steps, answer = self._three_set()
        else:
            prefix, steps, answer = self._two_set(variant)
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        result = {"problem_id": jid(),
                  "operation": f"probability_venn_{variant}",
                  "problem": problem, "steps": steps, "final_answer": answer}
        if variant == "three_set":
            result["difficulty"] = 4
        return result
