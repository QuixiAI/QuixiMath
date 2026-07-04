import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.conic_standard_form_generator import (
    ConicStandardFormGenerator,
)
from generators.parabola_features_generator import shift
from helpers import DELIM


def parse_general(eq):
    """'4x^2 + 9y^2 - 8x + 36y + 4 = 0' -> (A, B, D, E, F)."""
    left = eq.replace(" = 0", "")
    coefs = {"x^2": 0, "y^2": 0, "x": 0, "y": 0, "": 0}
    for sign, mag, sym in re.findall(
            r"([+-]?) ?(\d*)(x\^2|y\^2|x|y)?(?= |$)", left):
        if not mag and not sym:
            continue
        c = int(mag) if mag else 1
        if sign == "-":
            c = -c
        coefs[sym or ""] += c
    return (coefs["x^2"], coefs["y^2"], coefs["x"], coefs["y"], coefs[""])


def oracle_answer(example):
    """Completes the square independently from the general form."""
    m = re.fullmatch(r"Write in standard form: (.+)\.",
                     example["problem"])
    A, B, D, E, F = parse_general(m.group(1))
    h = Fraction(-D, 2 * A)
    k = Fraction(-E, 2 * B)
    assert h.denominator == 1 and k.denominator == 1
    h, k = h.numerator, k.numerator
    RHS = A * h * h + B * k * k - F
    if A == 1 and B == 1:
        r = math.isqrt(RHS)
        assert r * r == RHS
        return f"{shift('x', h)}^2 + {shift('y', k)}^2 = {RHS}"
    dx, rx = divmod(RHS, A)
    dy, ry = divmod(RHS, B)
    assert rx == 0 and ry == 0
    return f"{shift('x', h)}^2/{dx} + {shift('y', k)}^2/{dy} = 1"


class TestConicStandardFormGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ConicStandardFormGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: complete the square independently."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_complete_square_steps_are_correct(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "COMPLETE_SQUARE":
                    m1 = re.fullmatch(r"half of (-?\d+) = (-?\d+)", f[1])
                    self.assertIsNotNone(m1, s)
                    self.assertEqual(int(m1.group(1)),
                                     2 * int(m1.group(2)), s)
                    m2 = re.fullmatch(r"\((-?\d+)\)\^2 = (\d+)", f[2])
                    self.assertEqual(int(m2.group(1)) ** 2,
                                     int(m2.group(2)), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "D":
                    self.assertEqual(int(f[1]), int(f[2]) * int(f[3]), s)

    def test_ellipse_multiplies_added_squares(self):
        """The A·(half)^2 multiply-through appears for ellipses."""
        gen = ConicStandardFormGenerator("ellipse")
        for _ in range(200):
            result = gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("M"), 2)
            self.assertEqual(ops.count("FACTOR_GROUP"), 2)
            self.assertEqual(ops.count("COMPLETE_SQUARE"), 2)

    def test_circle_radius_is_integer(self):
        gen = ConicStandardFormGenerator("circle")
        for _ in range(200):
            result = gen.generate()
            rhs = int(result["final_answer"].split(" = ")[1])
            r = math.isqrt(rhs)
            self.assertEqual(r * r, rhs)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"conic_standard_form_circle",
                               "conic_standard_form_ellipse"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ConicStandardFormGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
