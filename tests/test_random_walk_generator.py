"""Path-enumeration and first-step-system oracle for RandomWalkGenerator."""
import itertools
import math
import random
import re
import unittest
from fractions import Fraction

from generators.random_walk_generator import QUERIES, RandomWalkGenerator
from helpers import DELIM


def ptext(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def walk_rows(n, p):
    q = 1 - p
    for increments in itertools.product((-1, 1), repeat=n):
        weight = Fraction(1)
        for increment in increments:
            weight *= p if increment == 1 else q
        yield sum(increments), weight


def solve_system(matrix, rhs):
    size = len(rhs)
    rows = [list(map(Fraction, matrix[row])) + [Fraction(rhs[row])]
            for row in range(size)]
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if rows[row][column] != 0)
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right
                         for left, right in zip(rows[row], rows[column])]
    return [rows[row][-1] for row in range(size)]


def first_step_values(boundary, p, duration=False):
    q = 1 - p
    size = boundary - 1
    matrix = [[Fraction(int(row == column)) for column in range(size)]
              for row in range(size)]
    rhs = [Fraction(1 if duration else 0) for _ in range(size)]
    for state in range(1, boundary):
        row = state - 1
        if state - 1 >= 1:
            matrix[row][state - 2] -= q
        if state + 1 <= boundary - 1:
            matrix[row][state] -= p
        elif not duration:
            rhs[row] += p
    return solve_system(matrix, rhs)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("position_prob", "biased_position", "return_to_origin",
                   "mean_var"):
        n = int(re.search(r"takes n=(\d+) independent steps", body).group(1))
        p = Fraction(re.search(r"probability p=(\d+(?:/\d+)?)", body).group(1))
        rows = list(walk_rows(n, p))
        if variant == "mean_var":
            mean = sum((position * weight for position, weight in rows), Fraction())
            second = sum((position ** 2 * weight for position, weight in rows),
                         Fraction())
            variance = second - mean ** 2
            answer = f"E[S_{n}] = {ptext(mean)}; Var(S_{n}) = {ptext(variance)}"
        else:
            position = int(re.search(r"Target: P\(S_\d+=(-?\d+)\)", body).group(1))
            probability = sum((weight for endpoint, weight in rows
                               if endpoint == position), Fraction())
            answer = ptext(probability)
    else:
        match = re.search(r"starts with i=(\d+) units.*0 or N=(\d+)", body)
        initial, boundary = map(int, match.groups())
        p = Fraction(re.search(r"probability p=(\d+(?:/\d+)?)", body).group(1))
        duration = variant == "duration_fair"
        values = first_step_values(boundary, p, duration)
        answer = ptext(values[initial - 1])
    return {"variant": variant, "query": query, "answer": answer}


class RandomWalkGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(240766)

    def test_output_contract(self):
        example = RandomWalkGenerator().generate()
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RandomWalkGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"], example["problem"])

    def test_arithmetic_combination_and_power_steps_are_exact(self):
        generator = RandomWalkGenerator()
        for _ in range(300):
            example = generator.generate()
            oracle_parts(example)
            for raw in example["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]))
                elif fields[0] == "NCR":
                    match = re.fullmatch(r"C\((\d+), (\d+)\)", fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(math.comb(int(match.group(1)),
                                               int(match.group(2))), int(fields[2]))
                elif fields[0] == "POW":
                    match = re.fullmatch(r"base (\d+(?:/\d+)?), exponent (\d+)",
                                         fields[1])
                    self.assertIsNotNone(match, raw)
                    self.assertEqual(Fraction(match.group(1)) ** int(match.group(2)),
                                     Fraction(fields[2]))

    def test_plan_examples(self):
        self.assertEqual(ptext(sum((weight for endpoint, weight in
                                   walk_rows(6, Fraction(1, 2)) if endpoint == 2),
                                  Fraction())), "15/64")
        self.assertEqual(ptext(sum((weight for endpoint, weight in
                                   walk_rows(6, Fraction(1, 2)) if endpoint == 0),
                                  Fraction())), "5/16")
        self.assertEqual(ptext(first_step_values(4, Fraction(2, 3))[1]), "4/5")

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RandomWalkGenerator.VARIANTS:
            generator = RandomWalkGenerator(variant)
            seen = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"probability_random_walk_{variant}")
                seen.add(parts["query"])
            self.assertEqual(seen, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RandomWalkGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RandomWalkGenerator()
        for _ in range(250):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            rendered = "\n".join([example["problem"], *example["steps"],
                                   example["final_answer"]])
            self.assertNotRegex(rendered, r"1x|\^1\b|\+ 0|--|− -")
            for raw in example["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
