"""Compute and interpret contextual rates with their units.

Variants: ``average_rate_from_table``, ``interpret_slope``,
``interpret_intercept``, ``interpret_derivative_sign``, ``units_of_a_rate``,
and ``compare_rates_two_intervals``. Five context frames and all four applied
modifiers are supported. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``AVG_RATE``, ``INTERPRET``,
``UNIT_ANALYSIS``, ``TABLE_ROW``, ``CMP``, ``A``, ``S``, ``M``, ``D``,
``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, exact, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("average_rate_from_table", "interpret_slope", "interpret_intercept",
            "interpret_derivative_sign", "units_of_a_rate",
            "compare_rates_two_intervals")
FRAMES = (
    "At {place}, {name} reviews the measurements. {facts} {question}",
    "{question} A record for {name} from {place} states: {facts}",
    "For {name}'s report at {place}: {facts} {question}",
    "A note from {place}, checked by {name}, gives: {facts} {question}",
    "Consider the measurements {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("garden", "sports", "business", "classroom")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class RateOfChangeInterpretGenerator(ProblemGenerator):
    """Generate six exact rate computations and contextual interpretations."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _average_rate_from_table():
        first_day = random.randint(0, 8)
        elapsed = random.randint(2, 8)
        rate = random.randint(1, 12)
        first_height = random.randint(4, 40)
        second_day, second_height = first_day + elapsed, first_height + rate * elapsed
        facts = (f"A plant-height record has two entries — day {first_day}: "
                 f"{first_height} cm; day {second_day}: {second_height} cm.")
        question = "What was the plant's average growth per day between the entries?"
        model = f"({second_height} − {first_height})/({second_day} − {first_day})"
        steps = [step("TABLE_ROW", f"day {first_day}", unit(first_height, "cm")),
                 step("TABLE_ROW", f"day {second_day}", unit(second_height, "cm")),
                 step("S", second_height, first_height, second_height - first_height),
                 step("S", second_day, first_day, elapsed),
                 step("D", second_height - first_height, elapsed, rate),
                 step("AVG_RATE", model, rate),
                 step("INTERPRET", f"{rate} cm per day", "plant growth on average"),
                 step("CHECK", f"{rate} × {elapsed}", second_height - first_height)]
        answer = f"{rate} cm per day"
        used = [f"day {first_day}: {first_height} cm", f"day {second_day}: {second_height} cm"]
        return facts, question, steps, answer, Fraction(rate), model, used, lambda v: f"{exact(v)} cm per day"

    @staticmethod
    def _interpret_slope():
        initial = random.randint(5, 100)
        rate = random.randint(2, 30)
        facts = (f"A delivery route's distance from the depot after t hours is "
                 f"d = {initial} + {rate}t kilometers.")
        question = f"What does the coefficient {rate} say about the route?"
        model = f"d = {initial} + {rate}t"
        steps = [step("MODEL_EQ", model, "distance after t hours"),
                 step("UNIT_ANALYSIS", "kilometers", "hours", "kilometers per hour"),
                 step("INTERPRET", rate, f"distance increases {rate} km each hour"),
                 step("A", initial, rate, initial + rate),
                 step("CHECK", "one-hour change", f"{initial + rate} − {initial} = {rate}")]
        answer = f"{rate} km per hour; distance increases {rate} km each hour"
        used = [model, "d in kilometers", "t in hours"]
        return facts, question, steps, answer, Fraction(rate), model, used, lambda v: f"{exact(v)} km per hour"

    @staticmethod
    def _interpret_intercept():
        initial = random.randint(5, 100)
        rate = random.randint(2, 30)
        facts = (f"A delivery route's distance from the depot after t hours is "
                 f"d = {initial} + {rate}t kilometers.")
        question = f"What does the constant {initial} say about the route?"
        model = f"d = {initial} + {rate}t"
        steps = [step("MODEL_EQ", model, "distance after t hours"),
                 step("M", rate, 0, 0), step("A", initial, 0, initial),
                 step("INTERPRET", initial, "distance from depot at t = 0"),
                 step("CHECK", "initial time", f"d(0) = {initial} km")]
        answer = f"{initial} km; starting distance from the depot at t = 0"
        used = [model, "d in kilometers", "t in hours"]
        return facts, question, steps, answer, Fraction(initial), model, used, lambda v: unit(v, "km")

    @staticmethod
    def _interpret_derivative_sign():
        time = random.randint(1, 20)
        magnitude = random.randint(1, 15)
        signed_rate = magnitude * random.choice((-1, 1))
        facts = (f"For an object's height h in meters and time t in seconds, "
                 f"h'({time}) = {signed_rate}.")
        question = f"What is happening to the object at t = {time}?"
        model = f"h'({time}) = {signed_rate} m/s"
        direction = "falling" if signed_rate < 0 else "rising"
        steps = [step("MODEL_EQ", model, "instantaneous vertical change"),
                 step("INTERPRET", "sign", direction),
                 step("INTERPRET", "magnitude", f"{magnitude} m per second"),
                 step("CHECK", f"t = {time}", f"{direction} at {magnitude} m/s")]
        answer = f"{direction}; {magnitude} m per second at t = {time}"
        used = [f"h'({time}) = {signed_rate}", "h in meters", "t in seconds"]
        return facts, question, steps, answer, Fraction(magnitude), model, used, lambda v: f"{exact(v)} m per second"

    @staticmethod
    def _units_of_a_rate():
        minutes = random.randint(2, 12)
        rate = random.randint(2, 20)
        liters = minutes * rate
        facts = f"A tank's volume increases by {liters} liters during {minutes} minutes."
        question = "State the change for each minute, including its units and meaning."
        model = f"{liters} liters/{minutes} minutes"
        steps = [step("UNIT_ANALYSIS", "liters", "minutes", "liters per minute"),
                 step("D", liters, minutes, rate),
                 step("INTERPRET", f"{rate} liters per minute", "volume added each minute"),
                 step("M", rate, minutes, liters),
                 step("CHECK", "total volume change", unit(liters, "liter"))]
        answer = f"{rate} liters per minute; volume increases {rate} liters each minute"
        used = [f"{liters} liters", f"{minutes} minutes"]
        return facts, question, steps, answer, Fraction(rate), model, used, lambda v: f"{exact(v)} liters per minute"

    @staticmethod
    def _compare_rates_two_intervals():
        first_days, second_days = random.randint(2, 6), random.randint(2, 6)
        first_rate, second_rate = random.sample(range(1, 13), 2)
        start = random.randint(3, 30)
        middle = start + first_rate * first_days
        end = middle + second_rate * second_days
        final_day = first_days + second_days
        facts = (f"A plant-height record lists day 0: {start} cm; day {first_days}: "
                 f"{middle} cm; day {final_day}: {end} cm.")
        question = "During which interval did the plant grow faster on average?"
        model = (f"r1 = ({middle} − {start})/{first_days}; "
                 f"r2 = ({end} − {middle})/{second_days}")
        winner = f"days 0–{first_days}" if first_rate > second_rate else f"days {first_days}–{final_day}"
        steps = [step("TABLE_ROW", "day 0", unit(start, "cm")),
                 step("TABLE_ROW", f"day {first_days}", unit(middle, "cm")),
                 step("TABLE_ROW", f"day {final_day}", unit(end, "cm")),
                 step("S", middle, start, middle - start),
                 step("D", middle - start, first_days, first_rate),
                 step("S", end, middle, end - middle),
                 step("D", end - middle, second_days, second_rate),
                 step("CMP", first_rate, second_rate, ">" if first_rate > second_rate else "<"),
                 step("INTERPRET", winner, "faster average growth"),
                 step("CHECK", "rates", f"{first_rate} vs {second_rate} cm/day")]
        answer = f"{winner}; {first_rate} vs {second_rate} cm per day"
        used = [f"day 0: {start} cm", f"day {first_days}: {middle} cm", f"day {final_day}: {end} cm"]
        return facts, question, steps, answer, Fraction(max(first_rate, second_rate)), model, used, lambda v: f"{exact(v)} cm per day"

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
            extra = random.choice([value for value in range(701, 1101) if value not in occupied])
            problem = f"An unrelated roster contains {extra} membership cards. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} membership cards"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the direction and scale of change",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "quantities and units"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_rate_of_change_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
