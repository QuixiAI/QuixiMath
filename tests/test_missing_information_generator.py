"""Problem-text-only oracles for :class:`MissingInformationGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.missing_information_generator import (
    APPLIED,
    FAMILIES,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MissingInformationGenerator,
)
from helpers import DELIM


SLOTS = {
    "purchase": "the price of a notebook",
    "work": "the time worker B needs alone",
    "motion": "the speed of train B",
    "mixture": "the concentration of the second solution",
    "linear": "the hourly charge",
}


def number(token):
    return Fraction(token.replace("$", "").replace("%", ""))


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


def hours_text(value):
    return f"{exact_text(value)} {'hour' if Fraction(value) == 1 else 'hours'}"


def variant_for(text, control):
    if control:
        return "solvable_control"
    if "Choose the needed fact" in text:
        return "which_of_two_missing"
    if "brochures" in text:
        return "extra_and_missing"
    return "identify_missing"


def missing(family):
    return f"insufficient information; need {SLOTS[family]}"


def solve(problem):
    """Invert the surface story, detect absent slots, and solve controls."""
    text = re.sub(r"^A sign nearby lists \d+ parking spaces\. ", "", problem)

    lowered = text.lower()
    if "shopper named mia" in lowered:
        family = "purchase"
        count = int(re.search(r"Mia buys (\d+) notebooks", text).group(1))
        paid = number(re.search(r"pays with (\$\d+\.\d{2})", text).group(1))
        price_match = re.search(r"notebooks at (\$\d+\.\d{2}) each", text)
        control = price_match is not None
        price = number(price_match.group(1)) if control else None
        model = f"x = {exact_text(paid)} - {count}*{exact_text(price) if control else 'p'}"
        answer = money_text(paid - count * price) if control else missing(family)

    elif "worker a can pack" in lowered:
        family = "work"
        first = int(re.search(r"Worker A can pack .*? in (\d+) hours", text, re.I).group(1))
        second_match = re.search(r"Worker B can pack .*? in (\d+) hours", text, re.I)
        control = second_match is not None
        second = int(second_match.group(1)) if control else None
        model = (f"1/{first} + 1/{second} = 1/t" if control
                 else f"1/{first} + 1/b = 1/t")
        answer = (hours_text(1 / (Fraction(1, first) + Fraction(1, second)))
                  if control else missing(family))

    elif "two trains are" in lowered:
        family = "motion"
        gap = number(re.search(r"Two trains are ([0-9.]+) km apart", text, re.I).group(1))
        first = int(re.search(r"Train A travels at (\d+) km/h", text, re.I).group(1))
        second_match = re.search(r"Train B travels at (\d+) km/h", text, re.I)
        control = second_match is not None
        second = int(second_match.group(1)) if control else None
        model = (f"{first}t + {second}t = {exact_text(gap)}" if control
                 else f"{first}t + bt = {exact_text(gap)}")
        answer = (hours_text(gap / (first + second))
                  if control else missing(family))

    elif "tank combines" in lowered:
        family = "mixture"
        match = re.search(
            r"combines (\d+) L of a (\d+)% salt solution with (\d+) L", text, re.I)
        first_volume, first_pct, second_volume = map(int, match.groups())
        second_match = re.search(r"concentration is (\d+)%", text, re.I)
        control = second_match is not None
        second_pct = int(second_match.group(1)) if control else None
        second_term = str(second_pct) if control else "p"
        model = (f"x = ({first_volume}*{first_pct} + {second_volume}*"
                 f"{second_term})/({first_volume}+{second_volume})")
        if control:
            pct = Fraction(first_volume * first_pct + second_volume * second_pct,
                           first_volume + second_volume)
            answer = f"{exact_text(pct)}%"
        else:
            answer = missing(family)

    elif "repair service charges" in lowered:
        family = "linear"
        fixed = number(re.search(r"charges a (\$\d+\.\d{2}) fixed fee", text, re.I).group(1))
        bill = number(re.search(r"bill of (\$\d+\.\d{2})", text, re.I).group(1))
        rate_match = re.search(r"plus (\$\d+\.\d{2}) per hour", text, re.I)
        control = rate_match is not None
        rate = number(rate_match.group(1)) if control else None
        model = (f"{fixed} + {rate}h = {bill}" if control
                 else f"{fixed} + rh = {bill}")
        answer = (hours_text((bill - fixed) / rate)
                  if control else missing(family))
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    return family, variant_for(text, control), answer, model, control


def expected(problem, modifier):
    family, variant, answer, model, control = solve(problem)
    if modifier == "with_model" and control:
        variable = {"work": "t", "motion": "t", "linear": "h"}.get(
            family, "x")
        answer = f"{model}; {variable} = {answer}"
    return family, variant, answer, model, control


class TestMissingInformationGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(263)
        seen = set()
        for family in FAMILIES:
            for variant in VARIANTS:
                for modifier in MODIFIERS:
                    for _ in range(8):
                        result = MissingInformationGenerator(
                            variant, modifier, family).generate()
                        self.assertEqual(result["steps"][-1],
                                         f"Z{DELIM}{result['final_answer']}")
                        parsed_family, parsed_variant, answer, model, control = expected(
                            result["problem"], modifier)
                        self.assertEqual(parsed_family, family)
                        self.assertEqual(parsed_variant, variant)
                        self.assertEqual(result["final_answer"], answer,
                                         result["problem"])
                        if modifier == "with_model":
                            self.assertEqual(result["steps"][0].split(DELIM)[1],
                                             model)
                        seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_control_and_missing(self):
        cases = {
            "purchase": (
                "A shopper named Mia buys 3 notebooks{slot} and pays with $20.00.",
                " at $2.50 each"),
            "work": (
                "Worker A can pack an order in 6 hours.{slot}",
                " Worker B can pack the same order in 3 hours."),
            "motion": (
                "Two trains are 300 km apart and move toward each other. Train A "
                "travels at 70 km/h.{slot}", " Train B travels at 80 km/h."),
            "mixture": (
                "A tank combines 10 L of a 30% salt solution with 5 L of a "
                "second salt solution{slot}.", " whose concentration is 60%"),
            "linear": (
                "A repair service charges a $40.00 fixed fee{slot}. A completed "
                "repair has a bill of $190.00.", " plus $25.00 per hour"),
        }
        questions = {
            "purchase": "How much change does Mia receive?",
            "work": "How many hours do they need when working together?",
            "motion": "After how many hours do the trains meet?",
            "mixture": "What percent salt is in the combined solution?",
            "linear": "How many hours of work were billed?",
        }
        self.assertEqual(len(FRAMES), 5)
        for family, (template, supplied) in cases.items():
            for control in (False, True):
                facts = template.format(slot=supplied if control else "")
                for index, frame in enumerate(FRAMES):
                    problem = frame.format(
                        facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                        question=questions[family], place="the corner shop",
                        name="Ada")
                    with self.subTest(family=family, control=control,
                                      rendering=index):
                        self.assertEqual(solve(problem)[4], control)

    def test_default_sampling_is_half_solvable(self):
        random.seed(264)
        controls = 0
        for _ in range(2000):
            result = MissingInformationGenerator().generate()
            controls += "_solvable_control_" in result["operation"]
        self.assertGreater(controls, 900)
        self.assertLess(controls, 1100)

    def test_arithmetic_steps_for_controls(self):
        random.seed(265)
        for family in FAMILIES:
            for _ in range(150):
                result = MissingInformationGenerator(
                    "solvable_control", random.choice(MODIFIERS), family).generate()
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

    def test_modifier_shapes_canonical_answers_and_invalid_inputs(self):
        random.seed(266)
        for family in FAMILIES:
            for variant in VARIANTS:
                for modifier in MODIFIERS:
                    result = MissingInformationGenerator(
                        variant, modifier, family).generate()
                    codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                    if variant != "solvable_control":
                        self.assertEqual(result["final_answer"], missing(family))
                    if modifier == "distractor":
                        self.assertEqual(codes[0], "SELECT_RELEVANT")
                    elif modifier == "estimate_first":
                        self.assertEqual(codes[0], "ESTIMATE")
                        self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                    elif modifier == "with_model":
                        self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MissingInformationGenerator("bogus")
        with self.assertRaises(ValueError):
            MissingInformationGenerator(modifier="bogus")
        with self.assertRaises(ValueError):
            MissingInformationGenerator(family="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(267)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = MissingInformationGenerator().generate()
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
