"""Problem-text-only oracles for :class:`RoundingEffectGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.rounding_effect_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    RoundingEffectGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").rstrip("."))


def round_to(value, increment):
    value, increment = Fraction(value), Fraction(increment)
    scaled = value / increment
    whole, remainder = divmod(scaled.numerator, scaled.denominator)
    return (whole + (2 * remainder >= scaled.denominator)) * increment


def fixed(value, places):
    value = Fraction(value)
    scaled = value * 10 ** places
    if scaled.denominator != 1:
        raise AssertionError(f"cannot fix {value} to {places} places")
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


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
    places = 0
    scaled = value
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    return fixed(value, places)


def clean(problem):
    return re.sub(r"^A nearby log lists \d+ old entries\. ", "", problem)


def solve(problem):
    """Recompute the range or rounding comparison from prompt values."""
    text = clean(problem)

    match = re.search(
        r"device shows ([0-9.]+) (kg|cm|L), rounded to the nearest "
        r"([0-9.]+) \2", text, re.I)
    if match:
        display_token, unit_name, increment_token = match.groups()
        display, increment = number(display_token), number(increment_token)
        low, high = display - increment / 2, display + increment / 2
        places = len(increment_token.split(".")[1]) if "." in increment_token else 0
        low_text, high_text = fixed(low, places + 1), fixed(high, places + 1)
        variable = {"kg": "m", "cm": "l", "l": "v"}[unit_name.lower()]
        answer = (f"{low_text} {unit_name} ≤ {variable} < {high_text} "
                  f"{unit_name}")
        model = f"{variable} ∈ [{low_text}, {high_text}) {unit_name}"
        return "true_range_of_display", answer, model, display, (unit_name, places)

    match = re.search(
        r"Two measurements are ([0-9.]+) and ([0-9.]+)\. Results are "
        r"reported to the nearest 0\.1", text, re.I)
    if match:
        first, second = map(number, match.groups())
        first_rounded = round_to(first, Fraction(1, 10))
        second_rounded = round_to(second, Fraction(1, 10))
        rounded_first_sum = first_rounded + second_rounded
        rounded_after = round_to(first + second, Fraction(1, 10))
        difference = abs(rounded_first_sum - rounded_after)
        answer = (f"{fixed(rounded_after, 1)}; rounding first gives "
                  f"{fixed(rounded_first_sum, 1)}, off by "
                  f"{fixed(difference, 1)}")
        model = (f"round({fixed(first, 2)} + {fixed(second, 2)}, 0.1) = "
                 f"{fixed(rounded_after, 1)}")
        return "round_before_vs_after", answer, model, rounded_after, None

    match = re.search(r"list of counts is (\d+), (\d+), (\d+)", text, re.I)
    if match:
        values = list(map(int, match.groups()))
        fronts = [(value // 100) * 100 for value in values]
        estimate, total = sum(fronts), sum(values)
        answer = f"about {estimate}; exact {total}"
        model = (f"{' + '.join(map(str, fronts))} = {estimate}; "
                 f"exact sum = {total}")
        return "front_end_estimate", answer, model, Fraction(total), None

    match = re.search(
        r"product is (\d+) × (\d+)\. Replace each factor by its nearest "
        r"multiple of ten", text, re.I)
    if match:
        first, second = map(int, match.groups())
        first_rounded = int(round_to(first, 10))
        second_rounded = int(round_to(second, 10))
        estimate, product = first_rounded * second_rounded, first * second
        answer = f"about {estimate}; exact {product}"
        model = f"{first} × {second} ≈ {first_rounded} × {second_rounded} = {estimate}"
        return "leading_digit_estimate", answer, model, Fraction(product), None

    match = re.search(
        r"There are (\d+) identical lengths of ([0-9.]+) cm.*?nearest 0\.1 cm",
        text, re.I)
    if match:
        count = int(match.group(1))
        per_item = number(match.group(2))
        rounded_item = round_to(per_item, Fraction(1, 10))
        rounded_each_total = count * rounded_item
        exact_total = count * per_item
        rounded_total = round_to(exact_total, Fraction(1, 10))
        difference = abs(rounded_each_total - rounded_total)
        answer = (f"{fixed(rounded_total, 1)} cm; rounding each gives "
                  f"{fixed(rounded_each_total, 1)} cm, off by "
                  f"{fixed(difference, 1)} cm")
        model = (f"round({count} × {fixed(per_item, 2)}, 0.1) = "
                 f"{fixed(rounded_total, 1)} cm")
        return "accumulated_rounding", answer, model, rounded_total, None

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestRoundingEffectGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(298)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(28):
                    result = RoundingEffectGenerator(variant, modifier).generate()
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
            "true_range_of_display": (
                "A device shows 3.4 kg, rounded to the nearest 0.1 kg."),
            "round_before_vs_after": (
                "Two measurements are 2.46 and 3.47. Results are reported to "
                "the nearest 0.1."),
            "front_end_estimate": (
                "A list of counts is 347, 582, 264. Keep only each hundreds "
                "place for an initial size estimate, then total the exact counts."),
            "leading_digit_estimate": (
                "A product is 47 × 62. Replace each factor by its nearest "
                "multiple of ten for an initial size estimate."),
            "accumulated_rounding": (
                "There are 19 identical lengths of 1.41 cm. A total must be "
                "reported to the nearest 0.1 cm."),
        }
        question = "Give the rounded comparison and exact check."
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_true_range_units_places_and_nonzero_rounding_effects(self):
        random.seed(299)
        units, places = set(), set()
        for _ in range(500):
            result = RoundingEffectGenerator(
                "true_range_of_display", "plain").generate()
            unit_name, place_count = solve(result["problem"])[4]
            units.add(unit_name)
            places.add(place_count)
        self.assertEqual(units, {"kg", "cm", "L"})
        self.assertEqual(places, {0, 1, 2})
        for variant in ("round_before_vs_after", "accumulated_rounding"):
            for _ in range(200):
                answer = RoundingEffectGenerator(variant, "plain").generate()[
                    "final_answer"]
                self.assertNotIn("off by 0.0", answer)

    def test_arithmetic_round_and_range_steps(self):
        random.seed(300)
        for _ in range(1400):
            result = RoundingEffectGenerator().generate()
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
                elif fields[0] == "ROUND":
                    increment = (Fraction(1, 10) if "0.1" in fields[2]
                                 else Fraction(10))
                    self.assertEqual(round_to(number(fields[1]), increment),
                                     number(fields[3]), raw)
                elif fields[0] == "FLOOR":
                    self.assertEqual((int(fields[1]) // 100) * 100,
                                     int(fields[3]), raw)

    def test_modifier_shapes_and_native_estimate_variants(self):
        random.seed(301)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = RoundingEffectGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_rounding_effect_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
                if variant in ("front_end_estimate", "leading_digit_estimate"):
                    self.assertIn("ESTIMATE", codes)
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
        with self.assertRaises(ValueError):
            RoundingEffectGenerator("bogus")
        with self.assertRaises(ValueError):
            RoundingEffectGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(302)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = RoundingEffectGenerator().generate()
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
