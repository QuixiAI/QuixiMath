import os
import random
import re
import sys
import unittest
from collections import Counter

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rational_expr_mult_div_generator import (
    RationalExprMultDivGenerator,
)
from generators.factor_trinomial_generator import binomial
from helpers import DELIM


def trinomial_constants(s, var):
    """'x^2 + 5x + 6' -> the two binomial constants {2, 3}."""
    m = re.fullmatch(rf"{var}\^2 ([+-]) (\d*){var} ([+-]) (\d+)", s)
    assert m, s
    b = int(m.group(2) or 1) * (1 if m.group(1) == "+" else -1)
    c = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    for p in range(-100, 101):
        if p != 0 and c % p == 0 and p + c // p == b:
            return Counter([p, c // p])
    raise AssertionError(s)


def bin_constant(s, var):
    m = re.fullmatch(rf"{var} ([+-]) (\d+)", s)
    return int(m.group(2)) * (1 if m.group(1) == "+" else -1)


def oracle_answer(example):
    """Independently factors, multiplies/inverts, and cancels."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if v in expr)
    m = re.fullmatch(
        rf"\((.+)\)/\((.+)\) ([·÷]) \((.+)\)/\((.+)\)", expr)
    assert m, expr
    num1 = trinomial_constants(m.group(1), var)
    den1 = trinomial_constants(m.group(2), var)
    n2 = Counter([bin_constant(m.group(4), var)])
    d2 = Counter([bin_constant(m.group(5), var)])
    if m.group(3) == "÷":
        n2, d2 = d2, n2

    num = num1 + n2
    den = den1 + d2
    common = num & den
    num -= common
    den -= common
    assert sum(num.values()) == 1 and sum(den.values()) == 1, expr
    top = next(iter(num))
    bottom = next(iter(den))
    return f"{binomial(var, top)}/{binomial(var, bottom)}"


class TestRationalExprMultDivGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RationalExprMultDivGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertIn(result["operation"],
                      ("rational_expr_multiply", "rational_expr_divide"))
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: factor, invert if dividing, multiply, cancel."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_divide_has_invert_step(self):
        for _ in range(200):
            result = self.gen.generate()
            has_invert = any(s.startswith(f"I{DELIM}")
                             for s in result["steps"])
            self.assertEqual(has_invert,
                             result["operation"] == "rational_expr_divide")

    def test_two_cancellations(self):
        for _ in range(200):
            result = self.gen.generate()
            cancels = [s for s in result["steps"]
                       if s.startswith(f"CANCEL{DELIM}")]
            self.assertEqual(len(cancels), 2)
            self.assertEqual(cancels[-1].split(DELIM)[2],
                             result["final_answer"])

    def test_both_operations_reachable(self):
        ops = {self.gen.generate()["operation"] for _ in range(60)}
        self.assertEqual(ops, {"rational_expr_multiply",
                               "rational_expr_divide"})

    def test_fixed_operation_constructor(self):
        gen = RationalExprMultDivGenerator("divide")
        for _ in range(10):
            self.assertEqual(gen.generate()["operation"],
                             "rational_expr_divide")
        with self.assertRaises(ValueError):
            RationalExprMultDivGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
