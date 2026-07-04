import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.natural_units_generator import NaturalUnitsGenerator
from helpers import DELIM


ENERGY_RE = re.compile(
    r"In natural units with hbar=c=1, a particle has energy "
    r"E=([^ ]+) GeV\. Compute its mass m, length scale L=1/E, "
    r"and time scale t=L\."
)
MASS_RE = re.compile(
    r"In natural units with hbar=c=1, a particle has mass "
    r"m=([^ ]+) GeV\. Compute its energy E, length scale L=1/E, "
    r"and time scale t=L\."
)
LENGTH_RE = re.compile(
    r"In natural units with hbar=c=1, a length scale "
    r"L=([^ ]+) GeV\^-1 is given\. Compute E=1/L, mass m=E, "
    r"and time scale t=L\."
)
TIME_RE = re.compile(
    r"In natural units with hbar=c=1, a time scale "
    r"t=([^ ]+) GeV\^-1 is given\. Compute length L=t, "
    r"energy E=1/t, and mass m=E\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = ENERGY_RE.fullmatch(problem)
    if match:
        return {"variant": "energy", "energy": Fraction(match.group(1))}
    match = MASS_RE.fullmatch(problem)
    if match:
        return {"variant": "mass", "mass": Fraction(match.group(1))}
    match = LENGTH_RE.fullmatch(problem)
    if match:
        return {"variant": "length", "length": Fraction(match.group(1))}
    match = TIME_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "time", "time": Fraction(match.group(1))}


def expected_energy(energy):
    mass = energy
    length = Fraction(1, 1) / energy
    time = length
    steps = [
        make_step("NATURAL_SETUP", "energy", "hbar=1,c=1",
                  f"E={fraction_text(energy)} GeV"),
        make_step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("UNIT_RULE", "hbar=1", "L=1/E", "GeV^-1"),
        make_step("D", 1, fraction_text(energy), fraction_text(length)),
        make_step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"m = {fraction_text(mass)} GeV, "
        f"L = {fraction_text(length)} GeV^-1, "
        f"t = {fraction_text(time)} GeV^-1"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_mass(mass):
    energy = mass
    length = Fraction(1, 1) / energy
    time = length
    steps = [
        make_step("NATURAL_SETUP", "mass", "hbar=1,c=1",
                  f"m={fraction_text(mass)} GeV"),
        make_step("UNIT_RULE", "c=1", "E=m", "energy uses GeV"),
        make_step("M", fraction_text(mass), 1, fraction_text(energy)),
        make_step("UNIT_RULE", "hbar=1", "L=1/E", "GeV^-1"),
        make_step("D", 1, fraction_text(energy), fraction_text(length)),
        make_step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"E = {fraction_text(energy)} GeV, "
        f"L = {fraction_text(length)} GeV^-1, "
        f"t = {fraction_text(time)} GeV^-1"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_length(length):
    energy = Fraction(1, 1) / length
    mass = energy
    time = length
    steps = [
        make_step("NATURAL_SETUP", "length", "hbar=1,c=1",
                  f"L={fraction_text(length)} GeV^-1"),
        make_step("UNIT_RULE", "hbar=1", "E=1/L", "GeV"),
        make_step("D", 1, fraction_text(length), fraction_text(energy)),
        make_step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("UNIT_RULE", "c=1", "t=L", "GeV^-1"),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"E = {fraction_text(energy)} GeV, "
        f"m = {fraction_text(mass)} GeV, "
        f"t = {fraction_text(time)} GeV^-1"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_time(time):
    length = time
    energy = Fraction(1, 1) / length
    mass = energy
    steps = [
        make_step("NATURAL_SETUP", "time", "hbar=1,c=1",
                  f"t={fraction_text(time)} GeV^-1"),
        make_step("UNIT_RULE", "c=1", "L=t", "GeV^-1"),
        make_step("M", fraction_text(time), 1, fraction_text(length)),
        make_step("UNIT_RULE", "hbar=1", "E=1/L", "GeV"),
        make_step("D", 1, fraction_text(length), fraction_text(energy)),
        make_step("UNIT_RULE", "c=1", "m=E", "mass uses GeV"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"L = {fraction_text(length)} GeV^-1, "
        f"E = {fraction_text(energy)} GeV, "
        f"m = {fraction_text(mass)} GeV"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "energy":
        return expected_energy(parts["energy"])
    if parts["variant"] == "mass":
        return expected_mass(parts["mass"])
    if parts["variant"] == "length":
        return expected_length(parts["length"])
    return expected_time(parts["time"])


class TestNaturalUnitsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = NaturalUnitsGenerator()

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

    def test_variants_are_available(self):
        for variant in NaturalUnitsGenerator.VARIANTS:
            result = NaturalUnitsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"natural_units_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NaturalUnitsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(200)}
        self.assertEqual(
            seen,
            {"natural_units_energy", "natural_units_mass",
             "natural_units_length", "natural_units_time"},
        )


if __name__ == "__main__":
    unittest.main()
