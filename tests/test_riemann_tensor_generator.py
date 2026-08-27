import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.riemann_tensor_generator import RiemannTensorGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r".* For a 2-sphere of radius R=([^ ]+) at a point with "
    r"sin\(phi\)=([^ ]+) and cos\(phi\)=([^,]+), compute "
    r"R\^phi_theta phi theta, the Ricci entries, and scalar curvature\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    radius = Fraction(match.group(1))
    sin_phi = Fraction(match.group(2))
    cos_phi = Fraction(match.group(3))
    assert sin_phi > 0 and cos_phi > 0
    assert sin_phi ** 2 + cos_phi ** 2 == 1
    return radius, sin_phi, cos_phi


def expected_flow(example):
    radius, sin_phi, cos_phi = parse_problem(example["problem"])
    sin_sq = sin_phi ** 2
    cos_sq = cos_phi ** 2
    sin_cos = sin_phi * cos_phi
    gamma_phi = -sin_cos
    gamma_theta = cos_phi / sin_phi
    deriv_gamma = sin_sq - cos_sq
    radius_sq = radius ** 2
    inv_radius_sq = Fraction(1, radius_sq)
    gamma_product = gamma_phi * gamma_theta
    riemann_phi = deriv_gamma - gamma_product
    inverse_theta = inv_radius_sq / sin_sq
    theta_contraction = inverse_theta * riemann_phi
    scalar = 2 * inv_radius_sq
    steps = [
        make_step("RIEMANN_SETUP", "sphere", f"R={fraction_text(radius)}",
                  f"sin(phi)={fraction_text(sin_phi)}, "
                  f"cos(phi)={fraction_text(cos_phi)}"),
        make_step("E", fraction_text(sin_phi), 2, fraction_text(sin_sq)),
        make_step("E", fraction_text(cos_phi), 2, fraction_text(cos_sq)),
        make_step("M", fraction_text(sin_phi), fraction_text(cos_phi),
                  fraction_text(sin_cos)),
        make_step("M", -1, fraction_text(sin_cos), fraction_text(gamma_phi)),
        make_step("D", fraction_text(cos_phi), fraction_text(sin_phi),
                  fraction_text(gamma_theta)),
        make_step("S", fraction_text(sin_sq), fraction_text(cos_sq),
                  fraction_text(deriv_gamma)),
        make_step("CHRISTOFFEL_VALUE", "Gamma^phi_thetatheta",
                  fraction_text(gamma_phi)),
        make_step("CHRISTOFFEL_VALUE", "Gamma^theta_phitheta",
                  fraction_text(gamma_theta)),
        make_step("DERIV", "d_phi Gamma^phi_thetatheta",
                  fraction_text(deriv_gamma)),
        make_step("M", fraction_text(gamma_phi),
                  fraction_text(gamma_theta),
                  fraction_text(gamma_product)),
        make_step("S", fraction_text(deriv_gamma),
                  fraction_text(gamma_product), fraction_text(riemann_phi)),
        make_step("RIEMANN_ENTRY", "R^phi_theta phi theta",
                  fraction_text(riemann_phi)),
        make_step("RIEMANN_ENTRY", "R^theta_phi theta phi", "1"),
        make_step("RICCI_ENTRY", "R_phiphi", "1"),
        make_step("RICCI_ENTRY", "R_thetatheta",
                  fraction_text(riemann_phi)),
        make_step("E", fraction_text(radius), 2, fraction_text(radius_sq)),
        make_step("D", 1, fraction_text(radius_sq),
                  fraction_text(inv_radius_sq)),
        make_step("INVERSE_METRIC", "g^phiphi=1/R^2",
                  "g^thetatheta=1/(R^2 sin^2(phi))"),
        make_step("D", fraction_text(inv_radius_sq), fraction_text(sin_sq),
                  fraction_text(inverse_theta)),
        make_step("M", fraction_text(inverse_theta),
                  fraction_text(riemann_phi),
                  fraction_text(theta_contraction)),
        make_step("CHECK", "g^thetatheta R_thetatheta",
                  fraction_text(theta_contraction), "sin^2 cancels"),
        make_step("A", fraction_text(inv_radius_sq),
                  fraction_text(inv_radius_sq), fraction_text(scalar)),
    ]
    answer = f"scalar curvature = {fraction_text(scalar)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRiemannTensorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = RiemannTensorGenerator()

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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
