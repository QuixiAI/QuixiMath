"""Problem-text-only oracles for unit-rate generators."""
import random
import re
import unittest
from fractions import Fraction

from generators.unit_rate_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    UnitRateFromTableGenerator,
    UnitRateGenerator,
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
    return re.sub(r"^A sign nearby shows aisle \d+\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"Brand A offers (\d+) oz for (\$\d+\.\d{2})\. Brand B offers "
        r"(\d+) oz for (\$\d+\.\d{2})", text, re.I)
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

    match = re.search(r"(\d+) ([a-z ]+) cost (\$\d+\.\d{2})", text, re.I)
    if match:
        quantity, plural, total = int(match.group(1)), match.group(2), number(match.group(3))
        singular = re.search(r"one ([a-z ]+) cost", text, re.I).group(1)
        value = total / quantity
        model = f"x = {exact_text(total)}/{quantity}"
        return "cost_per_item", f"{money_text(value)} per {singular}", model, None

    match = re.search(
        r"Traveling (\d+) miles takes ([0-9.]+) hours?", text, re.I)
    if match:
        quantity, total = int(match.group(1)), number(match.group(2))
        value = total / quantity
        time_word = "hour" if value == 1 else "hours"
        model = f"x = {exact_text(total)}/{quantity}"
        return ("time_per_distance",
                f"{exact_text(value)} {time_word} per mile", model, None)

    match = re.search(
        r"Completing (\d+) ([a-z]+) takes (\d+) minutes", text, re.I)
    if match:
        quantity, plural, total = int(match.group(1)), match.group(2), int(match.group(3))
        singular = re.search(r"one ([a-z]+) take", text, re.I).group(1)
        value = Fraction(total, quantity)
        model = f"x = {total}/{quantity}"
        return ("time_per_task",
                f"{exact_text(value)} minutes per {singular}", model, None)
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, winner = solve(problem)
    if modifier == "with_model":
        variable = "choice" if variant == "best_buy" else "x"
        answer = f"{model}; {variable} = {answer}"
    return variant, answer, winner


class TestUnitRateGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(257)
        seen = set()
        winners = set()
        for _ in range(1000):
            variant = random.choice(VARIANTS)
            modifier = random.choice(MODIFIERS)
            result = UnitRateGenerator(modifier=modifier, variant=variant).generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
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
            ("6 notebooks cost $15.00.", "How much does one notebook cost?",
             "cost_per_item"),
            ("Traveling 6 miles takes 9 hours at a steady pace.",
             "How much time does one mile take?", "time_per_distance"),
            ("Completing 6 pages takes 30 minutes.",
             "How much time does one page take?", "time_per_task"),
            ("Brand A offers 12 oz for $3.60. Brand B offers 20 oz for $5.00.",
             "Which brand costs less for each ounce?", "best_buy"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the corner shop", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(258)
        for _ in range(600):
            result = UnitRateGenerator(modifier=random.choice(MODIFIERS)).generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_modifier_shapes_and_legacy_constructor(self):
        random.seed(259)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = UnitRateGenerator(modifier=modifier, variant=variant).generate()
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
        self.assertEqual(UnitRateGenerator().modifier, "plain")
        self.assertEqual(UnitRateGenerator(distractor=True).modifier, "distractor")
        with self.assertRaises(ValueError):
            UnitRateGenerator(modifier="bogus")
        with self.assertRaises(ValueError):
            UnitRateGenerator(variant="bogus")
        with self.assertRaises(ValueError):
            UnitRateGenerator(distractor=True, modifier="plain")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(260)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = UnitRateGenerator(modifier=random.choice(MODIFIERS)).generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)1 hours\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


class TestUnitRateFromTableGenerator(unittest.TestCase):
    def test_problem_only_oracle_and_pipe_safety(self):
        random.seed(261)
        for _ in range(500):
            result = UnitRateFromTableGenerator().generate()
            rows = [(int(x), int(y)) for x, y in
                    re.findall(r"(\d+) to (\d+)", result["problem"])]
            self.assertGreaterEqual(len(rows), 3)
            rates = {Fraction(y, x) for x, y in rows}
            self.assertEqual(len(rates), 1)
            rate = rates.pop()
            labels = re.search(
                r"lists (.+?) to (.+?) as follows:.*How many (.+?) correspond "
                r"to one (.+?)\?", result["problem"])
            self.assertIsNotNone(labels)
            y_label, one_unit = labels.group(3), labels.group(4)
            answer = f"{rate} {y_label} per {one_unit}"
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"][-1], f"Z{DELIM}{answer}")
            self.assertNotIn(DELIM, result["problem"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
