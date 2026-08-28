"""Compare repeated growth, linear change, doubling, and depreciation.

Variants: ``linear_vs_exponential_table``, ``crossover_year``,
``rule_of_70_doubling``, ``depreciation_below_threshold``,
``repeated_doubling_count``, and ``which_offer``. Five context frames and all
four applied modifiers are supported. Rates come from a hand-friendly exact
set, and money values are constructed to remain exact to the cent. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``TABLE_ROW``, ``CROSSOVER``, ``RULE_OF_70``, ``TRY``, ``ACCEPT``, ``CMP``,
``A``, ``S``, ``M``, ``D``, ``E``, ``CHECK``, and ``Z``.
"""
import math
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, exact, money, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("linear_vs_exponential_table", "crossover_year",
            "rule_of_70_doubling", "depreciation_below_threshold",
            "repeated_doubling_count", "which_offer")
RATES = (5, 10, 20, 25, 50)
FRAMES = (
    "At {place}, {name} compares the following choices. {facts} {question}",
    "{question} A note for {name} from {place} says: {facts}",
    "For {name}'s review at {place}: {facts} {question}",
    "A report from {place}, checked by {name}, states: {facts} {question}",
    "Consider the figures {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


def _start_for(rate, years, low=100):
    factor = (1 + Fraction(rate, 100)) ** years
    stride = factor.denominator // math.gcd(factor.denominator, 100)
    minimum = max(1, (low + stride - 1) // stride)
    return stride * random.randint(minimum, minimum + 200)


def _growth_rows(start, rate, increment, years):
    factor = 1 + Fraction(rate, 100)
    return [(year, Fraction(start + increment * year), Fraction(start) * factor ** year)
            for year in range(1, years + 1)]


class GrowthComparisonGenerator(ProblemGenerator):
    """Generate six exact growth-comparison stories without method cues."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _linear_vs_exponential_table():
        years = random.randint(2, 6)
        rate = random.choice(RATES)
        start = _start_for(rate, years)
        increment = random.randint(5, max(6, start // 3))
        rows = _growth_rows(start, rate, increment, years)
        while rows[-1][1] == rows[-1][2]:
            increment += 1
            rows = _growth_rows(start, rate, increment, years)
        linear, exponential = rows[-1][1], rows[-1][2]
        winner = "exponential" if exponential > linear else "linear"
        facts = (f"A value starts at {money(start)}. Plan L adds {money(increment)} "
                 f"each year, while plan E grows by {rate}% each year.")
        question = f"At the end of year {years}, which plan is larger and by how much?"
        model = f"L(n) = {start} + {increment}n; E(n) = {start}({exact(1 + Fraction(rate, 100))})^n"
        steps = [step("MODEL_EQ", model, "two growth patterns")]
        for year, linear_value, exponential_value in rows:
            steps.append(step("TABLE_ROW", f"year {year}",
                              f"L {money(linear_value)}, E {money(exponential_value)}"))
        difference = abs(exponential - linear)
        steps += [step("S", max(linear, exponential), min(linear, exponential), difference),
                  step("CMP", money(exponential), money(linear), ">" if exponential > linear else "<"),
                  step("CHECK", f"year {years}", f"{winner} larger")]
        answer = f"{winner}; difference {money(difference)}"
        used = [f"start {money(start)}", f"L adds {money(increment)}", f"E grows {rate}%", f"year {years}"]
        return facts, question, steps, answer, difference, model, used, money

    @staticmethod
    def _crossover_year():
        while True:
            rate = random.choice(RATES)
            max_year = random.randint(5, 9)
            start = _start_for(rate, max_year)
            first_growth = Fraction(start * rate, 100)
            offset = random.randint(-max(1, int(first_growth // 3)), max(1, int(first_growth // 2)))
            increment = max(1, int(first_growth) + offset)
            rows = _growth_rows(start, rate, increment, max_year)
            crossings = [year for year, linear, exponential in rows if exponential > linear]
            if crossings and crossings[0] >= 2:
                crossing = crossings[0]
                break
        facts = (f"Offer A starts at {money(start)} and adds {money(increment)} each year. "
                 f"Offer B starts at {money(start)} and grows {rate}% each year.")
        question = "What is the first whole year when offer B is worth more than offer A?"
        model = f"A(n) = {start} + {increment}n; B(n) = {start}({exact(1 + Fraction(rate, 100))})^n"
        steps = [step("MODEL_EQ", model, "compare year by year")]
        for year, linear, exponential in rows[:crossing]:
            steps.append(step("TABLE_ROW", f"year {year}",
                              f"A {money(linear)}, B {money(exponential)}"))
        linear, exponential = rows[crossing - 1][1:]
        steps += [step("CROSSOVER", crossing, money(linear), money(exponential)),
                  step("CHECK", "first strict crossing", f"{money(exponential)} > {money(linear)}")]
        answer = f"year {crossing}; {money(exponential)} vs {money(linear)}"
        used = [f"start {money(start)}", f"A adds {money(increment)}", f"B grows {rate}%"]
        return facts, question, steps, answer, Fraction(crossing), model, used, lambda v: unit(v, "year")

    @staticmethod
    def _rule_of_70_doubling():
        rate = random.choice((5, 7, 10, 14))
        years = 70 // rate
        facts = (f"An account grows at {rate}% per year. For this estimate, use the "
                 "rule of 70: divide 70 by the annual percent rate.")
        question = "About how many years will doubling take?"
        model = f"doubling time ≈ 70/{rate}"
        steps = [step("MODEL_EQ", model, "supplied approximation"),
                 step("D", 70, rate, years), step("RULE_OF_70", f"{rate}%", years),
                 step("CHECK", "approximate doubling time", unit(years, "year"))]
        answer = unit(years, "year")
        used = [f"rate {rate}%", "supplied rule 70 ÷ rate"]
        return facts, question, steps, answer, Fraction(years), model, used, lambda v: unit(v, "year")

    @staticmethod
    def _depreciation_below_threshold():
        rate = random.choice((20, 25, 50))
        year = random.randint(2, 5)
        factor = 1 - Fraction(rate, 100)
        start = _start_for(-rate, year, low=1000)
        values = [Fraction(start) * factor ** n for n in range(1, year + 1)]
        previous_cents, current_cents = int(values[-2] * 100), int(values[-1] * 100)
        threshold = Fraction((previous_cents + current_cents) // 2, 100)
        facts = (f"A machine is worth {money(start)} and loses {rate}% of its value "
                 f"each year. A replacement is required once its value is below {money(threshold)}.")
        question = "What is the first whole year when replacement is required?"
        model = f"V(n) = {start}({exact(factor)})^n"
        steps = [step("MODEL_EQ", model, "value after n years")]
        for n, value in enumerate(values, 1):
            steps.append(step("TRY", f"year {n}", money(value)))
        steps += [step("ACCEPT", f"year {year}", f"{money(values[-1])} < {money(threshold)}"),
                  step("CHECK", f"year {year - 1}", f"{money(values[-2])} ≥ {money(threshold)}")]
        answer = f"year {year}; value {money(values[-1])}"
        used = [f"start {money(start)}", f"loss {rate}%", f"threshold {money(threshold)}"]
        return facts, question, steps, answer, Fraction(year), model, used, lambda v: unit(v, "year")

    @staticmethod
    def _repeated_doubling_count():
        start = random.randint(2, 250)
        count = random.randint(2, 10)
        target = start * 2 ** count
        facts = f"A culture starts with {start} cells and doubles once per hour."
        question = f"How many complete hours does it take to reach {target} cells?"
        model = f"{start} × 2^h = {target}"
        steps = [step("MODEL_EQ", model, "one doubling per hour")]
        current = start
        for hour in range(1, count + 1):
            steps += [step("M", current, 2, current * 2),
                      step("TABLE_ROW", f"hour {hour}", f"{current * 2} cells")]
            current *= 2
        steps += [step("ACCEPT", f"hour {count}", f"{current} cells"),
                  step("CHECK", "target reached", current)]
        answer = unit(count, "hour")
        used = [f"start {start} cells", "doubles hourly", f"target {target} cells"]
        return facts, question, steps, answer, Fraction(count), model, used, lambda v: unit(v, "hour")

    @staticmethod
    def _which_offer():
        while True:
            years = random.randint(2, 6)
            rate = random.choice(RATES)
            start = _start_for(rate, years)
            increment = random.randint(5, max(6, start // 2))
            linear = Fraction(start + increment * years)
            exponential = Fraction(start) * (1 + Fraction(rate, 100)) ** years
            if linear != exponential:
                break
        facts = (f"For {years} years, offer A pays {money(start)} initially plus "
                 f"{money(increment)} more each year. Offer B starts at {money(start)} "
                 f"and grows {rate}% per year.")
        question = "Which offer has the larger value at the end, and what are both values?"
        model = f"A = {start} + {increment}({years}); B = {start}({exact(1 + Fraction(rate, 100))})^{years}"
        winner = "offer B" if exponential > linear else "offer A"
        steps = [step("MODEL_EQ", model, "end values"),
                 step("M", increment, years, increment * years),
                 step("A", start, increment * years, linear),
                 step("E", exact(1 + Fraction(rate, 100)), years,
                      exact((1 + Fraction(rate, 100)) ** years)),
                 step("M", start, exact((1 + Fraction(rate, 100)) ** years), exponential),
                 step("CMP", money(exponential), money(linear), ">" if exponential > linear else "<"),
                 step("CHECK", winner, "larger end value")]
        answer = f"{winner}; A {money(linear)}; B {money(exponential)}"
        used = [f"term {years} years", f"start {money(start)}", f"A adds {money(increment)}", f"B grows {rate}%"]
        return facts, question, steps, answer, max(linear, exponential), model, used, money

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
            extra = random.choice([value for value in range(501, 901) if value not in occupied])
            problem = f"An unrelated memo lists {extra} archive boxes. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} archive boxes"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the likely growth scale",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "growth comparison"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_growth_comparison_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
