"""Prompt-only oracle for BigExactDivisionGenerator (depth strand)."""
import random
import re
import unittest

from generators.big_exact_division_generator import BigExactDivisionGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_FRACTION_FORMS = (re.compile(r"(\d+)/(\d+)"),
                   re.compile(r"[Dd]ivide (\d+) by (\d+)"))


class _Fraction:
    """p and q from either surface form (``p/q`` or ``Divide p by q``)."""

    @staticmethod
    def search(problem):
        for pattern in _FRACTION_FORMS:
            match = pattern.search(problem)
            if match:
                return match
        return None


_FRACTION = _Fraction()


def oracle_answer(example):
    """Big-int divmod / multiplicative order — never the digit algorithm."""
    problem = example["problem"]
    op = example["operation"]
    if op.startswith("big_exact_division_repetend_length"):
        q = int(_FRACTION.search(problem).group(2))
        # Order of 10 mod q via the divisors of q-1 (independent of the
        # generator's step-until-1 loop).
        divisors = sorted(d for k in range(1, int((q - 1) ** 0.5) + 1)
                          if (q - 1) % k == 0
                          for d in {k, (q - 1) // k})
        return str(next(d for d in divisors if pow(10, d, q) == 1))
    dividend_txt = re.search(r"(\d{5,})", problem).group(1)
    divisor = int(re.search(r"by (\d\d)\b|over (\d\d)\b", problem)
                  .group(1) or re.search(r"by (\d\d)\b|over (\d\d)\b",
                                         problem).group(2))
    quotient, remainder = divmod(int(dividend_txt), divisor)
    if op.startswith("big_exact_division_remainder_only"):
        return str(remainder)
    return str(sum(int(c) for c in str(quotient)))


class TestBigExactDivisionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BigExactDivisionGenerator()

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
        for variant in BigExactDivisionGenerator.VARIANTS:
            gen = BigExactDivisionGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:150])

    def test_every_div_step_is_exact(self):
        for variant, modulus_from in (("remainder_only", "divisor"),
                                      ("repetend_length", "q")):
            gen = BigExactDivisionGenerator(variant, tier="d50")
            for _ in range(10):
                result = gen.generate()
                if modulus_from == "divisor":
                    modulus = int(re.search(r"by (\d\d)\b|over (\d\d)\b",
                                            result["problem"]).group(1)
                                  or re.search(r"by (\d\d)\b|over (\d\d)\b",
                                               result["problem"]).group(2))
                else:
                    modulus = int(_FRACTION.search(
                        result["problem"]).group(2))
                for raw in result["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] != "DIV_STEP":
                        continue
                    r_prev = int(fields[1])
                    match = re.fullmatch(r"d=(\d), q=(\d+)", fields[2])
                    digit, q_digit = int(match.group(1)), int(match.group(2))
                    widened = r_prev * 10 + digit
                    self.assertEqual(widened // modulus, q_digit, raw)
                    self.assertEqual(widened % modulus, int(fields[3]), raw)

    def test_repetend_chain_returns_to_start(self):
        gen = BigExactDivisionGenerator("repetend_length", tier="d50")
        for _ in range(10):
            result = gen.generate()
            p = int(_FRACTION.search(result["problem"]).group(1))
            div_steps = [s for s in result["steps"]
                         if s.startswith(f"DIV_STEP{DELIM}")]
            self.assertEqual(int(div_steps[0].split(DELIM)[1]), p)
            self.assertEqual(int(div_steps[-1].split(DELIM)[3]), p)
            self.assertEqual(len(div_steps), int(result["final_answer"]))

    def test_dividend_length_matches_stated_digit_count(self):
        gen = BigExactDivisionGenerator("remainder_only", tier="d100")
        for _ in range(10):
            result = gen.generate()
            stated = int(re.search(r"(\d+) digits",
                                   result["problem"]).group(1))
            dividend = re.search(r"(\d{5,})", result["problem"]).group(1)
            self.assertEqual(len(dividend), stated)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = BigExactDivisionGenerator("remainder_only",
                                               tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            BigExactDivisionGenerator("bogus")
        with self.assertRaises(ValueError):
            BigExactDivisionGenerator(tier="d12")


if __name__ == "__main__":
    unittest.main()
