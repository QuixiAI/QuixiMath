import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quantum_formula_generator import QuantumFormulaGenerator
from helpers import DELIM


PHOTO_RE = re.compile(
    r"A photoelectric surface has work function phi=(\d+) J\. Light has "
    r"frequency f=(\d+) Hz and h=(\d+)\. Find K_max\."
)
DEBROGLIE_RE = re.compile(
    r"A particle has momentum p=(\d+) kg\*m/s\. Using h=(\d+), find its "
    r"de Broglie wavelength\."
)
COMPTON_RE = re.compile(
    r"In a Compton scattering setup, h=(\d+), particle mass m=(\d+), c=(\d+), "
    r"and 1-cos\(theta\)=([^ ]+)\. Find the wavelength shift Delta_lambda\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_photo(problem):
    phi, frequency, h = (int(value) for value in PHOTO_RE.fullmatch(problem).groups())
    photon_energy = h * frequency
    kinetic = photon_energy - phi
    steps = [
        make_step("QUANTUM_SETUP", "photoelectric",
                  f"h={h}, f={frequency}", f"phi={phi}"),
        make_step("QUANTUM_FORMULA", "K_max=h*f-phi"),
        make_step("M", h, frequency, photon_energy),
        make_step("S", photon_energy, phi, kinetic),
    ]
    answer = f"K_max={kinetic} J"
    return steps, answer


def expected_debroglie(problem):
    momentum, h = (
        int(value) for value in DEBROGLIE_RE.fullmatch(problem).groups()
    )
    wavelength = Fraction(h, momentum)
    steps = [
        make_step("QUANTUM_SETUP", "de_broglie", f"h={h}", f"p={momentum}"),
        make_step("QUANTUM_FORMULA", "lambda=h/p"),
        make_step("D", h, momentum, fraction_text(wavelength)),
    ]
    answer = f"lambda={fraction_text(wavelength)} m"
    return steps, answer


def expected_compton(problem):
    h_raw, mass_raw, c_raw, one_minus_cos_raw = COMPTON_RE.fullmatch(
        problem
    ).groups()
    h = int(h_raw)
    mass = int(mass_raw)
    c = int(c_raw)
    one_minus_cos = Fraction(one_minus_cos_raw)
    denominator = mass * c
    compton_factor = Fraction(h, denominator)
    shift = compton_factor * one_minus_cos
    steps = [
        make_step("QUANTUM_SETUP", "compton",
                  f"h={h}, m={mass}, c={c}",
                  f"one_minus_cos={fraction_text(one_minus_cos)}"),
        make_step("QUANTUM_FORMULA",
                  "Delta_lambda=h/(m*c)*(1-cos(theta))"),
        make_step("M", mass, c, denominator),
        make_step("D", h, denominator, fraction_text(compton_factor)),
        make_step("M", fraction_text(compton_factor),
                  fraction_text(one_minus_cos), fraction_text(shift)),
    ]
    answer = f"Delta_lambda={fraction_text(shift)} m"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if PHOTO_RE.fullmatch(problem):
        steps, answer = expected_photo(problem)
    elif DEBROGLIE_RE.fullmatch(problem):
        steps, answer = expected_debroglie(problem)
    else:
        steps, answer = expected_compton(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestQuantumFormulaGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = QuantumFormulaGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in QuantumFormulaGenerator.VARIANTS:
            result = QuantumFormulaGenerator(variant).generate()
            self.assertEqual(result["operation"], f"quantum_formula_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            QuantumFormulaGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
