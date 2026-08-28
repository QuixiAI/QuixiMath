"""Exact everyday money comparisons, budgets, pay, and savings stories.

Variants: ``best_buy``, ``budget_share``, ``payroll_overtime``,
``currency_supplied_rate``, ``split_by_ratio``, and ``savings_goal_weeks``.
Five shared-context renderings and all four applied modifiers are supported.
All monetary values are constructed as exact cents. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``UNIT_PRICE``,
``BUDGET``, ``OVERTIME``, ``RATE_SUPPLIED``, ``RATIO_PART``, ``MODEL_EQ``,
``CMP``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("best_buy", "budget_share", "payroll_overtime",
            "currency_supplied_rate", "split_by_ratio", "savings_goal_weeks")
PLACES = tuple(
    setting
    for key in ("shop", "business", "people", "trip")
    for setting in CONTEXTS[key].settings
)
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} note from {place} says: {facts}",
    "Account {record} at {place} — {facts} {question}",
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


class MoneyLifeGenerator(ProblemGenerator):
    """Generate exact personal-finance stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "%", "EUR", "weeks")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _best_buy():
        quantity1, quantity2 = random.sample(range(6, 25, 2), 2)
        unit1, unit2 = random.sample(range(15, 61, 5), 2)  # cents per ounce
        price1 = Fraction(quantity1 * unit1, 100)
        price2 = Fraction(quantity2 * unit2, 100)
        winner = "A" if unit1 < unit2 else "B"
        win_rate, lose_rate = sorted((Fraction(unit1, 100), Fraction(unit2, 100)))
        facts = (f"Brand A has {quantity1} oz for {dollars(price1)}. Brand B "
                 f"has {quantity2} oz for {dollars(price2)}.")
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
                 step("CHECK", f"brand {winner}", dollars(win_rate))]
        answer = (f"brand {winner}; {dollars(win_rate)} vs {dollars(lose_rate)} "
                  "per oz")
        used = [f"A {quantity1} oz for {dollars(price1)}",
                f"B {quantity2} oz for {dollars(price2)}"]
        return facts, question, steps, answer, win_rate, model, "choice", used, dollars

    @staticmethod
    def _budget_share():
        total = random.randrange(2000, 6001, 100)
        rent_pct = random.choice((25, 30, 35, 40))
        food_pct = random.choice((10, 15, 20))
        travel_pct = random.choice((5, 10, 15))
        spent_pct = rent_pct + food_pct + travel_pct
        remaining_pct = 100 - spent_pct
        rent = Fraction(total * rent_pct, 100)
        food = Fraction(total * food_pct, 100)
        travel = Fraction(total * travel_pct, 100)
        spent, remaining = rent + food + travel, Fraction(total) - rent - food - travel
        facts = (f"A monthly take-home amount is {dollars(total)}. Rent is "
                 f"{rent_pct}%, food is {food_pct}%, and travel is "
                 f"{travel_pct}% of that amount.")
        question = "How much remains, and what percent of the monthly amount is it?"
        model = f"x = {total}*(1-({rent_pct}+{food_pct}+{travel_pct})/100)"
        steps = [step("M", total, Fraction(rent_pct, 100), exact(rent)),
                 step("BUDGET", "rent", f"{rent_pct}%", dollars(rent)),
                 step("M", total, Fraction(food_pct, 100), exact(food)),
                 step("BUDGET", "food", f"{food_pct}%", dollars(food)),
                 step("M", total, Fraction(travel_pct, 100), exact(travel)),
                 step("BUDGET", "travel", f"{travel_pct}%", dollars(travel)),
                 step("A", exact(rent), exact(food), exact(rent + food)),
                 step("A", exact(rent + food), exact(travel), exact(spent)),
                 step("S", total, exact(spent), exact(remaining)),
                 step("CHECK", "remaining share", f"{remaining_pct}%")]
        answer = f"{dollars(remaining)}; {remaining_pct}% of monthly amount"
        used = [dollars(total), f"rent {rent_pct}%", f"food {food_pct}%",
                f"travel {travel_pct}%"]
        return facts, question, steps, answer, remaining, model, "x", used, dollars

    @staticmethod
    def _payroll():
        hourly = random.randrange(10, 31, 2)
        hours_worked = random.randint(41, 55)
        overtime_hours = hours_worked - 40
        overtime_rate = Fraction(hourly * 3, 2)
        regular_pay = hourly * 40
        overtime_pay = overtime_hours * overtime_rate
        total = regular_pay + overtime_pay
        facts = (f"An employee works {hours_worked} hours at {dollars(hourly)} "
                 "per hour. Hours above 40 are paid at 1.5 times the regular rate.")
        question = "What are the regular pay, overtime pay, and total pay?"
        model = f"x = 40*{hourly} + ({hours_worked}-40)*{exact(overtime_rate)}"
        steps = [step("M", 40, hourly, regular_pay),
                 step("S", hours_worked, 40, overtime_hours),
                 step("M", hourly, Fraction(3, 2), exact(overtime_rate)),
                 step("OVERTIME", overtime_hours, dollars(overtime_rate),
                      dollars(overtime_pay)),
                 step("M", overtime_hours, exact(overtime_rate), exact(overtime_pay)),
                 step("A", regular_pay, exact(overtime_pay), exact(total)),
                 step("CHECK", "regular plus overtime", dollars(total))]
        answer = (f"regular {dollars(regular_pay)}; overtime "
                  f"{dollars(overtime_pay)}; total {dollars(total)}")
        used = [f"{hours_worked} hours", f"{dollars(hourly)} per hour",
                "1.5 times above 40 hours"]
        return facts, question, steps, answer, total, model, "x", used, dollars

    @staticmethod
    def _currency():
        rate = random.choice((Fraction(3, 4), Fraction(4, 5), Fraction(9, 10),
                              Fraction(5, 4), Fraction(3, 2)))
        dollars_in = random.randrange(20, 401, 10)
        euros = dollars_in * rate
        facts = (f"A posted exchange states that 1 USD equals {exact(rate)} EUR. "
                 f"A traveller exchanges {dollars(dollars_in)}.")
        question = "How many EUR does the traveller receive?"
        model = f"x = {dollars_in}*{exact(rate)}"
        steps = [step("RATE_SUPPLIED", "1 USD", f"{exact(rate)} EUR"),
                 step("M", dollars_in, exact(rate), exact(euros)),
                 step("CHECK", "supplied exchange", f"{exact(euros)} EUR")]
        answer = f"{exact(euros)} EUR"
        used = [f"1 USD = {exact(rate)} EUR", dollars(dollars_in)]
        return (facts, question, steps, answer, euros, model, "x", used,
                lambda value: f"{exact(value)} EUR")

    @staticmethod
    def _split_ratio():
        first, second, third = (random.randint(1, 6) for _ in range(3))
        parts = first + second + third
        per_part = random.randrange(10, 101, 5)
        total = parts * per_part
        amounts = (first * per_part, second * per_part, third * per_part)
        facts = (f"Three friends, Ana, Ben, and Chi, split {dollars(total)} in the ratio "
                 f"{first}:{second}:{third}, in that order.")
        question = "How much money does each person receive?"
        model = f"x = {total}/({first}+{second}+{third})"
        steps = [step("A", first, second, first + second),
                 step("A", first + second, third, parts),
                 step("D", total, parts, per_part),
                 step("RATIO_PART", "Ana", first, dollars(amounts[0])),
                 step("M", first, per_part, amounts[0]),
                 step("RATIO_PART", "Ben", second, dollars(amounts[1])),
                 step("M", second, per_part, amounts[1]),
                 step("RATIO_PART", "Chi", third, dollars(amounts[2])),
                 step("M", third, per_part, amounts[2]),
                 step("CHECK", "shares sum", dollars(sum(amounts)))]
        answer = (f"Ana {dollars(amounts[0])}; Ben {dollars(amounts[1])}; "
                  f"Chi {dollars(amounts[2])}")
        used = [dollars(total), f"ratio {first}:{second}:{third}"]
        return facts, question, steps, answer, Fraction(amounts[0]), model, "x", used, dollars

    @staticmethod
    def _savings():
        start = random.randrange(0, 501, 25)
        weekly = random.randrange(10, 101, 5)
        weeks = random.randint(4, 30)
        goal = start + weekly * weeks
        facts = (f"A savings account starts with {dollars(start)}. Another "
                 f"{dollars(weekly)} is added at the end of each week. The "
                 f"goal is {dollars(goal)}.")
        question = "After how many weekly additions is the goal reached?"
        model = f"{start} + {weekly}w = {goal}"
        needed = goal - start
        steps = [step("S", goal, start, needed),
                 step("D", needed, weekly, weeks),
                 step("M", weekly, weeks, needed),
                 step("A", start, needed, goal),
                 step("CHECK", "savings goal", dollars(goal))]
        answer = f"{weeks} weeks; {dollars(goal)}"
        used = [f"start {dollars(start)}", f"weekly {dollars(weekly)}",
                f"goal {dollars(goal)}"]
        return (facts, question, steps, answer, Fraction(weeks), model, "w", used,
                lambda value: unit(value, "week"))

    @classmethod
    def _case(cls, variant):
        if variant == "best_buy":
            return cls._best_buy()
        if variant == "budget_share":
            return cls._budget_share()
        if variant == "payroll_overtime":
            return cls._payroll()
        if variant == "currency_supplied_rate":
            return cls._currency()
        if variant == "split_by_ratio":
            return cls._split_ratio()
        return cls._savings()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        (facts, question, steps, answer, value, model, variable, used,
         renderer) = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A notice nearby lists {extra} parking spaces. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"{extra} parking spaces"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "round the monetary amounts before calculating",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "money relationship"))
            answer = f"{model}; {variable} = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_money_life_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
