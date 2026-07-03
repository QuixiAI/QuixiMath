import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_grouping_generator import FactorGroupingGenerator
from tests.test_factor_special_forms_generator import (
    expand_answer,
    parse_poly,
    poly_mul,
)
from helpers import DELIM


class TestFactorGroupingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorGroupingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "factor_by_grouping")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_expansion_primitivity_irreducibility(self):
        """A9 oracle: the answer expands to the four-term polynomial, the
        polynomial is primitive, and the quadratic factor has no rational
        roots (the factorization is complete)."""
        for _ in range(400):
            result = self.gen.generate()
            original_txt = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xyn" if v in original_txt)
            original = parse_poly(original_txt, var)
            self.assertEqual(len(original), 4, original_txt)
            expanded = expand_answer(result["final_answer"], var)
            self.assertEqual(expanded, original, result["final_answer"])

            g = 0
            for cf in original.values():
                g = gcd(g, abs(cf))
            self.assertEqual(g, 1, f"hidden GCF in {original_txt}")

            # quadratic factor cx^2 + d must be irreducible over Z:
            # only reducible when c and -d are both perfect squares
            quad = re.findall(r"\(([^)]+)\)", result["final_answer"])[1]
            qp = parse_poly(quad, var)
            c, d = qp.get(2, 0), qp.get(0, 0)
            self.assertGreater(c, 0)
            if d < 0:
                c_root = int(c ** 0.5)
                d_root = int((-d) ** 0.5)
                self.assertFalse(c_root * c_root == c and
                                 d_root * d_root == -d,
                                 f"reducible quadratic: {quad}")

    def test_grouping_arithmetic(self):
        """Each FACTOR_GROUP's gcf × binomial must reproduce its group, and
        both groups must share the same binomial."""
        for _ in range(300):
            result = self.gen.generate()
            original_txt = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xyn" if v in original_txt)
            common = None
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "FACTOR_GROUP":
                    continue
                group, gcf_txt, bino = f[1], f[2], f[3]
                got = parse_poly(group, var)
                expected = poly_mul(parse_poly(gcf_txt, var),
                                    parse_poly(bino.strip("()"), var))
                self.assertEqual(expected, got, s)
                if common is None:
                    common = bino
                else:
                    self.assertEqual(common, bino, s)

    def test_check_expansion_matches(self):
        for _ in range(200):
            result = self.gen.generate()
            original_txt = result["problem"].split(": ", 1)[1]
            var = next(v for v in "xyn" if v in original_txt)
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            f = check.split(DELIM)
            self.assertEqual(parse_poly(f[2], var), parse_poly(f[3], var),
                             check)

    def test_negative_coefficients_appear(self):
        negatives = 0
        for _ in range(100):
            result = self.gen.generate()
            if " - " in result["problem"]:
                negatives += 1
        self.assertGreater(negatives, 30)


if __name__ == "__main__":
    unittest.main()
