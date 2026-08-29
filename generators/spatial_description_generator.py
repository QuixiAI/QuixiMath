"""Clock angles, bearings, coordinates, and nets — spatial reasoning in words.

Variants: ``clock_angle``, ``bearing_after_turns``, ``coordinates_from_story``,
``perimeter_from_walk``, ``compass_turns``, ``net_matches_solid``. Five
context frames and all four applied modifiers are supported. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``CLOCK_ANGLE``, ``BEARING``, ``COMPASS_TURN``, ``NET_SETUP``,
``SOLID_MATCH``, ``A``, ``S``, ``M``, ``D``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import NAMES, dec, estimate_first, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("clock_angle", "bearing_after_turns", "coordinates_from_story",
            "perimeter_from_walk", "compass_turns", "net_matches_solid")
FRAMES = (
    "{name} works out the following spatial puzzle. {facts} {question}",
    "{question} A puzzle for {name} reads: {facts}",
    "For {name}'s puzzle: {facts} {question}",
    "A note handed to {name} reads: {facts} {question}",
    "Consider the situation {name} is picturing. {facts} {question}",
)

COMPASS_POINTS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")

NET_TABLE = (
    ("6 identical squares", "cube"),
    ("2 identical squares and 4 identical rectangles", "square prism"),
    ("1 square and 4 identical triangles", "square pyramid"),
    ("2 identical triangles and 3 rectangles", "triangular prism"),
    ("4 identical triangles", "triangular pyramid"),
    ("3 pairs of identical rectangles", "rectangular prism"),
)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        name=random.choice(NAMES))


class SpatialDescriptionGenerator(ProblemGenerator):
    """Generate six exact spatial-reasoning models without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _clock_angle():
        h = random.randint(1, 12)
        m = random.choice((0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55))
        minute_angle = Fraction(m * 6)
        hour_expr = f"({h} + {m}/60) × 30" if m else f"{h} × 30"
        hour_angle = (h % 12) * 30 + Fraction(m, 60) * 30
        raw_diff = abs(hour_angle - minute_angle)
        hi, lo = max(hour_angle, minute_angle), min(hour_angle, minute_angle)
        answer_deg = min(raw_diff, 360 - raw_diff)
        facts = f"A clock reads {h}:{m:02d}."
        question = "What is the angle between the hour and minute hands?"
        model = "hour angle = (h + m/60) × 30; minute angle = m × 6; angle = abs(difference)"
        steps = [step("CLOCK_ANGLE", "minute hand", f"{dec(minute_angle)}°"),
                step("CLOCK_ANGLE", "hour hand", f"{hour_expr} = {dec(hour_angle)}°"),
                step("S", dec(hi), dec(lo), dec(raw_diff))]
        if raw_diff > 180:
            steps.append(step("S", 360, dec(raw_diff), dec(answer_deg)))
        answer = f"{dec(answer_deg)}°"
        used = [f"time {h}:{m:02d}"]
        return facts, question, steps, answer, minute_angle, model, used, str

    @staticmethod
    def _bearing_after_turns():
        start = random.choice(range(0, 360, 10))
        legs = []
        current = start
        for _ in range(random.choice((2, 3))):
            direction = random.choice(("right", "left"))
            amount = random.choice(range(10, 170, 10))
            current = (current + amount) % 360 if direction == "right" else (current - amount) % 360
            legs.append((direction, amount, current))
        facts = (f"A hiker starts heading {start:03d}°. They turn " +
                 ", then ".join(f"{d} {a}°" for d, a, _ in legs) + ".")
        question = "What is the final heading?"
        model = "right adds degrees; left subtracts degrees (mod 360)"
        steps = [step("BEARING", f"{d} {a}", f"{c:03d}°") for d, a, c in legs]
        answer = f"{current:03d}°"
        used = [f"start {start:03d}°"] + [f"{d} {a}°" for d, a, _ in legs]
        return facts, question, steps, answer, current, model, used, str

    @staticmethod
    def _coordinates_from_story():
        moves = random.sample(
            [("east", random.randint(2, 12)), ("west", random.randint(2, 12)),
            ("north", random.randint(2, 12)), ("south", random.randint(2, 12))], 4)
        x = y = 0
        for direction, dist in moves:
            if direction == "east":
                x += dist
            elif direction == "west":
                x -= dist
            elif direction == "north":
                y += dist
            else:
                y -= dist
        facts = ("Starting at the origin, a robot moves " +
                 ", then ".join(f"{d} units {n}" for n, d in moves) + ".")
        question = "What are its final coordinates?"
        model = "x = east − west; y = north − south"
        steps = [step("A" if d[0] in ("east", "north") else "S", "running total",
                     d[1], f"{d[0]} leg") for d in moves]
        answer = f"({x}, {y})"
        used = [f"{d} units {n}" for n, d in moves]
        return facts, question, steps, answer, x, model, used, str

    @staticmethod
    def _perimeter_from_walk():
        d1, d2 = random.randint(10, 90), random.randint(10, 90)
        perimeter = 2 * (d1 + d2)
        facts = (f"A rectangular path is walked: {d1} m in one direction, "
                 f"then {d2} m turning a corner, then back to the start "
                 "along the remaining two sides.")
        question = "What is the total distance walked?"
        model = "perimeter = 2 × (leg1 + leg2)"
        steps = [step("A", d1, d2, d1 + d2), step("M", 2, d1 + d2, perimeter)]
        answer = f"{perimeter} m"
        used = [f"legs {d1} m, {d2} m"]
        return facts, question, steps, answer, perimeter, model, used, str

    @staticmethod
    def _compass_turns():
        start = random.choice(COMPASS_POINTS)
        steps_turn = random.randint(1, 7)
        direction = random.choice(("clockwise", "counterclockwise"))
        turn_deg = steps_turn * 45
        shift = steps_turn if direction == "clockwise" else -steps_turn
        start_index = COMPASS_POINTS.index(start)
        end_index = (start_index + shift) % 8
        end = COMPASS_POINTS[end_index]
        facts = f"A drone starts facing {start}. It turns {turn_deg}° {direction}."
        question = "Which direction is it now facing?"
        model = "steps = degrees/45; new index = (start index + steps) mod 8"
        steps = [step("D", turn_deg, 45, steps_turn),
                step("COMPASS_TURN", f"{start} {direction} {steps_turn} steps", end)]
        answer = end
        used = [f"start {start}", f"turn {turn_deg}° {direction}"]
        return facts, question, steps, answer, steps_turn, model, used, str

    @staticmethod
    def _net_matches_solid():
        face_desc, solid = random.choice(NET_TABLE)
        size = random.randint(2, 12)
        facts = f"A flat net is made of {face_desc}, each edge about {size} cm."
        question = "What solid does the net fold into?"
        model = "match the face list to a known solid"
        steps = [step("NET_SETUP", face_desc, "identify the solid"),
                step("SOLID_MATCH", face_desc, solid)]
        answer = solid
        used = [face_desc]
        return facts, question, steps, answer, size, model, used, str

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(201, 501) if n not in occupied])
            problem = f"A nearby sign shows {extra} unrelated markers. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} unrelated markers"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the answer",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "spatial relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_spatial_description_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
