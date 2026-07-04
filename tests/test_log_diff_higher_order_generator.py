import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.log_diff_higher_order_generator import (
    LogDiffHigherOrderGenerator,
)
from generators.derivative_power_rule_generator import poly_pow
from tests.test_derivative_power_rule_generator import parse_terms
from helpers import DELIM


def oracle_check(example):
    p = example["problem"]
    m = re.fullmatch(r"Use logarithmic differentiation to find y' for "
                     r"y = x\^(?:\((\d)x\)|x)\.", p)
    if m:
        k = int(m.group(1) or 1)

        def f(t):
            return t ** (k * t)
        x, h = 1.31, 1e-6
        secant = (f(x + h) - f(x - h)) / (2 * h)
        claimed = k * f(x) * (math.log(x) + 1)
        want = (f"y' = x^x(ln x + 1)" if k == 1
                else f"y' = {k}·x^({k}x)(ln x + 1)")
        return (example["final_answer"] == want and
                abs(secant - claimed) / max(1, abs(claimed)) < 1e-4)
    m = re.fullmatch(r"Find the (second|third) derivative of "
                     r"f\(x\) = (.+)\.", p)
    assert m, p
    order = 2 if m.group(1) == "second" else 3
    terms = parse_terms(m.group(2))
    for _ in range(order):
        terms = [(c * n, n - 1) for c, n in terms if n != 0]
    marks = chr(39) * order
    return example["final_answer"] == f"f{marks}(x) = {poly_pow(terms)}"


class TestLogDiffHigherOrderGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LogDiffHigherOrderGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_verification(self):
        """A9 oracle: numeric for log-diff, symbolic for higher order."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_log_diff_ritual_order(self):
        gen = LogDiffHigherOrderGenerator("log_diff")
        for _ in range(100):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertLess(ops.index("LOG_BOTH_SIDES"),
                            ops.index("LOG_POWER"))
            self.assertLess(ops.index("LOG_POWER"),
                            ops.index("IMPLICIT_DIFF"))
            self.assertLess(ops.index("IMPLICIT_DIFF"),
                            ops.index("SUBST"))

    def test_higher_order_passes_recorded(self):
        for v, order in (("second", 2), ("third", 3)):
            gen = LogDiffHigherOrderGenerator(v)
            for _ in range(100):
                result = gen.generate()
                rewrites = [s for s in result["steps"]
                            if s.startswith(f"REWRITE{DELIM}f")]
                self.assertEqual(len(rewrites), order)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LogDiffHigherOrderGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
