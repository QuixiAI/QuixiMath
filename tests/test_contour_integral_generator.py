import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.contour_integral_generator import ContourIntegralGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Evaluate the positively oriented contour integral over \|z\|=(\d+) "
    r"of f\(z\) = (.+)\."
)
TERM_RE = re.compile(r"([+-]?) ?(\d+)/(z|\(z[+-]\d+\))")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def term_text(residue, pole):
    return f"{abs(residue)}/{z_minus(pole)}"


def function_text(residues, poles):
    parts = []
    for residue, pole in zip(residues, poles):
        text = term_text(residue, pole)
        if not parts:
            parts.append(text if residue > 0 else f"-{text}")
        else:
            parts.append(f"+ {text}" if residue > 0 else f"- {text}")
    return " ".join(parts)


def parse_pole(denominator):
    if denominator == "z":
        return 0
    body = denominator.strip("()")
    if "+" in body:
        return -int(body.split("+")[1])
    return int(body.split("-")[1])


def parse_function(text):
    residues = []
    poles = []
    for sign, value, denominator in TERM_RE.findall(text):
        residue = int(value)
        if sign == "-":
            residue = -residue
        residues.append(residue)
        poles.append(parse_pole(denominator))
    return residues, poles


def integral_text(residue_sum):
    if residue_sum == 0:
        return "0"
    coef = 2 * residue_sum
    if coef == 1:
        return "pi i"
    if coef == -1:
        return "-pi i"
    return f"{coef}pi i"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    radius = int(match.group(1))
    function = match.group(2)
    residues, poles = parse_function(function)
    return {"radius": radius, "function": function, "residues": residues,
            "poles": poles}


def expected_flow(example):
    parts = parse_problem(example["problem"])
    steps = [
        make_step("CONTOUR_SETUP", f"abs(z)={parts['radius']}",
                  "positive orientation", f"f={parts['function']}"),
    ]
    residue_sum = 0
    for pole, residue in zip(parts["poles"], parts["residues"]):
        inside = abs(pole) < parts["radius"]
        verdict = "inside" if inside else "outside"
        steps.append(make_step("POLE_TEST", f"pole {pole}",
                               f"abs({pole}) < {parts['radius']}", verdict))
        steps.append(make_step("RESIDUE", f"pole {pole}", residue, verdict))
        if inside:
            new_sum = residue_sum + residue
            steps.append(make_step("A", residue_sum, residue, new_sum))
            residue_sum = new_sum
    steps.append(make_step("RESIDUE_SUM", residue_sum))
    coefficient = 2 * residue_sum
    steps.append(make_step("M", 2, residue_sum, coefficient))
    answer = f"integral = {integral_text(residue_sum)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestContourIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ContourIntegralGenerator()

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
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_residue_sum_matches_answer(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            residue_sum = sum(
                residue for residue, pole in zip(parts["residues"],
                                                 parts["poles"])
                if abs(pole) < parts["radius"]
            )
            self.assertEqual(result["final_answer"],
                             f"integral = {integral_text(residue_sum)}")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
