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

from generators.proportional_relationship_generator import ProportionalRelationshipGenerator
from helpers import DELIM


def oracle_answer(problem):
    """Solve either proportion orientation from the problem text alone."""
    match = re.fullmatch(
        r"If (\d+) is to (\d+), what is (\d+) proportional to\?",
        problem,
    )
    if match:
        a, b, c = map(int, match.groups())
        numerator = b * c
        assert numerator % a == 0, problem
        return str(numerator // a)
    match = re.fullmatch(
        r"If (\d+) is to (\d+), what is proportional to (\d+)\?",
        problem,
    )
    assert match, problem
    a, b, c = map(int, match.groups())
    numerator = a * c
    assert numerator % b == 0, problem
    return str(numerator // b)

class TestProportionalRelationshipGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = ProportionalRelationshipGenerator()
        # random.seed(53) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "proportional_relationship")

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
            self.assertTrue(result["problem"].startswith("If "), f"Problem '{result['problem']}' doesn't start with 'If '")
            self.assertIn(" is to ", result["problem"])
            self.assertIn(" proportional to", result["problem"])

            # Check if final answer is a valid integer string (since we ensure integer results)
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer string.")

            # Check for specific proportional steps
            has_setup_step = any(s.startswith(f"PROP_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing PROP_SETUP step")

    def test_operation_name_correct(self):
        """Test that the correct operation name is returned."""
        # This test verifies the generator returns the correct operation name.
        result = self.generator.generate()
        self.assertEqual(result["operation"], "proportional_relationship", "Operation name should be 'proportional_relationship'")

    def test_oracle_and_arithmetic_steps(self):
        """A9 oracle plus independent checks of cross multiplication."""
        for _ in range(1000):
            result = self.generator.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0,
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.generator.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == '__main__':
    unittest.main()
