"""Independent A9 checks for CounterexampleSearchGenerator."""
import itertools
import math
import random
import re
import unittest

from generators.counterexample_search_generator import (
    CounterexampleSearchGenerator,
    QUERIES,
)
from helpers import DELIM
from tests import foundations_oracle as set_oracle


def first_factor(value):
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return divisor
    return None


def subsets(values):
    output = []
    for size in range(len(values) + 1):
        output.extend(frozenset(combo) for combo in itertools.combinations(values, size))
    return output


def split_query(problem, variant):
    for query in QUERIES[variant]:
        if problem.endswith(f" {query}"):
            return problem[:-(len(query) + 1)], query
    raise AssertionError(problem)


def oracle_parts(example):
    problem = example["problem"]
    if problem.startswith("Claim: every multiple"):
        body, query = split_query(problem, "arithmetic_claim")
        match = re.fullmatch(
            r"Claim: every multiple n of (\d+) with n ≥ (\d+) is also divisible "
            r"by (\d+)\. Scan eligible multiples in increasing order\.", body
        )
        assert match is not None, body
        divisor_a, lower, divisor_b = map(int, match.groups())
        value = ((lower + divisor_a - 1) // divisor_a) * divisor_a
        trials = []
        while value % divisor_b == 0:
            trials.append(value)
            value += divisor_a
        trials.append(value)
        witness = (f"{value} is divisible by {divisor_a} but not by "
                   f"{divisor_b}")
        return {"variant": "arithmetic_claim", "trials": trials,
                "answer": f"n = {value} ({witness})", "query": query}
    if problem.startswith("Claim: for every integer"):
        body, query = split_query(problem, "algebraic_claim")
        match = re.fullmatch(
            r"Claim: for every integer n ≥ (\d+), n\^2 \+ (\d+)n \+ (\d+) "
            r"is prime\. Scan consecutive integers in increasing order\.", body
        )
        assert match is not None, body
        lower, coefficient, constant = map(int, match.groups())
        trials = []
        for value in range(lower, lower + 12):
            output = value * value + coefficient * value + constant
            factor = first_factor(output)
            trials.append(value)
            if factor is not None:
                witness = f"{output} = {factor} × {output // factor}"
                return {"variant": "algebraic_claim", "trials": trials,
                        "answer": f"n = {value} ({witness})", "query": query}
        raise AssertionError("no counterexample in stated scan")

    body, query = split_query(problem, "set_claim")
    match = re.fullmatch(
        r"Universe U = (.+)\. Claim: for all subsets A and B of U, (.+)\. "
        r"Enumerate subsets by size then lexicographically; enumerate A first, "
        r"then B\.", body
    )
    assert match is not None, body
    universe = tuple(set_oracle.parse_roster(match.group(1)))
    claim = match.group(2)

    def sides(values_a, values_b):
        if claim == "A − B = B − A":
            return values_a - values_b, values_b - values_a
        if claim == "A ∪ B = A ∩ B":
            return values_a | values_b, values_a & values_b
        assert claim == "A Δ B = A ∪ B"
        return values_a ^ values_b, values_a | values_b

    trials = []
    for values_a in subsets(universe):
        for values_b in subsets(universe):
            left, right = sides(values_a, values_b)
            trials.append((values_a, values_b))
            if left != right:
                answer = (f"A = {set_oracle.roster_text(values_a)}; "
                          f"B = {set_oracle.roster_text(values_b)}; "
                          f"left = {set_oracle.roster_text(left)}; "
                          f"right = {set_oracle.roster_text(right)}")
                return {"variant": "set_claim", "trials": trials,
                        "answer": answer, "query": query}
    raise AssertionError("false identity had no counterexample")


class CounterexampleSearchGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(294001)

    def test_output_contract(self):
        example = CounterexampleSearchGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1], f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = CounterexampleSearchGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"], oracle_parts(example)["answer"],
                             example["problem"])

    def test_scan_order_bound_and_arithmetic_steps(self):
        generator = CounterexampleSearchGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            try_steps = []
            accepted = 0
            counterexamples = 0
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]), int(fields[3]))
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]), int(fields[3]))
                elif fields[0] == "DIV_CHECK":
                    value, divisor = int(fields[1]), int(fields[2])
                    self.assertIn(f"remainder {value % divisor}", fields[3])
                elif fields[0] == "TRY":
                    try_steps.append(fields)
                elif fields[0] == "ACCEPT":
                    accepted += 1
                elif fields[0] == "COUNTEREXAMPLE":
                    counterexamples += 1
            self.assertLessEqual(len(try_steps), 12)
            self.assertEqual(len(try_steps), len(parts["trials"]))
            self.assertEqual(accepted, 1)
            self.assertEqual(counterexamples, 1)

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in CounterexampleSearchGenerator.VARIANTS:
            generator = CounterexampleSearchGenerator(variant)
            seen = set()
            for _ in range(400):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"counterexample_search_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            CounterexampleSearchGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = CounterexampleSearchGenerator()
        for _ in range(300):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
