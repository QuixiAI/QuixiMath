"""Prompt-only oracle for PartialSumMarathonGenerator (depth strand)."""
import random
import re
import unittest
from fractions import Fraction

from generators.partial_sum_marathon_generator import (
    PartialSumMarathonGenerator)
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_ARITH = re.compile(
    r"(?:starting at|first term) (\d+)[,)]? (?:with (?:common )?difference|"
    r"difference) (\d+)")
_ARITH_LIST = re.compile(r"(\d+), (\d+), (\d+), \.\.\.")
_TELE = re.compile(r"k = (\d+)")
_N = re.compile(r"(\d+) terms")
_BOUND = re.compile(r"(?:exceeds?|passes|above) (\d+)")


def _arith_params(problem):
    match = _ARITH.search(problem)
    if match:
        a, d = map(int, match.groups())
        return a, d
    first, second, third = map(int, _ARITH_LIST.search(problem).groups())
    assert third - second == second - first
    return first, second - first


def oracle_answer(example):
    problem = example["problem"]
    op = example["operation"]
    if op.startswith("partial_sum_marathon_telescoping"):
        s = int(_TELE.search(problem).group(1))
        n = int(_N.search(problem).group(1))
        total = Fraction(1, s) - Fraction(1, s + n)  # closed form
        return (str(total.numerator) if total.denominator == 1
                else str(total))
    a, d = _arith_params(problem)
    if op.startswith("partial_sum_marathon_first_exceed"):
        bound = int(_BOUND.search(problem).group(1))
        total, k = 0, 0
        while total <= bound:
            total += a + k * d
            k += 1
        return str(k)
    n = int(_N.search(problem).group(1))
    return str(n * (2 * a + (n - 1) * d) // 2)  # Gauss closed form


class TestPartialSumMarathonGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PartialSumMarathonGenerator()

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
        for variant in PartialSumMarathonGenerator.VARIANTS:
            gen = PartialSumMarathonGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:160])

    def test_every_accumulation_is_exact(self):
        for variant in ("arithmetic", "telescoping"):
            gen = PartialSumMarathonGenerator(variant, tier="d100")
            for _ in range(8):
                result = gen.generate()
                for raw in result["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] != "A":
                        continue
                    term_txt = fields[2].split(" = ")[-1]
                    self.assertEqual(
                        Fraction(fields[1]) + Fraction(term_txt),
                        Fraction(fields[3]), raw)

    def test_check_step_agrees_with_the_accumulated_total(self):
        for variant in ("arithmetic", "telescoping", "first_exceed"):
            gen = PartialSumMarathonGenerator(variant, tier="d50")
            for _ in range(8):
                result = gen.generate()
                check = next(s for s in result["steps"]
                             if s.startswith(f"CHECK{DELIM}"))
                fields = check.split(DELIM)
                lhs = fields[2].split(" = ")[-1]
                rhs = fields[3].split(" = ")[-1]
                self.assertEqual(Fraction(lhs), Fraction(rhs), check)

    def test_telescoping_running_sums_stay_small(self):
        gen = PartialSumMarathonGenerator("telescoping", tier="d200")
        for _ in range(5):
            result = gen.generate()
            s = int(_TELE.search(result["problem"]).group(1))
            n = int(_N.search(result["problem"]).group(1))
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    running = Fraction(fields[3])
                    self.assertLessEqual(running.denominator,
                                         s * (s + n), raw)

    def test_first_exceed_crossing_is_at_the_last_term(self):
        gen = PartialSumMarathonGenerator("first_exceed", tier="d50")
        for _ in range(10):
            result = gen.generate()
            bound = int(_BOUND.search(result["problem"]).group(1))
            adds = [s for s in result["steps"]
                    if s.startswith(f"A{DELIM}")]
            self.assertGreater(int(adds[-1].split(DELIM)[3]), bound)
            self.assertLessEqual(int(adds[-2].split(DELIM)[3]), bound)
            self.assertEqual(len(adds), int(result["final_answer"]))

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = PartialSumMarathonGenerator("arithmetic",
                                                 tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            PartialSumMarathonGenerator("bogus")
        with self.assertRaises(ValueError):
            PartialSumMarathonGenerator(tier="dX")


if __name__ == "__main__":
    unittest.main()
