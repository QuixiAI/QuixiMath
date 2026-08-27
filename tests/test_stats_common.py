"""Tests for ``stats_common.py`` (statistics Phase 0).

Three things are checked here:

1. **Renderer ↔ parser round trips.** Every display rendering in
   ``plans/statistics_plan.md`` §3 is generated on hundreds of random inputs and
   parsed back by the *independent* grammar in ``tests/stats_oracle.py``. A
   round trip that loses information (a dropped empty row, an ambiguous
   column) fails here rather than in a generator six phases later.
2. **Pattern-library and standard-error-bank properties.** Zero sum, the
   requested perfect-square property, non-empty pools for n = 4..8, caching,
   and every banked SE recomputed from its definition with plain
   ``Fraction`` / ``math.isqrt`` arithmetic.
3. **Agreement with the code the helpers were adapted from** —
   ``five_summary`` against ``FiveNumberSummaryGenerator.summary`` on its
   own ``SIZES``, and ``running_sum_steps`` against the A-chain the existing
   statistics generators write by hand.
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

import stats_common as sc
from generators.five_number_summary_generator import SIZES as GEN_SIZES
from generators.five_number_summary_generator import summary as gen_summary
from tests import stats_oracle as oracle

ROUNDS = 200


def rng(seed):
    return random.Random(seed)


class TestDotAndLinePlots(unittest.TestCase):
    def test_dot_plot_round_trip(self):
        r = rng(1)
        for _ in range(ROUNDS):
            lo = r.randint(0, 25)
            hi = lo + r.randint(1, 12)
            counts = {v: r.randint(0, 5) for v in range(lo, hi + 1)}
            counts[lo] = r.randint(1, 5)
            counts[hi] = r.randint(1, 5)
            text = sc.render_dot_plot(counts)
            self.assertEqual(counts, oracle.parse_dot_plot(text))
            data = [v for v in sorted(counts) for _ in range(counts[v])]
            self.assertEqual(data, oracle.dot_plot_data(text))
            self.assertNotIn("|", text)

    def test_dot_plot_from_raw_data_keeps_empty_rows(self):
        text = sc.render_dot_plot([6, 6, 8, 8, 8, 8, 9, 10, 10])
        self.assertEqual(" 7 ∣", text.splitlines()[1])
        self.assertEqual({6: 2, 7: 0, 8: 4, 9: 1, 10: 2},
                         oracle.parse_dot_plot(text))

    def test_dot_plot_labels_are_right_aligned(self):
        text = sc.render_dot_plot([8, 12])
        widths = {len(ln.split(sc.BAR)[0]) for ln in text.splitlines()}
        self.assertEqual(1, len(widths))

    def test_line_plot_round_trip(self):
        r = rng(2)
        for _ in range(ROUNDS):
            unit = Fraction(1, r.choice([2, 4, 8]))
            rows = r.randint(3, 9)
            base = unit * r.randint(1, 6)
            counts = {base + i * unit: r.randint(0, 4) for i in range(rows)}
            keys = sorted(counts)
            counts[keys[0]] = r.randint(1, 4)
            counts[keys[-1]] = r.randint(1, 4)
            text = sc.render_line_plot(counts, unit)
            self.assertEqual(counts, oracle.parse_line_plot(text))
            self.assertNotIn("|", text)

    def test_line_plot_labels_are_mixed_numbers(self):
        text = sc.render_line_plot(
            [Fraction(1, 4), Fraction(1, 2), Fraction(5, 4)], Fraction(1, 4))
        labels = [ln.split(sc.BAR)[0].strip() for ln in text.splitlines()]
        self.assertEqual(["1/4", "1/2", "3/4", "1", "1 1/4"], labels)

    def test_line_plot_rejects_values_off_the_unit(self):
        with self.assertRaises(ValueError):
            sc.render_line_plot([Fraction(1, 3)], Fraction(1, 4))


class TestTally(unittest.TestCase):
    WORDS = ("Apple", "Blue", "Cherry", "Dog", "Elm", "Fish", "Green",
             "Melon", "Red", "Yellow")

    def test_tally_round_trip(self):
        r = rng(3)
        for _ in range(ROUNDS):
            cats = r.sample(self.WORDS, r.randint(2, 5))
            counts = {c: r.randint(1, 14) for c in cats}
            text = sc.render_tally(counts)
            self.assertEqual(counts, oracle.parse_tally(text))
            self.assertNotIn("|", text)

    def test_group_of_five_is_four_slashes_and_a_backslash(self):
        self.assertEqual("////\\", sc.tally_marks(5))
        self.assertEqual("////\\ //", sc.tally_marks(7))
        self.assertEqual("////\\ ////\\ /", sc.tally_marks(11))
        self.assertEqual("///", sc.tally_marks(3))

    def test_rows_are_alphabetical(self):
        text = sc.render_tally({"Red": 2, "Blue": 3, "Green": 1})
        self.assertEqual(["Blue", "Green", "Red"],
                         [ln.split(":")[0] for ln in text.splitlines()])


class TestStemAndLeaf(unittest.TestCase):
    def test_integer_round_trip(self):
        r = rng(4)
        for _ in range(ROUNDS):
            n = r.randint(5, 15)
            values = [r.randint(10, 99) for _ in range(n)]
            text = sc.render_stem_leaf(values)
            self.assertEqual(sorted(Fraction(v) for v in values),
                             oracle.parse_stem_leaf(text))
            self.assertNotIn("|", text)

    def test_decimal_round_trip(self):
        r = rng(5)
        for _ in range(ROUNDS):
            n = r.randint(5, 12)
            values = [Fraction(r.randint(0, 99), 10) for _ in range(n)]
            text = sc.render_stem_leaf(values, decimal=True)
            self.assertIn("means", text.splitlines()[-1])
            self.assertEqual(sorted(values), oracle.parse_stem_leaf(text))

    def test_empty_stems_are_kept(self):
        text = sc.render_stem_leaf([12, 15, 17, 20, 23, 23, 41])
        self.assertEqual([
            "Stem ∣ Leaves",
            "   1 ∣ 2 5 7",
            "   2 ∣ 0 3 3",
            "   3 ∣",
            "   4 ∣ 1",
            "Key: 1 ∣ 2 means 12",
        ], text.splitlines())

    def test_key_can_be_chosen(self):
        text = sc.render_stem_leaf([12, 15, 17, 20, 23, 23, 41], key=(2, 3))
        self.assertEqual("Key: 2 ∣ 3 means 23", text.splitlines()[-1])
        self.assertEqual(7, len(oracle.parse_stem_leaf(text)))

    def test_decimal_key_shows_a_decimal(self):
        text = sc.render_stem_leaf([Fraction(23, 10), Fraction(41, 10)],
                                   decimal=True, key=(2, 3))
        self.assertEqual("Key: 2 ∣ 3 means 2.3", text.splitlines()[-1])

    def test_text_list_form(self):
        self.assertEqual("1: 2 5 7; 2: 0 3 3; 3: none; 4: 1",
                         sc.stem_leaf_list([12, 15, 17, 20, 23, 23, 41]))


class TestBoxPlot(unittest.TestCase):
    def _summary(self, r, span=30):
        start = r.randint(0, 12)
        gaps = [r.randint(1, max(2, span // 6)) for _ in range(4)]
        vals = [start]
        for g in gaps:
            vals.append(vals[-1] + g)
        return tuple(vals)

    def test_round_trip(self):
        r = rng(6)
        for _ in range(ROUNDS):
            five = self._summary(r)
            text = sc.render_box_plot(five)
            self.assertEqual(tuple(Fraction(v) for v in five),
                             tuple(Fraction(v)
                                   for v in oracle.box_plot_summary(text)))
            self.assertNotIn("|", text)

    def test_round_trip_with_outliers(self):
        r = rng(7)
        for _ in range(ROUNDS):
            five = self._summary(r, span=18)
            out = [five[4] + r.randint(2, 6)]
            if r.random() < 0.4 and five[0] >= 3:
                out.append(five[0] - r.randint(1, 3))
            text = sc.render_box_plot(five, outliers=out)
            parsed = oracle.parse_box_plot(text)["Plot"]
            self.assertEqual(sorted(out), sorted(parsed["outliers"]))
            self.assertEqual(five[0], parsed["min"])
            self.assertEqual(five[4], parsed["max"])

    def test_plan_example_is_byte_exact(self):
        self.assertEqual([
            "Scale: 0    5    10   15   20",
            "       +----+----+----+----+",
            "Plot:     *-[==:===]--*",
        ], sc.render_box_plot((3, 5, 8, 12, 15)).splitlines())

    def test_two_plots_share_one_scale(self):
        text = sc.render_box_plots([("Plot A", (3, 5, 8, 12, 15)),
                                    ("Plot B", (6, 9, 14, 20, 24))])
        parsed = oracle.parse_box_plot(text)
        self.assertEqual((3, 5, Fraction(8), 12, 15),
                         (parsed["Plot A"]["min"], parsed["Plot A"]["q1"],
                          parsed["Plot A"]["median"], parsed["Plot A"]["q3"],
                          parsed["Plot A"]["max"]))
        self.assertEqual(24, parsed["Plot B"]["max"])
        self.assertEqual(1, len({len(ln) for ln in text.splitlines()[:1]}))

    def test_prefix_is_seven_characters(self):
        for label in ("Plot", "Plot A", "Scale"):
            self.assertEqual(7, len(f"{label}:".ljust(sc.BOX_PREFIX)))
        text = sc.render_box_plot((3, 5, 8, 12, 15))
        for line in text.splitlines():
            self.assertEqual(7, len(line) - len(line[7:]) + 0)

    def test_rejects_a_non_strict_summary(self):
        with self.assertRaises(ValueError):
            sc.render_box_plot((3, 5, 5, 12, 15))

    def test_rejects_an_outlier_inside_the_whiskers(self):
        with self.assertRaises(ValueError):
            sc.render_box_plot((3, 5, 8, 12, 15), outliers=[10])

    def test_rejects_a_scale_wider_than_forty(self):
        with self.assertRaises(ValueError):
            sc.render_box_plot((0, 10, 20, 30, 44))


class TestTwoWayTable(unittest.TestCase):
    ROWS = ("Grade 9", "Grade 10", "Grade 11", "Adults", "Team A")
    COLS = ("Yes", "No", "Maybe", "Walk", "Bus")

    def test_round_trip(self):
        r = rng(8)
        for _ in range(ROUNDS):
            nr, nc = r.randint(2, 3), r.randint(2, 3)
            rows = list(self.ROWS[:nr])
            cols = list(self.COLS[:nc])
            cells = [[r.randint(0, 99) for _ in range(nc)] for _ in range(nr)]
            totals = r.random() < 0.5
            text = sc.render_two_way(rows, cols, cells, totals=totals)
            got_rows, got_cols, got_cells = oracle.parse_two_way(text)
            self.assertEqual(rows + (["Total"] if totals else []), got_rows)
            self.assertEqual(cols + (["Total"] if totals else []), got_cols)
            body = {(rows[i], cols[j]): cells[i][j]
                    for i in range(nr) for j in range(nc)}
            self.assertEqual(body, oracle.two_way_counts(text))
            self.assertNotIn("|", text)

    def test_plan_example_is_byte_exact(self):
        text = sc.render_two_way(["Grade 9", "Grade 10"], ["Yes", "No"],
                                 [[12, 8], [15, 15]], totals=True)
        self.assertEqual([
            "           Yes   No   Total",
            "Grade 9     12    8      20",
            "Grade 10    15   15      30",
            "Total       27   23      50",
        ], text.splitlines())

    def test_totals_are_the_margins(self):
        text = sc.render_two_way(["A", "B"], ["X", "Y"], [[3, 4], [5, 6]],
                                 totals=True)
        _, _, cells = oracle.parse_two_way(text)
        self.assertEqual(["7", "11", "18"], [cells[0][2], cells[1][2],
                                             cells[2][2]])
        self.assertEqual(["8", "10", "18"], cells[2])

    def test_missing_cell_renders_and_parses(self):
        text = sc.render_two_way(["A", "B"], ["X", "Y"], [[3, None], [5, 6]])
        _, _, cells = oracle.parse_two_way(text)
        self.assertEqual("?", cells[0][1])

    def test_row_label_ending_in_a_digit_is_not_eaten(self):
        text = sc.render_two_way(["Grade 9"], ["Yes", "No"], [[12, 8]])
        rows, _, cells = oracle.parse_two_way(text)
        self.assertEqual(["Grade 9"], rows)
        self.assertEqual([["12", "8"]], cells)


class TestBins(unittest.TestCase):
    def test_round_trip(self):
        r = rng(9)
        for _ in range(ROUNDS):
            width = r.choice([5, 10, 20])
            start = width * r.randint(0, 3)
            values = [start + r.randint(0, width * 4 - 1) for _ in range(12)]
            bins = sc.bin_counts(values, width, start)
            text = sc.render_bins(bins)
            parsed = oracle.parse_bins(text)
            self.assertEqual([b for b, _ in bins],
                             [f"{lo}-{hi}" for (lo, hi), _ in parsed])
            self.assertEqual([c for _, c in bins], [c for _, c in parsed])
            self.assertEqual(len(values), sum(c for _, c in parsed))

    def test_text_list_form(self):
        self.assertEqual("0-9: 3; 10-19: 4; 20-29: 3",
                         sc.render_bins(sc.bin_counts(
                             [3, 12, 17, 25, 8, 14, 21, 29, 11, 6], 10, 0)))

    def test_prose_separator(self):
        self.assertEqual("0-9: 1, 10-19: 1",
                         sc.render_bins(sc.bin_counts([3, 12], 10, 0), sep=", "))

    def test_rejects_a_width_off_the_multiple_of_five(self):
        with self.assertRaises(ValueError):
            sc.bin_counts([1, 2, 3], 7, 0)


class TestSuppliedConstants(unittest.TestCase):
    def test_phi_table_round_trip(self):
        r = rng(10)
        for _ in range(ROUNDS):
            zs = sorted({round(r.randint(3, 250) / 100, 2)
                         for _ in range(r.randint(1, 3))})
            text = sc.phi_table(zs)
            rows = oracle.parse_phi_table(text)
            for z in zs:
                key = oracle.read_decimal(f"{z:.2f}")
                self.assertIn(key, rows)
                want = round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
                self.assertEqual(oracle.read_decimal(f"{want:.4f}"), rows[key])
            self.assertGreaterEqual(len(rows), len(zs) + 1)  # decoy rows

    def test_inverse_z_round_trip(self):
        r = rng(11)
        keys = list(sc.INVERSE_Z)
        for _ in range(ROUNDS):
            want = sorted(r.sample(keys, r.randint(1, 3)),
                          key=lambda k: float(k))
            decoys = r.randint(0, 2)
            text = sc.inverse_z_table(want, decoys=decoys)
            rows = oracle.parse_inverse_z(text)
            self.assertEqual(len(want) + min(decoys, len(keys) - len(want)),
                             len(rows))
            for p in want:
                key = oracle.read_decimal(str(p))
                self.assertIn(key, rows)
                self.assertEqual(oracle.read_decimal(sc.INVERSE_Z[p]), rows[key])

    def test_inverse_z_wording(self):
        self.assertEqual(
            "Selected z-scores: 80th percentile z = 0.84; 90th z = 1.28; "
            "95th z = 1.645; 97.5th z = 1.96; 99th z = 2.33",
            sc.inverse_z_table([80, 90, 95, 97.5, 99], decoys=0))

    def test_inverse_z_accepts_a_custom_table(self):
        text = sc.inverse_z_table([94.5], decoys=1,
                                  table=sc.INVERSE_Z_DIVIDABLE)
        rows = oracle.parse_inverse_z(text)
        self.assertIn(oracle.read_decimal("94.5"), rows)
        self.assertEqual(2, len(rows))

    def test_inline_critical_values(self):
        text = " ".join([
            sc.critical_value("z*", "1.96"),
            sc.critical_value("t*", "2.262", 9),
            sc.critical_value("χ² critical value", "5.991", 2),
            sc.critical_value("F critical value", "4.26", (2, 9)),
        ])
        found = oracle.parse_inline_constants(text)
        self.assertEqual(
            [("F", Fraction(213, 50), (2, 9)),
             ("chi2", Fraction(5991, 1000), 2),
             ("t", Fraction(1131, 500), 9),
             ("z", Fraction(49, 25), None)],
            found)

    def test_ordinals(self):
        self.assertEqual(["1st", "2nd", "3rd", "11th", "21st", "80th",
                          "97.5th"],
                         [sc.ordinal(k) for k in (1, 2, 3, 11, 21, 80,
                                                  Fraction(195, 2))])


class TestPatternLibrary(unittest.TestCase):
    def test_zero_sum_and_bounded(self):
        for n in range(3, 9):
            pool = sc.patterns(n)
            self.assertTrue(pool)
            for pat in pool:
                self.assertEqual(n, len(pat))
                self.assertEqual(0, sum(pat))
                self.assertTrue(all(abs(d) <= 8 for d in pat))
                self.assertTrue(any(pat), "the all-zero pattern is excluded")
                self.assertEqual(list(pat), sorted(pat), "canonical order")
            self.assertEqual(len(pool), len(set(pool)), "no duplicates")

    def test_pools_are_non_empty_for_n_four_to_eight(self):
        for n in range(4, 9):
            self.assertTrue(sc.patterns(n, pop_square=True),
                            f"no population-square patterns for n = {n}")
            self.assertTrue(sc.patterns(n, sample_square=True),
                            f"no sample-square patterns for n = {n}")

    def test_population_square_property(self):
        for n in range(4, 9):
            for pat in sc.patterns(n, pop_square=True):
                var = Fraction(sc.pattern_ss(pat), n)
                root = Fraction(math.isqrt(var.numerator),
                                math.isqrt(var.denominator))
                self.assertEqual(var, root * root)

    def test_sample_square_property(self):
        for n in range(4, 9):
            for pat in sc.patterns(n, sample_square=True):
                var = Fraction(sc.pattern_ss(pat), n - 1)
                root = Fraction(math.isqrt(var.numerator),
                                math.isqrt(var.denominator))
                self.assertEqual(var, root * root)

    def test_plan_examples_are_in_the_pools(self):
        self.assertIn((-3, 1, 1, 1), sc.patterns(4, sample_square=True))
        self.assertIn((-3, -3, 1, 1, 4), sc.patterns(5, sample_square=True))
        self.assertIn((-6, -2, 2, 2, 4), sc.patterns(5, sample_square=True))
        self.assertIn((-3, -3, -3, 0, 3, 3, 3),
                      sc.patterns(7, sample_square=True))

    def test_sxx_patterns_for_slope_inference(self):
        self.assertIn((-2, -2, 2, 2), sc.patterns(4, ss=16))
        self.assertIn((-3, -3, 0, 3, 3), sc.patterns(5, ss=36))
        self.assertIn((-4, -1, -1, 1, 1, 4), sc.patterns(6, ss=36))
        self.assertIn((-8, -2, -2, 2, 2, 8), sc.patterns(6, ss=144, max_abs=8))
        for pat in sc.patterns(6, ss=36):
            self.assertEqual(36, sc.pattern_ss(pat))

    def test_pools_are_cached(self):
        first = sc.patterns(6, sample_square=True)
        self.assertIs(first, sc.patterns(6, sample_square=True))
        self.assertIsNot(first, sc.patterns(6, pop_square=True))

    def test_max_abs_is_respected(self):
        for pat in sc.patterns(5, max_abs=3):
            self.assertTrue(all(abs(d) <= 3 for d in pat))
        self.assertLess(len(sc.patterns(5, max_abs=3)), len(sc.patterns(5)))

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            sc.patterns(2)
        with self.assertRaises(ValueError):
            sc.patterns(9)
        with self.assertRaises(ValueError):
            sc.patterns(5, max_abs=0)

    def test_sample_from_pattern_has_the_exact_mean(self):
        r = rng(12)
        for _ in range(ROUNDS):
            n = r.randint(4, 8)
            pool = sc.patterns(n, sample_square=True)
            pat = pool[r.randrange(len(pool))]
            mean = r.randint(10, 60)
            data = sc.sample_from_pattern(mean, pat)
            self.assertEqual(n, len(data))
            self.assertEqual(Fraction(mean), oracle.mean(data))
            self.assertEqual(sorted(pat), sorted(v - mean for v in data))
            var = oracle.variance(data, sample=True)
            self.assertTrue(oracle.is_square(var),
                            f"sample variance {var} is not a square")

    def test_population_patterns_give_an_exact_population_sd(self):
        r = rng(13)
        for _ in range(50):
            n = r.randint(4, 8)
            pool = sc.patterns(n, pop_square=True)
            pat = pool[r.randrange(len(pool))]
            data = sc.sample_from_pattern(20, pat)
            self.assertTrue(oracle.is_square(oracle.variance(data)))

    def test_sample_from_pattern_can_keep_the_order(self):
        data = sc.sample_from_pattern(10, (-3, 1, 1, 1), shuffle=False)
        self.assertEqual([7, 11, 11, 11], data)

    def test_sample_from_pattern_accepts_a_fractional_mean(self):
        data = sc.sample_from_pattern(Fraction(25, 2), (-3, 1, 1, 1),
                                      shuffle=False)
        self.assertEqual(Fraction(25, 2), oracle.mean(data))
        self.assertEqual("9.5", sc.num_txt(data[0]))


class TestStandardErrorBanks(unittest.TestCase):
    def test_verify_se_tables(self):
        self.assertTrue(sc.verify_se_tables())

    def test_proportion_se_bank(self):
        for p, n, se in sc.PROP_SE_BANK:
            value = Fraction(p) * (1 - Fraction(p)) / n
            self.assertTrue(oracle.is_square(value), f"{p}, {n}")
            self.assertEqual(se, oracle.exact_sqrt(value))
            self.assertEqual(se * se, value)

    def test_n_pair_bank(self):
        for n1, n2, v in sc.N_PAIR_BANK:
            self.assertLessEqual(n1, n2)
            self.assertEqual(Fraction(1, n1) + Fraction(1, n2), v)
            self.assertTrue(oracle.is_square(v))

    def test_two_sample_se_bank(self):
        for s1, n1, s2, n2, v in sc.TWO_SAMPLE_SE_BANK:
            self.assertEqual(Fraction(s1 * s1, n1) + Fraction(s2 * s2, n2), v)
            self.assertEqual(int(math.isqrt(v)) ** 2, v)

    def test_pooled_pairs(self):
        for s1, s2, sp in sc.POOLED_S_PAIRS:
            self.assertEqual(Fraction(s1 * s1 + s2 * s2, 2), sp * sp)

    def test_diff_prop_se_bank(self):
        for (p1, n1), (p2, n2), se in sc.DIFF_PROP_SE_BANK:
            value = (Fraction(p1) * (1 - Fraction(p1)) / n1
                     + Fraction(p2) * (1 - Fraction(p2)) / n2)
            self.assertTrue(oracle.is_square(value))
            self.assertEqual(se, oracle.exact_sqrt(value))
            self.assertLessEqual(n1, 2500)
            self.assertLessEqual(n2, 2500)

    def test_searches_find_the_banked_rows(self):
        found = set(sc.search_prop_se(n_max=2500))
        for row in sc.PROP_SE_BANK:
            self.assertIn(row, found)
        found = set(sc.search_n_pair_se(n_max=200))
        for row in sc.N_PAIR_BANK:
            self.assertIn(row, found)
        found = set(sc.search_pooled_pairs(s_max=30))
        for row in sc.POOLED_S_PAIRS:
            self.assertIn(row, found)
        found = set(sc.search_two_sample_se(s_max=25, n_max=100))
        for row in sc.TWO_SAMPLE_SE_BANK:
            self.assertIn(row, found)

    def test_diff_prop_search_extends_the_bank(self):
        found = set(sc.search_diff_prop_se(n_max=2500, step_n=200))
        for row in sc.DIFF_PROP_SE_BANK:
            if row[0][1] % 200 == 0 and row[1][1] % 200 == 0:
                self.assertIn(row, found)
        self.assertGreater(len(found), len(sc.DIFF_PROP_SE_BANK))

    def test_prop_se_helper(self):
        self.assertEqual(Fraction(1, 20), sc.prop_se(Fraction(1, 2), 100))
        with self.assertRaises(ValueError):
            sc.prop_se(Fraction(1, 3), 7)


class TestFiveSummaryAndRanks(unittest.TestCase):
    def test_agrees_with_the_five_number_summary_generator(self):
        r = rng(14)
        for n in GEN_SIZES:
            for _ in range(ROUNDS):
                data = [r.randint(5, 45) for _ in range(n)]
                mn, q1, med, q3, mx, lo_half, hi_half = gen_summary(data)
                got = sc.five_summary(data, halves=True)
                self.assertEqual(
                    (Fraction(mn), Fraction(q1), Fraction(med),
                     Fraction(q3), Fraction(mx)), got[:5])
                self.assertEqual([Fraction(v) for v in lo_half], got[5])
                self.assertEqual([Fraction(v) for v in hi_half], got[6])

    def test_sizes_make_the_quartiles_data_points(self):
        r = rng(15)
        self.assertEqual(GEN_SIZES, sc.SUMMARY_SIZES)
        for n in sc.SUMMARY_SIZES:
            data = sorted(r.sample(range(1, 90), n))
            _, q1, _, q3, _ = sc.five_summary(data)
            self.assertIn(q1, [Fraction(v) for v in data])
            self.assertIn(q3, [Fraction(v) for v in data])

    def test_agrees_with_the_oracle_summary(self):
        r = rng(16)
        for _ in range(ROUNDS):
            n = r.randint(4, 20)
            data = [r.randint(0, 60) for _ in range(n)]
            self.assertEqual(oracle.five_summary(data), sc.five_summary(data))
            self.assertEqual(oracle.iqr(data), sc.iqr(data))

    def test_outlier_fences(self):
        data = [10, 12, 14, 16, 18, 60]
        lo, hi = sc.outlier_fences(data)
        self.assertEqual(sorted(v for v in data if v < lo or v > hi),
                         [int(v) for v in oracle.outliers(data)])

    def test_nearest_rank_matches_the_oracle(self):
        r = rng(17)
        for _ in range(ROUNDS):
            n = r.choice([10, 20, 25, 40, 50])
            data = sorted(r.sample(range(1, 200), n))
            k = r.choice([10, 25, 50, 75, 80, 90])
            self.assertEqual(oracle.nearest_rank(data, k),
                             sc.nearest_rank(data, k))

    def test_nearest_rank_positions(self):
        self.assertEqual(16, sc.nearest_rank_position(20, 80))
        self.assertEqual(1, sc.nearest_rank_position(20, 1))
        self.assertEqual(20, sc.nearest_rank_position(20, 100))

    def test_nearest_rank_requires_sorted_input(self):
        with self.assertRaises(ValueError):
            sc.nearest_rank([3, 1, 2], 50)

    def test_percentile_rank(self):
        data = sorted([3, 7, 9, 11, 15, 18, 20, 24, 30, 41])
        self.assertEqual(oracle.percentile_rank(data, 15),
                         sc.percentile_rank(data, 15))
        self.assertEqual(Fraction(40), sc.percentile_rank(data, 15))


class TestStepsAndAnswerShapes(unittest.TestCase):
    def test_running_sum_steps_matches_the_hand_written_chain(self):
        values = [12, 15, 17, 4]
        steps, total = sc.running_sum_steps(values)
        self.assertEqual(["A|12|15|27", "A|27|17|44", "A|44|4|48"], steps)
        self.assertEqual(Fraction(48), total)

    def test_running_sum_steps_on_one_value(self):
        steps, total = sc.running_sum_steps([9])
        self.assertEqual([], steps)
        self.assertEqual(Fraction(9), total)

    def test_running_sum_steps_render_fractions_exactly(self):
        steps, total = sc.running_sum_steps([Fraction(1, 2), Fraction(1, 3)])
        self.assertEqual(["A|0.5|1/3|5/6"], steps)
        self.assertEqual(Fraction(5, 6), total)

    def test_dev_rows(self):
        steps, ss = sc.dev_rows([9, 11, 11, 13], 11)
        self.assertEqual(["DEV_ROW|9|-2|4", "DEV_ROW|11|0|0",
                          "DEV_ROW|11|0|0", "DEV_ROW|13|2|4"], steps)
        self.assertEqual(Fraction(8), ss)

    def test_text_list(self):
        self.assertEqual("6: 2; 7: 0; 8: 4", sc.text_list({6: 2, 7: 0, 8: 4}))
        self.assertEqual("3: 1/6; 4: 1/6; 5: 1/3",
                         sc.text_list([(3, "1/6"), (4, "1/6"), (5, "1/3")]))

    def test_frac_label(self):
        self.assertEqual(["1/4", "1/2", "3/4", "1", "1 1/4", "-3/4"],
                         [sc.frac_label(v) for v in
                          (Fraction(1, 4), Fraction(2, 4), Fraction(3, 4),
                           Fraction(4, 4), Fraction(5, 4), Fraction(-3, 4))])

    def test_num_txt(self):
        self.assertEqual("5", sc.num_txt(5))
        self.assertEqual("2.5", sc.num_txt(Fraction(5, 2)))
        self.assertEqual("8/3", sc.num_txt(Fraction(8, 3)))

    def test_no_rendering_leaks_an_ascii_bar(self):
        blocks = [
            sc.render_dot_plot([1, 2, 2, 3]),
            sc.render_line_plot([Fraction(1, 2), 1], Fraction(1, 2)),
            sc.render_tally({"Red": 7}),
            sc.render_stem_leaf([12, 25]),
            sc.render_box_plot((1, 3, 5, 7, 9)),
            sc.render_two_way(["A"], ["X", "Y"], [[1, 2]], totals=True),
            sc.render_bins(sc.bin_counts([1, 12], 10, 0)),
            sc.inverse_z_table([90]),
            sc.phi_table([1.5]),
            sc.critical_value("t*", "2.262", 9),
            " ".join(sc.RULES.values()),
        ]
        for block in blocks:
            self.assertNotIn("|", block)


class TestContextBank(unittest.TestCase):
    def test_every_context_is_well_formed(self):
        self.assertGreaterEqual(len(sc.CONTEXTS), 10)
        for ctx in sc.CONTEXTS:
            self.assertTrue(ctx.key and ctx.label and ctx.item)
            self.assertLess(ctx.lo, ctx.hi)
            self.assertEqual(ctx, sc.context(ctx.key))
        self.assertEqual(len(sc.CONTEXTS), len(sc.CONTEXTS_BY_KEY))

    def test_units_attach(self):
        ctx = sc.context("commute_times")
        self.assertEqual("42 minutes", sc.with_unit(42, ctx))
        self.assertEqual("1 minute", sc.with_unit(1, ctx, singular=True))
        self.assertEqual("9", sc.with_unit(9, sc.context("shoe_sizes")))

    def test_random_context(self):
        random.seed(3)
        self.assertIn(sc.context(), sc.CONTEXTS)


class TestOracleRoutines(unittest.TestCase):
    """The oracle's own exact routines, checked against independent facts."""

    def test_enumerate_samples(self):
        self.assertEqual(6, len(oracle.enumerate_samples([2, 4, 6, 8], 2)))
        self.assertEqual(16, len(oracle.enumerate_samples([2, 4, 6, 8], 2,
                                                          replace=True)))

    def test_sampling_distribution_of_xbar(self):
        dist = oracle.sampling_distribution([2, 4, 6, 8], 2)
        self.assertEqual({Fraction(3): Fraction(1, 6),
                          Fraction(4): Fraction(1, 6),
                          Fraction(5): Fraction(1, 3),
                          Fraction(6): Fraction(1, 6),
                          Fraction(7): Fraction(1, 6)}, dist)
        self.assertEqual(Fraction(1), sum(dist.values()))
        self.assertEqual(oracle.mean([2, 4, 6, 8]),
                         sum(k * v for k, v in dist.items()))

    def test_binomial_tail(self):
        self.assertEqual(Fraction(9, 256),
                         oracle.binomial_tail(8, 7, Fraction(1, 2)))
        self.assertEqual(Fraction(1),
                         oracle.binomial_tail(8, 0, Fraction(1, 2)))

    def test_chi_terms(self):
        terms, total = oracle.chi_terms([12, 8], [10, 10])
        self.assertEqual([Fraction(2, 5), Fraction(2, 5)], terms)
        self.assertEqual(Fraction(4, 5), total)

    def test_anova_matches_the_plan_worked_example(self):
        got = oracle.anova([[8, 10, 10, 12], [12, 14, 14, 16],
                            [16, 18, 18, 20]])
        self.assertEqual(Fraction(128), got["ssb"])
        self.assertEqual(Fraction(24), got["ssw"])
        self.assertEqual(got["sst"], got["ssb"] + got["ssw"])
        self.assertEqual((2, 9), got["df"])
        self.assertEqual(Fraction(64), got["msb"])
        self.assertEqual(Fraction(8, 3), got["msw"])
        self.assertEqual(Fraction(24), got["f"])

    def test_study_design_cue_banks_are_disjoint(self):
        for name, bank in oracle.CUE_BANKS.items():
            with self.subTest(bank=name):
                self.assertEqual([], oracle.cue_conflicts(bank))

    def test_label_from_scenario(self):
        text = ("The principal chose 20 students from each grade and "
                "surveyed them.")
        self.assertEqual("stratified",
                         oracle.label_from_scenario(text,
                                                    oracle.SAMPLING_CUES))
        with self.assertRaises(ValueError):
            oracle.label_from_scenario("No cue here.", oracle.SAMPLING_CUES)


if __name__ == "__main__":
    unittest.main()
