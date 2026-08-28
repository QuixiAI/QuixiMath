"""Translate exact relationships among words, equations, and text tables.

Variants: ``words_to_equation``, ``equation_to_words``,
``table_to_equation_linear``, ``table_to_equation_exponential``,
``equation_to_table``, ``graph_features_to_equation``, ``intercept_meaning``,
and ``which_representation_matches``. Five context frames and all four
applied modifiers are supported. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``TABLE_ROW``, ``TABLE_DIFF``,
``TABLE_RATIO``, ``PATTERN``, ``TRANSLATE``, ``INTERPRET``, ``OPTION``,
``MATCH_REP``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, money, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("words_to_equation", "equation_to_words",
            "table_to_equation_linear", "table_to_equation_exponential",
            "equation_to_table", "graph_features_to_equation",
            "intercept_meaning", "which_representation_matches")
FRAMES = (
    "At {place}, {name} compares representations. {facts} {question}",
    "{question} A record for {name} from {place} states: {facts}",
    "For {name}'s report at {place}: {facts} {question}",
    "A note from {place}, checked by {name}, gives: {facts} {question}",
    "Consider the representation {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


def _linear_equation(rate, initial):
    return f"y = {rate}x + {initial}"


class RepresentationTranslationGenerator(ProblemGenerator):
    """Generate eight exact translations among textual representations."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _words_to_equation():
        initial, rate = random.randint(5, 80), random.randint(2, 30)
        facts = (f"A tank begins with {initial} liters and receives {rate} liters "
                 "each minute. Let x be elapsed minutes and y be liters in the tank.")
        question = "Write the relationship between x and y."
        equation = _linear_equation(rate, initial)
        steps = [step("INTERPRET", initial, "value when x = 0"),
                 step("INTERPRET", rate, "increase for each 1 in x"),
                 step("TRANSLATE", "words", equation),
                 step("M", rate, 1, rate), step("A", initial, rate, initial + rate),
                 step("CHECK", "x = 1", f"y = {initial + rate}")]
        answer = equation
        used = [f"starts {initial} liters", f"adds {rate} liters each minute", "x minutes", "y liters"]
        return facts, question, steps, answer, Fraction(initial + rate), equation, used, str

    @staticmethod
    def _equation_to_words():
        initial, rate = random.randint(5, 80), random.randint(2, 30)
        equation = _linear_equation(rate, initial)
        facts = (f"The relationship {equation} uses x for hours worked and y for "
                 "total dollars earned.")
        question = "Describe what the two numbers mean."
        steps = [step("INTERPRET", initial, "starting payment at x = 0"),
                 step("INTERPRET", rate, "dollars added per hour"),
                 step("TRANSLATE", "equation", "payment description"),
                 step("CHECK", "units", "starting dollars and dollars per hour")]
        answer = f"starts with ${initial}; earns ${rate} per hour"
        used = [equation, "x hours", "y dollars"]
        return facts, question, steps, answer, Fraction(rate), equation, used, lambda v: f"${v} per hour"

    @staticmethod
    def _table_to_equation_linear():
        initial, difference = random.randint(2, 80), random.randint(2, 35)
        values = [initial + difference * x for x in range(4)]
        facts = "A table lists " + ", ".join(f"({x}, {value})" for x, value in enumerate(values)) + "."
        question = "Is the relationship linear or exponential, and what relationship gives y from x?"
        equation = _linear_equation(difference, initial)
        steps = [step("TABLE_DIFF", index, f"+{values[index] - values[index - 1]}")
                 for index in range(1, 4)]
        steps += [step("PATTERN", "linear", "constant difference"),
                  step("TRANSLATE", "table", equation),
                  step("M", difference, 3, difference * 3),
                  step("A", initial, difference * 3, values[3]),
                  step("CHECK", "x = 3", values[3])]
        answer = f"linear; common difference {difference}; {equation}"
        used = [f"points {list(zip(range(4), values))}"]
        return facts, question, steps, answer, Fraction(values[3]), equation, used, str

    @staticmethod
    def _table_to_equation_exponential():
        initial, ratio = random.randint(2, 20), random.randint(2, 5)
        values = [initial * ratio ** x for x in range(4)]
        facts = "A table lists " + ", ".join(f"({x}, {value})" for x, value in enumerate(values)) + "."
        question = "Is the relationship linear or exponential, and what relationship gives y from x?"
        equation = f"y = {initial}·{ratio}^x"
        steps = [step("TABLE_RATIO", index, ratio) for index in range(1, 4)]
        steps += [step("PATTERN", "exponential", "constant ratio"),
                  step("TRANSLATE", "table", equation),
                  step("M", values[2], ratio, values[3]),
                  step("CHECK", "x = 3", values[3])]
        answer = f"exponential; common ratio {ratio}; {equation}"
        used = [f"points {list(zip(range(4), values))}"]
        return facts, question, steps, answer, Fraction(values[3]), equation, used, str

    @staticmethod
    def _equation_to_table():
        initial, rate = random.randint(2, 80), random.randint(2, 30)
        first = random.randint(0, 4)
        xs = [first + offset for offset in range(4)]
        values = [rate * x + initial for x in xs]
        equation = _linear_equation(rate, initial)
        facts = f"The relationship is {equation}."
        question = f"Give the y-values for x = {', '.join(map(str, xs))}."
        steps = [step("MODEL_EQ", equation, "given relationship")]
        for x, value in zip(xs, values):
            steps += [step("M", rate, x, rate * x), step("A", rate * x, initial, value),
                      step("TABLE_ROW", f"x = {x}", f"y = {value}")]
        answer = "; ".join(f"x={x} → y={value}" for x, value in zip(xs, values))
        used = [equation, f"x-values {', '.join(map(str, xs))}"]
        return facts, question, steps, answer, Fraction(values[-1]), equation, used, str

    @staticmethod
    def _graph_features_to_equation():
        intercept, slope = random.randint(2, 80), random.randint(2, 25)
        equation = _linear_equation(slope, intercept)
        facts = (f"A line crosses the vertical axis at {intercept}. Moving 1 unit right "
                 f"moves {slope} units up.")
        question = "Write y in terms of x for this line."
        steps = [step("INTERPRET", intercept, "y-value when x = 0"),
                 step("INTERPRET", f"rise {slope}, run 1", f"change {slope} per x"),
                 step("D", slope, 1, slope), step("TRANSLATE", "described line", equation),
                 step("CHECK", "x = 0", f"y = {intercept}")]
        used = [f"vertical intercept {intercept}", f"right 1 and up {slope}"]
        return facts, question, steps, equation, Fraction(intercept), equation, used, str

    @staticmethod
    def _intercept_meaning():
        fixed, rate = random.randint(20, 100), random.randint(10, 50)
        equation = f"C = {fixed} + {rate}h"
        facts = (f"A plumber's total charge C dollars for h hours is {equation}.")
        question = f"What does {fixed} mean in this situation?"
        steps = [step("M", rate, 0, 0), step("A", fixed, 0, fixed),
                 step("INTERPRET", fixed, "fixed call-out fee"),
                 step("CHECK", "h = 0", money(fixed))]
        answer = f"{fixed}; the fixed call-out fee"
        used = [equation, "C dollars", "h hours"]
        return facts, question, steps, answer, Fraction(fixed), equation, used, money

    @staticmethod
    def _which_representation_matches():
        initial, rate = random.randint(5, 80), random.randint(2, 30)
        while initial == rate:
            rate = random.randint(2, 30)
        equation = _linear_equation(rate, initial)
        distractors = [_linear_equation(initial, rate), f"y = {rate}x − {initial}"]
        options = [equation] + distractors
        random.shuffle(options)
        label = "ABC"[options.index(equation)]
        facts = (f"A service charges ${initial} before work begins and ${rate} for each hour. "
                 + "Choices — " + "; ".join(f"{letter}: {option}" for letter, option in zip("ABC", options)) + ".")
        question = "Which choice matches the service cost?"
        steps = [step("INTERPRET", initial, "starting charge"),
                 step("INTERPRET", rate, "charge per hour")]
        steps += [step("OPTION", letter, option) for letter, option in zip("ABC", options)]
        steps += [step("MATCH_REP", label, equation),
                  step("CHECK", "zero hours", f"cost {money(initial)}")]
        answer = f"option {label}; {equation}"
        used = [f"fixed ${initial}", f"${rate} per hour", "three choices"]
        return facts, question, steps, answer, Fraction(initial + rate), equation, used, str

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
            extra = random.choice([value for value in range(801, 1201) if value not in occupied])
            problem = f"An unrelated file lists {extra} blank labels. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} blank labels"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale shown by the representation",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "canonical relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_representation_translation_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
