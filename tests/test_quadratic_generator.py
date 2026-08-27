import unittest
import sys
import os
import random
import re

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quadratic_generator import QuadraticGenerator
from helpers import DELIM

class TestQuadraticGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = QuadraticGenerator()
        # random.seed(47) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "quadratic_eq")
        self.assertIn("problem", result)
        self.assertIsInstance(result["problem"], str)
        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0, "Steps list should not be empty")
        self.assertIn("final_answer", result)
        self.assertIsInstance(result["final_answer"], str)

        # Check the final step format
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"), f"Final step should start with Z{DELIM}")
        # Check if final answer in step matches the final_answer field
        self.assertEqual(final_step.split(DELIM)[1], result["final_answer"])

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(10): # Generate a few examples
            result = self.generator.generate()
            # Re-run basic format checks
            self.assertIsInstance(result, dict)
            self.assertIn("problem_id", result)
            self.assertIn("operation", result)
            self.assertIn("problem", result)
            self.assertIn("steps", result)
            self.assertIn("final_answer", result)
            self.assertGreater(len(result["steps"]), 0)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM)[1], result["final_answer"])

            # Check if problem string looks reasonable
            self.assertIn("Solve", result["problem"])
            self.assertIn("=", result["problem"])
            self.assertRegex(result["problem"], r"[xytnz]\^2")

            # A0 convention: 'x = r1 or x = r2', roots ascending
            m = re.fullmatch(r"([xytnz]) = (-?\d+) or \1 = (-?\d+)",
                             result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            var = m.group(1)
            r_low, r_high = int(m.group(2)), int(m.group(3))
            self.assertLess(r_low, r_high)

            # Oracle: both roots satisfy the parsed equation exactly
            coeffs = re.fullmatch(
                rf"(-?\d*){var}\^2(?:([+-]\d*){var})?([+-]\d+)? = 0",
                result["problem"].replace("Solve ", ""))
            self.assertIsNotNone(coeffs, result["problem"])
            a_txt, b_txt, c_txt = coeffs.groups()
            a = int(a_txt) if a_txt not in ("", "-") else (-1 if a_txt == "-" else 1)
            b = (0 if b_txt is None
                 else 1 if b_txt == "+" else -1 if b_txt == "-" else int(b_txt))
            c = 0 if c_txt is None else int(c_txt)
            for root in (r_low, r_high):
                self.assertEqual(a * root * root + b * root + c, 0,
                                 result["problem"])

    def test_formula_arithmetic_and_pipe_safety(self):
        for _ in range(500):
            result = self.generator.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                self.assertLessEqual(len(fields) - 1, 4, raw_step)
                if fields[0] == "DISC":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)
                elif fields[0] == "Q1":
                    self.assertEqual(
                        int(fields[1]) + int(fields[2]),
                        int(fields[3]) * int(fields[4]), raw_step,
                    )
                elif fields[0] == "Q2":
                    self.assertEqual(
                        int(fields[1]) - int(fields[2]),
                        int(fields[3]) * int(fields[4]), raw_step,
                    )


if __name__ == '__main__':
    unittest.main()
