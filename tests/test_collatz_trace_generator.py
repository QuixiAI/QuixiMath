"""Prompt-only oracle for CollatzTraceGenerator (depth strand)."""
import random
import re
import unittest

from generators.collatz_trace_generator import CollatzTraceGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_SEED = re.compile(r"(?:Start at|add 1\) to|starting at|From|from) (\d+)")


def oracle_answer(example):
    """Plain independent simulation from the seed in the problem text."""
    problem = example["problem"]
    seed = int(_SEED.search(problem).group(1))
    op = example["operation"]
    below = seed if "steps_to_below_seed" in op else None
    value, applications, peak, odds = seed, 0, seed, 0
    while value != 1 and not (below is not None and value < below):
        if value % 2:
            odds += 1
            value = 3 * value + 1
        else:
            value //= 2
        applications += 1
        peak = max(peak, value)
    if "stopping_time" in op or "steps_to_below_seed" in op:
        return str(applications)
    if "max_value" in op:
        return str(peak)
    return str(odds)


class TestCollatzTraceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CollatzTraceGenerator()

    def test_output_contract_and_depth(self):
        for _ in range(20):
            result = self.gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            tier = result["operation"].rsplit("_", 1)[1]
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS[tier])
            self.assertFalse(milestone_violations(result["steps"]))
            self.assertLessEqual(record_chars(result), 16_000)
            self.assertIsNotNone(parse_count(result["problem"]))

    def test_oracle_recomputes_from_problem_text(self):
        for variant in CollatzTraceGenerator.VARIANTS:
            gen = CollatzTraceGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:150])

    def test_every_step_applies_the_collatz_rule(self):
        gen = CollatzTraceGenerator("stopping_time", tier="d100")
        for _ in range(10):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // 2, int(fields[3]), raw)
                    self.assertEqual(int(fields[1]) % 2, 0, raw)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * 3, int(fields[3]), raw)
                    self.assertEqual(int(fields[1]) % 2, 1, raw)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + 1, int(fields[3]), raw)

    def test_values_stay_under_the_cap(self):
        gen = CollatzTraceGenerator("max_value", tier="d200")
        for _ in range(8):
            result = gen.generate()
            self.assertLessEqual(int(result["final_answer"]), 99_999)

    def test_stated_cap_covers_the_applications(self):
        gen = CollatzTraceGenerator("stopping_time", tier="d50")
        for _ in range(10):
            result = gen.generate()
            cap = int(re.search(r"at most (\d+) steps",
                                result["problem"]).group(1))
            self.assertGreaterEqual(cap, int(result["final_answer"]))

    def test_below_seed_trace_stops_below_the_seed(self):
        gen = CollatzTraceGenerator("steps_to_below_seed", tier="d50")
        for _ in range(10):
            result = gen.generate()
            seed = int(_SEED.search(result["problem"]).group(1))
            last_value = int(result["steps"][-2].split(DELIM)[-1])
            self.assertLess(last_value, seed)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = CollatzTraceGenerator("stopping_time",
                                           tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(400):
            seen.add(self.gen.generate()["operation"])
        # three variants x three tiers, plus steps_to_below_seed at d50 only
        self.assertEqual(len(seen), 10)
        self.assertIn("collatz_trace_steps_to_below_seed_d50", seen)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            CollatzTraceGenerator("bogus")
        with self.assertRaises(ValueError):
            CollatzTraceGenerator(tier="d5")
        with self.assertRaises(ValueError):
            CollatzTraceGenerator("steps_to_below_seed", tier="d100")


if __name__ == "__main__":
    unittest.main()
