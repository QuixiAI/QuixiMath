import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.euler_characteristic_generator import (
    EulerCharacteristicGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"A (.+) has (\d+) vertices, (\d+) edges, and "
                     r"(\d+) faces\. Compute V - E \+ F\.", p)
    if m:
        V, E, F = int(m.group(2)), int(m.group(3)), int(m.group(4))
        return str(V - E + F)
    m = re.fullmatch(r"A convex polyhedron has (\d+) vertices and (\d+) "
                     r"faces\. How many edges does it have\?", p)
    if m:
        return f"E = {int(m.group(1)) + int(m.group(2)) - 2}"
    m = re.fullmatch(r"A convex polyhedron has (\d+) edges and (\d+) "
                     r"faces\. How many vertices does it have\?", p)
    if m:
        return f"V = {2 + int(m.group(1)) - int(m.group(2))}"
    m = re.fullmatch(r"A convex polyhedron has (\d+) vertices and (\d+) "
                     r"edges\. How many faces does it have\?", p)
    if m:
        return f"F = {2 + int(m.group(2)) - int(m.group(1))}"
    m = re.fullmatch(r"A doughnut-shaped \(torus\) surface is divided "
                     r"into a grid with (\d+) vertices, (\d+) edges, and "
                     r"(\d+) faces\. Compute V - E \+ F\.", p)
    assert m, p
    V, E, F = (int(v) for v in m.groups())
    return str(V - E + F)


class TestEulerCharacteristicGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EulerCharacteristicGenerator()

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

    def test_solid_data_is_genuinely_eulerian(self):
        """Every catalogued solid satisfies V - E + F = 2."""
        for name, (V, E, F) in EulerCharacteristicGenerator.SOLIDS.items():
            self.assertEqual(V - E + F, 2, name)

    def test_sphere_family_gives_2_and_torus_0(self):
        outcomes = set()
        for _ in range(200):
            result = self.gen.generate()
            if "torus" in result["problem"]:
                self.assertEqual(result["final_answer"], "0")
                outcomes.add("torus")
            elif "Compute" in result["problem"]:
                self.assertEqual(result["final_answer"], "2")
                outcomes.add("sphere")
        self.assertEqual(outcomes, {"torus", "sphere"})

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)


if __name__ == "__main__":
    unittest.main()
