import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.standing_wave_generator import StandingWaveGenerator
from helpers import DELIM


STRING_RE = re.compile(
    r"A string fixed at both ends has length L=(\d+) m and wave speed "
    r"v=(\d+) m/s\. Find wavelength lambda and frequency f for harmonic "
    r"n=(\d+)\."
)
OPEN_RE = re.compile(
    r"An open-open pipe has length L=(\d+) m and sound speed v=(\d+) m/s\. "
    r"Find wavelength lambda and frequency f for harmonic n=(\d+)\."
)
CLOSED_RE = re.compile(
    r"A closed-open pipe has length L=(\d+) m and sound speed v=(\d+) m/s\. "
    r"For mode k=(\d+), find the odd harmonic h, wavelength lambda, and "
    r"frequency f\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_fixed_fixed(problem, regex, setup_variant, boundary_text):
    length_raw, speed_raw, harmonic_raw = regex.fullmatch(problem).groups()
    length = int(length_raw)
    speed = int(speed_raw)
    harmonic = int(harmonic_raw)
    double_length = 2 * length
    wavelength = Fraction(double_length, harmonic)
    frequency = Fraction(speed, wavelength)
    steps = [
        make_step("STANDING_SETUP", setup_variant, f"n={harmonic}",
                  f"L={length}, v={speed}"),
        make_step("STANDING_BOUNDARY", boundary_text),
        make_step("STANDING_FORMULA", "lambda=2L/n, f=v/lambda"),
        make_step("M", 2, length, double_length),
        make_step("D", double_length, harmonic, fraction_text(wavelength)),
        make_step("D", speed, fraction_text(wavelength),
                  fraction_text(frequency)),
    ]
    answer = (
        f"lambda={fraction_text(wavelength)} m; "
        f"f={fraction_text(frequency)} Hz"
    )
    return steps, answer


def expected_closed(problem):
    length_raw, speed_raw, mode_raw = CLOSED_RE.fullmatch(problem).groups()
    length = int(length_raw)
    speed = int(speed_raw)
    mode = int(mode_raw)
    doubled_mode = 2 * mode
    harmonic = doubled_mode - 1
    four_length = 4 * length
    wavelength = Fraction(four_length, harmonic)
    frequency = Fraction(speed, wavelength)
    steps = [
        make_step("STANDING_SETUP", "closed_pipe", f"k={mode}",
                  f"L={length}, v={speed}"),
        make_step("STANDING_BOUNDARY", "closed-open pipe uses h=2k-1"),
        make_step("STANDING_FORMULA", "lambda=4L/h, f=v/lambda"),
        make_step("M", 2, mode, doubled_mode),
        make_step("S", doubled_mode, 1, harmonic),
        make_step("M", 4, length, four_length),
        make_step("D", four_length, harmonic, fraction_text(wavelength)),
        make_step("D", speed, fraction_text(wavelength),
                  fraction_text(frequency)),
    ]
    answer = (
        f"h={harmonic}; lambda={fraction_text(wavelength)} m; "
        f"f={fraction_text(frequency)} Hz"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if STRING_RE.fullmatch(problem):
        steps, answer = expected_fixed_fixed(
            problem,
            STRING_RE,
            "string_harmonic",
            "fixed-fixed string allows n=1,2,3,...",
        )
    elif OPEN_RE.fullmatch(problem):
        steps, answer = expected_fixed_fixed(
            problem,
            OPEN_RE,
            "open_pipe",
            "open-open pipe allows n=1,2,3,...",
        )
    elif CLOSED_RE.fullmatch(problem):
        steps, answer = expected_closed(problem)
    else:
        raise AssertionError(f"unrecognized problem: {problem}")
    steps.append(make_step("Z", answer))
    return steps, answer


class TestStandingWaveGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = StandingWaveGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in StandingWaveGenerator.VARIANTS:
            result = StandingWaveGenerator(variant).generate()
            self.assertEqual(result["operation"], f"standing_wave_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StandingWaveGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
