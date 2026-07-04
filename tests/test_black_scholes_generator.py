import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.black_scholes_generator import BlackScholesGenerator
from generators.finance_generator import exact
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Evaluate Black-Scholes option prices with S=([0-9]+), K=([0-9]+), "
    r"discount_factor=([-0-9/.]+), N\(d1\)=([-0-9/.]+), and "
    r"N\(d2\)=([-0-9/.]+)\. Use N\(-d\)=1-N\(d\)\. "
    r"Compute the call and put prices\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    stock = int(match.group(1))
    strike = int(match.group(2))
    discount = Fraction(match.group(3))
    n_d1 = Fraction(match.group(4))
    n_d2 = Fraction(match.group(5))

    stock_call_term = stock * n_d1
    discounted_strike = strike * discount
    strike_call_term = discounted_strike * n_d2
    call_price = stock_call_term - strike_call_term
    n_neg_d1 = 1 - n_d1
    n_neg_d2 = 1 - n_d2
    put_strike_term = discounted_strike * n_neg_d2
    put_stock_term = stock * n_neg_d1
    put_price = put_strike_term - put_stock_term
    answer = f"call={exact(call_price)}; put={exact(put_price)}"
    steps = [
        make_step("BS_SETUP", f"S={stock},K={strike}",
                  f"df={exact(discount)}",
                  f"N_d1={exact(n_d1)},N_d2={exact(n_d2)}"),
        make_step("BS_FORMULA", "C=S*N(d1)-K*df*N(d2)",
                  "P=K*df*N(-d2)-S*N(-d1)"),
        make_step("M", stock, exact(n_d1), exact(stock_call_term)),
        make_step("M", strike, exact(discount), exact(discounted_strike)),
        make_step("M", exact(discounted_strike), exact(n_d2),
                  exact(strike_call_term)),
        make_step("S", exact(stock_call_term), exact(strike_call_term),
                  exact(call_price)),
        make_step("S", 1, exact(n_d1), exact(n_neg_d1)),
        make_step("S", 1, exact(n_d2), exact(n_neg_d2)),
        make_step("NORMAL_SYMMETRY", f"N_neg_d1={exact(n_neg_d1)}",
                  f"N_neg_d2={exact(n_neg_d2)}"),
        make_step("M", exact(discounted_strike), exact(n_neg_d2),
                  exact(put_strike_term)),
        make_step("M", stock, exact(n_neg_d1), exact(put_stock_term)),
        make_step("S", exact(put_strike_term), exact(put_stock_term),
                  exact(put_price)),
        make_step("BS_RESULT", f"call={exact(call_price)}",
                  f"put={exact(put_price)}"),
        make_step("Z", answer),
    ]
    return steps, answer


class TestBlackScholesGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BlackScholesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "black_scholes_call_put")
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

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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
