import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.npv_irr_generator import NPVIRRGenerator
from generators.exponential_model_generator import dec
from generators.finance_generator import exact
from helpers import DELIM


NPV_RE = re.compile(
    r"Compute NPV for cash flows c0=([-0-9]+), c1=([-0-9]+), "
    r"c2=([-0-9]+), c3=([-0-9]+) at discount rate ([0-9]+)%\."
)
IRR_RE = re.compile(
    r"Estimate IRR for cash flows c0=([-0-9]+), c1=([-0-9]+) using "
    r"Newton's method from r0=([-0-9/]+) for ([0-9]+) iterations\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_npv(problem):
    match = NPV_RE.fullmatch(problem)
    c0 = int(match.group(1))
    cashflows = [int(match.group(2)), int(match.group(3)),
                 int(match.group(4))]
    rate_pct = int(match.group(5))
    rate = Fraction(rate_pct, 100)
    base = 1 + rate
    total = Fraction(c0)
    steps = [
        make_step("NPV_SETUP", f"c0={c0},c1={cashflows[0]},c2={cashflows[1]},c3={cashflows[2]}",
                  f"rate={rate_pct}%"),
        make_step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
        make_step("A", 1, dec(rate), exact(base)),
        make_step("NPV_TERM", "t=0", exact(total)),
    ]
    for t, cashflow in enumerate(cashflows, start=1):
        discount = base ** t
        pv = Fraction(cashflow, 1) / discount
        new_total = total + pv
        steps.extend([
            make_step("E", exact(base), t, exact(discount)),
            make_step("D", cashflow, exact(discount), exact(pv)),
            make_step("NPV_TERM", f"t={t}", exact(pv)),
            make_step("A", exact(total), exact(pv), exact(new_total)),
        ])
        total = new_total
    answer = f"NPV={exact(total)}"
    return steps, answer


def expected_irr(problem):
    match = IRR_RE.fullmatch(problem)
    c0 = int(match.group(1))
    payoff = int(match.group(2))
    r = Fraction(match.group(3))
    iterations = int(match.group(4))
    steps = [
        make_step("IRR_SETUP", f"c0={c0},c1={payoff}",
                  f"r0={fraction_text(r)},iterations={iterations}"),
    ]
    for iteration in range(1, iterations + 1):
        base = 1 + r
        pv = Fraction(payoff, 1) / base
        f_value = c0 + pv
        base_sq = base ** 2
        deriv_abs = Fraction(payoff, 1) / base_sq
        derivative = -deriv_abs
        correction = f_value / derivative
        next_r = r - correction
        steps.extend([
            make_step("A", 1, fraction_text(r), fraction_text(base)),
            make_step("D", payoff, fraction_text(base), fraction_text(pv)),
            make_step("A", c0, fraction_text(pv), fraction_text(f_value)),
            make_step("IRR_VALUE", f"f{iteration}", fraction_text(f_value)),
            make_step("E", fraction_text(base), 2, fraction_text(base_sq)),
            make_step("D", payoff, fraction_text(base_sq),
                      fraction_text(deriv_abs)),
            make_step("M", -1, fraction_text(deriv_abs),
                      fraction_text(derivative)),
            make_step("IRR_VALUE", f"fprime{iteration}",
                      fraction_text(derivative)),
            make_step("D", fraction_text(f_value), fraction_text(derivative),
                      fraction_text(correction)),
            make_step("S", fraction_text(r), fraction_text(correction),
                      fraction_text(next_r)),
            make_step("NEWTON_STEP", iteration, fraction_text(next_r)),
        ])
        r = next_r
    answer = f"IRR_estimate={fraction_text(r)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if NPV_RE.fullmatch(problem):
        steps, answer = expected_npv(problem)
    elif IRR_RE.fullmatch(problem):
        steps, answer = expected_irr(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestNPVIRRGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NPVIRRGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["operation"].startswith("npv_irr_"))
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
        for variant in NPVIRRGenerator.VARIANTS:
            result = NPVIRRGenerator(variant).generate()
            self.assertEqual(result["operation"], f"npv_irr_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NPVIRRGenerator("bogus")

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
