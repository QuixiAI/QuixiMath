"""Compute event probabilities by summing over a stated partition.

Variants: ``two_causes``, ``three_causes``, ``urn_choice``,
``two_stage_draw``, and ``weather``. Op-codes: ``TOTAL_PROB_FORMULA``,
``TOTAL_PROB_TERM``, ``M``, ``A``, ``CHECK``, and ``Z``. Random exact
priors, rates, contexts, inventories, and five phrasings give an unbounded
problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt


PROBABILITY = True
CAUSE_NAMES = ("amber", "cedar", "delta", "ember", "forest", "granite",
               "harbor", "indigo", "jade", "lunar", "maple", "nova",
               "onyx", "pearl", "quartz", "river", "solar", "topaz")
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal",
          "white", "yellow")
PLACES = ("Albany", "Boston", "Cedarville", "Dover", "Erie", "Fresno",
          "Galveston", "Hartford", "Ithaca", "Juneau", "Kingston",
          "Lowell", "Madison", "Norfolk", "Olympia", "Portland")
RATE_BANK = (Fraction(1, 20), Fraction(1, 10), Fraction(1, 8),
             Fraction(1, 5), Fraction(1, 4), Fraction(3, 10),
             Fraction(1, 3), Fraction(3, 8), Fraction(2, 5),
             Fraction(1, 2), Fraction(3, 5), Fraction(2, 3),
             Fraction(3, 4), Fraction(4, 5), Fraction(9, 10))
QUERIES = {
    "two_causes": (
        "Find the total probability of event B.",
        "Weight each source rate by its prior and add the two terms.",
        "Use the source partition to compute P(B).",
        "What is the exact overall event probability?",
        "Apply the law of total probability across both causes.",
    ),
    "three_causes": (
        "Find the total probability of event B across all three causes.",
        "Multiply each conditional rate by its prior, then sum the terms.",
        "Use the three-part source partition to compute P(B).",
        "What is the exact overall event probability from these causes?",
        "Apply the law of total probability to the full partition.",
    ),
    "urn_choice": (
        "Find the probability that the drawn ball has the target color.",
        "Weight each urn's target-color fraction by its selection prior.",
        "Use total probability over the urn-choice partition.",
        "What is the exact chance of drawing the target color?",
        "Add the prior-times-likelihood term for every urn.",
    ),
    "two_stage_draw": (
        "Find the probability that the second draw has the target color.",
        "Partition on the first draw and compute the second-draw probability.",
        "Use both first-draw branches in the law of total probability.",
        "What is the exact chance that draw two is the target color?",
        "Show that the second-draw marginal equals the initial color fraction.",
    ),
    "weather": (
        "Find the total probability of a delayed commute.",
        "Weight each weather-specific delay rate by its forecast prior.",
        "Use the weather partition to compute the overall delay chance.",
        "What is the exact probability of event B at this location?",
        "Apply total probability across sunny, cloudy, and rainy conditions.",
    ),
}


def _partition(count):
    total = random.randint(max(8, count + 2), 60)
    cuts = sorted(random.sample(range(1, total), count - 1))
    values = [cuts[0]] if cuts else []
    values += [cuts[index] - cuts[index - 1] for index in range(1, len(cuts))]
    values.append(total - cuts[-1] if cuts else total)
    return tuple(Fraction(value, total) for value in values)


def _total_steps(causes, priors, rates, event_label="B"):
    steps = [step("TOTAL_PROB_FORMULA",
                  f"P({event_label}) = Σ P(cause)·P({event_label} given cause)")]
    terms = []
    for cause, prior, rate in zip(causes, priors, rates):
        term = prior * rate
        steps.append(step("M", prob_txt(prior), prob_txt(rate), prob_txt(term)))
        steps.append(step("TOTAL_PROB_TERM", cause,
                          f"{prob_txt(prior)} × {prob_txt(rate)}",
                          prob_txt(term)))
        terms.append(term)
    running = terms[0]
    for term in terms[1:]:
        steps.append(step("A", prob_txt(running), prob_txt(term),
                          prob_txt(running + term)))
        running += term
    prior_running = priors[0]
    for prior in priors[1:]:
        steps.append(step("A", prob_txt(prior_running), prob_txt(prior),
                          prob_txt(prior_running + prior)))
        prior_running += prior
    steps.append(step("CHECK", "partition",
                      " + ".join(prob_txt(prior) for prior in priors),
                      prob_txt(prior_running)))
    return steps, running


def _data_text(causes, priors, rates, event_label):
    return "; ".join(
        f"{cause} prior={prob_txt(prior)} and P({event_label} given {cause})={prob_txt(rate)}"
        for cause, prior, rate in zip(causes, priors, rates))


class LawOfTotalProbabilityGenerator(ProblemGenerator):
    """Generate exact finite-partition total-probability exercises."""

    VARIANTS = ("two_causes", "three_causes", "urn_choice",
                "two_stage_draw", "weather")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _causes(count):
        causes = tuple(random.sample(CAUSE_NAMES, count))
        priors = _partition(count)
        rates = tuple(random.choice(RATE_BANK) for _ in causes)
        kind = "Suppliers" if count == 2 else "Servers"
        event_label = "defect" if count == 2 else "failure"
        prefix = (f"{kind} {', '.join(causes)} form the full source partition. "
                  f"Data: {_data_text(causes, priors, rates, event_label)}. "
                  f"Event B is a {event_label}.")
        steps, answer = _total_steps(causes, priors, rates)
        return prefix, steps, prob_txt(answer)

    @staticmethod
    def _urn():
        causes = tuple(random.sample(CAUSE_NAMES, 3))
        priors = _partition(3)
        target, other = random.sample(COLORS, 2)
        inventories = []
        rates = []
        for cause in causes:
            target_count, other_count = random.randint(1, 30), random.randint(1, 30)
            inventories.append((cause, target_count, other_count))
            rates.append(Fraction(target_count, target_count + other_count))
        prior_text = "; ".join(f"{cause}={prob_txt(prior)}"
                               for cause, prior in zip(causes, priors))
        inventory_text = "; ".join(
            f"{cause} has {target_count} {target} and {other_count} {other}"
            for cause, target_count, other_count in inventories)
        prefix = (f"Choose one urn with priors {prior_text}. Contents: "
                  f"{inventory_text}. Draw one ball. Target color: {target}.")
        steps, answer = _total_steps(causes, priors, tuple(rates), "target")
        return prefix, steps, prob_txt(answer)

    @staticmethod
    def _two_stage():
        target, other = random.sample(COLORS, 2)
        target_count, other_count = random.randint(2, 80), random.randint(2, 80)
        total = target_count + other_count
        causes = (f"first {target}", f"first {other}")
        priors = (Fraction(target_count, total), Fraction(other_count, total))
        rates = (Fraction(target_count - 1, total - 1),
                 Fraction(target_count, total - 1))
        prefix = (f"A bag has {target_count} {target} and {other_count} {other} "
                  f"balls. Draw two without replacement. Target color: {target}.")
        steps, answer = _total_steps(causes, priors, rates, "second target")
        expected = Fraction(target_count, total)
        steps.append(step("CHECK", "second-draw marginal equals initial fraction",
                          prob_txt(answer), prob_txt(expected)))
        return prefix, steps, prob_txt(answer)

    @staticmethod
    def _weather():
        place = random.choice(PLACES)
        causes = ("sunny", "cloudy", "rainy")
        priors = _partition(3)
        rates = tuple(random.choice(RATE_BANK) for _ in causes)
        prefix = (f"At {place}, sunny, cloudy, and rainy form the full weather "
                  f"partition. Data: {_data_text(causes, priors, rates, 'delay')}. "
                  "Event B is a delayed commute.")
        steps, answer = _total_steps(causes, priors, rates)
        return prefix, steps, prob_txt(answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "two_causes":
            prefix, steps, answer = self._causes(2)
        elif variant == "three_causes":
            prefix, steps, answer = self._causes(3)
        elif variant == "urn_choice":
            prefix, steps, answer = self._urn()
        elif variant == "two_stage_draw":
            prefix, steps, answer = self._two_stage()
        else:
            prefix, steps, answer = self._weather()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_total_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
