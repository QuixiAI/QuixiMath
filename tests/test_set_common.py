"""Tests for ``set_common`` — checked against the independent oracle.

Formatting is verified by parsing the printed text back with
``tests/foundations_oracle.py``; every structural routine (closures, covers,
bounds, linear extensions, classes) is cross-checked against the oracle's
brute-force route.
"""
import itertools
import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import set_common as S  # noqa: E402
from tests import foundations_oracle as O  # noqa: E402


def random_elements(rng, count):
    """A small multiset of mixed elements (ints, letters, pairs, sets)."""
    pool = []
    for _ in range(count):
        kind = rng.randrange(5)
        if kind == 0:
            pool.append(rng.randint(-9, 20))
        elif kind == 1:
            pool.append(rng.choice("abcdefg"))
        elif kind == 2:
            pool.append((rng.randint(1, 5), rng.randint(1, 5)))
        elif kind == 3:
            pool.append(frozenset(rng.sample(range(1, 8),
                                             rng.randint(0, 3))))
        else:
            pool.append(frozenset({frozenset(rng.sample(range(1, 5), 1))}))
    return pool


def random_relation(rng, elements, density=0.35):
    return frozenset((a, b) for a in elements for b in elements
                     if rng.random() < density)


def random_poset(rng, elements, density=0.4):
    """A random partial order, built with the oracle's closures only."""
    ordered = list(elements)
    rng.shuffle(ordered)
    edges = {(ordered[i], ordered[j])
             for i in range(len(ordered)) for j in range(i + 1, len(ordered))
             if rng.random() < density}
    return O.brute_reflexive_closure(O.brute_transitive_closure(edges),
                                     elements)


class RosterFormatTest(unittest.TestCase):
    def test_plan_examples(self):
        self.assertEqual(S.roster([3, 1, 2, 1]), "{1, 2, 3}")
        self.assertEqual(S.roster([]), "∅")
        self.assertEqual(S.roster(["b", "a"]), "{a, b}")
        self.assertEqual(S.pair("a", "b"), "(a, b)")
        self.assertEqual(S.pair_roster([(2, 1), (1, 3), (1, 2)]),
                         "{(1, 2), (1, 3), (2, 1)}")
        self.assertEqual(S.partition_text([[4, 5], [2], [3, 1]]),
                         "{{1, 3}, {2}, {4, 5}}")
        self.assertEqual(S.card_text("A"), "card(A)")
        self.assertEqual(S.card_eq("A", 4), "card(A) = 4")
        self.assertEqual(S.set_builder(S.range_condition(-3, 4)),
                         "{x ∈ ℤ : −3 ≤ x < 4}")
        self.assertEqual(S.sequence_text([1, 2, 3, 4, 6, 12]),
                         "1, 2, 3, 4, 6, 12")
        self.assertEqual(S.map_text({2: "a", 1: "b"}), "1→b, 2→a")

    def test_random_rosters_parse_back_sorted_and_deduplicated(self):
        rng = random.Random(3)
        for _ in range(2000):
            items = random_elements(rng, rng.randint(0, 6))
            text = S.roster(items)
            self.assertNotIn("|", text)
            listed = O.parse_roster(text)
            self.assertFalse(O.has_duplicates(listed), text)
            self.assertTrue(O.roster_order_ok(listed), text)
            self.assertEqual(frozenset(listed), frozenset(items), text)

    def test_nested_sets_sort_by_depth_then_elements(self):
        self.assertEqual(S.roster([frozenset({1, 2}), frozenset()]),
                         "{∅, {1, 2}}")
        self.assertEqual(
            S.roster([frozenset({"a", "b"}), frozenset({"a"})]),
            "{{a}, {a, b}}")
        self.assertEqual(
            S.roster([frozenset({frozenset()}), frozenset({1})]),
            "{{1}, {∅}}")

    def test_partitions_parse_back_with_blocks_in_order(self):
        rng = random.Random(5)
        for _ in range(500):
            size = rng.randint(1, 7)
            labels = list(range(1, size + 1))
            rng.shuffle(labels)
            cuts = sorted(rng.sample(range(1, size), rng.randint(0, size - 1)))
            blocks = []
            previous = 0
            for cut in cuts + [size]:
                blocks.append(labels[previous:cut])
                previous = cut
            text = S.partition_text(blocks)
            parsed = O.parse_partition(text)
            self.assertEqual([min(block) for block in parsed],
                             sorted(min(block) for block in parsed), text)
            self.assertEqual(frozenset(frozenset(b) for b in blocks),
                             frozenset(parsed), text)

    def test_set_builder_agrees_with_the_oracle(self):
        rng = random.Random(7)
        for _ in range(200):
            low = rng.randint(-8, 4)
            high = low + rng.randint(1, 12)
            word, test = rng.choice([
                ("x is odd", lambda v: v % 2 != 0),
                ("x is even", lambda v: v % 2 == 0),
                ("x is prime", lambda v: v > 1 and all(
                    v % d for d in range(2, int(v ** 0.5) + 1))),
                ("3 divides x", lambda v: v % 3 == 0),
            ])
            condition = "%s and %s" % (S.range_condition(low, high), word)
            text = S.set_builder(condition)
            self.assertNotIn("|", text)
            expected = [v for v in range(low, high) if test(v)]
            self.assertEqual(O.eval_set_builder(text), expected, text)
            self.assertEqual(S.roster(expected),
                             O.element_text(frozenset(expected)))

    def test_matrix_rendering(self):
        pairs = {(1, 2), (2, 3), (3, 1)}
        self.assertEqual(S.matrix_rows(pairs, [1, 2, 3]),
                         ["0 1 0", "0 0 1", "1 0 0"])
        self.assertEqual(S.matrix_text(pairs, [1, 2, 3]),
                         "0 1 0; 0 0 1; 1 0 0")
        self.assertEqual(S.matrix_pairs(S.relation_matrix(pairs, [1, 2, 3]),
                                        [1, 2, 3]), frozenset(pairs))

    def test_unicode_minus_option(self):
        self.assertEqual(S.roster([-3, 1]), "{-3, 1}")
        self.assertEqual(S.roster([-3, 1], unicode_minus=True), "{−3, 1}")
        self.assertEqual(O.parse_roster("{−3, 1}"), [-3, 1])


class SetOperationTest(unittest.TestCase):
    def test_operations_match_the_oracle_evaluator(self):
        rng = random.Random(11)
        universe = frozenset(range(1, 11))
        for _ in range(300):
            env = {name: frozenset(rng.sample(sorted(universe),
                                              rng.randint(0, 6)))
                   for name in "ABC"}
            expected = O.eval_set_expression("(A ∪ B)ᶜ ∩ C", env, universe)
            got = S.intersection(S.complement(universe,
                                              S.union(env["A"], env["B"])),
                                 env["C"])
            self.assertEqual(got, expected)
            expected = O.eval_set_expression("A Δ (B − C)", env, universe)
            got = S.symmetric_difference(
                env["A"], S.difference(env["B"], env["C"]))
            self.assertEqual(got, expected)

    def test_powerset_and_product(self):
        subsets = S.powerset([1, 2, 3])
        self.assertEqual(len(subsets), 8)
        self.assertEqual(S.roster(subsets),
                         "{∅, {1}, {1, 2}, {1, 2, 3}, {1, 3}, {2}, {2, 3}, "
                         "{3}}")
        self.assertEqual(
            S.pair_roster(S.cartesian_product({1, 2}, {"a"})),
            "{(1, a), (2, a)}")
        expected = O.eval_set_expression("P(A)", {"A": {1, 2}}, frozenset())
        self.assertEqual(frozenset(S.powerset([1, 2])), expected)


class HereditarilyFiniteTest(unittest.TestCase):
    def test_von_neumann_numerals(self):
        self.assertEqual(S.hf_text(S.von_neumann(0)), "∅")
        self.assertEqual(S.hf_text(S.von_neumann(1)), "{∅}")
        self.assertEqual(S.hf_text(S.von_neumann(2)), "{∅, {∅}}")
        self.assertEqual(S.hf_text(S.von_neumann(3)), "{∅, {∅}, {∅, {∅}}}")
        for n in range(7):
            numeral = S.von_neumann(n)
            self.assertEqual(S.von_neumann_index(numeral), n)
            self.assertEqual(S.set_rank(numeral), n)
            self.assertEqual(len(numeral), n)
            self.assertEqual(S.successor(numeral), S.von_neumann(n + 1))
            self.assertEqual(O.parse_set(S.hf_text(numeral)), numeral)
            self.assertTrue(S.is_transitive(numeral))
        with self.assertRaises(ValueError):
            S.von_neumann_index(frozenset({frozenset({frozenset()})}))

    def test_rank_and_depth(self):
        self.assertEqual(S.set_rank(frozenset()), 0)
        self.assertEqual(S.set_depth(frozenset()), 1)
        nested = frozenset({frozenset({frozenset()})})
        self.assertEqual(S.set_rank(nested), 2)
        self.assertEqual(S.set_depth(nested), 3)
        self.assertEqual(S.set_depth(3), 0)

    def test_transitivity_witness(self):
        self.assertIsNone(S.transitivity_witness(S.von_neumann(4)))
        bad = frozenset({frozenset({frozenset()})})
        witness = S.transitivity_witness(bad)
        self.assertEqual(witness, (frozenset({frozenset()}), frozenset()))
        self.assertEqual(
            "transitive: no (%s ∈ X but %s ∉ X)"
            % (S.hf_text(witness[0]), S.hf_text(witness[1])),
            "transitive: no ({∅} ∈ X but ∅ ∉ X)")

    def test_kuratowski_round_trip(self):
        rng = random.Random(13)
        for _ in range(300):
            first = rng.choice([1, 2, "a", "b", frozenset(), frozenset({1})])
            second = rng.choice([1, 2, "a", "b", frozenset(),
                                 frozenset({1})])
            encoded = S.kuratowski(first, second)
            self.assertEqual(S.un_kuratowski(encoded), (first, second))
            self.assertEqual(O.parse_set(S.hf_text(encoded)), encoded)
        self.assertEqual(S.hf_text(S.kuratowski("a", "b")), "{{a}, {a, b}}")
        self.assertEqual(S.hf_text(S.kuratowski("a", "a")), "{{a}}")
        with self.assertRaises(ValueError):
            S.un_kuratowski(frozenset({1, 2}))

    def test_ackermann_coding(self):
        for number in range(200):
            decoded = S.ackermann_decode(number)
            self.assertEqual(S.ackermann_code(decoded), number)
        self.assertEqual(S.ackermann_code(frozenset()), 0)
        self.assertEqual(S.ackermann_code(S.von_neumann(3)), 2 ** 0 + 2 ** 1
                         + 2 ** 3)

    def test_big_union(self):
        value = frozenset({frozenset({1, 2}), frozenset({2, 3})})
        self.assertEqual(S.big_union(value), frozenset({1, 2, 3}))
        self.assertEqual(S.big_union(S.von_neumann(4)), S.von_neumann(3))
        with self.assertRaises(TypeError):
            S.big_union(frozenset({1}))


class RelationTest(unittest.TestCase):
    def test_closures_match_brute_force(self):
        rng = random.Random(17)
        for _ in range(400):
            elements = list(range(1, rng.randint(3, 6)))
            relation = random_relation(rng, elements)
            self.assertEqual(S.reflexive_closure(relation, elements),
                             O.brute_reflexive_closure(relation, elements))
            self.assertEqual(S.symmetric_closure(relation),
                             O.brute_symmetric_closure(relation))
            self.assertEqual(S.transitive_closure(relation),
                             O.brute_transitive_closure(relation))
            self.assertEqual(S.equivalence_closure(relation, elements),
                             O.brute_equivalence_closure(relation, elements))

    def test_warshall_snapshots(self):
        rng = random.Random(19)
        for _ in range(200):
            elements = list(range(1, rng.randint(3, 6)))
            relation = random_relation(rng, elements)
            closure, snapshots = S.warshall(relation, elements)
            self.assertEqual(closure, O.brute_transitive_closure(relation))
            self.assertEqual([pivot for pivot, _ in snapshots], elements)
            previous = S.relation_matrix(relation, elements)
            for _, matrix in snapshots:
                for row_before, row_after in zip(previous, matrix):
                    for before, after in zip(row_before, row_after):
                        self.assertLessEqual(before, after)
                previous = matrix
            self.assertEqual(S.matrix_pairs(snapshots[-1][1], elements),
                             closure)

    def test_properties_and_witnesses(self):
        rng = random.Random(23)
        for _ in range(400):
            elements = list(range(1, rng.randint(3, 5)))
            relation = random_relation(rng, elements, density=0.5)
            properties = S.relation_properties(relation, elements)
            self.assertEqual(properties, O.brute_properties(relation,
                                                            elements))
            for name, holds in properties.items():
                witness = S.property_witness(relation, elements, name)
                if holds:
                    self.assertIsNone(witness)
                else:
                    self.assertIsNotNone(witness)
                    if name == "reflexive":
                        self.assertNotIn((witness, witness), relation)
                    elif name == "symmetric":
                        self.assertIn(witness, relation)
                        self.assertNotIn((witness[1], witness[0]), relation)
                    elif name == "antisymmetric":
                        self.assertIn(witness, relation)
                        self.assertIn((witness[1], witness[0]), relation)
                        self.assertNotEqual(witness[0], witness[1])
                    else:
                        self.assertNotIn(witness, relation)

    def test_composition_and_inverse(self):
        rng = random.Random(29)
        for _ in range(400):
            left = [1, 2, 3]
            middle = ["a", "b"]
            right = ["x", "y", "z"]
            first = frozenset((a, b) for a in left for b in middle
                              if rng.random() < 0.5)
            second = frozenset((b, c) for b in middle for c in right
                               if rng.random() < 0.5)
            expected = frozenset(
                (a, c) for a in left for c in right
                if any((a, b) in first and (b, c) in second for b in middle))
            self.assertEqual(S.compose(first, second), expected)
            self.assertEqual(S.inverse_relation(first),
                             frozenset((b, a) for (a, b) in first))
            self.assertEqual(S.domain_of(first),
                             frozenset(a for (a, _) in first))
            self.assertEqual(S.range_of(first),
                             frozenset(b for (_, b) in first))

    def test_equivalence_classes_match_brute_force(self):
        rng = random.Random(31)
        for _ in range(400):
            elements = list(range(1, rng.randint(3, 8)))
            relation = random_relation(rng, elements, density=0.25)
            classes = S.equivalence_classes(relation, elements)
            self.assertEqual(classes,
                             O.brute_equivalence_classes(relation, elements))
            self.assertEqual(sorted(itertools.chain(*classes)),
                             sorted(elements))
            text = S.partition_text(classes)
            self.assertEqual([frozenset(block) for block in classes],
                             O.parse_partition(text))

    def test_congruence_classes_example(self):
        elements = list(range(12))
        relation = {(a, b) for a in elements for b in elements
                    if a % 4 == b % 4}
        classes = S.equivalence_classes(relation, elements)
        self.assertEqual(S.partition_text(classes),
                         "{{0, 4, 8}, {1, 5, 9}, {2, 6, 10}, {3, 7, 11}}")


class PosetTest(unittest.TestCase):
    def test_divisor_poset(self):
        divisors, order = S.divisor_poset(12)
        self.assertEqual(divisors, [1, 2, 3, 4, 6, 12])
        self.assertTrue(S.is_partial_order(order, divisors))
        self.assertEqual(S.pair_roster(S.cover_relation(order, divisors)),
                         "{(1, 2), (1, 3), (2, 4), (2, 6), (3, 6), (4, 12), "
                         "(6, 12)}")
        self.assertEqual(S.minimal_elements(order, divisors), [1])
        self.assertEqual(S.maximal_elements(order, divisors), [12])
        self.assertEqual(S.least_element(order, divisors), 1)
        self.assertEqual(S.greatest_element(order, divisors), 12)
        self.assertEqual(S.lub(order, divisors, [4, 6]), 12)
        self.assertEqual(S.glb(order, divisors, [4, 6]), 2)
        self.assertEqual(S.sequence_text(S.linear_extension(order, divisors)),
                         "1, 2, 3, 4, 6, 12")
        self.assertTrue(S.is_lattice(order, divisors))

    def test_subset_poset(self):
        subsets, order = S.subset_poset(["a", "b"])
        self.assertTrue(S.is_partial_order(order, subsets))
        self.assertEqual(S.roster(S.minimal_elements(order, subsets)), "{∅}")
        self.assertEqual(S.lub(order, subsets, [frozenset({"a"}),
                                                frozenset({"b"})]),
                         frozenset({"a", "b"}))
        self.assertTrue(S.is_lattice(order, subsets))

    def test_random_posets_against_brute_force(self):
        rng = random.Random(37)
        for _ in range(300):
            elements = list(range(1, rng.randint(4, 7)))
            order = random_poset(rng, elements)
            self.assertTrue(S.is_partial_order(order, elements))
            self.assertEqual(S.cover_relation(order, elements),
                             O.brute_cover(order, elements))
            self.assertEqual(S.linear_extension(order, elements),
                             O.brute_linear_extension(order, elements))
            self.assertEqual(S.minimal_elements(order, elements),
                             O.brute_minimal(order, elements))
            self.assertEqual(S.maximal_elements(order, elements),
                             O.brute_maximal(order, elements))
            self.assertEqual(S.least_element(order, elements),
                             O.brute_least(order, elements))
            self.assertEqual(S.greatest_element(order, elements),
                             O.brute_greatest(order, elements))
            for pair in itertools.combinations(elements, 2):
                subset = list(pair)
                self.assertEqual(S.upper_bounds(order, elements, subset),
                                 O.brute_upper_bounds(order, elements, subset))
                self.assertEqual(S.lower_bounds(order, elements, subset),
                                 O.brute_lower_bounds(order, elements, subset))
                self.assertEqual(S.lub(order, elements, subset),
                                 O.brute_lub(order, elements, subset))
                self.assertEqual(S.glb(order, elements, subset),
                                 O.brute_glb(order, elements, subset))

    def test_linear_extension_tie_break(self):
        elements = [1, 2, 3, 4]
        order = O.brute_reflexive_closure({(1, 3), (2, 4)}, elements)
        self.assertEqual(S.linear_extension(order, elements), [1, 2, 3, 4])
        order = O.brute_reflexive_closure({(3, 1), (4, 2)}, elements)
        self.assertEqual(S.linear_extension(order, elements), [3, 1, 4, 2])

    def test_linear_extension_rejects_cycles(self):
        with self.assertRaises(ValueError):
            S.linear_extension({(1, 2), (2, 1)}, [1, 2])


class FunctionTableTest(unittest.TestCase):
    def test_witnesses_match_brute_force(self):
        rng = random.Random(41)
        for _ in range(400):
            domain = list(range(1, rng.randint(3, 6)))
            codomain = list(range(1, rng.randint(3, 6)))
            table = {a: rng.choice(codomain) for a in domain}
            collision, missed = O.brute_function_properties(table, codomain)
            self.assertEqual(S.injective_witness(table), collision)
            self.assertEqual(S.surjective_witness(table, codomain), missed)
            self.assertEqual(S.image(table, domain),
                             frozenset(table.values()))
            self.assertEqual(S.preimage(table, codomain), frozenset(domain))

    def test_answer_shape(self):
        table = {1: 2, 2: 3, 4: 3}
        collision = S.injective_witness(table)
        self.assertEqual(collision, (2, 4, 3))
        self.assertEqual(
            "injective no (f(%d) = f(%d) = %d); surjective yes; bijective no"
            % collision,
            "injective no (f(2) = f(4) = 3); surjective yes; bijective no")


class PipeSafetyTest(unittest.TestCase):
    def test_no_ascii_bar_in_rendered_output(self):
        rng = random.Random(43)
        for _ in range(300):
            items = random_elements(rng, rng.randint(0, 5))
            for text in (S.roster(items), S.sequence_text(items),
                         S.partition_text([items]) if items else "∅"):
                self.assertNotIn("|", text)
        self.assertNotIn("|", S.set_builder(S.range_condition(-2, 3)))
        self.assertEqual(S.DIVIDES, "∣")
        self.assertNotEqual(S.DIVIDES, "|")


if __name__ == "__main__":
    unittest.main()
