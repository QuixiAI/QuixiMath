import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometric_probability_generator import (
    GeometricProbabilityGenerator, exact,
)
from helpers import DELIM


def oracle_answer(example):
    """A9 oracle: recompute the probability from the problem text alone."""
    problem = example["problem"]
    m = re.search(
        r"number line from 0 to (\d+).*lands between (\d+) and (\d+)",
        problem,
    )
    if m:
        total, left, right = (int(v) for v in m.groups())
        return exact(Fraction(right - left, total))

    m = re.search(
        r"in a (\d+) by (\d+) rectangle\. A shaded rectangle inside it is "
        r"(\d+) by (\d+)",
        problem,
    )
    if m:
        width, height, shade_width, shade_height = (int(v) for v in m.groups())
        return exact(Fraction(shade_width * shade_height, width * height))

    angle = int(re.search(r"central angle (\d+) degrees", problem).group(1))
    return exact(Fraction(angle, 360))


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        code = parts[0]
        if code == "MEASURE_FAVORABLE" and "-" in parts[2]:
            right, left, length = (int(v) for v in re.search(
                r"(\d+) - (\d+) = (\d+)", parts[2]
            ).groups())
            if right - left != length:
                return False
        elif code in {"MEASURE_TOTAL", "MEASURE_FAVORABLE"} and "*" in parts[2]:
            a, b, product = (int(v) for v in re.search(
                r"(\d+) \* (\d+) = (\d+)", parts[2]
            ).groups())
            if a * b != product:
                return False
        elif code == "FRAC_BUILD":
            if exact(Fraction(parts[1])) != parts[2]:
                return False
    return True


class TestGeometricProbabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GeometricProbabilityGenerator()

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

    def test_probabilities_valid(self):
        for _ in range(300):
            result = self.gen.generate()
            val = float(Fraction(result["final_answer"]))
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 1)

    def test_formula_and_measures_present(self):
        for variant in GeometricProbabilityGenerator.VARIANTS:
            result = GeometricProbabilityGenerator(variant).generate()
            codes = {s.split(DELIM)[0] for s in result["steps"]}
            self.assertIn("GEO_PROB_FORMULA", codes)
            self.assertIn("MEASURE_TOTAL", codes)
            self.assertIn("MEASURE_FAVORABLE", codes)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 3)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GeometricProbabilityGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
