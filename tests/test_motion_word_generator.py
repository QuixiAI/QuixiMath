"""Problem-text-only oracles for :class:`MotionWordGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.motion_word_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MotionWordGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token)


def exact_text(value):
    """Independent renderer based on repeated long division."""
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


def hours(value):
    text = exact_text(value)
    return f"{text} hour" if Fraction(value) == 1 else f"{text} hours"


def clean(problem):
    return re.sub(r"^A sign nearby shows route number \d+\. ", "", problem)


def solve(problem):
    """Invert one story and solve solely from the printed quantities."""
    text = clean(problem)

    match = re.search(
        r"train A and train B are ([0-9.]+) km apart\. They travel toward each other at "
        r"(\d+) km/h and (\d+) km/h", text, re.I)
    if match:
        gap, first, second = number(match.group(1)), int(match.group(2)), int(match.group(3))
        value = gap / (first + second)
        model = f"{first}t + {second}t = {exact_text(gap)}"
        return "toward_each_other", hours(value), model, None

    match = re.search(
        r"Cyclist A leaves .*? at (\d+) km/h\. Cyclist B leaves the same "
        r"point (\d+) hours? later at (\d+) km/h", text, re.I)
    if match:
        slow, delay, fast = map(int, match.groups())
        # Compare the initial lead (fast*delay) with the per-hour gain.
        value = Fraction(fast * delay, fast - slow)
        trip = slow * value
        answer = f"{hours(value)} after A leaves; {exact_text(trip)} km"
        model = f"{slow}t = {fast}(t-{delay})"
        return "same_direction_catch_up", answer, model, None

    match = re.search(
        r"van travels (\d+) km .*? at (\d+) km/h and returns the same \1 km "
        r"at (\d+) km/h", text, re.I)
    if match:
        leg, outward, backward = map(int, match.groups())
        elapsed = Fraction(leg, outward) + Fraction(leg, backward)
        value = Fraction(2 * leg, 1) / elapsed
        answer = f"{exact_text(value)} km/h"
        model = f"x = {2 * leg}/({leg}/{outward} + {leg}/{backward})"
        return "round_trip_average_speed", answer, model, None

    match = re.search(
        r"boat moves at (\d+) km/h in still water, and the current is (\d+) "
        r"km/h\. It travels ([0-9.]+) km (downstream|upstream)", text, re.I)
    if match:
        still, current = int(match.group(1)), int(match.group(2))
        trip, direction = number(match.group(3)), match.group(4).lower()
        effective = still + current if direction == "downstream" else still - current
        value = trip / effective
        sign = "+" if direction == "downstream" else "-"
        model = f"t = {exact_text(trip)}/({still} {sign} {current})"
        return "with_current", hours(value), model, direction

    match = re.search(
        r"Runner A begins ([0-9.]+) km ahead .*? at (\d+) km/h\. Runner B "
        r"travels at (\d+) km/h", text, re.I)
    if match:
        lead, slow, fast = number(match.group(1)), int(match.group(2)), int(match.group(3))
        value = lead / (fast - slow)
        trip = fast * value
        answer = f"{hours(value)}; {exact_text(trip)} km"
        model = f"{fast}t = {exact_text(lead)} + {slow}t"
        return "head_start", answer, model, None

    match = re.search(
        r"traveller A: start 0 km, speed (\d+) km/h; traveller B: start "
        r"([0-9.]+) km, speed -(\d+) km/h", text, re.I)
    if match:
        first, gap, second = int(match.group(1)), number(match.group(2)), int(match.group(3))
        value = gap / (first + second)
        model = f"{first}t = {exact_text(gap)} - {second}t"
        return "time_to_meet_from_table", hours(value), model, None
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, direction = solve(problem)
    if modifier == "with_model":
        variable = "x" if variant == "round_trip_average_speed" else "t"
        answer = f"{model}; {variable} = {answer}"
    return variant, answer, direction


class TestMotionWordGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(233)
        seen = set()
        directions = set()
        for _ in range(1200):
            result = MotionWordGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_motion_")
            parsed_variant, answer, direction = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
            if direction:
                directions.add(direction)
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})
        self.assertEqual(directions, {"upstream", "downstream"})

    def test_all_five_renderings_preserve_every_template(self):
        cases = (
            ("Train A and train B are 300 km apart. They travel toward each "
             "other at 70 km/h and 80 km/h.",
             "After how many hours do the trains meet?", "toward_each_other"),
            ("Cyclist A leaves a trailhead first at 40 km/h. Cyclist B leaves "
             "the same point 2 hours later at 60 km/h.",
             "How many hours after cyclist A leaves does cyclist B catch up, "
             "and how far from the trailhead are they then?",
             "same_direction_catch_up"),
            ("A van travels 60 km from a depot at 40 km/h and returns the same "
             "60 km at 60 km/h.",
             "What is its average speed for the whole round trip?",
             "round_trip_average_speed"),
            ("A boat moves at 12 km/h in still water, and the current is 3 "
             "km/h. It travels 45 km downstream.",
             "How many hours does the trip take?", "with_current"),
            ("Runner A begins 6 km ahead of runner B and continues at 6 km/h. "
             "Runner B travels at 8 km/h in the same direction.",
             "How many hours until runner B catches runner A, and how far does "
             "runner B travel?", "head_start"),
            ("A travel table gives — traveller A: start 0 km, speed 40 km/h; "
             "traveller B: start 180 km, speed -50 km/h.",
             "After how many hours are the travellers at the same position?",
             "time_to_meet_from_table"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the coast road", record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(234)
        for _ in range(700):
            result = MotionWordGenerator().generate()
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
        random.seed(235)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MotionWordGenerator(variant, modifier).generate()
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
            MotionWordGenerator("bogus")
        with self.assertRaises(ValueError):
            MotionWordGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(236)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the")
        for _ in range(500):
            result = MotionWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)1 hours\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
