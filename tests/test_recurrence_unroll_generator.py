"""Prompt-only oracle for RecurrenceUnrollGenerator (depth strand)."""
import random
import re
import unittest

from generators.recurrence_unroll_generator import RecurrenceUnrollGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_SEEDS = re.compile(r"x0 = (\d+)(?:,| and) x1 = (\d+)")
_RULE = re.compile(r"\((\d+)\*x\(k\) \+ (\d+)\*x\(k-1\)\) mod (\d+)")
_FIB_MOD = re.compile(r"mod (\d+)")
_TERMS = re.compile(r"(\d+) terms")


def _mat_pow_vec(p, q, n, m, x1, x0):
    """x_n via C^n on (x1, x0) — fast power, never the unroll loop."""
    def mul(A, B):
        return (((A[0][0] * B[0][0] + A[0][1] * B[1][0]) % m,
                 (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % m),
                ((A[1][0] * B[0][0] + A[1][1] * B[1][0]) % m,
                 (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % m))
    result, base, e = ((1, 0), (0, 1)), ((p, q), (1, 0)), n
    while e:
        if e & 1:
            result = mul(result, base)
        base = mul(base, base)
        e >>= 1
    return (result[1][0] * x1 + result[1][1] * x0) % m


def oracle_answer(example):
    problem = example["problem"]
    op = example["operation"]
    if op.startswith("recurrence_unroll_pisano_period"):
        m = int(_FIB_MOD.search(problem).group(1))
        a, b, n = 0, 1, 0
        while True:
            a, b = b, (a + b) % m
            n += 1
            if (a, b) == (0, 1):
                return str(n)
    x0, x1 = map(int, _SEEDS.search(problem).groups())
    rule = _RULE.search(problem)
    if rule:
        p, q, m = map(int, rule.groups())
    else:
        p = q = 1
        m = int(_FIB_MOD.search(problem).group(1))
    n = int(_TERMS.search(problem).group(1))
    return str(_mat_pow_vec(p, q, n + 1, m, x1, x0))


class TestRecurrenceUnrollGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RecurrenceUnrollGenerator()

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
        for variant in RecurrenceUnrollGenerator.VARIANTS:
            gen = RecurrenceUnrollGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:160])

    def test_every_rec_step_applies_the_rule(self):
        gen = RecurrenceUnrollGenerator("term_n_mod_m", tier="d100")
        for _ in range(10):
            result = gen.generate()
            p, q, m = map(int, _RULE.search(result["problem"]).groups())
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "REC_STEP":
                    continue
                a, b = map(int, re.fullmatch(
                    r"\((\d+), (\d+)\)", fields[1]).groups())
                a2, b2 = map(int, re.fullmatch(
                    r"\((\d+), (\d+)\)", fields[3]).groups())
                self.assertEqual(a2, b, raw)
                self.assertEqual(b2, (p * b + q * a) % m, raw)

    def test_pisano_trace_returns_to_start(self):
        gen = RecurrenceUnrollGenerator("pisano_period", tier="d50")
        for _ in range(10):
            result = gen.generate()
            recs = [s for s in result["steps"]
                    if s.startswith(f"REC_STEP{DELIM}")]
            self.assertEqual(recs[-1].split(DELIM)[3], "(0, 1)")
            self.assertEqual(recs[0].split(DELIM)[1], "(0, 1)")
            self.assertEqual(len(recs), int(result["final_answer"]))

    def test_matrix_check_agrees(self):
        gen = RecurrenceUnrollGenerator("matrix_check", tier="d50")
        for _ in range(10):
            result = gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            fields = check.split(DELIM)
            lhs = int(re.search(r"= (\d+)$", fields[2]).group(1))
            rhs = int(re.search(r"= (\d+)$", fields[3]).group(1))
            self.assertEqual(lhs, rhs, check)
            self.assertEqual(str(rhs), result["final_answer"])
            self.assertTrue(any(s.startswith(f"MAT_POW{DELIM}")
                                for s in result["steps"]))

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = RecurrenceUnrollGenerator("term_n_mod_m",
                                               tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 12)  # 4 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            RecurrenceUnrollGenerator("bogus")
        with self.assertRaises(ValueError):
            RecurrenceUnrollGenerator(tier="d33")


if __name__ == "__main__":
    unittest.main()
