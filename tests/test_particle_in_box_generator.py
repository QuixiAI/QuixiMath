import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.particle_in_box_generator import ParticleInBoxGenerator
from helpers import DELIM


ENERGY_RE = re.compile(
    r"A particle in a 1D box has quantum number n=(\d+), h=(\d+), "
    r"mass m=(\d+), and box length L=(\d+)\. Find E_n\."
)
TRANSITION_RE = re.compile(
    r"A particle in a 1D box transitions from n=(\d+) to n=(\d+)\. Use "
    r"h=(\d+), c=(\d+), mass m=(\d+), and length L=(\d+) to find the "
    r"emitted photon wavelength\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_energy(problem):
    n, h, mass, length = (
        int(value) for value in ENERGY_RE.fullmatch(problem).groups()
    )
    n_sq = n ** 2
    h_sq = h ** 2
    numerator = n_sq * h_sq
    length_sq = length ** 2
    eight_m = 8 * mass
    denominator = eight_m * length_sq
    energy = Fraction(numerator, denominator)
    steps = [
        make_step("BOX_SETUP", "energy_level",
                  f"n={n}, h={h}", f"m={mass}, L={length}"),
        make_step("BOX_FORMULA", "E_n=n^2*h^2/(8*m*L^2)"),
        make_step("E", n, 2, n_sq),
        make_step("E", h, 2, h_sq),
        make_step("M", n_sq, h_sq, numerator),
        make_step("E", length, 2, length_sq),
        make_step("M", 8, mass, eight_m),
        make_step("M", eight_m, length_sq, denominator),
        make_step("D", numerator, denominator, fraction_text(energy)),
    ]
    answer = f"E_{n}={fraction_text(energy)} J"
    return steps, answer


def expected_transition(problem):
    n_high, n_low, h, c, mass, length = (
        int(value) for value in TRANSITION_RE.fullmatch(problem).groups()
    )
    n_low_sq = n_low ** 2
    n_high_sq = n_high ** 2
    delta_n_sq = n_high_sq - n_low_sq
    length_sq = length ** 2
    eight_m = 8 * mass
    numerator_left = eight_m * length_sq
    numerator = numerator_left * c
    denominator = delta_n_sq * h
    wavelength = Fraction(numerator, denominator)
    steps = [
        make_step("BOX_SETUP", "transition_wavelength",
                  f"n_low={n_low}, n_high={n_high}", f"h={h}, c={c}"),
        make_step("BOX_SETUP", f"m={mass}, L={length}"),
        make_step("BOX_FORMULA",
                  "lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)"),
        make_step("E", n_low, 2, n_low_sq),
        make_step("E", n_high, 2, n_high_sq),
        make_step("S", n_high_sq, n_low_sq, delta_n_sq),
        make_step("E", length, 2, length_sq),
        make_step("M", 8, mass, eight_m),
        make_step("M", eight_m, length_sq, numerator_left),
        make_step("M", numerator_left, c, numerator),
        make_step("M", delta_n_sq, h, denominator),
        make_step("D", numerator, denominator, fraction_text(wavelength)),
    ]
    answer = f"lambda={fraction_text(wavelength)} m"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ENERGY_RE.fullmatch(problem):
        steps, answer = expected_energy(problem)
    else:
        steps, answer = expected_transition(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestParticleInBoxGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ParticleInBoxGenerator()

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
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ParticleInBoxGenerator.VARIANTS:
            result = ParticleInBoxGenerator(variant).generate()
            self.assertEqual(result["operation"], f"particle_in_box_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ParticleInBoxGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
