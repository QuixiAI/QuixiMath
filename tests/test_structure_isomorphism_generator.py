"""Independent brute-force oracle for StructureIsomorphismGenerator."""
import itertools
import random
import re
import unittest

from generators.structure_isomorphism_generator import (
    QUERIES, StructureIsomorphismGenerator,
)
from helpers import DELIM
from tests import foundations_oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def parse_relation(text):
    if text == "∅":
        return set()
    return set(foundations_oracle.parse_pair_roster(text))


def parse_map(text):
    mapping = {}
    for binding in text.split(", "):
        source, target = binding.split("→")
        mapping[int(source)] = target
    return mapping


def map_text(mapping, left):
    return ", ".join(f"{value}→{mapping[value]}" for value in left)


def pair_text(pair):
    return f"({pair[0]}, {pair[1]})"


def parse_structures(body):
    match = re.fullmatch(
        r"Structure kind: (directed graph|relation|strict poset)\. Left "
        r"points: (\{[^{}]*\}); left relation: (.+?)\. Right points: "
        r"(\{[^{}]*\}); right relation: (.+?)\. (.+)", body)
    assert match is not None, body
    kind, left_text, left_relation, right_text, right_relation, rest = match.groups()
    left = tuple(foundations_oracle.parse_roster(left_text))
    right = tuple(foundations_oracle.parse_roster(right_text))
    return (kind, left, parse_relation(left_relation), right,
            parse_relation(right_relation), rest)


def first_discrepancy(left_edges, right_edges, mapping, left):
    for a in left:
        for b in left:
            source = (a, b) in left_edges
            target = (mapping[a], mapping[b])
            if source != (target in right_edges):
                return (a, b), target, source
    return None


def invariant_values(edges, nodes):
    out_degrees = sorted(sum((node, other) in edges for other in nodes)
                         for node in nodes)
    cycles = sum((a, b) in edges and (b, a) in edges
                 for index, a in enumerate(nodes)
                 for b in nodes[index + 1:])
    fixed = sum((node, node) in edges for node in nodes)
    return len(nodes), out_degrees, cycles, fixed


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    kind, left, left_edges, right, right_edges, rest = parse_structures(body)
    if variant == "check_given_map":
        match = re.fullmatch(r"Given bijection: f = (.+)\.", rest)
        assert match is not None, rest
        mapping = parse_map(match.group(1))
        discrepancy = first_discrepancy(
            left_edges, right_edges, mapping, left)
        if discrepancy is None:
            answer, case = f"isomorphism; f = {map_text(mapping, left)}", "valid"
        else:
            source, target, source_present = discrepancy
            status = "absent" if source_present else "present"
            answer = (f"not an isomorphism; pair {pair_text(source)} maps to "
                      f"{pair_text(target)}, which is {status}")
            case = "invalid"
    elif variant == "find_map":
        assert rest == ("Test bijections in lexicographic order of the "
                        "right-side image tuple."), rest
        mapping = None
        for permutation in itertools.permutations(right):
            candidate = dict(zip(left, permutation))
            if first_discrepancy(
                    left_edges, right_edges, candidate, left) is None:
                mapping = candidate
                break
        assert mapping is not None
        answer, case = f"isomorphic; f = {map_text(mapping, left)}", "find"
    else:
        assert rest == ("Invariant order: sizes; out-degree multisets; directed "
                        "2-cycle counts; fixed-point counts."), rest
        left_values = invariant_values(left_edges, left)
        right_values = invariant_values(right_edges, right)
        labels = ("sizes", "out-degree multisets", "directed 2-cycle counts",
                  "fixed-point counts")
        index = next(i for i, values in enumerate(zip(left_values, right_values))
                     if values[0] != values[1])
        answer = (f"not isomorphic; {labels[index]} differ "
                  f"({left_values[index]} vs {right_values[index]})")
        case = labels[index]
    return {"variant": variant, "query": query, "answer": answer,
            "case": case, "kind": kind, "left": left,
            "left_edges": left_edges, "right": right,
            "right_edges": right_edges}


class StructureIsomorphismGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(244949)

    def test_output_contract(self):
        example = StructureIsomorphismGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = StructureIsomorphismGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_find_map_is_lexicographically_first(self):
        generator = StructureIsomorphismGenerator("find_map")
        for _ in range(150):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"])

    def test_every_verdict_invariant_and_kind_is_reachable(self):
        check = StructureIsomorphismGenerator("check_given_map")
        self.assertEqual({oracle_parts(check.generate())["case"]
                          for _ in range(300)}, {"valid", "invalid"})
        noniso = StructureIsomorphismGenerator("non_isomorphic_invariant")
        self.assertEqual({oracle_parts(noniso.generate())["case"]
                          for _ in range(500)},
                         {"sizes", "out-degree multisets",
                          "directed 2-cycle counts", "fixed-point counts"})
        all_kinds = StructureIsomorphismGenerator()
        self.assertEqual({oracle_parts(all_kinds.generate())["kind"]
                          for _ in range(500)},
                         {"directed graph", "relation", "strict poset"})

    def test_all_variants_and_five_phrasings_are_reachable(self):
        for variant in StructureIsomorphismGenerator.VARIANTS:
            generator = StructureIsomorphismGenerator(variant)
            seen_queries = set()
            for _ in range(240):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"],
                                 f"structure_isomorphism_{variant}")
                seen_queries.add(parts["query"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StructureIsomorphismGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = StructureIsomorphismGenerator()
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
