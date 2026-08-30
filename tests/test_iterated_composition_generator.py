"""Prompt-only oracle for IteratedCompositionGenerator (depth strand)."""
import random
import re
import unittest
from fractions import Fraction

from generators.iterated_composition_generator import (
    IteratedCompositionGenerator)
from helpers import DELIM
from depth_common import TIER_FLOORS
from tests.conventions_common import assert_contract, assert_pipe_safe
from tests.depth_oracle import (chain_depth, milestone_violations,
                                parse_count, record_chars)

_X0 = re.compile(r"x = (-?\d+(?:/\d+)?)")
# Grammar-driven: the five rule strings are a fixed finite set, so find
# them directly (first occurrence = f, second = g) - immune to prose.
_RULE_TOKEN = re.compile(
    r"x -> (?:1 - x|1/x|1/\(1 - x\)|\(x - 1\)/x|x/\(x - 1\))")
_N = re.compile(r"(\d+) (?:applications|alternating applications)")

_MAP_BY_RULE = {
    "x -> 1 - x": lambda x: 1 - x,
    "x -> 1/x": lambda x: 1 / x,
    "x -> 1/(1 - x)": lambda x: 1 / (1 - x),
    "x -> (x - 1)/x": lambda x: (x - 1) / x,
    "x -> x/(x - 1)": lambda x: x / (x - 1),
}


def _txt(fr):
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


def _parse(problem):
    x0 = Fraction(_X0.search(problem).group(1))
    f_rule, g_rule = _RULE_TOKEN.findall(problem)[:2]
    return x0, _MAP_BY_RULE[f_rule], _MAP_BY_RULE[g_rule]


def _walk(x0, f, g, n):
    value = x0
    for k in range(n):
        value = (f if k % 2 == 0 else g)(value)
    return value


def _period(x0, f, g):
    """Via orbit lookup on the h = g.f composition — different route
    than the generator's even-step scan."""
    h = lambda x: g(f(x))
    value, order = h(x0), 1
    while value != x0:
        value = h(value)
        order += 1
    return 2 * order if _walk(x0, f, g, 2 * order) == x0 else None


def oracle_answer(example):
    problem = example["problem"]
    op = example["operation"]
    x0, f, g = _parse(problem)
    if op.startswith("iterated_composition_cycle_length"):
        return str(_period(x0, f, g))
    n = int(_N.search(problem).group(1))
    value = _walk(x0, f, g, n)
    if op.startswith("iterated_composition_shortcut_check"):
        return f"period {_period(x0, f, g)}; value {_txt(value)}"
    return _txt(value)


class TestIteratedCompositionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IteratedCompositionGenerator()

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
        for variant in IteratedCompositionGenerator.VARIANTS:
            gen = IteratedCompositionGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["final_answer"],
                                 oracle_answer(result),
                                 result["problem"][:170])

    def test_every_map_application_is_exact(self):
        gen = IteratedCompositionGenerator("final_value", tier="d100")
        for _ in range(10):
            result = gen.generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] != "MAP_APPLY":
                    continue
                mapping = _MAP_BY_RULE[fields[2]]
                self.assertEqual(mapping(Fraction(fields[1])),
                                 Fraction(fields[3]), raw)

    def test_orbit_values_stay_tiny(self):
        gen = IteratedCompositionGenerator("final_value", tier="d200")
        for _ in range(5):
            result = gen.generate()
            values = {fields[3]
                      for fields in (raw.split(DELIM)
                                     for raw in result["steps"])
                      if fields[0] == "MAP_APPLY"}
            self.assertLessEqual(len(values), 6)  # anharmonic orbit
            for value in values:
                fr = Fraction(value)
                self.assertLess(abs(fr.numerator), 200)
                self.assertLess(fr.denominator, 200)

    def test_shortcut_check_agrees(self):
        gen = IteratedCompositionGenerator("shortcut_check", tier="d50")
        for _ in range(10):
            result = gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            fields = check.split(DELIM)
            lhs = fields[2].rsplit(" ", 1)[-1]
            rhs = fields[3].rsplit(" ", 1)[-1]
            self.assertEqual(lhs, rhs, check)

    def test_tier_difficulty_bump(self):
        for tier, expected in (("d50", 3), ("d100", 4), ("d200", 5)):
            result = IteratedCompositionGenerator("final_value",
                                                  tier=tier).generate()
            self.assertEqual(result["difficulty"], expected)

    def test_all_variants_and_tiers_reachable(self):
        seen = set()
        for _ in range(250):
            seen.add(self.gen.generate()["operation"])
        self.assertEqual(len(seen), 9)  # 3 variants x 3 tiers

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            IteratedCompositionGenerator("bogus")
        with self.assertRaises(ValueError):
            IteratedCompositionGenerator(tier="dd")


if __name__ == "__main__":
    unittest.main()
