"""Problem-text-only oracles for RateOfChangeInterpretGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.rate_of_change_interpret_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, RateOfChangeInterpretGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("−", "-").rstrip("."))


def clean(problem):
    return re.sub(r"^An unrelated roster contains \d+ membership cards\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"plant-height record has two entries — day (\d+): (\d+) cm; "
        r"day (\d+): (\d+) cm", text, re.I)
    if match:
        day1, height1, day2, height2 = map(int, match.groups())
        rate = Fraction(height2 - height1, day2 - day1)
        model = f"({height2} − {height1})/({day2} − {day1})"
        return "average_rate_from_table", f"{rate} cm per day", model

    equation = re.search(
        r"distance from the depot after t hours is d = (\d+) \+ (\d+)t kilometers",
        text, re.I)
    coefficient = re.search(r"What does the coefficient (\d+) say", text, re.I)
    constant = re.search(r"What does the constant (\d+) say", text, re.I)
    if equation and coefficient:
        initial, rate = map(int, equation.groups())
        if int(coefficient.group(1)) != rate:
            raise AssertionError("coefficient mismatch")
        model = f"d = {initial} + {rate}t"
        answer = f"{rate} km per hour; distance increases {rate} km each hour"
        return "interpret_slope", answer, model
    if equation and constant:
        initial, rate = map(int, equation.groups())
        if int(constant.group(1)) != initial:
            raise AssertionError("constant mismatch")
        model = f"d = {initial} + {rate}t"
        answer = f"{initial} km; starting distance from the depot at t = 0"
        return "interpret_intercept", answer, model

    match = re.search(
        r"height h in meters and time t in seconds, h'\((\d+)\) = ([-−]?\d+)",
        text, re.I)
    if match:
        time, signed_rate = int(match.group(1)), int(match.group(2).replace("−", "-"))
        direction = "falling" if signed_rate < 0 else "rising"
        magnitude = abs(signed_rate)
        model = f"h'({time}) = {signed_rate} m/s"
        answer = f"{direction}; {magnitude} m per second at t = {time}"
        return "interpret_derivative_sign", answer, model

    match = re.search(
        r"tank's volume increases by (\d+) liters during (\d+) minutes", text, re.I)
    if match:
        liters, minutes = map(int, match.groups())
        rate = Fraction(liters, minutes)
        model = f"{liters} liters/{minutes} minutes"
        answer = f"{rate} liters per minute; volume increases {rate} liters each minute"
        return "units_of_a_rate", answer, model

    match = re.search(
        r"plant-height record lists day 0: (\d+) cm; day (\d+): (\d+) cm; "
        r"day (\d+): (\d+) cm", text, re.I)
    if match:
        start, middle_day, middle, final_day, end = map(int, match.groups())
        first_rate = Fraction(middle - start, middle_day)
        second_rate = Fraction(end - middle, final_day - middle_day)
        winner = f"days 0–{middle_day}" if first_rate > second_rate else f"days {middle_day}–{final_day}"
        model = (f"r1 = ({middle} − {start})/{middle_day}; "
                 f"r2 = ({end} − {middle})/{final_day - middle_day}")
        answer = f"{winner}; {first_rate} vs {second_rate} cm per day"
        return "compare_rates_two_intervals", answer, model

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestRateOfChangeInterpretGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(370)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = RateOfChangeInterpretGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "average_rate_from_table": ("A plant-height record has two entries — day 2: "
                                        "15 cm; day 5: 27 cm.",
                                        "What was the plant's average growth per day between the entries?"),
            "interpret_slope": ("A delivery route's distance from the depot after t hours "
                                "is d = 55 + 12t kilometers.",
                                "What does the coefficient 12 say about the route?"),
            "interpret_intercept": ("A delivery route's distance from the depot after t "
                                    "hours is d = 55 + 12t kilometers.",
                                    "What does the constant 55 say about the route?"),
            "interpret_derivative_sign": ("For an object's height h in meters and time t "
                                          "in seconds, h'(3) = -2.",
                                          "What is happening to the object at t = 3?"),
            "units_of_a_rate": ("A tank's volume increases by 48 liters during 6 minutes.",
                                "State the change for each minute, including its units and meaning."),
            "compare_rates_two_intervals": ("A plant-height record lists day 0: 10 cm; "
                                            "day 3: 22 cm; day 5: 26 cm.",
                                            "During which interval did the plant grow faster on average?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the greenhouse", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(371)
        for _ in range(900):
            result = RateOfChangeInterpretGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]), number(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(372)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = RateOfChangeInterpretGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_rate_of_change_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            RateOfChangeInterpretGenerator("bogus")
        with self.assertRaises(ValueError):
            RateOfChangeInterpretGenerator(modifier="bogus")

    def test_both_direction_and_interval_outcomes_are_reachable(self):
        random.seed(374)
        directions, intervals = set(), set()
        for _ in range(300):
            derivative = RateOfChangeInterpretGenerator(
                "interpret_derivative_sign", "plain").generate()
            directions.add(derivative["final_answer"].split(";", 1)[0])
            comparison = RateOfChangeInterpretGenerator(
                "compare_rates_two_intervals", "plain").generate()
            intervals.add(comparison["final_answer"].split(";", 1)[0].startswith("days 0–"))
        self.assertEqual(directions, {"falling", "rising"})
        self.assertEqual(intervals, {False, True})

    def test_pipe_safety_and_render_sanity(self):
        random.seed(373)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = RateOfChangeInterpretGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
