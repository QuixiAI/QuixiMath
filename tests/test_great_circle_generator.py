import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.great_circle_generator import GreatCircleGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"On a sphere of radius (\d+), point A is at latitude (-?\d+) deg, "
    r"longitude (-?\d+) deg, and point B is at latitude (-?\d+) deg, "
    r"longitude (-?\d+) deg\. The longitude difference is (\d+) deg\. "
    r"Given sin\(lat1\)=([^,]+), sin\(lat2\)=([^,]+), "
    r"cos\(lat1\)=([^,]+), cos\(lat2\)=([^,]+), cos\(delta\)=([^,]+), "
    r"and arccos\(([^)]+)\)=([^,]+), find the great-circle distance\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def exact_value(text):
    if text == "sqrt(3)/2":
        return Fraction(0), Fraction(1, 2)
    if text == "-sqrt(3)/2":
        return Fraction(0), Fraction(-1, 2)
    return Fraction(text), Fraction(0)


def exact_text(value):
    rational, sqrt3 = value
    if sqrt3 == 0:
        return str(rational)
    if rational == 0:
        if sqrt3 == 1:
            return "sqrt(3)"
        if sqrt3 == -1:
            return "-sqrt(3)"
        if sqrt3 == Fraction(1, 2):
            return "sqrt(3)/2"
        if sqrt3 == Fraction(-1, 2):
            return "-sqrt(3)/2"
        return f"{sqrt3}*sqrt(3)"
    raise AssertionError(value)


def exact_mul(left, right):
    a, b = exact_value(left)
    c, d = exact_value(right)
    return exact_text((a * c + 3 * b * d, a * d + b * c))


def exact_add(left, right):
    a, b = exact_value(left)
    c, d = exact_value(right)
    return exact_text((a + c, b + d))


def parse_pi(text):
    if text == "0":
        return Fraction(0)
    if text == "pi":
        return Fraction(1)
    if text == "-pi":
        return Fraction(-1)
    match = re.fullmatch(r"(-?\d+)pi", text)
    if match:
        return Fraction(int(match.group(1)))
    match = re.fullmatch(r"(-?\d*)pi/(\d+)", text)
    if match:
        numerator = match.group(1)
        if numerator in ("", "+"):
            top = 1
        elif numerator == "-":
            top = -1
        else:
            top = int(numerator)
        return Fraction(top, int(match.group(2)))
    raise AssertionError(text)


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


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "radius": int(match.group(1)),
        "lat1": int(match.group(2)),
        "lon1": int(match.group(3)),
        "lat2": int(match.group(4)),
        "lon2": int(match.group(5)),
        "delta": int(match.group(6)),
        "s1": match.group(7),
        "s2": match.group(8),
        "c1": match.group(9),
        "c2": match.group(10),
        "cd": match.group(11),
        "cos_c_supplied": match.group(12),
        "theta": match.group(13),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    sin_product = exact_mul(parts["s1"], parts["s2"])
    cos_pair = exact_mul(parts["c1"], parts["c2"])
    cos_product = exact_mul(cos_pair, parts["cd"])
    cos_c = exact_add(sin_product, cos_product)
    theta = parts["theta"]
    distance = pi_text(parts["radius"] * parse_pi(theta))
    steps = [
        make_step("GREAT_CIRCLE_SETUP", f"R={parts['radius']}",
                  f"A=({parts['lat1']},{parts['lon1']})",
                  f"B=({parts['lat2']},{parts['lon2']})"),
        make_step("SPHERICAL_COSINES",
                  "cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)"),
        make_step("TRIG_VALUE", f"sin(lat1)={parts['s1']}",
                  f"sin(lat2)={parts['s2']}",
                  f"cos(dlon)={parts['cd']}"),
        make_step("TRIG_VALUE", f"cos(lat1)={parts['c1']}",
                  f"cos(lat2)={parts['c2']}"),
        make_step("M", parts["s1"], parts["s2"], sin_product),
        make_step("M", parts["c1"], parts["c2"], cos_pair),
        make_step("M", cos_pair, parts["cd"], cos_product),
        make_step("A", sin_product, cos_product, cos_c),
        make_step("ARCCOS", f"cos(c)={cos_c}", f"c={theta}"),
        make_step("M", parts["radius"], theta, distance),
    ]
    answer = f"distance = {distance}"
    steps.append(make_step("Z", answer))
    return steps, answer, cos_c


class TestGreatCircleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GreatCircleGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "great_circle_distance")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer, _ = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_spherical_cosines_matches_supplied_arccos_input(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            _, _, cos_c = expected_flow(result)
            self.assertEqual(cos_c, parts["cos_c_supplied"],
                             result["problem"])

    def test_distance_is_radius_times_central_angle(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            distance = pi_text(parts["radius"] * parse_pi(parts["theta"]))
            self.assertEqual(result["final_answer"],
                             f"distance = {distance}")

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M" and "pi" not in fields[2]:
                    self.assertEqual(exact_mul(fields[1], fields[2]),
                                     fields[3], raw_step)
                elif fields[0] == "M":
                    self.assertEqual(pi_text(Fraction(fields[1]) *
                                             parse_pi(fields[2])),
                                     fields[3], raw_step)
                elif fields[0] == "A":
                    self.assertEqual(exact_add(fields[1], fields[2]),
                                     fields[3], raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
