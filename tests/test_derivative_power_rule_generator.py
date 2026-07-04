import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.derivative_power_rule_generator import (
    DerivativePowerRuleGenerator,
    poly_pow,
)
from helpers import DELIM


def parse_terms(txt):
    """'4x^3 - 7x^(-2) + 5' -> [(4, 3), (-7, -2), (5, 0)]."""
    terms = []
    for sign, coef, has_x, power in re.findall(
            r"([+-]?) ?(\d*)(x)?(?:\^\(?(-?\d+)\)?)?(?= |$)", txt):
        if not coef and not has_x:
            continue
        c = int(coef) if coef else 1
        if sign == "-":
            c = -c
        n = int(power) if power else (1 if has_x else 0)
        terms.append((c, n))
    return terms


def oracle_answer(example):
    m = re.fullmatch(r"Differentiate f\(x\) = (.+)\.",
                     example["problem"])
    terms = parse_terms(m.group(1))
    dterms = [(c * n, n - 1) for c, n in terms if n != 0]
    return f"f'(x) = {poly_pow(dterms)}"


def value(terms, x):
    return sum(c * x ** n for c, n in terms)


class TestDerivativePowerRuleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DerivativePowerRuleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_numeric_secant_agreement(self):
        """The claimed derivative matches a tiny secant numerically."""
        for _ in range(200):
            result = self.gen.generate()
            f_terms = parse_terms(
                re.fullmatch(r"Differentiate f\(x\) = (.+)\.",
                             result["problem"]).group(1))
            d_terms = parse_terms(
                result["final_answer"].replace("f'(x) = ", ""))
            x, h = 1.7, 1e-7
            secant = (value(f_terms, x + h) - value(f_terms, x)) / h
            self.assertLess(abs(secant - value(d_terms, x)), 1e-4)

    def test_constants_explicitly_zeroed(self):
        gen = DerivativePowerRuleGenerator("polynomial")
        found = False
        for _ in range(200):
            result = gen.generate()
            for s in result["steps"]:
                if "constant rule" in s:
                    found = True
        self.assertTrue(found)

    def test_negative_powers_occur(self):
        gen = DerivativePowerRuleGenerator("negative_power")
        for _ in range(50):
            result = gen.generate()
            self.assertIn("^(-", result["problem"] +
                          result["final_answer"])

    def test_coefficient_products_shown(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DerivativePowerRuleGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
