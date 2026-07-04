import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gaussian_curvature_generator import GaussianCurvatureGenerator
from helpers import DELIM


SPHERE_RE = re.compile(
    r"Find the Gaussian curvature of a sphere of radius (\d+)\."
)
SADDLE_RE = re.compile(
    r"For the saddle surface z=\((\d+)x\^2-(\d+)y\^2\)/2, "
    r"find the Gaussian curvature at the origin using the graph "
    r"curvature formula\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = SPHERE_RE.fullmatch(problem)
    if match:
        return {"variant": "sphere", "radius": int(match.group(1))}
    match = SADDLE_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "saddle", "a": int(match.group(1)),
            "b": int(match.group(2))}


def expected_sphere(parts):
    radius_sq = parts["radius"] ** 2
    curvature = Fraction(1, radius_sq)
    answer = f"K = {fraction_text(curvature)}"
    steps = [
        make_step("GAUSSIAN_CURVATURE_SETUP", "sphere",
                  f"R={parts['radius']}"),
        make_step("FORMULA", "K = 1/R^2"),
        make_step("E", parts["radius"], 2, radius_sq),
        make_step("D", 1, radius_sq, fraction_text(curvature)),
        make_step("CHECK", "positive curvature", fraction_text(curvature),
                  "sphere"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_saddle(parts):
    f_xx = parts["a"]
    f_yy = -parts["b"]
    f_xy = 0
    numerator_left = f_xx * f_yy
    numerator_right = f_xy ** 2
    numerator = numerator_left - numerator_right
    grad_sum = 1
    denominator = grad_sum ** 2
    curvature = Fraction(numerator, denominator)
    answer = f"K = {fraction_text(curvature)}"
    steps = [
        make_step("GAUSSIAN_CURVATURE_SETUP", "saddle",
                  f"z=({parts['a']}x^2-{parts['b']}y^2)/2",
                  "point=(0,0)"),
        make_step("FORMULA",
                  "K=(f_xx f_yy - f_xy^2)/(1+f_x^2+f_y^2)^2"),
        make_step("DERIV", "f_x=0, f_y=0", f"f_xx={f_xx}",
                  f"f_yy={f_yy}, f_xy={f_xy}"),
        make_step("M", f_xx, f_yy, numerator_left),
        make_step("E", f_xy, 2, numerator_right),
        make_step("S", numerator_left, numerator_right, numerator),
        make_step("A", 1, 0, grad_sum),
        make_step("E", grad_sum, 2, denominator),
        make_step("D", numerator, denominator, fraction_text(curvature)),
        make_step("CHECK", "negative curvature", fraction_text(curvature),
                  "saddle"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "sphere":
        return expected_sphere(parts)
    return expected_saddle(parts)


class TestGaussianCurvatureGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GaussianCurvatureGenerator()

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

    def test_variants_are_available(self):
        for variant in ("sphere", "saddle"):
            gen = GaussianCurvatureGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"gaussian_curvature_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GaussianCurvatureGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
