"""Independent class-graph oracle for EquivalenceRelationGenerator."""
import random
import re
import unittest

from generators.equivalence_relation_generator import QUERIES, EquivalenceRelationGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def canonical_partition(blocks):
    blocks = [sorted(block, key=oracle.element_key) for block in blocks]
    blocks.sort(key=lambda block: oracle.element_key(block[0]))
    return "{" + ", ".join(oracle.roster_text(block) for block in blocks) + "}"


def relation_from_blocks(blocks):
    return frozenset((first, second)
                     for block in blocks for first in block for second in block)


def blocks_from_key(values, key):
    grouped = {}
    for value in sorted(values):
        grouped.setdefault(key(value), []).append(value)
    return list(grouped.values())


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "check_and_classes":
        match = re.fullmatch(r"A = (.+)\. R = (.+)\.", body)
        assert match is not None, body
        values = oracle.parse_set(match.group(1))
        relation = frozenset(oracle.parse_pair_roster(match.group(2)))
        blocks = oracle.brute_equivalence_classes(relation, values)
        answer = canonical_partition(blocks)
        return {"variant": variant, "query": query, "A": values,
                "R": relation, "blocks": blocks, "answer": answer}
    if variant in ("from_partition", "count_pairs"):
        match = re.fullmatch(r"A = (.+)\. Partition P = (.+)\.", body)
        assert match is not None, body
        values = oracle.parse_set(match.group(1))
        blocks = oracle.parse_partition(match.group(2))
        relation = relation_from_blocks(blocks)
        answer = (oracle.roster_text(relation) if variant == "from_partition"
                  else str(len(relation)))
        return {"variant": variant, "query": query, "A": values,
                "R": relation, "blocks": blocks, "answer": answer}
    if variant == "congruence_classes":
        match = re.fullmatch(
            r"A = (.+)\. m = (\d+)\. Relation: xRy iff x ≡ y \(mod m\)\.",
            body,
        )
        assert match is not None, body
        values, modulus = oracle.parse_set(match.group(1)), int(match.group(2))
        blocks = blocks_from_key(values, lambda value: value % modulus)
        return {"variant": variant, "query": query, "A": values,
                "blocks": blocks, "answer": canonical_partition(blocks)}
    match = re.fullmatch(r"A = (.+)\. Rule: (.+)\.", body)
    assert match is not None, body
    values, rule = oracle.parse_set(match.group(1)), match.group(2)
    if rule == "xRy iff x and y have the same parity":
        key = lambda value: value % 2
    elif rule == "xRy iff x and y have the same digit sum":
        key = lambda value: sum(int(digit) for digit in str(value))
    else:
        rule_match = re.fullmatch(
            r"xRy iff x and y have the same remainder modulo (\d+)", rule)
        assert rule_match is not None, rule
        modulus = int(rule_match.group(1))
        key = lambda value: value % modulus
    blocks = blocks_from_key(values, key)
    return {"variant": variant, "query": query, "A": values,
            "blocks": blocks, "answer": canonical_partition(blocks)}


class EquivalenceRelationGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(501823)

    def test_output_contract(self):
        example = EquivalenceRelationGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = EquivalenceRelationGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_classes_relations_and_property_checks_are_exact(self):
        generator = EquivalenceRelationGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            if "R" in parts:
                properties = oracle.brute_properties(parts["R"], parts["A"])
                self.assertTrue(properties["reflexive"])
                self.assertTrue(properties["symmetric"])
                self.assertTrue(properties["transitive"])
            partition_steps = [item for item in steps if item[0] == "PARTITION"]
            if parts["variant"] != "check_and_classes" or partition_steps:
                expected_partition = canonical_partition(parts["blocks"])
                self.assertIn(["PARTITION", expected_partition], steps)
            if parts["variant"] == "from_partition":
                emitted = {oracle.parse_pair(item[1]) for item in steps
                           if item[0] == "REL_PAIR"}
                self.assertEqual(emitted, set(parts["R"]))

    def test_pair_count_arithmetic(self):
        generator = EquivalenceRelationGenerator("count_pairs")
        for _ in range(200):
            example = generator.generate()
            running = 0
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]))
                    running = int(fields[3])
            self.assertEqual(running, int(example["final_answer"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in EquivalenceRelationGenerator.VARIANTS:
            generator = EquivalenceRelationGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"equivalence_relation_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EquivalenceRelationGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = EquivalenceRelationGenerator()
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
