"""Independent finite-poset oracle for PartialOrderGenerator."""
import itertools
import random
import re
import unittest

from generators.partial_order_generator import QUERIES, PartialOrderGenerator
from helpers import DELIM
from tests import foundations_oracle as oracle


def split_query(problem):
    for variant, queries in QUERIES.items():
        for query in queries:
            suffix = " " + query
            if problem.endswith(suffix):
                return problem[:-len(suffix)], variant, query
    raise AssertionError(problem)


def value_text(value):
    return oracle.element_text(value)


def sequence_text(values):
    return ", ".join(value_text(value) for value in values)


def relation_text(pairs):
    return oracle.roster_text(frozenset(pairs))


def parse_poset(body):
    div_match = re.fullmatch(
        r"Carrier A = (.+)\. Order rule: a ≤ b iff a divides b\.(?: Q = (.+)\.)?",
        body,
    )
    if div_match:
        elements = tuple(oracle.parse_roster(div_match.group(1)))
        order = frozenset((first, second) for first in elements for second in elements
                          if second % first == 0)
        subset = (oracle.parse_set(div_match.group(2))
                  if div_match.group(2) else None)
        return "divisibility", elements, order, subset
    subset_match = re.fullmatch(
        r"Base B = (.+)\. Carrier A = (.+)\. "
        r"Order rule: X ≤ Y iff X ⊆ Y\.(?: Q = (.+)\.)?",
        body,
    )
    if subset_match:
        elements = tuple(oracle.parse_roster(subset_match.group(2)))
        order = frozenset((first, second) for first in elements for second in elements
                          if first <= second)
        subset = (oracle.parse_set(subset_match.group(3))
                  if subset_match.group(3) else None)
        return "subset", elements, order, subset
    explicit_match = re.fullmatch(
        r"Carrier A = (.+)\. Hasse edges H = (.+)\. "
        r"Order rule: reflexive-transitive closure of H\.(?: Q = (.+)\.)?",
        body,
    )
    assert explicit_match is not None, body
    elements = tuple(oracle.parse_roster(explicit_match.group(1)))
    edges = frozenset(oracle.parse_pair_roster(explicit_match.group(2)))
    relation = set(edges) | {(value, value) for value in elements}
    order = oracle.brute_transitive_closure(relation)
    subset = (oracle.parse_set(explicit_match.group(3))
              if explicit_match.group(3) else None)
    return "explicit", elements, order, subset


def extrema(order, elements):
    strict = {(first, second) for first, second in order if first != second}
    ordered = sorted(elements, key=oracle.element_key)
    minima = [value for value in ordered
              if not any(second == value for _, second in strict)]
    maxima = [value for value in ordered
              if not any(first == value for first, _ in strict)]
    least = next((value for value in ordered
                  if all((value, other) in order for other in elements)), None)
    greatest = next((value for value in ordered
                     if all((other, value) in order for other in elements)), None)
    answer = (f"minimal {oracle.roster_text(minima)}; "
              f"maximal {oracle.roster_text(maxima)}; "
              f"least {value_text(least) if least is not None else 'none'}; "
              f"greatest {value_text(greatest) if greatest is not None else 'none'}")
    return minima, maxima, least, greatest, answer


def maximum_chain_antichain(order, elements):
    ordered = tuple(sorted(elements, key=oracle.element_key))
    best_chain = best_antichain = ()
    for size in range(len(ordered) + 1):
        for subset in itertools.combinations(ordered, size):
            if (all((a, b) in order or (b, a) in order
                    for a, b in itertools.combinations(subset, 2))
                    and len(subset) > len(best_chain)):
                best_chain = subset
            if (all((a, b) not in order and (b, a) not in order
                    for a, b in itertools.combinations(subset, 2))
                    and len(subset) > len(best_antichain)):
                best_antichain = subset
    return best_chain, best_antichain


def oracle_parts(example):
    body, variant, query = split_query(example["problem"])
    family, elements, order, subset = parse_poset(body)
    if variant == "hasse_edges":
        result = oracle.brute_cover(order, elements)
        answer = relation_text(result)
    elif variant == "extremal_elements":
        *result, answer = extrema(order, elements)
    elif variant == "bounds_lub_glb":
        result = (oracle.brute_upper_bounds(order, elements, subset),
                  oracle.brute_lower_bounds(order, elements, subset),
                  oracle.brute_lub(order, elements, subset),
                  oracle.brute_glb(order, elements, subset))
        answer = (f"lub {value_text(result[2]) if result[2] is not None else 'none'}; "
                  f"glb {value_text(result[3]) if result[3] is not None else 'none'}")
    elif variant == "linear_extension":
        result = oracle.brute_linear_extension(order, elements)
        answer = sequence_text(result)
    elif variant == "lattice_check":
        failure = None
        ordered = sorted(elements, key=oracle.element_key)
        for index, first in enumerate(ordered):
            for second in ordered[index:]:
                pair_subset = (first, second)
                pair_lub = oracle.brute_lub(order, elements, pair_subset)
                pair_glb = oracle.brute_glb(order, elements, pair_subset)
                if failure is None and (pair_lub is None or pair_glb is None):
                    failure = (first, second, "lub" if pair_lub is None else "glb")
        if failure is None:
            answer = "lattice yes"
        else:
            first, second, missing = failure
            answer = (f"lattice no; pair ({value_text(first)}, {value_text(second)}) "
                      f"lacks {missing}")
        result = failure
    else:
        result = maximum_chain_antichain(order, elements)
        answer = (f"chain {oracle.roster_text(result[0])}; "
                  f"antichain {oracle.roster_text(result[1])}")
    return {"variant": variant, "query": query, "family": family,
            "A": elements, "order": order, "Q": subset, "result": result,
            "answer": answer}


class PartialOrderGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(953111)

    def test_output_contract(self):
        example = PartialOrderGenerator().generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, example)
        self.assertEqual(example["steps"][-1],
                         f"Z{DELIM}{example['final_answer']}")

    def test_oracle_recomputes_500_answers_from_problem_text(self):
        generator = PartialOrderGenerator()
        for _ in range(500):
            example = generator.generate()
            self.assertEqual(example["final_answer"],
                             oracle_parts(example)["answer"],
                             example["problem"])

    def test_cover_bounds_topological_and_witness_steps(self):
        generator = PartialOrderGenerator()
        for _ in range(250):
            example = generator.generate()
            parts = oracle_parts(example)
            steps = [item.split(DELIM) for item in example["steps"]]
            if parts["variant"] == "hasse_edges":
                emitted_pairs = {(parse_value(item[1]), parse_value(item[2]))
                                 for item in steps if item[0] == "COVER"}
                self.assertEqual(emitted_pairs, set(parts["result"]))
            elif parts["variant"] == "bounds_lub_glb":
                uppers, lowers, pair_lub, pair_glb = parts["result"]
                self.assertIn(["UB", oracle.roster_text(parts["Q"]),
                               oracle.roster_text(uppers)], steps)
                self.assertIn(["LB", oracle.roster_text(parts["Q"]),
                               oracle.roster_text(lowers)], steps)
            elif parts["variant"] == "linear_extension":
                picks = [item[2].removeprefix("pick ") for item in steps
                         if item[0] == "TOPO_PICK"]
                self.assertEqual(picks, [value_text(value)
                                         for value in parts["result"]])
            elif parts["variant"] == "chains_antichains":
                self.assertIn(["CHAIN", oracle.roster_text(parts["result"][0]),
                               f"length {len(parts['result'][0])}"], steps)
                self.assertIn(["ANTICHAIN",
                               oracle.roster_text(parts["result"][1]),
                               f"size {len(parts['result'][1])}"], steps)

    def test_all_variants_phrasings_and_poset_families(self):
        families = set()
        for variant in PartialOrderGenerator.VARIANTS:
            generator = PartialOrderGenerator(variant)
            seen_queries = set()
            for _ in range(350):
                example = generator.generate()
                parts = oracle_parts(example)
                self.assertEqual(parts["variant"], variant)
                self.assertEqual(example["operation"], f"partial_order_{variant}")
                seen_queries.add(parts["query"])
                families.add(parts["family"])
            self.assertEqual(seen_queries, set(QUERIES[variant]))
        self.assertEqual(families, {"divisibility", "subset", "explicit"})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PartialOrderGenerator("bogus")

    def test_pipe_safety_and_render_sanity(self):
        generator = PartialOrderGenerator()
        for _ in range(200):
            example = generator.generate()
            self.assertNotIn(DELIM, example["problem"])
            self.assertNotIn(DELIM, example["final_answer"])
            self.assertNotRegex(example["problem"], r"1x|\^1|\+ 0|--")
            for raw_step in example["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


def parse_value(text):
    values = oracle.parse_set("{" + text + "}")
    assert len(values) == 1
    return next(iter(values))


if __name__ == "__main__":
    unittest.main()
