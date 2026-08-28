"""Reason about scale, direction, thresholds, and signs before calculating.

Variants: ``dominant_term``, ``limiting_value``, ``direction_of_change``,
``doubling_effect_in_formula``, ``compare_growth_rates``, and
``sign_without_computing``. Five shared-context renderings and all four
applied modifiers are supported. Every qualitative label is paired with an
exact numerical check. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``DOMINANT``, ``LIMIT``, ``DIRECTION``,
``SIGN``, ``PERCENT_TO_DEC``, ``CMP``, ``A``, ``M``, ``D``, ``E``,
``CHECK``, and ``Z``.
"""
import math
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("dominant_term", "limiting_value", "direction_of_change",
            "doubling_effect_in_formula", "compare_growth_rates",
            "sign_without_computing")
FRAMES = (
    "At {place}, {name} studies a quantitative pattern. {facts} {question}",
    "{question} A record given to {name} at {place} states: {facts}",
    "For {name} at {place}, the pattern is described this way: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the quantitative pattern from {place} that {name} is checking. "
    "{facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("classroom", "business", "garden", "trip", "lab", "workshop")
    for setting in CONTEXTS[key].settings
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


class QualitativeReasoningGenerator(ProblemGenerator):
    """Generate exact checks for qualitative quantitative reasoning."""

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
    def _dominant_term():
        coefficient = random.randint(10, 250)
        check_n = 2 * coefficient
        square = check_n ** 2
        multiple = coefficient * check_n
        facts = (f"Two outputs at input n are n² and {coefficient}n. "
                 f"{random.choice(NAMES)} wants to know which is larger once n "
                 "passes their positive meeting point.")
        question = "Which output is then larger, and what is the exact threshold?"
        answer = (f"n²; larger for n > {coefficient} (at n = {check_n}: "
                  f"{square} vs {multiple})")
        model = f"n² > {coefficient}n when n > {coefficient}"
        steps = [step("REWRITE", f"n² = {coefficient}n",
                      f"n(n - {coefficient}) = 0"),
                 step("ZERO_PRODUCT", f"n(n - {coefficient}) = 0",
                      f"n = 0 or n = {coefficient}"),
                 step("DOMINANT", "n²", f"n > {coefficient}"),
                 step("E", check_n, 2, square),
                 step("M", coefficient, check_n, multiple),
                 step("CMP", square, multiple, ">"),
                 step("CHECK", f"n = {check_n}",
                      f"{square} vs {multiple}")]
        used = ["output n²", f"output {coefficient}n",
                f"meeting point {coefficient}"]
        return (facts, question, steps, answer, Fraction(coefficient), model,
                used, exact)

    @staticmethod
    def _limiting_value():
        leading = random.randint(2, 9)
        offset = random.randint(1, 15)
        denominator_offset = random.randint(1, 12)
        while offset == leading * denominator_offset:
            offset = random.randint(1, 15)
        check_n = random.choice((100, 200, 500, 1000))
        numerator = leading * check_n + offset
        denominator = check_n + denominator_offset
        check_value = Fraction(numerator, denominator)
        approximation = f"{float(check_value):.3f}"
        expression = f"({leading}n + {offset})/(n + {denominator_offset})"
        facts = (f"A changing ratio is {expression}. The input n keeps growing "
                 f"while the constants stay fixed, and a check uses n = "
                 f"{check_n}.")
        question = "What number does the ratio approach, and how does a large input check it?"
        answer = (f"{leading}; at n = {check_n}, {numerator}/{denominator} "
                  f"≈ {approximation}")
        model = f"{expression} → {leading} as n grows"
        steps = [step("M", leading, check_n, leading * check_n),
                 step("A", leading * check_n, offset, numerator),
                 step("A", check_n, denominator_offset, denominator),
                 step("D", numerator, denominator, exact(check_value)),
                 step("LIMIT", expression, leading, "leading coefficients"),
                 step("CHECK", f"n = {check_n}",
                      f"{numerator}/{denominator} ≈ {approximation}")]
        used = [f"leading value {leading}", f"offsets {offset}, {denominator_offset}"]
        return (facts, question, steps, answer, Fraction(leading), model, used,
                exact)

    @staticmethod
    def _direction_of_change():
        years = random.randint(2, 4)
        first_rate, second_rate = sorted(random.sample((5, 10, 20, 25, 40, 50), 2))
        if random.choice((True, False)):
            first_rate, second_rate = second_rate, first_rate
        first_factor = Fraction(100 + first_rate, 100)
        second_factor = Fraction(100 + second_rate, 100)
        cents_quantum = math.lcm((first_factor ** years).denominator,
                                 (second_factor ** years).denominator)
        principal_cents = cents_quantum * random.randint(
            max(1, 5000 // cents_quantum),
            max(2, 25000 // cents_quantum))
        principal = Fraction(principal_cents, 100)
        first_value = principal * first_factor ** years
        second_value = principal * second_factor ** years
        direction = "increases" if second_value > first_value else "decreases"
        facts = (f"An account starts with {money(principal)} and changes each "
                 f"year by the same percentage of its current balance. Over "
                 f"{years} years, the annual change shifts from {first_rate}% "
                 f"to {second_rate}%.")
        question = "In which direction does the ending balance move, and what exact balances confirm it?"
        answer = (f"{direction}; {money(first_value)} → {money(second_value)} "
                  f"when the annual change goes {first_rate}% → {second_rate}%")
        model = (f"A1={exact(principal)}*(1+{first_rate}/100)^{years}; "
                 f"A2={exact(principal)}*(1+{second_rate}/100)^{years}")
        steps = [step("PERCENT_TO_DEC", f"{first_rate}%", exact(first_factor - 1)),
                 step("A", 1, exact(first_factor - 1), exact(first_factor)),
                 step("E", exact(first_factor), years,
                      exact(first_factor ** years)),
                 step("M", exact(principal), exact(first_factor ** years),
                      exact(first_value)),
                 step("PERCENT_TO_DEC", f"{second_rate}%",
                      exact(second_factor - 1)),
                 step("A", 1, exact(second_factor - 1), exact(second_factor)),
                 step("E", exact(second_factor), years,
                      exact(second_factor ** years)),
                 step("M", exact(principal), exact(second_factor ** years),
                      exact(second_value)),
                 step("DIRECTION", "ending balance", direction,
                      f"{money(first_value)} → {money(second_value)}")]
        used = [f"start {money(principal)}", f"{years} years",
                f"rates {first_rate}% and {second_rate}%"]
        return (facts, question, steps, answer, second_value, model, used, money)

    @staticmethod
    def _doubling_effect_in_formula():
        family = random.choice(("square", "cube", "inverse"))
        if family == "square":
            old = random.randint(2, 15)
            new = 2 * old
            old_value, new_value = old ** 2, new ** 2
            facts = (f"A square garden changes from side length {old} m to "
                     f"side length {new} m.")
            question = "By what factor does its covered surface change, and what values verify it?"
            effect = "multiplies by 4"
            old_text, new_text = unit(old_value, "m²"), unit(new_value, "m²")
            model = f"q1={old}²={old_value}; q2={new}²={new_value}"
            steps = [step("E", old, 2, old_value),
                     step("E", new, 2, new_value),
                     step("D", new_value, old_value, 4)]
            renderer = lambda value: unit(value, "m²")
        elif family == "cube":
            old = random.randint(2, 10)
            new = 2 * old
            old_value, new_value = old ** 3, new ** 3
            facts = (f"A cube-shaped tank changes from edge length {old} m to "
                     f"edge length {new} m.")
            question = "By what factor does its capacity change, and what values verify it?"
            effect = "multiplies by 8"
            old_text, new_text = unit(old_value, "m³"), unit(new_value, "m³")
            model = f"q1={old}³={old_value}; q2={new}³={new_value}"
            steps = [step("E", old, 3, old_value),
                     step("E", new, 3, new_value),
                     step("D", new_value, old_value, 8)]
            renderer = lambda value: unit(value, "m³")
        else:
            old = random.randrange(20, 81, 5)
            new = 2 * old
            old_time = random.randint(2, 8)
            distance = old * old_time
            new_time = Fraction(distance, new)
            old_value, new_value = Fraction(old_time), new_time
            facts = (f"A vehicle covers a fixed {distance} km route. Its speed "
                     f"changes from {old} km/h to {new} km/h.")
            question = "By what factor does its travel time change, and what times verify it?"
            effect = "multiplies by 1/2"
            old_text, new_text = unit(old_value, "hour"), unit(new_value, "hour")
            model = f"t1={distance}/{old}={exact(old_value)}; t2={distance}/{new}={exact(new_value)}"
            steps = [step("D", distance, old, exact(old_value)),
                     step("D", distance, new, exact(new_value)),
                     step("D", exact(new_value), exact(old_value), "1/2")]
            renderer = lambda value: unit(value, "hour")
        answer = f"{effect}; {old_text} → {new_text}"
        steps += [step("DIRECTION", "result after doubling", effect,
                       f"{old_text} → {new_text}"),
                  step("CHECK", "new/old", effect.split("by ", 1)[1])]
        used = [f"old input {old}", f"new input {new}",
                f"old result {old_text}"]
        return (facts, question, steps, answer, Fraction(new_value), model,
                used, renderer)

    @staticmethod
    def _compare_growth_rates():
        while True:
            base = random.choice((2, 3, 4))
            power = random.choice((2, 3))
            coefficient = random.randint(2, 8)
            upper = random.choice((25, 30, 35, 40))
            comparisons = [base ** n > coefficient * n ** power
                           for n in range(1, upper + 1)]
            thresholds = [n for n in range(1, upper + 1)
                          if all(comparisons[n - 1:])]
            if thresholds and 2 <= thresholds[0] < upper:
                threshold = thresholds[0]
                break
        first_value = base ** threshold
        second_power = threshold ** power
        second_value = coefficient * second_power
        facts = (f"For integer inputs n from 1 through {upper}, two sequences "
                 f"give {base}^n and {coefficient}n^{power}.")
        question = "From which input onward does the first remain larger through the stated range?"
        answer = (f"{base}^n; from n = {threshold} through {upper} "
                  f"(at n = {threshold}: {first_value} vs {second_value})")
        model = (f"{base}^n > {coefficient}n^{power} for "
                 f"{threshold} ≤ n ≤ {upper}")
        steps = [step("E", base, threshold, first_value),
                 step("E", threshold, power, second_power),
                 step("M", coefficient, second_power, second_value),
                 step("CMP", first_value, second_value, ">"),
                 step("DOMINANT", f"{base}^n", f"n = {threshold} through {upper}"),
                 step("CHECK", f"n = {threshold}",
                      f"{first_value} vs {second_value}")]
        used = [f"range 1 to {upper}", f"sequence {base}^n",
                f"sequence {coefficient}n^{power}"]
        return (facts, question, steps, answer, Fraction(threshold), model,
                used, exact)

    @staticmethod
    def _sign_without_computing():
        count = random.choice((3, 4, 5))
        magnitudes = random.sample(range(2, 13), count)
        negative_count = random.randint(1, count - 1)
        signs = [-1] * negative_count + [1] * (count - negative_count)
        random.shuffle(signs)
        factors = [sign * magnitude for sign, magnitude in zip(signs, magnitudes)]
        product = 1
        for factor in factors:
            product *= factor
        label = "positive" if product > 0 else "negative"
        expression = " × ".join(f"({factor})" if factor < 0 else str(factor)
                                for factor in factors)
        facts = f"A recorded product is {expression}."
        question = "Is its result positive or negative, and what exact product verifies the sign?"
        answer = f"{label}; {expression} = {product}"
        sign_value = -1 if negative_count % 2 else 1
        model = f"negative-factor count = {negative_count}; sign = {sign_value}"
        steps = [step("SIGN", "negative factors", negative_count, label)]
        running = factors[0]
        for factor in factors[1:]:
            steps.append(step("M", running, factor, running * factor))
            running *= factor
        steps.append(step("CHECK", expression, product, label))
        used = [f"factors {expression}"]
        return (facts, question, steps, answer, Fraction(product), model, used,
                exact)

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
            extra = random.choice([number for number in range(131, 431)
                                   if number not in occupied])
            problem = f"A nearby cabinet contains {extra} old folders. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} old folders"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "predict the direction or scale before evaluating the check",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "relationship supporting the qualitative claim"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_qualitative_reasoning_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
