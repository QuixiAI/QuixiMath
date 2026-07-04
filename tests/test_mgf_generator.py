import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mgf_generator import MGFGenerator, exp_term
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A discrete random variable has P\(X=0\)=([^,]+), "
    r"P\(X=1\)=([^,]+), and P\(X=2\)=([^ ]+)\. "
    r"Derive M\(t\), then use M'\(0\) and M''\(0\) to find "
    r"E\[X\], E\[X\^2\], and Var\(X\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def formula(terms):
    return " + ".join(terms)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(Fraction(match.group(i)) for i in range(1, 4))


def expected_flow(example):
    p0, p1, p2 = parse_problem(example["problem"])
    mgf = formula([exp_term(p0, 0), exp_term(p1, 1), exp_term(p2, 2)])
    first_derivative = formula([exp_term(p1, 1), exp_term(2 * p2, 2)])
    second_derivative = formula([exp_term(p1, 1), exp_term(4 * p2, 2)])
    two_p2 = 2 * p2
    mean = p1 + two_p2
    four = 2 ** 2
    four_p2 = four * p2
    second_moment = p1 + four_p2
    mean_sq = mean * mean
    variance = second_moment - mean_sq
    steps = [
        make_step("MGF_SETUP", f"P(X=0)={fraction_text(p0)}",
                  f"P(X=1)={fraction_text(p1)}",
                  f"P(X=2)={fraction_text(p2)}"),
        make_step("MGF_TERM", "x=0", "p0*e^(0t)", fraction_text(p0)),
        make_step("MGF_TERM", "x=1", "p1*e^t", exp_term(p1, 1)),
        make_step("MGF_TERM", "x=2", "p2*e^(2t)", exp_term(p2, 2)),
        make_step("REWRITE", f"M(t)={mgf}"),
        make_step("DERIVATIVE", f"M'(t)={first_derivative}"),
        make_step("DERIVATIVE", f"M''(t)={second_derivative}"),
        make_step("EVAL_AT_ZERO", "e^0=1", "e^(2*0)=1"),
        make_step("M", 2, fraction_text(p2), fraction_text(two_p2)),
        make_step("A", fraction_text(p1), fraction_text(two_p2),
                  fraction_text(mean)),
        make_step("E", 2, 2, four),
        make_step("M", four, fraction_text(p2), fraction_text(four_p2)),
        make_step("A", fraction_text(p1), fraction_text(four_p2),
                  fraction_text(second_moment)),
        make_step("M", fraction_text(mean), fraction_text(mean),
                  fraction_text(mean_sq)),
        make_step("S", fraction_text(second_moment), fraction_text(mean_sq),
                  fraction_text(variance)),
    ]
    answer = (
        f"M(t)={mgf}; E[X]={fraction_text(mean)}; "
        f"E[X^2]={fraction_text(second_moment)}; "
        f"Var(X)={fraction_text(variance)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMGFGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MGFGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "mgf_discrete_three_point")
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
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_probabilities_sum_to_one(self):
        for _ in range(300):
            p0, p1, p2 = parse_problem(self.gen.generate()["problem"])
            self.assertEqual(p0 + p1 + p2, 1)
            for p in (p0, p1, p2):
                self.assertGreater(p, 0)
                self.assertLess(p, 1)

    def test_enough_unique_distributions_for_sampling(self):
        problems = {self.gen.generate()["problem"] for _ in range(500)}
        self.assertGreaterEqual(len(problems), 200)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
