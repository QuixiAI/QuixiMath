"""Convert among probabilities, counts, and odds ratios.

Variants: ``prob_to_odds_for``, ``prob_to_odds_against``, ``odds_to_prob``,
``from_counts``, and ``odds_of_complement``. Op-codes: ``ODDS_FORMULA``,
``COMPLEMENT``, ``A``, ``PROB_SETUP``, ``ODDS``, ``ODDS_REDUCE``, ``CHECK``,
and ``Z``. Random exact ratios, contexts, and five phrasings give an
unbounded problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import odds_txt, prob_txt


PROBABILITY = True
EVENTS = ("rain", "a win", "a correct answer", "a red draw", "a make",
          "an on-time arrival", "a successful trial", "a six", "a renewal")
QUERIES = {
    "prob_to_odds_for": (
        "Convert the probability to odds in favor.",
        "Find the reduced success-to-failure ratio.",
        "Give the exact odds for the event.",
        "Use P(A) and P(Aᶜ) to form odds in favor.",
        "Report favorable odds as a reduced colon ratio.",
    ),
    "prob_to_odds_against": (
        "Convert the probability to odds against.",
        "Find the reduced failure-to-success ratio.",
        "Give the exact odds against the event.",
        "Use P(Aᶜ) and P(A) to form odds against.",
        "Report unfavorable odds as a reduced colon ratio.",
    ),
    "odds_to_prob": (
        "Convert the odds in favor to an exact probability.",
        "Add the two odds parts, then find P(A).",
        "Recover the event probability from the favorable odds.",
        "Turn the success-to-failure ratio into a reduced fraction.",
        "Use favorable divided by total odds parts to compute P(A).",
    ),
    "from_counts": (
        "Find the reduced odds in favor of the focus outcome.",
        "Convert the two outcome counts to favorable odds.",
        "Reduce the focus-to-other count ratio.",
        "Give the exact odds for the named outcome.",
        "Use the observed counts to form a colon ratio.",
    ),
    "odds_of_complement": (
        "Find the odds in favor of the complementary event.",
        "Convert P(Aᶜ) to reduced favorable odds.",
        "Reverse the event and report the complement's odds.",
        "Use the failure probability as the new favorable part.",
        "Determine the exact odds for not A.",
    ),
}


def reverse_odds(value):
    favorable = odds_txt(value)
    left, right = favorable.split(":")
    return f"{right}:{left}"


class OddsProbabilityGenerator(ProblemGenerator):
    """Generate exact conversions between probabilities, odds, and counts."""

    VARIANTS = ("prob_to_odds_for", "prob_to_odds_against", "odds_to_prob",
                "from_counts", "odds_of_complement")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _probability_case(mode):
        denominator = random.randint(3, 1000)
        numerator = random.randint(1, denominator - 1)
        value = Fraction(numerator, denominator)
        event = random.choice(EVENTS)
        problem = f"For event A ({event}), P(A) = {prob_txt(value)}."
        complement = 1 - value
        steps = [step("ODDS_FORMULA",
                      "odds for A = P(A) : P(Aᶜ)"),
                 step("COMPLEMENT", "P(Aᶜ) = 1 − P(A)",
                      f"1 − {prob_txt(value)}", prob_txt(complement))]
        if mode == "prob_to_odds_for":
            answer = odds_txt(value)
            steps.append(step("ODDS", "for", answer))
        elif mode == "prob_to_odds_against":
            answer = reverse_odds(value)
            steps[0] = step("ODDS_FORMULA",
                            "odds against A = P(Aᶜ) : P(A)")
            steps.append(step("ODDS", "against", answer))
        else:
            answer = odds_txt(complement)
            steps[0] = step("ODDS_FORMULA",
                            "odds for Aᶜ = P(Aᶜ) : P(A)")
            steps.append(step("ODDS", "for complement", answer))
        steps.append(step("CHECK", "ratio reduced", answer))
        return problem, steps, answer

    @staticmethod
    def _odds_to_probability():
        first, second = random.randint(1, 1000), random.randint(1, 1000)
        divisor = math.gcd(first, second)
        first, second = first // divisor, second // divisor
        total = first + second
        value = Fraction(first, total)
        problem = f"The odds in favor of event A are {first}:{second}."
        steps = [step("ODDS_FORMULA", "P(A) = favorable/(favorable + against)"),
                 step("A", first, second, total),
                 step("PROB_SETUP", first, total),
                 step("CHECK", f"odds {first}:{second}", prob_txt(value))]
        return problem, steps, prob_txt(value)

    @staticmethod
    def _counts():
        labels = random.sample(("red", "blue", "green", "orange", "purple",
                                "silver", "teal"), 2)
        first, second = random.randint(1, 1000), random.randint(1, 1000)
        raw = f"{first}:{second}"
        divisor = math.gcd(first, second)
        answer = f"{first // divisor}:{second // divisor}"
        problem = (f"Observed outcome counts are {labels[0]}={first}; "
                   f"{labels[1]}={second}. Focus outcome: {labels[0]}.")
        steps = [step("ODDS", "for", raw),
                 step("ODDS_REDUCE", raw, answer),
                 step("CHECK", f"gcd={divisor}", answer)]
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("prob_to_odds_for", "prob_to_odds_against",
                       "odds_of_complement"):
            prefix, steps, answer = self._probability_case(variant)
        elif variant == "odds_to_prob":
            prefix, steps, answer = self._odds_to_probability()
        else:
            prefix, steps, answer = self._counts()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_odds_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
