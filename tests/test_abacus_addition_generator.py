import unittest
import sys
import os
import random

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.abacus_addition_generator import AbacusAdditionGenerator
from helpers import DELIM

class TestAbacusAdditionGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = AbacusAdditionGenerator()
        # random.seed(52) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "abacus_addition")
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
            self.assertIn("+", result["problem"])

            # Check if final answer is a valid integer string
            try:
                int(result["final_answer"])
            except ValueError:
                self.fail(f"Final answer '{result['final_answer']}' is not a valid integer string.")

            # Check for specific abacus steps
            has_set_step = any(s.startswith(f"AB_SET{DELIM}") for s in result["steps"])
            has_add_step = any(s.startswith(f"AB_ADD{DELIM}") for s in result["steps"])
            self.assertTrue(has_set_step, "Missing AB_SET step")
            self.assertTrue(has_add_step, "Missing AB_ADD step")

    def test_oracle_running_total_trace(self):
        """A9 oracle: the AB_ADD chain must start at the first addend,
        add place-value components of the second addend left to right,
        and end at the true sum."""
        for _ in range(300):
            result = self.generator.generate()
            num1_text, num2_text = result["problem"].split(" + ")
            num1, num2 = int(num1_text), int(num2_text)
            self.assertEqual(result["final_answer"], str(num1 + num2))

            total = num1
            components = []
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "AB_SET":
                    self.assertEqual(int(fields[1]), num1)
                elif fields[0] == "AB_ADD":
                    component = int(fields[1])
                    self.assertEqual(int(fields[2]), total, raw)
                    self.assertEqual(int(fields[3]), total + component, raw)
                    total += component
                    components.append(component)
            self.assertEqual(total, num1 + num2)
            self.assertEqual(sum(components), num2)
            # left to right: strictly decreasing place values
            self.assertEqual(components,
                             sorted(components, reverse=True))


if __name__ == '__main__':
    unittest.main()
