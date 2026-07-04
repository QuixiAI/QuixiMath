import unittest
import random
import sys
import os
from fractions import Fraction
from statistics import median, multimode

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.simple_stats_generator import SimpleStatsGenerator
from helpers import DELIM


class TestSimpleStatsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = SimpleStatsGenerator()

    def test_stats_correctness(self):
        for _ in range(500):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            data_str = res["problem"].split("of")[1].strip().strip("[]")
            data = [int(x.strip()) for x in data_str.split(",") if x.strip()]
            op = res["operation"]
            if op == "mean":
                # Datasets are constructed so the mean is an exact integer
                expected = Fraction(sum(data), len(data))
                self.assertEqual(expected.denominator, 1, res["problem"])
                self.assertEqual(res["final_answer"], str(expected))
            elif op == "median":
                expected = Fraction(median(data))
                self.assertEqual(Fraction(res["final_answer"]), expected)
                # Exact rendering: integer or n.5, never a rounded float
                self.assertRegex(res["final_answer"], r"^\d+(\.5)?$")
            else:
                modes = multimode(data)
                result_modes = [int(x.strip()) for x in res["final_answer"].split(",")]
                self.assertCountEqual(result_modes, modes)


if __name__ == "__main__":
    unittest.main()
