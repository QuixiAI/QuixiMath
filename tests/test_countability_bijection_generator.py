"""Problem-text oracles for CountabilityBijectionGenerator."""
from fractions import Fraction
import math
import random
import re
import unittest

from generators.countability_bijection_generator import (
    CountabilityBijectionGenerator, QUERIES,
)
from helpers import DELIM


def int_text(value):
    return str(value).replace("-", "−")


def parse_int(text):
    return int(text.replace("−", "-"))


def fraction_text(value):
    value = Fraction(value)
    return (int_text(value.numerator) if value.denominator == 1
            else f"{int_text(value.numerator)}/{value.denominator}")


def independent_calkin_wilf(index):
    left, right = 1, 1
    mask = 1 << (index.bit_length() - 2) if index > 1 else 0
    while mask:
        if index & mask:
            left += right
        else:
            right += left
        mask >>= 1
    return Fraction(left, right)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "nat_to_int":
        prefix = ("Define f: ℕ → ℤ by f(n) = n/2 when n is even and "
                  "f(n) = −(n + 1)/2 when n is odd. ")
        assert body.startswith(prefix), body
        request = body[len(prefix):]
        evaluation = re.fullmatch(r"Evaluation request: n = (\d+)\.", request)
        inverse = re.fullmatch(r"Inverse request: z = ([−-]?\d+)\.", request)
        assert evaluation or inverse, request
        if evaluation:
            natural = int(evaluation.group(1))
            integer = natural // 2 if natural % 2 == 0 else -(natural + 1) // 2
            answer = f"f({natural}) = {int_text(integer)}"
            mode = "evaluation"
        else:
            integer = parse_int(inverse.group(1))
            natural = 2 * integer if integer >= 0 else -2 * integer - 1
            answer = f"f⁻¹({int_text(integer)}) = {natural}"
            mode = "inverse"
    elif variant == "nat_to_evens":
        prefix = "Define e from ℕ to the nonnegative even integers by e(n) = 2n. "
        assert body.startswith(prefix), body
        request = body[len(prefix):]
        evaluation = re.fullmatch(r"Evaluation request: n = (\d+)\.", request)
        inverse = re.fullmatch(r"Inverse request: even value = (\d+)\.", request)
        assert evaluation or inverse, request
        if evaluation:
            natural = int(evaluation.group(1))
            even = 2 * natural
            answer, mode = f"e({natural}) = {even}", "evaluation"
        else:
            even = int(inverse.group(1))
            assert even % 2 == 0
            natural = even // 2
            answer, mode = f"e⁻¹({even}) = {natural}", "inverse"
    elif variant == "nat_to_squares":
        prefix = "Define s from ℕ to the perfect squares by s(n) = n². "
        assert body.startswith(prefix), body
        request = body[len(prefix):]
        match = re.fullmatch(
            r"Evaluation request: n = (\d+); inverse request: square value = "
            r"(\d+)\.", request)
        assert match is not None, request
        natural, inverse_square = map(int, match.groups())
        square = natural * natural
        inverse_natural = math.isqrt(inverse_square)
        assert inverse_natural * inverse_natural == inverse_square
        answer = (f"s({natural}) = {square}; "
                  f"s⁻¹({inverse_square}) = {inverse_natural}")
        mode = "both"
    elif variant == "calkin_wilf":
        match = re.fullmatch(
            r"For n ≥ 1, the Calkin–Wilf binary walk starts at 1/1, "
            r"skips the leading 1 of n in binary, then sends bit 0: "
            r"a/b → a/\(a \+ b\) and bit 1: a/b → \(a \+ b\)/b\. "
            r"Index: n = (\d+)\.", body)
        assert match is not None, body
        index = int(match.group(1))
        value = independent_calkin_wilf(index)
        answer = f"term {index} = {fraction_text(value)}"
        mode = "index"
        natural, square, even, integer = index, 0, 0, 0
    else:
        match = re.fullmatch(
            r"A hotel has rooms and guest labels in ℕ\. To admit countably "
            r"many new guests, move the existing guest from room n to room "
            r"2n and place new guest n in room 2n \+ 1\. Existing room "
            r"request: (\d+); new guest request: (\d+)\.", body)
        assert match is not None, body
        existing, newcomer = map(int, match.groups())
        answer = (f"existing room {existing} → {2 * existing}; "
                  f"new guest {newcomer} → {2 * newcomer + 1}")
        mode = "reassign"
        natural, square, even, integer = existing, 0, 0, 0
    return {"variant": variant, "query": query, "answer": answer,
            "mode": mode, "natural": natural,
            "integer": integer if variant == "nat_to_int" else None,
            "even": even if variant == "nat_to_evens" else None,
            "square": square if variant == "nat_to_squares" else None}


class CountabilityBijectionGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(271828)

    def test_output_contract(self):
        example = CountabilityBijectionGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CountabilityBijectionGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_arithmetic_inside_steps(self):
        generator = CountabilityBijectionGenerator()
        for _ in range(350):
            example = generator.generate()
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(parse_int(fields[1]) + parse_int(fields[2]),
                                     parse_int(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(parse_int(fields[1]) - parse_int(fields[2]),
                                     parse_int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(parse_int(fields[1]) * parse_int(fields[2]),
                                     parse_int(fields[3]))
                elif fields[0] == "D":
                    dividend, divisor, quotient = map(parse_int, fields[1:])
                    self.assertEqual(dividend, divisor * quotient)
                elif fields[0] == "NEGATE":
                    self.assertEqual(-parse_int(fields[1]), parse_int(fields[2]))
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]))
                elif fields[0] == "BINARY":
                    self.assertEqual(bin(int(fields[1]))[2:], fields[2])

    def test_forward_and_inverse_modes_are_reachable(self):
        for variant in ("nat_to_int", "nat_to_evens"):
            generator = CountabilityBijectionGenerator(variant)
            modes = {oracle_parts(generator.generate())["mode"]
                     for _ in range(100)}
            self.assertEqual(modes, {"evaluation", "inverse"})
        square = CountabilityBijectionGenerator("nat_to_squares").generate()
        self.assertEqual(oracle_parts(square)["mode"], "both")

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CountabilityBijectionGenerator.VARIANTS:
            generator = CountabilityBijectionGenerator(variant)
            seen_queries = set()
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"countability_bijection_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CountabilityBijectionGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CountabilityBijectionGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
