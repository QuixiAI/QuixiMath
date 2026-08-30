"""Prompt-only oracle for CompoundLedgerGenerator (depth strand)."""
import random
import re
import unittest

from generators.compound_ledger_generator import CompoundLedgerGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_START = re.compile(
    r"(?:opens at|starts at|Starting from|statement at) (\$\d+\.\d\d)")
_RATE = re.compile(r"(\d+)% of the whole-dollar")


def _cents(txt):
    sign = -1 if txt.startswith("-") else 1
    whole, cents = txt.lstrip("-$").split(".")
    return sign * (int(whole) * 100 + int(cents))


def _money(cents):
    sign = "-" if cents < 0 else ""
    return f"{sign}${abs(cents) // 100}.{abs(cents) % 100:02d}"


def _event_list(problem):
    """The '; '-separated events between 'in order' and the sentence end.

    Event phrases never contain '(', ')' or '. ' (dollar periods sit
    between digits), so the list ends at the first of either.
    """
    tail = problem.split("in order", 1)[1]
    tail = tail.lstrip(":( ")
    for boundary in (". ", ")"):
        cut = tail.find(boundary)
        if cut != -1:
            tail = tail[:cut]
    phrases = [p.strip() for p in tail.split(";")]
    for phrase in phrases:
        assert re.fullmatch(r"deposit \$\d+\.\d\d|withdraw \$\d+\.\d\d|"
                            r"interest", phrase), phrase
    return phrases


def oracle_answer(example):
    problem = example["problem"]
    start = _cents(_START.search(problem).group(1))
    rate = int(_RATE.search(problem).group(1))
    balance, interest_total = start, 0
    first_negative = None
    for index, phrase in enumerate(_event_list(problem), start=1):
        if phrase == "interest":
            credit = rate * (max(balance, 0) // 100)
            interest_total += credit
            balance += credit
        else:
            amount = _cents(phrase.split(" ", 1)[1])
            balance += amount if phrase.startswith("deposit") else -amount
        if first_negative is None and balance < 0:
            first_negative = (index, balance)
    op = example["operation"]
    if op.startswith("compound_ledger_interest_earned"):
        return _money(interest_total)
    if op.startswith("compound_ledger_first_negative"):
        return (f"event {first_negative[0]}; "
                f"balance {_money(first_negative[1])}")
    return _money(balance)  # final_balance and statement_check


class TestCompoundLedgerGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CompoundLedgerGenerator()

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
        for variant in CompoundLedgerGenerator.VARIANTS:
            gen = CompoundLedgerGenerator(variant)
            for _ in range(20):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:160])

    def test_interest_steps_are_exact_floors(self):
        gen = CompoundLedgerGenerator("interest_earned", tier="d100")
        for _ in range(10):
            result = gen.generate()
            rate = int(_RATE.search(result["problem"]).group(1))
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "INTEREST":
                    continue
                balance = _cents(fields[1])
                match = re.fullmatch(r"(\d+)% of \$(\d+) = (\d+) cents",
                                     fields[2])
                self.assertEqual(int(match.group(1)), rate, raw)
                self.assertEqual(int(match.group(2)),
                                 max(balance, 0) // 100, raw)
                credit = int(match.group(3))
                self.assertEqual(credit, rate * (max(balance, 0) // 100), raw)
                self.assertEqual(_cents(fields[3]), balance + credit, raw)

    def test_statement_check_reconciles(self):
        gen = CompoundLedgerGenerator("statement_check", tier="d50")
        for _ in range(10):
            result = gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            self.assertEqual(check.split(DELIM)[3], result["final_answer"])

    def test_first_negative_lands_late(self):
        gen = CompoundLedgerGenerator("first_negative", tier="d100")
        for _ in range(10):
            result = gen.generate()
            n = parse_count(result["problem"])
            index = int(re.match(r"event (\d+);",
                                 result["final_answer"]).group(1))
            self.assertGreaterEqual(index, (3 * n) // 4)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = CompoundLedgerGenerator("final_balance",
                                             tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 12)  # 4 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            CompoundLedgerGenerator("bogus")
        with self.assertRaises(ValueError):
            CompoundLedgerGenerator(tier="deep")


if __name__ == "__main__":
    unittest.main()
