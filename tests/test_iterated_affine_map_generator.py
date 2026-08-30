"""Prompt-only oracle for IteratedAffineMapGenerator (depth strand)."""
import random
import re
import unittest

from generators.iterated_affine_map_generator import IteratedAffineMapGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (affine_orbit_value, brent_cycle, chain_depth,
                                milestone_violations, parse_count,
                                record_chars)

_MAP = re.compile(r"x -> \((\d+)x \+ (\d+)\) mod (\d+)")
_N = re.compile(r"(\d+)\s+(?:times|iterations|applications)")
_START_PATTERNS = (re.compile(r"x = (\d+)"),
                   re.compile(r"starting at (\d+)"),
                   re.compile(r"from (\d+) until"),
                   re.compile(r"orbit of (\d+) under"))


class _Start:
    @staticmethod
    def search(problem):
        for pattern in _START_PATTERNS:
            match = pattern.search(problem)
            if match:
                return match
        return None


_START = _Start()
_END = re.compile(r"(?:produced|value\s+is|into|ending at) (\d+)[,.\s]")


def oracle_answer(example):
    problem = example["problem"]
    a, b, m = map(int, _MAP.search(problem).groups())
    op = example["operation"]
    f = lambda x: (a * x + b) % m
    if op.startswith("iterated_affine_map_final_state"):
        x0 = int(_START.search(problem).group(1))
        n = int(_N.search(problem).group(1))
        return str(affine_orbit_value(a, b, m, x0, n))
    if op.startswith("iterated_affine_map_backward"):
        xn = int(_END.search(problem).group(1))
        n = int(_N.search(problem).group(1))
        # Solve the closed form for x0 instead of stepping the inverse.
        an = pow(a, n, m)
        drift = (b * ((pow(a, n) - 1) // (a - 1))) % m if a != 1 else (n * b) % m
        return str(((xn - drift) * pow(an, -1, m)) % m)
    x0 = int(_START.search(problem).group(1))
    mu, lam = brent_cycle(f, x0)
    if op.startswith("iterated_affine_map_first_return"):
        return str(lam)
    return f"period {lam}; enters cycle at n={mu}"


class TestIteratedAffineMapGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IteratedAffineMapGenerator()

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
            self.assertIsNotNone(parse_count(result["problem"]))

    def test_oracle_recomputes_from_problem_text(self):
        for variant in IteratedAffineMapGenerator.VARIANTS:
            gen = IteratedAffineMapGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:160])

    def test_every_iter_step_applies_the_stated_map(self):
        for variant in ("final_state", "orbit_period", "first_return"):
            gen = IteratedAffineMapGenerator(variant, tier="d50")
            for _ in range(10):
                result = gen.generate()
                a, b, m = map(int, _MAP.search(result["problem"]).groups())
                for raw in result["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] == "ITER":
                        self.assertEqual((a * int(fields[1]) + b) % m,
                                         int(fields[3]), raw)

    def test_backward_steps_apply_the_inverse_map(self):
        gen = IteratedAffineMapGenerator("backward", tier="d50")
        for _ in range(10):
            result = gen.generate()
            a, b, m = map(int, _MAP.search(result["problem"]).groups())
            ainv = pow(a, -1, m)
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "ITER_INV":
                    self.assertEqual((ainv * (int(fields[1]) - b)) % m,
                                     int(fields[3]), raw)

    def test_first_return_trace_ends_at_the_start(self):
        gen = IteratedAffineMapGenerator("first_return", tier="d50")
        for _ in range(10):
            result = gen.generate()
            x0 = int(_START.search(result["problem"]).group(1))
            iters = [s for s in result["steps"]
                     if s.startswith(f"ITER{DELIM}")]
            self.assertEqual(int(iters[-1].split(DELIM)[3]), x0)
            self.assertEqual(len(iters), int(result["final_answer"]))

    def test_orbit_period_trace_witnesses_the_repeat(self):
        gen = IteratedAffineMapGenerator("orbit_period", tier="d50")
        for _ in range(10):
            result = gen.generate()
            x0 = int(_START.search(result["problem"]).group(1))
            values = [x0] + [int(s.split(DELIM)[3])
                             for s in result["steps"]
                             if s.startswith(f"ITER{DELIM}")]
            match = re.fullmatch(r"period (\d+); enters cycle at n=(\d+)",
                                 result["final_answer"])
            lam, mu = int(match.group(1)), int(match.group(2))
            self.assertEqual(values[-1], values[mu])
            self.assertEqual(len(values) - 1, mu + lam)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = IteratedAffineMapGenerator("final_state",
                                                tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 12)  # 4 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            IteratedAffineMapGenerator("bogus")
        with self.assertRaises(ValueError):
            IteratedAffineMapGenerator(tier="huge")


if __name__ == "__main__":
    unittest.main()
