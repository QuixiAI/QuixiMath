"""Prompt-only oracle for ArithmeticChainGenerator (depth strand)."""
import random
import re
import unittest
from fractions import Fraction

from generators.arithmetic_chain_generator import ArithmeticChainGenerator
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

def _kind(operation):
    """Rendering family from the operation string (part of the record)."""
    return "money" if "money_chain" in operation else "number"


def _parse_value(txt, kind):
    if kind == "money":
        sign = -1 if txt.startswith("-") else 1
        whole, cents = txt.lstrip("-$").split(".")
        return sign * (int(whole) * 100 + int(cents))
    return Fraction(txt)  # exact for integers and fractions alike


def _render(value, kind):
    if kind == "money":
        sign = "-" if value < 0 else ""
        return f"{sign}${abs(value) // 100}.{abs(value) % 100:02d}"
    fr = Fraction(value)
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


def _apply_op(value, phrase, kind):
    """Re-execute one textual instruction, independently of the generator."""
    if phrase == "double it":
        return value * 2
    if phrase == "halve it":
        if kind == "money":
            assert value % 2 == 0, phrase
            return value // 2
        return Fraction(value) / 2  # exact; never guesses parity
    verb, amount_txt = phrase.split(" ", 1)
    amount = _parse_value(amount_txt, kind)
    if verb in ("add", "receive"):
        return value + amount
    assert verb in ("subtract", "pay"), phrase
    return value - amount


_OP_PHRASE = re.compile(
    r"(?:add|subtract|receive|pay)\s+-?\$?\d+(?:[./]\d+)?|double it|halve it")
_START = re.compile(
    r"(?:Start with|begins at|Beginning from|Take|starts at|"
    r"Starting from a balance of|opens at)\s+(-?\$?\d+(?:[./]\d+)?)")


def _instructions(problem):
    """Every op phrase, in order — grammar-driven, template-independent.

    The instruction grammar has exactly six shapes, so extracting them
    directly is robust to any template's punctuation (colons, parens,
    money amounts containing periods).
    """
    return _OP_PHRASE.findall(problem)


def oracle_answer(example):
    problem = example["problem"]
    kind = _kind(example["operation"])
    phrases = _instructions(problem)
    if example["operation"].startswith("arithmetic_chain_missing_start"):
        end_txt = (re.search(r"(?:result is|final value is|into|produced)\s+"
                             r"(-?\$?\d+(?:[./]\d+)?)", problem).group(1))
        value = _parse_value(end_txt, kind)
        for phrase in reversed(phrases):
            if phrase == "double it":
                value = Fraction(value) / 2
            elif phrase == "halve it":
                value *= 2
            else:
                verb, amount_txt = phrase.split(" ", 1)
                amount = _parse_value(amount_txt, kind)
                value = value - amount if verb == "add" else value + amount
        return _render(value, kind)
    value = _parse_value(_START.search(problem).group(1), kind)
    for phrase in phrases:
        value = _apply_op(value, phrase, kind)
    return _render(value, kind)


def milestone_values_check(example):
    """Re-simulate and verify every MILESTONE against its stated invariant."""
    op = example["operation"]
    problem = example["problem"]
    if op.startswith("arithmetic_chain_missing_start"):
        return True  # backward chain checked via oracle_answer already
    kind = _kind(op)
    value = _parse_value(_START.search(problem).group(1), kind)
    phrases = _instructions(problem)
    values = [value]
    for phrase in phrases:
        value = _apply_op(value, phrase, kind)
        values.append(value)
    for raw in example["steps"]:
        fields = raw.split(DELIM)
        if fields[0] != "MILESTONE":
            continue
        k = int(fields[1])
        state = values[k]
        if op.startswith("arithmetic_chain_fraction_chain"):
            expected = (Fraction(state) * 12).numerator % 9
        else:
            expected = int(state) % 9
        if str(expected) != fields[3]:
            return False
    return True


class TestArithmeticChainGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ArithmeticChainGenerator()

    def test_output_contract_and_depth(self):
        for _ in range(30):
            result = self.gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            tier = result["operation"].rsplit("_", 1)[1]
            self.assertGreaterEqual(chain_depth(result["steps"]),
                                    TIER_FLOORS[tier])
            self.assertFalse(milestone_violations(result["steps"]))
            self.assertLessEqual(record_chars(result), 16_000)
            self.assertEqual(parse_count(result["problem"]),
                             chain_depth(result["steps"]))

    def test_oracle_recomputes_from_problem_text(self):
        for variant in ArithmeticChainGenerator.VARIANTS:
            gen = ArithmeticChainGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:200])

    def test_milestone_values_are_honest(self):
        for variant in ("integer_chain", "fraction_chain", "money_chain"):
            gen = ArithmeticChainGenerator(variant, tier="d100")
            for _ in range(25):
                result = gen.generate()
                self.assertTrue(milestone_values_check(result))
                self.assertTrue(any(s.startswith("MILESTONE")
                                    for s in result["steps"]))

    def test_d50_is_plain_and_deeper_tiers_checkpointed(self):
        plain = ArithmeticChainGenerator("integer_chain", tier="d50").generate()
        self.assertFalse(any(s.startswith("MILESTONE") for s in plain["steps"]))
        deep = ArithmeticChainGenerator("integer_chain", tier="d200").generate()
        self.assertTrue(any(s.startswith("MILESTONE") for s in deep["steps"]))

    def test_bounded_intermediates(self):
        gen = ArithmeticChainGenerator("integer_chain", tier="d200")
        for _ in range(10):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] in ("A", "S", "M", "D"):
                    self.assertTrue(10 < int(fields[-1]) < 500, raw)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 2), ("d100", 3), ("d200", 4)):
            result = ArithmeticChainGenerator("integer_chain",
                                              tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(300):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 12)  # 4 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            ArithmeticChainGenerator("bogus")
        with self.assertRaises(ValueError):
            ArithmeticChainGenerator(tier="d999")


if __name__ == "__main__":
    unittest.main()
