"""Problem-text-only oracles for :class:`AssumptionCheckGenerator`."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.assumption_check_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    AssumptionCheckGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


def exact_text(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return (str(value.numerator) if value.denominator == 1 else
                f"{value.numerator}/{value.denominator}")
    scaled, places = value, 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return sign + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def unit_text(value, name):
    value = Fraction(value)
    text = exact_text(value)
    if "/" in name:
        return f"{text} {name}"
    return f"{text} {name if abs(value) == 1 else name + 's'}"


def clean(problem):
    return re.sub(r"^A wall chart nearby shows \d+ archived entries\. ", "",
                  problem)


def solved(variant, holds, reason, correct, model, value):
    label = "applies" if holds else "does not apply"
    return variant, holds, f"{label}; {reason}; correct {correct}", model, value


def solve(problem):
    """Identify the sole premise and recompute its correction independently."""
    text = clean(problem)

    match = re.search(
        r"ride service charges (no starting fee|a \$[0-9.]+ starting fee) "
        r"plus (\$[0-9.]+) per km.*?says a (\d+) km ride costs "
        r"(\$[0-9.]+)", text, re.I)
    if match:
        fee_phrase, rate_token, target_token, claim_token = match.groups()
        fixed = Fraction(0) if fee_phrase.lower().startswith("no") else number(
            re.search(r"\$[0-9.]+", fee_phrase).group())
        rate, target, claim = number(rate_token), int(target_token), number(claim_token)
        correct_value = fixed + rate * target
        holds = claim == correct_value
        reason = ("no fixed fee" if holds else
                  f"fixed {money_text(fixed)} fee prevents direct scaling")
        correct = money_text(correct_value)
        model = (f"c = {exact_text(fixed)} + {exact_text(rate)}*{target} = "
                 f"{correct}")
        return solved("proportional_reasoning_with_fixed_cost", holds, reason,
                      correct, model, correct_value)

    match = re.search(
        r"bag has (\d+) green tokens among (\d+) tokens.*?draws one token, "
        r"(returns it to the bag and mixes again|sets it aside before the "
        r"second draw)", text, re.I)
    if match:
        target, total = map(int, match.groups()[:2])
        returned = match.group(3).lower().startswith("returns")
        first = Fraction(target, total)
        second = first if returned else Fraction(target - 1, total - 1)
        value = first * second
        reason = ("first token is returned" if returned else
                  "first token is not returned, so the bag changes")
        correct = exact_text(value)
        model = (f"p = {target}/{total}*{target if returned else target - 1}/"
                 f"{total if returned else total - 1} = {correct}")
        return solved("independence_without_replacement", returned, reason,
                      correct, model, value)

    match = re.search(
        r"rods have lengths (\d+) cm, (\d+) cm, and (\d+) cm", text, re.I)
    if match:
        sides = sorted(map(int, match.groups()))
        short_sum, longest = sides[0] + sides[1], sides[2]
        holds = short_sum > longest
        relation = ">" if holds else "<"
        reason = f"{sides[0]} + {sides[1]} {relation} {longest}"
        correct = "triangle possible" if holds else "no triangle"
        model = reason
        return solved("triangle_inequality", holds, reason, correct, model,
                      Fraction(short_sum))

    match = re.search(
        r"gives t² - (\d+)t ([+-]) (\d+) = 0.*?lists t = (-?\d+) and "
        r"t = (-?\d+)", text, re.I)
    if match:
        coefficient, sign, magnitude, listed_first, listed_second = match.groups()
        b = -int(coefficient)
        c = int(magnitude) if sign == "+" else -int(magnitude)
        discriminant = b * b - 4 * c
        root_disc = math.isqrt(discriminant)
        if root_disc * root_disc != discriminant:
            raise AssertionError("story polynomial lacks integer roots")
        roots = sorted((Fraction(-b - root_disc, 2),
                        Fraction(-b + root_disc, 2)))
        listed = sorted((Fraction(listed_first), Fraction(listed_second)))
        if roots != listed:
            raise AssertionError(f"listed roots {listed} differ from {roots}")
        physical = [root for root in roots if root >= 0]
        holds = len(physical) == 2
        reason = ("both times are nonnegative" if holds else
                  f"{unit_text(roots[0], 'hour')} is before the observation starts")
        correct = " or ".join(f"t = {unit_text(root, 'hour')}"
                              for root in physical)
        equation = f"t² - {coefficient}t {sign} {magnitude} = 0"
        model = f"{equation}; t ≥ 0"
        return solved("nonphysical_root", holds, reason, correct, model,
                      max(physical))

    match = re.search(
        r"Across (\d+) repeated trials, an event has a (\d+)% chance", text,
        re.I)
    if match:
        trials, percent = map(int, match.groups())
        success = Fraction(trials * percent, 100)
        failure = trials - success
        holds = success >= 10 and failure >= 10
        reason = ("both expected counts meet 10" if holds else
                  "at least one expected count is below 10")
        correct = f"expected counts {exact_text(success)} and {exact_text(failure)}"
        model = (f"counts = {trials}*{percent}/100, "
                 f"{trials}*(1-{percent}/100)")
        return solved("normal_approx_small_n", holds, reason, correct, model,
                      min(success, failure))

    match = re.search(
        r"Measurements cover inputs from (\d+) through (\d+).*?includes "
        r"\((\d+), (\d+)\) and \((\d+), (\d+)\), with output changing by "
        r"(\d+) per input.*?uses the record at input (\d+)", text, re.I)
    if match:
        low, high, x1, y1, x2, y2, stated_rate, query = map(int, match.groups())
        rate = Fraction(y2 - y1, x2 - x1)
        if rate != stated_rate or (x1, x2) != (low, high):
            raise AssertionError("inconsistent measurement record")
        fixed = y1 - rate * x1
        projected = fixed + rate * query
        holds = low <= query <= high
        reason = (f"input {query} lies within [{low}, {high}]" if holds else
                  f"input {query} lies outside [{low}, {high}]")
        correct = f"projected y = {exact_text(projected)}"
        model = (f"y = {exact_text(fixed)} + {exact_text(rate)}*{query} = "
                 f"{exact_text(projected)}")
        return solved("extrapolation_beyond_data", holds, reason, correct,
                      model, projected)

    match = re.search(
        r"distance change of (\d+) km over (\d+) hours?", text, re.I)
    if match:
        distance, elapsed = map(int, match.groups())
        holds = elapsed != 0
        reason = "elapsed time is nonzero" if holds else "elapsed time is 0"
        if holds:
            value = Fraction(distance, elapsed)
            correct = unit_text(value, "km/h")
        else:
            value = Fraction(0)
            correct = "undefined km/h"
        model = f"r = {distance}/{elapsed} = {correct}"
        return solved("division_by_zero_rate", holds, reason, correct, model,
                      value)

    match = re.search(
        r"Group A has (\d+) scores with average (\d+)\. Group B has (\d+) "
        r"scores with average (\d+)", text, re.I)
    if match:
        first_count, first_average, second_count, second_average = map(
            int, match.groups())
        total = first_count * first_average + second_count * second_average
        count = first_count + second_count
        value = Fraction(total, count)
        holds = first_count == second_count
        reason = ("group sizes are equal" if holds else
                  "group sizes differ, so the groups need different weights")
        correct = f"overall average {exact_text(value)}"
        model = (f"a = ({first_count}*{first_average} + "
                 f"{second_count}*{second_average})/{count} = "
                 f"{exact_text(value)}")
        return solved("average_of_averages", holds, reason, correct, model,
                      value)

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, holds, answer, model, value = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, holds, answer, model, value


class TestAssumptionCheckGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(278)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(18):
                    result = AssumptionCheckGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, _, answer, model, _ = expected(
                        result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer,
                                     result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1],
                                         model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "proportional_reasoning_with_fixed_cost": (
                "A ride service charges a $3.00 starting fee plus $2.00 per km. "
                "A 5 km ride costs $13.00. Sara says a 10 km ride costs $26.00 "
                "because the distance doubled."),
            "independence_without_replacement": (
                "A bag has 4 green tokens among 10 tokens. A person draws one "
                "token, sets it aside before the second draw. Sara multiplies "
                "2/5 by 2/5 for the chance of two green draws."),
            "triangle_inequality": (
                "Three rigid rods have lengths 3 cm, 4 cm, and 8 cm. Sara plans "
                "to join their ends to make a triangular frame."),
            "nonphysical_root": (
                "A timing record defines t as hours after an observation starts "
                "and gives t² - 3t - 10 = 0. Sara lists t = -2 and t = 5 and "
                "says both describe times in the record."),
            "normal_approx_small_n": (
                "Across 20 repeated trials, an event has a 25% chance each time. "
                "Sara says both the expected event count and expected non-event "
                "count are at least 10."),
            "extrapolation_beyond_data": (
                "Measurements cover inputs from 2 through 8. The record includes "
                "(2, 7) and (8, 19), with output changing by 2 per input. Sara "
                "uses the record at input 12 and says that input is inside the "
                "measured span."),
            "division_by_zero_rate": (
                "A sensor records a distance change of 120 km over 0 hours. Sara "
                "wants to report the distance change per hour by dividing those "
                "two readings."),
            "average_of_averages": (
                "Group A has 10 scores with average 80. Group B has 20 scores "
                "with average 90. Sara says the overall average is 85 by "
                "averaging the two displayed averages."),
        }
        question = "Does the stated premise hold?"
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_every_variant_reaches_holds_and_fails(self):
        random.seed(279)
        for variant in VARIANTS:
            outcomes = set()
            for _ in range(180):
                result = AssumptionCheckGenerator(variant, "plain").generate()
                outcomes.add(solve(result["problem"])[1])
            self.assertEqual(outcomes, {False, True}, variant)

    def test_arithmetic_steps_and_single_assumption(self):
        random.seed(280)
        for _ in range(1500):
            result = AssumptionCheckGenerator().generate()
            assumptions = []
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "ASSUMPTION":
                    assumptions.append(fields)
                elif fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)
            self.assertEqual(len(assumptions), 1)
            holds = solve(result["problem"])[1]
            self.assertEqual(assumptions[0][2], "holds" if holds else "fails")

    def test_modifier_shapes_operation_and_invalid_inputs(self):
        random.seed(281)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = AssumptionCheckGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(
                    result["operation"],
                    f"applied_assumption_check_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            AssumptionCheckGenerator("bogus")
        with self.assertRaises(ValueError):
            AssumptionCheckGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(282)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = AssumptionCheckGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
