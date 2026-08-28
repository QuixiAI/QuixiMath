"""Count and apply measurement-reporting digits with exact arithmetic.

Variants: ``count_sig_figs``, ``round_to_sig_figs``,
``multiply_divide_rule``, ``add_subtract_rule``, and
``scientific_notation_measurement``. Five shared-context renderings and all
four applied modifiers are supported. Rules needed for multiplication,
division, addition, and subtraction are stated in the problem. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``SIGFIG``, ``ROUND_SF``, ``ROUND``, ``A``, ``S``, ``M``, ``D``, ``E``,
``CHECK``, and ``Z``.
"""
import random
import re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact,
                            select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("count_sig_figs", "round_to_sig_figs",
            "multiply_divide_rule", "add_subtract_rule",
            "scientific_notation_measurement")
FRAMES = (
    "At {place}, {name} checks a reported measurement. {facts} {question}",
    "{question} A measurement given to {name} at {place} states: {facts}",
    "For {name} at {place}, the measurement record is this: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the measurement from {place} that {name} is checking. {facts} "
    "{question}",
)
PLACES = tuple(
    setting
    for key in ("lab", "classroom", "workshop", "garden", "business")
    for setting in CONTEXTS[key].settings
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _sig_count(token):
    """Count significant digits in an ordinary or scientific numeral."""
    text = token.strip().lstrip("+-")
    if "×" in text:
        text = text.split("×", 1)[0].strip()
    if "." in text:
        digits = text.replace(".", "").lstrip("0")
        return len(digits)
    digits = text.lstrip("0").rstrip("0")
    return len(digits)


def _round_sig(value, count):
    """Round positive Decimal ``value`` to ``count`` significant digits."""
    value = Decimal(value)
    quantum = Decimal(1).scaleb(value.adjusted() - count + 1)
    rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
    places = max(0, count - rounded.adjusted() - 1)
    return f"{rounded:.{places}f}"


def _decimal_fraction(value):
    return Fraction(Decimal(value))


class SignificantFiguresGenerator(ProblemGenerator):
    """Generate exact measurement-digit interpretation and rounding tasks."""

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
    def _count_sig_figs():
        family = random.choice(("leading", "decimal", "whole_decimal"))
        if family == "leading":
            leading_zeros = "0" * random.randint(1, 4)
            core = str(random.randint(1, 9)) + "".join(
                str(random.randint(0, 9)) for _ in range(random.randint(1, 3)))
            trailing = "0" * random.randint(0, 2)
            token = f"0.{leading_zeros}{core}{trailing}"
            reason = ("leading zeros not significant; displayed trailing "
                      "zeros after the decimal are")
        elif family == "decimal":
            whole = random.randint(1, 99)
            fraction = "".join(str(random.randint(0, 9))
                               for _ in range(random.randint(1, 3)))
            fraction += "0" * random.randint(0, 2)
            token = f"{whole}.{fraction}"
            reason = "all displayed digits from the first nonzero digit count"
        else:
            whole = random.randint(1, 999)
            zeros = "0" * random.randint(1, 3)
            token = f"{whole}.{zeros}"
            reason = "the decimal point makes the displayed trailing zeros significant"
        count = _sig_count(token)
        facts = f"A measurement is written as {token}."
        question = "How many significant figures are displayed?"
        answer = str(count)
        model = f"significant-digit count({token}) = {count}"
        steps = [step("SIGFIG", token, count, reason),
                 step("CHECK", "displayed significant digits", count)]
        used = [f"measurement {token}"]
        return (facts, question, steps, answer, Fraction(count), model, used,
                exact)

    @staticmethod
    def _round_to_sig_figs():
        while True:
            raw = Decimal(random.randint(101, 9999)) / Decimal(100)
            token = f"{raw:.2f}"
            count = random.choice((2, 3))
            rounded = _round_sig(raw, count)
            if _sig_count(rounded) == count and rounded != token:
                break
        facts = f"A measured value is {token} cm."
        question = f"Report it to {count} significant figures."
        answer = f"{rounded} cm"
        model = f"{token} cm → {rounded} cm ({count} significant figures)"
        steps = [step("SIGFIG", token, _sig_count(token),
                      "count from the first nonzero digit"),
                 step("ROUND_SF", token, count, rounded),
                 step("CHECK", f"{count} significant figures", rounded)]
        used = [f"value {token} cm", f"target {count} figures"]
        return (facts, question, steps, answer, _decimal_fraction(rounded), model,
                used, exact)

    @staticmethod
    def _multiply_divide_rule():
        operation = random.choice(("multiply", "divide"))
        while True:
            if operation == "multiply":
                first = f"{Decimal(random.randint(12, 99)) / Decimal(10):.1f}"
                second = f"{Decimal(random.randint(120, 999)) / Decimal(100):.2f}"
                raw_fraction = (_decimal_fraction(first) *
                                _decimal_fraction(second))
                raw_value = Decimal(first) * Decimal(second)
                symbol, unit_name = "×", "cm²"
                quantity_text = f"{first} cm × {second} cm"
            else:
                first = f"{Decimal(random.randint(101, 999)) / Decimal(10):.1f}"
                second = f"{Decimal(random.randint(12, 99)) / Decimal(10):.1f}"
                raw_fraction = (_decimal_fraction(first) /
                                _decimal_fraction(second))
                raw_value = (Decimal(raw_fraction.numerator) /
                             Decimal(raw_fraction.denominator))
                symbol, unit_name = "÷", "m/s"
                quantity_text = f"{first} m ÷ {second} s"
            target = min(_sig_count(first), _sig_count(second))
            rounded = _round_sig(raw_value, target)
            if _sig_count(rounded) == target:
                break
        rule_word = "multiplying" if operation == "multiply" else "dividing"
        facts = (f"Two measurements give {quantity_text}. When "
                 f"{rule_word} measurements, report the result to the fewer "
                 "significant figures shown by either input.")
        question = "What reported result follows?"
        answer = f"{rounded} {unit_name}"
        model = f"{first} {symbol} {second} → {rounded} {unit_name}"
        opcode = "M" if operation == "multiply" else "D"
        raw_text = exact(raw_fraction)
        steps = [step("SIGFIG", first, _sig_count(first), "first input"),
                 step("SIGFIG", second, _sig_count(second), "second input"),
                 step(opcode, first, second, raw_text),
                 step("ROUND_SF", raw_text, target, rounded),
                 step("CHECK", f"fewer count {target}", rounded)]
        used = [f"input {first} {'cm' if operation == 'multiply' else 'm'}",
                f"input {second} {'cm' if operation == 'multiply' else 's'}"]
        return (facts, question, steps, answer, _decimal_fraction(rounded), model,
                used, exact)

    @staticmethod
    def _add_subtract_rule():
        operation = random.choice(("add", "subtract"))
        first = Decimal(random.randint(200, 999)) / Decimal(100)
        second = Decimal(random.randint(20, 99)) / Decimal(10)
        if operation == "subtract" and first <= second:
            first = second + Decimal("5.25")
        first_text, second_text = f"{first:.2f}", f"{second:.1f}"
        raw_value = first + second if operation == "add" else first - second
        rounded = raw_value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        rounded_text = f"{rounded:.1f}"
        symbol = "+" if operation == "add" else "−"
        verb = "adding" if operation == "add" else "subtracting"
        facts = (f"Two measurements give {first_text} {symbol} {second_text} g. "
                 f"When {verb} measurements, report to the fewest decimal "
                 "places shown by either input.")
        question = "What reported result follows?"
        answer = f"{rounded_text} g"
        model = f"{first_text} {symbol} {second_text} → {rounded_text} g"
        raw_text = f"{raw_value:.2f}"
        opcode = "A" if operation == "add" else "S"
        steps = [step("ROUND", first_text, "2 decimal places", first_text),
                 step("ROUND", second_text, "1 decimal place", second_text),
                 step(opcode, first_text, second_text, raw_text),
                 step("ROUND", raw_text, "1 decimal place", rounded_text),
                 step("CHECK", "fewest decimal places 1", rounded_text)]
        used = [f"measurement {first_text} g", f"measurement {second_text} g"]
        return (facts, question, steps, answer, _decimal_fraction(rounded), model,
                used, exact)

    @staticmethod
    def _scientific_notation_measurement():
        count = random.randint(3, 6)
        fractional = "".join(str(random.randint(0, 9)) for _ in range(count - 1))
        mantissa = f"{random.randint(1, 9)}.{fractional}"
        exponent = -random.randint(2, 6)
        unit_name = random.choice(("m", "g", "L"))
        ordinary_decimal = Decimal(mantissa) * (Decimal(10) ** exponent)
        ordinary = format(ordinary_decimal, "f")
        facts = (f"A measurement is written as {mantissa} × 10^{exponent} "
                 f"{unit_name}.")
        question = "How many significant figures are shown, and what is the ordinary decimal form?"
        answer = f"{count} significant figures; {ordinary} {unit_name}"
        model = f"{mantissa} × 10^{exponent} = {ordinary} {unit_name}"
        power = Fraction(10) ** exponent
        steps = [step("SIGFIG", mantissa, count,
                      "the power of ten does not change the digit count"),
                 step("E", 10, exponent, exact(power)),
                 step("M", mantissa, exact(power),
                      exact(_decimal_fraction(ordinary))),
                 step("CHECK", "ordinary decimal", ordinary)]
        used = [f"mantissa {mantissa}", f"power 10^{exponent}"]
        return (facts, question, steps, answer, _decimal_fraction(ordinary), model,
                used, exact)

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
            extra = random.choice([number for number in range(161, 461)
                                   if number not in occupied])
            problem = f"A nearby shelf holds {extra} sealed vials. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} sealed vials"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "predict the reported scale before applying the stated rule",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "measurement reporting relationship"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_significant_figures_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
