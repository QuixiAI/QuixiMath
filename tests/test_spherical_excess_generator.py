import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.spherical_excess_generator import SphericalExcessGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"A spherical triangle on a sphere of radius (\d+) has angles "
    r"(\d+) deg, (\d+) deg, and (\d+) deg\. Use Girard's theorem "
    r"to find its exact area in terms of pi\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "radius": int(match.group(1)),
        "a": int(match.group(2)),
        "b": int(match.group(3)),
        "c": int(match.group(4)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    first_sum = parts["a"] + parts["b"]
    angle_sum = first_sum + parts["c"]
    excess_deg = angle_sum - 180
    excess_turn = Fraction(excess_deg, 180)
    radius_sq = parts["radius"] ** 2
    area_coeff = excess_turn * radius_sq
    answer = f"area = {pi_text(area_coeff)}"
    steps = [
        make_step("SPHERICAL_EXCESS_SETUP", f"R={parts['radius']}",
                  f"angles={parts['a']},{parts['b']},{parts['c']}"),
        make_step("THEOREM", "Girard",
                  "area = (A+B+C-180 deg)/180 * pi * R^2"),
        make_step("A", parts["a"], parts["b"], first_sum),
        make_step("A", first_sum, parts["c"], angle_sum),
        make_step("S", angle_sum, 180, excess_deg),
        make_step("D", excess_deg, 180, excess_turn),
        make_step("E", parts["radius"], 2, radius_sq),
        make_step("M", excess_turn, radius_sq, area_coeff),
        make_step("Z", answer),
    ]
    return steps, answer


class TestSphericalExcessGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SphericalExcessGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "spherical_excess_area")
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

    def test_area_is_spherical_excess_times_radius_squared(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            excess = Fraction(parts["a"] + parts["b"] + parts["c"] - 180,
                              180)
            answer = f"area = {pi_text(excess * parts['radius'] ** 2)}"
            self.assertEqual(result["final_answer"], answer)

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(int(fields[1]),
                                              int(fields[2])),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) *
                                     Fraction(fields[2]),
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
