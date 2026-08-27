"""Independent evaluators for RecursiveDefinitionUnfoldGenerator."""
import math
import random
import re
import unittest
from unittest.mock import patch

from generators.recursive_definition_unfold_generator import (
    QUERIES, RecursiveDefinitionUnfoldGenerator,
)
from helpers import DELIM


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def ackermann(first, second):
    if first == 0:
        return second + 1
    if second == 0:
        return ackermann(first - 1, 1)
    return ackermann(first - 1, ackermann(first, second - 1))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    factorial_match = re.fullmatch(
        r"Definition: F\(0\) = 1; F\(n\) = n·F\(n−1\) for n ≥ 1\. "
        r"Target: F\((\d+)\)\.", body)
    if factorial_match:
        number = int(factorial_match.group(1))
        return {"variant": variant, "query": query, "target": f"F({number})",
                "answer": str(math.factorial(number))}
    additive_match = re.fullmatch(
        r"Definition: (\w)\(0\) = (-?\d+); \1\(n\) = \1\(n−1\) \+ "
        r"(\d+)·n for n ≥ 1\. Target: \1\((\d+)\)\.", body)
    if additive_match:
        symbol, base, coefficient, number = additive_match.groups()
        base, coefficient, number = int(base), int(coefficient), int(number)
        result = base + coefficient * sum(range(1, number + 1))
        return {"variant": variant, "query": query,
                "target": f"{symbol}({number})", "answer": str(result)}
    ack_match = re.fullmatch(
        r"Definition: Ack\(0, n\) = n \+ 1; Ack\(m, 0\) = Ack\(m−1, 1\); "
        r"Ack\(m, n\) = Ack\(m−1, Ack\(m, n−1\)\) for m,n ≥ 1\. "
        r"Target: Ack\((\d+), (\d+)\)\.", body)
    if ack_match:
        first, second = map(int, ack_match.groups())
        return {"variant": variant, "query": query,
                "target": f"Ack({first}, {second})",
                "answer": str(ackermann(first, second))}
    gcd_match = re.fullmatch(
        r"Definition: gcd\(a, 0\) = a; gcd\(a, b\) = gcd\(b, a mod b\) "
        r"for b > 0\. Target: gcd\((\d+), (\d+)\)\.", body)
    if gcd_match:
        first, second = map(int, gcd_match.groups())
        return {"variant": variant, "query": query,
                "target": f"gcd({first}, {second})",
                "answer": str(math.gcd(first, second))}
    length_match = re.fullmatch(
        r"Definition: len\(ε\) = 0; len\(cw\) = 1 \+ len\(w\)\. "
        r'Target: len\("([a-z]+)"\)\.', body)
    if length_match:
        text = length_match.group(1)
        return {"variant": variant, "query": query,
                "target": f'len("{text}")', "answer": str(len(text))}
    reverse_match = re.fullmatch(
        r"Definition: rev\(ε\) = ε; rev\(cw\) = rev\(w\)c\. "
        r'Target: rev\("([a-z]+)"\)\.', body)
    if reverse_match:
        text = reverse_match.group(1)
        return {"variant": variant, "query": query,
                "target": f'rev("{text}")', "answer": text[::-1]}
    count_match = re.fullmatch(
        r"Definition: count_([a-z])\(ε\) = 0; count_\1\(cw\) = "
        r"\[c=\1\] \+ count_\1\(w\)\. "
        r'Target: count_\1\("([a-z]+)"\)\.', body)
    if count_match:
        target, text = count_match.groups()
        return {"variant": variant, "query": query,
                "target": f'count_{target}("{text}")',
                "answer": str(text.count(target))}
    mutual_match = re.fullmatch(
        r"Definition: Even\(0\) = true; Odd\(0\) = false; "
        r"Even\(n\+1\) = Odd\(n\); Odd\(n\+1\) = Even\(n\)\. "
        r"Target: (Even|Odd)\((\d+)\)\.", body)
    assert mutual_match is not None, body
    predicate, number = mutual_match.group(1), int(mutual_match.group(2))
    result = (number % 2 == 0) if predicate == "Even" else (number % 2 == 1)
    return {"variant": variant, "query": query,
            "target": f"{predicate}({number})",
            "answer": "true" if result else "false"}


class RecursiveDefinitionUnfoldGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(617083)

    def test_output_contract(self):
        example = RecursiveDefinitionUnfoldGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RecursiveDefinitionUnfoldGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_arithmetic_division_and_fold_target_are_exact(self):
        generator = RecursiveDefinitionUnfoldGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            bases = []
            folds = []
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "DIVMOD":
                    match = re.fullmatch(r"(\d+) R (\d+)", fields[3])
                    self.assertIsNotNone(match)
                    quotient, remainder = map(int, match.groups())
                    self.assertEqual(int(fields[1]),
                                     quotient * int(fields[2]) + remainder)
                    self.assertLess(remainder, int(fields[2]))
                elif fields[0] == "BASE":
                    bases.append(fields)
                elif fields[0] == "FOLD":
                    folds.append(fields)
            self.assertTrue(bases)
            if folds:
                target_folds = [item for item in folds if item[1] == parts["target"]]
                self.assertTrue(target_folds)
                self.assertEqual(target_folds[-1][2], example["final_answer"])

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RecursiveDefinitionUnfoldGenerator.VARIANTS:
            generator = RecursiveDefinitionUnfoldGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"recursive_definition_unfold_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_factorial_and_ackermann_subcases_are_reachable(self):
        with patch(
                "generators.recursive_definition_unfold_generator.random.random",
                return_value=0.0):
            factorial = RecursiveDefinitionUnfoldGenerator("one_arg").generate()
            ackermann_example = RecursiveDefinitionUnfoldGenerator("two_arg").generate()
        self.assertIn("Definition: F(0) = 1", factorial["problem"])
        self.assertIn("Definition: Ack(0, n) = n + 1", ackermann_example["problem"])
        self.assertEqual(factorial["final_answer"], oracle_parts(factorial)["answer"])
        self.assertEqual(ackermann_example["final_answer"],
                         oracle_parts(ackermann_example)["answer"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RecursiveDefinitionUnfoldGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RecursiveDefinitionUnfoldGenerator()
        for _ in range(200):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
