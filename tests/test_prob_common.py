"""Unit tests for ``prob_common`` — the probability strand's Phase 0 module.

Covers the canonical renderings (A0 / DESIGN.md "Probability answers"), the
experiment objects and their §3 enumeration order, the named event
predicates, weighted spaces, two-way tables, and the ``phi_table`` excerpt
that ``NormalTableGenerator`` now delegates to. Every prose renderer is
round-tripped through the independent parser in ``tests/probability_oracle``.
"""
import math
import os
import random
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import prob_common as pc  # noqa: E402
from generators.conditional_probability_generator import (  # noqa: E402
    ConditionalProbabilityGenerator,
)
from generators.normal_table_generator import NormalTableGenerator  # noqa: E402
from tests import probability_oracle as oracle  # noqa: E402


def reference_table(zs):
    """The pre-refactor ``NormalTableGenerator._table`` body, kept here so the
    shared ``phi_table`` can be proved byte-identical to it."""
    def local_phi(z):
        return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)

    need = sorted({abs(z) for z in zs})
    decoys = [round(z, 1) for z in (need[0] + 0.2, need[-1] + 0.3)]
    rows = sorted(set(need + [d for d in decoys if 0 < d <= 3.4]))
    cells = "; ".join(f"z={z:.2f}: {local_phi(z):.4f}" for z in rows)
    return f"Standard normal table, Φ(z) = P(Z < z): {cells}"


def experiments():
    """One instance of every experiment class, with its expected labels."""
    return [
        (pc.Coin(), ["H", "T"]),
        (pc.Die(6), ["1", "2", "3", "4", "5", "6"]),
        (pc.Die(8), [str(v) for v in range(1, 9)]),
        (pc.Spinner([1, 2, 3]), ["1", "2", "3"]),
        (pc.Spinner(["red", "blue", "green"]), ["red", "blue", "green"]),
        (pc.Bag([("red", 3), ("blue", 4), ("green", 1)]), ["R", "B", "G"]),
        (pc.NumberedCards(12), [str(v) for v in range(1, 13)]),
        (pc.LetterTiles("PROBABILITY"),
         ["P", "R", "O", "B", "A", "I", "L", "T", "Y"]),
        (pc.Menu([("sandwich", ["ham", "tuna"]), ("drink", ["milk", "juice"])]),
         ["ham + milk", "ham + juice", "tuna + milk", "tuna + juice"]),
    ]


class RenderingTest(unittest.TestCase):
    """A0 renderings and their edge cases."""

    def test_dec(self):
        self.assertEqual(pc.dec(Fraction(33, 10)), "3.3")
        self.assertEqual(pc.dec(Fraction(1331, 1000)), "1.331")
        self.assertEqual(pc.dec(Fraction(0)), "0")
        self.assertEqual(pc.dec(Fraction(5)), "5")
        self.assertEqual(pc.dec(Fraction(-1, 8)), "-0.125")
        self.assertEqual(pc.dec(Fraction(20, 4)), "5")
        with self.assertRaises(ValueError):
            pc.dec(Fraction(1, 3))

    def test_terminates_and_exact(self):
        self.assertTrue(pc.terminates(Fraction(3, 8)))
        self.assertFalse(pc.terminates(Fraction(1, 6)))
        self.assertEqual(pc.exact(Fraction(1, 4)), "0.25")
        self.assertEqual(pc.exact(Fraction(1, 3)), "1/3")
        self.assertEqual(pc.exact(Fraction(-7, 2)), "-3.5")
        self.assertEqual(pc.exact(Fraction(6, 3)), "2")

    def test_prob_txt(self):
        self.assertEqual(pc.prob_txt(Fraction(2, 6)), "1/3")
        self.assertEqual(pc.prob_txt(Fraction(4, 2)), "2")
        self.assertEqual(pc.prob_txt(Fraction(0)), "0")
        self.assertEqual(pc.prob_txt(Fraction(1)), "1")
        self.assertEqual(pc.prob_txt(Fraction(-1, 8)), "-1/8")

    def test_p4(self):
        self.assertEqual(pc.p4(Fraction(1353, 10000)), "0.1353")
        self.assertEqual(pc.p4(0.5), "0.5000")
        self.assertEqual(pc.p4(1), "1.0000")

    def test_pct(self):
        self.assertEqual(pc.pct(Fraction(3, 8)), "37.5%")
        self.assertEqual(pc.pct(Fraction(1)), "100%")
        self.assertEqual(pc.pct(Fraction(0)), "0%")
        self.assertEqual(pc.pct(Fraction(1, 200)), "0.5%")
        with self.assertRaises(ValueError):
            pc.pct(Fraction(1, 3))

    def test_money(self):
        self.assertEqual(pc.money(Fraction(2006, 100)), "$20.06")
        self.assertEqual(pc.money(Fraction(7, 2)), "$3.50")
        self.assertEqual(pc.money(Fraction(0)), "$0.00")
        self.assertEqual(pc.money(Fraction(-1, 4)), "-$0.25")
        self.assertEqual(pc.money(5), "$5.00")
        with self.assertRaises(ValueError):
            pc.money(Fraction(1, 3))

    def test_odds_txt(self):
        self.assertEqual(pc.odds_txt(Fraction(3, 8)), "3:5")
        self.assertEqual(pc.odds_txt(Fraction(2, 9)), "2:7")
        self.assertEqual(pc.odds_txt(Fraction(1, 2)), "1:1")
        self.assertEqual(pc.odds_txt(Fraction(4, 10)), "2:3")
        self.assertEqual(pc.odds_txt(Fraction(0)), "0:1")
        self.assertEqual(pc.odds_txt(Fraction(1)), "1:0")

    def test_roster_and_given(self):
        self.assertEqual(pc.roster([1, 2, 3]), "{1, 2, 3}")
        self.assertEqual(pc.roster([]), "∅")
        self.assertEqual(pc.given("A", "B"), "P(A given B)")
        self.assertNotIn("|", pc.given("A", "B"))

    def test_supplied_constant(self):
        self.assertEqual(pc.supplied_constant("e^-2", math.exp(-2)),
                         "e^-2 = 0.1353")

    def test_banks_and_roots(self):
        for n, p in pc.NP_BANK:
            sigma = pc.binomial_sigma(n, p)
            self.assertEqual(Fraction(sigma) ** 2, Fraction(n) * p * (1 - p))
        self.assertTrue(pc.is_perfect_square(Fraction(9, 4)))
        self.assertFalse(pc.is_perfect_square(Fraction(2)))
        self.assertEqual(pc.sqrt_fraction(Fraction(9, 4)), Fraction(3, 2))
        with self.assertRaises(ValueError):
            pc.sqrt_fraction(Fraction(2))


class ExperimentTest(unittest.TestCase):
    """Enumeration order, rosters, and renderer / oracle round trips."""

    def test_enumeration_order(self):
        for experiment, expected in experiments():
            with self.subTest(experiment=type(experiment).__name__):
                self.assertEqual(experiment.labels(), expected)

    def test_roster_printing(self):
        self.assertEqual(pc.Coin().roster_text(), "{H, T}")
        self.assertEqual(pc.Die(6).roster_text(), "{1, 2, 3, 4, 5, 6}")
        self.assertEqual(pc.Bag([("red", 3), ("blue", 1)]).roster_text(),
                         "{R, B}")
        self.assertEqual(pc.LetterTiles("BOB").roster_text(), "{B, O}")

    def test_bag_items_and_weights(self):
        bag = pc.Bag([("red", 3), ("blue", 4), ("green", 1)])
        self.assertEqual([o.label for o in bag.items()],
                         ["R1", "R2", "R3", "B1", "B2", "B3", "B4", "G1"])
        self.assertEqual(bag.total, 8)
        self.assertEqual(bag.probability(pc.colour("red")), Fraction(3, 8))
        self.assertEqual(bag.weighted().weight("B"), Fraction(1, 2))
        self.assertEqual(bag.weighted().total(), 1)

    def test_bag_uses_full_names_when_initials_collide(self):
        bag = pc.Bag([("red", 2), ("rose", 3)])
        self.assertEqual(bag.labels(), ["red", "rose"])

    def test_letter_tiles_items_and_weights(self):
        tiles = pc.LetterTiles("PROBABILITY")
        self.assertEqual([o.label for o in tiles.items()],
                         ["P", "R", "O", "B1", "A", "B2", "I1", "L", "I2",
                          "T", "Y"])
        self.assertEqual(tiles.probability(pc.vowel), Fraction(4, 11))
        self.assertEqual(tiles.weighted().weight("B"), Fraction(2, 11))

    def test_menu_stage_counts(self):
        menu = pc.Menu([("sandwich", ["ham", "tuna", "cheese"]),
                        ("drink", ["milk", "juice"]),
                        ("fruit", ["apple", "pear", "grapes", "plum"])])
        self.assertEqual(menu.stage_counts(),
                         [("sandwich", 3), ("drink", 2), ("fruit", 4)])
        self.assertEqual(menu.size(), 24)
        milk_and_apple = pc.at_least_one("milk") & pc.at_least_one("apple")
        self.assertEqual(menu.probability(milk_and_apple), Fraction(1, 8))

    def test_prose_round_trips_through_the_oracle(self):
        for experiment, expected in experiments():
            for style in experiment.PHRASINGS:
                with self.subTest(experiment=type(experiment).__name__,
                                  style=style):
                    text = experiment.prose(style)
                    self.assertTrue(text[0].isupper() and text.endswith("."))
                    self.assertNotIn("|", text)
                    self.assertEqual(oracle.outcomes_from_text(text), expected)
                    self.assertEqual(
                        oracle.items_from_text(text),
                        [o.label for o in experiment.items()])

    def test_clauses_never_contain_and(self):
        """``Product`` joins clauses with ' and '; components must not."""
        for experiment, _ in experiments():
            for style in experiment.PHRASINGS:
                self.assertNotIn(" and ", experiment.clause(style))

    def test_invalid_style_raises(self):
        with self.assertRaises(ValueError):
            pc.Coin().prose("bogus")
        with self.assertRaises(ValueError):
            pc.Product([pc.Coin(), pc.Die(6)]).prose("bogus")

    def test_prose_is_deterministic_given_random(self):
        random.seed(11)
        first = [pc.Die(6).prose() for _ in range(20)]
        random.seed(11)
        self.assertEqual(first, [pc.Die(6).prose() for _ in range(20)])
        self.assertGreater(len(set(first)), 1)

    def test_constructor_guards(self):
        for bad in (lambda: pc.Die(1), lambda: pc.Spinner([1]),
                    lambda: pc.Spinner([1, 1]), lambda: pc.Bag([]),
                    lambda: pc.Bag([("red", 0)]),
                    lambda: pc.Bag([("red", 1), ("red", 2)]),
                    lambda: pc.NumberedCards(1), lambda: pc.LetterTiles("A1"),
                    lambda: pc.Menu([("drink", ["milk"])]),
                    lambda: pc.Product([pc.Coin()])):
            with self.assertRaises(ValueError):
                bad()


class ProductSpaceTest(unittest.TestCase):
    """Compound experiments and their §3 labels."""

    def test_labels(self):
        coin_spinner = pc.Product([pc.Coin(), pc.Spinner([1, 2, 3])])
        self.assertEqual(coin_spinner.labels(),
                         ["H1", "H2", "H3", "T1", "T2", "T3"])
        self.assertEqual(pc.Product([pc.Coin(), pc.Coin()]).labels(),
                         ["HH", "HT", "TH", "TT"])
        self.assertEqual(pc.Product([pc.Die(3), pc.Die(2)]).labels(),
                         ["(1, 1)", "(1, 2)", "(2, 1)", "(2, 2)",
                          "(3, 1)", "(3, 2)"])
        bag = pc.Bag([("red", 1), ("blue", 1)])
        self.assertEqual(pc.Product([bag, bag]).labels(),
                         ["RR", "RB", "BR", "BB"])

    def test_product_label_modes(self):
        self.assertEqual(pc.product_label(["H", "1"]), "H1")
        self.assertEqual(pc.product_label(["3", "4"]), "(3, 4)")
        self.assertEqual(pc.product_label(["3", "4"], "concat"), "34")
        self.assertEqual(pc.product_label(["ham", "milk"], "plus"),
                         "ham + milk")
        with self.assertRaises(ValueError):
            pc.product_label(["a", "b"], "bogus")

    def test_repeated_trials_read_naturally(self):
        self.assertEqual(pc.Product([pc.Coin(), pc.Coin()]).prose("flip"),
                         "A fair coin is flipped twice.")
        self.assertEqual(
            pc.Product([pc.Die(6)] * 3).prose("roll"),
            "A fair 6-sided die is rolled three times.")

    def test_mixed_products_join_with_and(self):
        text = pc.Product([pc.Coin(), pc.Spinner([1, 2, 3])]).prose("flip")
        self.assertIn(" and ", text)
        self.assertTrue(text.startswith("A fair coin is flipped and "))

    def test_product_round_trips(self):
        products = [
            pc.Product([pc.Coin(), pc.Spinner([1, 2, 3])]),
            pc.Product([pc.Coin(), pc.Coin()]),
            pc.Product([pc.Die(6), pc.Die(6)]),
            pc.Product([pc.Coin(), pc.Die(4)]),
            pc.Product([pc.Bag([("red", 2), ("blue", 3)]), pc.Coin()]),
        ]
        random.seed(5)
        for product in products:
            for _ in range(4):
                text = product.prose()
                with self.subTest(text=text):
                    self.assertEqual(oracle.outcomes_from_text(text),
                                     product.labels())
                    self.assertEqual(oracle.items_from_text(text),
                                     [o.label for o in product.items()])

    def test_brute_force_agrees_on_two_dice(self):
        two_dice = pc.Product([pc.Die(6), pc.Die(6)])
        text = two_dice.prose("roll")
        points = oracle.item_space(oracle.parse_experiment(text))
        def total_is(k):
            return lambda p: sum(int(v) for v in p.parts) == k

        for k in range(2, 13):
            self.assertEqual(two_dice.probability(pc.sum_equals(k)),
                             oracle.probability(points, total_is(k)))
        self.assertEqual(
            two_dice.probability(pc.doubles),
            oracle.probability(points, lambda p: len(set(p.parts)) == 1))


class PredicateTest(unittest.TestCase):
    """Named events: printable names and brute-force agreement."""

    def test_names(self):
        self.assertEqual(pc.even.name, "even")
        self.assertEqual(pc.odd.name, "odd")
        self.assertEqual(pc.vowel.name, "a vowel")
        self.assertEqual(pc.doubles.name, "doubles")
        self.assertEqual(pc.multiple_of(3).name, "a multiple of 3")
        self.assertEqual(pc.greater_than(4).name, "greater than 4")
        self.assertEqual(pc.at_most(4).name, "at most 4")
        self.assertEqual(pc.at_least(2).name, "at least 2")
        self.assertEqual(pc.less_than(2).name, "less than 2")
        self.assertEqual(pc.colour("red").name, "red")
        self.assertEqual(pc.sum_equals(7).name, "a sum of 7")
        self.assertEqual(pc.at_least_one("H").name, "at least one H")
        self.assertEqual(pc.component(0, pc.even).name, "the first is even")
        self.assertEqual((pc.even & pc.greater_than(3)).name,
                         "even and greater than 3")
        self.assertEqual((~pc.even).name, "not even")
        self.assertEqual((pc.even | pc.odd).name, "even or odd")

    def test_on_a_die(self):
        die = pc.Die(6)
        self.assertEqual(die.probability(pc.even), Fraction(1, 2))
        self.assertEqual(die.probability(pc.odd), Fraction(1, 2))
        self.assertEqual(die.probability(pc.multiple_of(3)), Fraction(1, 3))
        self.assertEqual(die.probability(pc.greater_than(4)), Fraction(1, 3))
        self.assertEqual(die.probability(pc.at_most(4)), Fraction(2, 3))
        self.assertEqual(die.event_roster(pc.even), "{2, 4, 6}")
        self.assertEqual(die.event_roster(pc.greater_than(6)), "∅")

    def test_at_least_one_and_component(self):
        two_coins = pc.Product([pc.Coin(), pc.Coin()])
        self.assertEqual(two_coins.probability(pc.at_least_one("H")),
                         Fraction(3, 4))
        first_head = pc.component(0, pc.at_least_one("H"))
        self.assertEqual(two_coins.probability(first_head), Fraction(1, 2))

    def test_compound_number_needs_a_component(self):
        with self.assertRaises(ValueError):
            pc.even(pc.Outcome("(3, 4)", ("3", "4")))
        self.assertTrue(pc.component(1, pc.even)(pc.Outcome("(3, 4)",
                                                            ("3", "4"))))

    def test_outcome_equality_and_numbers(self):
        outcome = pc.as_outcome("(3, 4)")
        self.assertEqual(outcome.parts, ("3", "4"))
        self.assertEqual(outcome.numbers(), [3, 4])
        self.assertEqual(outcome, "(3, 4)")
        self.assertEqual({pc.Outcome("H")}, {"H"})


class WeightedSpaceTest(unittest.TestCase):
    """P as a measure on atoms, and conditioning as renormalization."""

    def space(self):
        return pc.WeightedSpace([("a", Fraction(1, 10)), ("b", Fraction(1, 5)),
                                 ("c", Fraction(3, 10)), ("d", Fraction(1, 4)),
                                 ("e", Fraction(3, 20))])

    def test_measure_and_validity(self):
        space = self.space()
        self.assertEqual(space.total(), 1)
        self.assertTrue(space.is_valid())
        self.assertEqual(space.validity_report(), "valid; sum = 1")
        self.assertEqual(space.measure(["a", "c"]), Fraction(2, 5))
        self.assertEqual(space.measure("c"), Fraction(3, 10))
        self.assertEqual(space.measure(lambda o: o.label in "bd"),
                         Fraction(9, 20))
        self.assertEqual(space.event_roster(["b", "d"]), "{b, d}")

    def test_weight_lines(self):
        space = pc.WeightedSpace([("1", Fraction(1, 4)), ("2", Fraction(3, 4))])
        self.assertEqual(space.weight_lines(), "P(1) = 1/4; P(2) = 3/4")

    def test_conditioning_renormalizes(self):
        conditioned = self.space().given(["b", "c", "e"])
        self.assertEqual(conditioned.weight_lines(),
                         "P(b) = 4/13; P(c) = 6/13; P(e) = 3/13")
        self.assertEqual(conditioned.total(), 1)

    def test_invalid_spaces(self):
        heavy = pc.WeightedSpace([("1", Fraction(1, 2)), ("2", Fraction(5, 8))])
        self.assertEqual(heavy.validity_report(), "invalid; sum = 9/8")
        negative = pc.WeightedSpace([("1", Fraction(9, 8)),
                                     ("3", Fraction(-1, 8))])
        self.assertEqual(negative.validity_report(), "invalid; P(3) = -1/8 < 0")
        with self.assertRaises(ValueError):
            heavy.validate()

    def test_uniform_and_from_counts(self):
        self.assertEqual(pc.WeightedSpace.uniform("HT").weight("H"),
                         Fraction(1, 2))
        counts = pc.WeightedSpace.from_counts([("red", 3), ("blue", 5)])
        self.assertEqual(counts.weight("red"), Fraction(3, 8))
        self.assertTrue(counts.is_valid())

    def test_guards(self):
        with self.assertRaises(ValueError):
            pc.WeightedSpace([("a", 1), ("a", 0)])
        with self.assertRaises(ValueError):
            pc.WeightedSpace([]).total()
        space = self.space()
        with self.assertRaises(ValueError):
            space.measure(["z"])
        with self.assertRaises(ValueError):
            space.given(lambda o: False)

    def test_oracle_parses_the_weight_lines(self):
        space = self.space()
        text = f"The outcomes have {space.weight_lines()}."
        parsed = oracle.parse_weights(text)
        self.assertEqual(parsed, {a: space.weight(a) for a in space.atoms})
        self.assertEqual(oracle.weighted_probability(
            parsed, lambda atom: atom in {"a", "c"}), Fraction(2, 5))


class TwoWayTableTest(unittest.TestCase):
    """The ``<row>=<v> and <col>=<w>: n`` prose form and its arithmetic."""

    def table(self):
        return pc.TwoWayTable(
            "sport", ["yes", "no"], "pet", ["yes", "no"],
            {("yes", "yes"): 12, ("yes", "no"): 18,
             ("no", "yes"): 8, ("no", "no"): 12})

    def test_cells_text(self):
        table = self.table()
        self.assertEqual(
            table.cells_text(),
            "sport=yes and pet=yes: 12; sport=yes and pet=no: 18; "
            "sport=no and pet=yes: 8; sport=no and pet=no: 12")
        self.assertEqual(
            table.cells_text("column"),
            "sport=yes and pet=yes: 12; sport=no and pet=yes: 8; "
            "sport=yes and pet=no: 18; sport=no and pet=no: 12")
        with self.assertRaises(ValueError):
            table.cells_text("diagonal")

    def test_probabilities(self):
        table = self.table()
        self.assertEqual(table.grand_total(), 50)
        self.assertEqual(table.row_total("yes"), 30)
        self.assertEqual(table.col_total("yes"), 20)
        self.assertEqual(table.joint("yes", "yes"), Fraction(6, 25))
        self.assertEqual(table.marginal_row("yes"), Fraction(3, 5))
        self.assertEqual(table.col_given_row("yes", "yes"), Fraction(2, 5))
        self.assertEqual(table.row_given_col("yes", "yes"), Fraction(3, 5))
        self.assertEqual(table.union("yes", "yes"), Fraction(19, 25))
        self.assertEqual(table.row_total_work("yes"), "12 + 18 = 30")
        self.assertEqual(table.given_text("pet=yes", "sport=yes"),
                         "P(pet=yes given sport=yes)")

    def test_sentence_and_oracle_round_trip(self):
        table = self.table()
        sentence = table.sentence()
        self.assertTrue(sentence.startswith(
            "A two-way table for students has counts: "))
        row_name, col_name, cells = oracle.parse_two_way(sentence)
        self.assertEqual((row_name, col_name), ("sport", "pet"))
        self.assertEqual(cells, table.cells)
        rows, cols, grand = oracle.two_way_totals(cells)
        self.assertEqual((rows["yes"], cols["yes"], grand), (30, 20, 50))

    def test_matches_the_existing_generator_format(self):
        """The renderer must reproduce ``ConditionalProbabilityGenerator``'s
        table prose verbatim (that generator and its oracle already parse
        this form)."""
        random.seed(19)
        generator = ConditionalProbabilityGenerator("table")
        for _ in range(50):
            example = generator.generate()
            row_name, col_name, cells = oracle.parse_two_way(example["problem"])
            row_values = list(dict.fromkeys(row for row, _ in cells))
            col_values = list(dict.fromkeys(col for _, col in cells))
            table = pc.TwoWayTable(row_name, row_values,
                                   col_name, col_values, cells)
            self.assertIn(table.cells_text("row"), example["problem"])

    def test_random_counts_and_guards(self):
        random.seed(4)
        table = pc.TwoWayTable.random_counts("club", ["yes", "no"],
                                             "commute", ["bike", "bus"])
        self.assertEqual(len(table.cells), 4)
        self.assertTrue(all(4 <= n <= 28 for n in table.cells.values()))
        with self.assertRaises(ValueError):
            pc.TwoWayTable("a", ["x", "y"], "b", ["u"], {("x", "u"): 1})

    def test_brute_force_agrees_on_a_labelled_universe(self):
        table = self.table()
        people = [(r, c) for r in table.row_values for c in table.col_values
                  for _ in range(table.count(r, c))]
        self.assertEqual(len(people), 50)
        joint = Fraction(sum(1 for p in people if p == ("yes", "yes")),
                         len(people))
        self.assertEqual(joint, table.joint("yes", "yes"))
        sport = [p for p in people if p[0] == "yes"]
        self.assertEqual(Fraction(sum(1 for p in sport if p[1] == "yes"),
                                  len(sport)),
                         table.col_given_row("yes", "yes"))


class PhiTableTest(unittest.TestCase):
    """``phi_table`` is the single home of the supplied Φ excerpt."""

    def test_phi_values(self):
        self.assertEqual(pc.phi(0), 0.5)
        self.assertEqual(pc.phi(1.5), 0.9332)
        self.assertEqual(pc.phi(1.0), 0.8413)

    def test_matches_the_reference_and_the_generator(self):
        random.seed(23)
        generator = NormalTableGenerator()
        for _ in range(300):
            zs = [round(random.randint(1, 34) / 10, 1)
                  for _ in range(random.randint(1, 3))]
            expected = reference_table(zs)
            self.assertEqual(pc.phi_table(zs), expected)
            self.assertEqual(generator._table(zs), expected)

    def test_decoy_rows(self):
        rendered = pc.phi_table([1.0])
        self.assertEqual(rendered.count("z="), 3)
        self.assertIn("z=1.00: 0.8413", rendered)
        self.assertEqual(pc.phi_table([1.0], decoys=0).count("z="), 1)
        # decoys past the end of the table are dropped, not clamped
        self.assertEqual(pc.phi_table([3.4]).count("z="), 1)

    def test_signed_inputs_fold(self):
        self.assertEqual(pc.phi_table([-1.2]), pc.phi_table([1.2]))

    def test_oracle_parses_the_table(self):
        parsed = oracle.parse_phi_table(pc.phi_table([1.5]))
        self.assertEqual(parsed["1.50"], Fraction("0.9332"))


class OracleSelfTest(unittest.TestCase):
    """The oracle must stay an independent route (A9)."""

    def test_oracle_never_imports_prob_common(self):
        path = os.path.join(repo_root, "tests", "probability_oracle.py")
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        self.assertNotIn("prob_common", source.replace(
            "**this module never imports ``prob_common``**", ""))

    def test_solve_linear(self):
        solution = oracle.solve_linear([[2, 1], [1, -1]], [5, 1])
        self.assertEqual(solution, [Fraction(2), Fraction(1)])
        with self.assertRaises(ValueError):
            oracle.solve_linear([[1, 1], [2, 2]], [1, 2])

    def test_number_parsing(self):
        self.assertEqual(oracle.number("3/8"), Fraction(3, 8))
        self.assertEqual(oracle.number("0.375"), Fraction(3, 8))
        self.assertEqual(oracle.number("37.5%"), Fraction(3, 8))
        self.assertEqual(oracle.parse_supplied("Use e^-2 = 0.1353 here."),
                         {"e^-2": Fraction(1353, 10000)})
        self.assertEqual(oracle.parse_pmf("P(S=0) = 1/8; P(S=1) = 3/8"),
                         {"S=0": Fraction(1, 8), "S=1": Fraction(3, 8)})
        self.assertEqual(oracle.parse_cdf("F(1) = 1/8; F(2) = 1/2"),
                         {"1": Fraction(1, 8), "2": Fraction(1, 2)})
        self.assertEqual(
            oracle.parse_transition_rows("rows P1 = (1/2, 1/4, 1/4), "
                                         "P2 = (0, 1/2, 1/2)"),
            {"1": [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)],
             "2": [Fraction(0), Fraction(1, 2), Fraction(1, 2)]})
        self.assertEqual(oracle.parse_roster("A = {2, 4, 6}"),
                         ["2", "4", "6"])
        self.assertEqual(oracle.parse_roster("A = ∅"), [])


if __name__ == "__main__":
    unittest.main()
