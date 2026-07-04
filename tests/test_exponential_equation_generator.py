import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponential_equation_generator import (
    ExponentialEquationGenerator,
)
from helpers import DELIM


def oracle_check(example):
    """Substitutes the claimed x back into the equation, exactly."""
    p = example["problem"]
    ans = example["final_answer"].replace("x = ", "")

    m = re.fullmatch(r"Solve: (\d+) · (\d+)\^\((.+)\) = (\d+)\.", p)
    if m:
        mult, b, exp_txt, rhs = (m.group(1), int(m.group(2)),
                                 m.group(3), int(m.group(4)))
        x = Fraction(ans)
        e = eval_linear(exp_txt, x)
        return int(mult) * b ** e == rhs and e.denominator == 1
    m = re.fullmatch(r"Solve: (\d+)\^\((.+)\) = (\d+)\.", p)
    if m:
        b, exp_txt, rhs = int(m.group(1)), m.group(2), int(m.group(3))
        x = Fraction(ans)
        e = eval_linear(exp_txt, x)
        return e.denominator == 1 and b ** e.numerator == rhs
    m = re.fullmatch(r"Solve: (\d+)\^x = (\d+)\.", p)
    if m:
        B1, B2 = int(m.group(1)), int(m.group(2))
        x = Fraction(ans)
        return abs(x * math.log(B1) - math.log(B2)) < 1e-9
    m = re.fullmatch(r"Solve: (\d+)\^x = (\d+)\. Give the exact answer\.",
                     p)
    if m:
        b, C = int(m.group(1)), int(m.group(2))
        L = math.log(C, b)
        assert abs(L - round(L)) > 1e-9  # must genuinely need logs
        return ans == f"log_{b}({C})"
    m = re.fullmatch(r"Solve: e\^(?:\((\d+)x\)|x) = (\d+)\. Give the "
                     r"exact answer\.", p)
    assert m, p
    a = int(m.group(1) or 1)
    C = int(m.group(2))
    want = f"ln({C})/{a}" if a > 1 else f"ln({C})"
    return ans == want


def eval_linear(exp_txt, x):
    """'3x - 1' at x -> Fraction."""
    m = re.fullmatch(r"(\d*)x(?: ([+-]) (\d+))?", exp_txt)
    assert m, exp_txt
    a = int(m.group(1) or 1)
    c = int(m.group(3) or 0) * (1 if (m.group(2) or "+") == "+" else -1)
    return a * x + c


class TestExponentialEquationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExponentialEquationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_satisfies_equation(self):
        """A9 oracle: substitute the claimed solution back."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)
                elif f[0] == "D" and "/" not in f[1] + f[2]:
                    self.assertEqual(Fraction(int(f[1]), int(f[2])),
                                     Fraction(f[3]), s)

    def test_same_base_has_equate_step(self):
        gen = ExponentialEquationGenerator("same_base")
        for _ in range(200):
            result = gen.generate()
            eq = next(s for s in result["steps"]
                      if s.startswith(f"EQUATE_EXP{DELIM}"))
            lhs, rhs = eq.split(DELIM)[1].split(" = ")
            x = Fraction(result["final_answer"].replace("x = ", ""))
            self.assertEqual(eval_linear(lhs, x), Fraction(rhs), eq)

    def test_common_base_fraction_answers_occur(self):
        gen = ExponentialEquationGenerator("common_base")
        kinds = set()
        for _ in range(100):
            kinds.add("/" in gen.generate()["final_answer"])
        self.assertIn(True, kinds)

    def test_log_answers_take_logs_first(self):
        for v in ("log_exact", "ln_exact"):
            gen = ExponentialEquationGenerator(v)
            for _ in range(100):
                result = gen.generate()
                ops = [s.split(DELIM)[0] for s in result["steps"]]
                self.assertIn("LOG_BOTH_SIDES", ops)
                self.assertIn("LOG_IDENT", ops)
                self.assertLess(ops.index("LOG_BOTH_SIDES"),
                                ops.index("LOG_IDENT"))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"exponential_eq_same_base",
                               "exponential_eq_common_base",
                               "exponential_eq_log",
                               "exponential_eq_ln"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ExponentialEquationGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
