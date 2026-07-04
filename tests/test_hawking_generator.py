import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hawking_generator import HawkingGenerator
from helpers import DELIM


TEMP_RE = re.compile(
    r"Given hbar=(\d+), c=(\d+), G=(\d+), M=(\d+), and k_B=(\d+), "
    r"compute the Hawking temperature "
    r"T_H=hbar\*c\^3/\(8π\*G\*M\*k_B\)\."
)
ENTROPY_RE = re.compile(
    r"Given k_B=(\d+), c=(\d+), A=(\d+), hbar=(\d+), and G=(\d+), "
    r"compute the Bekenstein-Hawking entropy "
    r"S_BH=k_B\*c\^3\*A/\(4\*hbar\*G\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    coeff = Fraction(value)
    if coeff.denominator == 1:
        return f"{coeff.numerator}/π"
    return f"{coeff.numerator}/({coeff.denominator}π)"


def parse_problem(problem):
    match = TEMP_RE.fullmatch(problem)
    if match:
        return {
            "variant": "temperature",
            "hbar": int(match.group(1)),
            "c": int(match.group(2)),
            "G": int(match.group(3)),
            "M": int(match.group(4)),
            "k_b": int(match.group(5)),
        }
    match = ENTROPY_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "entropy",
        "k_b": int(match.group(1)),
        "c": int(match.group(2)),
        "area": int(match.group(3)),
        "hbar": int(match.group(4)),
        "G": int(match.group(5)),
    }


def expected_temperature(parts):
    hbar = parts["hbar"]
    c = parts["c"]
    G = parts["G"]
    M = parts["M"]
    k_b = parts["k_b"]
    c_cubed = c ** 3
    numerator = hbar * c_cubed
    den_8g = 8 * G
    den_8gm = den_8g * M
    denominator = den_8gm * k_b
    coeff = Fraction(numerator, denominator)
    value = over_pi_text(coeff)
    constants = f"hbar={hbar},c={c},G={G},M={M},k_B={k_b}"
    steps = [
        make_step("HAWKING_SETUP", "temperature",
                  "T_H=hbar*c^3/(8π*G*M*k_B)", constants),
        make_step("E", c, 3, c_cubed),
        make_step("M", hbar, c_cubed, numerator),
        make_step("M", 8, G, den_8g),
        make_step("M", den_8g, M, den_8gm),
        make_step("M", den_8gm, k_b, denominator),
        make_step("D", numerator, denominator, fraction_text(coeff)),
        make_step("PI_DEN", fraction_text(coeff), "π", value),
    ]
    answer = f"T_H = {value}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_entropy(parts):
    k_b = parts["k_b"]
    c = parts["c"]
    area = parts["area"]
    hbar = parts["hbar"]
    G = parts["G"]
    c_cubed = c ** 3
    left = k_b * c_cubed
    numerator = left * area
    den_4hbar = 4 * hbar
    denominator = den_4hbar * G
    entropy = Fraction(numerator, denominator)
    constants = f"k_B={k_b},c={c},A={area},hbar={hbar},G={G}"
    steps = [
        make_step("HAWKING_SETUP", "entropy",
                  "S_BH=k_B*c^3*A/(4*hbar*G)", constants),
        make_step("E", c, 3, c_cubed),
        make_step("M", k_b, c_cubed, left),
        make_step("M", left, area, numerator),
        make_step("M", 4, hbar, den_4hbar),
        make_step("M", den_4hbar, G, denominator),
        make_step("D", numerator, denominator, fraction_text(entropy)),
    ]
    answer = f"S_BH = {fraction_text(entropy)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "temperature":
        return expected_temperature(parts)
    return expected_entropy(parts)


class TestHawkingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HawkingGenerator()

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
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "PI_DEN":
                    self.assertEqual(fields[2], "π", raw_step)
                    self.assertEqual(over_pi_text(Fraction(fields[1])),
                                     fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in HawkingGenerator.VARIANTS:
            result = HawkingGenerator(variant).generate()
            self.assertEqual(result["operation"], f"hawking_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HawkingGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_temperature_and_entropy_both_seen(self):
        seen = {self.gen.generate()["operation"] for _ in range(100)}
        self.assertIn("hawking_temperature", seen)
        self.assertIn("hawking_entropy", seen)


if __name__ == "__main__":
    unittest.main()
