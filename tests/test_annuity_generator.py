import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.annuity_generator import AnnuityGenerator
from generators.exponential_model_generator import dec, money
from generators.finance_generator import exact
from helpers import DELIM


FV_RE = re.compile(
    r"An ordinary annuity pays \$(\d+) at the end of each period for "
    r"(\d+) periods at (\d+)% per period\. Find the future value\."
)
PV_RE = re.compile(
    r"An ordinary annuity pays \$(\d+) at the end of each period for "
    r"(\d+) periods at (\d+)% per period\. Find the present value\."
)
AMORT_RE = re.compile(
    r"Build a (\d+)-payment amortization schedule for a loan with starting "
    r"balance \$(\d+), payment \$(\d+), and period rate (\d+)%\. Find total "
    r"interest and final balance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_future(problem):
    match = FV_RE.fullmatch(problem)
    payment = int(match.group(1))
    periods = int(match.group(2))
    rate_pct = int(match.group(3))
    rate = Fraction(rate_pct, 100)
    base = 1 + rate
    growth = base ** periods
    numerator = growth - 1
    factor = numerator / rate
    value = payment * factor
    answer = f"future_value {money(value)}"
    steps = [
        make_step("ANNUITY_SETUP", "ordinary annuity future value",
                  f"PMT={payment},r={rate_pct}%,n={periods}"),
        make_step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
        make_step("ANNUITY_FORMULA", "FV = PMT*((1+r)^n - 1)/r"),
        make_step("A", 1, dec(rate), exact(base)),
        make_step("E", exact(base), periods, exact(growth)),
        make_step("S", exact(growth), 1, exact(numerator)),
        make_step("D", exact(numerator), dec(rate), exact(factor)),
        make_step("M", payment, exact(factor), exact(value)),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_present(problem):
    match = PV_RE.fullmatch(problem)
    payment = int(match.group(1))
    periods = int(match.group(2))
    rate_pct = int(match.group(3))
    rate = Fraction(rate_pct, 100)
    base = 1 + rate
    growth = base ** periods
    discount = Fraction(1, 1) / growth
    numerator = 1 - discount
    factor = numerator / rate
    value = payment * factor
    answer = f"present_value {money(value)}"
    steps = [
        make_step("ANNUITY_SETUP", "ordinary annuity present value",
                  f"PMT={payment},r={rate_pct}%,n={periods}"),
        make_step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
        make_step("ANNUITY_FORMULA", "PV = PMT*(1 - (1+r)^(-n))/r"),
        make_step("A", 1, dec(rate), exact(base)),
        make_step("E", exact(base), periods, exact(growth)),
        make_step("D", 1, exact(growth), exact(discount)),
        make_step("S", 1, exact(discount), exact(numerator)),
        make_step("D", exact(numerator), dec(rate), exact(factor)),
        make_step("M", payment, exact(factor), exact(value)),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_amort(problem):
    match = AMORT_RE.fullmatch(problem)
    periods = int(match.group(1))
    balance = Fraction(int(match.group(2)))
    payment = int(match.group(3))
    rate_pct = int(match.group(4))
    rate = Fraction(rate_pct, 100)
    steps = [
        make_step("ANNUITY_SETUP", "amortization schedule",
                  f"balance={int(balance)},payment={payment},r={rate_pct}%",
                  f"periods={periods}"),
        make_step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
        make_step("ANNUITY_FORMULA",
                  "interest=balance*r; principal=payment-interest"),
    ]
    total_interest = Fraction(0)
    for period in range(1, periods + 1):
        interest = balance * rate
        principal = payment - interest
        new_balance = balance - principal
        new_total = total_interest + interest
        steps.extend([
            make_step("M", exact(balance), dec(rate), exact(interest)),
            make_step("S", payment, exact(interest), exact(principal)),
            make_step("S", exact(balance), exact(principal), exact(new_balance)),
            make_step("A", exact(total_interest), exact(interest),
                      exact(new_total)),
            make_step("AMORT_ROW", period, f"interest={money(interest)}",
                      f"principal={money(principal)},balance={money(new_balance)}"),
        ])
        balance = new_balance
        total_interest = new_total
    answer = (
        f"total_interest {money(total_interest)}; "
        f"final_balance {money(balance)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if FV_RE.fullmatch(problem):
        return expected_future(problem)
    if PV_RE.fullmatch(problem):
        return expected_present(problem)
    if AMORT_RE.fullmatch(problem):
        return expected_amort(problem)
    raise AssertionError(problem)


class TestAnnuityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AnnuityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("annuity_"))
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_variants_are_available(self):
        for variant in AnnuityGenerator.VARIANTS:
            result = AnnuityGenerator(variant).generate()
            self.assertEqual(result["operation"], f"annuity_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            AnnuityGenerator("bogus")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
