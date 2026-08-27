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


VALUE_RE = r"(?P<value>\d+(?:/\d+)?)"
UNIT_RE = r"(?P<unit>TeV|GeV|MeV|keV|eV)"
IUNIT_RE = r"(?P<unit>TeV|GeV|MeV|keV|eV)\^-1"
SUBJECT_RE = r"(?:[a-z ]+)"

# Independent copies of the phrasings; drift fails the coverage test.
TEMPLATES = {
    "energy": [
        "In natural units with hbar=c=1, {subject} has energy E={value} "
        "{unit}. Compute its mass m, length scale L=1/E, and time scale t=L.",
        "Working with hbar=c=1, {subject} carries energy E={value} {unit}. "
        "Give the mass m, the length scale L=1/E, and the time scale t=L.",
        "Set hbar=c=1. If {subject} has energy E={value} {unit}, find the "
        "mass m, the length scale L=1/E, and the time scale t=L.",
        "Natural units (hbar=c=1) are in use and {subject} is measured at "
        "energy E={value} {unit}. Report m, L=1/E, and t=L.",
        "Using hbar=c=1, convert the energy E={value} {unit} of {subject} "
        "into a mass m, a length scale L=1/E, and a time scale t=L.",
    ],
    "mass": [
        "In natural units with hbar=c=1, {subject} has mass m={value} {unit}. "
        "Compute its energy E, length scale L=1/E, and time scale t=L.",
        "Working with hbar=c=1, {subject} has rest mass m={value} {unit}. "
        "Give the energy E, the length scale L=1/E, and the time scale t=L.",
        "Set hbar=c=1. If {subject} has mass m={value} {unit}, find the "
        "energy E, the length scale L=1/E, and the time scale t=L.",
        "Natural units (hbar=c=1) are in use and {subject} has mass m={value} "
        "{unit}. Report E, L=1/E, and t=L.",
        "Using hbar=c=1, convert the mass m={value} {unit} of {subject} into "
        "an energy E, a length scale L=1/E, and a time scale t=L.",
    ],
    "length": [
        "In natural units with hbar=c=1, a length scale L={value} {iunit} is "
        "given. Compute E=1/L, mass m=E, and time scale t=L.",
        "Working with hbar=c=1, {subject} has size L={value} {iunit}. Give "
        "E=1/L, the mass m=E, and the time scale t=L.",
        "Set hbar=c=1. A length scale L={value} {iunit} describes {subject}; "
        "find E=1/L, m=E, and t=L.",
        "Natural units (hbar=c=1) are in use and {subject} spans L={value} "
        "{iunit}. Report E=1/L, m=E, and t=L.",
        "Using hbar=c=1, convert the length scale L={value} {iunit} of "
        "{subject} into an energy E=1/L, a mass m=E, and a time t=L.",
    ],
    "time": [
        "In natural units with hbar=c=1, a time scale t={value} {iunit} is "
        "given. Compute length L=t, energy E=1/t, and mass m=E.",
        "Working with hbar=c=1, {subject} lives for t={value} {iunit}. Give "
        "the length L=t, the energy E=1/t, and the mass m=E.",
        "Set hbar=c=1. A time scale t={value} {iunit} is attached to "
        "{subject}; find L=t, E=1/t, and m=E.",
        "Natural units (hbar=c=1) are in use and {subject} evolves on the "
        "time scale t={value} {iunit}. Report L=t, E=1/t, and m=E.",
        "Using hbar=c=1, convert the time scale t={value} {iunit} of "
        "{subject} into a length L=t, an energy E=1/t, and a mass m=E.",
    ],
    "cross_section": [
        "In natural units with hbar=c=1, {subject} has energy E={value} "
        "{unit}. Compute the length scale L=1/E and the geometric cross "
        "section sigma=L^2.",
        "Working with hbar=c=1, {subject} is probed at energy E={value} "
        "{unit}. Give L=1/E and sigma=L^2.",
        "Set hbar=c=1. At energy E={value} {unit}, {subject} has length scale "
        "L=1/E; find L and the cross section sigma=L^2.",
        "Natural units (hbar=c=1) are in use and {subject} scatters at energy "
        "E={value} {unit}. Report L=1/E and sigma=L^2.",
        "Using hbar=c=1, turn the energy E={value} {unit} of {subject} into a "
        "length scale L=1/E and a cross section sigma=L^2.",
    ],
}


def to_pattern(template):
    parts = re.split(r"(\{value\}|\{unit\}|\{iunit\}|\{subject\})", template)
    lookup = {"{value}": VALUE_RE, "{unit}": UNIT_RE, "{iunit}": IUNIT_RE,
              "{subject}": SUBJECT_RE}
    return "".join(lookup.get(part, re.escape(part)) for part in parts)


PATTERNS = {variant: [re.compile(to_pattern(t)) for t in templates]
            for variant, templates in TEMPLATES.items()}


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    for variant, patterns in PATTERNS.items():
        for index, pattern in enumerate(patterns):
            match = pattern.fullmatch(problem)
            if match:
                return {
                    "variant": variant,
                    "index": index,
                    "value": Fraction(match.group("value")),
                    "unit": match.group("unit"),
                }
    raise AssertionError(f"unparsed phrasing: {problem!r}")


def reciprocal(value):
    """1/x built by swapping numerator and denominator, not by division."""
    value = Fraction(value)
    assert value > 0
    return Fraction(value.denominator, value.numerator)


def expected_energy(value, unit, iunit):
    energy = value
    mass = energy
    length = reciprocal(energy)
    time = length
    steps = [
        make_step("NATURAL_SETUP", "energy", "hbar=1,c=1",
                  f"E={fraction_text(energy)} {unit}"),
        make_step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
        make_step("D", 1, fraction_text(energy), fraction_text(length)),
        make_step("UNIT_RULE", "c=1", "t=L", iunit),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"m = {fraction_text(mass)} {unit}, "
        f"L = {fraction_text(length)} {iunit}, "
        f"t = {fraction_text(time)} {iunit}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_mass(value, unit, iunit):
    mass = value
    energy = mass
    length = reciprocal(energy)
    time = length
    steps = [
        make_step("NATURAL_SETUP", "mass", "hbar=1,c=1",
                  f"m={fraction_text(mass)} {unit}"),
        make_step("UNIT_RULE", "c=1", "E=m", f"energy uses {unit}"),
        make_step("M", fraction_text(mass), 1, fraction_text(energy)),
        make_step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
        make_step("D", 1, fraction_text(energy), fraction_text(length)),
        make_step("UNIT_RULE", "c=1", "t=L", iunit),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"E = {fraction_text(energy)} {unit}, "
        f"L = {fraction_text(length)} {iunit}, "
        f"t = {fraction_text(time)} {iunit}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_length(value, unit, iunit):
    length = value
    energy = reciprocal(length)
    mass = energy
    time = length
    steps = [
        make_step("NATURAL_SETUP", "length", "hbar=1,c=1",
                  f"L={fraction_text(length)} {iunit}"),
        make_step("UNIT_RULE", "hbar=1", "E=1/L", unit),
        make_step("D", 1, fraction_text(length), fraction_text(energy)),
        make_step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("UNIT_RULE", "c=1", "t=L", iunit),
        make_step("M", fraction_text(length), 1, fraction_text(time)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"E = {fraction_text(energy)} {unit}, "
        f"m = {fraction_text(mass)} {unit}, "
        f"t = {fraction_text(time)} {iunit}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_time(value, unit, iunit):
    time = value
    length = time
    energy = reciprocal(length)
    mass = energy
    steps = [
        make_step("NATURAL_SETUP", "time", "hbar=1,c=1",
                  f"t={fraction_text(time)} {iunit}"),
        make_step("UNIT_RULE", "c=1", "L=t", iunit),
        make_step("M", fraction_text(time), 1, fraction_text(length)),
        make_step("UNIT_RULE", "hbar=1", "E=1/L", unit),
        make_step("D", 1, fraction_text(length), fraction_text(energy)),
        make_step("UNIT_RULE", "c=1", "m=E", f"mass uses {unit}"),
        make_step("M", fraction_text(energy), 1, fraction_text(mass)),
        make_step("M", fraction_text(energy), fraction_text(length), 1),
    ]
    answer = (
        f"L = {fraction_text(length)} {iunit}, "
        f"E = {fraction_text(energy)} {unit}, "
        f"m = {fraction_text(mass)} {unit}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_cross_section(value, unit, iunit):
    energy = value
    length = reciprocal(energy)
    sigma = length * length
    sq_unit = f"{unit}^-2"
    steps = [
        make_step("NATURAL_SETUP", "cross section", "hbar=1,c=1",
                  f"E={fraction_text(energy)} {unit}"),
        make_step("UNIT_RULE", "hbar=1", "L=1/E", iunit),
        make_step("D", 1, fraction_text(energy), fraction_text(length)),
        make_step("UNIT_RULE", "area", "sigma=L^2", sq_unit),
        make_step("E", fraction_text(length), 2, fraction_text(sigma)),
        make_step("M", fraction_text(sigma), fraction_text(energy * energy),
                  1),
    ]
    answer = (
        f"L = {fraction_text(length)} {iunit}, "
        f"sigma = {fraction_text(sigma)} {sq_unit}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


BUILDERS = {
    "energy": expected_energy,
    "mass": expected_mass,
    "length": expected_length,
    "time": expected_time,
    "cross_section": expected_cross_section,
}


def expected_flow(example):
    parts = parse_problem(example["problem"])
    unit = parts["unit"]
    return BUILDERS[parts["variant"]](parts["value"], unit, f"{unit}^-1")


class TestNaturalUnitsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = NaturalUnitsGenerator()

    def test_output_contract(self):
        for _ in range(50):
            result = self.gen.generate()
            for key in ("problem_id", "operation", "problem", "steps",
                        "final_answer"):
                self.assertIn(key, result)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                             result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(800):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_dimensional_identities_hold(self):
        for _ in range(400):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            numbers = re.findall(r"= (\d+(?:/\d+)?) ", result["final_answer"])
            values = [Fraction(n) for n in numbers]
            if parts["variant"] == "cross_section":
                length, sigma = values
                self.assertEqual(length * parts["value"], 1)
                self.assertEqual(sigma, length * length)
            elif parts["variant"] in ("energy", "mass"):
                first, length, time = values
                self.assertEqual(first, parts["value"])
                self.assertEqual(length * parts["value"], 1)
                self.assertEqual(time, length)
            elif parts["variant"] == "length":
                a, b, c = values
                self.assertEqual(a * parts["value"], 1)
                self.assertIn(parts["value"], (b, c))
            else:
                length, energy, mass = values
                self.assertEqual(length, parts["value"])
                self.assertEqual(energy * parts["value"], 1)
                self.assertEqual(mass, energy)

    def test_arithmetic_steps(self):
        for _ in range(400):
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
        for variant in NaturalUnitsGenerator.VARIANTS:
            gen = NaturalUnitsGenerator(variant)
            for _ in range(20):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"natural_units_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NaturalUnitsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_every_variant_phrasing_and_unit_appears(self):
        seen_ops = set()
        seen_phrasings = set()
        seen_units = set()
        for _ in range(1500):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            seen_ops.add(result["operation"])
            seen_phrasings.add((parts["variant"], parts["index"]))
            seen_units.add(parts["unit"])
        self.assertEqual(
            seen_ops,
            {f"natural_units_{v}" for v in NaturalUnitsGenerator.VARIANTS})
        self.assertEqual(
            seen_phrasings,
            {(variant, index)
             for variant, templates in TEMPLATES.items()
             for index in range(len(templates))})
        self.assertEqual(seen_units, {"TeV", "GeV", "MeV", "keV", "eV"})

    def test_deterministic_under_seed(self):
        random.seed(13)
        first = [self.gen.generate()["problem"] for _ in range(30)]
        random.seed(13)
        second = [self.gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
