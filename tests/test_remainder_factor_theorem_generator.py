import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.remainder_factor_theorem_generator import (
    RemainderFactorTheoremGenerator,
)
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_answer(example):
    """Independently applies the theorems from the problem text."""
    p = example["problem"]
    m = re.fullmatch(
        r"Find the remainder when P\(x\) = (.+) is divided by "
        r"\(?(x [+-] \d+)\)?\.", p) or re.fullmatch(
        r"Find the remainder when P\(x\) = (.+) is divided by (.+)\.", p)
    if m:
        coefs = parse_poly(m.group(1), "x")
        d = parse_poly(m.group(2), "x")
        r = -d.get(0, 0)
        return str(poly_value(coefs, r))
    m = re.fullmatch(r"Is (.+) a factor of P\(x\) = (.+)\?", p)
    if m:
        d = parse_poly(m.group(1), "x")
        coefs = parse_poly(m.group(2), "x")
        return "Yes" if poly_value(coefs, -d.get(0, 0)) == 0 else "No"
    m = re.fullmatch(r"Find k so that (.+) is a factor of "
                     r"P\(x\) = (.+) k\.", p)
    assert m, p
    d = parse_poly(m.group(1), "x")
    r = -d.get(0, 0)
    body = m.group(2).rstrip("+- ")
    sign = 1 if m.group(2).rstrip().endswith("+") else -1
    assert sign == 1, p  # constant is always '+ k' by construction
    coefs = parse_poly(body, "x")
    return f"k = {-poly_value(coefs, r)}"


class TestRemainderFactorTheoremGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RemainderFactorTheoremGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute each theorem application."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_theorem_stated_first(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(result["steps"][0].startswith(f"THEOREM{DELIM}"))

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1].strip("()")) ** int(f[2]),
                                     int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_factor_check_yes_and_no_occur(self):
        gen = RemainderFactorTheoremGenerator("factor_check")
        answers = set()
        for _ in range(100):
            result = gen.generate()
            answers.add(result["final_answer"])
            ev = next(s for s in result["steps"]
                      if s.startswith(f"EVAL{DELIM}"))
            val = int(ev.split(DELIM)[2])
            self.assertEqual(result["final_answer"],
                             "Yes" if val == 0 else "No")
        self.assertEqual(answers, {"Yes", "No"})

    def test_find_k_verifies(self):
        """Substituting the found k makes P(r) exactly zero."""
        gen = RemainderFactorTheoremGenerator("find_k")
        for _ in range(200):
            result = gen.generate()
            m = re.fullmatch(r"Find k so that (.+) is a factor of "
                             r"P\(x\) = (.+) \+ k\.", result["problem"])
            self.assertIsNotNone(m, result["problem"])
            d = parse_poly(m.group(1), "x")
            r = -d.get(0, 0)
            coefs = parse_poly(m.group(2), "x")
            k = int(result["final_answer"].replace("k = ", ""))
            self.assertEqual(poly_value(coefs, r) + k, 0)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"remainder_theorem", "factor_theorem_check",
                               "factor_theorem_find_k"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            RemainderFactorTheoremGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
