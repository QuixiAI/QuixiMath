import unittest
import random
import sys
import os
from fractions import Fraction

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.fraction_comparison_generator import FractionComparisonGenerator
from helpers import DELIM


class TestFractionComparisonGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = FractionComparisonGenerator()

    def test_basic_format_and_relation(self):
        res = self.gen.generate()
        for key in ["problem_id", "operation", "problem", "steps", "final_answer"]:
            self.assertIn(key, res)
        self.assertEqual(res["operation"], "fraction_compare")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # final answer includes relation symbol
        self.assertRegex(res["final_answer"], r"[<>=]")

        # Verify relation correctness
        _, relation, _ = res["final_answer"].split()
        lhs_str = res["final_answer"].split()[0]
        rhs_str = res["final_answer"].split()[2]
        lhs = Fraction(lhs_str)
        rhs = Fraction(rhs_str)
        if relation == ">":
            self.assertGreater(lhs, rhs)
        elif relation == "<":
            self.assertLess(lhs, rhs)
        else:
            self.assertEqual(lhs, rhs)

    def test_oracle_recomputes_relation_from_problem_text(self):
        """A9 oracle: parse both fractions from the problem, compare
        exactly, and check the answer echoes the operands as written."""
        relations = set()
        for _ in range(500):
            res = self.gen.generate()
            lhs_str, rhs_str = res["problem"].replace("Compare: ", "").split(" ? ")
            lhs, rhs = Fraction(lhs_str), Fraction(rhs_str)
            relation = ">" if lhs > rhs else "<" if lhs < rhs else "="
            relations.add(relation)
            self.assertEqual(res["final_answer"],
                             f"{lhs_str} {relation} {rhs_str}", res["problem"])
        # all three relations should appear, including equivalent pairs
        self.assertEqual(relations, {">", "<", "="})


if __name__ == "__main__":
    unittest.main()
