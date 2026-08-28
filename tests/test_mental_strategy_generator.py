"""Problem-text-only oracles for :class:`MentalStrategyGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.mental_strategy_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MentalStrategyGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


def exact_text(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return (str(value.numerator) if value.denominator == 1 else
                f"{value.numerator}/{value.denominator}")
    scaled, places = value, 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return sign + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def clean(problem):
    return re.sub(r"^A shelf nearby holds \d+ unused labels\. ", "", problem)


def eval_rewrite(expression):
    """Evaluate the generator's tiny rewrite grammar independently."""
    if " − " in expression:
        left, right = expression.split(" − ")
        return eval_rewrite(left) - eval_rewrite(right)
    if " + " in expression:
        return sum(eval_rewrite(part) for part in expression.split(" + "))
    if " × " in expression:
        product = 1
        for part in expression.split(" × "):
            product *= int(part)
        return product
    return int(expression)


def solve(problem):
    """Recognize the requested rewrite and recompute the exact result."""
    text = clean(problem)

    match = re.search(
        r"calculation is (\d+) × (\d+), and a nearby power-of-ten rewrite",
        text, re.I)
    if match:
        first, second = map(int, match.groups())
        benchmark = 100 if second < 100 else 1000
        gap = benchmark - second
        correction = first * gap
        result = first * second
        rewrite = (f"{first} × {benchmark} − {correction}" if gap > 1 else
                   f"{first} × {benchmark} − {first}")
        answer = f"{result} ({rewrite})"
        model = f"{first} × {second} = {rewrite}"
        return "compensation", answer, model, Fraction(result), None

    match = re.search(
        r"product is (\d+) × (\d+)\. Keep the same product after one factor "
        r"is halved", text, re.I)
    if match:
        first, second = map(int, match.groups())
        result = first * second
        rewrite = f"{first // 2} × {2 * second}"
        answer = f"{result} ({rewrite})"
        model = f"{first} × {second} = {rewrite}"
        return "doubling_halving", answer, model, Fraction(result), None

    match = re.search(
        r"product is (\d+) × (\d+)\. Split the second factor into its tens",
        text, re.I)
    if match:
        first, second = map(int, match.groups())
        tens, ones = second - second % 10, second % 10
        result = first * second
        rewrite = f"{first} × {tens} + {first} × {ones}"
        answer = f"{result} ({rewrite})"
        model = f"{first} × {second} = {rewrite}"
        return "distributive_split", answer, model, Fraction(result), None

    match = re.search(
        r"sum is (\d+) \+ (\d+)\. Move just enough from the second addend",
        text, re.I)
    if match:
        first, second = map(int, match.groups())
        shift = 10 - first % 10
        friendly, adjusted = first + shift, second - shift
        result = first + second
        rewrite = f"{friendly} + {adjusted}"
        answer = f"{result} ({rewrite})"
        model = f"{first} + {second} = {rewrite}"
        return "friendly_numbers", answer, model, Fraction(result), None

    match = re.search(
        r"purchase costs (\$[0-9.]+) and is paid with (\$[0-9.]+)", text,
        re.I)
    if match:
        price, payment = map(number, match.groups())
        next_dollar = Fraction(price.numerator // price.denominator + 1)
        first_jump, second_jump = next_dollar - price, payment - next_dollar
        change = payment - price
        rewrite = (f"{money_text(first_jump)} to {money_text(next_dollar)}, "
                   f"then {money_text(second_jump)}")
        answer = f"{money_text(change)} ({rewrite})"
        model = f"change = {money_text(payment)} − {money_text(price)}"
        return "count_up_change", answer, model, change, None

    match = re.search(r"target is (\d+)% of (\d+)", text, re.I)
    if match:
        percent, base = map(int, match.groups())
        result = Fraction(percent * base, 100)
        tens_count = percent // 10
        rewrite = f"{10 * tens_count}% + 5%"
        answer = f"{exact_text(result)} ({rewrite})"
        model = (f"{percent}% of {base} = {10 * tens_count}% of {base} + "
                 f"5% of {base}")
        return "percent_shortcut", answer, model, result, None

    match = re.search(
        r"For (\d+) × (\d+), proposal A is (.+?); proposal B is (.+?)\.",
        text, re.I)
    if match:
        first, second = map(int, match.groups()[:2])
        proposal_a, proposal_b = match.groups()[2:]
        result = first * second
        if eval_rewrite(proposal_a) != result:
            raise AssertionError("proposal A is not equivalent")
        if eval_rewrite(proposal_b) == result:
            raise AssertionError("proposal B unexpectedly equivalent")
        if " − " in proposal_a:
            label, family = "compensation", "compensation"
        elif proposal_a.count(" × ") == 1:
            label, family = "doubling and halving", "doubling_halving"
        else:
            label, family = "distributive split", "distributive_split"
        answer = f"A: {label}; {result} ({proposal_a})"
        model = f"{first} × {second} = {proposal_a}"
        return "choose_strategy", answer, model, Fraction(result), family

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, family = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, family


class TestMentalStrategyGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(288)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(20):
                    result = MentalStrategyGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model, _, _ = expected(
                        result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer,
                                     result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1],
                                         model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "compensation": (
                "The calculation is 47 × 99, and a nearby power-of-ten rewrite "
                "is requested."),
            "doubling_halving": (
                "The product is 16 × 25. Keep the same product after one factor "
                "is halved and the other is doubled."),
            "distributive_split": (
                "The product is 23 × 47. Split the second factor into its tens "
                "and ones."),
            "friendly_numbers": (
                "The sum is 58 + 37. Move just enough from the second addend to "
                "make the first end in zero."),
            "count_up_change": (
                "A purchase costs $13.45 and is paid with $20.00. Count upward "
                "through the next whole dollar."),
            "percent_shortcut": (
                "The target is 15% of 80. Build it from a whole number of 10% "
                "pieces and one 5% piece."),
            "choose_strategy": (
                "For 47 × 99, proposal A is 47 × 100 − 47; proposal B is "
                "47 × 100 + 47."),
        }
        question = "Give the exact result and rewrite."
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_choose_strategy_reaches_all_subfamilies(self):
        random.seed(289)
        families = set()
        for _ in range(400):
            result = MentalStrategyGenerator("choose_strategy", "plain").generate()
            families.add(solve(result["problem"])[4])
        self.assertEqual(families,
                         {"compensation", "doubling_halving",
                          "distributive_split"})

    def test_arithmetic_steps(self):
        random.seed(290)
        for _ in range(1400):
            result = MentalStrategyGenerator().generate()
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

    def test_modifier_shapes_strategy_labels_and_invalid_inputs(self):
        labels = {
            "compensation": "compensation",
            "doubling_halving": "doubling and halving",
            "distributive_split": "distributive split",
            "friendly_numbers": "friendly numbers",
            "count_up_change": "count up change",
            "percent_shortcut": "percent shortcut",
        }
        random.seed(291)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MentalStrategyGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_mental_strategy_{variant}_{modifier}")
                strategy = next(raw for raw in result["steps"]
                                if raw.startswith(f"STRATEGY{DELIM}"))
                if variant in labels:
                    self.assertIn(labels[variant], strategy)
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MentalStrategyGenerator("bogus")
        with self.assertRaises(ValueError):
            MentalStrategyGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(292)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = MentalStrategyGenerator().generate()
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
