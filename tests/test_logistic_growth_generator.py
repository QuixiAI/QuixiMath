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

from generators.logistic_growth_generator import LogisticGrowthGenerator
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    m = re.fullmatch(r"A population satisfies dP/dt = (\S+)P - (\S+)P\^2 "
                     r"with P\(0\) = (\d+)\. Find lim t→∞ P\.", p)
    if m:
        a, b = Fraction(m.group(1)), Fraction(m.group(2))
        return 0 < int(m.group(3)) < a / b and ans == str(a / b)
    m = re.fullmatch(r"A population satisfies dP/dt = (\S+)P\(1 - "
                     r"P/(\d+)\)\. (.+)", p)
    if m:
        k, L = float(Fraction(m.group(1))), int(m.group(2))
        q = m.group(3)

        def g(P):
            return k * P * (1 - P / L)
        grid = [i * L / 2000 for i in range(2001)]
        if q.startswith("At what value"):
            best = max(grid, key=g)
            return abs(best - float(ans)) <= L / 1000
        if q.startswith("What is the maximum"):
            return abs(max(map(g, grid)) - float(Fraction(ans))) < 1e-6
        mm = re.fullmatch(r"Compute dP/dt when P = (\d+)\.", q)
        P = Fraction(mm.group(1))
        rate = Fraction(m.group(1)) * P * (1 - P / L)
        return ans == dec(rate)
    m = re.fullmatch(r"A logistic population has carrying capacity "
                     r"(\d+), P\(0\) = (\d+), and growth constant "
                     r"k = (\S+)\. Write the particular solution .*", p)
    assert m, p
    L, P0, k = int(m.group(1)), int(m.group(2)), float(Fraction(m.group(3)))
    mm = re.fullmatch(r"P = (\d+)/\(1 \+ (\d*)e\^\(-(\S+)t\)\)", ans)
    if not mm or int(mm.group(1)) != L or float(mm.group(3)) != k:
        return False
    A = int(mm.group(2) or 1)

    def P(t):
        return L / (1 + A * math.exp(-k * t))
    h, t = 1e-6, 0.7
    dP = (P(t + h) - P(t - h)) / (2 * h)
    return (abs(P(0) - P0) < 1e-9 and
            abs(dP - k * P(t) * (1 - P(t) / L)) < 1e-4)


class TestLogisticGrowthGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LogisticGrowthGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: brute-force / exact recomputation per variant."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_theorem_cited_where_used(self):
        for v in ("half_capacity", "max_rate", "solution", "limit"):
            gen = LogisticGrowthGenerator(v)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(any(s.startswith(f"THEOREM{DELIM}")
                                    for s in result["steps"]))

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1P", r"(?<!\d)1e\^", "--", r"\+ -"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LogisticGrowthGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
