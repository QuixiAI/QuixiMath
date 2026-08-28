"""Compute with exact, explicitly named mental rewrites.

Variants: ``compensation``, ``doubling_halving``, ``distributive_split``,
``friendly_numbers``, ``count_up_change``, ``percent_shortcut``, and
``choose_strategy``. Five shared-context renderings and all four applied
modifiers are supported. Every answer contains both the exact value and the
rewrite that earned it. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``STRATEGY``, ``A``, ``S``, ``M``, ``D``,
``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("compensation", "doubling_halving", "distributive_split",
            "friendly_numbers", "count_up_change", "percent_shortcut",
            "choose_strategy")
FRAMES = (
    "At {place}, {name} needs a quick exact result. {facts} {question}",
    "{question} A calculation given to {name} at {place} reads: {facts}",
    "For {name} at {place}, the calculation is described this way: {facts} {question}",
    "At {place}, a note reviewed by {name} says: {facts} {question}",
    "Consider the calculation from {place} that {name} is checking. {facts} "
    "{question}",
)
PLACES = tuple(
    setting
    for key in ("classroom", "shop", "business", "workshop", "recipe")
    for setting in CONTEXTS[key].settings
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


class MentalStrategyGenerator(ProblemGenerator):
    """Generate exact arithmetic rewrites designed for mental calculation."""

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
    def _compensation():
        multiplicand = random.randint(12, 98)
        benchmark = random.choice((100, 1000))
        factor = benchmark - random.choice((1, 2))
        gap = benchmark - factor
        benchmark_product = multiplicand * benchmark
        correction = multiplicand * gap
        result = benchmark_product - correction
        rewrite = (f"{multiplicand} × {benchmark} − {correction}" if gap > 1
                   else f"{multiplicand} × {benchmark} − {multiplicand}")
        facts = (f"The calculation is {multiplicand} × {factor}, and a nearby "
                 "power-of-ten rewrite is requested.")
        question = "Give the exact result and show the rewrite."
        answer = f"{result} ({rewrite})"
        model = f"{multiplicand} × {factor} = {rewrite}"
        steps = [step("STRATEGY", "compensation",
                      f"{factor} = {benchmark} − {gap}"),
                 step("M", multiplicand, benchmark, benchmark_product)]
        if gap > 1:
            steps.append(step("M", multiplicand, gap, correction))
        steps += [step("S", benchmark_product, correction, result),
                  step("CHECK", f"{multiplicand} × {factor}", result)]
        used = [f"factor {multiplicand}", f"factor {factor}"]
        return facts, question, steps, answer, Fraction(result), model, used, exact

    @staticmethod
    def _doubling_halving():
        half = random.randint(3, 40)
        first = 2 * half
        second = random.choice((15, 25, 35, 45, 75, 125))
        doubled = 2 * second
        result = first * second
        rewrite = f"{half} × {doubled}"
        facts = (f"The product is {first} × {second}. Keep the same product "
                 "after one factor is halved and the other is doubled.")
        question = "Give the exact result and the friendlier equivalent product."
        answer = f"{result} ({rewrite})"
        model = f"{first} × {second} = {rewrite}"
        steps = [step("STRATEGY", "doubling and halving", rewrite),
                 step("D", first, 2, half),
                 step("M", second, 2, doubled),
                 step("M", half, doubled, result),
                 step("CHECK", f"{first} × {second}", result)]
        used = [f"factor {first}", f"factor {second}"]
        return facts, question, steps, answer, Fraction(result), model, used, exact

    @staticmethod
    def _distributive_split():
        first = random.randint(12, 99)
        tens = random.randrange(20, 100, 10)
        ones = random.randint(2, 9)
        second = tens + ones
        first_part = first * tens
        second_part = first * ones
        result = first_part + second_part
        rewrite = f"{first} × {tens} + {first} × {ones}"
        facts = (f"The product is {first} × {second}. Split the second factor "
                 "into its tens and ones.")
        question = "Give the exact result and show the two partial products."
        answer = f"{result} ({rewrite})"
        model = f"{first} × {second} = {rewrite}"
        steps = [step("STRATEGY", "distributive split",
                      f"{second} = {tens} + {ones}"),
                 step("M", first, tens, first_part),
                 step("M", first, ones, second_part),
                 step("A", first_part, second_part, result),
                 step("CHECK", f"{first} × {second}", result)]
        used = [f"factor {first}", f"factor {second}"]
        return facts, question, steps, answer, Fraction(result), model, used, exact

    @staticmethod
    def _friendly_numbers():
        first = random.randint(4, 49) * 10 + random.randint(1, 8)
        shift = 10 - first % 10
        second = random.randint(shift + 2, 99)
        friendly = first + shift
        adjusted = second - shift
        result = first + second
        rewrite = f"{friendly} + {adjusted}"
        facts = (f"The sum is {first} + {second}. Move just enough from the "
                 "second addend to make the first end in zero.")
        question = "Give the exact result and show the adjusted addends."
        answer = f"{result} ({rewrite})"
        model = f"{first} + {second} = {rewrite}"
        steps = [step("STRATEGY", "friendly numbers",
                      f"move {shift} from {second} to {first}"),
                 step("A", first, shift, friendly),
                 step("S", second, shift, adjusted),
                 step("A", friendly, adjusted, result),
                 step("CHECK", f"{first} + {second}", result)]
        used = [f"addend {first}", f"addend {second}"]
        return facts, question, steps, answer, Fraction(result), model, used, exact

    @staticmethod
    def _count_up_change():
        dollars = random.randint(5, 74)
        cents = random.choice((5, 15, 25, 35, 45, 55, 65, 75, 85, 95))
        price = Fraction(100 * dollars + cents, 100)
        next_dollar = dollars + 1
        payment = ((next_dollar // 5) + random.randint(1, 4)) * 5
        while payment <= next_dollar:
            payment += 5
        first_jump = Fraction(next_dollar) - price
        second_jump = Fraction(payment - next_dollar)
        change = first_jump + second_jump
        rewrite = (f"{money(first_jump)} to {money(next_dollar)}, then "
                   f"{money(second_jump)}")
        facts = (f"A purchase costs {money(price)} and is paid with "
                 f"{money(payment)}. Count upward through the next whole dollar.")
        question = "How much change is due, and what two jumps give it?"
        answer = f"{money(change)} ({rewrite})"
        model = f"change = {money(payment)} − {money(price)}"
        steps = [step("STRATEGY", "count up change", rewrite),
                 step("S", next_dollar, exact(price), exact(first_jump)),
                 step("S", payment, next_dollar, exact(second_jump)),
                 step("A", exact(first_jump), exact(second_jump), exact(change)),
                 step("CHECK", f"{money(price)} + {money(change)}",
                      money(payment))]
        used = [f"price {money(price)}", f"payment {money(payment)}"]
        return facts, question, steps, answer, change, model, used, money

    @staticmethod
    def _percent_shortcut():
        base = random.randrange(40, 401, 20)
        percent = random.choice((15, 25, 35, 45))
        tens_count = percent // 10
        ten_percent = Fraction(base, 10)
        tens_part = tens_count * ten_percent
        five_percent = Fraction(base, 20)
        result = tens_part + five_percent
        first_label = f"{10 * tens_count}%"
        rewrite = f"{first_label} + 5%"
        facts = (f"The target is {percent}% of {base}. Build it from a whole "
                 "number of 10% pieces and one 5% piece.")
        question = "Give the exact result and name the percentage split."
        answer = f"{exact(result)} ({rewrite})"
        model = (f"{percent}% of {base} = {first_label} of {base} + "
                 f"5% of {base}")
        steps = [step("STRATEGY", "percent shortcut", rewrite),
                 step("D", base, 10, exact(ten_percent)),
                 step("M", tens_count, exact(ten_percent), exact(tens_part)),
                 step("D", exact(ten_percent), 2, exact(five_percent)),
                 step("A", exact(tens_part), exact(five_percent), exact(result)),
                 step("CHECK", f"{percent}/100 × {base}", exact(result))]
        used = [f"{percent}%", f"base {base}"]
        return facts, question, steps, answer, result, model, used, exact

    @classmethod
    def _choose_strategy(cls):
        family = random.choice(("compensation", "doubling_halving",
                                "distributive_split"))
        if family == "compensation":
            first = random.randint(12, 98)
            benchmark = random.choice((100, 1000))
            second = benchmark - 1
            result = first * second
            proposal_a = f"{first} × {benchmark} − {first}"
            proposal_b = f"{first} × {benchmark} + {first}"
            label = "compensation"
            steps = [step("STRATEGY", label, f"A: {proposal_a}"),
                     step("M", first, benchmark, first * benchmark),
                     step("S", first * benchmark, first, result)]
        elif family == "doubling_halving":
            half = random.randint(3, 40)
            first = 2 * half
            second = random.choice((15, 25, 35, 45, 75, 125))
            doubled = 2 * second
            result = first * second
            proposal_a = f"{half} × {doubled}"
            proposal_b = f"{half} × {second + 1}"
            label = "doubling and halving"
            steps = [step("STRATEGY", label, f"A: {proposal_a}"),
                     step("D", first, 2, half),
                     step("M", second, 2, doubled),
                     step("M", half, doubled, result)]
        else:
            first = random.randint(12, 99)
            tens = random.randrange(20, 100, 10)
            ones = random.randint(2, 9)
            second = tens + ones
            result = first * second
            proposal_a = f"{first} × {tens} + {first} × {ones}"
            proposal_b = f"{first} × {tens} + {ones}"
            label = "distributive split"
            first_part, second_part = first * tens, first * ones
            steps = [step("STRATEGY", label, f"A: {proposal_a}"),
                     step("M", first, tens, first_part),
                     step("M", first, ones, second_part),
                     step("A", first_part, second_part, result)]
        facts = (f"For {first} × {second}, proposal A is {proposal_a}; proposal "
                 f"B is {proposal_b}.")
        question = "Which proposed rewrite is equivalent, and what exact result follows?"
        answer = f"A: {label}; {result} ({proposal_a})"
        model = f"{first} × {second} = {proposal_a}"
        steps.append(step("CHECK", f"{first} × {second}", result))
        used = [f"expression {first} × {second}", "proposals A and B"]
        return facts, question, steps, answer, Fraction(result), model, used, exact

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
            extra = random.choice([number for number in range(111, 411)
                                   if number not in occupied])
            problem = f"A shelf nearby holds {extra} unused labels. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} unused labels"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "round to a friendly benchmark before the exact rewrite",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "equivalent mental rewrite"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_mental_strategy_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
