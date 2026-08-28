import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hypothesis_test_generator import HypothesisTestGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def num(pattern, text):
    return Fraction(re.search(pattern, text).group(1).rstrip("."))


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    if "one-proportion z-test" in p:
        n = int(num(r"sample of size (\d+)", p))
        x = int(num(r"has (\d+) successes", p))
        se = Fraction(1, 2) / math.isqrt(n)
        stat = (Fraction(x, n) - Fraction(1, 2)) / se
    elif "known-σ" in p:
        mu0 = num(r"H0: μ = (\d+)", p)
        n = int(num(r"sample of size (\d+)", p))
        xbar = num(r"mean x̄ = (-?\d+)", p)
        sigma = num(r"population standard deviation σ = ([\d.]+)", p)
        stat = (xbar - mu0) / (sigma / math.isqrt(n))
    else:
        mu0 = num(r"H0: μ = (\d+)", p)
        n = int(num(r"sample of size (\d+)", p))
        xbar = num(r"x̄ = (-?\d+)", p)
        s = num(r"(?:deviation )?s = ([\d.]+)", p)
        se = s / math.isqrt(n)
        stat = (xbar - mu0) / se
    if "what is the test statistic" in p.lower():
        return ans == dec(stat)
    if "supplied left-tail critical" in p:
        crit = num(r"left-tail critical value ([\d.]+)", p)
        want = "reject H0" if stat < -crit else "fail to reject H0"
    elif "supplied right-tail critical" in p:
        crit = num(r"right-tail critical value ([\d.]+)", p)
        want = "reject H0" if stat > crit else "fail to reject H0"
    else:
        crit = num(r"critical value of ([\d.]+)", p)
        want = "reject H0" if abs(stat) > crit else "fail to reject H0"
    return ans.split(" (")[0] == want


class TestHypothesisTestGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HypothesisTestGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute statistic and decision from the text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_critical_value_in_problem(self):
        """Principle 5: the critical value is always supplied."""
        decision_variants = ("prop_z_decision", "t_decision",
                             "one_sided_left", "one_sided_right",
                             "z_mean_decision")
        for variant in decision_variants:
            generator = HypothesisTestGenerator(variant)
            for _ in range(100):
                result = generator.generate()
                self.assertRegex(result["problem"], r"critical value(?: of)? [\d.]+")

    def test_both_decisions_occur(self):
        for v in ("prop_z_decision", "t_decision", "one_sided_left",
                  "one_sided_right", "z_mean_decision"):
            gen = HypothesisTestGenerator(v)
            verdicts = {gen.generate()["final_answer"] for _ in range(300)}
            heads = {v.split(" (")[0] for v in verdicts}
            self.assertIn("reject H0", heads)
            self.assertIn("fail to reject H0", heads)

    def test_stat_formula_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"TEST_STAT_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_arithmetic_and_supplied_lookups(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result))
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "LOOKUP_SUPPLIED":
                    self.assertIn(fields[2], result["problem"])

    def test_one_sided_hypotheses_and_alpha_labels(self):
        for variant, relation, tail in (("one_sided_left", "<", "left"),
                                        ("one_sided_right", ">", "right")):
            generator = HypothesisTestGenerator(variant)
            seen_alpha = set()
            for _ in range(300):
                result = generator.generate()
                self.assertRegex(result["problem"], rf"Ha: μ {relation} \d+")
                self.assertIn(f"{tail}-tail critical", result["problem"])
                seen_alpha.add(re.search(r"At α = (0\.\d+)",
                                         result["problem"]).group(1))
            self.assertEqual(seen_alpha, {"0.10", "0.05", "0.01"})

    def test_known_sigma_variants_use_population_sigma(self):
        for variant in ("z_mean_stat", "z_mean_decision"):
            generator = HypothesisTestGenerator(variant)
            for _ in range(250):
                result = generator.generate()
                self.assertIn("known-σ one-sample z-test", result["problem"])
                self.assertIn("population standard deviation σ", result["problem"])
                self.assertTrue(oracle_check(result))

    def test_four_phrasings_reachable_for_every_variant(self):
        def framing(problem):
            return next(prefix for prefix in ("In ", "At ", "For ", "During ")
                        if problem.startswith(prefix))

        for variant in HypothesisTestGenerator.VARIANTS:
            generator = HypothesisTestGenerator(variant)
            seen = {framing(generator.generate()["problem"]) for _ in range(350)}
            self.assertEqual(seen, {"In ", "At ", "For ", "During "})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 8)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            HypothesisTestGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
