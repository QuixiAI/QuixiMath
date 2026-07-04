import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fixed_point_generator import FixedPointGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use fixed-point iteration x=g\(x\) with g\(x\)=([^*]+)\*x([+-][^ ]+) "
    r"from x0=([^ ]+) for (\d+) iterations\. First check abs\(g'\)<1\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def signed_fraction(value):
    fr = Fraction(value)
    if fr >= 0:
        return f"+{fraction_text(fr)}"
    return fraction_text(fr)


def linear_text(a_coeff, b_coeff):
    return f"{fraction_text(a_coeff)}*x{signed_fraction(b_coeff)}"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "a": Fraction(match.group(1)),
        "b": Fraction(match.group(2)),
        "x0": Fraction(match.group(3)),
        "iterations": int(match.group(4)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    a_coeff = parts["a"]
    b_coeff = parts["b"]
    x_value = parts["x0"]
    iterations = parts["iterations"]
    g_text = linear_text(a_coeff, b_coeff)
    abs_a = abs(a_coeff)
    steps = [
        make_step("FIXED_POINT_SETUP", f"g(x)={g_text}",
                  f"x0={fraction_text(x_value)}",
                  f"iterations={iterations}"),
        make_step("DERIVATIVE", "g'(x)", fraction_text(a_coeff)),
        make_step("ABS", fraction_text(a_coeff), fraction_text(abs_a)),
        make_step("COMPARE", fraction_text(abs_a), "< 1", "converges"),
    ]
    for index in range(1, iterations + 1):
        ax = a_coeff * x_value
        next_x = ax + b_coeff
        steps.extend([
            make_step("M", fraction_text(a_coeff), fraction_text(x_value),
                      fraction_text(ax)),
            make_step("A", fraction_text(ax), fraction_text(b_coeff),
                      fraction_text(next_x)),
            make_step("FIXED_POINT_UPDATE", index,
                      f"x_{index - 1}={fraction_text(x_value)}",
                      f"x_{index}={fraction_text(next_x)}"),
        ])
        x_value = next_x
    answer = f"x_{iterations} = {fraction_text(x_value)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestFixedPointGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = FixedPointGenerator()

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
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ABS":
                    self.assertEqual(abs(Fraction(fields[1])),
                                     Fraction(fields[2]), raw_step)

    def test_contraction_check(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            self.assertLess(abs(parts["a"]), 1)
            self.assertIn("COMPARE", "\n".join(result["steps"]))

    def test_variant_is_available(self):
        result = FixedPointGenerator("affine").generate()
        self.assertEqual(result["operation"], "fixed_point_affine")
        parse_problem(result["problem"])

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FixedPointGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
