import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.uncertainty_generator import UncertaintyGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For a particle in a 1D box with L=1 and hbar=1 in state n=(\d+), "
    r"use the supplied expectation formulas to compute Delta x Delta p exactly\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return int(match.group(1))


def expected_flow(example):
    n = parse_problem(example["problem"])
    n_sq = n * n
    two_n_sq = 2 * n_sq
    product_inside = f"{n_sq}pi^2/12 - 1/2"
    answer = f"Delta x Delta p = sqrt({product_inside})"
    steps = [
        make_step("UNCERTAINTY_SETUP", "particle in a box",
                  "L=1, hbar=1", f"n={n}"),
        make_step("FORMULA", "<x>=1/2",
                  "<x^2>=1/3 - 1/(2 n^2 pi^2)"),
        make_step("FORMULA", "<p>=0", "<p^2>=n^2 pi^2"),
        make_step("E", n, 2, n_sq),
        make_step("M", 2, n_sq, two_n_sq),
        make_step("VARIANCE", "Delta x^2",
                  f"1/12 - 1/({two_n_sq}pi^2)"),
        make_step("VARIANCE", "Delta p^2", f"{n_sq}pi^2"),
        make_step("PRODUCT", "Delta x^2 * Delta p^2", product_inside),
        make_step("CHECK", "Heisenberg lower bound", ">= 1/4", "holds"),
        make_step("Z", answer),
    ]
    return steps, answer


class TestUncertaintyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = UncertaintyGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "uncertainty_particle_box")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
