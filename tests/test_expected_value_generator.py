import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.expected_value_generator import (
    ExpectedValueGenerator, signed_money,
)
from generators.exponential_model_generator import dec
from helpers import DELIM


def oracle_check(example):
    p = example["problem"]
    ans = example["final_answer"]
    m = re.search(r"Find E\[X\]", p)
    if m:
        pairs = re.findall(r"P\(X=(-?\d+)\) = (\S+?)[;.]", p)
        E = sum(int(x) * Fraction(pr) for x, pr in pairs)
        return ans == dec(E)
    m = re.search(r"Find Var\(X\)", p)
    if m:
        pairs = re.findall(r"P\(X=(-?\d+)\) = (\S+?)[;\s]", p)
        xs = [int(x) for x, _ in pairs]
        ps = [Fraction(pr) for _, pr in pairs]
        mu = sum(x * pp for x, pp in zip(xs, ps))
        var = sum(pp * (x - mu) ** 2 for x, pp in zip(xs, ps))
        return ans == dec(var)
    m = re.search(r"expected value of the game", p)
    if m:
        outs = re.findall(r"(win|lose) \$(\d+) with probability (\S+?)[,.]",
                          p)
        E = sum((1 if w == "win" else -1) * int(v) * Fraction(pr)
                for w, v, pr in outs)
        return ans == signed_money(E)
    m = re.search(r"A game costs \$(\d+) to play", p)
    assert m, p
    cost = int(m.group(1))
    outs = re.findall(r"win \$(\d+) with probability (\S+?)[,.]", p)
    E = sum(int(v) * Fraction(pr) for v, pr in outs)
    net = E - cost
    want = ("fair" if net == 0 else
            "favorable" if net > 0 else "unfavorable")
    return ans == want


class TestExpectedValueGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExpectedValueGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        """A9 oracle: recompute E, Var, or the verdict from the text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_variance_nonnegative(self):
        gen = ExpectedValueGenerator("variance")
        for _ in range(200):
            result = gen.generate()
            self.assertGreaterEqual(Fraction(result["final_answer"]), 0)

    def test_fair_game_verdicts_occur(self):
        gen = ExpectedValueGenerator("fair_game")
        verdicts = {gen.generate()["final_answer"] for _ in range(300)}
        self.assertIn("favorable", verdicts)
        self.assertIn("unfavorable", verdicts)

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
            ExpectedValueGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
