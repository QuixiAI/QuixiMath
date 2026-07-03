import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.inverse_function_generator import InverseFunctionGenerator
from helpers import DELIM


def parse_forward(rule):
    """Problem rule -> callable on Fraction."""
    m = re.fullmatch(r"x\^3 ([+-]) (\d+)", rule)
    if m:
        c = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        return lambda x: x ** 3 + c
    m = re.fullmatch(r"\(x ([+-]) (\d+)\)/(\d+)", rule)
    if m:
        b = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        c = int(m.group(3))
        return lambda x: Fraction(x + b, c)
    m = re.fullmatch(r"(-?\d+)x ([+-]) (\d+)", rule)
    assert m, rule
    a = int(m.group(1))
    b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
    return lambda x: a * x + b


def parse_inverse(expr):
    """Answer expression -> callable on Fraction (cube via exact root)."""
    m = re.fullmatch(r"∛\(x ([+-]) (\d+)\)", expr)
    if m:
        c = int(m.group(2)) * (1 if m.group(1) == "+" else -1)

        def cbrt(x):
            r = x + c
            root = round(abs(r) ** (1 / 3)) * (1 if r >= 0 else -1)
            assert root ** 3 == r, (expr, x)
            return Fraction(root)
        return cbrt
    m = re.fullmatch(r"\(x ([+-]) (\d+)\)/\(?(-?\d+)\)?", expr)
    if m:
        b = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        a = int(m.group(3))
        return lambda x: Fraction(x + b, a)
    m = re.fullmatch(r"(-?\d+)x ([+-]) (\d+)", expr)
    assert m, expr
    a = int(m.group(1))
    b = int(m.group(3)) * (1 if m.group(2) == "+" else -1)
    return lambda x: a * x + b


class TestInverseFunctionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = InverseFunctionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "inverse_function")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_round_trip_oracle(self):
        """A9 oracle: f(f⁻¹(s)) = s and f⁻¹(f(t)) = t, exactly."""
        for _ in range(500):
            result = self.gen.generate()
            rule = re.fullmatch(r"Find the inverse of [a-z]\(x\) = (.+)\.",
                                result["problem"]).group(1)
            f = parse_forward(rule)
            inv = parse_inverse(result["final_answer"])
            if "∛" in result["final_answer"]:
                m = re.search(r"x ([+-]) (\d+)", result["final_answer"])
                c = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
                points = [Fraction(-c + u ** 3) for u in (-2, -1, 0, 1, 3)]
            else:
                points = [Fraction(p) for p in (-7, -1, 0, 2, 5, 9)]
            for s in points:
                self.assertEqual(f(inv(s)), s,
                                 (result["problem"],
                                  result["final_answer"], s))
            for t in (Fraction(-3), Fraction(0), Fraction(4)):
                self.assertEqual(inv(f(t)), t, result["problem"])

    def test_method_steps_present_in_order(self):
        """y-rewrite, swap, ..., inverse statement, composition check."""
        for _ in range(300):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertLess(ops.index("REWRITE"), ops.index("SWAP_VARS"))
            self.assertIn("EQ_OP_BOTH", ops)
            self.assertIn("CHECK", ops)
            self.assertLess(ops.index("SWAP_VARS"), ops.index("CHECK"))
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            self.assertEqual(check.split(DELIM)[3], "x", check)
            inv_stmt = [s for s in result["steps"]
                        if s.startswith(f"REWRITE{DELIM}") and "⁻¹" in s]
            self.assertEqual(len(inv_stmt), 1)
            self.assertIn(result["final_answer"], inv_stmt[0])

    def test_swap_actually_swaps(self):
        """The SWAP_VARS equation is the y-rewrite with x and y exchanged."""
        for _ in range(300):
            result = self.gen.generate()
            y_eq = result["steps"][1].split(DELIM)[1]
            swapped = result["steps"][2].split(DELIM)[1]
            expected = y_eq.replace("x", "@").replace("y", "x") \
                .replace("@", "y")
            self.assertEqual(swapped, expected, result["steps"][:3])

    def test_all_variants_reachable(self):
        kinds = set()
        for _ in range(200):
            a = self.gen.generate()["final_answer"]
            kinds.add("cube" if "∛" in a
                      else ("linear" if a.startswith("(") else "divide"))
        self.assertEqual(kinds, {"cube", "linear", "divide"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            InverseFunctionGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
