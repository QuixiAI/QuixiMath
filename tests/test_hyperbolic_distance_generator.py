import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hyperbolic_distance_generator import HyperbolicDistanceGenerator
from helpers import DELIM


HALF_PLANE_RE = re.compile(
    r"In the Poincare half-plane, P=\((-?\d+),([^)]*)\) and "
    r"Q=\((-?\d+),([^)]*)\) lie on the same vertical geodesic\. "
    r"Use d=abs\(ln\(y_Q/y_P\)\) to find the hyperbolic distance\."
)
DISK_RE = re.compile(
    r"In the Poincare disk, P=\(0,0\) and Q=\(([^,]+),0\) lie on "
    r"a diameter\. Use d=ln\(\(1\+r\)/\(1-r\)\) to find the "
    r"hyperbolic distance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def ln_text(value):
    return f"ln({fraction_text(value)})"


def parse_problem(problem):
    match = HALF_PLANE_RE.fullmatch(problem)
    if match:
        return {
            "variant": "half_plane",
            "x1": int(match.group(1)),
            "y1": Fraction(match.group(2)),
            "x2": int(match.group(3)),
            "y2": Fraction(match.group(4)),
        }
    match = DISK_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "disk_radial", "r": Fraction(match.group(1))}


def expected_half_plane(parts):
    ratio = parts["y2"] / parts["y1"]
    distance = ln_text(ratio)
    steps = [
        make_step("HYPERBOLIC_DISTANCE_SETUP", "half-plane",
                  f"P=({parts['x1']},{fraction_text(parts['y1'])})",
                  f"Q=({parts['x2']},{fraction_text(parts['y2'])})"),
        make_step("FORMULA",
                  "vertical geodesic distance = abs(ln(y_Q/y_P))"),
        make_step("D", fraction_text(parts["y2"]),
                  fraction_text(parts["y1"]), fraction_text(ratio)),
        make_step("LOG_EVAL", fraction_text(ratio), distance),
    ]
    answer = f"distance = {distance}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_disk(parts):
    r = parts["r"]
    one_plus = 1 + r
    one_minus = 1 - r
    ratio = one_plus / one_minus
    distance = ln_text(ratio)
    steps = [
        make_step("HYPERBOLIC_DISTANCE_SETUP", "disk",
                  "P=(0,0)", f"Q=({fraction_text(r)},0)"),
        make_step("FORMULA", "radial disk distance = ln((1+r)/(1-r))"),
        make_step("A", 1, fraction_text(r), fraction_text(one_plus)),
        make_step("S", 1, fraction_text(r), fraction_text(one_minus)),
        make_step("D", fraction_text(one_plus), fraction_text(one_minus),
                  fraction_text(ratio)),
        make_step("LOG_EVAL", fraction_text(ratio), distance),
    ]
    answer = f"distance = {distance}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "half_plane":
        return expected_half_plane(parts)
    return expected_disk(parts)


class TestHyperbolicDistanceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HyperbolicDistanceGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("half_plane", "disk_radial"):
            gen = HyperbolicDistanceGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"hyperbolic_distance_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HyperbolicDistanceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
