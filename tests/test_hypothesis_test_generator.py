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
    crit = num(r"critical value of ([\d.]+)", p)
    if "z-test" in p:
        n = int(num(r"sample of size (\d+)", p))
        x = int(num(r"has (\d+) successes", p))
        se = Fraction(1, 2) / math.isqrt(n)
        stat = (Fraction(x, n) - Fraction(1, 2)) / se
    else:
        mu0 = num(r"H0: μ = (\d+)", p)
        n = int(num(r"sample of size (\d+)", p))
        xbar = num(r"x̄ = (\d+)", p)
        s = num(r"s = ([\d.]+)", p)
        se = s / math.isqrt(n)
        stat = (xbar - mu0) / se
    if "test statistic" in p:
        return ans == dec(stat)
    want = "reject H0" if abs(stat) > crit else "fail to reject H0"
    ans = ans.split(" (")[0]
    return ans == want


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
        for _ in range(300):
            result = self.gen.generate()
            self.assertRegex(result["problem"], r"critical value of [\d.]+")

    def test_both_decisions_occur(self):
        for v in ("prop_z_decision", "t_decision"):
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            HypothesisTestGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
