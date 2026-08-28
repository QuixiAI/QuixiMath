"""Compute complements in finite exact probability models.

Variants: ``not_event``, ``missing_probability``,
``at_least_one_two_stage``, and ``complement_of_described``. Op-codes:
``EVENT``, ``WEIGHT``, ``PROB_SETUP``, ``F``, ``L``, ``C``, ``A``, ``S``,
``M``, ``COMPLEMENT``, ``CHECK``, and ``Z``. Random finite models and five phrasings
per variant give an unbounded problem space.
"""
import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
PLACES = (
    "classroom", "game club", "science lab", "school fair", "library",
    "museum", "math club", "community center", "study hall", "robotics lab",
    "design studio", "field station", "learning center", "workshop",
)
COLORS = ("amber", "blue", "green", "orange", "purple", "red", "teal")
QUERIES = {
    "not_event": (
        "Find the probability that event A does not occur.",
        "Compute P(Aᶜ) by the complement rule.",
        "Count event A, then determine the chance of not A.",
        "Use one minus P(A) to find the requested probability.",
        "Give the exact probability of the complementary event.",
    ),
    "missing_probability": (
        "Find the missing outcome probability.",
        "Use total probability one to determine x.",
        "Compute the unlisted weight from the finite probability model.",
        "Add the known outcome probabilities, then find the remainder.",
        "Complete the probability assignment with an exact value.",
    ),
    "at_least_one_two_stage": (
        "Find the probability of at least one success.",
        "Use the complement of two failures to compute the event chance.",
        "Determine the exact chance that one or both stages succeed.",
        "Compute one minus the probability that neither stage succeeds.",
        "Apply the complement rule to the independent two-stage model.",
    ),
    "complement_of_described": (
        "Find P(Aᶜ) for the described event.",
        "Determine the exact chance of the outcomes outside A.",
        "Use the displayed event roster to compute its complement.",
        "Count the non-event outcomes and give their probability.",
        "Apply the complement rule to the finite card experiment.",
    ),
}


def complement_steps(event, favorable, total):
    value = Fraction(favorable, total)
    result = 1 - value
    value_text, result_text = prob_txt(value), prob_txt(result)
    steps = [step("EVENT", "A", event, favorable),
             step("PROB_SETUP", favorable, total)]
    if value.denominator != total:
        steps.append(step("F", f"{favorable}/{total}", value_text))
    steps.append(step("COMPLEMENT", "P(Aᶜ) = 1 − P(A)",
                      f"1 − {value_text}", result_text))
    steps.append(step("CHECK", "P(A) + P(Aᶜ)",
                      f"{value_text} + {result_text}", "1"))
    return steps, result_text


class ComplementProbabilityGenerator(ProblemGenerator):
    """Generate exact finite complement-probability exercises."""

    VARIANTS = ("not_event", "missing_probability",
                "at_least_one_two_stage", "complement_of_described")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _not_event():
        total = random.randint(6, 40)
        labels = tuple(range(1, total + 1))
        divisor = random.randint(2, min(7, total - 1))
        event = tuple(value for value in labels if value % divisor == 0)
        problem = (f"An equal-area spinner has sectors S = {roster(labels)}. "
                   f"Event A is landing on a multiple of {divisor}; "
                   f"A = {roster(event)}.")
        steps, answer = complement_steps(roster(event), len(event), total)
        return problem, steps, answer

    @staticmethod
    def _missing():
        labels = tuple(sorted(random.sample(COLORS, 3)))
        denominator = random.randint(8, 100)
        first = random.randint(1, denominator - 2)
        second = random.randint(1, denominator - first - 1)
        numerators = (first, second, denominator - first - second)
        missing_index = random.randrange(3)
        known = [(label, Fraction(value, denominator))
                 for index, (label, value) in enumerate(zip(labels, numerators))
                 if index != missing_index]
        missing_label = labels[missing_index]
        known_text = "; ".join(
            f"P({label}) = {prob_txt(value)}" for label, value in known)
        problem = (f"A finite model has outcomes {', '.join(labels)}. "
                   f"Known weights: {known_text}; P({missing_label}) = x.")
        common = math.lcm(*(value.denominator for _, value in known))
        converted = [value.numerator * (common // value.denominator)
                     for _, value in known]
        known_sum = sum(value for _, value in known)
        missing = 1 - known_sum
        steps = [step("WEIGHT", label, prob_txt(value))
                 for label, value in known]
        steps.append(step("L", *(value.denominator for _, value in known), common))
        steps.extend(step("C", prob_txt(value), common,
                          f"{numerator}/{common}")
                     for (_, value), numerator in zip(known, converted)
                     if value.denominator != common)
        steps.append(step("A", *(prob_txt(value) for _, value in known),
                          prob_txt(known_sum)))
        steps.append(step("S", "1", prob_txt(known_sum), prob_txt(missing)))
        steps.append(step("CHECK", "all outcome weights sum to 1",
                          f"{prob_txt(known_sum)} + {prob_txt(missing)}", "1"))
        return problem, steps, prob_txt(missing)

    @staticmethod
    def _at_least_one():
        first_total, second_total = random.randint(3, 20), random.randint(3, 20)
        first_success = random.randint(1, first_total - 1)
        second_success = random.randint(1, second_total - 1)
        first = Fraction(first_success, first_total)
        second = Fraction(second_success, second_total)
        none = (1 - first) * (1 - second)
        answer_value = 1 - none
        problem = (f"Two independent stages are performed. Stage 1 succeeds "
                   f"in {first_success} of {first_total} equally likely "
                   f"outcomes; stage 2 succeeds in {second_success} of "
                   f"{second_total} equally likely outcomes.")
        steps = [step("PROB_SETUP", first_success, first_total),
                 step("PROB_SETUP", second_success, second_total),
                 step("COMPLEMENT", "stage 1 failure",
                      f"1 − {prob_txt(first)}", prob_txt(1 - first)),
                 step("COMPLEMENT", "stage 2 failure",
                      f"1 − {prob_txt(second)}", prob_txt(1 - second)),
                 step("M", prob_txt(1 - first), prob_txt(1 - second),
                      prob_txt(none)),
                 step("COMPLEMENT", "at least one success",
                      f"1 − {prob_txt(none)}", prob_txt(answer_value)),
                 step("CHECK", "none + at least one",
                      f"{prob_txt(none)} + {prob_txt(answer_value)}", "1")]
        return problem, steps, prob_txt(answer_value)

    @staticmethod
    def _described():
        total = random.randint(6, 35)
        start = random.randint(-1000, 1000)
        labels = tuple(range(start, start + total))
        case = random.choice(("even", "positive", "at least"))
        if case == "even":
            event = tuple(value for value in labels if value % 2 == 0)
            description = "an even number"
        elif case == "positive":
            event = tuple(value for value in labels if value > 0)
            if not event or len(event) == total:
                cutoff = labels[total // 2]
                event = tuple(value for value in labels if value >= cutoff)
                description = f"a number at least {cutoff}"
            else:
                description = "a positive number"
        else:
            cutoff = random.choice(labels[1:-1])
            event = tuple(value for value in labels if value >= cutoff)
            description = f"a number at least {cutoff}"
        problem = (f"Numbered cards form S = {roster(labels)}. Event A is "
                   f"drawing {description}; A = {roster(event)}.")
        steps, answer = complement_steps(roster(event), len(event), total)
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "not_event":
            prefix, steps, answer = self._not_event()
        elif variant == "missing_probability":
            prefix, steps, answer = self._missing()
        elif variant == "at_least_one_two_stage":
            prefix, steps, answer = self._at_least_one()
        else:
            prefix, steps, answer = self._described()
        contextual = prefix[0].lower() + prefix[1:]
        problem = (f"At the {random.choice(PLACES)}, {contextual} "
                   f"{random.choice(QUERIES[variant])}")
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_complement_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
