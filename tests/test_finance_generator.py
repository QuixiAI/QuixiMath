import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.finance_generator import FinanceGenerator, exact
from generators.exponential_model_generator import money
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute finance answers from the prompt alone."""
    problem = example["problem"]
    m = re.search(
        r"starts with \$(\d+) and earns simple interest at (\d+)% per "
        r"year for (\d+) years",
        problem,
    )
    if m:
        principal, rate_pct, years = (int(v) for v in m.groups())
        interest = Fraction(principal * rate_pct * years, 100)
        balance = principal + interest
        return f"interest {money(interest)}; balance {money(balance)}"

    m = re.search(
        r"starts with \$(\d+) and earns (\d+)% interest compounded once "
        r"per year for (\d+) years",
        problem,
    )
    if m:
        principal, rate_pct, years = (int(v) for v in m.groups())
        balance = principal * (1 + Fraction(rate_pct, 100)) ** years
        interest = balance - principal
        return f"balance {money(balance)}; interest {money(interest)}"

    m = re.search(
        r"current balance \$(\d+)\. The monthly payment is \$(\d+) and "
        r"the annual interest rate is (\d+)%",
        problem,
    )
    if m:
        balance, payment, annual_pct = (int(v) for v in m.groups())
        interest = balance * Fraction(annual_pct, 1200)
        principal_paid = payment - interest
        new_balance = balance - principal_paid
        return (f"interest {money(interest)}; principal "
                f"{money(principal_paid)}; balance {money(new_balance)}")

    m = re.search(
        r"monthly income of \$(\d+) is split into needs (\d+)%, savings "
        r"(\d+)%, and fun (\d+)%",
        problem,
    )
    income, needs_pct, savings_pct, fun_pct = (int(v) for v in m.groups())
    needs = income * Fraction(needs_pct, 100)
    savings = income * Fraction(savings_pct, 100)
    fun = income * Fraction(fun_pct, 100)
    return (f"needs {money(needs)}; savings {money(savings)}; "
            f"fun {money(fun)}")


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "PERCENT_TO_DEC":
            pct = int(parts[1].rstrip("%"))
            if exact(Fraction(pct, 100)) != parts[2]:
                return False
        elif code == "RATE_MONTHLY":
            pct = int(re.search(r"(\d+)% / 12", parts[1]).group(1))
            if exact(Fraction(pct, 1200)) != parts[2]:
                return False
        elif code == "M":
            if exact(Fraction(parts[1]) * Fraction(parts[2])) != parts[3]:
                return False
        elif code == "A":
            if exact(Fraction(parts[1]) + Fraction(parts[2])) != parts[3]:
                return False
        elif code == "S":
            if exact(Fraction(parts[1]) - Fraction(parts[2])) != parts[3]:
                return False
        elif code == "E":
            if exact(Fraction(parts[1]) ** int(parts[2])) != parts[3]:
                return False
    return True


class TestFinanceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FinanceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_money_format(self):
        for _ in range(200):
            result = self.gen.generate()
            amounts = re.findall(r"\$\d+\.\d{2}", result["final_answer"])
            self.assertGreaterEqual(len(amounts), 2, result["final_answer"])

    def test_formula_present(self):
        for variant in FinanceGenerator.VARIANTS:
            result = FinanceGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"FIN_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            FinanceGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
