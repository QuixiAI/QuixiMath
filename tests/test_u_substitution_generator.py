import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.u_substitution_generator import USubstitutionGenerator
from helpers import DELIM


def to_py(expr):
    s = expr.replace("+ C", "").strip()
    s = re.sub(r"e\^\(([^)]*(?:\([^)]*\))?[^)]*)\)",
               lambda m: f"math.exp({m.group(1)})", s)
    s = s.replace("ln(abs(", "math.log(abs(")
    s = s.replace("^", "**")
    for _ in range(3):
        s = re.sub(r"(\d)x", r"\1*x", s)
        s = re.sub(r"(\d)\(", r"\1*(", s)
        s = re.sub(r"\)\(", ")*(", s)
        s = re.sub(r"x\(", "x*(", s)
        s = re.sub(r"x e", "x*e", s)
        s = re.sub(r"x ?math", "x*math", s)
        s = re.sub(r"(\d) ?math", r"\1*math", s)
        s = re.sub(r"(\d) ?ln", r"\1*ln", s)
    return s


def numeric_check(example):
    m = re.fullmatch(r"Find ∫ (.+) dx\.", example["problem"])
    integrand = to_py(m.group(1))
    F = to_py(example["final_answer"])
    ok = 0
    for x in (0.6, 1.4, 2.2):
        try:
            h = 1e-6
            dF = (eval(F, {"math": math, "x": x + h}) -
                  eval(F, {"math": math, "x": x - h})) / (2 * h)
            want = eval(integrand, {"math": math, "x": x})
        except (ValueError, ZeroDivisionError):
            continue
        if abs(dF - want) / max(1.0, abs(want)) > 1e-3:
            return False
        ok += 1
    return ok >= 2


class TestUSubstitutionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = USubstitutionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_derivative_recovers_integrand(self):
        """A9 oracle: d/dx F equals the integrand numerically."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertTrue(numeric_check(result),
                            (result["problem"], result["final_answer"]))

    def test_du_bookkeeping_present(self):
        for _ in range(200):
            result = self.gen.generate()
            subs = [s for s in result["steps"]
                    if s.startswith(f"SUBST{DELIM}u{DELIM}")]
            self.assertGreaterEqual(len(subs), 2)  # in and back out
            self.assertIn("du", subs[0], subs[0])

    def test_plus_c_always_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(result["final_answer"].endswith("+ C"))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            USubstitutionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
