import unittest
import sys
import os
import random
import math
import re

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pythag_hyp_generator import PythagHypGenerator
from helpers import DELIM


def oracle_answer(problem):
    match = re.fullmatch(
        r"In right triangle [A-Z]{3}, [A-Z]{2} and [A-Z]{2} are "
        r"perpendicular legs of lengths (\d+) and (\d+)\. Find "
        r"hypotenuse [A-Z]{2}\.",
        problem,
    )
    assert match, problem
    a, b = map(int, match.groups())
    root = math.isqrt(a * a + b * b)
    assert root * root == a * a + b * b, problem
    return str(root)

class TestPythagHypGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = PythagHypGenerator()
        # random.seed(51) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "pythag_hyp")
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
            self.assertIn("right triangle", result["problem"])
            self.assertIn("perpendicular legs", result["problem"])
            self.assertIn("Find hypotenuse", result["problem"])

            # Check if final answer is a valid integer string (since we use scaled triples)
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer string.")

    def test_oracle_and_arithmetic_steps(self):
        """A9 oracle: solve the labeled triangle from prompt lengths."""
        for _ in range(500):
            result = self.generator.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.generator.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == '__main__':
    unittest.main()
