"""Prompt-only oracle for LedgerAuditGenerator (depth strand)."""
import random
import re
import unittest

from generators.ledger_audit_generator import LedgerAuditGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_MONEY_START = re.compile(
    r"(?:starts at|opens at|Starting from|balance|value) (\$\d+\.\d\d)")
_INT_START = re.compile(r"(?:starts at|opens at|Starting from|value) (\d+)")
_AFFINE = re.compile(r"x -> \((\d+)x \+ (\d+)\) mod (\d+)")
_X_START = re.compile(r"x = (\d+)")
_ROW = re.compile(r"(\d+): (\+\$\d+\.\d\d|-\$\d+\.\d\d|\+\d+|-\d+|iterate)"
                  r" = (-?\$?\d+(?:\.\d\d)?)")


def _cents(txt):
    sign = -1 if txt.startswith("-") else 1
    whole, cents = txt.lstrip("+-$").split(".")
    return sign * (int(whole) * 100 + int(cents))


def _money(cents):
    sign = "-" if cents < 0 else ""
    return f"{sign}${abs(cents) // 100}.{abs(cents) % 100:02d}"


def oracle_answer(example):
    problem = example["problem"]
    op = example["operation"]
    rows = _ROW.findall(problem)
    if op.startswith("ledger_audit_affine_table"):
        a, b, m = map(int, _AFFINE.search(problem).groups())
        value = int(_X_START.search(problem).group(1))
        advance = lambda v, delta: (a * v + b) % m
        parse_claim = int
        render = str
        unit = "value"
        deltas = [None] * len(rows)
    elif op.startswith("ledger_audit_money_ledger"):
        value = _cents(_MONEY_START.search(problem).group(1))
        advance = lambda v, delta: v + delta
        parse_claim = _cents
        render = _money
        unit = "balance"
        deltas = [_cents(d) for _, d, _ in rows]
    else:
        value = int(_INT_START.search(problem).group(1))
        advance = lambda v, delta: v + delta
        parse_claim = int
        render = str
        unit = "value"
        deltas = [int(d) for _, d, _ in rows]

    error_row = None
    for (k_txt, _, claim_txt), delta in zip(rows, deltas):
        value = advance(value, delta)
        if error_row is None and parse_claim(claim_txt) != value:
            error_row = int(k_txt)
    if error_row is None:
        return f"no errors; final {unit} {render(value)} confirmed"
    return (f"first error at row {error_row}; "
            f"correct final {unit} {render(value)}")


class TestLedgerAuditGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LedgerAuditGenerator()

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
        for variant in LedgerAuditGenerator.VARIANTS:
            gen = LedgerAuditGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:170])

    def test_error_rows_propagate_consistently(self):
        """Every claimed row AFTER the error must follow from the bad
        value by the correct operation — the audit's defining shape."""
        for variant in LedgerAuditGenerator.VARIANTS:
            gen = LedgerAuditGenerator(variant, tier="d50")
            checked = 0
            for _ in range(30):
                result = gen.generate()
                match = re.match(r"first error at row (\d+)",
                                 result["final_answer"])
                if not match:
                    continue
                checked += 1
                problem = result["problem"]
                rows = _ROW.findall(problem)
                if variant == "affine_table":
                    a, b, m = map(int, _AFFINE.search(problem).groups())
                    advance = lambda v, d: (a * v + b) % m
                    claims = [int(c) for _, _, c in rows]
                    deltas = [None] * len(rows)
                elif variant == "money_ledger":
                    advance = lambda v, d: v + d
                    claims = [_cents(c) for _, _, c in rows]
                    deltas = [_cents(d) for _, d, _ in rows]
                else:
                    advance = lambda v, d: v + d
                    claims = [int(c) for _, _, c in rows]
                    deltas = [int(d) for _, d, _ in rows]
                error = int(match.group(1))
                for index in range(error, len(rows)):
                    self.assertEqual(claims[index],
                                     advance(claims[index - 1],
                                             deltas[index]),
                                     (variant, error, index))
            self.assertGreater(checked, 10)

    def test_flag_row_matches_the_answer(self):
        gen = LedgerAuditGenerator("money_ledger", tier="d100")
        for _ in range(20):
            result = gen.generate()
            flags = [s for s in result["steps"]
                     if s.startswith(f"AUDIT_FLAG{DELIM}")]
            match = re.match(r"first error at row (\d+)",
                             result["final_answer"])
            if match:
                self.assertEqual(len(flags), 1)
                claimed_row = re.search(r"row (\d+) claims",
                                        flags[0]).group(1)
                self.assertEqual(claimed_row, match.group(1))
            else:
                self.assertEqual(flags, [])

    def test_both_outcomes_occur(self):
        outcomes = set()
        gen = LedgerAuditGenerator("running_sum")
        for _ in range(60):
            answer = gen.generate()["final_answer"]
            outcomes.add("clean" if answer.startswith("no errors")
                         else "error")
        self.assertEqual(outcomes, {"clean", "error"})

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = LedgerAuditGenerator("running_sum",
                                          tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            LedgerAuditGenerator("bogus")
        with self.assertRaises(ValueError):
            LedgerAuditGenerator(tier="dz")


if __name__ == "__main__":
    unittest.main()
