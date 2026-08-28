"""Unstated-method linear cost, pricing, and plan stories.

Variants: ``evaluate``, ``invert``, ``from_two_points``, ``break_even``,
``compare_plans``, and ``interpret_parts``. Five shared-context renderings and
all four applied modifiers are supported. Dollar inputs are integral so every
result is exact and hand-friendly. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``DEFINE_VAR``, ``MODEL_EQ``, ``INTERPRET``, ``CMP``,
``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, estimate_first, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("evaluate", "invert", "from_two_points", "break_even",
            "compare_plans", "interpret_parts")
PLACES = tuple(
    setting
    for key in ("business", "shop", "workshop", "classroom")
    for setting in CONTEXTS[key].settings
)
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} note from {place} says: {facts}",
    "Order {record} at {place} — {facts} {question}",
    "At {place}, record {record}: {facts_lc} {question}",
    "Consider the {record} report from {place}: {facts} {question}",
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(PLACES),
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def dollars(value):
    return money(Fraction(value))


class LinearModelWordGenerator(ProblemGenerator):
    """Generate exact affine-model stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "hours", "items", "posters", "minutes")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _evaluate(invert=False):
        fixed = random.randrange(10, 61, 5)
        rate = random.randrange(5, 31, 5)
        hours_worked = random.randint(2, 10)
        variable = rate * hours_worked
        total = fixed + variable
        facts = (f"A repair service charges a {dollars(fixed)} call-out fee "
                 f"plus {dollars(rate)} per hour.")
        model = f"C = {fixed} + {rate}h"
        if invert:
            facts += f" A completed repair has a bill of {dollars(total)}."
            question = "How many hours of work were billed?"
            steps = [step("DEFINE_VAR", "h", "hours billed"),
                     step("MODEL_EQ", f"{fixed} + {rate}h = {total}",
                          "bill equals fixed fee plus hourly charge"),
                     step("S", total, fixed, variable),
                     step("D", variable, rate, hours_worked),
                     step("M", rate, hours_worked, variable),
                     step("A", fixed, variable, total),
                     step("CHECK", "reconstructed bill", dollars(total))]
            answer = unit(hours_worked, "hour")
            used = [dollars(fixed), f"{dollars(rate)} per hour", dollars(total)]
            return (facts, question, steps, answer, Fraction(hours_worked),
                    f"{fixed} + {rate}h = {total}", "h", used,
                    lambda value: unit(value, "hour"))
        facts += f" A repair takes {hours_worked} hours."
        question = "What is the total bill?"
        steps = [step("DEFINE_VAR", "C", "total cost"),
                 step("MODEL_EQ", model, "fixed fee plus hourly charge"),
                 step("M", rate, hours_worked, variable),
                 step("A", fixed, variable, total),
                 step("CHECK", "fee plus hourly subtotal", dollars(total))]
        used = [dollars(fixed), f"{dollars(rate)} per hour",
                f"{hours_worked} hours"]
        return (facts, question, steps, dollars(total), Fraction(total), model,
                "C", used, dollars)

    @staticmethod
    def _from_two_points():
        fixed = random.randrange(5, 31, 5)
        rate = random.randrange(2, 13)
        first_count = random.randint(2, 8)
        second_count = first_count + random.randint(2, 8)
        first_cost = fixed + rate * first_count
        second_cost = fixed + rate * second_count
        facts = (f"A printer charges {dollars(first_cost)} for {first_count} "
                 f"posters and {dollars(second_cost)} for {second_count} "
                 "posters. The charge changes by the same amount for each "
                 "additional poster.")
        question = "What are the fixed fee and the charge per poster?"
        model = f"C = {fixed} + {rate}n"
        cost_change, count_change = second_cost - first_cost, second_count - first_count
        first_variable = rate * first_count
        steps = [step("DEFINE_VAR", "n", "number of posters"),
                 step("S", second_cost, first_cost, cost_change),
                 step("S", second_count, first_count, count_change),
                 step("D", cost_change, count_change, rate),
                 step("M", rate, first_count, first_variable),
                 step("S", first_cost, first_variable, fixed),
                 step("MODEL_EQ", model, "fixed fee and per-poster charge"),
                 step("CHECK", f"n={second_count}",
                      f"{fixed}+{rate}*{second_count}", second_cost)]
        answer = f"{dollars(fixed)} fixed; {dollars(rate)} per poster"
        used = [f"{first_count} posters cost {dollars(first_cost)}",
                f"{second_count} posters cost {dollars(second_cost)}"]
        return (facts, question, steps, answer, Fraction(fixed), model, "parts",
                used, dollars)

    @staticmethod
    def _break_even():
        sale_price = random.randrange(8, 21)
        item_cost = random.randrange(2, sale_price)
        units = random.randrange(5, 31)
        margin = sale_price - item_cost
        fixed = margin * units
        revenue = sale_price * units
        facts = (f"A market stall pays {dollars(fixed)} before opening. Each "
                 f"item then costs {dollars(item_cost)} to make and sells for "
                 f"{dollars(sale_price)}.")
        question = "How many items must be sold for sales income to equal all costs?"
        model = f"{sale_price}x = {fixed} + {item_cost}x"
        steps = [step("DEFINE_VAR", "x", "items sold"),
                 step("MODEL_EQ", model, "sales income equals all costs"),
                 step("S", sale_price, item_cost, margin),
                 step("D", fixed, margin, units),
                 step("M", sale_price, units, revenue),
                 step("M", item_cost, units, item_cost * units),
                 step("A", fixed, item_cost * units, revenue),
                 step("CHECK", "income equals cost", dollars(revenue))]
        answer = f"{units} items; {dollars(revenue)} income and cost"
        used = [f"fixed {dollars(fixed)}", f"cost {dollars(item_cost)} per item",
                f"sale {dollars(sale_price)} per item"]
        return (facts, question, steps, answer, Fraction(units), model, "x", used,
                lambda value: unit(value, "item"))

    @staticmethod
    def _compare_plans():
        rate = random.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4),
                              Fraction(1, 2), Fraction(1)))
        fixed = random.randrange(5, 31, 5)
        crossing = random.randrange(20, 241, 10)
        flat = Fraction(fixed) + rate * crossing
        after = crossing + 10
        plan_a_after = fixed + rate * after
        model = f"{fixed} + {Fraction(rate)}m = {Fraction(flat)}"
        facts = (f"Phone plan A costs {dollars(fixed)} plus {dollars(rate)} per "
                 f"minute. Plan B costs {dollars(flat)} with no added charge "
                 "for minutes.")
        question = "When do the plans cost the same, and which plan costs less beyond that?"
        difference = flat - fixed
        steps = [step("DEFINE_VAR", "m", "minutes used"),
                 step("MODEL_EQ", model, "equal monthly costs"),
                 step("S", Fraction(flat), fixed, Fraction(difference)),
                 step("D", Fraction(difference), Fraction(rate), crossing),
                 step("M", Fraction(rate), after, Fraction(rate * after)),
                 step("A", fixed, Fraction(rate * after), Fraction(plan_a_after)),
                 step("CMP", dollars(plan_a_after), dollars(flat), ">"),
                 step("CHECK", f"at {after} minutes", "plan B costs less")]
        answer = (f"plan B beyond {crossing} minutes; break-even "
                  f"{crossing} minutes")
        used = [f"A fixed {dollars(fixed)}", f"A {dollars(rate)} per minute",
                f"B {dollars(flat)}"]
        return (facts, question, steps, answer, Fraction(crossing), model, "m",
                used, lambda value: unit(value, "minute"))

    @staticmethod
    def _interpret_parts():
        fixed = random.randrange(10, 61, 5)
        rate = random.randrange(5, 31, 5)
        example_hours = random.randint(2, 8)
        example_cost = fixed + rate * example_hours
        model = f"C = {fixed} + {rate}h"
        facts = (f"A delivery company's bill is described by {model}, where C "
                 "is the cost in dollars and h is the number of hours.")
        question = (f"What do {fixed} and {rate} mean, and what is the cost for "
                    f"{example_hours} hours?")
        variable_cost = rate * example_hours
        steps = [step("INTERPRET", fixed, "fixed booking charge"),
                 step("INTERPRET", rate, "charge per hour"),
                 step("M", rate, example_hours, variable_cost),
                 step("A", fixed, variable_cost, example_cost),
                 step("CHECK", f"h={example_hours}", dollars(example_cost))]
        answer = (f"{dollars(fixed)} fixed booking charge; {dollars(rate)} per "
                  f"hour; {dollars(example_cost)} for {example_hours} hours")
        used = [model, f"C means dollars", f"h means hours", f"{example_hours} hours"]
        return (facts, question, steps, answer, Fraction(example_cost), model,
                "C", used, dollars)

    @classmethod
    def _case(cls, variant):
        if variant == "evaluate":
            return cls._evaluate()
        if variant == "invert":
            return cls._evaluate(invert=True)
        if variant == "from_two_points":
            return cls._from_two_points()
        if variant == "break_even":
            return cls._break_even()
        if variant == "compare_plans":
            return cls._compare_plans()
        return cls._interpret_parts()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        (facts, question, steps, answer, estimate_value, model, variable,
         used, renderer) = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A nearby shelf holds {extra} unused folders. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"{extra} unused folders"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], estimate_value,
                "round the charges before calculating", render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "linear relationship"))
            if variant in ("from_two_points", "interpret_parts"):
                answer = f"{model}; {answer}"
            elif variant == "compare_plans":
                crossing = re.search(r"break-even (\d+) minutes", answer).group(1)
                answer = (f"{model}; m = {crossing} minutes; plan B costs "
                          f"less beyond {crossing} minutes")
            else:
                answer = f"{model}; {variable} = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_linear_model_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
