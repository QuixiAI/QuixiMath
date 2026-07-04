import os
import re
import sys
import unittest
from fractions import Fraction
from math import isqrt

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.energy_conservation_generator import EnergyConservationGenerator
from helpers import DELIM


WORK_RE = re.compile(
    r"A (\d+) kg object starts at (\d+) m/s and net work ([^ ]+) J is "
    r"done on it\. Use the work-energy theorem to find the final speed\."
)
DROP_RE = re.compile(
    r"A (\d+) kg object is dropped from height (\d+) m\. Use g=10 m/s\^2 "
    r"and energy conservation to find impact speed and initial potential "
    r"energy\."
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


def expected_work(problem):
    mass_raw, vi_raw, work_raw = WORK_RE.fullmatch(problem).groups()
    mass = int(mass_raw)
    vi = int(vi_raw)
    work = Fraction(work_raw)
    vi_sq = vi ** 2
    two_work = 2 * work
    two_work_over_m = two_work / mass
    final_sq = vi_sq + two_work_over_m
    vf = exact_square_root(final_sq)
    steps = [
        make_step("ENERGY_SETUP", "work_energy", f"m={mass}",
                  f"vi={vi}, W={fraction_text(work)}"),
        make_step("ENERGY_FORMULA", "vf^2=vi^2+2W/m"),
        make_step("E", vi, 2, vi_sq),
        make_step("M", 2, fraction_text(work), fraction_text(two_work)),
        make_step("D", fraction_text(two_work), mass,
                  fraction_text(two_work_over_m)),
        make_step("A", vi_sq, fraction_text(two_work_over_m),
                  fraction_text(final_sq)),
        make_step("ROOT", fraction_text(final_sq), vf),
    ]
    assert vf.denominator == 1
    answer = f"vf={vf.numerator} m/s"
    return steps, answer


def expected_drop(problem):
    mass, height = (int(value) for value in DROP_RE.fullmatch(problem).groups())
    g = 10
    potential = mass * g * height
    two_g = 2 * g
    speed_sq = two_g * height
    speed = exact_square_root(speed_sq)
    steps = [
        make_step("ENERGY_SETUP", "gravity_drop", f"m={mass}",
                  f"h={height}, g={g}"),
        make_step("ENERGY_FORMULA", "mgh=1/2*m*v^2"),
        make_step("M", mass, g, mass * g),
        make_step("M", mass * g, height, potential),
        make_step("ENERGY_FORMULA", "v^2=2gh"),
        make_step("M", 2, g, two_g),
        make_step("M", two_g, height, speed_sq),
        make_step("ROOT", speed_sq, speed.numerator),
    ]
    assert speed.denominator == 1
    answer = f"impact speed={speed.numerator} m/s; potential energy={potential} J"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if WORK_RE.fullmatch(problem):
        steps, answer = expected_work(problem)
    else:
        steps, answer = expected_drop(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestEnergyConservationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = EnergyConservationGenerator()

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
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) * Fraction(fields[2]),
                                     Fraction(fields[1]), raw_step)

    def test_variants_are_available(self):
        for variant in EnergyConservationGenerator.VARIANTS:
            result = EnergyConservationGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"energy_conservation_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EnergyConservationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
