"""Problem-text-only brute-force oracles for SpatialDescriptionGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.spatial_description_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, SpatialDescriptionGenerator,
)
from helpers import DELIM

MODELS = {
    "clock_angle": "hour angle = (h + m/60) × 30; minute angle = m × 6; angle = abs(difference)",
    "bearing_after_turns": "right adds degrees; left subtracts degrees (mod 360)",
    "coordinates_from_story": "x = east − west; y = north − south",
    "perimeter_from_walk": "perimeter = 2 × (leg1 + leg2)",
    "compass_turns": "steps = degrees/45; new index = (start index + steps) mod 8",
    "net_matches_solid": "match the face list to a known solid",
}

COMPASS_POINTS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")

#: An independent copy of the net-to-solid classification (a supplied fact
#: table, not a computed procedure — the oracle looks it up itself).
NET_TABLE = {
    "6 identical squares": "cube",
    "2 identical squares and 4 identical rectangles": "square prism",
    "1 square and 4 identical triangles": "square pyramid",
    "2 identical triangles and 3 rectangles": "triangular prism",
    "4 identical triangles": "triangular pyramid",
    "3 pairs of identical rectangles": "rectangular prism",
}


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        raise AssertionError(f"does not terminate: {value}")
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def clean(problem):
    return re.sub(r"^A nearby sign shows \d+ unrelated markers\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(r"A clock reads (\d+):(\d+)", text)
    if match:
        h, m = int(match.group(1)), int(match.group(2))
        minute_angle = Fraction(m * 6)
        hour_angle = (h % 12) * 30 + Fraction(m, 60) * 30
        raw_diff = abs(hour_angle - minute_angle)
        answer_deg = min(raw_diff, 360 - raw_diff)
        return "clock_angle", f"{dec(answer_deg)}°"

    match = re.search(r"starts heading (\d+)°\. They turn ([^.]+)\.", text)
    if match:
        current = int(match.group(1))
        for leg in match.group(2).split(", then "):
            leg_match = re.match(r"(right|left) (\d+)°", leg)
            direction, amount = leg_match.group(1), int(leg_match.group(2))
            current = (current + amount) % 360 if direction == "right" else (current - amount) % 360
        return "bearing_after_turns", f"{current:03d}°"

    match = re.search(r"a robot moves ([^.]+)\.", text)
    if match:
        x = y = 0
        for leg in match.group(1).split(", then "):
            leg_match = re.match(r"(\d+) units (east|west|north|south)", leg)
            dist, direction = int(leg_match.group(1)), leg_match.group(2)
            if direction == "east":
                x += dist
            elif direction == "west":
                x -= dist
            elif direction == "north":
                y += dist
            else:
                y -= dist
        return "coordinates_from_story", f"({x}, {y})"

    match = re.search(
        r"walked: (\d+) m in one direction, then (\d+) m turning a corner", text)
    if match:
        d1, d2 = int(match.group(1)), int(match.group(2))
        return "perimeter_from_walk", f"{2 * (d1 + d2)} m"

    match = re.search(
        r"starts facing (\w+)\. It turns (\d+)° (clockwise|counterclockwise)", text)
    if match:
        start, turn_deg, direction = match.group(1), int(match.group(2)), match.group(3)
        assert turn_deg % 45 == 0, text
        steps_turn = turn_deg // 45
        shift = steps_turn if direction == "clockwise" else -steps_turn
        end_index = (COMPASS_POINTS.index(start) + shift) % 8
        return "compass_turns", COMPASS_POINTS[end_index]

    match = re.search(r"flat net is made of (.+?), each edge about \d+ cm", text)
    if match:
        face_desc = match.group(1)
        return "net_matches_solid", NET_TABLE[face_desc]

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer)


class TestSpatialDescriptionGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(430)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = SpatialDescriptionGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], MODELS[variant])
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_examples(self):
        self.assertEqual(
            solve("What is the angle between the hour and minute hands? "
                  "A clock reads 3:30."),
            ("clock_angle", "75°"))
        self.assertEqual(
            solve("A hiker starts heading 040°. They turn right 90°, then "
                  "left 30°. What is the final heading?"),
            ("bearing_after_turns", "100°"))

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "clock_angle": ("A clock reads 3:30.",
                            "What is the angle between the hour and minute hands?"),
            "bearing_after_turns": (
                "A hiker starts heading 040°. They turn right 90°, then left 30°.",
                "What is the final heading?"),
            "coordinates_from_story": (
                "Starting at the origin, a robot moves 5 units east, then "
                "3 units north, then 2 units west, then 1 units south.",
                "What are its final coordinates?"),
            "perimeter_from_walk": (
                "A rectangular path is walked: 30 m in one direction, then "
                "20 m turning a corner, then back to the start along the "
                "remaining two sides.",
                "What is the total distance walked?"),
            "compass_turns": (
                "A drone starts facing N. It turns 90° clockwise.",
                "Which direction is it now facing?"),
            "net_matches_solid": (
                "A flat net is made of 6 identical squares, each edge "
                "about 5 cm.",
                "What solid does the net fold into?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(name="Ari", facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(432)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SpatialDescriptionGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_spatial_description_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SpatialDescriptionGenerator("bogus")
        with self.assertRaises(ValueError):
            SpatialDescriptionGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(433)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = SpatialDescriptionGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = SpatialDescriptionGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
