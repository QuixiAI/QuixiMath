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

from generators.binomial_probability_generator import (
    BinomialProbabilityGenerator, exact,
)
from helpers import DELIM


def term(n, i, p):
    return Fraction(math.comb(n, i)) * p ** i * (1 - p) ** (n - i)


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    n = int(re.search(r"n = (\d+)", p).group(1))
    prob = Fraction(re.search(r"p = (\d+/\d+)", p).group(1))
    q = 1 - prob
    m = re.search(r"Find P\(X = (\d+)\)", p)
    if m:
        return ans == exact(term(n, int(m.group(1)), prob))
    m = re.search(r"Find P\(X ≤ (\d+)\)", p)
    if m:
        k = int(m.group(1))
        return ans == exact(sum(term(n, i, prob) for i in range(k + 1)))
    if "at least one success" in p:
        return ans == exact(1 - q ** n)
    if "expected number of successes" in p:
        return ans == exact(n * prob)
    return ans == exact(n * prob * q)


class TestBinomialProbabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BinomialProbabilityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute each binomial quantity exactly."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_probabilities_in_unit_interval(self):
        for v in ("exact_k", "at_most", "at_least_one"):
            gen = BinomialProbabilityGenerator(v)
            for _ in range(100):
                result = gen.generate()
                val = float(Fraction(result["final_answer"]))
                self.assertGreaterEqual(val, 0)
                self.assertLessEqual(val, 1)

    def test_formula_and_ncr_shown(self):
        gen = BinomialProbabilityGenerator("exact_k")
        for _ in range(100):
            result = gen.generate()
            self.assertTrue(any(s.startswith(f"NCR{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"POW{DELIM}")
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
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            BinomialProbabilityGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
