"""Brute-force prompt-text oracle for IndependenceCheckGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.independence_check_generator import QUERIES, IndependenceCheckGenerator
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_roster(text):
    body = text[1:-1]
    return tuple() if not body else tuple(body.split(", "))


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def predicate(description, outcome):
    if description == "the roll is even":
        return outcome % 2 == 0
    if description == "the roll is odd":
        return outcome % 2 == 1
    if description == "the roll is prime":
        return outcome >= 2 and all(outcome % d for d in range(2, math.isqrt(outcome) + 1))
    match = re.fullmatch(r"the roll is at most (\d+)", description)
    if match:
        return outcome <= int(match.group(1))
    match = re.fullmatch(r"the roll is at least (\d+)", description)
    if match:
        return outcome >= int(match.group(1))
    match = re.fullmatch(r"the roll is a multiple of (\d+)", description)
    assert match is not None, description
    return outcome % int(match.group(1)) == 0


def pair_predicate(description, outcome):
    match = re.fullmatch(r"the sum equals (\d+)", description)
    if match:
        return sum(outcome) == int(match.group(1))
    match = re.fullmatch(r"the sum is at least (\d+)", description)
    if match:
        return sum(outcome) >= int(match.group(1))
    if description == "the dice show doubles":
        return outcome[0] == outcome[1]
    if description == "the first die exceeds the second":
        return outcome[0] > outcome[1]
    if description == "the product is even":
        return outcome[0] * outcome[1] % 2 == 0
    match = re.fullmatch(r"the maximum is at most (\d+)", description)
    assert match is not None, description
    return max(outcome) <= int(match.group(1))


def verdict(p_a, p_b, p_inter):
    product = p_a * p_b
    if p_inter == product:
        return f"independent; P(A ∩ B) = {ptext(p_inter)} = P(A)·P(B)"
    return (f"dependent; P(A ∩ B) = {ptext(p_inter)} ≠ "
            f"P(A)·P(B) = {ptext(product)}")


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "die_events":
        match = re.fullmatch(
            r"A fair ([a-z]+) (\d+)-sided die with faces 1 through \2 is rolled\. A: "
            r"(.+)\. B: (.+)\.", body)
        assert match is not None, body
        outcomes = tuple(range(1, int(match.group(2)) + 1))
        event_a = {o for o in outcomes if predicate(match.group(3), o)}
        event_b = {o for o in outcomes if predicate(match.group(4), o)}
    elif variant == "two_dice_events":
        match = re.fullmatch(
            r"A fair ([a-z]+) (\d+)-sided die and a fair ([a-z]+) (\d+)-sided "
            r"die are rolled in that order\. A: (.+)\. B: (.+)\.", body)
        assert match is not None, body
        outcomes = tuple(itertools.product(range(1, int(match.group(2)) + 1),
                                           range(1, int(match.group(4)) + 1)))
        event_a = {o for o in outcomes if pair_predicate(match.group(5), o)}
        event_b = {o for o in outcomes if pair_predicate(match.group(6), o)}
    elif variant == "small_deck":
        match = re.fullmatch(
            r"A mini-deck has cards (\{[^{}]+\})\. Cards marked for A: "
            r"(\{[^{}]*\}|∅)\. Cards marked for B: (\{[^{}]*\}|∅)\. One card "
            r"is drawn uniformly\.", body)
        assert match is not None, body
        outcomes = parse_roster(match.group(1))
        event_a, event_b = set(parse_roster(match.group(2))), set(parse_roster(match.group(3)))
    elif variant == "table_events":
        match = re.fullmatch(
            r"A 2 by 2 table has counts R1C1=(\d+); R1C2=(\d+); R2C1=(\d+); "
            r"R2C2=(\d+); total=(\d+)\. Event A is row R1 and event B is column C1\.", body)
        assert match is not None, body
        counts = list(map(int, match.groups()))
        assert sum(counts[:4]) == counts[4]
        outcomes = tuple((r, c, i) for r in (1, 2) for c in (1, 2)
                         for i in range(counts[(r - 1) * 2 + c - 1]))
        event_a = {o for o in outcomes if o[0] == 1}
        event_b = {o for o in outcomes if o[1] == 1}
    elif variant == "given_probabilities":
        match = re.fullmatch(
            r"Events A and B have P\(A\) = (\d+(?:/\d+)?), P\(B\) = "
            r"(\d+(?:/\d+)?), and P\(A ∩ B\) = (\d+(?:/\d+)?)\.", body)
        assert match is not None, body
        p_a, p_b, p_inter = map(Fraction, match.groups())
        return {"variant": variant, "query": query,
                "answer": verdict(p_a, p_b, p_inter), "case": p_inter == p_a * p_b}
    else:
        match = re.fullmatch(
            r"Independent fair devices ([a-z]+) and ([a-z]+) each output one of "
            r"(\{[^{}]+\})\. A: \1 outputs ([a-z]+)\. B: \2 outputs \4\. C: "
            r"the two outputs match\.", body)
        assert match is not None, body
        outputs = parse_roster(match.group(3))
        assert match.group(4) in outputs and len(outputs) == 2
        answer = ("pairwise independent; not mutually independent; "
                  "P(A ∩ B ∩ C) = 1/4 ≠ 1/8")
        return {"variant": variant, "query": query, "answer": answer, "case": "pairwise"}
    p_a = Fraction(len(event_a), len(outcomes))
    p_b = Fraction(len(event_b), len(outcomes))
    p_inter = Fraction(len(event_a & event_b), len(outcomes))
    return {"variant": variant, "query": query,
            "answer": verdict(p_a, p_b, p_inter), "case": p_inter == p_a * p_b}


class IndependenceCheckGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(316228)

    def test_output_contract(self):
        example = IndependenceCheckGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = IndependenceCheckGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_steps_are_exact(self):
        generator = IndependenceCheckGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]), Fraction(fields[2]))
                    self.assertEqual(fields[2], ptext(Fraction(fields[2])))
                elif fields[0] == "EVENT":
                    if fields[2] == "∅":
                        count = 0
                    elif fields[2].startswith("{("):
                        count = len(re.findall(r"\(\d+, \d+\)", fields[2]))
                    else:
                        count = len(parse_roster(fields[2]))
                    self.assertEqual(count, int(fields[3]))

    def test_both_binary_verdicts_are_reachable(self):
        for variant in ("die_events", "two_dice_events", "small_deck",
                        "table_events", "given_probabilities"):
            generator = IndependenceCheckGenerator(variant)
            self.assertEqual({oracle_parts(generator.generate())["case"]
                              for _ in range(600)}, {False, True})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in IndependenceCheckGenerator.VARIANTS:
            generator = IndependenceCheckGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_independence_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            IndependenceCheckGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = IndependenceCheckGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4, raw_step)


if __name__ == "__main__":
    unittest.main()
