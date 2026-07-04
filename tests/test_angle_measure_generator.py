import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.angle_measure_generator import AngleMeasureGenerator
from generators.arc_sector_generator import pi_txt
from helpers import DELIM


def parse_pi(txt):
    """'5π/6' -> Fraction(5, 6); 'π' -> 1; '2π' -> 2."""
    m = re.fullmatch(r"(?:(\d+))?π(?:/(\d+))?", txt)
    assert m, txt
    return Fraction(int(m.group(1) or 1), int(m.group(2) or 1))


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Convert (\d+)° to radians\. Give an exact answer "
                     r"in terms of π\.", p)
    if m:
        return pi_txt(Fraction(int(m.group(1)), 180))
    m = re.fullmatch(r"Convert (.+) radians to degrees\.", p)
    if m:
        fr = parse_pi(m.group(1))
        deg = fr * 180
        assert deg.denominator == 1
        return f"{deg.numerator}°"
    m = re.fullmatch(r"Find the angle between 0° and 360° that is "
                     r"coterminal with (-?\d+)°\.", p)
    if m:
        return f"{int(m.group(1)) % 360}°"
    m = re.fullmatch(r"Find the reference angle of (\d+)°\.", p)
    assert m, p
    t = int(m.group(1)) % 360
    ref = min(t % 180, 180 - (t % 180))
    return f"{ref}°"


class TestAngleMeasureGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AngleMeasureGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_coterminal_answers_in_range(self):
        gen = AngleMeasureGenerator("coterminal")
        for _ in range(200):
            result = gen.generate()
            v = int(result["final_answer"].rstrip("°"))
            self.assertTrue(0 <= v < 360)

    def test_reference_angles_acute(self):
        gen = AngleMeasureGenerator("reference")
        for _ in range(200):
            result = gen.generate()
            v = int(result["final_answer"].rstrip("°"))
            self.assertTrue(0 < v < 90)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(Fraction(f[1]) * Fraction(f[2]),
                                     Fraction(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)


if __name__ == "__main__":
    unittest.main()
