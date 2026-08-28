"""Check independence by comparing intersections with probability products.

Variants: ``die_events``, ``two_dice_events``, ``small_deck``,
``table_events``, ``given_probabilities``, and
``three_events_pairwise_vs_mutual``. Op-codes: ``EVENT``, ``TABLE_CELL``,
``PROB_SETUP``, ``F``, ``INDEP_FORMULA``, ``INDEP_CHECK``, ``M``, ``CHECK``,
and ``Z``. Random spaces, predicates, marks, tables, and five phrasings give
an unbounded problem space.
"""
import itertools
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
DEVICE_NAMES = ("alpha", "beta", "cobalt", "delta", "ember", "forest",
                "gamma", "harbor", "indigo", "jade", "kelvin", "lunar",
                "marble", "nova", "onyx", "pearl", "quartz", "river",
                "solar", "topaz", "umber", "violet", "willow", "xenon")
OUTPUT_LABELS = ("amber", "blue", "coral", "gold", "green", "indigo",
                 "ivory", "lime", "orange", "pearl", "purple", "red",
                 "silver", "teal", "white", "yellow")
QUERIES = {
    "die_events": (
        "Determine whether A and B are independent.",
        "Compare P(A ∩ B) with P(A)·P(B) and give the verdict.",
        "Enumerate the die outcomes and test the independence equation.",
        "Are the two die events independent? Include the exact numerical check.",
        "Use the intersection and product probabilities to classify the events.",
    ),
    "two_dice_events": (
        "Determine whether the two ordered-pair events are independent.",
        "Enumerate both dice and compare the intersection with the product.",
        "Test A and B for independence using all ordered outcomes.",
        "Are these two-dice events independent? Give the exact equality or inequality.",
        "Compute P(A), P(B), and P(A ∩ B) before giving the verdict.",
    ),
    "small_deck": (
        "Determine whether the two card-mark events are independent.",
        "Use the marked-card rosters to test the probability product rule.",
        "Are A and B independent on this uniformly drawn mini-deck?",
        "Compare the shared marked cards with the product of both event chances.",
        "Give an exact independence verdict for the two deck events.",
    ),
    "table_events": (
        "Determine whether the target row and target column events are independent.",
        "Use the table cell, margins, and grand total to test independence.",
        "Compare the joint table probability with the product of its marginals.",
        "Are the displayed row and column events independent? Show the exact check.",
        "Compute the intersection and marginal product before classifying the events.",
    ),
    "given_probabilities": (
        "Determine whether A and B are independent from the stated probabilities.",
        "Compare the supplied intersection with P(A)·P(B).",
        "Are the events independent? Give the exact product-law check.",
        "Use the numerical definition of independence to classify A and B.",
        "Report the verdict together with the intersection and product values.",
    ),
    "three_events_pairwise_vs_mutual": (
        "Decide whether A, B, and C are pairwise independent and mutually independent.",
        "Check all event pairs, then compare the triple intersection with the triple product.",
        "Classify the three events using pairwise and mutual independence tests.",
        "Show why every pair is independent but the three events together are not.",
        "Give the composite independence verdict and its exact triple-probability check.",
    ),
}


def _fraction_steps(numerator, denominator):
    value = Fraction(numerator, denominator)
    raw = f"{numerator}/{denominator}"
    steps = [step("PROB_SETUP", numerator, denominator)]
    if raw != prob_txt(value):
        steps.append(step("F", raw, prob_txt(value)))
    return steps, value


def _verdict_answer(intersection, product):
    if intersection == product:
        return (f"independent; P(A ∩ B) = {prob_txt(intersection)} = "
                "P(A)·P(B)")
    return (f"dependent; P(A ∩ B) = {prob_txt(intersection)} ≠ "
            f"P(A)·P(B) = {prob_txt(product)}")


def _uniform_steps(labels, event_a, event_b):
    total = len(labels)
    inter = event_a & event_b
    steps = [step("EVENT", "A", roster(label for label in labels
                                         if label in event_a), len(event_a)),
             step("EVENT", "B", roster(label for label in labels
                                         if label in event_b), len(event_b)),
             step("EVENT", "A ∩ B", roster(label for label in labels
                                             if label in inter), len(inter))]
    a_steps, p_a = _fraction_steps(len(event_a), total)
    b_steps, p_b = _fraction_steps(len(event_b), total)
    i_steps, p_inter = _fraction_steps(len(inter), total)
    steps.extend(a_steps + b_steps + i_steps)
    product = p_a * p_b
    steps.extend([step("INDEP_FORMULA",
                       "independent iff P(A ∩ B) = P(A)·P(B)"),
                  step("M", prob_txt(p_a), prob_txt(p_b), prob_txt(product)),
                  step("INDEP_CHECK", f"P(A ∩ B) = {prob_txt(p_inter)}",
                       f"product = {prob_txt(product)}",
                       "yes" if p_inter == product else "no")])
    return steps, _verdict_answer(p_inter, product)


def _die_event(sides):
    kind = random.choice(("even", "odd", "prime", "at_most", "at_least",
                          "multiple"))
    values = set(range(1, sides + 1))
    if kind == "even":
        return "the roll is even", {value for value in values if value % 2 == 0}
    if kind == "odd":
        return "the roll is odd", {value for value in values if value % 2 == 1}
    if kind == "prime":
        event = {value for value in values
                 if value >= 2 and all(value % d for d in range(2, int(value ** 0.5) + 1))}
        return "the roll is prime", event
    if kind == "at_most":
        cutoff = random.randint(2, sides - 1)
        return f"the roll is at most {cutoff}", {v for v in values if v <= cutoff}
    if kind == "at_least":
        cutoff = random.randint(2, sides - 1)
        return f"the roll is at least {cutoff}", {v for v in values if v >= cutoff}
    divisor = random.randint(2, min(12, sides))
    return f"the roll is a multiple of {divisor}", {v for v in values if v % divisor == 0}


def _two_dice_event(first_sides, second_sides):
    outcomes = tuple(itertools.product(range(1, first_sides + 1),
                                       range(1, second_sides + 1)))
    kind = random.choice(("sum_equals", "sum_at_least", "doubles",
                          "first_greater", "product_even", "max_at_most"))
    if kind == "sum_equals":
        target = random.randint(2, first_sides + second_sides)
        return f"the sum equals {target}", {o for o in outcomes if sum(o) == target}
    if kind == "sum_at_least":
        target = random.randint(3, first_sides + second_sides - 1)
        return f"the sum is at least {target}", {o for o in outcomes if sum(o) >= target}
    if kind == "doubles":
        return "the dice show doubles", {o for o in outcomes if o[0] == o[1]}
    if kind == "first_greater":
        return "the first die exceeds the second", {o for o in outcomes if o[0] > o[1]}
    if kind == "product_even":
        return "the product is even", {o for o in outcomes if o[0] * o[1] % 2 == 0}
    cutoff = random.randint(2, min(first_sides, second_sides))
    return f"the maximum is at most {cutoff}", {o for o in outcomes if max(o) <= cutoff}


class IndependenceCheckGenerator(ProblemGenerator):
    """Generate exact finite-space tests of event independence."""

    VARIANTS = ("die_events", "two_dice_events", "small_deck",
                "table_events", "given_probabilities",
                "three_events_pairwise_vs_mutual")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _die():
        sides = random.randint(6, 80)
        color = random.choice(OUTPUT_LABELS)
        labels = tuple(str(value) for value in range(1, sides + 1))
        while True:
            desc_a, raw_a = _die_event(sides)
            desc_b, raw_b = _die_event(sides)
            if desc_a != desc_b and raw_a and raw_b:
                break
        event_a, event_b = {str(v) for v in raw_a}, {str(v) for v in raw_b}
        prefix = (f"A fair {color} {sides}-sided die with faces 1 through {sides} is "
                  f"rolled. A: {desc_a}. B: {desc_b}.")
        steps, answer = _uniform_steps(labels, event_a, event_b)
        return prefix, steps, answer

    @staticmethod
    def _two_dice():
        first_sides, second_sides = random.randint(4, 12), random.randint(4, 12)
        first_color, second_color = random.sample(OUTPUT_LABELS, 2)
        outcomes = tuple(itertools.product(range(1, first_sides + 1),
                                           range(1, second_sides + 1)))
        while True:
            desc_a, raw_a = _two_dice_event(first_sides, second_sides)
            desc_b, raw_b = _two_dice_event(first_sides, second_sides)
            if desc_a != desc_b and raw_a and raw_b:
                break
        labels = tuple(f"({a}, {b})" for a, b in outcomes)
        event_a = {f"({a}, {b})" for a, b in raw_a}
        event_b = {f"({a}, {b})" for a, b in raw_b}
        prefix = (f"A fair {first_color} {first_sides}-sided die and a fair "
                  f"{second_color} {second_sides}-sided die are rolled in that "
                  f"order. A: {desc_a}. B: {desc_b}.")
        steps, answer = _uniform_steps(labels, event_a, event_b)
        return prefix, steps, answer

    @staticmethod
    def _deck():
        suits = tuple(sorted(random.sample("ABCDEFGHJKLMNPQRSTUVWXYZ",
                                           random.randint(2, 4))))
        ranks = random.randint(3, 8)
        cards = tuple(f"{suit}{rank}" for suit in suits for rank in range(1, ranks + 1))
        event_a = set(random.sample(cards, random.randint(1, len(cards) - 1)))
        event_b = set(random.sample(cards, random.randint(1, len(cards) - 1)))
        prefix = (f"A mini-deck has cards {roster(cards)}. Cards marked for A: "
                  f"{roster(card for card in cards if card in event_a)}. Cards "
                  f"marked for B: {roster(card for card in cards if card in event_b)}. "
                  "One card is drawn uniformly.")
        steps, answer = _uniform_steps(cards, event_a, event_b)
        return prefix, steps, answer

    @staticmethod
    def _table():
        counts = [random.randint(1, 80) for _ in range(4)]
        total = sum(counts)
        labels = tuple(f"R{r}C{c}#{index}"
                       for r in (1, 2) for c in (1, 2)
                       for index in range(1, counts[(r - 1) * 2 + c - 1] + 1))
        event_a = {label for label in labels if label.startswith("R1")}
        event_b = {label for label in labels if "C1#" in label}
        prefix = (f"A 2 by 2 table has counts R1C1={counts[0]}; R1C2={counts[1]}; "
                  f"R2C1={counts[2]}; R2C2={counts[3]}; total={total}. "
                  "Event A is row R1 and event B is column C1.")
        steps = [step("TABLE_CELL", cell, count)
                 for cell, count in zip(("R1C1", "R1C2", "R2C1", "R2C2"), counts)]
        common, answer = _uniform_steps(labels, event_a, event_b)
        return prefix, steps + common, answer

    @staticmethod
    def _given():
        independent = random.choice((True, False))
        if independent:
            denominator_a, denominator_b = (random.randint(4, 40)
                                              for _ in range(2))
            p_a = Fraction(random.randint(1, denominator_a - 1), denominator_a)
            p_b = Fraction(random.randint(1, denominator_b - 1), denominator_b)
            p_inter = p_a * p_b
        else:
            while True:
                total = random.randint(20, 500)
                cuts = sorted(random.sample(range(1, total), 3))
                only_a, inter, only_b = cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1]
                p_a, p_b, p_inter = (Fraction(only_a + inter, total),
                                     Fraction(only_b + inter, total),
                                     Fraction(inter, total))
                if p_inter != p_a * p_b:
                    break
        product = p_a * p_b
        prefix = (f"Events A and B have P(A) = {prob_txt(p_a)}, P(B) = "
                  f"{prob_txt(p_b)}, and P(A ∩ B) = {prob_txt(p_inter)}.")
        steps = [step("INDEP_FORMULA", "independent iff P(A ∩ B) = P(A)·P(B)"),
                 step("M", prob_txt(p_a), prob_txt(p_b), prob_txt(product)),
                 step("INDEP_CHECK", f"P(A ∩ B) = {prob_txt(p_inter)}",
                      f"product = {prob_txt(product)}",
                      "yes" if p_inter == product else "no")]
        return prefix, steps, _verdict_answer(p_inter, product)

    @staticmethod
    def _three_events():
        first, second = random.sample(DEVICE_NAMES, 2)
        low, high = random.sample(OUTPUT_LABELS, 2)
        outcomes = ((low, low), (low, high), (high, low), (high, high))
        labels = tuple(f"{a}-{b}" for a, b in outcomes)
        event_a = {label for label, outcome in zip(labels, outcomes) if outcome[0] == low}
        event_b = {label for label, outcome in zip(labels, outcomes) if outcome[1] == low}
        event_c = {label for label, outcome in zip(labels, outcomes) if outcome[0] == outcome[1]}
        prefix = (f"Independent fair devices {first} and {second} each output one "
                  f"of {roster((low, high))}. A: {first} outputs {low}. B: "
                  f"{second} outputs {low}. C: the two outputs match.")
        steps = [step("EVENT", "A", roster(label for label in labels if label in event_a), 2),
                 step("EVENT", "B", roster(label for label in labels if label in event_b), 2),
                 step("EVENT", "C", roster(label for label in labels if label in event_c), 2),
                 step("INDEP_FORMULA", "pair independent iff intersection equals product")]
        for left_name, left, right_name, right in (
                ("A", event_a, "B", event_b),
                ("A", event_a, "C", event_c),
                ("B", event_b, "C", event_c)):
            inter = Fraction(len(left & right), 4)
            product = Fraction(len(left), 4) * Fraction(len(right), 4)
            steps.extend([step("M", "1/2", "1/2", prob_txt(product)),
                          step("INDEP_CHECK", f"P({left_name} ∩ {right_name}) = {prob_txt(inter)}",
                               f"product = {prob_txt(product)}", "yes")])
        triple = Fraction(len(event_a & event_b & event_c), 4)
        steps.extend([step("M", "1/2", "1/2", "1/4"),
                      step("M", "1/4", "1/2", "1/8"),
                      step("CHECK", "mutual independence",
                           f"P(A ∩ B ∩ C) = {prob_txt(triple)}", "product = 1/8")])
        answer = ("pairwise independent; not mutually independent; "
                  f"P(A ∩ B ∩ C) = {prob_txt(triple)} ≠ 1/8")
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "die_events":
            prefix, steps, answer = self._die()
        elif variant == "two_dice_events":
            prefix, steps, answer = self._two_dice()
        elif variant == "small_deck":
            prefix, steps, answer = self._deck()
        elif variant == "table_events":
            prefix, steps, answer = self._table()
        elif variant == "given_probabilities":
            prefix, steps, answer = self._given()
        else:
            prefix, steps, answer = self._three_events()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_independence_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
