"""Exact per-item, per-distance, per-task, and best-buy stories.

``UnitRateGenerator`` variants are ``cost_per_item``, ``time_per_distance``,
``time_per_task``, and ``best_buy``. Five shared-context renderings and all
four applied modifiers are supported; the historical ``distractor=True``
constructor remains valid. ``UnitRateFromTableGenerator`` remains the table
counterpart and now uses pipe-safe prose without naming a method. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``UNIT_RATE_SETUP``, ``UNIT_RATE_DIV``, ``UNIT_PRICE``, ``CMP``, ``D``,
``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("cost_per_item", "time_per_distance", "time_per_task", "best_buy")
FRAMES = (
    "At {place}, {name} records this: {facts} {question}",
    "{question} A note by {name} at {place} says: {facts}",
    "For {name} at {place}, {facts_lc} {question}",
    "At {place}, {facts_lc} {name} asks: {question}",
    "Consider {name}'s report from {place}: {facts} {question}",
)
ITEMS = (("notebooks", "notebook"), ("oranges", "orange"),
         ("books", "book"), ("pencil packs", "pencil pack"),
         ("shirts", "shirt"), ("tickets", "ticket"))
PLACE_KEYS = {
    "cost_per_item": ("shop", "business"),
    "time_per_distance": ("trip", "sports"),
    "time_per_task": ("classroom", "workshop", "business"),
    "best_buy": ("shop", "business"),
}


def _render(facts, question, variant):
    places = tuple(
        setting
        for key in PLACE_KEYS[variant]
        for setting in CONTEXTS[key].settings
    )
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(places), name=random.choice(NAMES))


def dollars(value):
    return money(Fraction(value))


class UnitRateGenerator(ProblemGenerator):
    """Generate exact one-unit comparisons with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "hours", "minutes")

    def __init__(self, distractor=False, modifier=None, variant=None):
        if modifier is None:
            modifier = "distractor" if distractor else "plain"
        elif distractor and modifier != "distractor":
            raise ValueError("distractor=True requires modifier='distractor'")
        if modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS}")
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.modifier = modifier
        self.variant = variant
        self.distractor = modifier == "distractor"

    @staticmethod
    def _cost_per_item():
        plural, singular = random.choice(ITEMS)
        quantity = random.randint(2, 16)
        unit_price = Fraction(random.randrange(25, 1001, 25), 100)
        total = quantity * unit_price
        facts = f"{quantity} {plural} cost {dollars(total)}."
        question = f"How much does one {singular} cost?"
        model = f"x = {exact(total)}/{quantity}"
        steps = [step("UNIT_RATE_SETUP", quantity, plural, dollars(total)),
                 step("D", exact(total), quantity, exact(unit_price)),
                 step("UNIT_RATE_DIV", dollars(total), quantity,
                      f"{dollars(unit_price)} per {singular}"),
                 step("CHECK", "one-item cost", dollars(unit_price))]
        answer = f"{dollars(unit_price)} per {singular}"
        used = [f"{quantity} {plural}", f"total {dollars(total)}"]
        renderer = lambda value: f"{dollars(value)} per {singular}"
        return facts, question, steps, answer, unit_price, model, used, renderer

    @staticmethod
    def _time_per_distance():
        quantity = random.randint(2, 16)
        per_mile = random.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2),
                                  Fraction(2), Fraction(5, 2), Fraction(3)))
        total = quantity * per_mile
        total_text = f"{exact(total)} {('hour' if total == 1 else 'hours')}"
        facts = (f"Traveling {quantity} miles takes {total_text} at a "
                 "steady pace.")
        question = "How much time does one mile take?"
        model = f"x = {exact(total)}/{quantity}"
        answer = f"{exact(per_mile)} {('hour' if per_mile == 1 else 'hours')} per mile"
        steps = [step("UNIT_RATE_SETUP", quantity, "miles", total_text),
                 step("D", exact(total), quantity, exact(per_mile)),
                 step("UNIT_RATE_DIV", total_text, quantity, answer),
                 step("CHECK", "time per mile", answer)]
        used = [f"{quantity} miles", total_text]
        renderer = lambda value: (f"{exact(value)} "
                                  f"{('hour' if Fraction(value) == 1 else 'hours')} per mile")
        return facts, question, steps, answer, per_mile, model, used, renderer

    @staticmethod
    def _time_per_task():
        plural, singular = random.choice((("pages", "page"), ("laps", "lap"),
                                          ("packages", "package")))
        quantity = random.randint(2, 16)
        per_task = random.choice((2, 3, 4, 5, 6, 8, 10, 12, 15))
        total = quantity * per_task
        facts = f"Completing {quantity} {plural} takes {total} minutes."
        question = f"How much time does one {singular} take?"
        model = f"x = {total}/{quantity}"
        steps = [step("UNIT_RATE_SETUP", quantity, plural, f"{total} minutes"),
                 step("D", total, quantity, per_task),
                 step("UNIT_RATE_DIV", f"{total} minutes", quantity,
                      f"{per_task} minutes per {singular}"),
                 step("CHECK", f"time per {singular}", f"{per_task} minutes")]
        answer = f"{per_task} minutes per {singular}"
        used = [f"{quantity} {plural}", f"{total} minutes"]
        renderer = lambda value: f"{exact(value)} minutes per {singular}"
        return (facts, question, steps, answer, Fraction(per_task), model, used,
                renderer)

    @staticmethod
    def _best_buy():
        quantity1, quantity2 = random.sample(range(6, 25, 2), 2)
        unit1, unit2 = random.sample(range(15, 61, 5), 2)
        price1, price2 = Fraction(quantity1 * unit1, 100), Fraction(quantity2 * unit2, 100)
        winner = "A" if unit1 < unit2 else "B"
        low, high = sorted((Fraction(unit1, 100), Fraction(unit2, 100)))
        facts = (f"Brand A offers {quantity1} oz for {dollars(price1)}. Brand B "
                 f"offers {quantity2} oz for {dollars(price2)}.")
        question = "Which brand costs less for each ounce?"
        model = (f"u_A = {exact(price1)}/{quantity1}; "
                 f"u_B = {exact(price2)}/{quantity2}")
        steps = [step("D", exact(price1), quantity1, exact(Fraction(unit1, 100))),
                 step("UNIT_PRICE", "A", f"{exact(price1)}/{quantity1}",
                      dollars(Fraction(unit1, 100))),
                 step("D", exact(price2), quantity2, exact(Fraction(unit2, 100))),
                 step("UNIT_PRICE", "B", f"{exact(price2)}/{quantity2}",
                      dollars(Fraction(unit2, 100))),
                 step("CMP", exact(Fraction(unit1, 100)),
                      exact(Fraction(unit2, 100)), "<" if unit1 < unit2 else ">"),
                 step("CHECK", f"brand {winner}", dollars(low))]
        answer = f"brand {winner}; {dollars(low)} vs {dollars(high)} per oz"
        used = [f"A {quantity1} oz for {dollars(price1)}",
                f"B {quantity2} oz for {dollars(price2)}"]
        return facts, question, steps, answer, low, model, used, dollars

    @classmethod
    def _case(cls, variant):
        if variant == "cost_per_item":
            return cls._cost_per_item()
        if variant == "time_per_distance":
            return cls._time_per_distance()
        if variant == "time_per_task":
            return cls._time_per_task()
        return cls._best_buy()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question, variant)
        if self.modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A sign nearby shows aisle {extra}. {problem}"
            steps.insert(0, select_relevant_step(used, f"aisle {extra}"))
        elif self.modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "round the total before dividing by the count",
                render=renderer)[:-1]
        elif self.modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "per-one comparison"))
            variable = "choice" if variant == "best_buy" else "x"
            answer = f"{model}; {variable} = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_unit_rate_{variant}_{self.modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}


class UnitRateFromTableGenerator(ProblemGenerator):
    """Generate a constant per-one comparison from a supplied text table."""

    def generate(self):
        rate = random.choice((2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25))
        count = random.randint(3, 4)
        x_values = sorted(random.sample(range(1, 11), count))
        y_values = [x * rate for x in x_values]
        contexts = (
            ("hours worked", "dollars earned", "hour"),
            ("gallons of gas", "miles traveled", "gallon"),
            ("pounds of fruit", "total cost in dollars", "pound"),
            ("hours", "pages read", "hour"),
            ("days", "miles run", "day"),
        )
        x_label, y_label, one_unit = random.choice(contexts)
        rows = "; ".join(f"{x} to {y}" for x, y in zip(x_values, y_values))
        problem = (f"A data note lists {x_label} to {y_label} as follows: "
                   f"{rows}. How many {y_label} correspond to one {one_unit}?")
        x_pick, y_pick = x_values[0], y_values[0]
        steps = [step("UNIT_RATE_TABLE", ",".join(map(str, x_values)),
                      ",".join(map(str, y_values))),
                 step("UNIT_RATE_PICK", x_pick, y_pick),
                 step("D", y_pick, x_pick, rate),
                 step("UNIT_RATE_DIV", y_pick, x_pick, rate),
                 step("Z", f"{rate} {y_label} per {one_unit}")]
        return {"problem_id": jid(), "operation": "unit_rate_table",
                "problem": problem, "steps": steps,
                "final_answer": f"{rate} {y_label} per {one_unit}"}
