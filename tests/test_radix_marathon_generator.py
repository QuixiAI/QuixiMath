"""Prompt-only oracle for RadixMarathonGenerator (depth strand)."""
import random
import re
import unittest

from generators.radix_marathon_generator import (RadixMarathonGenerator,
                                                 VARIANT_TIERS)
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_DIGITS = "0123456789ABCDEF"


def _last_base(problem):
    match = re.search(r"last base, (\d+)", problem)
    if match:
        return int(match.group(1))
    return int(re.findall(r"base[- ](\d+)", problem)[-1])


def _to_base_greedy(value, base):
    """Greedy top-down conversion — a different route than divmod."""
    if value == 0:
        return "0"
    power = 1
    while power * base <= value:
        power *= base
    out = []
    while power:
        digit, value = divmod(value, power)
        out.append(_DIGITS[digit])
        power //= base
    return "".join(out)


def oracle_answer(example):
    problem = example["problem"]
    v = int(re.search(r"(\d{9})", problem).group(1))
    base = _last_base(problem)
    return f"{_to_base_greedy(v, base)} (base {base})"


class TestRadixMarathonGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RadixMarathonGenerator()

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
        for variant in RadixMarathonGenerator.VARIANTS:
            gen = RadixMarathonGenerator(variant)
            for _ in range(25):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:160])

    def test_every_radix_and_horner_step_is_exact(self):
        gen = RadixMarathonGenerator("base_tour", tier="d100")
        for _ in range(10):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "RADIX_STEP":
                    match = re.fullmatch(r"div (\d+) rem (.)", fields[2])
                    base = int(match.group(1))
                    digit = _DIGITS.index(match.group(2))
                    self.assertEqual(int(fields[3]) * base + digit,
                                     int(fields[1]), raw)
                    self.assertLess(digit, base, raw)
                elif fields[0] == "HORNER":
                    match = re.fullmatch(r"x (\d+) \+ (.)", fields[2])
                    base = int(match.group(1))
                    digit = _DIGITS.index(match.group(2))
                    self.assertEqual(int(fields[1]) * base + digit,
                                     int(fields[3]), raw)

    def test_round_trip_check_step_agrees(self):
        gen = RadixMarathonGenerator("round_trip_check")
        for _ in range(10):
            result = gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            fields = check.split(DELIM)
            self.assertEqual(fields[2], fields[3], check)
            v = int(re.search(r"(\d{9})", result["problem"]).group(1))
            self.assertEqual(int(fields[2]), v)

    def test_values_never_exceed_the_start(self):
        gen = RadixMarathonGenerator("base_tour", tier="d200")
        for _ in range(5):
            result = gen.generate()
            v = int(re.search(r"(\d{9})", result["problem"]).group(1))
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] in ("RADIX_STEP", "HORNER"):
                    self.assertLessEqual(int(fields[3]), v, raw)

    def test_variant_tier_latitude(self):
        with self.assertRaises(ValueError):
            RadixMarathonGenerator("round_trip_check", tier="d200")
        with self.assertRaises(ValueError):
            RadixMarathonGenerator("chain_two", tier="d200")
        seen = set()
        for _ in range(400):
            seen.add(self.gen.generate()["operation"])
        expected = {f"radix_marathon_{v}_{t}"
                    for v, tiers in VARIANT_TIERS.items() for t in tiers}
        self.assertEqual(seen, expected)  # 1 + 2 + 3 = 6 operations

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = RadixMarathonGenerator("base_tour",
                                            tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            RadixMarathonGenerator("bogus")
        with self.assertRaises(ValueError):
            RadixMarathonGenerator(tier="d75")


if __name__ == "__main__":
    unittest.main()
