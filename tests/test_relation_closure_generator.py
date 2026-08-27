"""Independent fixed-point and Warshall oracle for RelationClosureGenerator."""
import random
import re
import unittest

from generators.relation_closure_generator import QUERIES, RelationClosureGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    match = re.fullmatch(r"A = (.+)\. R = (.+)\.", body)
    assert match is not None, body
    values = tuple(oracle.parse_roster(match.group(1)))
    relation = frozenset(oracle.parse_pair_roster(match.group(2)))
    if variant == "reflexive":
        result = oracle.brute_reflexive_closure(relation, values)
    elif variant == "symmetric":
        result = oracle.brute_symmetric_closure(relation)
    elif variant in ("transitive_warshall", "transitive_by_paths"):
        result = oracle.brute_transitive_closure(relation)
    else:
        result = oracle.brute_equivalence_closure(relation, values)
    return {"variant": variant, "query": query, "A": values, "R": relation,
            "result": result, "answer": oracle.roster_text(result)}


def warshall_snapshots(relation, values):
    size = len(values)
    matrix = [[(values[row], values[column]) in relation
               for column in range(size)] for row in range(size)]
    snapshots = []
    for pivot in range(size):
        for row in range(size):
            for column in range(size):
                matrix[row][column] = (matrix[row][column]
                                       or (matrix[row][pivot]
                                           and matrix[pivot][column]))
        text = "; ".join(" ".join("1" if value else "0" for value in row)
                         for row in matrix)
        snapshots.append((values[pivot], text))
    return snapshots


class RelationClosureGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(829541)

    def test_output_contract(self):
        example = RelationClosureGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RelationClosureGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_added_pairs_paths_and_final_properties(self):
        generator = RelationClosureGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            current = set(parts["R"])
            for raw_step in example["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CLOSURE_ADD":
                    pair = oracle.parse_pair(fields[1])
                    self.assertNotIn(pair, current)
                    if fields[2] == "reflexive":
                        self.assertEqual(pair[0], pair[1])
                    else:
                        self.assertIn((pair[1], pair[0]), current)
                    current.add(pair)
                elif fields[0] == "PATH":
                    match = re.fullmatch(r"(\d+)→(\d+)→(\d+)", fields[1])
                    self.assertIsNotNone(match)
                    first, middle, last = map(int, match.groups())
                    self.assertIn((first, middle), current)
                    self.assertIn((middle, last), current)
                    self.assertNotIn((first, last), current)
                    self.assertEqual(fields[2], f"add ({first}, {last})")
                    current.add((first, last))
            if parts["variant"] != "transitive_warshall":
                self.assertEqual(current, set(parts["result"]))
            properties = oracle.brute_properties(parts["result"], parts["A"])
            if parts["variant"] == "reflexive":
                self.assertTrue(properties["reflexive"])
            elif parts["variant"] == "symmetric":
                self.assertTrue(properties["symmetric"])
            elif parts["variant"] == "equivalence_closure":
                self.assertTrue(properties["reflexive"])
                self.assertTrue(properties["symmetric"])
                self.assertTrue(properties["transitive"])
            else:
                self.assertTrue(properties["transitive"])

    def test_warshall_snapshots_match_independent_algorithm(self):
        generator = RelationClosureGenerator("transitive_warshall")
        for _ in range(180):
            example = generator.generate()
            parts = oracle_parts(example)
            observed = [(int(fields[1].split("=")[1]), fields[2])
                        for fields in (step_text.split(DELIM)
                                       for step_text in example["steps"])
                        if fields[0] == "WARSHALL_K"]
            self.assertEqual(observed, warshall_snapshots(parts["R"], parts["A"]))

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RelationClosureGenerator.VARIANTS:
            generator = RelationClosureGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"relation_closure_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RelationClosureGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RelationClosureGenerator()
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
