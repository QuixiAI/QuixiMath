import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.metric_arc_length_generator import MetricArcLengthGenerator
from helpers import DELIM


RADIAL_RE = re.compile(
    r"In polar coordinates with metric ds\^2=dr\^2\+r\^2 dtheta\^2, "
    r"find the length of the path theta=(\d+) deg from r=(\d+) to r=(\d+)\."
)
CIRCLE_RE = re.compile(
    r"In polar coordinates with metric ds\^2=dr\^2\+r\^2 dtheta\^2, "
    r"find the length of the path r=(\d+) from theta=0 to theta=(.+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def pi_text(multiplier):
    multiplier = Fraction(multiplier)
    if multiplier == 0:
        return "0"
    if multiplier == 1:
        return "pi"
    if multiplier == -1:
        return "-pi"
    if multiplier.denominator == 1:
        return f"{multiplier.numerator}pi"
    if multiplier.numerator == 1:
        return f"pi/{multiplier.denominator}"
    if multiplier.numerator == -1:
        return f"-pi/{multiplier.denominator}"
    return f"{multiplier.numerator}pi/{multiplier.denominator}"


def parse_pi(text):
    if text == "pi":
        return Fraction(1)
    match = re.fullmatch(r"(\d+)pi", text)
    if match:
        return Fraction(int(match.group(1)))
    match = re.fullmatch(r"pi/(\d+)", text)
    if match:
        return Fraction(1, int(match.group(1)))
    match = re.fullmatch(r"(\d+)pi/(\d+)", text)
    if match:
        return Fraction(int(match.group(1)), int(match.group(2)))
    raise AssertionError(text)


def parse_problem(problem):
    match = RADIAL_RE.fullmatch(problem)
    if match:
        return {"variant": "radial", "theta0": int(match.group(1)),
                "start": int(match.group(2)), "end": int(match.group(3))}
    match = CIRCLE_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "circle", "radius": int(match.group(1)),
            "theta": parse_pi(match.group(2)),
            "theta_text": match.group(2)}


def expected_radial(parts):
    length = parts["end"] - parts["start"]
    answer = f"length = {length}"
    steps = [
        make_step("METRIC_ARC_SETUP", "polar metric",
                  "ds^2=dr^2+r^2 dtheta^2",
                  f"theta={parts['theta0']} deg, "
                  f"r:{parts['start']}->{parts['end']}"),
        make_step("METRIC_RESTRICT", "dtheta=0", "ds^2=dr^2"),
        make_step("INTEGRAL_SETUP", "L = integral from r0 to r1 of 1 dr"),
        make_step("S", parts["end"], parts["start"], length),
        make_step("M", 1, length, length),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_circle(parts):
    radius_sq = parts["radius"] ** 2
    length_coeff = parts["radius"] * parts["theta"]
    answer = f"length = {pi_text(length_coeff)}"
    steps = [
        make_step("METRIC_ARC_SETUP", "polar metric",
                  "ds^2=dr^2+r^2 dtheta^2",
                  f"r={parts['radius']}, theta:0->{parts['theta_text']}"),
        make_step("METRIC_RESTRICT", "dr=0", "ds^2=r^2 dtheta^2"),
        make_step("E", parts["radius"], 2, radius_sq),
        make_step("ROOT", radius_sq, parts["radius"]),
        make_step("INTEGRAL_SETUP",
                  f"L = integral from 0 to {parts['theta_text']} of "
                  f"{parts['radius']} dtheta"),
        make_step("M", parts["radius"], parts["theta"], length_coeff),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "radial":
        return expected_radial(parts)
    return expected_circle(parts)


class TestMetricArcLengthGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MetricArcLengthGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in ("radial", "circle"):
            gen = MetricArcLengthGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"metric_arc_length_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MetricArcLengthGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
