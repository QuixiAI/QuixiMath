"""Compare quantitative size by bounds, scale, and exact verification.

Variants: ``benchmark_fraction``, ``compare_without_computing``,
``order_of_magnitude``, ``reasonable_answer``,
``bigger_product_or_quotient``, and ``estimate_then_verify``. Five
shared-context renderings and all four applied modifiers are supported.
Qualitative labels always carry an exact numerical fact. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``BOUND``, ``ORDER_MAG``, ``PLAUSIBLE``, ``CMP``, ``A``, ``M``, ``D``,
``E``, ``CHECK``, and ``Z``.
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
VARIANTS = ("benchmark_fraction", "compare_without_computing",
            "order_of_magnitude", "reasonable_answer",
            "bigger_product_or_quotient", "estimate_then_verify")
FRAMES = (
    "At {place}, {name} compares quantitative sizes. {facts} {question}",
    "{question} A record given to {name} at {place} states: {facts}",
    "For {name} at {place}, the comparison is described this way: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the quantitative comparison from {place} that {name} is checking. "
    "{facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("classroom", "shop", "trip", "business", "garden", "lab")
    for setting in CONTEXTS[key].settings
)
BENCHMARKS = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3),
              Fraction(3, 4))
FACTORS = (Fraction(1, 2), Fraction(3, 4), Fraction(5, 4),
           Fraction(3, 2), Fraction(2))


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _relation(left, right):
    return "<" if left < right else ">" if left > right else "="


def _relation_words(symbol):
    return {"<": "less than", ">": "greater than", "=": "equal to"}[symbol]


def _round_ten(value):
    return 10 * ((int(value) + 5) // 10)


class MagnitudeComparisonGenerator(ProblemGenerator):
    """Generate comparison-first reasoning followed by exact checks."""

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
    def _benchmark_fraction():
        benchmark = random.choice(BENCHMARKS)
        denominator = random.randint(7, 40)
        while True:
            numerator = random.randint(1, denominator - 1)
            value = Fraction(numerator, denominator)
            if value != benchmark:
                break
        left_cross = numerator * benchmark.denominator
        right_cross = benchmark.numerator * denominator
        symbol = _relation(value, benchmark)
        words = _relation_words(symbol)
        fraction_text = f"{numerator}/{denominator}"
        benchmark_text = f"{benchmark.numerator}/{benchmark.denominator}"
        facts = (f"A tank contains {numerator} filled sections out of "
                 f"{denominator} equal sections. Compare that share with "
                 f"{benchmark_text} of the tank.")
        question = "Is the recorded share less, equal, or greater, and what integer check proves it?"
        answer = (f"{words} {benchmark_text}; {left_cross} {symbol} "
                  f"{right_cross}")
        model = f"{fraction_text} {symbol} {benchmark_text}"
        steps = [step("M", numerator, benchmark.denominator, left_cross),
                 step("M", benchmark.numerator, denominator, right_cross),
                 step("BOUND", fraction_text, f"{symbol} {benchmark_text}",
                      f"{left_cross} {symbol} {right_cross}"),
                 step("CMP", fraction_text, benchmark_text, symbol),
                 step("CHECK", "integer products",
                      f"{left_cross} {symbol} {right_cross}")]
        used = [f"{numerator} filled", f"{denominator} total",
                f"comparison {benchmark_text}"]
        return facts, question, steps, answer, value, model, used, exact

    @staticmethod
    def _compare_without_computing():
        while True:
            tenth = random.randint(2, 8)
            divisor = random.randint(2, 6)
            left_factor = Fraction(tenth, 10)
            right_factor = Fraction(1, divisor)
            if left_factor != right_factor:
                break
        base = math.lcm(10, divisor) * random.randint(3, 20)
        left_value = left_factor * base
        right_value = Fraction(base, divisor)
        left_expr = f"{exact(left_factor)} × {base}"
        right_expr = f"{base} ÷ {divisor}"
        symbol = _relation(left_value, right_value)
        if left_value > right_value:
            larger_expr, larger_value = left_expr, left_value
            smaller_value = right_value
        else:
            larger_expr, larger_value = right_expr, right_value
            smaller_value = left_value
        facts = f"The two expressions are {left_expr} and {right_expr}."
        question = "Which is larger from the multipliers' sizes, and what exact values confirm it?"
        answer = (f"{larger_expr}; {exact(larger_value)} > "
                  f"{exact(smaller_value)}")
        model = f"{left_expr} {symbol} {right_expr}"
        steps = [step("BOUND", right_expr,
                      f"= (1/{divisor}) × {base}", "exact"),
                 step("BOUND", left_expr, f"{symbol} (1/{divisor}) × {base}",
                      f"{exact(left_factor)} {symbol} 1/{divisor}"),
                 step("M", exact(left_factor), base, exact(left_value)),
                 step("D", base, divisor, exact(right_value)),
                 step("CMP", left_expr, right_expr, symbol),
                 step("CHECK", "exact values",
                      f"{exact(left_value)} vs {exact(right_value)}")]
        used = [left_expr, right_expr]
        return (facts, question, steps, answer, larger_value, model, used,
                exact)

    @staticmethod
    def _order_of_magnitude():
        first_mantissa = Fraction(random.randint(12, 95), 10)
        second_mantissa = Fraction(random.randint(12, 95), 10)
        first_exp = random.randint(2, 4)
        second_exp = random.randint(2, 3)
        first_count = first_mantissa * 10 ** first_exp
        per_person = second_mantissa * 10 ** second_exp
        total = first_count * per_person
        raw_mantissa = first_mantissa * second_mantissa
        raw_exp = first_exp + second_exp
        digits = len(str(total.numerator // total.denominator)) - 1
        normalized = total / 10 ** digits
        facts = (f"A region has about {exact(first_mantissa)} × 10^{first_exp} "
                 f"residents, and a program costs {exact(second_mantissa)} × "
                 f"10^{second_exp} dollars per resident.")
        question = "Which power of ten describes the total-dollar scale, and what exact total checks it?"
        answer = f"10^{digits} dollars; exact {money(total)}"
        model = (f"({exact(first_mantissa)} × 10^{first_exp})"
                 f"({exact(second_mantissa)} × 10^{second_exp}) = "
                 f"{exact(normalized)} × 10^{digits}")
        steps = [step("E", 10, first_exp, 10 ** first_exp),
                 step("M", exact(first_mantissa), 10 ** first_exp,
                      exact(first_count)),
                 step("E", 10, second_exp, 10 ** second_exp),
                 step("M", exact(second_mantissa), 10 ** second_exp,
                      exact(per_person)),
                 step("M", exact(first_count), exact(per_person), exact(total)),
                 step("M", exact(first_mantissa), exact(second_mantissa),
                      exact(raw_mantissa)),
                 step("A", first_exp, second_exp, raw_exp),
                 step("ORDER_MAG", money(total), f"10^{digits} dollars",
                      f"{exact(normalized)} × 10^{digits}"),
                 step("CHECK", "exact total", money(total))]
        used = [f"{exact(first_mantissa)} × 10^{first_exp} residents",
                f"{exact(second_mantissa)} × 10^{second_exp} dollars each"]
        return facts, question, steps, answer, total, model, used, money

    @staticmethod
    def _reasonable_answer():
        family = random.choice(("cost", "travel", "area"))
        claim_correct = random.choice((True, False))
        if family == "cost":
            count = random.randint(4, 30)
            price = Fraction(random.randrange(8, 81), 4)
            value = count * price
            claim = value if claim_correct else value * 10
            correct, claim_text = money(value), money(claim)
            facts = (f"A shopper buys {count} identical notebooks at "
                     f"{money(price)} each. A report gives the total as "
                     f"{claim_text}.")
            model = f"c = {count} × {exact(price)} = {correct}"
            steps = [step("M", count, exact(price), exact(value))]
            used = [f"{count} notebooks", f"{money(price)} each",
                    f"claim {claim_text}"]
            renderer = money
        elif family == "travel":
            speed = random.randrange(25, 91, 5)
            elapsed = random.randint(2, 8)
            value = Fraction(speed * elapsed)
            claim = value if claim_correct else value / 10
            correct, claim_text = unit(value, "km"), unit(claim, "km")
            facts = (f"A bus travels at {speed} km/h for {elapsed} hours. A "
                     f"report gives the distance as {claim_text}.")
            model = f"d = {speed} × {elapsed} = {correct}"
            steps = [step("M", speed, elapsed, exact(value))]
            used = [f"speed {speed} km/h", f"time {elapsed} hours",
                    f"claim {claim_text}"]
            renderer = lambda item: unit(item, "km")
        else:
            length, width = random.sample(range(3, 21), 2)
            value = Fraction(length * width)
            claim = value if claim_correct else value * 10
            correct, claim_text = unit(value, "m²"), unit(claim, "m²")
            facts = (f"A rectangular floor is {length} m by {width} m. A report "
                     f"gives the covered surface as {claim_text}.")
            model = f"q = {length} × {width} = {correct}"
            steps = [step("M", length, width, exact(value))]
            used = [f"length {length} m", f"width {width} m",
                    f"claim {claim_text}"]
            renderer = lambda item: unit(item, "m²")
        verdict = "reasonable" if claim_correct else "unreasonable"
        question = "Is the reported result a reasonable size, and what exact result verifies it?"
        answer = f"{verdict}; correct {correct}"
        steps += [step("BOUND", "expected scale", correct,
                       "same scale" if claim_correct else "claim is off by factor 10"),
                  step("PLAUSIBLE", "yes" if claim_correct else "no",
                       "claim matches exact size" if claim_correct else
                       "claim differs by a factor of 10"),
                  step("CHECK", f"claim {claim_text}", f"correct {correct}",
                       verdict)]
        return facts, question, steps, answer, value, model, used, renderer

    @staticmethod
    def _bigger_product_or_quotient():
        base = random.randrange(20, 241, 5)
        factor = random.choice(FACTORS)
        product = base * factor
        quotient = base / factor
        factor_text = exact(factor)
        product_expr = f"{base} × {factor_text}"
        quotient_expr = f"{base} ÷ {factor_text}"
        symbol = _relation(product, quotient)
        if product > quotient:
            larger_expr, larger_value, smaller_value = product_expr, product, quotient
        else:
            larger_expr, larger_value, smaller_value = quotient_expr, quotient, product
        facts = (f"The same positive number {base} is multiplied by "
                 f"{factor_text} in one expression and divided by "
                 f"{factor_text} in another.")
        question = "Which expression is larger, and what exact values confirm the direction?"
        answer = (f"{larger_expr}; {exact(larger_value)} > "
                  f"{exact(smaller_value)}")
        model = f"{product_expr} {symbol} {quotient_expr}"
        steps = [step("BOUND", factor_text,
                      "> 1" if factor > 1 else "< 1",
                      "multiplication and division move in opposite directions"),
                 step("M", base, factor_text, exact(product)),
                 step("D", base, factor_text, exact(quotient)),
                 step("CMP", product_expr, quotient_expr, symbol),
                 step("CHECK", "exact values",
                      f"{exact(product)} vs {exact(quotient)}")]
        used = [f"base {base}", f"factor {factor_text}"]
        return facts, question, steps, answer, larger_value, model, used, exact

    @staticmethod
    def _estimate_then_verify():
        first, second = random.randint(21, 99), random.randint(21, 99)
        first_rounded, second_rounded = _round_ten(first), _round_ten(second)
        estimate = first_rounded * second_rounded
        value = first * second
        facts = (f"A size check is needed for {first} × {second}. Round each "
                 "factor to the nearest ten before finding the exact product.")
        question = "What estimate comes first, and what exact value verifies it?"
        answer = f"about {estimate}; exact {value}"
        model = f"{first} × {second} ≈ {first_rounded} × {second_rounded} = {estimate}"
        steps = [step("ESTIMATE", f"{first} ≈ {first_rounded}, "
                      f"{second} ≈ {second_rounded}", estimate),
                 step("M", first, second, value),
                 step("ESTIMATE_CHECK", estimate, value,
                      f"exact {value} has the predicted scale")]
        used = [f"factor {first}", f"factor {second}"]
        return facts, question, steps, answer, Fraction(value), model, used, exact

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
            extra = random.choice([number for number in range(141, 441)
                                   if number not in occupied])
            problem = f"A nearby display lists {extra} archived tickets. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"{extra} archived tickets"))
        elif modifier == "estimate_first" and variant != "estimate_then_verify":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "predict the scale before the exact comparison",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "comparison or scale relationship"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_magnitude_comparison_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
