"""Prompt-only oracle for DigitProcessGenerator (depth strand)."""
import random
import re
import unittest

from generators.digit_process_generator import DigitProcessGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_SEED = re.compile(r"(\d{10,})")
_LENGTH = re.compile(r"with (\d+) digits")


def _digit_sum(n):
    return sum(int(c) for c in str(n))


def _squared_digit_sum(n):
    return sum(int(c) * int(c) for c in str(n))


def oracle_answer(example):
    """Recompute from the problem text by an independent route."""
    problem = example["problem"]
    seed = int(_SEED.search(problem).group(1))
    op = example["operation"]
    if op.startswith("digit_process_fixed_point"):
        # Digital root closed form — never touches the iteration.
        return str(1 + (seed - 1) % 9)
    if op.startswith("digit_process_step_count"):
        passes = 0
        n = seed
        while n >= 10 or passes == 0:
            n = _digit_sum(n)
            passes += 1
        return str(passes)
    # happy_classification: standard set-based simulation.
    seen = set()
    n = seed
    passes = 0
    while True:
        n = _squared_digit_sum(n)
        passes += 1
        if n == 1:
            return f"happy; reaches 1 after {passes} passes"
        if n in seen:
            return f"unhappy; repeats {n} after {passes} passes"
        seen.add(n)


def digit_split_violations(example):
    """Each DIGIT_SPLIT must honestly split its own previous total."""
    happy = "happy_classification" in example["operation"]
    bad = []
    for raw in example["steps"]:
        fields = raw.split(DELIM)
        if fields[0] != "DIGIT_SPLIT":
            continue
        total, listed, carry = fields[1], fields[2], fields[3]
        digits = [int(d) for d in listed.removeprefix("digits ").split(",")]
        if [int(c) for c in total] != digits:
            bad.append(f"listed digits do not match the total: {raw}")
        expected = digits[0] * digits[0] if happy else digits[0]
        if int(carry) != expected:
            bad.append(f"carry is not the first digit's contribution: {raw}")
    return bad


class TestDigitProcessGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DigitProcessGenerator()

    def test_output_contract_and_depth(self):
        for _ in range(25):
            result = self.gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            tier = result["operation"].rsplit("_", 1)[1]
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS[tier])
            self.assertFalse(milestone_violations(result["steps"]))
            self.assertLessEqual(record_chars(result), 16_000)
            stated = parse_count(result["problem"])
            length = int(_LENGTH.search(result["problem"]).group(1))
            self.assertEqual(stated, length)
            self.assertEqual(len(_SEED.search(result["problem"]).group(1)),
                             length)

    def test_oracle_recomputes_from_problem_text(self):
        for variant in DigitProcessGenerator.VARIANTS:
            gen = DigitProcessGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:150])

    def test_digit_splits_are_honest(self):
        for variant in DigitProcessGenerator.VARIANTS:
            gen = DigitProcessGenerator(variant, tier="d100")
            for _ in range(20):
                result = gen.generate()
                self.assertFalse(digit_split_violations(result))

    def test_milestones_only_at_deeper_tiers(self):
        plain = DigitProcessGenerator("fixed_point", tier="d50").generate()
        self.assertFalse(any(s.startswith("MILESTONE")
                             for s in plain["steps"]))
        deep = DigitProcessGenerator("fixed_point", tier="d200").generate()
        self.assertTrue(any(s.startswith("MILESTONE") for s in deep["steps"]))

    def test_milestone_values_match_running_total(self):
        gen = DigitProcessGenerator("fixed_point", tier="d100")
        for _ in range(15):
            result = gen.generate()
            running = None
            links = 0
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] in ("A", "DIGIT_SPLIT"):
                    running = int(fields[-1])
                    links += 1
                elif fields[0] == "MILESTONE":
                    self.assertEqual(int(fields[1]), links)
                    self.assertEqual(int(fields[3]), running % 9)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = DigitProcessGenerator("fixed_point",
                                           tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            DigitProcessGenerator("bogus")
        with self.assertRaises(ValueError):
            DigitProcessGenerator(tier="d1")


if __name__ == "__main__":
    unittest.main()
