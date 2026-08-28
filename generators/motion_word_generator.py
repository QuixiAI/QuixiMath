"""Exact distance-rate-time stories whose problem text names no method.

Variants: ``toward_each_other``, ``same_direction_catch_up``,
``round_trip_average_speed``, ``with_current``, ``head_start``, and
``time_to_meet_from_table``. Five shared-context renderings and the four
standard applied modifiers are supported. All times are built backward to be
integers or terminating half/quarter hours. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``DRT``, ``TABLE_READ``, ``MODEL_EQ``,
``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, estimate_first, exact,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("toward_each_other", "same_direction_catch_up",
            "round_trip_average_speed", "with_current", "head_start",
            "time_to_meet_from_table")
PLACES = tuple(
    setting
    for key in ("trip", "sports", "people")
    for setting in CONTEXTS[key].settings
)
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} travel note from {place} says: {facts}",
    "Trip {record} at {place} — {facts} {question}",
    "At {place}, record {record}: {facts_lc} {question}",
    "Consider the {record} report from {place}: {facts} {question}",
)
TIMES = (Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2),
         Fraction(3), Fraction(7, 2), Fraction(4))


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(PLACES),
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def hours(value):
    return unit(value, "hour")


def speed(value):
    return unit(value, "km/h")


def distance(value):
    return unit(value, "km")


class MotionWordGenerator(ProblemGenerator):
    """Generate exact relative-motion stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("hours", "km", "km/h")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _toward_each_other(table=False):
        first = random.randrange(30, 91, 5)
        second = random.randrange(30, 91, 5)
        meet_time = random.choice(TIMES)
        gap = (first + second) * meet_time
        if table:
            facts = ("A travel table gives — traveller A: start 0 km, speed "
                     f"{first} km/h; traveller B: start {exact(gap)} km, "
                     f"speed -{second} km/h.")
            question = "After how many hours are the travellers at the same position?"
            model = f"{first}t = {exact(gap)} - {second}t"
            variant = "time_to_meet_from_table"
            steps = [step("TABLE_READ", "traveller A", "start 0 km",
                          f"speed {first} km/h"),
                     step("TABLE_READ", "traveller B",
                          f"start {exact(gap)} km", f"speed -{second} km/h")]
        else:
            facts = (f"Train A and train B are {exact(gap)} km apart. They "
                     f"travel toward each other at {first} km/h and "
                     f"{second} km/h.")
            question = "After how many hours do the trains meet?"
            model = f"{first}t + {second}t = {exact(gap)}"
            variant = "toward_each_other"
            steps = [step("DRT", "train A", f"d = {first}t"),
                     step("DRT", "train B", f"d = {second}t")]
        combined = first + second
        distance1, distance2 = first * meet_time, second * meet_time
        steps += [step("MODEL_EQ", model, "positions agree at meeting"),
                  step("A", first, second, combined),
                  step("D", exact(gap), combined, exact(meet_time)),
                  step("M", first, exact(meet_time), exact(distance1)),
                  step("M", second, exact(meet_time), exact(distance2)),
                  step("A", exact(distance1), exact(distance2), exact(gap)),
                  step("CHECK", "distances cover initial gap", exact(gap))]
        answer = hours(meet_time)
        used = [f"gap {exact(gap)} km", f"{first} km/h", f"{second} km/h"]
        return (variant, facts, question, steps, answer, meet_time, model, "t",
                used, hours)

    @staticmethod
    def _catch_up():
        while True:
            slow = random.randrange(20, 61, 5)
            fast = random.randrange(slow + 5, 91, 5)
            delay = random.randint(1, 4)
            total_time = Fraction(fast * delay, fast - slow)
            if total_time <= 12 and total_time.denominator in (1, 2, 4):
                break
        fast_time = total_time - delay
        catch_distance = slow * total_time
        facts = (f"Cyclist A leaves a trailhead first at {slow} km/h. Cyclist "
                 f"B leaves the same point {hours(delay)} later at {fast} km/h.")
        question = ("How many hours after cyclist A leaves does cyclist B catch "
                    "up, and how far from the trailhead are they then?")
        model = f"{slow}t = {fast}(t-{delay})"
        steps = [step("DRT", "cyclist A", f"d = {slow}t"),
                 step("DRT", "cyclist B", f"d = {fast}(t-{delay})"),
                 step("MODEL_EQ", model, "equal distances at catch-up"),
                 step("S", fast, slow, fast - slow),
                 step("M", fast, delay, fast * delay),
                 step("D", fast * delay, fast - slow, exact(total_time)),
                 step("S", exact(total_time), delay, exact(fast_time)),
                 step("M", slow, exact(total_time), exact(catch_distance)),
                 step("M", fast, exact(fast_time), exact(catch_distance)),
                 step("CHECK", "equal distances", exact(catch_distance))]
        answer = (f"{hours(total_time)} after A leaves; "
                  f"{distance(catch_distance)}")
        used = [f"A {slow} km/h", f"B {fast} km/h", f"delay {hours(delay)}"]
        return ("same_direction_catch_up", facts, question, steps, answer,
                total_time, model, "t", used, hours)

    @staticmethod
    def _round_trip():
        while True:
            out_speed, back_speed = random.sample(range(20, 81, 5), 2)
            leg = random.randrange(20, 201, 10)
            out_time = Fraction(leg, out_speed)
            back_time = Fraction(leg, back_speed)
            total_time = out_time + back_time
            average = Fraction(2 * leg, total_time)
            if average.denominator in (1, 2, 4, 5, 10):
                break
        facts = (f"A van travels {leg} km from a depot at {out_speed} km/h "
                 f"and returns the same {leg} km at {back_speed} km/h.")
        question = "What is its average speed for the whole round trip?"
        model = (f"x = {2 * leg}/({leg}/{out_speed} + "
                 f"{leg}/{back_speed})")
        steps = [step("DRT", "outward leg", f"t = {leg}/{out_speed}"),
                 step("D", leg, out_speed, exact(out_time)),
                 step("DRT", "return leg", f"t = {leg}/{back_speed}"),
                 step("D", leg, back_speed, exact(back_time)),
                 step("A", exact(out_time), exact(back_time), exact(total_time)),
                 step("M", 2, leg, 2 * leg),
                 step("D", 2 * leg, exact(total_time), exact(average)),
                 step("CHECK", "total distance over total time", speed(average))]
        answer = speed(average)
        used = [f"{leg} km each way", f"{out_speed} km/h", f"{back_speed} km/h"]
        return ("round_trip_average_speed", facts, question, steps, answer,
                average, model, "x", used, speed)

    @staticmethod
    def _with_current():
        still = random.randrange(8, 25, 2)
        current = random.randint(1, min(6, still - 2))
        direction = random.choice(("downstream", "upstream"))
        effective = still + current if direction == "downstream" else still - current
        travel_time = random.choice(TIMES)
        trip_distance = effective * travel_time
        sign = "+" if direction == "downstream" else "-"
        facts = (f"A boat moves at {still} km/h in still water, and the current "
                 f"is {current} km/h. It travels {exact(trip_distance)} km "
                 f"{direction}.")
        question = "How many hours does the trip take?"
        model = f"t = {exact(trip_distance)}/({still} {sign} {current})"
        combine_code = "A" if direction == "downstream" else "S"
        steps = [step(combine_code, still, current, effective),
                 step("DRT", direction, f"d = {effective}t"),
                 step("MODEL_EQ", model, f"{direction} trip"),
                 step("D", exact(trip_distance), effective, exact(travel_time)),
                 step("M", effective, exact(travel_time), exact(trip_distance)),
                 step("CHECK", "recovered trip distance", distance(trip_distance))]
        answer = hours(travel_time)
        used = [f"still-water speed {still} km/h", f"current {current} km/h",
                f"distance {exact(trip_distance)} km", direction]
        return ("with_current", facts, question, steps, answer, travel_time,
                model, "t", used, hours)

    @staticmethod
    def _head_start():
        slow = random.randrange(4, 13)
        fast = random.randrange(slow + 1, 19)
        catch_time = random.choice(TIMES)
        head_start = (fast - slow) * catch_time
        fast_distance = fast * catch_time
        slow_distance = slow * catch_time
        facts = (f"Runner A begins {exact(head_start)} km ahead of runner B "
                 f"and continues at {slow} km/h. Runner B travels at "
                 f"{fast} km/h in the same direction.")
        question = ("How many hours until runner B catches runner A, and how "
                    "far does runner B travel?")
        model = f"{fast}t = {exact(head_start)} + {slow}t"
        steps = [step("DRT", "runner A position",
                      f"d = {exact(head_start)} + {slow}t"),
                 step("DRT", "runner B position", f"d = {fast}t"),
                 step("MODEL_EQ", model, "equal positions at catch-up"),
                 step("S", fast, slow, fast - slow),
                 step("D", exact(head_start), fast - slow, exact(catch_time)),
                 step("M", fast, exact(catch_time), exact(fast_distance)),
                 step("M", slow, exact(catch_time), exact(slow_distance)),
                 step("A", exact(head_start), exact(slow_distance),
                      exact(fast_distance)),
                 step("CHECK", "equal positions", distance(fast_distance))]
        answer = f"{hours(catch_time)}; {distance(fast_distance)}"
        used = [f"head start {exact(head_start)} km", f"A {slow} km/h",
                f"B {fast} km/h"]
        return ("head_start", facts, question, steps, answer, catch_time,
                model, "t", used, hours)

    @classmethod
    def _case(cls, variant):
        if variant == "toward_each_other":
            return cls._toward_each_other()
        if variant == "time_to_meet_from_table":
            return cls._toward_each_other(table=True)
        if variant == "same_direction_catch_up":
            return cls._catch_up()
        if variant == "round_trip_average_speed":
            return cls._round_trip()
        if variant == "with_current":
            return cls._with_current()
        return cls._head_start()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        (actual_variant, facts, question, steps, answer, estimate_value, model,
         variable, used, renderer) = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(101, 999)
                                   if value not in occupied])
            problem = f"A sign nearby shows route number {extra}. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"route number {extra}"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], estimate_value,
                "round the distance and speeds before dividing",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "motion relationship"))
            answer = f"{model}; {variable} = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_motion_{actual_variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
