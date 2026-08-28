"""Percent change, markup, discount, and tax stories.

Arithmetic variants are ``increase``, ``decrease``, ``markup``, ``discount``,
and ``tax``. Each has five phrasings drawn through shared applied contexts and
supports ``plain``, ``distractor``, ``estimate_first``, and ``with_model``.
The historical ``distractor=True`` constructor remains supported. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``PERCENT_TO_DEC``, ``M``, ``A``, ``S``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, dec, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("increase", "decrease", "markup", "discount", "tax")
PHRASINGS = {
    "increase": (
        "A measurement starts at {base} units and grows by {pct}%. What is its new value?",
        "A quantity of {base} units becomes {pct}% larger. What is the result?",
        "A {base}-unit reading rises by {pct}%. What reading follows?",
        "Growth of {pct}% is recorded from an initial {base} units. What is the new amount?",
        "The starting level is {base} units; it then gains {pct}%. What is the ending level?",
    ),
    "decrease": (
        "A measurement starts at {base} units and falls by {pct}%. What is its new value?",
        "A quantity of {base} units becomes {pct}% smaller. What is the result?",
        "A {base}-unit reading drops by {pct}%. What reading follows?",
        "A reduction of {pct}% is recorded from an initial {base} units. What remains?",
        "The starting level is {base} units; it then loses {pct}%. What is the ending level?",
    ),
    "markup": (
        "A store raises a {base}-dollar item's price by {pct}%. What is the new price?",
        "A wholesaler pays ${base}.00 and raises that price by {pct}%. What is the retail price?",
        "An item starts at ${base}.00 and its price grows {pct}%. What price follows?",
        "The base price is ${base}.00 before a {pct}% increase. What is the resulting price?",
        "A shop adds {pct}% to a ${base}.00 price. What is the new price?",
    ),
    "discount": (
        "A {pct}% discount is applied to ${base}.00. What is the sale price?",
        "An item priced at ${base}.00 is {pct}% off. What is the sale price?",
        "A shop reduces a ${base}.00 price by {pct}%. What price remains?",
        "The listed price is ${base}.00 before a {pct}% reduction. What is the new price?",
        "A ${base}.00 item becomes {pct}% cheaper. What does it cost now?",
    ),
    "tax": (
        "An item costs ${base}.00 before {pct}% sales tax. What is the total cost?",
        "A ${base}.00 purchase has {pct}% sales tax added. What is the total?",
        "Tax adds {pct}% to a ${base}.00 price. What amount is paid?",
        "The pre-tax price is ${base}.00 and the tax rate is {pct}%. What is the final price?",
        "A buyer pays {pct}% tax on an item priced at ${base}.00. What is the total charge?",
    ),
}
ADDITIVE = ("increase", "markup", "tax")
MONEY_OPS = ("markup", "discount", "tax")
PLACES = tuple(
    setting
    for key in ("shop", "business", "lab")
    for setting in CONTEXTS[key].settings
)


class PercentWordProblemGenerator(ProblemGenerator):
    """Generate exact one-step percent stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("$", "units")

    def __init__(self, distractor=False, modifier=None, variant=None):
        if modifier is None:
            modifier = "distractor" if distractor else "plain"
        elif distractor and modifier != "distractor":
            raise ValueError("distractor=True requires modifier='distractor'")
        if modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS}")
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.modifier = modifier
        self.variant = variant
        self.distractor = modifier == "distractor"

    def generate(self):
        op_type = self.variant or random.choice(self.VARIANTS)
        pct = random.choice((5, 8, 10, 12, 15, 20, 25, 30))
        base = random.randint(20, 200)
        problem = random.choice(PHRASINGS[op_type]).format(pct=pct, base=base)
        problem = f"At {random.choice(PLACES)}, {problem[:1].lower() + problem[1:]}"

        pct_dec = Fraction(pct, 100)
        change = Fraction(base) * pct_dec
        additive = op_type in ADDITIVE
        new_total = Fraction(base) + change if additive else Fraction(base) - change
        model_sign = "+" if additive else "-"
        model = f"x = {base}*(1{model_sign}{pct}/100)"
        steps = [step("PERCENT_TO_DEC", f"{pct}%", dec(pct_dec)),
                 step("M", base, dec(pct_dec), exact(change)),
                 step("A" if additive else "S", base, exact(change),
                      exact(new_total)),
                 step("CHECK", "percent change from base", exact(new_total))]

        if op_type in MONEY_OPS:
            final_answer = money(new_total)
            renderer = money
        else:
            final_answer = unit(new_total, "unit")
            renderer = lambda value: unit(value, "unit")

        if self.modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A shelf nearby holds {extra} empty folders. {problem}"
            steps.insert(0, select_relevant_step(
                [f"base {base}", f"rate {pct}%"], f"{extra} empty folders"))
        elif self.modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", final_answer)], new_total,
                "round the base before applying the percent", render=renderer)[:-1]
        elif self.modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "changed value"))
            final_answer = f"{model}; x = {final_answer}"

        steps.append(step("Z", final_answer))
        return {"problem_id": jid(),
                "operation": f"applied_percent_word_{op_type}_{self.modifier}",
                "problem": problem, "steps": steps,
                "final_answer": final_answer}
