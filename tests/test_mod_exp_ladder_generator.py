"""Prompt-only oracle for ModExpLadderGenerator (depth strand)."""
import random
import re
import unittest

from generators.mod_exp_ladder_generator import ModExpLadderGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_POWER = re.compile(r"(\d+)\^(\d+) mod (\d+)")


def _order_by_divisors(a, m):
    """Smallest d | m-1 with a^d = 1 — never the generator's step loop."""
    divisors = sorted(d for k in range(1, int((m - 1) ** 0.5) + 1)
                      if (m - 1) % k == 0 for d in {k, (m - 1) // k})
    return next(d for d in divisors if pow(a, d, m) == 1)


def _consumed_schedule(e):
    """Bit index consumed at each ladder link, from the expansion alone."""
    bits = bin(e)[2:]
    out = [1]
    for index, bit in enumerate(bits[1:], start=2):
        out.append(index)
        if bit == "1":
            out.append(index)
    return out


def oracle_answer(example):
    a, e, m = map(int, _POWER.search(example["problem"]).groups())
    op = example["operation"]
    if op.startswith("mod_exp_ladder_fermat_route"):
        order = _order_by_divisors(a, m)
        reduced = e % order
        return (f"E = {reduced} (mod {order}); "
                f"{a}^E = {pow(a, reduced, m)} (mod {m})")
    if op.startswith("mod_exp_ladder_ladder_audit"):
        return f"{pow(a, e, m)}; {e.bit_length()} bits consumed"
    return str(pow(a, e, m))


class TestModExpLadderGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ModExpLadderGenerator()

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
        for variant in ModExpLadderGenerator.VARIANTS:
            gen = ModExpLadderGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:120])

    def test_every_ladder_step_is_exact(self):
        gen = ModExpLadderGenerator("final_residue", tier="d100")
        for _ in range(10):
            result = gen.generate()
            a, e, m = map(int, _POWER.search(result["problem"]).groups())
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "LADDER":
                    continue
                if fields[2].startswith("start"):
                    self.assertEqual(int(fields[-1]), a % m, raw)
                elif fields[2].startswith("square"):
                    self.assertEqual((int(fields[1]) ** 2) % m,
                                     int(fields[3]), raw)
                else:
                    self.assertEqual((int(fields[1]) * a) % m,
                                     int(fields[3]), raw)

    def test_audit_milestones_track_bits_consumed(self):
        gen = ModExpLadderGenerator("ladder_audit", tier="d100")
        for _ in range(10):
            result = gen.generate()
            _, e, _ = map(int, _POWER.search(result["problem"]).groups())
            schedule = _consumed_schedule(e)
            audits = 0
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "MILESTONE":
                    continue
                audits += 1
                link = int(fields[1])
                self.assertEqual(int(fields[3]), schedule[link - 1], raw)
            self.assertGreater(audits, 0)

    def test_fermat_reduction_chain_is_exact(self):
        gen = ModExpLadderGenerator("fermat_route", tier="d50")
        for _ in range(10):
            result = gen.generate()
            a, e, m = map(int, _POWER.search(result["problem"]).groups())
            order = _order_by_divisors(a, m)
            div_steps = [s for s in result["steps"]
                         if s.startswith(f"DIV_STEP{DELIM}")]
            self.assertEqual(len(div_steps), len(str(e)))
            self.assertEqual(int(div_steps[-1].split(DELIM)[3]), e % order)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = ModExpLadderGenerator("final_residue",
                                           tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            ModExpLadderGenerator("bogus")
        with self.assertRaises(ValueError):
            ModExpLadderGenerator(tier="d10")


if __name__ == "__main__":
    unittest.main()
