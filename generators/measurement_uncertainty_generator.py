"""Compute exact tolerance and measurement-uncertainty intervals.

Variants: ``tolerance_interval``, ``within_tolerance``,
``sum_difference_propagation``, ``area_from_measured_sides``,
``percent_error``, and ``relative_uncertainty_rule``. Five shared-context
renderings and all four applied modifiers are supported. All values and
interval endpoints use exact ``Fraction`` arithmetic. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``INTERVAL``, ``PROPAGATE``, ``PCT_ERROR``, ``CMP``, ``A``, ``S``, ``M``,
``D``, ``CHECK``, and ``Z``.
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
VARIANTS = ("tolerance_interval", "within_tolerance",
            "sum_difference_propagation", "area_from_measured_sides",
            "percent_error", "relative_uncertainty_rule")
FRAMES = (
    "At {place}, {name} checks a measurement record. {facts} {question}",
    "{question} A record given to {name} at {place} states: {facts}",
    "For {name} at {place}, the measured quantities are these: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the measurement record from {place} that {name} is checking. "
    "{facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("lab", "workshop", "garden", "classroom", "business")
    for setting in CONTEXTS[key].settings
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _interval_text(low, high):
    return f"[{exact(low)}, {exact(high)}]"


class MeasurementUncertaintyGenerator(ProblemGenerator):
    """Generate exact worst-case interval and error calculations."""

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
    def _tolerance_interval():
        nominal = Fraction(random.randint(50, 500), 10)
        tolerance = Fraction(random.randint(1, 20), 10)
        low, high = nominal - tolerance, nominal + tolerance
        unit_name = random.choice(("cm", "g", "mL"))
        facts = (f"A part is specified as {exact(nominal)} ± "
                 f"{exact(tolerance)} {unit_name}.")
        question = "What closed interval contains every allowed value?"
        answer = f"{exact(low)} {unit_name} to {exact(high)} {unit_name}"
        model = f"x ∈ {_interval_text(low, high)} {unit_name}"
        steps = [step("S", exact(nominal), exact(tolerance), exact(low)),
                 step("A", exact(nominal), exact(tolerance), exact(high)),
                 step("INTERVAL", "allowed value", _interval_text(low, high)),
                 step("CHECK", f"center {exact(nominal)}",
                      f"half-width {exact(tolerance)}")]
        used = [f"nominal {exact(nominal)} {unit_name}",
                f"tolerance {exact(tolerance)} {unit_name}"]
        renderer = lambda value: unit(value, unit_name)
        return facts, question, steps, answer, nominal, model, used, renderer

    @staticmethod
    def _within_tolerance():
        nominal = Fraction(random.randint(50, 500), 10)
        tolerance = Fraction(random.randint(2, 20), 10)
        inside = random.choice((True, False))
        if inside:
            offset = Fraction(random.randint(0, int(tolerance * 10)), 10)
        else:
            offset = tolerance + Fraction(random.randint(1, 10), 10)
        measured = nominal + random.choice((-1, 1)) * offset
        difference = abs(measured - nominal)
        symbol = "≤" if inside else ">"
        verdict = "within tolerance" if inside else "outside tolerance"
        unit_name = random.choice(("cm", "g", "mL"))
        facts = (f"A target is {exact(nominal)} ± {exact(tolerance)} "
                 f"{unit_name}, and a part measures {exact(measured)} "
                 f"{unit_name}.")
        question = "Is the measured part within the allowed tolerance?"
        answer = (f"{verdict}; difference {exact(difference)} {unit_name} "
                  f"{symbol} {exact(tolerance)} {unit_name}")
        model = (f"abs({exact(measured)} − {exact(nominal)}) = "
                 f"{exact(difference)} {symbol} {exact(tolerance)}")
        steps = [step("S", exact(max(measured, nominal)),
                      exact(min(measured, nominal)), exact(difference)),
                 step("CMP", exact(difference), exact(tolerance), symbol),
                 step("INTERVAL", "allowed value",
                      _interval_text(nominal - tolerance,
                                     nominal + tolerance)),
                 step("CHECK", f"measured {exact(measured)}", verdict)]
        used = [f"target {exact(nominal)} {unit_name}",
                f"tolerance {exact(tolerance)} {unit_name}",
                f"measured {exact(measured)} {unit_name}"]
        renderer = lambda value: unit(value, unit_name)
        return facts, question, steps, answer, difference, model, used, renderer

    @staticmethod
    def _sum_difference_propagation():
        operation = random.choice(("sum", "difference"))
        first = Fraction(random.randint(80, 300), 10)
        second = Fraction(random.randint(20, 70), 10)
        first_u = Fraction(random.randint(1, 8), 10)
        second_u = Fraction(random.randint(1, 8), 10)
        first_low, first_high = first - first_u, first + first_u
        second_low, second_high = second - second_u, second + second_u
        total_u = first_u + second_u
        if operation == "sum":
            nominal = first + second
            low, high = first_low + second_low, first_high + second_high
            symbol, verb = "+", "added"
        else:
            nominal = first - second
            low, high = first_low - second_high, first_high - second_low
            symbol, verb = "−", "subtracted"
        facts = (f"Two lengths are {exact(first)} ± {exact(first_u)} cm and "
                 f"{exact(second)} ± {exact(second_u)} cm. The second is "
                 f"{verb} {'from the first' if operation == 'difference' else 'to the first'}.")
        question = "Give the worst-case interval for the resulting length."
        answer = (f"{exact(nominal)} ± {exact(total_u)} cm; "
                  f"{exact(low)} cm to {exact(high)} cm")
        model = (f"({exact(first)} ± {exact(first_u)}) {symbol} "
                 f"({exact(second)} ± {exact(second_u)})")
        steps = [step("INTERVAL", "first", _interval_text(first_low, first_high)),
                 step("INTERVAL", "second", _interval_text(second_low, second_high))]
        opcode = "A" if operation == "sum" else "S"
        if operation == "sum":
            steps += [step(opcode, exact(first_low), exact(second_low), exact(low)),
                      step(opcode, exact(first_high), exact(second_high), exact(high))]
        else:
            steps += [step(opcode, exact(first_low), exact(second_high), exact(low)),
                      step(opcode, exact(first_high), exact(second_low), exact(high))]
        steps += [step("A", exact(first_u), exact(second_u), exact(total_u)),
                  step("PROPAGATE", f"endpoint {operation}",
                       _interval_text(low, high)),
                  step("CHECK", f"center {exact(nominal)}",
                       f"half-width {exact(total_u)}")]
        used = [f"first {exact(first)} ± {exact(first_u)} cm",
                f"second {exact(second)} ± {exact(second_u)} cm"]
        renderer = lambda value: unit(value, "cm")
        return facts, question, steps, answer, nominal, model, used, renderer

    @staticmethod
    def _area_from_measured_sides():
        length = Fraction(random.randint(80, 200), 10)
        width = Fraction(random.randint(40, 120), 10)
        length_u = Fraction(random.randint(1, 5), 10)
        width_u = Fraction(random.randint(1, 4), 10)
        length_low, length_high = length - length_u, length + length_u
        width_low, width_high = width - width_u, width + width_u
        low, high = length_low * width_low, length_high * width_high
        nominal = length * width
        facts = (f"A rectangle measures {exact(length)} ± {exact(length_u)} cm "
                 f"by {exact(width)} ± {exact(width_u)} cm.")
        question = "Give the smallest and largest possible covered surface."
        answer = f"{exact(low)} cm² to {exact(high)} cm²"
        model = (f"A ∈ [{exact(length_low)} × {exact(width_low)}, "
                 f"{exact(length_high)} × {exact(width_high)}]")
        steps = [step("INTERVAL", "length",
                      _interval_text(length_low, length_high)),
                 step("INTERVAL", "width",
                      _interval_text(width_low, width_high)),
                 step("M", exact(length_low), exact(width_low), exact(low)),
                 step("M", exact(length_high), exact(width_high), exact(high)),
                 step("PROPAGATE", "min × min, max × max",
                      _interval_text(low, high)),
                 step("CHECK", "nominal area", exact(nominal))]
        used = [f"length {exact(length)} ± {exact(length_u)} cm",
                f"width {exact(width)} ± {exact(width_u)} cm"]
        renderer = lambda value: unit(value, "cm²")
        return facts, question, steps, answer, nominal, model, used, renderer

    @staticmethod
    def _percent_error():
        true_value = Fraction(random.randint(10, 200))
        percent = random.choice((1, 2, 5, 10))
        difference = true_value * Fraction(percent, 100)
        measured = true_value + random.choice((-1, 1)) * difference
        facts = (f"A reference value is {exact(true_value)} g, while a "
                 f"measurement gives {exact(measured)} g.")
        question = "What percent of the reference value is the absolute error?"
        answer = f"{percent}%"
        model = (f"abs({exact(measured)} − {exact(true_value)})/"
                 f"{exact(true_value)} × 100 = {percent}%")
        steps = [step("S", exact(max(measured, true_value)),
                      exact(min(measured, true_value)), exact(difference)),
                 step("D", exact(difference), exact(true_value),
                      exact(Fraction(percent, 100))),
                 step("M", exact(Fraction(percent, 100)), 100, percent),
                 step("PCT_ERROR",
                      f"abs({exact(measured)} − {exact(true_value)})/"
                      f"{exact(true_value)}", f"{percent}%"),
                 step("CHECK", "absolute error", exact(difference))]
        used = [f"reference {exact(true_value)} g",
                f"measured {exact(measured)} g"]
        return (facts, question, steps, answer, Fraction(percent), model, used,
                exact)

    @staticmethod
    def _relative_uncertainty_rule():
        operation = random.choice(("multiply", "divide"))
        first = random.randint(4, 30)
        second = random.randint(2, 15)
        first_pct = random.choice((1, 2, 3, 5))
        second_pct = random.choice((1, 2, 3, 5))
        combined_pct = first_pct + second_pct
        if operation == "multiply":
            value = Fraction(first * second)
            symbol, unit_name = "×", "cm²"
            quantity_text = f"{first} cm by {second} cm"
            opcode = "M"
        else:
            value = Fraction(first, second)
            symbol, unit_name = "÷", "m/s"
            quantity_text = f"{first} m over {second} s"
            opcode = "D"
        absolute = value * Fraction(combined_pct, 100)
        facts = (f"A result uses {quantity_text}. Their percentage "
                 f"uncertainties are {first_pct}% and {second_pct}%. For this "
                 "report, add the percentage uncertainties for multiplication "
                 "or division.")
        question = "Give the reported value, combined percentage, and absolute uncertainty."
        answer = (f"{exact(value)} ± {exact(absolute)} {unit_name} "
                  f"({combined_pct}%)")
        model = (f"{first} {symbol} {second} = {exact(value)}; "
                 f"u = {combined_pct}% × {exact(value)}")
        steps = [step(opcode, first, second, exact(value)),
                 step("A", first_pct, second_pct, combined_pct),
                 step("D", combined_pct, 100,
                      exact(Fraction(combined_pct, 100))),
                 step("M", exact(value), exact(Fraction(combined_pct, 100)),
                      exact(absolute)),
                 step("PROPAGATE", "add percentage uncertainties",
                      f"{combined_pct}%", exact(absolute)),
                 step("CHECK", "reported interval",
                      _interval_text(value - absolute, value + absolute))]
        used = [quantity_text, f"uncertainties {first_pct}% and {second_pct}%"]
        renderer = lambda item: unit(item, unit_name)
        return facts, question, steps, answer, value, model, used, renderer

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
            extra = random.choice([number for number in range(171, 471)
                                   if number not in occupied])
            problem = f"A nearby cabinet holds {extra} spare clips. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} spare clips"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "predict the central scale before computing the uncertainty",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "measurement and uncertainty relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_measurement_uncertainty_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
