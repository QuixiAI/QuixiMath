import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.interference_generator import InterferenceGenerator
from helpers import DELIM


DOUBLE_RE = re.compile(
    r"A double-slit setup has order m=(\d+), wavelength lambda=(\d+) m, "
    r"screen distance L=(\d+) m, and slit spacing d=(\d+) m\. Find "
    r"fringe position y\."
)
GRATING_RE = re.compile(
    r"A diffraction grating has spacing d=(\d+) m\. For order m=(\d+) and "
    r"wavelength lambda=(\d+) m, find sin\(theta\)\."
)
FILM_RE = re.compile(
    r"A thin film has refractive index n=([^ ]+)\. For order m=(\d+) and "
    r"wavelength lambda=(\d+) m, use 2\*n\*t=m\*lambda to find thickness t\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_double(problem):
    order, wavelength, screen_distance, slit_spacing = (
        int(value) for value in DOUBLE_RE.fullmatch(problem).groups()
    )
    first_product = order * wavelength
    numerator = first_product * screen_distance
    fringe = Fraction(numerator, slit_spacing)
    steps = [
        make_step("INTERFERENCE_SETUP", "double_slit",
                  f"m={order}, lambda={wavelength}",
                  f"L={screen_distance}, d={slit_spacing}"),
        make_step("INTERFERENCE_FORMULA", "y=m*lambda*L/d"),
        make_step("M", order, wavelength, first_product),
        make_step("M", first_product, screen_distance, numerator),
        make_step("D", numerator, slit_spacing, fraction_text(fringe)),
    ]
    answer = f"y={fraction_text(fringe)} m"
    return steps, answer


def expected_grating(problem):
    spacing, order, wavelength = (
        int(value) for value in GRATING_RE.fullmatch(problem).groups()
    )
    numerator = order * wavelength
    sine = Fraction(numerator, spacing)
    steps = [
        make_step("INTERFERENCE_SETUP", "diffraction_grating",
                  f"m={order}, lambda={wavelength}", f"d={spacing}"),
        make_step("INTERFERENCE_FORMULA", "d*sin(theta)=m*lambda"),
        make_step("M", order, wavelength, numerator),
        make_step("D", numerator, spacing, fraction_text(sine)),
    ]
    answer = f"sin(theta)={fraction_text(sine)}"
    return steps, answer


def expected_film(problem):
    n_raw, order_raw, wavelength_raw = FILM_RE.fullmatch(problem).groups()
    refractive_index = Fraction(n_raw)
    order = int(order_raw)
    wavelength = int(wavelength_raw)
    numerator = order * wavelength
    denominator = 2 * refractive_index
    thickness = numerator / denominator
    steps = [
        make_step("INTERFERENCE_SETUP", "thin_film",
                  f"m={order}, lambda={wavelength}",
                  f"n={fraction_text(refractive_index)}"),
        make_step("INTERFERENCE_FORMULA", "2*n*t=m*lambda"),
        make_step("M", order, wavelength, numerator),
        make_step("M", 2, fraction_text(refractive_index),
                  fraction_text(denominator)),
        make_step("D", numerator, fraction_text(denominator),
                  fraction_text(thickness)),
    ]
    answer = f"t={fraction_text(thickness)} m"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if DOUBLE_RE.fullmatch(problem):
        steps, answer = expected_double(problem)
    elif GRATING_RE.fullmatch(problem):
        steps, answer = expected_grating(problem)
    else:
        steps, answer = expected_film(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestInterferenceGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = InterferenceGenerator()

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
        for variant in InterferenceGenerator.VARIANTS:
            result = InterferenceGenerator(variant).generate()
            self.assertEqual(result["operation"], f"interference_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            InterferenceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
