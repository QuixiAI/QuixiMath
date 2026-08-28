"""Solvable controls and stories with one indispensable quantity omitted.

Variants: ``identify_missing``, ``solvable_control``,
``which_of_two_missing``, and ``extra_and_missing``. Five story families
(purchase, work, motion, mixture, linear billing), five shared-context
renderings, and all four applied modifiers are supported. Default sampling is
half solvable controls. Missing answers always retain the canonical
``insufficient information; need <slot phrase>`` form, including under
``with_model``. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``MISSING``, ``A``, ``S``, ``M``, ``D``,
``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, WORK_RATE_PAIRS, estimate_first,
                            exact, missing_answer, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("identify_missing", "solvable_control", "which_of_two_missing",
            "extra_and_missing")
FAMILIES = ("purchase", "work", "motion", "mixture", "linear")
FRAMES = (
    "At {place}, {name} records this: {facts} {question}",
    "{question} A note by {name} at {place} says: {facts}",
    "For {name} at {place}, {facts_lc} {question}",
    "At {place}, {facts_lc} {name} asks: {question}",
    "Consider {name}'s report from {place}: {facts} {question}",
)
PLACE_KEYS = {
    "purchase": ("shop", "classroom"),
    "work": ("business", "workshop"),
    "motion": ("trip", "sports"),
    "mixture": ("lab", "recipe"),
    "linear": ("business", "shop"),
}
TIMES = (Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2),
         Fraction(3), Fraction(7, 2), Fraction(4))


def _render(facts, question, family):
    places = tuple(
        setting
        for key in PLACE_KEYS[family]
        for setting in CONTEXTS[key].settings
    )
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(places), name=random.choice(NAMES))


def percent(value):
    return f"{exact(Fraction(value))}%"


class MissingInformationGenerator(ProblemGenerator):
    """Generate missing-data judgments paired with numeric controls."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "hours", "%")

    def __init__(self, variant=None, modifier=None, family=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        if family is not None and family not in FAMILIES:
            raise ValueError(f"family must be one of {FAMILIES} or None")
        self.variant = variant
        self.modifier = modifier
        self.family = family

    @staticmethod
    def _purchase(control):
        count = random.randint(2, 10)
        price = Fraction(random.randrange(4, 33), 4)
        cost = count * price
        paid = Fraction(((int(cost) // 5) + 2) * 5)
        while paid <= cost:
            paid += 5
        change = paid - cost
        facts = f"A shopper named Mia buys {count} notebooks"
        if control:
            facts += f" at {money(price)} each"
        facts += f" and pays with {money(paid)}."
        question = "How much change does Mia receive?"
        slot = "the price of a notebook"
        alternative = "the notebook color"
        price_term = exact(price) if control else "p"
        model = f"x = {exact(paid)} - {count}*{price_term}"
        steps = [step("M", count, exact(price), exact(cost)),
                 step("S", exact(paid), exact(cost), exact(change)),
                 step("CHECK", "purchase plus change", money(paid))]
        used = [f"{count} notebooks", f"payment {money(paid)}"]
        if control:
            used.append(f"price {money(price)} each")
        return facts, question, slot, alternative, model, steps, money(change), change, used, money

    @staticmethod
    def _work(control):
        first, second = random.choice(WORK_RATE_PAIRS)
        together = 1 / (Fraction(1, first) + Fraction(1, second))
        facts = f"Worker A can pack an order in {first} hours."
        if control:
            facts += f" Worker B can pack the same order in {second} hours."
        else:
            facts += " Worker B can also pack the same order."
        question = "How many hours do they need when working together?"
        slot = "the time worker B needs alone"
        alternative = "worker B's name"
        model = (f"1/{first} + 1/{second} = 1/t" if control
                 else f"1/{first} + 1/b = 1/t")
        rate_sum = Fraction(1, first) + Fraction(1, second)
        steps = [step("A", f"1/{first}", f"1/{second}", exact(rate_sum)),
                 step("D", 1, exact(rate_sum), exact(together)),
                 step("CHECK", "one whole order", exact(together * rate_sum))]
        answer = unit(together, "hour")
        used = [f"worker A {first} hours"]
        if control:
            used.append(f"worker B {second} hours")
        renderer = lambda value: unit(value, "hour")
        return (facts, question, slot, alternative, model, steps, answer,
                together, used, renderer)

    @staticmethod
    def _motion(control):
        first = random.randrange(30, 81, 5)
        second = random.randrange(30, 81, 5)
        meet_time = random.choice(TIMES)
        gap = (first + second) * meet_time
        facts = (f"Two trains are {exact(gap)} km apart and move toward each "
                 f"other. Train A travels at {first} km/h.")
        if control:
            facts += f" Train B travels at {second} km/h."
        else:
            facts += " Train B's speed is not shown."
        question = "After how many hours do the trains meet?"
        slot = "the speed of train B"
        alternative = "train B's color"
        model = (f"{first}t + {second}t = {exact(gap)}" if control
                 else f"{first}t + bt = {exact(gap)}")
        steps = [step("A", first, second, first + second),
                 step("D", exact(gap), first + second, exact(meet_time)),
                 step("CHECK", "closing distance", exact(gap))]
        answer = unit(meet_time, "hour")
        used = [f"gap {exact(gap)} km", f"train A {first} km/h"]
        if control:
            used.append(f"train B {second} km/h")
        renderer = lambda value: unit(value, "hour")
        return (facts, question, slot, alternative, model, steps, answer,
                meet_time, used, renderer)

    @staticmethod
    def _mixture(control):
        while True:
            first_pct, second_pct = sorted(random.sample((10, 20, 25, 30, 40, 50, 60, 75), 2))
            first_volume, second_volume = random.randint(2, 15), random.randint(2, 15)
            result = Fraction(first_volume * first_pct + second_volume * second_pct,
                              first_volume + second_volume)
            if result.denominator in (1, 2, 4, 5, 10):
                break
        facts = (f"A tank combines {first_volume} L of a {first_pct}% salt "
                 f"solution with {second_volume} L of a second salt solution")
        if control:
            facts += f" whose concentration is {second_pct}%"
        facts += "."
        question = "What percent salt is in the combined solution?"
        slot = "the concentration of the second solution"
        alternative = "the second container's label"
        second_term = str(second_pct) if control else "p"
        model = (f"x = ({first_volume}*{first_pct} + "
                 f"{second_volume}*{second_term})/"
                 f"({first_volume}+{second_volume})")
        first_amount = Fraction(first_volume * first_pct, 100)
        second_amount = Fraction(second_volume * second_pct, 100)
        total_amount = first_amount + second_amount
        total_volume = first_volume + second_volume
        steps = [step("M", first_volume, Fraction(first_pct, 100), exact(first_amount)),
                 step("M", second_volume, Fraction(second_pct, 100), exact(second_amount)),
                 step("A", exact(first_amount), exact(second_amount), exact(total_amount)),
                 step("A", first_volume, second_volume, total_volume),
                 step("D", exact(total_amount), total_volume,
                      exact(total_amount / total_volume)),
                 step("CHECK", "combined concentration", percent(result))]
        used = [f"{first_volume} L at {first_pct}%", f"{second_volume} L"]
        if control:
            used.append(f"second concentration {second_pct}%")
        return (facts, question, slot, alternative, model, steps,
                percent(result), result, used, percent)

    @staticmethod
    def _linear(control):
        fixed = random.randrange(10, 61, 5)
        rate = random.randrange(5, 31, 5)
        hours_worked = random.randint(2, 10)
        bill = fixed + rate * hours_worked
        facts = f"A repair service charges a {money(fixed)} fixed fee"
        if control:
            facts += f" plus {money(rate)} per hour"
        else:
            facts += " plus an hourly charge"
        facts += f". A completed repair has a bill of {money(bill)}."
        question = "How many hours of work were billed?"
        slot = "the hourly charge"
        alternative = "the invoice date"
        model = (f"{fixed} + {rate}h = {bill}" if control
                 else f"{fixed} + rh = {bill}")
        variable = bill - fixed
        steps = [step("S", bill, fixed, variable),
                 step("D", variable, rate, hours_worked),
                 step("CHECK", "reconstructed bill", money(bill))]
        used = [f"fixed fee {money(fixed)}", f"bill {money(bill)}"]
        if control:
            used.append(f"hourly charge {money(rate)}")
        renderer = lambda value: unit(value, "hour")
        return (facts, question, slot, alternative, model, steps,
                unit(hours_worked, "hour"), Fraction(hours_worked), used,
                renderer)

    @classmethod
    def _case(cls, family, control):
        return getattr(cls, f"_{family}")(control)

    def generate(self):
        if self.variant is None:
            variant = random.choices(
                self.VARIANTS, weights=(1, 3, 1, 1), k=1)[0]
        else:
            variant = self.variant
        modifier = self.modifier or random.choice(self.MODIFIERS)
        family = self.family or random.choice(FAMILIES)
        control = variant == "solvable_control"
        (facts, question, slot, alternative, model, solve_steps, numeric_answer,
         value, used, renderer) = self._case(family, control)
        if variant == "which_of_two_missing":
            question += f" Choose the needed fact from {slot} or {alternative}."
        base_extra = None
        if variant == "extra_and_missing":
            base_extra = random.randint(20, 40)
            facts += f" A nearby display holds {base_extra} brochures."
        problem = _render(facts, question, family)

        extra = None
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(41, 100)
                                   if number not in occupied])
            problem = f"A sign nearby lists {extra} parking spaces. {problem}"
        ignored = []
        if base_extra is not None:
            ignored.append(f"{base_extra} brochures")
        if extra is not None:
            ignored.append(f"{extra} parking spaces")

        if control:
            steps = list(solve_steps)
            answer = numeric_answer
            if ignored:
                steps.insert(0, select_relevant_step(used, ignored))
        else:
            answer = missing_answer(slot)
            steps = [select_relevant_step(used, ignored, slot),
                     step("MISSING", slot, model)]

        if modifier == "estimate_first":
            if control:
                steps = estimate_first(
                    steps + [step("Z", answer)], value,
                    "check whether the known values determine a result",
                    render=renderer)[:-1]
            else:
                steps.insert(0, step("ESTIMATE", "inspect required quantities",
                                     "insufficient data"))
                steps.append(step("ESTIMATE_CHECK", "insufficient data",
                                  answer, "missing slot confirmed"))
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "required relationship"))
            if control:
                variable = {"work": "t", "motion": "t", "linear": "h"}.get(
                    family, "x")
                answer = f"{model}; {variable} = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": (f"applied_missing_information_{variant}_"
                              f"{modifier}"),
                "problem": problem, "steps": steps,
                "final_answer": answer}
