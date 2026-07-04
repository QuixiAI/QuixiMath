import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.schwarzschild_generator import SchwarzschildGenerator
from helpers import DELIM


RADIUS_RE = re.compile(
    r"Given G=(\d+), M=(\d+), and c=(\d+), compute the Schwarzschild "
    r"radius r_s=2GM/c\^2\."
)
DILATION_RE = re.compile(
    r"Given Schwarzschild radius r_s=(\d+) and radius r=([^,]+), compute "
    r"the time dilation factor sqrt\(1 - r_s/r\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = RADIUS_RE.fullmatch(problem)
    if match:
        return {
            "variant": "radius",
            "G": int(match.group(1)),
            "M": int(match.group(2)),
            "c": int(match.group(3)),
        }
    match = DILATION_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "time_dilation",
        "r_s": int(match.group(1)),
        "r": Fraction(match.group(2)),
    }


def expected_radius(G, M, c):
    numerator_left = 2 * G
    numerator = numerator_left * M
    c_sq = c ** 2
    radius = Fraction(numerator, c_sq)
    steps = [
        make_step("SCHWARZSCHILD_SETUP", "radius", f"G={G}",
                  f"M={M}", f"c={c}"),
        make_step("M", 2, G, numerator_left),
        make_step("M", numerator_left, M, numerator),
        make_step("E", c, 2, c_sq),
        make_step("D", numerator, c_sq, fraction_text(radius)),
    ]
    answer = f"r_s = {fraction_text(radius)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_dilation(r_s, radius):
    ratio = Fraction(r_s, 1) / radius
    inside = 1 - ratio
    root = sqrt_fraction(inside)
    steps = [
        make_step("SCHWARZSCHILD_SETUP", "time_dilation",
                  f"r_s={r_s}", f"r={fraction_text(radius)}"),
        make_step("D", r_s, fraction_text(radius), fraction_text(ratio)),
        make_step("S", 1, fraction_text(ratio), fraction_text(inside)),
        make_step("ROOT", f"sqrt({fraction_text(inside)})",
                  fraction_text(root)),
    ]
    answer = f"time dilation factor = {fraction_text(root)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def sqrt_fraction(value):
    num = int(value.numerator ** 0.5)
    den = int(value.denominator ** 0.5)
    assert num * num == value.numerator
    assert den * den == value.denominator
    return Fraction(num, den)


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "radius":
        return expected_radius(parts["G"], parts["M"], parts["c"])
    return expected_dilation(parts["r_s"], parts["r"])


class TestSchwarzschildGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SchwarzschildGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    inside = Fraction(fields[1].removeprefix("sqrt(").rstrip(")"))
                    root = Fraction(fields[2])
                    self.assertEqual(root * root, inside, raw_step)

    def test_variants_are_available(self):
        for variant in SchwarzschildGenerator.VARIANTS:
            result = SchwarzschildGenerator(variant).generate()
            self.assertEqual(result["operation"], f"schwarzschild_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SchwarzschildGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
