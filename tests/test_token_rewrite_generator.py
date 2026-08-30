"""Prompt-only oracle for TokenRewriteGenerator (depth strand)."""
import random
import re
import unittest

from generators.token_rewrite_generator import TokenRewriteGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_START = re.compile(r"(?:string|to|Reduce|Drive) ([abc]{4,})\b")
_RULES = re.compile(r"([abc]{2}) -> ([abc]{2})")


def _inversions(start, pair):
    """Count of (pair[0] ... pair[1]) out-of-order pairs — closed form,
    never the rewriting loop."""
    high, low = pair
    count = 0
    highs_seen = 0
    for ch in start:
        if ch == high:
            highs_seen += 1
        elif ch == low:
            count += highs_seen
    return count


def oracle_answer(example):
    problem = example["problem"]
    start = _START.search(problem).group(1)
    rules = [f"{a} -> {b}" for a, b in _RULES.findall(problem)]
    op = example["operation"]
    if op.startswith("token_rewrite_normal_form"):
        return "".join(sorted(start))  # total sort's fixed point
    per_rule = {rule: _inversions(start, rule.split(" ")[0])
                for rule in rules}
    if op.startswith("token_rewrite_step_count"):
        return str(sum(per_rule.values()))
    return "; ".join(f"{rule.split(' ')[0]}: {per_rule[rule]}"
                     for rule in rules)


class TestTokenRewriteGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TokenRewriteGenerator()

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
        for variant in TokenRewriteGenerator.VARIANTS:
            gen = TokenRewriteGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:170])

    def test_every_rw_step_applies_a_stated_rule(self):
        gen = TokenRewriteGenerator("step_count", tier="d100")
        for _ in range(8):
            result = gen.generate()
            rules = {f"{a} -> {b}": (a, b) for a, b in
                     _RULES.findall(result["problem"])}
            lhs_set = {a for a, b in rules.values()}
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "RW_STEP":
                    continue
                lhs, position = fields[2].split("@")
                position = int(position)
                self.assertIn(lhs, lhs_set, raw)
                before, after = fields[1], fields[3]
                self.assertEqual(before[position:position + 2], lhs, raw)
                self.assertEqual(after[position:position + 2],
                                 lhs[::-1], raw)
                self.assertEqual(before[:position], after[:position], raw)
                self.assertEqual(before[position + 2:],
                                 after[position + 2:], raw)

    def test_letter_counts_conserved_throughout(self):
        gen = TokenRewriteGenerator("normal_form", tier="d200")
        for _ in range(5):
            result = gen.generate()
            start = _START.search(result["problem"]).group(1)
            expected = sorted(start)
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "RW_STEP":
                    self.assertEqual(sorted(fields[3]), expected, raw)

    def test_trace_length_matches_step_count_answer(self):
        gen = TokenRewriteGenerator("step_count", tier="d50")
        for _ in range(10):
            result = gen.generate()
            rows = sum(1 for s in result["steps"]
                       if s.startswith(f"RW_STEP{DELIM}"))
            self.assertEqual(rows, int(result["final_answer"]))

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = TokenRewriteGenerator("step_count",
                                           tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            TokenRewriteGenerator("bogus")
        with self.assertRaises(ValueError):
            TokenRewriteGenerator(tier="deep")


if __name__ == "__main__":
    unittest.main()
