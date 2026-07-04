import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.running_coupling_generator import RunningCouplingGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"At one loop, use 1/alpha\(mu\)=1/alpha0\+beta\*L with "
    r"L=ln\(mu/mu0\) supplied\. Given alpha0=([^,]+), beta=([^,]+), "
    r"and L=([^,]+), compute alpha\(mu\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "alpha0": Fraction(match.group(1)),
        "beta": Fraction(match.group(2)),
        "L": Fraction(match.group(3)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    alpha0 = parts["alpha0"]
    beta = parts["beta"]
    log_ratio = parts["L"]
    inv_alpha0 = Fraction(1, 1) / alpha0
    shift = beta * log_ratio
    inv_alpha_mu = inv_alpha0 + shift
    alpha_mu = Fraction(1, 1) / inv_alpha_mu
    steps = [
        make_step("RG_SETUP", "one_loop",
                  f"alpha0={fraction_text(alpha0)}",
                  f"beta={fraction_text(beta)},L={fraction_text(log_ratio)}"),
        make_step("D", 1, fraction_text(alpha0), fraction_text(inv_alpha0)),
        make_step("M", fraction_text(beta), fraction_text(log_ratio),
                  fraction_text(shift)),
        make_step("A", fraction_text(inv_alpha0), fraction_text(shift),
                  fraction_text(inv_alpha_mu)),
        make_step("D", 1, fraction_text(inv_alpha_mu),
                  fraction_text(alpha_mu)),
        make_step("M", fraction_text(alpha_mu), fraction_text(inv_alpha_mu),
                  1),
        make_step("CHECK", "reciprocal", "alpha_mu*inv_alpha_mu", 1),
    ]
    answer = f"alpha(mu) = {fraction_text(alpha_mu)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRunningCouplingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RunningCouplingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variant_is_available(self):
        result = RunningCouplingGenerator("evolve").generate()
        self.assertEqual(result["operation"], "running_coupling_evolve")
        parse_problem(result["problem"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RunningCouplingGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
