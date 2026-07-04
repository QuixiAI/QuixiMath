import unittest
import sys
import os
import random

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
            self.assertIn("x^2", result["problem"]) # Check for x squared term

            # A0 convention: 'x = r1 or x = r2', roots ascending
            import re
            m = re.fullmatch(r"x = (-?\d+) or x = (-?\d+)",
                             result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            r_low, r_high = int(m.group(1)), int(m.group(2))
            self.assertLess(r_low, r_high)

            # Oracle: both roots satisfy the parsed equation exactly
            pm = re.fullmatch(
                r"Solve (-?\d*)x\^2([+-]\d*)?x?([+-]\d+)? = 0",
                result["problem"].replace(" ", " "))
            coeffs = re.fullmatch(
                r"(-?\d*)x\^2(?:([+-]\d*)x)?([+-]\d+)? = 0",
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


if __name__ == '__main__':
    unittest.main()
