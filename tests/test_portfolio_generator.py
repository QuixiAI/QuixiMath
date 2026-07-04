import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.portfolio_generator import PortfolioGenerator
from generators.exponential_model_generator import dec
from generators.finance_generator import exact
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A portfolio invests weight wA=([-0-9/.]+) in asset A and "
    r"wB=([-0-9/.]+) in asset B\. Asset A has expected return ([0-9]+)% "
    r"and variance ([-0-9/.]+); asset B has expected return ([0-9]+)% "
    r"and variance ([-0-9/.]+); covariance is ([-0-9/.]+)\. "
    r"Compute portfolio expected return and variance\."
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
    w_a = Fraction(match.group(1))
    w_b = Fraction(match.group(2))
    r_a_pct = int(match.group(3))
    var_a = Fraction(match.group(4))
    r_b_pct = int(match.group(5))
    var_b = Fraction(match.group(6))
    cov = Fraction(match.group(7))

    r_a = Fraction(r_a_pct, 100)
    r_b = Fraction(r_b_pct, 100)
    er_a = w_a * r_a
    er_b = w_b * r_b
    expected_return = er_a + er_b
    w_a_sq = w_a ** 2
    w_b_sq = w_b ** 2
    var_term_a = w_a_sq * var_a
    var_term_b = w_b_sq * var_b
    two_w_a = 2 * w_a
    two_w_aw_b = two_w_a * w_b
    cov_term = two_w_aw_b * cov
    variance_without_cov = var_term_a + var_term_b
    variance = variance_without_cov + cov_term

    answer = (
        f"expected_return={exact(expected_return)}; "
        f"variance={exact(variance)}"
    )
    steps = [
        make_step("PORT_SETUP", f"wA={exact(w_a)},wB={exact(w_b)}",
                  f"rA={r_a_pct}%,rB={r_b_pct}%",
                  f"varA={exact(var_a)},varB={exact(var_b)},cov={exact(cov)}"),
        make_step("PERCENT_TO_DEC", f"{r_a_pct}%", dec(r_a)),
        make_step("PERCENT_TO_DEC", f"{r_b_pct}%", dec(r_b)),
        make_step("PORT_FORMULA", "E=wA*rA+wB*rB",
                  "Var=wA^2*varA+wB^2*varB+2*wA*wB*cov"),
        make_step("M", exact(w_a), dec(r_a), exact(er_a)),
        make_step("M", exact(w_b), dec(r_b), exact(er_b)),
        make_step("A", exact(er_a), exact(er_b), exact(expected_return)),
        make_step("E", exact(w_a), 2, exact(w_a_sq)),
        make_step("M", exact(w_a_sq), exact(var_a), exact(var_term_a)),
        make_step("E", exact(w_b), 2, exact(w_b_sq)),
        make_step("M", exact(w_b_sq), exact(var_b), exact(var_term_b)),
        make_step("M", 2, exact(w_a), exact(two_w_a)),
        make_step("M", exact(two_w_a), exact(w_b), exact(two_w_aw_b)),
        make_step("M", exact(two_w_aw_b), exact(cov), exact(cov_term)),
        make_step("A", exact(var_term_a), exact(var_term_b),
                  exact(variance_without_cov)),
        make_step("A", exact(variance_without_cov), exact(cov_term),
                  exact(variance)),
        make_step("PORT_RESULT", f"expected_return={exact(expected_return)}",
                  f"variance={exact(variance)}"),
        make_step("Z", answer),
    ]
    return steps, answer


class TestPortfolioGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PortfolioGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "portfolio_two_asset")
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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
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
