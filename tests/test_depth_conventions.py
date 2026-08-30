"""Strand conventions for the depth strand (``plans/depth_plan.md`` §3).

Discovers generators by the module flag ``DEPTH = True`` and enforces the
strand contract on every one: tier floors on measured dependency depth,
milestone shape, pipe safety, the base output contract, and the record
size cap.  Fixture tests prove each checker actually rejects a violating
trace, so the suite stays meaningful while the strand has few (or zero)
registered classes.
"""
import unittest

from helpers import step
from depth_common import (Chain, DEPTH_TIERS, MAX_RECORD_CHARS, TIER_FLOORS,
                          cents_ledger, cents_txt, contractive_orbit,
                          find_cycle, modular_orbit, parse_count, pick_tier,
                          tier_of, tier_target)
from tests.conventions_common import (assert_contract, assert_pipe_safe,
                                      flagged_generators, sample_examples)
from tests.depth_oracle import (affine_orbit_value, brent_cycle, chain_depth,
                                geometric_partial_sum, milestone_violations,
                                record_chars)
from tests.depth_oracle import parse_count as oracle_parse_count


def depth_generators():
    return flagged_generators("DEPTH")


class TestRegisteredDepthGenerators(unittest.TestCase):
    """The per-generator battery (vacuous until Phase 1 lands classes).

    Retrofit semantics (plans/depth_plan.md §3): a ⟲ class keeps its
    legacy variants untiered, and untiered draws are exempt from the
    depth checks — but every flagged module must REACH tiered
    operations in sampling, or its DEPTH flag is meaningless.
    """

    def test_strand_contract(self):
        for gen in depth_generators():
            tiered_seen = 0
            for example in sample_examples(gen, n=25, seed=11):
                with self.subTest(gen=type(gen).__name__,
                                  op=example["operation"]):
                    assert_contract(self, example)
                    assert_pipe_safe(self, example)
                    self.assertLessEqual(record_chars(example),
                                         MAX_RECORD_CHARS)
                    tier = tier_of(example["operation"])
                    if tier is None:
                        continue  # a retrofit class's legacy face
                    tiered_seen += 1
                    self.assertGreaterEqual(
                        chain_depth(example["steps"]), TIER_FLOORS[tier],
                        "measured dependency depth below the tier floor")
                    self.assertFalse(milestone_violations(example["steps"]))
                    self.assertIsNotNone(
                        oracle_parse_count(example["problem"]),
                        "problem text must state the chain length")
            self.assertGreater(
                tiered_seen, 0,
                f"{type(gen).__name__} is DEPTH-flagged but never "
                "produced a tiered operation in 25 draws")


class TestChainEmitter(unittest.TestCase):
    def test_chain_links_by_string_equality(self):
        chain = Chain(7)
        value = 7
        for k in range(50):
            value = (3 * value + 1) % 97
            chain.apply("ITER", f"n={k + 1}", value)
        self.assertEqual(chain.links, 50)
        self.assertEqual(chain_depth(chain.steps), 50)

    def test_extra_annotation_does_not_break_the_chain(self):
        chain = Chain(10)
        chain.apply("ITER", "n=1", 31, extra="tripled plus one")
        chain.apply("ITER", "n=2", 94)
        self.assertEqual(chain_depth(chain.steps), 2)

    def test_milestones_interleave_without_breaking_depth(self):
        chain = Chain(5, milestone_spacing=True)
        chain.set_invariant("value mod 9", lambda v, k: v % 9)
        value = 5
        for k in range(60):
            value = (2 * value + 3) % 89
            chain.apply("ITER", f"n={k + 1}", value)
        milestones = [s for s in chain.steps if s.startswith("MILESTONE")]
        self.assertGreaterEqual(len(milestones), 2)
        self.assertEqual(chain_depth(chain.steps), 60)
        self.assertFalse(milestone_violations(chain.steps))

    def test_milestone_requires_invariant(self):
        with self.assertRaises(ValueError):
            Chain(1).milestone()


class TestCheckersRejectViolations(unittest.TestCase):
    """Each conventions checker must fail the trace it exists to catch."""

    def test_broken_chain_is_measured_short(self):
        steps = [step("ITER", 7, "n=1", 22),
                 step("ITER", 22, "n=2", 67),
                 step("ITER", 999, "n=3", 12),   # stale state: not 67
                 step("ITER", 12, "n=4", 37)]
        self.assertEqual(chain_depth(steps), 2)

    def test_enumeration_does_not_masquerade_as_depth(self):
        # Wide, independent rows (truth-table style): no linkage at all.
        steps = [step("ROW", k, "eval", k * k) for k in range(40)]
        self.assertLess(chain_depth(steps), 3)

    def test_milestone_shape_violations_are_caught(self):
        missing_field = [step("MILESTONE", 10, "value mod 9")]
        self.assertTrue(milestone_violations(missing_field))
        bad_position = [step("MILESTONE", "ten", "value mod 9", 4)]
        self.assertTrue(milestone_violations(bad_position))
        its = [step("ITER", k, "n", k + 1) for k in range(40)]
        too_close = (its[:12] + [step("MILESTONE", 12, "inv", 1)]
                     + its[12:14] + [step("MILESTONE", 14, "inv", 1)]
                     + its[14:])
        self.assertTrue(milestone_violations(too_close))
        not_increasing = (its[:12] + [step("MILESTONE", 12, "inv", 1)]
                          + its[12:24] + [step("MILESTONE", 12, "inv", 1)]
                          + its[24:])
        self.assertTrue(milestone_violations(not_increasing))
        beyond_chain = its[:8] + [step("MILESTONE", 30, "inv", 1)]
        self.assertTrue(milestone_violations(beyond_chain))

    def test_record_size_cap_is_measured(self):
        example = {"problem": "p" * 15_000, "steps": ["Z|x" * 500],
                   "final_answer": "x"}
        self.assertGreater(record_chars(example), MAX_RECORD_CHARS)


class TestTiers(unittest.TestCase):
    def test_tier_windows_and_floors_agree(self):
        for tier, (lo, hi) in DEPTH_TIERS.items():
            self.assertLess(lo, hi)
            self.assertEqual(TIER_FLOORS[tier], lo)

    def test_tier_target_lands_in_window(self):
        for tier, (lo, hi) in DEPTH_TIERS.items():
            for _ in range(50):
                self.assertTrue(lo <= tier_target(tier) <= hi)

    def test_pick_tier_hits_all_tiers(self):
        import random
        random.seed(4)
        seen = {pick_tier() for _ in range(300)}
        self.assertEqual(seen, set(DEPTH_TIERS))

    def test_tier_of_parses_only_the_suffix(self):
        self.assertEqual(tier_of("iterated_affine_map_final_state_d100"),
                         "d100")
        self.assertIsNone(tier_of("mean"))
        self.assertIsNone(tier_of("d50_warmup"))


class TestBoundedConstructors(unittest.TestCase):
    def test_modular_orbit_matches_closed_form(self):
        orbit = modular_orbit(5, 3, 101, 17, 200)
        for n in (0, 1, 50, 137, 200):
            self.assertEqual(orbit[n], affine_orbit_value(5, 3, 101, 17, n))
        self.assertTrue(all(0 <= x < 101 for x in orbit))

    def test_modular_orbit_identity_multiplier(self):
        orbit = modular_orbit(1, 7, 30, 4, 90)
        self.assertEqual(orbit[90], affine_orbit_value(1, 7, 30, 4, 90))

    def test_floyd_and_brent_agree(self):
        f = lambda x: (7 * x + 4) % 64
        self.assertEqual(find_cycle(f, 3), brent_cycle(f, 3))
        g = lambda x: (x * x + 1) % 255
        self.assertEqual(find_cycle(g, 2), brent_cycle(g, 2))

    def test_contractive_orbit_is_integral_and_bounded(self):
        orbit = contractive_orbit(2, 40, 12, delta=3)
        self.assertEqual(orbit[0], 40 + 3 * 2 ** 12)
        self.assertEqual(orbit[-1], 43)
        for early, late in zip(orbit, orbit[1:]):
            self.assertEqual(late - 40, (early - 40) // 2)
        with self.assertRaises(ValueError):
            contractive_orbit(2, 0, 40)  # 2**40 breaks the value bound

    def test_cents_ledger_respects_bounds_and_granularity(self):
        import random
        rng = random.Random(9)
        events = cents_ledger(500_00, 120, rng=rng)
        balance = 500_00
        for kind, amount, new_balance in events:
            self.assertEqual(amount % 25, 0)
            balance += amount if kind == "deposit" else -amount
            self.assertEqual(balance, new_balance)
            self.assertTrue(0 <= balance <= 1_000_00)

    def test_geometric_partial_sum_closed_form(self):
        total = sum((3 * (2 ** k) for k in range(20)))
        self.assertEqual(geometric_partial_sum(3, 2, 20), total)
        self.assertEqual(geometric_partial_sum(5, 1, 7), 35)


class TestCountParsing(unittest.TestCase):
    PHRASES = (
        ("Iterate the map 120 times starting from 17.", 120),
        ("Unroll the recurrence for 96 terms.", 96),
        ("The account records 55 events this quarter.", 55),
        ("Apply the rule 200 times.", 200),
        ("Execute the program for 150 instructions.", 150),
        ("Find the balance after the first 84 payments.", 84),
        ("No count here at all.", None),
    )

    def test_both_parsers_agree_on_every_phrase(self):
        for text, expected in self.PHRASES:
            self.assertEqual(parse_count(text), expected, text)
            self.assertEqual(oracle_parse_count(text), expected, text)

    def test_money_rendering(self):
        self.assertEqual(cents_txt(123456), "$1234.56")
        self.assertEqual(cents_txt(5), "$0.05")
        self.assertEqual(cents_txt(-75), "-$0.75")


if __name__ == "__main__":
    unittest.main()
