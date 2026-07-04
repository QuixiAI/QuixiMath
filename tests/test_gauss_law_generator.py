import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gauss_law_generator import GaussLawGenerator
from helpers import DELIM


SPHERE_RE = re.compile(
    r"A spherical Gaussian surface of radius r=(\d+) m encloses charge "
    r"Q=(\d+) C\. Use epsilon0=1 and Gauss's law to find the electric "
    r"field on the surface\."
)
LINE_RE = re.compile(
    r"An infinite line charge has lambda=(\d+) C/m\. A cylindrical "
    r"Gaussian surface has radius r=(\d+) m and length L=(\d+) m\. Use "
    r"epsilon0=1 to find the electric field\."
)
SHEET_RE = re.compile(
    r"An infinite sheet has surface charge density sigma=(\d+) C/m\^2\. "
    r"A pillbox Gaussian surface has cap area A=(\d+) m\^2\. Use "
    r"epsilon0=1 to find the electric field on each side\."
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


def expected_sphere(problem):
    radius, charge = (
        int(value) for value in SPHERE_RE.fullmatch(problem).groups()
    )
    radius_sq = radius ** 2
    area_coeff = 4 * radius_sq
    coeff = Fraction(charge, area_coeff)
    field = over_pi_text(coeff)
    steps = [
        make_step("GAUSS_SETUP", "sphere", f"Q={charge}", f"r={radius}"),
        make_step("GAUSS_FORMULA", "E*(4πr^2)=Q"),
        make_step("E", radius, 2, radius_sq),
        make_step("M", 4, radius_sq, area_coeff),
        make_step("D", charge, area_coeff, fraction_text(coeff)),
        make_step("PI_DEN", fraction_text(coeff), "π", field),
    ]
    answer = f"E={field} N/C outward-positive"
    return steps, answer


def expected_line(problem):
    line_density, radius, length = (
        int(value) for value in LINE_RE.fullmatch(problem).groups()
    )
    enclosed = line_density * length
    two_r = 2 * radius
    area_coeff = two_r * length
    coeff = Fraction(enclosed, area_coeff)
    field = over_pi_text(coeff)
    steps = [
        make_step("GAUSS_SETUP", "line_charge",
                  f"lambda={line_density}, r={radius}", f"L={length}"),
        make_step("GAUSS_FORMULA", "E*(2πrL)=lambda*L"),
        make_step("M", line_density, length, enclosed),
        make_step("M", 2, radius, two_r),
        make_step("M", two_r, length, area_coeff),
        make_step("D", enclosed, area_coeff, fraction_text(coeff)),
        make_step("PI_DEN", fraction_text(coeff), "π", field),
    ]
    answer = f"E={field} N/C outward-positive"
    return steps, answer


def expected_sheet(problem):
    sigma, area = (int(value) for value in SHEET_RE.fullmatch(problem).groups())
    enclosed = sigma * area
    flux_coeff = 2 * area
    field = Fraction(enclosed, flux_coeff)
    steps = [
        make_step("GAUSS_SETUP", "sheet_charge", f"sigma={sigma}",
                  f"A={area}"),
        make_step("GAUSS_FORMULA", "2*E*A=sigma*A"),
        make_step("M", sigma, area, enclosed),
        make_step("M", 2, area, flux_coeff),
        make_step("D", enclosed, flux_coeff, fraction_text(field)),
    ]
    answer = f"E={fraction_text(field)} N/C away from sheet"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SPHERE_RE.fullmatch(problem):
        steps, answer = expected_sphere(problem)
    elif LINE_RE.fullmatch(problem):
        steps, answer = expected_line(problem)
    else:
        steps, answer = expected_sheet(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestGaussLawGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GaussLawGenerator()

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
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "PI_DEN":
                    self.assertEqual(fields[2], "π", raw_step)
                    self.assertEqual(over_pi_text(Fraction(fields[1])),
                                     fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in GaussLawGenerator.VARIANTS:
            result = GaussLawGenerator(variant).generate()
            self.assertEqual(result["operation"], f"gauss_law_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GaussLawGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
