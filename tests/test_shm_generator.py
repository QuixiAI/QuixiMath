import os
import re
import sys
import unittest
from fractions import Fraction
from math import isqrt

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.arc_sector_generator import pi_txt
from generators.shm_generator import SHMGenerator
from helpers import DELIM


SPRING_RE = re.compile(
    r"A mass-spring oscillator has m=(\d+) kg, k=(\d+) N/m, amplitude "
    r"A=(\d+) m, and is at displacement x=(\d+) m\. Find omega, period, "
    r"kinetic energy, and potential energy\."
)
PENDULUM_RE = re.compile(
    r"A small-angle pendulum uses g=10 m/s\^2 and length L=([^ ]+) m\. "
    r"Find angular frequency and period\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def exact_square_root(value):
    value = Fraction(value)
    root_num = isqrt(value.numerator)
    root_den = isqrt(value.denominator)
    assert root_num * root_num == value.numerator
    assert root_den * root_den == value.denominator
    return Fraction(root_num, root_den)


def expected_spring(problem):
    mass, spring_k, amplitude, displacement = (
        int(value) for value in SPRING_RE.fullmatch(problem).groups()
    )
    omega_sq = Fraction(spring_k, mass)
    omega = exact_square_root(omega_sq)
    assert omega.denominator == 1
    period_coeff = Fraction(2, omega.numerator)
    period = pi_txt(period_coeff)
    amplitude_sq = amplitude ** 2
    spring_amp = spring_k * amplitude_sq
    total_energy = Fraction(spring_amp, 2)
    displacement_sq = displacement ** 2
    spring_disp = spring_k * displacement_sq
    potential_energy = Fraction(spring_disp, 2)
    kinetic_energy = total_energy - potential_energy
    energy_sum = kinetic_energy + potential_energy
    steps = [
        make_step("SHM_SETUP", "mass_spring_energy",
                  f"m={mass}, k={spring_k}",
                  f"A={amplitude}, x={displacement}"),
        make_step("SHM_FORMULA", "omega^2=k/m"),
        make_step("D", spring_k, mass, fraction_text(omega_sq)),
        make_step("ROOT", fraction_text(omega_sq), omega.numerator),
        make_step("SHM_FORMULA", "T=2π/omega"),
        make_step("D", 2, omega.numerator, fraction_text(period_coeff)),
        make_step("PI_MULT", fraction_text(period_coeff), "π", period),
        make_step("SHM_FORMULA", "E_total=1/2*k*A^2"),
        make_step("E", amplitude, 2, amplitude_sq),
        make_step("M", spring_k, amplitude_sq, spring_amp),
        make_step("D", spring_amp, 2, fraction_text(total_energy)),
        make_step("SHM_FORMULA", "U=1/2*k*x^2"),
        make_step("E", displacement, 2, displacement_sq),
        make_step("M", spring_k, displacement_sq, spring_disp),
        make_step("D", spring_disp, 2, fraction_text(potential_energy)),
        make_step("S", fraction_text(total_energy),
                  fraction_text(potential_energy), fraction_text(kinetic_energy)),
        make_step("A", fraction_text(kinetic_energy),
                  fraction_text(potential_energy), fraction_text(energy_sum)),
        make_step("CHECK", "K+U", fraction_text(energy_sum),
                  f"E {fraction_text(total_energy)}"),
    ]
    answer = (
        f"omega={omega.numerator} rad/s; T={period} s; "
        f"K={fraction_text(kinetic_energy)} J; "
        f"U={fraction_text(potential_energy)} J"
    )
    return steps, answer


def expected_pendulum(problem):
    (length_raw,) = PENDULUM_RE.fullmatch(problem).groups()
    g = 10
    length = Fraction(length_raw)
    omega_sq = Fraction(g, length)
    omega = exact_square_root(omega_sq)
    assert omega.denominator == 1
    period_coeff = Fraction(2, omega.numerator)
    period = pi_txt(period_coeff)
    steps = [
        make_step("SHM_SETUP", "pendulum_period", f"g={g}",
                  f"L={fraction_text(length)}"),
        make_step("SHM_FORMULA", "omega^2=g/L"),
        make_step("D", g, fraction_text(length), fraction_text(omega_sq)),
        make_step("ROOT", fraction_text(omega_sq), omega.numerator),
        make_step("SHM_FORMULA", "T=2π/omega"),
        make_step("D", 2, omega.numerator, fraction_text(period_coeff)),
        make_step("PI_MULT", fraction_text(period_coeff), "π", period),
    ]
    answer = f"omega={omega.numerator} rad/s; T={period} s"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SPRING_RE.fullmatch(problem):
        steps, answer = expected_spring(problem)
    else:
        steps, answer = expected_pendulum(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSHMGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SHMGenerator()

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
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) * Fraction(fields[2]),
                                     Fraction(fields[1]), raw_step)
                elif fields[0] == "PI_MULT":
                    self.assertEqual(fields[2], "π", raw_step)
                    self.assertEqual(pi_txt(Fraction(fields[1])), fields[3],
                                     raw_step)

    def test_energy_checks_are_true(self):
        for _ in range(300):
            result = SHMGenerator("mass_spring_energy").generate()
            check = [
                raw for raw in result["steps"]
                if raw.startswith(f"CHECK{DELIM}K+U")
            ][0]
            _, _, computed, target = check.split(DELIM)
            self.assertEqual(Fraction(computed),
                             Fraction(target.removeprefix("E ")), check)

    def test_variants_are_available(self):
        for variant in SHMGenerator.VARIANTS:
            result = SHMGenerator(variant).generate()
            self.assertEqual(result["operation"], f"shm_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SHMGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
