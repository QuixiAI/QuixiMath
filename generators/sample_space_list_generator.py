"""Enumerate small product sample spaces and exact event probabilities.

Variants: ``list_and_count``, ``event_probability``, ``two_coins``,
``two_spinners``, and ``digit_cards``. Op-codes: ``SAMPLE_SPACE``,
``OUTCOME_CHECK``, ``EVENT``, ``PROB_SETUP``, ``F``, ``CHECK``, and ``Z``.
Random component labels and five phrasings give an unbounded problem space.
"""
import itertools
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
COIN_NAMES = (
    "amber", "blue", "copper", "gold", "green", "indigo", "orange",
    "purple", "red", "silver", "teal", "white",
)
QUERIES = {
    "list_and_count": (
        "List the complete sample space and count its outcomes.",
        "Enumerate every ordered outcome, then give the total count.",
        "Build the Cartesian sample space in the stated order.",
        "Write all possible outcomes without omissions and report how many there are.",
        "Use the component order to list and count the sample space.",
    ),
    "event_probability": (
        "List the sample space and find the exact probability of event A.",
        "Enumerate every outcome, test event A, and give its probability.",
        "Build the product space before counting the favorable outcomes.",
        "List and count all outcomes, then compute P(A).",
        "Use complete enumeration to determine the event chance.",
    ),
    "two_coins": (
        "List the four ordered outcomes and find the probability of event A.",
        "Enumerate the two-coin sample space and count event A.",
        "Use first-coin then second-coin order to compute P(A).",
        "Build the complete two-coin table and give the event probability.",
        "Check all four head-tail strings for event A.",
    ),
    "two_spinners": (
        "List the ordered pairs and find the exact probability of event A.",
        "Enumerate the two-spinner Cartesian product before counting event A.",
        "Use first-spinner then second-spinner order to compute P(A).",
        "Build the complete ordered-pair sample space and give the event probability.",
        "Check every spinner pair and determine P(A).",
    ),
    "digit_cards": (
        "List the two-digit numbers and find the exact probability of event A.",
        "Enumerate the no-repeat arrangements before counting event A.",
        "Use each card once to build the sample space and compute P(A).",
        "List all ordered two-card numbers, then give the event probability.",
        "Check every no-replacement arrangement for event A.",
    ),
}


def joined(items):
    return ", ".join(map(str, items))


def probability_steps(component, outcomes, favorable, description):
    steps = [step("SAMPLE_SPACE", component, joined(outcomes), len(outcomes))]
    favorable_set = set(favorable)
    steps.extend(step("OUTCOME_CHECK", outcome, description,
                      "yes" if outcome in favorable_set else "no")
                 for outcome in outcomes)
    steps.append(step("EVENT", "A", joined(favorable), len(favorable)))
    steps.append(step("PROB_SETUP", len(favorable), len(outcomes)))
    value = Fraction(len(favorable), len(outcomes))
    if value.denominator != len(outcomes):
        steps.append(step("F", f"{len(favorable)}/{len(outcomes)}",
                          prob_txt(value)))
    steps.append(step("CHECK", "favorable outcomes rescanned", len(favorable)))
    return steps, prob_txt(value)


class SampleSpaceListGenerator(ProblemGenerator):
    """Generate exact enumeration exercises for small finite experiments."""

    VARIANTS = ("list_and_count", "event_probability", "two_coins",
                "two_spinners", "digit_cards")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _coin_spinner(variant):
        sectors = tuple(sorted(random.sample(range(1, 100), random.randint(2, 6))))
        outcomes = tuple(f"{coin}{sector}"
                         for coin in ("H", "T") for sector in sectors)
        component = "coin × spinner"
        prefix = (f"A coin is flipped and a spinner with sectors "
                  f"{roster(sectors)} is spun. Outcomes put H before T and "
                  "write the spinner label second.")
        if variant == "list_and_count":
            answer = f"{joined(outcomes)}; {len(outcomes)} outcomes"
            steps = [step("SAMPLE_SPACE", component, joined(outcomes),
                          len(outcomes)),
                     step("CHECK", "2 × sectors", f"2 × {len(sectors)}",
                          len(outcomes))]
            return prefix, steps, answer
        parity = random.choice(("odd", "even"))
        favorable = tuple(f"H{sector}" for sector in sectors
                          if sector % 2 == (1 if parity == "odd" else 0))
        if not favorable:
            parity = "odd" if parity == "even" else "even"
            favorable = tuple(f"H{sector}" for sector in sectors
                              if sector % 2 == (1 if parity == "odd" else 0))
        article = "an" if parity in ("odd", "even") else "a"
        description = f"heads and {article} {parity} spinner label"
        steps, probability = probability_steps(
            component, outcomes, favorable, description)
        answer = (f"{joined(outcomes)}; {len(outcomes)} outcomes; "
                  f"{probability}")
        return f"{prefix} Event A is {description}.", steps, answer

    @staticmethod
    def _two_coins():
        first, second = random.sample(COIN_NAMES, 2)
        outcomes = ("HH", "HT", "TH", "TT")
        case = random.choice(("exactly one head", "at least one head",
                              "matching faces"))
        if case == "exactly one head":
            favorable = ("HT", "TH")
        elif case == "at least one head":
            favorable = ("HH", "HT", "TH")
        else:
            favorable = ("HH", "TT")
        prefix = (f"The {first} coin is flipped, then the {second} coin. "
                  f"Event A is {case}; outcome strings record that order.")
        steps, probability = probability_steps(
            f"{first} coin × {second} coin", outcomes, favorable, case)
        answer = f"{joined(outcomes)}; 4 outcomes; {probability}"
        return prefix, steps, answer

    @staticmethod
    def _two_spinners():
        first = tuple(sorted(random.sample(range(1, 40), random.randint(2, 5))))
        second = tuple(sorted(random.sample(range(41, 90), random.randint(2, 5))))
        pairs = tuple((a, b) for a in first for b in second)
        outcomes = tuple(f"({a}, {b})" for a, b in pairs)
        parity = random.choice((0, 1))
        favorable_pairs = tuple(pair for pair in pairs if sum(pair) % 2 == parity)
        favorable = tuple(f"({a}, {b})" for a, b in favorable_pairs)
        description = f"the pair sum is {'even' if parity == 0 else 'odd'}"
        prefix = (f"Spinner 1 sectors are {roster(first)}; spinner 2 sectors "
                  f"are {roster(second)}. Event A is that {description}. "
                  "Pairs list spinner 1 first.")
        steps, probability = probability_steps(
            "spinner 1 × spinner 2", outcomes, favorable, description)
        answer = f"{joined(outcomes)}; {len(outcomes)} outcomes; {probability}"
        return prefix, steps, answer

    @staticmethod
    def _digit_cards():
        digits = tuple(sorted(random.sample(range(1, 10), 3)))
        numbers = tuple(10 * a + b for a in digits for b in digits if a != b)
        ordered = sorted(numbers)
        threshold = random.choice(ordered[:-1])
        favorable = tuple(number for number in numbers if number > threshold)
        description = f"the two-digit number is greater than {threshold}"
        prefix = (f"Digit cards are {roster(digits)}. Draw two without "
                  f"replacement to form a two-digit number. Event A is that "
                  f"{description}.")
        steps, probability = probability_steps(
            "ordered digit cards", numbers, favorable, description)
        answer = f"{joined(numbers)}; {len(numbers)} outcomes; {probability}"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("list_and_count", "event_probability"):
            prefix, steps, answer = self._coin_spinner(variant)
        elif variant == "two_coins":
            prefix, steps, answer = self._two_coins()
        elif variant == "two_spinners":
            prefix, steps, answer = self._two_spinners()
        else:
            prefix, steps, answer = self._digit_cards()
        problem = (f"At the {random.choice(PLACES)}, {prefix} "
                   f"{random.choice(QUERIES[variant])}")
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_sample_space_list_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
