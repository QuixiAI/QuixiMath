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

from generators.arc_sector_generator import ArcSectorGenerator
from helpers import DELIM


WORDS = r"[a-z ]+"
ANG = r"\d*π(?:/\d+)?"


def rx(pattern):
    return re.compile(pattern)


# One regex per phrasing.  The oracle never imports the templates.
DEGREE_PATTERNS = [
    ("arc", rx(r"Circle (?P<L>[A-Z]) has radius (?P<r>\d+)\. Find the "
               r"length of the arc cut off by a central angle of "
               r"(?P<theta>\d+)°\. Give the exact answer in terms of π\.")),
    ("arc", rx(r"A circular (?P<noun>" + WORDS + r") has radius (?P<r>\d+)\. "
               r"A central angle of (?P<theta>\d+)° cuts off an arc along "
               r"its edge\. Find the exact arc length in terms of π\.")),
    ("arc", rx(r"On a circular (?P<noun>" + WORDS + r") of radius "
               r"(?P<r>\d+), an arc is intercepted by a central angle "
               r"measuring (?P<theta>\d+)°\. How long is that arc\? Give "
               r"the exact answer in terms of π\.")),
    ("arc", rx(r"A central angle of (?P<theta>\d+)° is drawn in circle "
               r"(?P<L>[A-Z]), which has radius (?P<r>\d+)\. Find the "
               r"exact length of the intercepted arc in terms of π\.")),
    ("arc", rx(r"A circular (?P<noun>" + WORDS + r") has radius "
               r"(?P<r>\d+)\. Find the exact length, in terms of π, of "
               r"the arc swept out by a turn of (?P<theta>\d+)° about the "
               r"center\.")),
    ("sector", rx(r"Circle (?P<L>[A-Z]) has radius (?P<r>\d+)\. Find the "
                  r"area of the sector with central angle (?P<theta>\d+)°\. "
                  r"Give the exact answer in terms of π\.")),
    ("sector", rx(r"A circular (?P<noun>" + WORDS + r") has radius "
                  r"(?P<r>\d+)\. Find the exact area, in terms of π, of "
                  r"the sector with a central angle of (?P<theta>\d+)°\.")),
    ("sector", rx(r"A sector of (?P<theta>\d+)° is cut from a circular "
                  r"(?P<noun>" + WORDS + r") of radius (?P<r>\d+)\. What "
                  r"is its exact area in terms of π\?")),
    ("sector", rx(r"In circle (?P<L>[A-Z]) of radius (?P<r>\d+), a central "
                  r"angle of (?P<theta>\d+)° determines a sector\. Find "
                  r"the sector's exact area in terms of π\.")),
    ("sector", rx(r"A circular (?P<noun>" + WORDS + r") of radius "
                  r"(?P<r>\d+) has two radii meeting at a central angle of "
                  r"(?P<theta>\d+)°\. Find the exact area of the sector "
                  r"they bound, in terms of π\.")),
]

RADIAN_PATTERNS = [
    ("arc_radians", rx(r"Circle (?P<L>[A-Z]) has radius (?P<r>\d+)\. A "
                       r"central angle of (?P<ang>" + ANG + r") radians "
                       r"cuts off an arc\. Find its exact length in terms "
                       r"of π\.")),
    ("arc_radians", rx(r"A circular (?P<noun>" + WORDS + r") has radius "
                       r"(?P<r>\d+)\. Find the exact arc length, in terms "
                       r"of π, intercepted by a central angle of (?P<ang>" +
                       ANG + r") radians\.")),
    ("arc_radians", rx(r"In circle (?P<L>[A-Z]) of radius (?P<r>\d+), a "
                       r"central angle measures (?P<ang>" + ANG + r") "
                       r"radians\. Find the exact length of the arc it "
                       r"intercepts, in terms of π\.")),
    ("arc_radians", rx(r"A point on the rim of a circular (?P<noun>" +
                       WORDS + r") of radius (?P<r>\d+) turns through "
                       r"(?P<ang>" + ANG + r") radians\. Find the exact "
                       r"distance it travels, in terms of π\.")),
    ("sector_radians", rx(r"Circle (?P<L>[A-Z]) has radius (?P<r>\d+)\. "
                          r"Find the exact area, in terms of π, of the "
                          r"sector with central angle (?P<ang>" + ANG +
                          r") radians\.")),
    ("sector_radians", rx(r"A circular (?P<noun>" + WORDS + r") has radius "
                          r"(?P<r>\d+)\. A central angle of (?P<ang>" +
                          ANG + r") radians bounds a sector\. Find its "
                          r"exact area in terms of π\.")),
    ("sector_radians", rx(r"In circle (?P<L>[A-Z]) of radius (?P<r>\d+), a "
                          r"sector has central angle (?P<ang>" + ANG +
                          r") radians\. Find the sector's exact area in "
                          r"terms of π\.")),
    ("sector_radians", rx(r"A sector of a circular (?P<noun>" + WORDS +
                          r") of radius (?P<r>\d+) has central angle "
                          r"(?P<ang>" + ANG + r") radians\. Give its exact "
                          r"area in terms of π\.")),
]

ALL_PATTERNS = DEGREE_PATTERNS + RADIAN_PATTERNS


def parse(problem):
    hits = [(variant, index, m.groupdict())
            for index, (variant, pattern) in enumerate(ALL_PATTERNS)
            for m in [pattern.fullmatch(problem)] if m]
    if len(hits) != 1:
        raise AssertionError(f"{len(hits)} phrasings matched: {problem!r}")
    return hits[0]


def parse_pi(text):
    """'5π/6' -> Fraction(5, 6); 'π' -> 1; '3π' -> 3."""
    match = re.fullmatch(r"(\d*)π(?:/(\d+))?", text)
    assert match, text
    num = int(match.group(1)) if match.group(1) else 1
    den = int(match.group(2)) if match.group(2) else 1
    return Fraction(num, den)


def render_pi(fr):
    """Independent re-implementation of the π rendering convention."""
    if fr.denominator == 1:
        return "π" if fr == 1 else f"{fr.numerator}π"
    head = "π" if fr.numerator == 1 else f"{fr.numerator}π"
    return f"{head}/{fr.denominator}"


def oracle(problem):
    """Solve from the text by the radian route: L = rθ, A = r²θ/2."""
    variant, _, fields = parse(problem)
    r = Fraction(int(fields["r"]))
    if "theta" in fields:
        # degrees -> radians: θ_rad = θπ/180 (never θ/360 · 2π)
        theta = Fraction(int(fields["theta"]), 180)
    else:
        theta = parse_pi(fields["ang"])
    coefficient = r * theta if variant.startswith("arc") \
        else r * r * theta / 2
    return variant, render_pi(coefficient), coefficient


class TestArcSectorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ArcSectorGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        seen = set()
        for _ in range(2000):
            result = self.gen.generate()
            variant, answer, coefficient = oracle(result["problem"])
            seen.add(variant)
            self.assertEqual(result["operation"], f"{variant}_measure",
                             result["problem"])
            self.assertEqual(answer, result["final_answer"],
                             result["problem"])
            # numeric cross-check against the float value of the answer
            self.assertAlmostEqual(float(coefficient) * math.pi,
                                   self._float_value(result["problem"]),
                                   places=8, msg=result["problem"])
        self.assertEqual(seen, set(ArcSectorGenerator.VARIANTS))

    @staticmethod
    def _float_value(problem):
        variant, _, fields = parse(problem)
        r = int(fields["r"])
        if "theta" in fields:
            radians = math.radians(int(fields["theta"]))
        else:
            radians = float(parse_pi(fields["ang"])) * math.pi
        return r * radians if variant.startswith("arc") \
            else 0.5 * r * r * radians

    def test_every_phrasing_is_reachable_and_unambiguous(self):
        seen = set()
        for _ in range(4000):
            _, index, _ = parse(self.gen.generate()["problem"])
            seen.add(index)
        self.assertEqual(seen, set(range(len(ALL_PATTERNS))))

    def test_setup_step_matches_problem_text(self):
        for _ in range(400):
            result = self.gen.generate()
            variant, _, fields = parse(result["problem"])
            setup = result["steps"][0].split(DELIM)
            self.assertEqual(setup[0], "ARC_SETUP")
            self.assertIn(f"r = {fields['r']}", setup[1])
            if "theta" in fields:
                self.assertIn(f"{fields['theta']}°", setup[1])
            else:
                self.assertIn(f"{fields['ang']} rad", setup[1])
            self.assertEqual(setup[2], "arc length"
                             if variant.startswith("arc") else "sector area")

    def test_angle_fraction_reduced(self):
        gen = ArcSectorGenerator("sector")
        for _ in range(300):
            result = gen.generate()
            fr = next(s for s in result["steps"]
                      if s.startswith(f"FRAC_REDUCE{DELIM}"))
            f = fr.split(DELIM)
            theta = int(f[1].split("/")[0])
            self.assertEqual(Fraction(theta, 360), Fraction(f[2]), fr)

    def test_pi_coeff_step_strips_pi(self):
        for variant in ("arc_radians", "sector_radians"):
            gen = ArcSectorGenerator(variant)
            for _ in range(200):
                result = gen.generate()
                fr = next(s for s in result["steps"]
                          if s.startswith(f"PI_COEFF{DELIM}"))
                f = fr.split(DELIM)
                self.assertEqual(parse_pi(f[1]), Fraction(f[2]), fr)

    def test_step_arithmetic_exact(self):
        for _ in range(600):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(Fraction(f[1]) * Fraction(f[2]),
                                     Fraction(f[3]), s)
                elif f[0] == "E":
                    self.assertEqual(int(f[1]) ** int(f[2]), int(f[3]), s)

    def test_last_arithmetic_step_produces_the_answer(self):
        for _ in range(400):
            result = self.gen.generate()
            _, _, coefficient = oracle(result["problem"])
            last_math = [s for s in result["steps"]
                         if s.split(DELIM)[0] in ("M", "E")][-1]
            self.assertEqual(Fraction(last_math.split(DELIM)[3]),
                             coefficient, last_math)

    def test_fraction_pi_answers_occur(self):
        kinds = set()
        for _ in range(200):
            kinds.add("/" in self.gen.generate()["final_answer"])
        self.assertEqual(kinds, {True, False})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(400):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {f"{v}_measure"
                               for v in ArcSectorGenerator.VARIANTS})

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ArcSectorGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(400):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_answer_render_conventions(self):
        for _ in range(300):
            answer = self.gen.generate()["final_answer"]
            self.assertIn("π", answer)
            self.assertFalse(answer.startswith("1π"), answer)
            self.assertIsNone(re.search(r"π\d", answer), answer)
            self.assertEqual(render_pi(parse_pi(answer)), answer)


if __name__ == "__main__":
    unittest.main()
