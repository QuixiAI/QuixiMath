"""Independent nested-set oracle for HereditarilyFiniteSetGenerator."""
import random
import re
import unittest

from generators.hereditarily_finite_set_generator import (
    QUERIES, HereditarilyFiniteSetGenerator,
)
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def set_text(value):
    return oracle.element_text(value)


def successor(value):
    return frozenset(value) | {frozenset(value)}


def numeral(number):
    value = frozenset()
    for _ in range(number):
        value = successor(value)
    return value


def rank(value):
    if not value:
        return 0
    return max(rank(element) + 1 for element in value)


def kuratowski(first, second):
    return frozenset({frozenset({first}), frozenset({first, second})})


def decode_kuratowski(value):
    blocks = list(value)
    if len(blocks) == 1:
        assert len(blocks[0]) == 1
        element = next(iter(blocks[0]))
        return element, element
    assert len(blocks) == 2
    singleton = next(block for block in blocks if len(block) == 1)
    doubleton = next(block for block in blocks if len(block) == 2)
    first = next(iter(singleton))
    second = next(iter(doubleton - singleton))
    return first, second


def transitivity_witness(value):
    for element in sorted(value, key=oracle.element_key):
        for member in sorted(element, key=oracle.element_key):
            if member not in value:
                return element, member
    return None


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "kuratowski_encode":
        match = re.fullmatch(
            r"Ordered pair: (.+)\. Definition: \(a, b\) = "
            r"\{\{a\}, \{a, b\}\}\.", body)
        assert match is not None, body
        first, second = oracle.parse_pair(match.group(1))
        value = kuratowski(first, second)
        answer = set_text(value)
    elif variant == "kuratowski_decode":
        match = re.fullmatch(
            r"K = (.+)\. Definition: \(a, b\) = \{\{a\}, \{a, b\}\}\.",
            body)
        assert match is not None, body
        value = oracle.parse_set(match.group(1))
        decoded = decode_kuratowski(value)
        answer = oracle.element_text(decoded)
    elif variant == "von_neumann_numeral":
        match = re.fullmatch(
            r"n = (\d+)\. Definition: 0 = ∅ and S\(k\) = k ∪ \{k\}\.", body)
        assert match is not None, body
        number = int(match.group(1))
        value = numeral(number)
        answer = set_text(value)
    elif variant == "successor":
        match = re.fullmatch(
            r"X = (.+)\. Definition: S\(X\) = X ∪ \{X\}\.", body)
        assert match is not None, body
        source = oracle.parse_set(match.group(1))
        value = successor(source)
        answer = set_text(value)
    elif variant == "big_union":
        match = re.fullmatch(r"X = (.+)\.", body)
        assert match is not None, body
        source = oracle.parse_set(match.group(1))
        value = frozenset(member for element in source for member in element)
        answer = set_text(value)
    elif variant == "transitive_check":
        match = re.fullmatch(
            r"X = (.+)\. A set is transitive iff every element of X is a "
            r"subset of X\.", body)
        assert match is not None, body
        value = oracle.parse_set(match.group(1))
        witness = transitivity_witness(value)
        if witness is None:
            answer = "transitive: yes (every element is a subset of X)"
        else:
            element, missing = witness
            answer = (f"transitive: no ({set_text(element)} ∈ X but "
                      f"{set_text(missing)} ∉ X)")
    else:
        match = re.fullmatch(
            r"X = (.+)\. Use rank\(∅\) = 0 and "
            r"rank\(X\) = max\(rank\(e\) \+ 1 : e ∈ X\)\.", body)
        assert match is not None, body
        value = oracle.parse_set(match.group(1))
        answer = str(rank(value))
    return {"variant": variant, "query": query, "value": value,
            "answer": answer}


class HereditarilyFiniteSetGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(833117)

    def test_output_contract(self):
        example = HereditarilyFiniteSetGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = HereditarilyFiniteSetGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_rank_union_and_transitivity_steps_are_exact(self):
        for variant in ("rank", "big_union", "transitive_check"):
            generator = HereditarilyFiniteSetGenerator(variant)
            for _ in range(200):
                example = generator.generate()
                parts = oracle_parts(example)
                fields = [raw.split(DELIM) for raw in example["steps"]]
                if variant == "rank":
                    for item in fields:
                        if item[0] == "RANK":
                            self.assertEqual(int(item[2]),
                                             rank(oracle.parse_set(item[1])))
                elif variant == "big_union":
                    contributions = {oracle.parse_set(item[1]) for item in fields
                                     if item[0] == "UNION_ELEMENT"}
                    body, _, _ = split_query(example["problem"])
                    source = re.fullmatch(r"X = (.+)\.", body).group(1)
                    self.assertEqual(contributions,
                                     set(oracle.parse_set(source)))
                else:
                    witness = transitivity_witness(parts["value"])
                    checks = [item for item in fields
                              if item[0] == "TRANSITIVE_CHECK"]
                    if witness is not None:
                        self.assertEqual(oracle.parse_set(checks[-1][1]), witness[0])
                        self.assertTrue(checks[-1][2].endswith("no"))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in HereditarilyFiniteSetGenerator.VARIANTS:
            generator = HereditarilyFiniteSetGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"hereditarily_finite_set_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HereditarilyFiniteSetGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = HereditarilyFiniteSetGenerator()
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
