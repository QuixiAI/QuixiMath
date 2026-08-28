"""Check whether a quantitative premise is valid before calculating.

Variants: ``proportional_reasoning_with_fixed_cost``,
``independence_without_replacement``, ``triangle_inequality``,
``nonphysical_root``, ``normal_approx_small_n``,
``extrapolation_beyond_data``, ``division_by_zero_rate``, and
``average_of_averages``. Every variant emits both holding and failing cases,
uses five shared-context renderings, and supports all four applied modifiers.
Each story isolates exactly one premise. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``ASSUMPTION``, ``REWRITE``,
``ZERO_PRODUCT``, ``FLAG``, ``CMP``, ``A``, ``M``, ``D``, ``CHECK``, and
``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = (
    "proportional_reasoning_with_fixed_cost",
    "independence_without_replacement",
    "triangle_inequality",
    "nonphysical_root",
    "normal_approx_small_n",
    "extrapolation_beyond_data",
    "division_by_zero_rate",
    "average_of_averages",
)
FRAMES = (
    "At {place}, {name} checks a stated premise. {facts} {question}",
    "{question} A report given to {name} at {place} says: {facts}",
    "For {name} at {place}, the situation is this: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the report from {place} that {name} is auditing. {facts} "
    "{question}",
)
PLACES = tuple(
    setting
    for key in ("trip", "shop", "classroom", "lab", "workshop", "business")
    for setting in CONTEXTS[key].settings
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _label(holds):
    return "applies" if holds else "does not apply"


def _answer(holds, reason, correct):
    return f"{_label(holds)}; {reason}; correct {correct}"


def _factor(root):
    return f"(t - {root})" if root >= 0 else f"(t + {-root})"


class AssumptionCheckGenerator(ProblemGenerator):
    """Generate one-premise checks with exact corrections."""

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
    def _proportional_reasoning_with_fixed_cost():
        holds = random.choice((True, False))
        fixed = 0 if holds else random.randrange(2, 11)
        rate = random.randrange(2, 9)
        distance = random.randint(2, 10)
        target = 2 * distance
        first_cost = fixed + rate * distance
        claim = 2 * first_cost
        correct_cost = fixed + rate * target
        fee_text = ("no starting fee" if fixed == 0 else
                    f"a {money(fixed)} starting fee")
        facts = (f"A ride service charges {fee_text} plus {money(rate)} per km. "
                 f"A {distance} km ride costs {money(first_cost)}. "
                 f"{random.choice(NAMES)} says a {target} km ride costs "
                 f"{money(claim)} because the distance doubled.")
        question = "Does that doubling premise fit this price structure?"
        reason = ("no fixed fee" if holds else
                  f"fixed {money(fixed)} fee prevents direct scaling")
        correct = money(correct_cost)
        model = f"c = {fixed} + {rate}*{target} = {correct}"
        steps = [step("ASSUMPTION", "direct scaling", "holds" if holds else "fails",
                      reason),
                 step("M", rate, target, rate * target),
                 step("A", fixed, rate * target, correct_cost),
                 step("CMP", money(claim), correct,
                      "=" if holds else "≠")]
        used = [f"starting fee {money(fixed)}", f"rate {money(rate)}/km",
                f"distance {target} km", f"claim {money(claim)}"]
        return (facts, question, steps, _answer(holds, reason, correct),
                Fraction(correct_cost), model, used, money)

    @staticmethod
    def _independence_without_replacement():
        holds = random.choice((True, False))
        target = random.randint(2, 8)
        total = random.randint(target + 2, target + 10)
        first = Fraction(target, total)
        second = first if holds else Fraction(target - 1, total - 1)
        correct_value = first * second
        claimed = first * first
        action = ("returns it to the bag and mixes again" if holds else
                  "sets it aside before the second draw")
        facts = (f"A bag has {target} green tokens among {total} tokens. A person "
                 f"draws one token, {action}. {random.choice(NAMES)} multiplies "
                 f"{exact(first)} by {exact(first)} for the chance of two green "
                 "draws.")
        question = "Does the premise that the second chance is unchanged hold?"
        reason = ("first token is returned" if holds else
                  "first token is not returned, so the bag changes")
        correct = exact(correct_value)
        model = (f"p = {target}/{total}*{target if holds else target - 1}/"
                 f"{total if holds else total - 1} = {correct}")
        steps = [step("ASSUMPTION", "unchanged second chance",
                      "holds" if holds else "fails", reason),
                 step("M", exact(first), exact(second), correct),
                 step("CMP", exact(claimed), correct, "=" if holds else "≠"),
                 step("CHECK", "two green draws", correct)]
        used = [f"{target} green", f"{total} total",
                "returned first token" if holds else "first token set aside"]
        return (facts, question, steps, _answer(holds, reason, correct),
                correct_value, model, used, exact)

    @staticmethod
    def _triangle_inequality():
        holds = random.choice((True, False))
        first, second = sorted(random.sample(range(3, 15), 2))
        if holds:
            longest = random.randint(second, first + second - 1)
        else:
            longest = first + second + random.randint(1, 6)
        relation = ">" if holds else "<"
        sum_short = first + second
        facts = (f"Three rigid rods have lengths {first} cm, {second} cm, and "
                 f"{longest} cm. {random.choice(NAMES)} plans to join their ends "
                 "to make a triangular frame.")
        question = "Can the rods close into that frame?"
        reason = (f"{first} + {second} > {longest}" if holds else
                  f"{first} + {second} < {longest}")
        correct = "triangle possible" if holds else "no triangle"
        model = f"{first} + {second} {relation} {longest}"
        steps = [step("A", first, second, sum_short),
                 step("ASSUMPTION", "shorter sides exceed longest",
                      "holds" if holds else "fails", reason),
                 step("CMP", sum_short, longest, relation),
                 step("CHECK", "rod closure", correct)]
        used = [f"{first} cm", f"{second} cm", f"{longest} cm"]
        return (facts, question, steps, _answer(holds, reason, correct),
                Fraction(sum_short), model, used, exact)

    @staticmethod
    def _nonphysical_root():
        holds = random.choice((True, False))
        first = random.randint(1, 4) if holds else -random.randint(1, 4)
        second = random.randint(7, 10)
        roots = sorted((first, second))
        root_sum = sum(roots)
        product = roots[0] * roots[1]
        product_term = (f"+ {product}" if product > 0 else f"- {-product}")
        equation = f"t² - {root_sum}t {product_term} = 0"
        listed = f"t = {roots[0]} and t = {roots[1]}"
        facts = (f"A timing record defines t as hours after an observation "
                 f"starts and gives {equation}. {random.choice(NAMES)} lists "
                 f"{listed} and says both describe times in the record.")
        question = "Does the premise that both listed values are allowable hold?"
        physical = [root for root in roots if root >= 0]
        reason = ("both times are nonnegative" if holds else
                  f"{unit(roots[0], 'hour')} is before the observation starts")
        correct = " or ".join(f"t = {unit(root, 'hour')}" for root in physical)
        model = f"{equation}; t ≥ 0"
        factored = f"{_factor(roots[0])}{_factor(roots[1])} = 0"
        steps = [step("REWRITE", equation, factored),
                 step("ZERO_PRODUCT", factored, listed),
                 step("ASSUMPTION", "nonnegative elapsed time",
                      "holds" if holds else "fails", reason),
                 step("CHECK", "both roots satisfy the equation", "0, 0")]
        used = [equation, listed, "t is hours after start"]
        return (facts, question, steps, _answer(holds, reason, correct),
                Fraction(max(physical)), model, used,
                lambda value: unit(value, "hour"))

    @staticmethod
    def _normal_approx_small_n():
        holds = random.choice((True, False))
        choices = (10, 20, 25, 40, 50, 60, 75, 80, 90)
        while True:
            trials = random.randint(12, 120)
            percent = random.choice(choices)
            success = Fraction(trials * percent, 100)
            failure = trials - success
            if (success >= 10 and failure >= 10) == holds:
                break
        facts = (f"Across {trials} repeated trials, an event has a {percent}% "
                 f"chance each time. {random.choice(NAMES)} says both the "
                 "expected event count and expected non-event count are at "
                 "least 10.")
        question = "Do the two expected counts support that premise?"
        reason = ("both expected counts meet 10" if holds else
                  "at least one expected count is below 10")
        correct = f"expected counts {exact(success)} and {exact(failure)}"
        model = (f"counts = {trials}*{percent}/100, "
                 f"{trials}*(1-{percent}/100)")
        steps = [step("M", trials, exact(Fraction(percent, 100)), exact(success)),
                 step("M", trials, exact(Fraction(100 - percent, 100)),
                      exact(failure)),
                 step("ASSUMPTION", "both expected counts at least 10",
                      "holds" if holds else "fails", reason),
                 step("CMP", f"{exact(success)}, {exact(failure)}", "10",
                      "both ≥" if holds else "one <")]
        used = [f"{trials} trials", f"{percent}% event chance"]
        return (facts, question, steps, _answer(holds, reason, correct),
                min(success, failure), model, used, exact)

    @staticmethod
    def _extrapolation_beyond_data():
        holds = random.choice((True, False))
        low = random.randint(1, 10)
        high = low + random.randint(4, 12)
        rate = random.randint(2, 10)
        fixed = random.randint(1, 20)
        if holds:
            query = random.randint(low, high)
        else:
            query = random.choice((random.randint(max(0, low - 8), low - 1),
                                   random.randint(high + 1, high + 12)))
        low_y, high_y = fixed + rate * low, fixed + rate * high
        projected = fixed + rate * query
        facts = (f"Measurements cover inputs from {low} through {high}. The "
                 f"record includes ({low}, {low_y}) and ({high}, {high_y}), "
                 f"with output changing by {rate} per input. "
                 f"{random.choice(NAMES)} uses the record at input {query} and "
                 "says that input is inside the measured span.")
        question = "Does that location premise hold?"
        reason = (f"input {query} lies within [{low}, {high}]" if holds else
                  f"input {query} lies outside [{low}, {high}]")
        correct = f"projected y = {projected}"
        model = f"y = {fixed} + {rate}*{query} = {projected}"
        steps = [step("ASSUMPTION", "query inside measured span",
                      "holds" if holds else "fails", reason),
                 step("M", rate, query, rate * query),
                 step("A", fixed, rate * query, projected),
                 step("CHECK", f"input {query}", f"range [{low}, {high}]",
                      "inside" if holds else "outside")]
        used = [f"input range {low} to {high}", f"change {rate}",
                f"query {query}"]
        return (facts, question, steps, _answer(holds, reason, correct),
                Fraction(projected), model, used, exact)

    @staticmethod
    def _division_by_zero_rate():
        holds = random.choice((True, False))
        distance = random.randrange(20, 241, 10)
        elapsed = random.randint(1, 6) if holds else 0
        facts = (f"A sensor records a distance change of {distance} km over "
                 f"{unit(elapsed, 'hour')}. {random.choice(NAMES)} wants to report the "
                 "distance change per hour by dividing those two readings.")
        question = "Is the required division defined for this record?"
        reason = ("elapsed time is nonzero" if holds else
                  "elapsed time is 0")
        if holds:
            value = Fraction(distance, elapsed)
            correct = unit(value, "km/h")
            steps = [step("ASSUMPTION", "nonzero denominator", "holds", reason),
                     step("D", distance, elapsed, exact(value)),
                     step("CHECK", f"{distance}/{elapsed}", correct)]
            renderer = lambda item: unit(item, "km/h")
        else:
            value = Fraction(0)
            correct = "undefined km/h"
            steps = [step("ASSUMPTION", "nonzero denominator", "fails", reason),
                     step("FLAG", f"{distance}/0", "undefined"),
                     step("CHECK", "division by zero", correct)]
            renderer = lambda item: "undefined"
        model = f"r = {distance}/{elapsed} = {correct}"
        used = [f"distance change {distance} km", f"elapsed {elapsed} hours"]
        return (facts, question, steps, _answer(holds, reason, correct),
                value, model, used, renderer)

    @staticmethod
    def _average_of_averages():
        holds = random.choice((True, False))
        first_count = random.randint(4, 20)
        if holds:
            second_count = first_count
        else:
            second_count = random.choice(
                [count for count in range(4, 21) if count != first_count])
        first_average, second_average = random.sample(range(60, 96), 2)
        claimed = Fraction(first_average + second_average, 2)
        total = (first_count * first_average +
                 second_count * second_average)
        count = first_count + second_count
        correct_value = Fraction(total, count)
        facts = (f"Group A has {first_count} scores with average "
                 f"{first_average}. Group B has {second_count} scores with "
                 f"average {second_average}. {random.choice(NAMES)} says the "
                 f"overall average is {exact(claimed)} by averaging the two "
                 "displayed averages.")
        question = "Does treating the two displayed averages equally apply?"
        reason = ("group sizes are equal" if holds else
                  "group sizes differ, so the groups need different weights")
        correct = f"overall average {exact(correct_value)}"
        model = (f"a = ({first_count}*{first_average} + "
                 f"{second_count}*{second_average})/{count} = "
                 f"{exact(correct_value)}")
        first_total, second_total = (first_count * first_average,
                                     second_count * second_average)
        steps = [step("ASSUMPTION", "equal group weights",
                      "holds" if holds else "fails", reason),
                 step("M", first_count, first_average, first_total),
                 step("M", second_count, second_average, second_total),
                 step("A", first_total, second_total, total),
                 step("A", first_count, second_count, count),
                 step("D", total, count, exact(correct_value)),
                 step("CMP", exact(claimed), exact(correct_value),
                      "=" if holds else "≠")]
        used = [f"group A {first_count} at {first_average}",
                f"group B {second_count} at {second_average}"]
        return (facts, question, steps, _answer(holds, reason, correct),
                correct_value, model, used, exact)

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
            extra = random.choice([number for number in range(121, 421)
                                   if number not in occupied])
            problem = f"A wall chart nearby shows {extra} archived entries. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"{extra} archived entries"))
        elif modifier == "estimate_first":
            if variant == "division_by_zero_rate" and "undefined" in answer:
                steps.insert(0, step("ESTIMATE", "inspect the denominator",
                                     "undefined when elapsed time is zero"))
                steps.append(step("ESTIMATE_CHECK", "undefined",
                                  "undefined km/h",
                                  "zero denominator confirmed"))
            else:
                steps = estimate_first(
                    steps + [step("Z", answer)], value,
                    "check the premise before approximating the corrected result",
                    render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "relationship after checking the premise"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_assumption_check_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
