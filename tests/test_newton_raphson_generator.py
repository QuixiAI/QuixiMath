import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.newton_raphson_generator import NewtonRaphsonGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Newton-Raphson on f\(x\)=x\^2-(\d+) with x0=([^ ]+) "
    r"for (\d+) iterations\. Give the final iterate\."
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
        "n": int(match.group(1)),
        "x0": Fraction(match.group(2)),
        "iterations": int(match.group(3)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    n = parts["n"]
    x_value = parts["x0"]
    iterations = parts["iterations"]
    steps = [
        make_step("NEWTON_SETUP", f"f(x)=x^2-{n}", "f'(x)=2x",
                  f"x0={fraction_text(x_value)},iterations={iterations}"),
    ]
    for index in range(1, iterations + 1):
        x_sq = x_value * x_value
        f_value = x_sq - n
        derivative = 2 * x_value
        correction = f_value / derivative
        next_x = x_value - correction
        steps.extend([
            make_step("M", fraction_text(x_value), fraction_text(x_value),
                      fraction_text(x_sq)),
            make_step("S", fraction_text(x_sq), n, fraction_text(f_value)),
            make_step("M", 2, fraction_text(x_value),
                      fraction_text(derivative)),
            make_step("D", fraction_text(f_value), fraction_text(derivative),
                      fraction_text(correction)),
            make_step("S", fraction_text(x_value), fraction_text(correction),
                      fraction_text(next_x)),
            make_step("NEWTON_UPDATE", index,
                      f"x_{index - 1}={fraction_text(x_value)}",
                      f"x_{index}={fraction_text(next_x)}"),
        ])
        x_value = next_x
    answer = f"x_{iterations} = {fraction_text(x_value)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestNewtonRaphsonGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NewtonRaphsonGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variant_is_available(self):
        result = NewtonRaphsonGenerator("sqrt").generate()
        self.assertEqual(result["operation"], "newton_raphson_sqrt")
        parse_problem(result["problem"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NewtonRaphsonGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
