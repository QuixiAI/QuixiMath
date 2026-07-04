import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hyperbolic_function_generator import HyperbolicFunctionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given e\^x = ([^ ]+) and e\^\(-x\) = ([^,]+), compute sinh x, "
    r"cosh x, and tanh x\."
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
    return Fraction(match.group(1)), Fraction(match.group(2))


def expected_flow(example):
    exp_x, exp_neg_x = parse_problem(example["problem"])
    diff = exp_x - exp_neg_x
    sinh_x = diff / 2
    total = exp_x + exp_neg_x
    cosh_x = total / 2
    tanh_x = sinh_x / cosh_x
    cosh_sq = cosh_x ** 2
    sinh_sq = sinh_x ** 2
    identity = cosh_sq - sinh_sq
    steps = [
        make_step("HYPERBOLIC_SETUP", f"e^x={fraction_text(exp_x)}",
                  f"e^(-x)={fraction_text(exp_neg_x)}"),
        make_step("FORMULA", "sinh x = (e^x - e^(-x))/2"),
        make_step("S", fraction_text(exp_x), fraction_text(exp_neg_x),
                  fraction_text(diff)),
        make_step("D", fraction_text(diff), 2, fraction_text(sinh_x)),
        make_step("FORMULA", "cosh x = (e^x + e^(-x))/2"),
        make_step("A", fraction_text(exp_x), fraction_text(exp_neg_x),
                  fraction_text(total)),
        make_step("D", fraction_text(total), 2, fraction_text(cosh_x)),
        make_step("FORMULA", "tanh x = sinh x / cosh x"),
        make_step("D", fraction_text(sinh_x), fraction_text(cosh_x),
                  fraction_text(tanh_x)),
        make_step("E", fraction_text(cosh_x), 2, fraction_text(cosh_sq)),
        make_step("E", fraction_text(sinh_x), 2, fraction_text(sinh_sq)),
        make_step("S", fraction_text(cosh_sq), fraction_text(sinh_sq),
                  fraction_text(identity)),
        make_step("CHECK", "cosh^2 x - sinh^2 x", fraction_text(identity),
                  "identity holds"),
    ]
    answer = (
        f"sinh x = {fraction_text(sinh_x)}, "
        f"cosh x = {fraction_text(cosh_x)}, "
        f"tanh x = {fraction_text(tanh_x)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestHyperbolicFunctionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HyperbolicFunctionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "hyperbolic_function_eval")
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

    def test_identity_check_is_exact(self):
        for _ in range(300):
            result = self.gen.generate()
            check = [s for s in result["steps"]
                     if s.startswith(f"CHECK{DELIM}")][-1]
            self.assertEqual(check.split(DELIM)[2], "1")

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
