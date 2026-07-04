import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.order_statistics_generator import OrderStatisticsGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For (\d+) iid Uniform\(0,1\) samples, find the pdf, mean, "
    r"variance, and f\(([^)]+)\) for the (\d+)-th order statistic "
    r"X_\(\3\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    assert match is not None, example["problem"]
    n = int(match.group(1))
    q = Fraction(match.group(2))
    k = int(match.group(3))

    n_fact = math.factorial(n)
    k_minus = k - 1
    n_minus = n - k
    k_minus_fact = math.factorial(k_minus)
    n_minus_fact = math.factorial(n_minus)
    denom_fact = k_minus_fact * n_minus_fact
    coef = Fraction(n_fact, denom_fact)
    one_minus_q = 1 - q
    q_power = q ** k_minus
    one_minus_power = one_minus_q ** n_minus
    pdf_partial = coef * q_power
    pdf_value = pdf_partial * one_minus_power
    n_plus_one = n + 1
    mean = Fraction(k, n_plus_one)
    n_plus_one_minus_k = n_plus_one - k
    var_num = k * n_plus_one_minus_k
    n_plus_one_sq = n_plus_one ** 2
    n_plus_two = n_plus_one + 1
    var_den = n_plus_one_sq * n_plus_two
    variance = Fraction(var_num, var_den)
    # Answer-format conventions: drop ^0 factors, render ^1 as the bare base
    factors = []
    if k_minus == 1:
        factors.append("x")
    elif k_minus > 1:
        factors.append(f"x^{k_minus}")
    if n_minus == 1:
        factors.append("(1-x)")
    elif n_minus > 1:
        factors.append(f"(1-x)^{n_minus}")
    pdf_formula = "*".join(([fraction_text(coef)] if coef != 1 or not factors
                            else []) + factors)
    steps = [
        make_step("ORDER_SETUP", f"n={n}", f"k={k}",
                  f"q={fraction_text(q)}"),
        make_step("FACT", n, n_fact),
        make_step("S", k, 1, k_minus),
        make_step("S", n, k, n_minus),
        make_step("FACT", k_minus, k_minus_fact),
        make_step("FACT", n_minus, n_minus_fact),
        make_step("M", k_minus_fact, n_minus_fact, denom_fact),
        make_step("D", n_fact, denom_fact, fraction_text(coef)),
        make_step("ORDER_PDF", f"f_{{{k}:{n}}}(x)={pdf_formula}"),
        make_step("S", 1, fraction_text(q), fraction_text(one_minus_q)),
        make_step("E", fraction_text(q), k_minus, fraction_text(q_power)),
        make_step("E", fraction_text(one_minus_q), n_minus,
                  fraction_text(one_minus_power)),
        make_step("M", fraction_text(coef), fraction_text(q_power),
                  fraction_text(pdf_partial)),
        make_step("M", fraction_text(pdf_partial),
                  fraction_text(one_minus_power), fraction_text(pdf_value)),
        make_step("A", n, 1, n_plus_one),
        make_step("D", k, n_plus_one, fraction_text(mean)),
        make_step("S", n_plus_one, k, n_plus_one_minus_k),
        make_step("M", k, n_plus_one_minus_k, var_num),
        make_step("E", n_plus_one, 2, n_plus_one_sq),
        make_step("A", n_plus_one, 1, n_plus_two),
        make_step("M", n_plus_one_sq, n_plus_two, var_den),
        make_step("D", var_num, var_den, fraction_text(variance)),
    ]
    answer = (
        f"f_{{{k}:{n}}}(x)={pdf_formula}; "
        f"E[X_({k})]={fraction_text(mean)}; "
        f"Var(X_({k}))={fraction_text(variance)}; "
        f"f_{{{k}:{n}}}({fraction_text(q)})={fraction_text(pdf_value)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestOrderStatisticsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = OrderStatisticsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"],
                         "order_statistics_uniform_pdf_moments")
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
                elif fields[0] == "FACT":
                    self.assertEqual(math.factorial(int(fields[1])),
                                     int(fields[2]), raw_step)

    def test_parameters_are_in_range(self):
        for _ in range(300):
            problem = self.gen.generate()["problem"]
            n, q, k = PROBLEM_RE.fullmatch(problem).groups()
            n = int(n)
            k = int(k)
            q = Fraction(q)
            self.assertGreaterEqual(n, 2)
            self.assertLessEqual(k, n)
            self.assertGreater(q, 0)
            self.assertLess(q, 1)

    def test_enough_unique_problems_for_sampling(self):
        problems = {self.gen.generate()["problem"] for _ in range(500)}
        self.assertGreaterEqual(len(problems), 200)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_pdf_formula_follows_answer_format_conventions(self):
        # No x^0 / (1-x)^0 factors and no ^1 in the rendered pdf
        for _ in range(300):
            answer = self.gen.generate()["final_answer"]
            self.assertNotIn("^0", answer)
            self.assertNotRegex(answer, r"\^1(?!\d)")


if __name__ == "__main__":
    unittest.main()
