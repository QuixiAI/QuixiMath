"""Prompt-only oracle for AmortizationScheduleGenerator (depth strand)."""
import random
import re
import unittest

from generators.amortization_schedule_generator import (
    AmortizationScheduleGenerator)
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_MONEY = re.compile(r"\$(\d+)\.(\d\d)")
_RATE = re.compile(r"(\d+)% per period")
_PERIODS = re.compile(r"(?:for|Walk) (\d+) periods|After (\d+) periods")
_EXTRA = re.compile(r"extra \$(\d+)\.(\d\d)(?: toward| principal|,| in)")
_EXTRA_AT = re.compile(r"period (\d+)(?: adds| \(at)|in period (\d+)")


def _cents(match):
    return int(match.group(1)) * 100 + int(match.group(2))


def _parse(problem):
    monies = _MONEY.finditer(problem)
    principal = _cents(next(monies))
    payment = _cents(next(monies))
    return principal, int(_RATE.search(problem).group(1)), payment


def _resimulate(principal, rate, payment, extra_at=None, extra=0,
                stop_at=None):
    balance, interest_total, period = principal, 0, 0
    while balance > 0:
        period += 1
        interest = rate * (balance // 100)
        pay = payment + (extra if extra_at == period else 0)
        pay = min(pay, balance + interest)
        interest_total += interest
        balance -= pay - interest
        if stop_at is not None and period == stop_at:
            break
    return period, interest_total, balance


def _money_txt(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def oracle_answer(example):
    problem = example["problem"]
    op = example["operation"]
    principal, rate, payment = _parse(problem)
    if op.startswith("amortization_schedule_balance_after_k"):
        n = int(next(g for g in _PERIODS.search(problem).groups() if g))
        _, _, balance = _resimulate(principal, rate, payment, stop_at=n)
        return _money_txt(balance)
    extra_at = extra = None
    if op.startswith("amortization_schedule_extra_payment"):
        # the extra amount is the third money figure in every template
        extra = _cents(list(_MONEY.finditer(problem))[2])
        extra_at = int(next(g for g in
                            _EXTRA_AT.search(problem).groups() if g))
    periods, interest_total, _ = _resimulate(
        principal, rate, payment, extra_at=extra_at, extra=extra or 0)
    if op.startswith("amortization_schedule_total_interest"):
        return _money_txt(interest_total)
    return str(periods)


class TestAmortizationScheduleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AmortizationScheduleGenerator()

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
        for variant in AmortizationScheduleGenerator.VARIANTS:
            gen = AmortizationScheduleGenerator(variant)
            for _ in range(20):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:170])

    def test_every_amort_step_is_exact(self):
        gen = AmortizationScheduleGenerator("payoff_period", tier="d100")
        for _ in range(8):
            result = gen.generate()
            _, rate, _ = _parse(result["problem"])
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "AMORT_STEP":
                    continue
                balance = _cents(_MONEY.search(fields[1]))
                middle = re.fullmatch(
                    r"k=(\d+), i=\$(\d+)\.(\d\d), p=\$(\d+)\.(\d\d)",
                    fields[2])
                interest = int(middle.group(2)) * 100 + int(middle.group(3))
                principal_part = (int(middle.group(4)) * 100
                                  + int(middle.group(5)))
                new_balance = _cents(_MONEY.search(fields[3]))
                self.assertEqual(interest, rate * (balance // 100), raw)
                self.assertEqual(new_balance, balance - principal_part, raw)

    def test_schedule_retires_or_truncates_cleanly(self):
        gen = AmortizationScheduleGenerator("payoff_period", tier="d50")
        for _ in range(8):
            result = gen.generate()
            last = [s for s in result["steps"]
                    if s.startswith(f"AMORT_STEP{DELIM}")][-1]
            self.assertTrue(last.endswith(f"{DELIM}$0.00"), last)
        gen = AmortizationScheduleGenerator("balance_after_k", tier="d50")
        for _ in range(8):
            result = gen.generate()
            principal, _, _ = _parse(result["problem"])
            final = _cents(_MONEY.search(result["final_answer"]))
            self.assertGreater(final, 0)
            self.assertLess(final, principal)  # strictly amortizing

    def test_extra_payment_shortens_the_schedule(self):
        gen = AmortizationScheduleGenerator("extra_payment", tier="d100")
        for _ in range(8):
            result = gen.generate()
            principal, rate, payment = _parse(result["problem"])
            baseline, _, _ = _resimulate(principal, rate, payment)
            self.assertLess(int(result["final_answer"]), baseline)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = AmortizationScheduleGenerator("payoff_period",
                                                   tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 12)  # 4 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            AmortizationScheduleGenerator("bogus")
        with self.assertRaises(ValueError):
            AmortizationScheduleGenerator(tier="dxx")


if __name__ == "__main__":
    unittest.main()
