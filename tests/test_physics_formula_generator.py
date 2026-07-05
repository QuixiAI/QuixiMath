import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.physics_formula_generator import PhysicsFormulaGenerator
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the physics quantity from the prompt."""
    problem = example["problem"]
    m = re.search(
        r"force of (\d+) newtons moves an object (\d+) meters",
        problem,
    )
    if m:
        force, distance = (int(v) for v in m.groups())
        return f"{force * distance} joules"

    m = re.search(
        r"(\d+) joules of work move an object (\d+) meters",
        problem,
    )
    if m:
        work, distance = (int(v) for v in m.groups())
        return f"{work // distance} newtons"

    m = re.search(
        r"(?:machine|motor) does (\d+) joules of work in (\d+) seconds",
        problem,
    )
    if m:
        work, seconds = (int(v) for v in m.groups())
        return f"{work // seconds} watts"

    m = re.search(
        r"(?:machine|pump) does (\d+) joules of work in (\d+) minutes?",
        problem,
    )
    if m:
        work, minutes = (int(v) for v in m.groups())
        return f"{work // (minutes * 60)} watts"

    m = re.search(r"(?:device|appliance|tool) runs at (\d+) watts for (\d+) minutes?", problem)
    power, minutes = (int(v) for v in m.groups())
    return f"{power * minutes * 60} joules"


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
        elif code == "UNIT_CONVERT":
            minutes = int(re.search(r"(\d+) minutes?", parts[1]).group(1))
            seconds = int(re.search(r"(\d+) seconds", parts[2]).group(1))
            if minutes * 60 != seconds:
                return False
        elif code == "UNIT_ATTACH":
            if parts[3] != f"{parts[1]} {parts[2]}":
                return False
    return True


class TestPhysicsFormulaGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PhysicsFormulaGenerator()

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
        for variant in PhysicsFormulaGenerator.VARIANTS:
            result = PhysicsFormulaGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"PHYS_FORMULA{DELIM}")
                                for s in result["steps"]))

    def test_conversion_variants_have_conversion_step(self):
        for variant in ("power_minutes", "energy"):
            result = PhysicsFormulaGenerator(variant).generate()
            self.assertTrue(any(s.startswith(f"UNIT_CONVERT{DELIM}")
                                for s in result["steps"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            PhysicsFormulaGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
