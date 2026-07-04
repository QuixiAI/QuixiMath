import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.number_comparison_generator import NumberComparisonGenerator
from helpers import DELIM


class TestNumberComparisonGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = NumberComparisonGenerator()

    def test_compare_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        parts = res["final_answer"].split()
        a, rel, b = float(parts[0]), parts[1], float(parts[2])
        if rel == ">":
            self.assertGreater(a, b)
        elif rel == "<":
            self.assertLess(a, b)
        else:
            self.assertEqual(a, b)


    def test_oracle_and_digit_walk(self):
        """A9 oracle: recompute the relation exactly; the scratchpad must
        contain the digit-by-digit CMP_DIGIT walk."""
        from decimal import Decimal
        gen = NumberComparisonGenerator()
        for _ in range(500):
            res = gen.generate()
            x, y = res["problem"].replace("Compare: ", "").split(" ? ")
            relation = ">" if Decimal(x) > Decimal(y) else "<"
            self.assertEqual(res["final_answer"], f"{x} {relation} {y}",
                             res["problem"])
            self.assertTrue(any(s.startswith("CMP_DIGIT")
                                for s in res["steps"]), res["problem"])


if __name__ == "__main__":
    unittest.main()
