"""Problem-text-only oracles for :class:`MoneyLifeGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.money_life_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MoneyLifeGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", ""))


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def clean(problem):
    return re.sub(r"^A notice nearby lists \d+ parking spaces\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"Brand A has (\d+) oz for (\$\d+\.\d{2})\. Brand B has (\d+) oz "
        r"for (\$\d+\.\d{2})", text, re.I)
    if match:
        quantity1, price1, quantity2, price2 = match.groups()
        quantity1, quantity2 = int(quantity1), int(quantity2)
        price1, price2 = number(price1), number(price2)
        unit1, unit2 = price1 / quantity1, price2 / quantity2
        winner = "A" if unit1 < unit2 else "B"
        low, high = sorted((unit1, unit2))
        model = (f"u_A = {exact_text(price1)}/{quantity1}; "
                 f"u_B = {exact_text(price2)}/{quantity2}")
        answer = f"brand {winner}; {money_text(low)} vs {money_text(high)} per oz"
        return "best_buy", answer, model, winner

    match = re.search(
        r"take-home amount is (\$\d+\.\d{2})\. Rent is (\d+)%, food is "
        r"(\d+)%, and travel is (\d+)%", text, re.I)
    if match:
        total = number(match.group(1))
        rent, food, travel = map(int, match.groups()[1:])
        remaining_pct = 100 - rent - food - travel
        remaining = total * remaining_pct / 100
        model = f"x = {total}*(1-({rent}+{food}+{travel})/100)"
        answer = f"{money_text(remaining)}; {remaining_pct}% of monthly amount"
        return "budget_share", answer, model, None

    match = re.search(
        r"employee works (\d+) hours at (\$\d+\.\d{2}) per hour\. Hours "
        r"above 40 are paid at 1\.5 times", text, re.I)
    if match:
        elapsed, hourly = int(match.group(1)), number(match.group(2))
        regular = 40 * hourly
        overtime = (elapsed - 40) * hourly * Fraction(3, 2)
        total = regular + overtime
        model = f"x = 40*{hourly} + ({elapsed}-40)*{hourly * Fraction(3, 2)}"
        answer = (f"regular {money_text(regular)}; overtime {money_text(overtime)}; "
                  f"total {money_text(total)}")
        return "payroll_overtime", answer, model, None

    match = re.search(
        r"1 USD equals ([0-9./]+) EUR\. A traveller exchanges "
        r"(\$\d+\.\d{2})", text, re.I)
    if match:
        rate, amount = number(match.group(1)), number(match.group(2))
        received = rate * amount
        model = f"x = {amount}*{exact_text(rate)}"
        return "currency_supplied_rate", f"{exact_text(received)} EUR", model, None

    match = re.search(
        r"Ana, Ben, and Chi, split (\$\d+\.\d{2}) in the ratio "
        r"(\d+):(\d+):(\d+)", text, re.I)
    if match:
        total = number(match.group(1))
        first, second, third = map(int, match.groups()[1:])
        per_part = total / (first + second + third)
        model = f"x = {total}/({first}+{second}+{third})"
        answer = (f"Ana {money_text(first * per_part)}; "
                  f"Ben {money_text(second * per_part)}; "
                  f"Chi {money_text(third * per_part)}")
        return "split_by_ratio", answer, model, None

    match = re.search(
        r"account starts with (\$\d+\.\d{2})\. Another (\$\d+\.\d{2}) is "
        r"added .*? goal is (\$\d+\.\d{2})", text, re.I)
    if match:
        start, weekly, goal = map(number, match.groups())
        weeks = (goal - start) / weekly
        model = f"{start} + {weekly}w = {goal}"
        return "savings_goal_weeks", f"{weeks} weeks; {money_text(goal)}", model, None
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, winner = solve(problem)
    if modifier == "with_model":
        variable = {"best_buy": "choice", "savings_goal_weeks": "w"}.get(variant, "x")
        answer = f"{model}; {variable} = {answer}"
    return variant, answer, winner


class TestMoneyLifeGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(245)
        seen = set()
        winners = set()
        for _ in range(1200):
            result = MoneyLifeGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_money_life_")
            parsed_variant, answer, winner = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
            if winner:
                winners.add(winner)
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})
        self.assertEqual(winners, {"A", "B"})

    def test_all_five_renderings_preserve_every_template(self):
        cases = (
            ("Brand A has 12 oz for $3.60. Brand B has 20 oz for $5.00.",
             "Which brand costs less for each ounce?", "best_buy"),
            ("A monthly take-home amount is $3000.00. Rent is 30%, food is "
             "15%, and travel is 10% of that amount.",
             "How much remains, and what percent of the monthly amount is it?",
             "budget_share"),
            ("An employee works 45 hours at $15.00 per hour. Hours above 40 "
             "are paid at 1.5 times the regular rate.",
             "What are the regular pay, overtime pay, and total pay?",
             "payroll_overtime"),
            ("A posted exchange states that 1 USD equals 0.8 EUR. A traveller "
             "exchanges $120.00.", "How many EUR does the traveller receive?",
             "currency_supplied_rate"),
            ("Three friends, Ana, Ben, and Chi, split $600.00 in the ratio "
             "2:3:5, in that order.", "How much money does each person receive?",
             "split_by_ratio"),
            ("A savings account starts with $100.00. Another $25.00 is added at "
             "the end of each week. The goal is $300.00.",
             "After how many weekly additions is the goal reached?",
             "savings_goal_weeks"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the market stand", record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(246)
        for _ in range(700):
            result = MoneyLifeGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(247)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MoneyLifeGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MoneyLifeGenerator("bogus")
        with self.assertRaises(ValueError):
            MoneyLifeGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(248)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = MoneyLifeGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
