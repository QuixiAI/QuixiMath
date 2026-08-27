"""Independent finite-pair oracle for RelationOperationsGenerator."""
import random
import re
import unittest

from generators.relation_operations_generator import QUERIES, RelationOperationsGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def pair_text(pairs):
    return oracle.roster_text(frozenset(map(tuple, pairs)))


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    if variant == "composition":
        match = re.fullmatch(
            r"A = (.+)\. B = (.+)\. C = (.+)\. R = (.+)\. S = (.+)\.",
            body,
        )
        assert match is not None, body
        set_a, set_b, set_c = (oracle.parse_set(match.group(index))
                               for index in (1, 2, 3))
        first = frozenset(oracle.parse_pair_roster(match.group(4)))
        second = frozenset(oracle.parse_pair_roster(match.group(5)))
        result = frozenset((a, c) for a, b in first for b2, c in second
                           if b == b2)
        return {"variant": variant, "query": query, "A": set_a, "B": set_b,
                "C": set_c, "R": first, "S": second, "result": result,
                "answer": pair_text(result)}
    if variant == "restriction":
        match = re.fullmatch(
            r"A = (.+)\. B = (.+)\. R = (.+)\. D = (.+)\.", body)
        assert match is not None, body
        subset = oracle.parse_set(match.group(4))
    else:
        match = re.fullmatch(r"A = (.+)\. B = (.+)\. R = (.+)\.", body)
        assert match is not None, body
        subset = None
    set_a, set_b = oracle.parse_set(match.group(1)), oracle.parse_set(match.group(2))
    relation = frozenset(oracle.parse_pair_roster(match.group(3)))
    if variant == "inverse":
        result = frozenset((second, first) for first, second in relation)
        answer = pair_text(result)
    elif variant == "matrix":
        rows = [" ".join("1" if (first, second) in relation else "0"
                         for second in sorted(set_b, key=oracle.element_key))
                for first in sorted(set_a, key=oracle.element_key)]
        result, answer = rows, "; ".join(rows)
    elif variant == "domain_range":
        domain = frozenset(first for first, _ in relation)
        range_values = frozenset(second for _, second in relation)
        result = (domain, range_values)
        answer = (f"domain = {oracle.roster_text(domain)}; "
                  f"range = {oracle.roster_text(range_values)}")
    else:
        result = frozenset(pair for pair in relation if pair[0] in subset)
        answer = pair_text(result)
    return {"variant": variant, "query": query, "A": set_a, "B": set_b,
            "R": relation, "D": subset, "result": result, "answer": answer}


class RelationOperationsGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(740233)

    def test_output_contract(self):
        example = RelationOperationsGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = RelationOperationsGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_pair_matrix_projection_and_restriction_steps(self):
        generator = RelationOperationsGenerator()
        for _ in range(300):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            if parts["variant"] == "inverse":
                emitted = {(oracle.parse_pair(item[1]), oracle.parse_pair(item[2]))
                           for item in steps if item[0] == "INVERSE_PAIR"}
                expected = {(pair, (pair[1], pair[0])) for pair in parts["R"]}
                self.assertEqual(emitted, expected)
            elif parts["variant"] == "composition":
                emitted = {oracle.parse_pair(item[3]) for item in steps
                           if item[0] == "COMPOSE_PAIR"}
                self.assertEqual(emitted, set(parts["result"]))
            elif parts["variant"] == "matrix":
                rows = [item[2] for item in steps if item[0] == "MATRIX_ROW"]
                self.assertEqual(rows, parts["result"])
            elif parts["variant"] == "domain_range":
                self.assertIn(["DOMAIN", oracle.roster_text(parts["result"][0])],
                              steps)
                self.assertIn(["RANGE", oracle.roster_text(parts["result"][1])],
                              steps)
            else:
                checks = [item for item in steps if item[0] == "RESTRICT_CHECK"]
                self.assertEqual(len(checks), len(parts["R"]))
                for item in checks:
                    pair = oracle.parse_pair(item[1])
                    self.assertEqual(item[3],
                                     "keep" if pair[0] in parts["D"] else "skip")

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in RelationOperationsGenerator.VARIANTS:
            generator = RelationOperationsGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"relation_operations_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RelationOperationsGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = RelationOperationsGenerator()
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
