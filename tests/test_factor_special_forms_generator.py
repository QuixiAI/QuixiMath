import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_special_forms_generator import FactorSpecialFormsGenerator
from helpers import DELIM


def parse_poly(s, var=None):
    """Polynomial string -> {multivariate monomial: coefficient}."""
    out = {}
    for part in s.replace(" - ", " + -").split(" + "):
        part = part.strip()
        m = re.fullmatch(r"(-?\d*)((?:[a-z](?:\^\d+)?)*)", part)
        assert m and part, (s, part)
        raw_coefficient, variables = m.groups()
        if raw_coefficient == "":
            coefficient = 1
        elif raw_coefficient == "-":
            coefficient = -1
        else:
            coefficient = int(raw_coefficient)
        powers = {}
        for variable, power in re.findall(r"([a-z])(?:\^(\d+))?", variables):
            powers[variable] = powers.get(variable, 0) + int(power or 1)
        monomial = tuple(sorted(powers.items()))
        out[monomial] = out.get(monomial, 0) + coefficient
    out = {monomial: coefficient for monomial, coefficient in out.items()
           if coefficient != 0}
    if var is None:
        return out
    converted = {}
    for monomial, coefficient in out.items():
        assert all(variable == var for variable, _ in monomial), (s, var)
        power = sum(power for _, power in monomial)
        converted[power] = coefficient
    return converted


def poly_mul(p1, p2):
    if all(isinstance(key, int) for key in p1) and \
            all(isinstance(key, int) for key in p2):
        out = {}
        for power1, coefficient1 in p1.items():
            for power2, coefficient2 in p2.items():
                power = power1 + power2
                out[power] = (out.get(power, 0)
                              + coefficient1 * coefficient2)
        return {power: coefficient for power, coefficient in out.items()
                if coefficient != 0}
    out = {}
    for monomial1, coefficient1 in p1.items():
        for monomial2, coefficient2 in p2.items():
            powers = dict(monomial1)
            for variable, power in monomial2:
                powers[variable] = powers.get(variable, 0) + power
            monomial = tuple(sorted(powers.items()))
            out[monomial] = (out.get(monomial, 0)
                             + coefficient1 * coefficient2)
    return {monomial: coefficient
            for monomial, coefficient in out.items() if coefficient != 0}


def expand_answer(ans, var=None):
    """Expand the printed one- or two-variable factorization exactly."""
    factors = re.findall(r"\(([^)]+)\)(?:\^(\d+))?", ans)
    assert factors, ans
    result = {0: 1} if var is not None else {(): 1}
    for inner, exp in factors:
        p = parse_poly(inner, var)
        for _ in range(int(exp) if exp else 1):
            result = poly_mul(result, p)
    return result


PROBLEM_PATTERNS = (
    r"Factor: (?P<poly>.+)",
    r"Factor completely: (?P<poly>.+)",
    r"Write (?P<poly>.+) in factored form\.",
    r"Rewrite (?P<poly>.+) as a product of factors\.",
    r"Factor the expression (?P<poly>.+) over the integers\.",
    r"[A-Za-z]+ is asked to factor (?P<poly>.+) completely\. Give the "
    r"factored form\.",
    r"[A-Za-z]+ sees (?P<poly>.+) on a worksheet\. Factor it completely\.",
    r"A review sheet gives [A-Za-z]+ the expression (?P<poly>.+)\. "
    r"Factor it\.",
    r"[A-Za-z]+ needs (?P<poly>.+) written as a product\. Factor it "
    r"completely\.",
)


def polynomial_from_problem(problem):
    """Extract the polynomial independently from every public phrasing."""
    for pattern in PROBLEM_PATTERNS:
        match = re.fullmatch(pattern, problem)
        if match:
            return match.group("poly")
    raise AssertionError(f"unparsed problem: {problem!r}")


class TestFactorSpecialFormsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorSpecialFormsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_expansion(self):
        """A9 oracle: the factored answer must expand to the problem
        polynomial exactly, and the roots must be coprime (no hidden GCF)."""
        for _ in range(400):
            result = self.gen.generate()
            original_txt = polynomial_from_problem(result["problem"])
            original = parse_poly(original_txt)
            expanded = expand_answer(result["final_answer"])
            self.assertEqual(expanded, original, result["final_answer"])
            coefs = [abs(c) for c in original.values()]
            g = 0
            for c in coefs:
                g = gcd(g, c)
            self.assertEqual(g, 1, f"hidden GCF in {original_txt}")

    def test_pattern_checks_verified(self):
        """The PST middle-term CHECK and expansion CHECKs must be true."""
        for _ in range(400):
            result = self.gen.generate()
            original_txt = polynomial_from_problem(result["problem"])
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "ROOT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)
                elif f[0] == "CBRT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 3, int(f[1]), s)
                elif f[0] == "CHECK" and f[1] == "middle_term":
                    self.assertEqual(f[2].rsplit("= ", 1)[1], f[3], s)
                elif f[0] == "CHECK" and f[1] in ("foil", "expand"):
                    self.assertEqual(parse_poly(f[2]), parse_poly(f[3]), s)

    def test_all_variants_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(120)}
        self.assertEqual(seen, {"factor_difference_of_squares",
                                "factor_perfect_square",
                                "factor_sum_of_cubes",
                                "factor_difference_of_cubes"})

    def test_pst_signs_both_appear(self):
        gen = FactorSpecialFormsGenerator("perfect_square")
        signs = {"+" if "+ " in gen.generate()["final_answer"] else "-"
                 for _ in range(60)}
        self.assertEqual(signs, {"+", "-"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FactorSpecialFormsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
