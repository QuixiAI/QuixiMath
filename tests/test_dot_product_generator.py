import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dot_product_generator import DotProductGenerator
from helpers import DELIM


def parse_vec(txt):
    return [int(v) for v in txt.strip("⟨⟩").split(", ")]


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Given u = (⟨.+?⟩) and v = (⟨.+?⟩), compute the "
                     r"dot product u·v\.", p)
    if m:
        u, v = parse_vec(m.group(1)), parse_vec(m.group(2))
        return str(u[0] * v[0] + u[1] * v[1])
    m = re.fullmatch(r"Are u = (⟨.+?⟩) and v = (⟨.+?⟩) perpendicular\?",
                     p)
    if m:
        u, v = parse_vec(m.group(1)), parse_vec(m.group(2))
        return "Yes" if u[0] * v[0] + u[1] * v[1] == 0 else "No"
    m = re.fullmatch(r"Find the angle between u = (⟨.+?⟩) and "
                     r"v = (⟨.+?⟩)\.", p)
    assert m, p
    u, v = parse_vec(m.group(1)), parse_vec(m.group(2))
    d = u[0] * v[0] + u[1] * v[1]
    cos = d / (math.hypot(*u) * math.hypot(*v))
    theta = round(math.degrees(math.acos(max(-1.0, min(1.0, cos)))))
    return f"{theta}°"


class TestDotProductGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DotProductGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute dots and angles numerically."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_perp_yes_and_no_occur(self):
        gen = DotProductGenerator("perp")
        answers = set()
        for _ in range(100):
            answers.add(gen.generate()["final_answer"])
        self.assertEqual(answers, {"Yes", "No"})

    def test_step_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_all_angles_reachable(self):
        gen = DotProductGenerator("angle")
        angles = set()
        for _ in range(200):
            angles.add(gen.generate()["final_answer"])
        self.assertEqual(angles, {"0°", "45°", "90°", "135°", "180°"})

    def test_no_pipe_bars_inside_fields(self):
        """Magnitude uses ‖ ‖, never ASCII pipes (the delimiter)."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                op = s.split(DELIM)[0]
                self.assertTrue(op.replace("_", "").isalpha(), s)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DotProductGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
