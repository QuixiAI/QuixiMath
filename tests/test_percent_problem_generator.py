import unittest
import sys
import os
import random
import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.percent_problem_generator import PercentProblemGenerator
from helpers import DELIM


def decimal_text(value):
    """Exact plain-decimal rendering for a terminating Fraction."""
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    rendered = format(decimal, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def oracle_answer(problem):
    """Solve a percent question using only the quantities in its text."""
    match = re.fullmatch(r"What is ([0-9.]+)% of ([0-9]+)\?", problem)
    if match:
        percent = Fraction(match.group(1))
        whole = int(match.group(2))
        return decimal_text(percent * whole / 100)
    match = re.fullmatch(
        r"([0-9]+) is what percent of ([0-9]+)\?", problem
    )
    if match:
        part, whole = map(int, match.groups())
        return f"{decimal_text(Fraction(100 * part, whole))}%"
    match = re.fullmatch(
        r"([0-9]+) is ([0-9.]+)% of what number\?", problem
    )
    assert match, problem
    part = int(match.group(1))
    percent = Fraction(match.group(2))
    return decimal_text(Fraction(100 * part, 1) / percent)

class TestPercentProblemGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = PercentProblemGenerator()
        # random.seed(55) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("percent_"), "Operation name should start with 'percent_'")
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

        # Check for core percent steps based on operation type
        op = result["operation"]
        steps_str = "|".join(result["steps"]) # For easier searching

        if op == "percent_find_part":
            self.assertIn(f"PERCENT_TO_DEC{DELIM}", steps_str, "Missing PERCENT_TO_DEC")
            self.assertIn(f"SETUP_PERCENT_EQ{DELIM}", steps_str, "Missing SETUP_PERCENT_EQ")
            self.assertIn(f"PERCENT_CALC_PART{DELIM}", steps_str, "Missing PERCENT_CALC_PART")
            # Ensure no division steps are present for find_part
            self.assertNotIn(f"DEC_SHIFT{DELIM}", steps_str, "DEC_SHIFT should not be in find_part")
            self.assertNotIn(f"DIV_SETUP{DELIM}", steps_str, "DIV_SETUP should not be in find_part")
        elif op == "percent_find_percent":
            self.assertIn(f"SETUP_PERCENT_EQ{DELIM}", steps_str, "Missing SETUP_PERCENT_EQ")
            # Check for division steps (DEC_SHIFT only when the divisor
            # has decimals — find_percent divides by an integer whole)
            self.assertIn(f"DIV_SETUP{DELIM}", steps_str, "Missing DIV_SETUP")
            self.assertTrue(any(s.startswith(f"D{DELIM}") for s in result["steps"]), "Missing D step")
            self.assertTrue(any(s.startswith(f"M{DELIM}") for s in result["steps"]), "Missing M step")
            self.assertTrue(any(s.startswith(f"S{DELIM}") for s in result["steps"]), "Missing S step")
            self.assertIn(f"PLACE_DP_Q{DELIM}", steps_str, "Missing PLACE_DP_Q")
            # Check for final conversion step
            self.assertIn(f"DEC_TO_PERCENT{DELIM}", steps_str, "Missing DEC_TO_PERCENT")
            # Ensure calculation steps specific to other types are not present
            self.assertNotIn(f"PERCENT_CALC_PART{DELIM}", steps_str)
            self.assertNotIn(f"PERCENT_CALC_WHOLE{DELIM}", steps_str)
            self.assertNotIn(f"REARRANGE_EQ{DELIM}", steps_str)
        elif op == "percent_find_whole":
            self.assertIn(f"PERCENT_TO_DEC{DELIM}", steps_str, "Missing PERCENT_TO_DEC")
            self.assertIn(f"SETUP_PERCENT_EQ{DELIM}", steps_str, "Missing SETUP_PERCENT_EQ")
            self.assertIn(f"REARRANGE_EQ{DELIM}", steps_str, "Missing REARRANGE_EQ")
            # Check for division steps
            self.assertIn(f"DIV_SETUP{DELIM}", steps_str, "Missing DIV_SETUP")
            self.assertTrue(any(s.startswith(f"D{DELIM}") for s in result["steps"]), "Missing D step")
            self.assertTrue(any(s.startswith(f"M{DELIM}") for s in result["steps"]), "Missing M step")
            self.assertTrue(any(s.startswith(f"S{DELIM}") for s in result["steps"]), "Missing S step")
            self.assertIn(f"PLACE_DP_Q{DELIM}", steps_str, "Missing PLACE_DP_Q")
            # Ensure calculation steps specific to other types are not present
            self.assertNotIn(f"PERCENT_CALC_PART{DELIM}", steps_str)
            self.assertNotIn(f"PERCENT_CALC_PERCENT{DELIM}", steps_str)
            self.assertNotIn(f"DEC_TO_PERCENT{DELIM}", steps_str)
        else:
            self.fail(f"Unknown percent operation type: {op}")

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(10): # Generate a few examples
            result = self.generator.generate()
            # Re-run basic format checks (includes step checks)
            self.test_generate_output_format()

            # Check if problem string looks reasonable based on type
            op = result["operation"]
            problem = result["problem"]
            if op == "percent_find_part":
                self.assertIn("What is", problem)
                self.assertIn("% of", problem)
            elif op == "percent_find_percent":
                self.assertIn("is what percent of", problem)
            elif op == "percent_find_whole":
                 self.assertIn("is", problem)
                 self.assertIn("% of what number", problem)

            # Check final answer format
            final_answer = result["final_answer"]
            if op == "percent_find_percent":
                self.assertTrue(final_answer.endswith('%'), "Find Percent answer should end with %")
                try:
                    float(final_answer.rstrip('%'))
                except ValueError:
                    self.fail(f"Find Percent answer value '{final_answer}' is not valid.")
            else: # Find Part or Whole - should be a number
                 try:
                     Decimal(final_answer)
                 except InvalidOperation:
                     self.fail(f"Find Part/Whole answer '{final_answer}' is not a valid Decimal.")

    def test_oracle_recomputes_answer_from_problem_text(self):
        """A9 oracle: independently solve all three percent forms."""
        for _ in range(1000):
            result = self.generator.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_long_division_arithmetic(self):
        for _ in range(500):
            result = self.generator.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe_and_plain_numbers(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn("E", result["final_answer"].upper())
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == '__main__':
    unittest.main()
