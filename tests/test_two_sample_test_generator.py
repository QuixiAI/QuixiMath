import math
import random
import re
import unittest
from fractions import Fraction

from generators.two_sample_test_generator import (
    TWO_SAMPLE_SE_BANK, TwoSampleTestGenerator,
)
from helpers import DELIM
from tests.new_generator_test_utils import GeneratorTestMixin, oracle_two_sample


class TestTwoSampleTestGenerator(GeneratorTestMixin, unittest.TestCase):
    GEN = TwoSampleTestGenerator
    ORACLE = staticmethod(oracle_two_sample)
    VARIANTS = TwoSampleTestGenerator.VARIANTS
    OP_PREFIX = "two_sample_test"

    def setUp(self):
        random.seed(42)
        super().setUp()

    def test_arithmetic_steps_recompute_exactly(self):
        for variant in self.VARIANTS:
            generator = self.GEN(variant)
            for _ in range(100):
                result = generator.generate()
                for raw in result["steps"]:
                    fields = raw.split(DELIM)
                    if fields[0] == "A":
                        self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "S":
                        self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "M":
                        self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "D":
                        self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "E":
                        self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                         Fraction(fields[3]), raw)
                    elif fields[0] == "ROOT" and len(fields) == 4:
                        self.assertEqual(Fraction(fields[3]) ** int(fields[2]),
                                         Fraction(fields[1]), raw)
                    elif fields[0] == "MIN":
                        candidates = [Fraction(x) for x in fields[1].split(",")]
                        self.assertEqual(min(candidates), Fraction(fields[2]), raw)

    def test_original_t_cases_draw_from_shared_bank(self):
        bank = {(s1, n1, s2, n2) for s1, n1, s2, n2, _ in TWO_SAMPLE_SE_BANK}
        seen = set()
        generator = self.GEN("t_stat")
        for _ in range(300):
            problem = generator.generate()["problem"]
            n1, _, s1, n2, _, s2 = map(int, re.search(
                r"n1=(\d+), x̄1=(\d+), s1=(\d+); sample 2 has "
                r"n2=(\d+), x̄2=(\d+), s2=(\d+)", problem).groups())
            seen.add((s1, n1, s2, n2))
        self.assertGreater(len(seen), 1)
        self.assertLessEqual(seen, bank)

    def test_pooled_df_critical_value_and_both_decisions(self):
        generator = self.GEN("t_pooled_decision")
        verdicts = set()
        for _ in range(500):
            result = generator.generate()
            problem = result["problem"]
            n1, n2 = map(int, re.search(r"n1=(\d+).+n2=(\d+)", problem).groups())
            df = int(re.search(r"df = (\d+)", problem).group(1))
            self.assertEqual(df, n1 + n2 - 2)
            lookup = next(s.split(DELIM) for s in result["steps"]
                          if s.startswith(f"LOOKUP_SUPPLIED{DELIM}"))
            self.assertIn(f"df = {df}", lookup[1])
            self.assertIn(lookup[2], problem)
            verdicts.add(result["final_answer"].split(" (")[0])
        self.assertEqual(verdicts, {"reject H0", "fail to reject H0"})

    def test_welch_uses_conservative_df_rule(self):
        generator = self.GEN("t_welch_stat")
        for _ in range(200):
            result = generator.generate()
            n1, n2 = map(int, re.search(r"n1=(\d+).+n2=(\d+)",
                                        result["problem"]).groups())
            df = min(n1 - 1, n2 - 1)
            self.assertIn(
                "RULE|conservative df|df = min(n1 − 1, n2 − 1)",
                result["steps"])
            self.assertIn(f"MIN|{n1 - 1},{n2 - 1}|{df}", result["steps"])
            self.assertTrue(result["final_answer"].endswith(f"df = {df}"))

    def test_unequal_proportion_cases_are_exact_and_unequal(self):
        generator = self.GEN("prop_z_unequal_n")
        pooled_seen = set()
        for _ in range(300):
            result = generator.generate()
            n1, x1, n2, x2 = map(int, re.search(
                r"n1=(\d+), x1=(\d+); sample 2 has n2=(\d+), x2=(\d+)",
                result["problem"]).groups())
            self.assertNotEqual(n1, n2)
            pooled = Fraction(x1 + x2, n1 + n2)
            self.assertIn(pooled, (Fraction(1, 5), Fraction(1, 2),
                                   Fraction(4, 5)))
            pooled_seen.add(pooled)
            self.assertEqual(result["final_answer"], oracle_two_sample(result))
        self.assertEqual(pooled_seen, {Fraction(1, 5), Fraction(1, 2),
                                      Fraction(4, 5)})

    def test_every_variant_has_formula_and_oracle_coverage(self):
        for variant in self.VARIANTS:
            generator = self.GEN(variant)
            for _ in range(50):
                result = generator.generate()
                self.assertTrue(any(s.startswith(f"TEST_STAT_FORMULA{DELIM}")
                                    for s in result["steps"]))
                self.assertEqual(result["final_answer"], oracle_two_sample(result))


if __name__ == "__main__":
    unittest.main()
