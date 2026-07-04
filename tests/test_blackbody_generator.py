import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.blackbody_generator import BlackbodyGenerator
from helpers import DELIM


WIEN_RE = re.compile(
    r"A blackbody has temperature T=(\d+) K\. Using Wien constant b=(\d+) "
    r"m\*K, find peak wavelength lambda_max\."
)
STEFAN_RE = re.compile(
    r"A blackbody has area A=(\d+) m\^2 and temperature T=(\d+) K\. Using "
    r"Stefan-Boltzmann constant sigma=(\d+), find radiated power P\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_wien(problem):
    temperature, wien_constant = (
        int(value) for value in WIEN_RE.fullmatch(problem).groups()
    )
    wavelength = Fraction(wien_constant, temperature)
    steps = [
        make_step("BLACKBODY_SETUP", "wien_peak",
                  f"b={wien_constant}", f"T={temperature}"),
        make_step("BLACKBODY_FORMULA", "lambda_max=b/T"),
        make_step("D", wien_constant, temperature, wavelength),
    ]
    answer = f"lambda_max={wavelength} m"
    return steps, answer


def expected_stefan(problem):
    area, temperature, sigma = (
        int(value) for value in STEFAN_RE.fullmatch(problem).groups()
    )
    t_fourth = temperature ** 4
    sigma_area = sigma * area
    power = sigma_area * t_fourth
    steps = [
        make_step("BLACKBODY_SETUP", "stefan_power",
                  f"sigma={sigma}, A={area}", f"T={temperature}"),
        make_step("BLACKBODY_FORMULA", "P=sigma*A*T^4"),
        make_step("E", temperature, 4, t_fourth),
        make_step("M", sigma, area, sigma_area),
        make_step("M", sigma_area, t_fourth, power),
    ]
    answer = f"P={power} W"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if WIEN_RE.fullmatch(problem):
        steps, answer = expected_wien(problem)
    else:
        steps, answer = expected_stefan(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestBlackbodyGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = BlackbodyGenerator()

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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in BlackbodyGenerator.VARIANTS:
            result = BlackbodyGenerator(variant).generate()
            self.assertEqual(result["operation"], f"blackbody_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BlackbodyGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
