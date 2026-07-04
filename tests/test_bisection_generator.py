import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bisection_generator import BisectionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use bisection for f\(x\)=x\^2-(\d+) on \[([^,]+), ([^\]]+)\] "
    r"for (\d+) iterations\. Give the final bracket\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def sign_text(value):
    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def interval_text(left, right):
    return f"[{fraction_text(left)}, {fraction_text(right)}]"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "n": int(match.group(1)),
        "left": Fraction(match.group(2)),
        "right": Fraction(match.group(3)),
        "iterations": int(match.group(4)),
    }


def eval_steps(steps, label, x_value, n):
    square = x_value * x_value
    value = square - n
    steps.append(make_step("M", fraction_text(x_value), fraction_text(x_value),
                           fraction_text(square)))
    steps.append(make_step("S", fraction_text(square), n,
                           fraction_text(value)))
    steps.append(make_step("SIGN", label, fraction_text(value),
                           sign_text(value)))
    return value


def expected_flow(example):
    parts = parse_problem(example["problem"])
    n = parts["n"]
    left = parts["left"]
    right = parts["right"]
    iterations = parts["iterations"]
    steps = [
        make_step("BISECTION_SETUP", f"f(x)=x^2-{n}",
                  f"interval={interval_text(left, right)}",
                  f"iterations={iterations}"),
    ]
    f_left = eval_steps(steps, "left", left, n)
    eval_steps(steps, "right", right, n)
    for index in range(1, iterations + 1):
        total = left + right
        mid = total / 2
        steps.append(make_step("A", fraction_text(left),
                               fraction_text(right), fraction_text(total)))
        steps.append(make_step("D", fraction_text(total), 2,
                               fraction_text(mid)))
        f_mid = eval_steps(steps, f"mid{index}", mid, n)
        product = f_left * f_mid
        steps.append(make_step("M", fraction_text(f_left),
                               fraction_text(f_mid), fraction_text(product)))
        steps.append(make_step("SIGN", f"product_{index}",
                               fraction_text(product), sign_text(product)))
        if product < 0:
            right = mid
            relation = "product < 0"
            update = interval_text(left, right)
        else:
            left = mid
            f_left = f_mid
            relation = "product > 0"
            update = interval_text(left, right)
        steps.append(make_step("BISECT_UPDATE", index, relation, update))
    answer = f"root in {interval_text(left, right)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBisectionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BisectionGenerator()

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
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_sign_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "SIGN":
                    self.assertEqual(sign_text(Fraction(fields[2])),
                                     fields[3], raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_final_bracket_contains_root(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            left_raw, right_raw = result["final_answer"].removeprefix(
                "root in ["
            ).rstrip("]").split(", ")
            left = Fraction(left_raw)
            right = Fraction(right_raw)
            f_left = left * left - parts["n"]
            f_right = right * right - parts["n"]
            self.assertLess(f_left, 0)
            self.assertGreater(f_right, 0)


if __name__ == "__main__":
    unittest.main()
