import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.horner_evaluation_generator import HornerEvaluationGenerator
from tests.test_polynomial_long_division_generator import (
    parse_poly,
    poly_value,
)
from helpers import DELIM


def oracle_answer(example):
    """Evaluates the polynomial directly from the problem text."""
    m = re.fullmatch(
        r"Use Horner's method to evaluate P\(x\) = (.+) at x = (-?\d+)\.",
        example["problem"])
    assert m, example["problem"]
    coefs = parse_poly(m.group(1), "x")
    return str(poly_value(coefs, int(m.group(2))))


class TestHornerEvaluationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HornerEvaluationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: direct polynomial evaluation."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_multiply_add_rhythm(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_nested_form_is_equivalent(self):
        """The REWRITE nested form evaluates to the same value."""
        for _ in range(200):
            result = self.gen.generate()
            r = int(re.search(r"at x = (-?\d+)\.",
                              result["problem"]).group(1))
            nested = result["steps"][1].split(DELIM)[1]
            expr = nested.replace("(x", "(1x").replace("-x", "-1x")
            if expr.startswith("x"):
                expr = "1" + expr
            expr = expr.replace("x", f"*({r})").replace("^", "**")
            self.assertEqual(eval(expr), int(result["final_answer"]),
                             nested)

    def test_check_step_verifies_leading_term(self):
        for _ in range(200):
            result = self.gen.generate()
            chk = next(s for s in result["steps"]
                       if s.startswith(f"CHECK{DELIM}"))
            f = chk.split(DELIM)
            m = re.fullmatch(r"(-?\d+)·\((-?\d+)\)\^(\d+) = (-?\d+)", f[2])
            self.assertIsNotNone(m, chk)
            a, r, d, v = (int(m.group(i)) for i in range(1, 5))
            self.assertEqual(a * r ** d, v, chk)
            self.assertEqual(str(v), f[3], chk)

    def test_degrees_three_and_four_occur(self):
        degs = set()
        for _ in range(100):
            result = self.gen.generate()
            degs.add(4 if "^4" in result["problem"] else 3)
        self.assertEqual(degs, {3, 4})


if __name__ == "__main__":
    unittest.main()
