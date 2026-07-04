import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.curve_analysis_generator import CurveAnalysisGenerator
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def get_f(example):
    m = re.search(r"f\(x\) = (.+?)(?: and| using)", example["problem"] +
                  " using")
    return parse_poly(m.group(1).rstrip("."), "x")


def critical_points(coefs):
    d1 = {p - 1: c * p for p, c in coefs.items() if p >= 1}
    return sorted(t for t in range(-30, 31)
                  if poly_value(d1, t) == 0), d1


def oracle_check(example):
    coefs = get_f(example)
    crits, d1 = critical_points(coefs)
    d2 = {p - 1: c * p for p, c in d1.items() if p >= 1}
    if "classify" in example["problem"]:
        assert len(crits) == 2
        parts = []
        for r in crits:
            v = poly_value(d2, r)
            parts.append(f"local {'max' if v < 0 else 'min'} at x = {r}")
        return example["final_answer"] == "; ".join(parts)
    # inflection: solve f'' = 0
    mid = [t for t in range(-30, 31) if poly_value(d2, t) == 0]
    assert len(mid) == 1
    m = mid[0]
    want = (f"inflection at x = {m}; concave down on (-∞, {m}), "
            f"concave up on ({m}, ∞)")
    return example["final_answer"] == want


class TestCurveAnalysisGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CurveAnalysisGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_verification(self):
        """A9 oracle: recompute critical/inflection structure."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_max_before_min(self):
        """For a positive-leading cubic, the max precedes the min."""
        gen = CurveAnalysisGenerator("critical")
        for _ in range(200):
            result = gen.generate()
            m = re.fullmatch(r"local max at x = (-?\d+); local min at "
                             r"x = (-?\d+)", result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            self.assertLess(int(m.group(1)), int(m.group(2)))

    def test_second_derivative_test_cited(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(
                s.startswith(f"SECOND_DERIV_TEST{DELIM}")
                for s in result["steps"]))

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            CurveAnalysisGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
