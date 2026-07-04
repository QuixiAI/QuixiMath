import os
import re
import sys
import unittest
import math
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.doppler_generator import DopplerGenerator
from helpers import DELIM


ACOUSTIC_RE = re.compile(
    r"A sound source emits f=(\d+) Hz\. Sound speed is v=(\d+) m/s, the "
    r"observer moves toward the source at v_observer=(\d+) m/s, and the "
    r"source moves toward the observer at v_source=(\d+) m/s\. Find f_obs\."
)
REL_RE = re.compile(
    r"A light source approaches with beta=([^ ]+) and emits f=(\d+) Hz\. "
    r"Use the relativistic Doppler formula to find f_obs\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_acoustic(problem):
    frequency, sound_speed, observer_speed, source_speed = (
        int(value) for value in ACOUSTIC_RE.fullmatch(problem).groups()
    )
    top = sound_speed + observer_speed
    bottom = sound_speed - source_speed
    numerator = frequency * top
    observed = Fraction(numerator, bottom)
    steps = [
        make_step("DOPPLER_SETUP", "acoustic_toward",
                  f"f={frequency}, v={sound_speed}",
                  f"v_observer={observer_speed}, v_source={source_speed}"),
        make_step("DOPPLER_FORMULA",
                  "f_obs=f*(v+v_observer)/(v-v_source)"),
        make_step("A", sound_speed, observer_speed, top),
        make_step("S", sound_speed, source_speed, bottom),
        make_step("M", frequency, top, numerator),
        make_step("D", numerator, bottom, fraction_text(observed)),
    ]
    answer = f"f_obs={fraction_text(observed)} Hz"
    return steps, answer


def expected_relativistic(problem):
    beta_raw, frequency_raw = REL_RE.fullmatch(problem).groups()
    beta = Fraction(beta_raw)
    frequency = int(frequency_raw)
    one_plus = 1 + beta
    one_minus = 1 - beta
    ratio = one_plus / one_minus
    assert ratio.denominator == 1
    factor = math.isqrt(ratio.numerator)
    assert factor * factor == ratio.numerator
    factor_sq = factor ** 2
    beta_num = factor_sq - 1
    beta_den = factor_sq + 1
    observed = frequency * factor
    steps = [
        make_step("DOPPLER_SETUP", "relativistic_approach",
                  f"f={frequency}", f"beta={fraction_text(beta)}"),
        make_step("DOPPLER_FORMULA",
                  "f_obs=f*sqrt((1+beta)/(1-beta))"),
        make_step("E", factor, 2, factor_sq),
        make_step("S", factor_sq, 1, beta_num),
        make_step("A", factor_sq, 1, beta_den),
        make_step("A", 1, fraction_text(beta), fraction_text(one_plus)),
        make_step("S", 1, fraction_text(beta), fraction_text(one_minus)),
        make_step("D", fraction_text(one_plus), fraction_text(one_minus),
                  fraction_text(ratio)),
        make_step("ROOT", f"sqrt({fraction_text(ratio)})", factor),
        make_step("M", frequency, factor, observed),
    ]
    answer = f"f_obs={observed} Hz"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ACOUSTIC_RE.fullmatch(problem):
        steps, answer = expected_acoustic(problem)
    else:
        steps, answer = expected_relativistic(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestDopplerGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = DopplerGenerator()

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
                    root = int(fields[2])
                    radicand = Fraction(
                        fields[1].removeprefix("sqrt(").rstrip(")")
                    )
                    self.assertEqual(root * root, radicand, raw_step)

    def test_variants_are_available(self):
        for variant in DopplerGenerator.VARIANTS:
            result = DopplerGenerator(variant).generate()
            self.assertEqual(result["operation"], f"doppler_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DopplerGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
