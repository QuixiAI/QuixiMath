"""Brute-force problem-text oracles for IntegerPuzzleWordGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.integer_puzzle_word_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    IntegerPuzzleWordGenerator,
)
from helpers import DELIM


def core(problem):
    return re.sub(r"^A notice board lists \d+ events\. ", "", problem)


def solve(problem):
    text = core(problem)
    match = re.search(
        r"([A-Z][a-z]+) is (\d+) years older than twice "
        r"([A-Z][a-z]+)'s age.*?total (\d+) years", text, re.I)
    if match:
        first, offset, second, total = match.groups()
        offset, total = int(offset), int(total)
        answers = [(a, b) for a in range(0, 101) for b in range(0, 101)
                   if a == 2 * b + offset and a + b == total]
        (older, younger), = answers
        model = f"b + (2b + {offset}) = {total}"
        return "age_now", f"{first.title()} {older} years; {second.title()} {younger} years", model

    match = re.search(
        r"([A-Z][a-z]+) is (\d+) years older than ([A-Z][a-z]+)\. "
        r"In (\d+) years their ages will total (\d+) years", text, re.I)
    if match:
        first, gap, second, years, total = match.groups()
        gap, years, total = map(int, (gap, years, total))
        answers = [(a, b) for a in range(0, 101) for b in range(0, 101)
                   if a == b + gap and a + years + b + years == total]
        (older, younger), = answers
        model = f"b + (b + {gap}) + 2*{years} = {total}"
        return "age_future", f"{first.title()} {older} years; {second.title()} {younger} years", model

    match = re.search(r"Three consecutive (even|odd) integers have sum (-?\d+)",
                      text, re.I)
    if match:
        kind, total = match.group(1).lower(), int(match.group(2))
        parity = 0 if kind == "even" else 1
        answers = [(x, x + 2, x + 4) for x in range(-100, 101)
                   if x % 2 == parity and 3 * x + 6 == total]
        values, = answers
        model = f"x + (x + 2) + (x + 4) = {total}"
        return "consecutive_even_odd", ", ".join(map(str, values)), model

    match = re.search(r"Three consecutive integers have sum (-?\d+)", text,
                      re.I)
    if match:
        total = int(match.group(1))
        answers = [(x, x + 1, x + 2) for x in range(-100, 101)
                   if 3 * x + 3 == total]
        values, = answers
        model = f"x + (x + 1) + (x + 2) = {total}"
        return "consecutive_integers", ", ".join(map(str, values)), model

    match = re.search(r"contains (\d+) nickels and dimes worth (\d+) cents",
                      text, re.I)
    if match:
        count, cents = map(int, match.groups())
        answers = [(n, d) for n in range(count + 1) for d in range(count + 1)
                   if n + d == count and 5 * n + 10 * d == cents]
        (nickels, dimes), = answers
        model = f"n + d = {count}; 5n + 10d = {cents}"
        return "coins_count_value", f"nickels {nickels}; dimes {dimes}", model

    match = re.search(
        r"larger of two integers is (\d+) more than (\d+) times the smaller\. "
        r"Their sum is (-?\d+)", text, re.I)
    if match:
        offset, multiplier, total = map(int, match.groups())
        answers = [(x, y) for x in range(-100, 101) for y in range(-100, 201)
                   if y == multiplier * x + offset and x + y == total and y > x]
        (smaller, larger), = answers
        model = f"x + ({multiplier}x + {offset}) = {total}"
        return "number_relationship", f"smaller {smaller}; larger {larger}", model

    match = re.search(
        r"two-digit number has digit sum (\d+)\. It is (\d+) greater than "
        r"the number made by reversing its digits", text, re.I)
    if match:
        digit_sum, difference = map(int, match.groups())
        answers = []
        for number in range(10, 100):
            tens, ones = divmod(number, 10)
            reverse = 10 * ones + tens
            if tens + ones == digit_sum and number - reverse == difference:
                answers.append((number, reverse))
        (number, reverse), = answers
        model = (f"a + b = {digit_sum}; (10a+b) - (10b+a) = {difference}")
        return "digit_reversal", f"number {number}; reversed {reverse}", model
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; x = {answer}"
    return variant, answer


class TestIntegerPuzzleWordGenerator(unittest.TestCase):
    def test_applied_marker_and_contract(self):
        self.assertIs(APPLIED, True)
        result = IntegerPuzzleWordGenerator().generate()
        self.assertEqual(result["steps"][-1],
                         f"Z{DELIM}{result['final_answer']}")

    def test_brute_force_oracle_from_problem_only(self):
        random.seed(381)
        seen = set()
        for _ in range(1400):
            result = IntegerPuzzleWordGenerator().generate()
            modifier = next(m for m in MODIFIERS
                            if result["operation"].endswith("_" + m))
            variant = result["operation"][:-len(modifier)-1].removeprefix(
                "applied_integer_puzzle_")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_five_rendering_orders_are_parseable(self):
        cases = {
            "age_now": ("Ann is 3 years older than twice Ben's age. Together their ages total 27 years.",
                        "How old are Ann and Ben?"),
            "age_future": ("Mia is 4 years older than Leo. In 5 years their ages will total 30 years.",
                           "What are Mia's and Leo's ages now?"),
            "consecutive_integers": ("Three consecutive integers have sum 18.",
                                     "What are the three integers?"),
            "consecutive_even_odd": ("Three consecutive even integers have sum 24.",
                                     "What are the three even integers?"),
            "coins_count_value": ("A jar contains 24 nickels and dimes worth 190 cents altogether.",
                                  "How many nickels and how many dimes are in the jar?"),
            "number_relationship": ("The larger of two integers is 3 more than 2 times the smaller. Their sum is 27.",
                                    "What are the two integers?"),
            "digit_reversal": ("A two-digit number has digit sum 10. It is 36 greater than the number made by reversing its digits.",
                               "What is the number and its reversal?"),
        }
        self.assertEqual(len(FRAMES), 5)
        for variant, (facts, question) in cases.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       setting="library club",
                                       facts_lc=facts[:1].lower() + facts[1:],
                                       record="A17")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        for _ in range(700):
            result = IntegerPuzzleWordGenerator().generate()
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
                result = IntegerPuzzleWordGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                    self.assertEqual(codes.count("SELECT_RELEVANT"), 1)
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            IntegerPuzzleWordGenerator("bogus")
        with self.assertRaises(ValueError):
            IntegerPuzzleWordGenerator(modifier="bogus")

    def test_pipe_and_render_safety(self):
        for _ in range(500):
            result = IntegerPuzzleWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
