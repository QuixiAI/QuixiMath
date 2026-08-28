"""Exact conservation stories for concentrations, alloys, and blends.

Variants: ``two_solutions``, ``add_pure``, ``add_water``, ``price_blend``,
``alloy``, and ``target_concentration_unknown_amount``. Inputs are filtered so
percentages, amounts, and prices remain hand-friendly. Five renderings and all
four applied modifiers are supported. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``PERCENT_TO_DEC``, ``AMOUNT``,
``MODEL_EQ``, ``A``, ``S``, ``M``, ``D``, ``DEC_TO_PERCENT``, ``CHECK``,
and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, dec, estimate_first, exact, money,
                            select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("two_solutions", "add_pure", "add_water", "price_blend",
            "alloy", "target_concentration_unknown_amount")
PLACES = tuple(
    setting
    for key in ("lab", "recipe", "workshop", "garden", "business")
    for setting in CONTEXTS[key].settings
)
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} note from {place} says: {facts}",
    "Batch {record} at {place} — {facts} {question}",
    "At {place}, record {record}: {facts_lc} {question}",
    "Consider the {record} report from {place}: {facts} {question}",
)
PERCENT_BANK = (10, 15, 20, 25, 30, 40, 50, 60, 75, 80)


def percent_text(value):
    return f"{exact(Fraction(value))}%"


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(PLACES),
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def _clean_percent(value):
    return Fraction(value).denominator in (1, 2, 4, 5, 10)


class MixtureGenerator(ProblemGenerator):
    """Generate exact conservation stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("%", "L", "kg", "$")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _two_component(kind):
        while True:
            low, high = sorted(random.sample(PERCENT_BANK, 2))
            v1, v2 = random.randint(2, 20), random.randint(2, 20)
            amount1 = Fraction(v1 * low, 100)
            amount2 = Fraction(v2 * high, 100)
            concentration = 100 * (amount1 + amount2) / (v1 + v2)
            if _clean_percent(concentration):
                break
        unit_name = "kg" if kind == "alloy" else "L"
        substance = "copper" if kind == "alloy" else "salt"
        noun = "alloy" if kind == "alloy" else "solution"
        facts = (f"{v1} {unit_name} of a {low}% {substance} {noun} is combined "
                 f"with {v2} {unit_name} of a {high}% {substance} {noun}.")
        question = f"What percent {substance} is in the combined {noun}?"
        model = (f"x = ({v1}*{low}/100 + {v2}*{high}/100) / "
                 f"({v1}+{v2}) * 100")
        total_amount = amount1 + amount2
        total_volume = v1 + v2
        steps = [step("PERCENT_TO_DEC", f"{low}%", dec(Fraction(low, 100))),
                 step("M", v1, dec(Fraction(low, 100)), exact(amount1)),
                 step("AMOUNT", f"{substance} in first part", exact(amount1)),
                 step("PERCENT_TO_DEC", f"{high}%", dec(Fraction(high, 100))),
                 step("M", v2, dec(Fraction(high, 100)), exact(amount2)),
                 step("AMOUNT", f"{substance} in second part", exact(amount2)),
                 step("A", exact(amount1), exact(amount2), exact(total_amount)),
                 step("A", v1, v2, total_volume),
                 step("D", exact(total_amount), total_volume,
                      exact(total_amount / total_volume)),
                 step("DEC_TO_PERCENT", exact(total_amount / total_volume),
                      percent_text(concentration)),
                 step("CHECK", "component conservation", exact(total_amount))]
        answer = percent_text(concentration)
        used = [f"{v1} {unit_name} at {low}%", f"{v2} {unit_name} at {high}%"]
        return facts, question, steps, answer, concentration, model, used, percent_text

    @staticmethod
    def _add_pure():
        while True:
            start = random.choice((10, 20, 25, 30, 40, 50, 60))
            target = random.choice([p for p in PERCENT_BANK if start < p < 100])
            volume = random.randint(2, 30)
            added = Fraction(volume * (target - start), 100 - target)
            if added.denominator == 1 and 1 <= added <= 30:
                added = int(added)
                break
        facts = (f"A tank holds {volume} L of a {start}% acid solution. Pure "
                 f"acid is added until the concentration is {target}%.")
        question = "How many litres of pure acid are added?"
        model = f"({start}/100*{volume} + x)/({volume}+x) = {target}/100"
        initial = Fraction(volume * start, 100)
        final_amount = initial + added
        final_volume = volume + added
        steps = [step("PERCENT_TO_DEC", f"{start}%", dec(Fraction(start, 100))),
                 step("M", volume, dec(Fraction(start, 100)), exact(initial)),
                 step("AMOUNT", "acid initially", exact(initial)),
                 step("MODEL_EQ", model, "target concentration"),
                 step("A", exact(initial), added, exact(final_amount)),
                 step("A", volume, added, final_volume),
                 step("D", exact(final_amount), final_volume,
                      dec(Fraction(target, 100))),
                 step("CHECK", "target percent", f"{target}%")]
        return facts, question, steps, f"{added} L", Fraction(added), model, [f"{volume} L", f"{start}%", f"target {target}%"], None

    @staticmethod
    def _add_water():
        while True:
            start = random.choice((20, 25, 30, 40, 50, 60, 75, 80))
            target = random.choice([p for p in PERCENT_BANK if 0 < p < start])
            volume = random.randint(2, 30)
            added = Fraction(volume * (start - target), target)
            if added.denominator == 1 and 1 <= added <= 40:
                added = int(added)
                break
        facts = (f"A container has {volume} L of a {start}% cleaner. Water is "
                 f"added until the cleaner is {target}%.")
        question = "How many litres of water are added?"
        model = f"({start}/100*{volume})/({volume}+x) = {target}/100"
        active = Fraction(volume * start, 100)
        final_volume = volume + added
        steps = [step("PERCENT_TO_DEC", f"{start}%", dec(Fraction(start, 100))),
                 step("M", volume, dec(Fraction(start, 100)), exact(active)),
                 step("AMOUNT", "cleaner stays fixed", exact(active)),
                 step("MODEL_EQ", model, "target concentration"),
                 step("A", volume, added, final_volume),
                 step("D", exact(active), final_volume, dec(Fraction(target, 100))),
                 step("CHECK", "target percent", f"{target}%")]
        return facts, question, steps, f"{added} L", Fraction(added), model, [f"{volume} L", f"{start}%", f"target {target}%"], None

    @staticmethod
    def _price_blend():
        while True:
            q1, q2 = random.randint(2, 15), random.randint(2, 15)
            p1 = Fraction(random.randint(8, 40), 4)
            p2 = Fraction(random.randint(8, 40), 4)
            if p1 == p2:
                continue
            price = (q1 * p1 + q2 * p2) / (q1 + q2)
            if (price * 100).denominator == 1:
                break
        facts = (f"A coffee blend uses {q1} kg costing {money(p1)} per kg and "
                 f"{q2} kg costing {money(p2)} per kg.")
        question = "What does the combined blend cost per kg?"
        total1, total2 = q1 * p1, q2 * p2
        total_cost, total_mass = total1 + total2, q1 + q2
        model = f"x = ({q1}*{p1} + {q2}*{p2})/({q1}+{q2})"
        steps = [step("M", q1, exact(p1), exact(total1)),
                 step("AMOUNT", "cost of first coffee", money(total1)),
                 step("M", q2, exact(p2), exact(total2)),
                 step("AMOUNT", "cost of second coffee", money(total2)),
                 step("A", exact(total1), exact(total2), exact(total_cost)),
                 step("A", q1, q2, total_mass),
                 step("D", exact(total_cost), total_mass, exact(price)),
                 step("CHECK", "weighted cost", money(total_cost))]
        answer = f"{money(price)} per kg"
        used = [f"{q1} kg at {money(p1)}", f"{q2} kg at {money(p2)}"]
        return facts, question, steps, answer, price, model, used, money

    @staticmethod
    def _unknown_amount():
        while True:
            low, target, high = sorted(random.sample(PERCENT_BANK, 3))
            volume = random.randint(2, 30)
            added = Fraction(volume * (target - low), high - target)
            if added.denominator == 1 and 1 <= added <= 40:
                added = int(added)
                break
        facts = (f"A vat contains {volume} L of a {low}% dye solution. A "
                 f"{high}% solution is added to make a {target}% mixture.")
        question = f"How many litres of the {high}% solution are added?"
        model = f"({low}/100*{volume} + {high}/100*x)/({volume}+x) = {target}/100"
        first_amount = Fraction(volume * low, 100)
        second_amount = Fraction(added * high, 100)
        total_amount, total_volume = first_amount + second_amount, volume + added
        steps = [step("M", volume, dec(Fraction(low, 100)), exact(first_amount)),
                 step("AMOUNT", "dye initially", exact(first_amount)),
                 step("M", added, dec(Fraction(high, 100)), exact(second_amount)),
                 step("AMOUNT", "dye added", exact(second_amount)),
                 step("A", exact(first_amount), exact(second_amount), exact(total_amount)),
                 step("A", volume, added, total_volume),
                 step("D", exact(total_amount), total_volume,
                      dec(Fraction(target, 100))),
                 step("CHECK", "target percent", f"{target}%")]
        used = [f"{volume} L at {low}%", f"added solution {high}%", f"target {target}%"]
        return facts, question, steps, f"{added} L", Fraction(added), model, used, None

    @classmethod
    def _case(cls, variant):
        if variant in ("two_solutions", "alloy"):
            return cls._two_component(variant)
        if variant == "add_pure":
            return cls._add_pure()
        if variant == "add_water":
            return cls._add_water()
        if variant == "price_blend":
            return cls._price_blend()
        return cls._unknown_amount()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(41, 100)
                                   if number not in occupied])
            problem = f"A shelf nearby holds {extra} empty bottles. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} empty bottles"))
        elif modifier == "estimate_first":
            render = renderer or exact
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "round the amounts before combining",
                                   render=render)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "amount conservation"))
            answer = f"{model}; x = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_mixture_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
