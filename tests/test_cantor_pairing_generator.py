"""Independent integer oracle for CantorPairingGenerator."""
import math
import random
import re
import unittest

from generators.cantor_pairing_generator import CantorPairingGenerator, QUERIES
from helpers import DELIM


def oracle_pair(first, second):
    diagonal = first + second
    return diagonal * (diagonal + 1) // 2 + second


def oracle_unpair(value):
    diagonal = (math.isqrt(8 * value + 1) - 1) // 2
    while (diagonal + 1) * (diagonal + 2) // 2 <= value:
        diagonal += 1
    while diagonal * (diagonal + 1) // 2 > value:
        diagonal -= 1
    second = value - diagonal * (diagonal + 1) // 2
    return diagonal - second, second


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    formula = (r"Cantor pairing uses π\(m, n\) = "
               r"\(m \+ n\)\(m \+ n \+ 1\)/2 \+ n\. ")
    if variant == "pair":
        match = re.fullmatch(formula + r"Input pair: \((\d+), (\d+)\)\.", body)
        assert match is not None, body
        first, second = map(int, match.groups())
        paired = oracle_pair(first, second)
        answer = f"π({first}, {second}) = {paired}"
        mode = "pair"
    elif variant == "unpair":
        match = re.fullmatch(formula + r"Encoded value: z = (\d+)\.", body)
        assert match is not None, body
        paired = int(match.group(1))
        first, second = oracle_unpair(paired)
        answer = f"z = {paired} ↔ ({first}, {second})"
        mode = "unpair"
    else:
        prefix = (r"The zero-indexed diagonal walk of ℕ × ℕ starts "
                  r"\(0, 0\), \(1, 0\), \(0, 1\), \(2, 0\), \(1, 1\), "
                  r"\(0, 2\), \.\.\. \. ")
        pair_match = re.fullmatch(
            prefix + r"Requested pair: \((\d+), (\d+)\)\. Find its position\.",
            body)
        position_match = re.fullmatch(
            prefix + r"Requested position: (\d+)\. Find the pair at that position\.",
            body)
        assert pair_match is not None or position_match is not None, body
        if pair_match:
            first, second = map(int, pair_match.groups())
            paired = oracle_pair(first, second)
            mode = "pair_at_position"
        else:
            paired = int(position_match.group(1))
            first, second = oracle_unpair(paired)
            mode = "position_to_pair"
        answer = f"position {paired}: ({first}, {second})"
    return {"variant": variant, "query": query, "first": first,
            "second": second, "paired": paired, "mode": mode,
            "answer": answer}


class CantorPairingGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(618033)

    def test_output_contract(self):
        example = CantorPairingGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CantorPairingGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_arithmetic_and_triangular_bounds_inside_steps(self):
        generator = CantorPairingGenerator()
        for _ in range(350):
            example = generator.generate()
            parts = oracle_parts(example)
            for fields in (raw.split(DELIM) for raw in example["steps"]):
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]))
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "TRY":
                    candidate = int(fields[1].split("=")[1])
                    self.assertLessEqual(candidate * (candidate + 1) // 2,
                                         parts["paired"])
                elif fields[0] == "REJECT":
                    candidate = int(fields[1].split("=")[1])
                    self.assertGreater(candidate * (candidate + 1) // 2,
                                       parts["paired"])

    def test_pairing_is_inverted_exactly(self):
        for first in range(35):
            for second in range(35):
                paired = oracle_pair(first, second)
                self.assertEqual(oracle_unpair(paired), (first, second))

    def test_diagonal_variant_exercises_both_lookup_directions(self):
        generator = CantorPairingGenerator("diagonal_enumeration")
        modes = {oracle_parts(generator.generate())["mode"]
                 for _ in range(120)}
        self.assertEqual(modes, {"pair_at_position", "position_to_pair"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CantorPairingGenerator.VARIANTS:
            generator = CantorPairingGenerator(variant)
            seen_queries = set()
            for _ in range(250):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"cantor_pairing_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CantorPairingGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CantorPairingGenerator()
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
