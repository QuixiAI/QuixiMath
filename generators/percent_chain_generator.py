"""Exact sequential-percent stories that expose multiplicative composition.

Variants: ``markup_then_discount``, ``tax_then_tip``,
``successive_changes_net``, ``reverse_from_sale_price``,
``reverse_from_total_with_tax``, and ``percent_of_percent``. Five
shared-context renderings and all four applied modifiers are supported. Cases
are filtered to exact cents; percent answers terminate. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``PERCENT_TO_DEC``,
``PCT_STEP``, ``REVERSE_PCT``, ``MODEL_EQ``, ``A``, ``S``, ``M``, ``D``,
``DEC_TO_PERCENT``, ``CHECK``, and ``Z``.
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
VARIANTS = ("markup_then_discount", "tax_then_tip",
            "successive_changes_net", "reverse_from_sale_price",
            "reverse_from_total_with_tax", "percent_of_percent")
PLACES = tuple(
    setting
    for key in ("shop", "business", "people", "recipe")
    for setting in CONTEXTS[key].settings
)
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} note from {place} says: {facts}",
    "Receipt {record} at {place} — {facts} {question}",
    "At {place}, record {record}: {facts_lc} {question}",
    "Consider the {record} report from {place}: {facts} {question}",
)
RATES = (5, 10, 12, 15, 20, 25, 30, 40, 50)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts[:1].upper() + facts[1:],
        facts_lc=facts[:1].lower() + facts[1:], question=question,
        place=random.choice(PLACES),
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def percent(value):
    return f"{exact(Fraction(value))}%"


def cents_exact(value):
    return (Fraction(value) * 100).denominator == 1


def net_steps(base, final):
    change = final - base
    ratio = change / base
    return [step("S", exact(final), exact(base), exact(change)),
            step("D", exact(change), exact(base), exact(ratio)),
            step("DEC_TO_PERCENT", exact(ratio), percent(ratio * 100))]


class PercentChainGenerator(ProblemGenerator):
    """Generate exact chained-percent stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "%")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _markup_discount():
        while True:
            base = Fraction(random.randrange(20, 201, 5))
            markup, discount = random.sample(RATES, 2)
            marked = base * (100 + markup) / 100
            final = marked * (100 - discount) / 100
            if cents_exact(marked) and cents_exact(final):
                break
        net = (final - base) / base * 100
        facts = (f"A jacket starts at {money(base)}. Its price rises by "
                 f"{markup}%, then the marked price is reduced by {discount}%.")
        question = "What is the final price and the net percent change from the start?"
        model = f"x = {exact(base)}*(1+{markup}/100)*(1-{discount}/100)"
        steps = [step("PERCENT_TO_DEC", f"{markup}%", dec(Fraction(markup, 100))),
                 step("PCT_STEP", 1,
                      f"{exact(base)}*(1+{markup}/100)", exact(marked)),
                 step("M", exact(base), dec(Fraction(100 + markup, 100)),
                      exact(marked)),
                 step("PERCENT_TO_DEC", f"{discount}%",
                      dec(Fraction(discount, 100))),
                 step("PCT_STEP", 2,
                      f"{exact(marked)}*(1-{discount}/100)", exact(final)),
                 step("M", exact(marked), dec(Fraction(100 - discount, 100)),
                      exact(final))]
        steps += net_steps(base, final)
        steps.append(step("CHECK", "sequential price", money(final)))
        answer = f"{money(final)}; net change {percent(net)}"
        used = [f"start {money(base)}", f"rise {markup}%", f"reduction {discount}%"]
        return facts, question, steps, answer, final, model, used, money

    @staticmethod
    def _tax_tip():
        while True:
            base = Fraction(random.randrange(20, 151, 5))
            tax = random.choice((5, 10, 15, 20))
            tip = random.choice((10, 15, 20, 25))
            taxed = base * (100 + tax) / 100
            gratuity = taxed * tip / 100
            final = taxed + gratuity
            if cents_exact(taxed) and cents_exact(gratuity) and cents_exact(final):
                break
        facts = (f"A meal costs {money(base)} before {tax}% tax. A {tip}% tip "
                 "is then calculated from the taxed subtotal.")
        question = "What are the taxed subtotal, the tip, and the final total?"
        model = f"x = {exact(base)}*(1+{tax}/100)*(1+{tip}/100)"
        steps = [step("PERCENT_TO_DEC", f"{tax}%", dec(Fraction(tax, 100))),
                 step("PCT_STEP", 1, f"{exact(base)}*(1+{tax}/100)", exact(taxed)),
                 step("M", exact(base), dec(Fraction(100 + tax, 100)), exact(taxed)),
                 step("PERCENT_TO_DEC", f"{tip}%", dec(Fraction(tip, 100))),
                 step("M", exact(taxed), dec(Fraction(tip, 100)), exact(gratuity)),
                 step("PCT_STEP", 2, f"{exact(taxed)}+{exact(gratuity)}", exact(final)),
                 step("A", exact(taxed), exact(gratuity), exact(final)),
                 step("CHECK", "taxed subtotal plus tip", money(final))]
        answer = (f"subtotal {money(taxed)}; tip {money(gratuity)}; total "
                  f"{money(final)}")
        used = [f"meal {money(base)}", f"tax {tax}%", f"tip {tip}% of taxed subtotal"]
        return facts, question, steps, answer, final, model, used, money

    @staticmethod
    def _successive_changes():
        while True:
            base = Fraction(random.randrange(20, 201, 5))
            first, second = random.sample(RATES, 2)
            first_value = base * (100 + first) / 100
            final = first_value * (100 - second) / 100
            if cents_exact(first_value) and cents_exact(final):
                break
        net = (final - base) / base * 100
        facts = (f"A monthly cost is {money(base)}. It increases by {first}% "
                 f"one month and decreases by {second}% the next month.")
        question = "What is the new cost and the net percent change from the original?"
        model = f"x = {exact(base)}*(1+{first}/100)*(1-{second}/100)"
        steps = [step("PCT_STEP", 1, f"{exact(base)}*(1+{first}/100)",
                      exact(first_value)),
                 step("M", exact(base), dec(Fraction(100 + first, 100)),
                      exact(first_value)),
                 step("PCT_STEP", 2, f"{exact(first_value)}*(1-{second}/100)",
                      exact(final)),
                 step("M", exact(first_value), dec(Fraction(100 - second, 100)),
                      exact(final))]
        steps += net_steps(base, final)
        steps.append(step("CHECK", "two successive changes", money(final)))
        answer = f"{money(final)}; net change {percent(net)}"
        used = [f"original {money(base)}", f"increase {first}%", f"decrease {second}%"]
        return facts, question, steps, answer, final, model, used, money

    @staticmethod
    def _reverse(tax=False):
        while True:
            base = Fraction(random.randrange(20, 201, 5))
            rate = random.choice(RATES)
            factor = Fraction(100 + rate if tax else 100 - rate, 100)
            shown = base * factor
            if cents_exact(shown):
                break
        if tax:
            facts = (f"A purchase totals {money(shown)} after {rate}% tax is "
                     "added to its pre-tax price.")
            question = "What was the pre-tax price?"
            relation = f"x*(1+{rate}/100) = {exact(shown)}"
            label = "pre-tax price"
        else:
            facts = (f"A sale price is {money(shown)} after a {rate}% discount "
                     "from the original price.")
            question = "What was the original price?"
            relation = f"x*(1-{rate}/100) = {exact(shown)}"
            label = "original price"
        steps = [step("PERCENT_TO_DEC", f"{rate}%", dec(Fraction(rate, 100))),
                 step("REVERSE_PCT", relation, exact(base)),
                 step("D", exact(shown), exact(factor), exact(base)),
                 step("M", exact(base), exact(factor), exact(shown)),
                 step("CHECK", label, money(base))]
        used = [f"shown total {money(shown)}", f"rate {rate}%"]
        return facts, question, steps, money(base), base, relation, used, money

    @staticmethod
    def _percent_of_percent():
        first = random.choice((20, 25, 30, 40, 50, 60, 75, 80))
        second = random.choice((10, 20, 25, 40, 50, 75))
        result = Fraction(first * second, 100)
        facts = (f"In a survey, {first}% of all respondents choose option A. "
                 f"Of those respondents, {second}% also choose option B.")
        question = "What percent of all respondents choose both A and B?"
        model = f"x = {first}/100*{second}/100*100"
        decimal_result = Fraction(first, 100) * Fraction(second, 100)
        steps = [step("PERCENT_TO_DEC", f"{first}%", dec(Fraction(first, 100))),
                 step("PERCENT_TO_DEC", f"{second}%", dec(Fraction(second, 100))),
                 step("M", dec(Fraction(first, 100)), dec(Fraction(second, 100)),
                      exact(decimal_result)),
                 step("DEC_TO_PERCENT", exact(decimal_result), percent(result)),
                 step("CHECK", "share of all respondents", percent(result))]
        answer = percent(result)
        used = [f"{first}% choose A", f"{second}% of those choose B"]
        return facts, question, steps, answer, result, model, used, percent

    @classmethod
    def _case(cls, variant):
        if variant == "markup_then_discount":
            return cls._markup_discount()
        if variant == "tax_then_tip":
            return cls._tax_tip()
        if variant == "successive_changes_net":
            return cls._successive_changes()
        if variant == "reverse_from_sale_price":
            return cls._reverse()
        if variant == "reverse_from_total_with_tax":
            return cls._reverse(tax=True)
        return cls._percent_of_percent()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A display nearby holds {extra} postcards. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} postcards"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "round the starting amount before applying the rates",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "successive multipliers"))
            answer = f"{model}; x = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_percent_chain_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
