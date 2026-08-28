"""Problem-text-only oracles for :class:`LinearModelWordGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.linear_model_word_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    LinearModelWordGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", ""))


def money(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not an exact cent amount: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def clean(problem):
    return re.sub(r"^A nearby shelf holds \d+ unused folders\. ", "", problem)


def solve(problem):
    """Parse the printed situation and recompute by elementary differences."""
    text = clean(problem)

    match = re.search(
        r"repair service charges a (\$\d+\.\d{2}) call-out fee plus "
        r"(\$\d+\.\d{2}) per hour\. A repair takes (\d+) hours", text, re.I)
    if match:
        fixed, rate, elapsed = number(match.group(1)), number(match.group(2)), int(match.group(3))
        total = fixed + rate * elapsed
        model = f"C = {fixed} + {rate}h"
        return "evaluate", money(total), model

    match = re.search(
        r"repair service charges a (\$\d+\.\d{2}) call-out fee plus "
        r"(\$\d+\.\d{2}) per hour\. A completed repair has a bill of "
        r"(\$\d+\.\d{2})", text, re.I)
    if match:
        fixed, rate, total = map(number, match.groups())
        elapsed = (total - fixed) / rate
        word = "hour" if elapsed == 1 else "hours"
        model = f"{fixed} + {rate}h = {total}"
        return "invert", f"{elapsed} {word}", model

    match = re.search(
        r"printer charges (\$\d+\.\d{2}) for (\d+) posters and "
        r"(\$\d+\.\d{2}) for (\d+) posters", text, re.I)
    if match:
        cost1, count1, cost2, count2 = match.groups()
        cost1, cost2 = number(cost1), number(cost2)
        count1, count2 = int(count1), int(count2)
        rate = (cost2 - cost1) / (count2 - count1)
        fixed = cost1 - rate * count1
        model = f"C = {fixed} + {rate}n"
        answer = f"{money(fixed)} fixed; {money(rate)} per poster"
        return "from_two_points", answer, model

    match = re.search(
        r"stall pays (\$\d+\.\d{2}) before opening\. Each item then costs "
        r"(\$\d+\.\d{2}) to make and sells for (\$\d+\.\d{2})", text, re.I)
    if match:
        fixed, cost, price = map(number, match.groups())
        units = fixed / (price - cost)
        revenue = units * price
        model = f"{price}x = {fixed} + {cost}x"
        return ("break_even",
                f"{units} items; {money(revenue)} income and cost", model)

    match = re.search(
        r"plan A costs (\$\d+\.\d{2}) plus (\$\d+\.\d{2}) per minute\. "
        r"Plan B costs (\$\d+\.\d{2})", text, re.I)
    if match:
        fixed, rate, flat = map(number, match.groups())
        crossing = (flat - fixed) / rate
        model = f"{fixed} + {rate}m = {flat}"
        answer = (f"plan B beyond {crossing} minutes; break-even "
                  f"{crossing} minutes")
        return "compare_plans", answer, model

    equation = re.search(
        r"bill is described by C = (\d+) \+ (\d+)h, where C is the cost in "
        r"dollars and h is the number of hours", text, re.I)
    question = re.search(r"what is the cost for (\d+) hours", text, re.I)
    if equation and question:
        fixed, rate = map(int, equation.groups())
        elapsed = int(question.group(1))
        total = fixed + rate * elapsed
        model = f"C = {fixed} + {rate}h"
        answer = (f"{money(fixed)} fixed booking charge; {money(rate)} per "
                  f"hour; {money(total)} for {elapsed} hours")
        return "interpret_parts", answer, model
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        if variant in ("from_two_points", "interpret_parts"):
            answer = f"{model}; {answer}"
        elif variant == "compare_plans":
            crossing = re.search(r"break-even ([0-9/]+) minutes", answer).group(1)
            answer = (f"{model}; m = {crossing} minutes; plan B costs less "
                      f"beyond {crossing} minutes")
        else:
            variable = {"evaluate": "C", "invert": "h", "break_even": "x"}[variant]
            answer = f"{model}; {variable} = {answer}"
    return variant, answer


class TestLinearModelWordGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(237)
        seen = set()
        for _ in range(1200):
            result = LinearModelWordGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_linear_model_")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_preserve_every_template(self):
        cases = (
            ("A repair service charges a $40.00 call-out fee plus $25.00 per "
             "hour. A repair takes 6 hours.", "What is the total bill?", "evaluate"),
            ("A repair service charges a $40.00 call-out fee plus $25.00 per "
             "hour. A completed repair has a bill of $190.00.",
             "How many hours of work were billed?", "invert"),
            ("A printer charges $20.00 for 5 posters and $32.00 for 8 posters. "
             "The charge changes by the same amount for each additional poster.",
             "What are the fixed fee and the charge per poster?", "from_two_points"),
            ("A market stall pays $100.00 before opening. Each item then costs "
             "$5.00 to make and sells for $10.00.",
             "How many items must be sold for sales income to equal all costs?",
             "break_even"),
            ("Phone plan A costs $30.00 plus $0.10 per minute. Plan B costs "
             "$50.00 with no added charge for minutes.",
             "When do the plans cost the same, and which plan costs less beyond that?",
             "compare_plans"),
            ("A delivery company's bill is described by C = 40 + 25h, where C "
             "is the cost in dollars and h is the number of hours.",
             "What do 40 and 25 mean, and what is the cost for 6 hours?",
             "interpret_parts"),
        )
        self.assertEqual(len(FRAMES), 5)
        for facts, question, variant in cases:
            for index, frame in enumerate(FRAMES):
                problem = frame.format(
                    facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                    question=question, place="the market stand", record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(238)
        for _ in range(700):
            result = LinearModelWordGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(239)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = LinearModelWordGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            LinearModelWordGenerator("bogus")
        with self.assertRaises(ValueError):
            LinearModelWordGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(240)
        banned = ("^1", "+ 0", "--", "the the")
        for _ in range(500):
            result = LinearModelWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)-?1x\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
