import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.kinematics_generator import KinematicsGenerator
from helpers import DELIM


SPEED_UNITS = {
    ("meters", "seconds"): "m/s",
    ("kilometers", "hours"): "km/hour",
    ("miles", "hours"): "miles/hour",
    ("feet", "seconds"): "ft/s",
}


def oracle_answer(example):
    """A9 oracle: recompute the kinematics quantity from the prompt."""
    problem = example["problem"]
    m = re.search(
        r"travels at (\d+) (meters|kilometers|miles|feet) per "
        r"(second|hour) for (\d+) (seconds|hours)",
        problem,
    )
    if m:
        speed = int(m.group(1))
        dist_unit = m.group(2)
        time = int(m.group(4))
        return f"{speed * time} {dist_unit}"

    m = re.search(
        r"travels (\d+) (meters|kilometers|miles|feet) in (\d+) "
        r"(seconds|hours)\. Find the speed",
        problem,
    )
    if m:
        distance = int(m.group(1))
        dist_unit = m.group(2)
        time = int(m.group(3))
        time_unit = m.group(4)
        return f"{distance // time} {SPEED_UNITS[(dist_unit, time_unit)]}"

    m = re.search(
        r"travels (\d+) (meters|kilometers|miles|feet) at (\d+) "
        r"(?:meters|kilometers|miles|feet) per (second|hour)",
        problem,
    )
    if m:
        distance = int(m.group(1))
        speed = int(m.group(3))
        time_root = m.group(4)
        time_unit = f"{time_root}s"
        return f"{distance // speed} {time_unit}"

    m = re.search(
        r"velocity changes from (\d+) meters per second to (\d+) meters "
        r"per second in (\d+) seconds",
        problem,
    )
    start, final, time = (int(v) for v in m.groups())
    return f"{(final - start) // time} m/s^2"


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "M":
            if Fraction(parts[1]) * Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif code == "D":
            if Fraction(parts[1]) / Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif code == "S":
            if Fraction(parts[1]) - Fraction(parts[2]) != Fraction(parts[3]):
                return False
        elif code == "UNIT_ATTACH":
            if parts[3] != f"{parts[1]} {parts[2]}":
                return False
    return True


class TestKinematicsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = KinematicsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_formula_present(self):
        for variant in KinematicsGenerator.VARIANTS:
            result = KinematicsGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"KIN_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_answer_has_units(self):
        for _ in range(200):
            self.assertRegex(self.gen.generate()["final_answer"],
                             r"(meters|kilometers|miles|feet|seconds|hours|m/s|km/hour|miles/hour|ft/s)")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            KinematicsGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
