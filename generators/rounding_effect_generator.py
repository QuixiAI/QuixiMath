"""Expose how rounding choices change ranges, estimates, and totals.

Variants: ``true_range_of_display``, ``round_before_vs_after``,
``front_end_estimate``, ``leading_digit_estimate``, and
``accumulated_rounding``. Five shared-context renderings and all four applied
modifiers are supported. All decimals are constructed and rounded with exact
``Fraction`` arithmetic. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``TRUE_RANGE``, ``ROUND``, ``FLOOR``,
``A``, ``S``, ``M``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("true_range_of_display", "round_before_vs_after",
            "front_end_estimate", "leading_digit_estimate",
            "accumulated_rounding")
FRAMES = (
    "At {place}, {name} checks the effect of a recorded approximation. {facts} {question}",
    "{question} A record given to {name} at {place} states: {facts}",
    "For {name} at {place}, the numerical record is this: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the numerical record from {place} that {name} is checking. "
    "{facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("lab", "shop", "classroom", "business", "workshop", "garden")
    for setting in CONTEXTS[key].settings
)
MEASUREMENTS = (("kg", "mass", "m"), ("cm", "length", "l"),
                ("L", "volume", "v"))


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _round_to(value, increment):
    """Round nonnegative ``value`` to ``increment`` with halves upward."""
    value, increment = Fraction(value), Fraction(increment)
    scaled = value / increment
    whole, remainder = divmod(scaled.numerator, scaled.denominator)
    if 2 * remainder >= scaled.denominator:
        whole += 1
    return whole * increment


def _fixed(value, places):
    value = Fraction(value)
    scale = 10 ** places
    scaled = value * scale
    if scaled.denominator != 1:
        raise ValueError(f"{value} cannot be rendered in {places} places")
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _round_ten(value):
    return int(_round_to(Fraction(value), 10))


class RoundingEffectGenerator(ProblemGenerator):
    """Generate exact examples where the point of rounding matters."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _true_range_of_display():
        places = random.choice((0, 1, 2))
        increment = Fraction(1, 10 ** places)
        ticks = random.randint(15, 900)
        display = ticks * increment
        half = increment / 2
        low, high = display - half, display + half
        unit_name, quantity, variable = random.choice(MEASUREMENTS)
        display_text = _fixed(display, places)
        increment_text = _fixed(increment, places)
        endpoint_places = places + 1
        low_text, high_text = (_fixed(low, endpoint_places),
                               _fixed(high, endpoint_places))
        facts = (f"A device shows {display_text} {unit_name}, rounded to the "
                 f"nearest {increment_text} {unit_name}.")
        question = f"What half-open interval can contain the true {quantity}?"
        answer = (f"{low_text} {unit_name} ≤ {variable} < {high_text} "
                  f"{unit_name}")
        model = f"{variable} ∈ [{low_text}, {high_text}) {unit_name}"
        steps = [step("TRUE_RANGE",
                      f"{display_text} to nearest {increment_text} {unit_name}",
                      f"[{low_text}, {high_text})"),
                 step("CHECK", f"half increment {exact(half)}",
                      f"{display_text} ± {exact(half)}")]
        used = [f"display {display_text} {unit_name}",
                f"increment {increment_text} {unit_name}"]
        renderer = lambda value: unit(value, unit_name)
        return facts, question, steps, answer, display, model, used, renderer

    @staticmethod
    def _round_before_vs_after():
        while True:
            first = Fraction(random.randint(105, 995), 100)
            second = Fraction(random.randint(105, 995), 100)
            first_rounded = _round_to(first, Fraction(1, 10))
            second_rounded = _round_to(second, Fraction(1, 10))
            rounded_first_sum = first_rounded + second_rounded
            exact_sum = first + second
            rounded_after = _round_to(exact_sum, Fraction(1, 10))
            difference = abs(rounded_first_sum - rounded_after)
            if difference:
                break
        facts = (f"Two measurements are {_fixed(first, 2)} and "
                 f"{_fixed(second, 2)}. Results are reported to the nearest "
                 "0.1.")
        question = "Compare rounding each measurement first with adding exactly and rounding once."
        answer = (f"{_fixed(rounded_after, 1)}; rounding first gives "
                  f"{_fixed(rounded_first_sum, 1)}, off by "
                  f"{_fixed(difference, 1)}")
        model = (f"round({_fixed(first, 2)} + {_fixed(second, 2)}, 0.1) = "
                 f"{_fixed(rounded_after, 1)}")
        steps = [step("ROUND", _fixed(first, 2), "nearest 0.1",
                      _fixed(first_rounded, 1)),
                 step("ROUND", _fixed(second, 2), "nearest 0.1",
                      _fixed(second_rounded, 1)),
                 step("A", _fixed(first_rounded, 1),
                      _fixed(second_rounded, 1),
                      _fixed(rounded_first_sum, 1)),
                 step("A", _fixed(first, 2), _fixed(second, 2),
                      _fixed(exact_sum, 2)),
                 step("ROUND", _fixed(exact_sum, 2), "nearest 0.1",
                      _fixed(rounded_after, 1)),
                 step("S", _fixed(max(rounded_first_sum, rounded_after), 1),
                      _fixed(min(rounded_first_sum, rounded_after), 1),
                      _fixed(difference, 1)),
                 step("CHECK", "round once vs round twice",
                      f"{_fixed(rounded_after, 1)} vs "
                      f"{_fixed(rounded_first_sum, 1)}")]
        used = [f"measurement {_fixed(first, 2)}",
                f"measurement {_fixed(second, 2)}", "nearest 0.1"]
        return facts, question, steps, answer, rounded_after, model, used, exact

    @staticmethod
    def _front_end_estimate():
        values = random.sample(range(125, 996), 3)
        fronts = [(value // 100) * 100 for value in values]
        estimate = sum(fronts)
        total = sum(values)
        value_text = ", ".join(map(str, values))
        front_text = " + ".join(map(str, fronts))
        facts = (f"A list of counts is {value_text}. Keep only each hundreds "
                 "place for an initial size estimate, then total the exact counts.")
        question = "What estimate comes first, and what exact total checks its scale?"
        answer = f"about {estimate}; exact {total}"
        model = f"{front_text} = {estimate}; exact sum = {total}"
        steps = [step("ESTIMATE", front_text, estimate)]
        for value, front in zip(values, fronts):
            steps.append(step("FLOOR", value, "lower hundred", front))
        estimate_running = fronts[0]
        for front in fronts[1:]:
            steps.append(step("A", estimate_running, front,
                              estimate_running + front))
            estimate_running += front
        running = values[0]
        for value in values[1:]:
            steps.append(step("A", running, value, running + value))
            running += value
        steps.append(step("ESTIMATE_CHECK", estimate, total,
                          "same hundreds scale"))
        used = [f"counts {value_text}"]
        return (facts, question, steps, answer, Fraction(total), model, used,
                exact)

    @staticmethod
    def _leading_digit_estimate():
        first, second = random.randint(21, 99), random.randint(21, 99)
        first_rounded, second_rounded = _round_ten(first), _round_ten(second)
        estimate = first_rounded * second_rounded
        product = first * second
        facts = (f"A product is {first} × {second}. Replace each factor by its "
                 "nearest multiple of ten for an initial size estimate.")
        question = "What estimate comes first, and what exact product verifies it?"
        answer = f"about {estimate}; exact {product}"
        model = f"{first} × {second} ≈ {first_rounded} × {second_rounded} = {estimate}"
        steps = [step("ESTIMATE", f"{first} ≈ {first_rounded}, "
                      f"{second} ≈ {second_rounded}", estimate),
                 step("ROUND", first, "nearest 10", first_rounded),
                 step("ROUND", second, "nearest 10", second_rounded),
                 step("M", first, second, product),
                 step("ESTIMATE_CHECK", estimate, product,
                      "same product scale")]
        used = [f"factor {first}", f"factor {second}"]
        return (facts, question, steps, answer, Fraction(product), model, used,
                exact)

    @staticmethod
    def _accumulated_rounding():
        while True:
            count = random.randint(3, 20)
            per_item = Fraction(random.randint(105, 999), 100)
            rounded_item = _round_to(per_item, Fraction(1, 10))
            rounded_each_total = count * rounded_item
            exact_total = count * per_item
            rounded_total = _round_to(exact_total, Fraction(1, 10))
            difference = abs(rounded_each_total - rounded_total)
            if difference:
                break
        facts = (f"There are {count} identical lengths of "
                 f"{_fixed(per_item, 2)} cm. A total must be reported to the "
                 "nearest 0.1 cm.")
        question = "Compare rounding every length first with multiplying exactly and rounding once."
        answer = (f"{_fixed(rounded_total, 1)} cm; rounding each gives "
                  f"{_fixed(rounded_each_total, 1)} cm, off by "
                  f"{_fixed(difference, 1)} cm")
        model = (f"round({count} × {_fixed(per_item, 2)}, 0.1) = "
                 f"{_fixed(rounded_total, 1)} cm")
        steps = [step("ROUND", _fixed(per_item, 2), "nearest 0.1",
                      _fixed(rounded_item, 1)),
                 step("M", count, _fixed(rounded_item, 1),
                      _fixed(rounded_each_total, 1)),
                 step("M", count, _fixed(per_item, 2),
                      _fixed(exact_total, 2)),
                 step("ROUND", _fixed(exact_total, 2), "nearest 0.1",
                      _fixed(rounded_total, 1)),
                 step("S", _fixed(max(rounded_each_total, rounded_total), 1),
                      _fixed(min(rounded_each_total, rounded_total), 1),
                      _fixed(difference, 1)),
                 step("CHECK", "round once vs every item",
                      f"{_fixed(rounded_total, 1)} vs "
                      f"{_fixed(rounded_each_total, 1)}")]
        used = [f"{count} lengths", f"each {_fixed(per_item, 2)} cm",
                "nearest 0.1 cm"]
        renderer = lambda value: unit(value, "cm")
        return (facts, question, steps, answer, rounded_total, model, used,
                renderer)

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(
            variant)
        problem = _render(facts, question)

        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(151, 451)
                                   if number not in occupied])
            problem = f"A nearby log lists {extra} old entries. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} old entries"))
        elif (modifier == "estimate_first" and
              variant not in ("front_end_estimate", "leading_digit_estimate")):
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "predict the rounded scale before evaluating exactly",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "rounding point and exact relationship"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_rounding_effect_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
