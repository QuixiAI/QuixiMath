"""Independent exact counting oracle for SetCountingGenerator."""
import itertools
import math
import random
import re
import unittest

from generators.set_counting_generator import QUERIES, SetCountingGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def partition_count(size):
    """Brute-force restricted-growth strings, independent of Bell formulas."""
    if size == 0:
        return 1
    count = 0

    def extend(labels):
        nonlocal count
        if len(labels) == size:
            count += 1
            return
        for label in range(max(labels) + 2):
            extend(labels + [label])

    extend([0])
    return count


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant in ("functions", "injections", "bijections", "relations"):
        match = re.fullmatch(r"A = (.+)\. B = (.+)\.", body)
        assert match is not None, body
        set_a, set_b = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
        m, n = len(set_a), len(set_b)
        if variant == "functions":
            answer = n ** m
        elif variant == "injections":
            answer = math.factorial(n) // math.factorial(n - m)
        elif variant == "bijections":
            answer = math.factorial(m)
        else:
            answer = 2 ** (m * n)
        return {"variant": variant, "query": query, "A": set_a, "B": set_b,
                "answer": str(answer)}
    if variant == "k_subsets":
        match = re.fullmatch(r"A = (.+)\. k = (\d+)\.", body)
        assert match is not None, body
        set_a, chosen = oracle.parse_set(match.group(1)), int(match.group(2))
        answer = math.comb(len(set_a), chosen)
        return {"variant": variant, "query": query, "A": set_a, "k": chosen,
                "answer": str(answer)}
    if variant == "subsets_containing":
        match = re.fullmatch(r"A = (.+)\. R = (.+)\.", body)
        assert match is not None, body
        set_a, required = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
        answer = 2 ** (len(set_a) - len(required))
        return {"variant": variant, "query": query, "A": set_a,
                "R": required, "answer": str(answer)}
    match = re.fullmatch(r"A = (.+)\.", body)
    assert match is not None, body
    set_a = oracle.parse_set(match.group(1))
    size = len(set_a)
    if variant == "subsets":
        answer = 2 ** size
    elif variant == "reflexive_relations":
        answer = 2 ** (size * size - size)
    elif variant == "symmetric_relations":
        answer = 2 ** (size * (size + 1) // 2)
    else:
        assert variant == "partitions"
        answer = partition_count(size)
    return {"variant": variant, "query": query, "A": set_a,
            "answer": str(answer)}


class SetCountingGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(493771)

    def test_output_contract(self):
        example = SetCountingGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = SetCountingGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_emitted_integer_arithmetic_and_stirling_cells(self):
        generator = SetCountingGenerator()
        for _ in range(300):
            example = generator.generate()
            bell_rows = {}
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
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
                    self.assertEqual(int(fields[1]),
                                     int(fields[2]) * int(fields[3]))
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "STIRLING_CELL":
                    match = re.fullmatch(r"(\d+)×(\d+)\+(\d+)", fields[2])
                    self.assertIsNotNone(match)
                    multiplier, same, new = map(int, match.groups())
                    self.assertEqual(multiplier * same + new, int(fields[3]))
                elif fields[0] == "BELL_ROW":
                    values = [int(item) for item in fields[2].split()]
                    self.assertEqual(sum(values), int(fields[3]))
                    bell_rows[int(fields[1].split("=")[1])] = int(fields[3])
            if oracle_parts(example)["variant"] == "partitions":
                size = len(oracle_parts(example)["A"])
                self.assertEqual(bell_rows[size], int(example["final_answer"]))

    def test_small_cases_match_brute_force_enumeration(self):
        for size in range(1, 5):
            subsets = list(itertools.product((False, True), repeat=size))
            self.assertEqual(len(subsets), 2 ** size)
            functions = list(itertools.product(range(3), repeat=size))
            self.assertEqual(len(functions), 3 ** size)
            self.assertEqual(partition_count(size), (1, 2, 5, 15)[size - 1])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in SetCountingGenerator.VARIANTS:
            generator = SetCountingGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"set_counting_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SetCountingGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = SetCountingGenerator()
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
