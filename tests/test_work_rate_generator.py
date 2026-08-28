"""Alternate-route problem-only oracles for WorkRateGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.work_rate_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    WorkRateGenerator,
)
from helpers import DELIM


def clean(problem):
    return re.sub(r"^A storage shelf holds \d+ labels\. ", "", problem)


def hours(value):
    value = Fraction(value)
    if value.denominator == 2:
        text = f"{value.numerator // 2}.5"
    else:
        text = str(value)
    return f"{text} hour" if value == 1 else f"{text} hours"


def solve(problem):
    text = clean(problem)
    match = re.search(r"pump fills one tank in (\d+) hours.*?drains a full "
                      r"tank in (\d+) hours", text, re.I)
    if match:
        fill, drain = map(int, match.groups())
        # Integer-job route: the pump adds drain units and the valve removes
        # fill units during lcm(fill, drain) hours.
        job = math.lcm(fill, drain)
        value = Fraction(job, job // fill - job // drain)
        model = f"1/{fill} - 1/{drain} = 1/t"
        return "fill_and_drain", hours(value), model

    match = re.search(r"alone can each .*? in (\d+), (\d+), and (\d+) "
                      r"hours respectively", text, re.I)
    if match:
        a, b, c = map(int, match.groups())
        job = math.lcm(a, b, c)
        value = Fraction(job, job // a + job // b + job // c)
        model = f"1/{a} + 1/{b} + 1/{c} = 1/t"
        return "three_workers", hours(value), model

    match = re.search(r"completes (\d+)/(\d+) of an order in (\d+) hours",
                      text, re.I)
    if match:
        numerator, denominator, elapsed = map(int, match.groups())
        total = Fraction(elapsed * denominator, numerator)
        remaining = total - elapsed
        model = f"({numerator}/{denominator})/{elapsed} = 1/t"
        answer = f"{hours(total)} total; {hours(remaining)} remaining"
        return "partial_job", answer, model

    match = re.search(
        r"alone can .*? in (\d+) hours, and .*? alone needs (\d+) hours\. "
        r"They start together, but .*? leaves after (\d+) hours", text, re.I)
    if match:
        a, b, lead = map(int, match.groups())
        completed = lead * (Fraction(1, a) + Fraction(1, b))
        total = lead + (1 - completed) * a
        model = f"(1/{a} + 1/{b})*{lead} + (t-{lead})/{a} = 1"
        return "one_leaves_early", hours(total), model

    match = re.search(
        r"alone can .*? in (\d+) hours\. Working with .*?, the same job "
        r"takes ([0-9/]+) hours", text, re.I)
    if match:
        a, together = int(match.group(1)), Fraction(match.group(2))
        rate_b = Fraction(1, together) - Fraction(1, a)
        b = 1 / rate_b
        model = f"1/{a} + 1/b = 1/{together}"
        return "one_alone_unknown", hours(b), model

    match = re.search(
        r"alone can .*? in (\d+) hours\. .*? alone can .*? in (\d+) hours",
        text, re.I)
    if match:
        a, b = map(int, match.groups())
        job = math.lcm(a, b)
        together = Fraction(job, job // a + job // b)
        model = f"1/{a} + 1/{b} = 1/t"
        return "together", hours(together), model
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; t = {answer}"
    return variant, answer


class TestWorkRateGenerator(unittest.TestCase):
    def test_marker_contract_and_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(227)
        seen = set()
        for _ in range(1200):
            result = WorkRateGenerator().generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_work_rate_")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_five_renderings_preserve_parseable_facts(self):
        facts = ("Hose A alone can fill one pool in 6 hours. Hose B alone "
                 "can fill one pool in 3 hours.")
        question = "How many hours do they need when both run at once?"
        self.assertEqual(len(FRAMES), 5)
        for index, frame in enumerate(FRAMES):
            problem = frame.format(
                facts=facts, facts_lc=facts[:1].lower() + facts[1:],
                question=question, place="the garden",
                place_cap="The garden", record="A17")
            with self.subTest(rendering=index):
                self.assertEqual(solve(problem)[0], "together")

    def test_arithmetic_steps(self):
        for _ in range(700):
            result = WorkRateGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = WorkRateGenerator(variant, modifier).generate()
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
            WorkRateGenerator("bogus")
        with self.assertRaises(ValueError):
            WorkRateGenerator(modifier="bogus")

    def test_pipe_safety(self):
        for _ in range(500):
            result = WorkRateGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
