import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_exponent_generator import (
    RationalExponentGenerator,
    ROOT_SYM,
    radical_txt,
)
from helpers import DELIM

SYM_TO_N = {v: k for k, v in ROOT_SYM.items()}


def oracle_answer(example):
    """Independently converts / evaluates from the problem text alone."""
    p = example["problem"]
    op = example["operation"]
    expr = p.split(": ", 1)[1]

    if op == "rational_exponent_to_radical":
        m0 = re.fullmatch(r"(\d+)\^\((\d+)/(\d+)\)", expr)
        if m0:  # numeric base: 7^(2/3) -> ∛49
            b, m, n = (int(v) for v in m0.groups())
            assert gcd(m, n) == 1
            return f"{ROOT_SYM[n]}{b ** m}"
        m0 = re.fullmatch(r"([a-z])\^\((\d+)/(\d+)\)", expr)
        var, m, n = m0.group(1), int(m0.group(2)), int(m0.group(3))
        assert gcd(m, n) == 1
        return radical_txt(n, var, m)

    if op == "rational_exponent_from_radical":
        m0 = re.fullmatch(r"([√∛∜])\(?([a-z])(?:\^(\d+))?\)?", expr)
        assert m0, expr
        n = SYM_TO_N[m0.group(1)]
        var = m0.group(2)
        m = int(m0.group(3) or 1)
        g = gcd(m, n)
        mr, nr = m // g, n // g
        if nr == 1:
            return var if mr == 1 else f"{var}^{mr}"
        return f"{var}^({mr}/{nr})"

    m0 = re.fullmatch(r"(\d+)\^\((-?)(\d+)/(\d+)\)", expr)
    assert m0, expr
    base = int(m0.group(1))
    neg = m0.group(2) == "-"
    m, n = int(m0.group(3)), int(m0.group(4))
    k = round(base ** (1 / n))
    assert k ** n == base, expr
    value = k ** m
    return f"1/{value}" if neg else str(value)


class TestRationalExponentGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalExponentGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-derive from the text; exponent fractions in
        answers must be fully reduced."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])
            m = re.search(r"\^\((\d+)/(\d+)\)", result["final_answer"])
            if m:
                self.assertEqual(gcd(int(m.group(1)), int(m.group(2))), 1,
                                 result["final_answer"])

    def test_root_and_power_steps(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "ROOT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 2, int(f[1]), s)
                elif f[0] == "CBRT" and f[1].isdigit():
                    self.assertEqual(int(f[2]) ** 3, int(f[1]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "F":
                    parts = f[1].split("/")
                    a, b = int(parts[0]), int(parts[1])
                    g = gcd(a, b)
                    expected = (f"{a // g}/{b // g}" if b // g > 1
                                else str(a // g))
                    self.assertEqual(f[2], expected, s)

    def test_all_variants_reachable(self):
        ops = {self.gen.generate()["operation"] for _ in range(150)}
        self.assertEqual(ops, {"rational_exponent_to_radical",
                               "rational_exponent_from_radical",
                               "rational_exponent_evaluate"})

    def test_negative_exponents_appear(self):
        gen = RationalExponentGenerator("evaluate")
        answers = [gen.generate()["final_answer"] for _ in range(80)]
        self.assertTrue(any(a.startswith("1/") for a in answers))

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RationalExponentGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
