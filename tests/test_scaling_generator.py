import unittest
import random
import re
import sys
import os
from fractions import Fraction

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.scaling_generator import ScalingGenerator, SimilarFiguresScaleGenerator
from helpers import DELIM


NUMBER = r"\d+(?:\.\d+|/\d+)?"


def unit_plural(unit, value):
    if value == 1:
        return unit
    return unit + "es" if unit == "inch" else unit + "s"


def number_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    if value.denominator in (2, 4):
        whole, remainder = divmod(value.numerator, value.denominator)
        tail = {Fraction(1, 4): "25", Fraction(1, 2): "5",
                Fraction(3, 4): "75"}[Fraction(remainder, value.denominator)]
        return f"{whole}.{tail}"
    return str(value)


def scaling_oracle(problem):
    scale_match = re.search(
        r"scale of 1 (inch|centimeter) = (\d+) "
        r"(miles|kilometers|feet|meters)", problem)
    assert scale_match, problem
    scale_unit, factor_text, actual_unit = scale_match.groups()
    factor = int(factor_text)
    if "what is the actual" in problem:
        unit_pattern = "inch(?:es)?" if scale_unit == "inch" else "centimeters?"
        values = re.findall(rf"({NUMBER}) {unit_pattern}", problem)
        scaled = Fraction(values[-1])
        return f"{number_text(scaled * factor)} {actual_unit}"
    actual_values = re.findall(rf"({NUMBER}) {actual_unit}", problem)
    actual = Fraction(actual_values[-1])
    scaled = actual / factor
    assert scaled.denominator == 1
    return f"{scaled} {unit_plural(scale_unit, scaled)}"


class TestScalingGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = ScalingGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertIn(result["operation"], ["scale_find_actual", "scale_find_scaled"])
        self.assertIn("problem", result)
        self.assertIsInstance(result["problem"], str)
        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0)
        self.assertIn("final_answer", result)
        self.assertIsInstance(result["final_answer"], str)

        # Check final step
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(20):
            result = self.generator.generate()

            self.assertIsInstance(result, dict)
            self.assertIn("operation", result)

            # Problem should mention scale
            self.assertIn("scale", result["problem"].lower())

            # Check for scale steps
            has_setup_step = any(s.startswith(f"SCALE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing SCALE_SETUP step")

    def test_find_actual_problems(self):
        """Test that find_actual problems multiply correctly."""
        for _ in range(10):
            result = self.generator.generate()
            if result["operation"] == "scale_find_actual":
                # Should have SCALE_MULT step
                has_mult_step = any(s.startswith(f"SCALE_MULT{DELIM}") for s in result["steps"])
                self.assertTrue(has_mult_step, "Missing SCALE_MULT step for find_actual problem")

    def test_find_scaled_problems(self):
        """Test that find_scaled problems divide correctly."""
        for _ in range(10):
            result = self.generator.generate()
            if result["operation"] == "scale_find_scaled":
                # Should have SCALE_DIV step
                has_div_step = any(s.startswith(f"SCALE_DIV{DELIM}") for s in result["steps"])
                self.assertTrue(has_div_step, "Missing SCALE_DIV step for find_scaled problem")

    def test_oracle_from_problem_text(self):
        for _ in range(500):
            result = self.generator.generate()
            self.assertEqual(scaling_oracle(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_exact_step_arithmetic_and_pipe_safety(self):
        for _ in range(300):
            result = self.generator.generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                self.assertLessEqual(len(fields) - 1, 4, raw_step)
                if fields[0] == "SCALE_MULT":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "SCALE_DIV":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)


class TestSimilarFiguresScaleGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = SimilarFiguresScaleGenerator()

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith(
            ("similar_scale_factor_", "similar_missing_side_")), result["operation"])
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)

    def test_generate_consistency(self):
        """Generate multiple examples and check consistency."""
        for _ in range(10):
            result = self.generator.generate()

            # Problem should mention similar figures
            self.assertIn("similar", result["problem"].lower())

            # Check for similar figures steps
            has_setup_step = any(s.startswith(f"SIMILAR_SETUP{DELIM}") for s in result["steps"])
            has_scale_step = any(s.startswith(f"SIMILAR_SCALE{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup_step, "Missing SIMILAR_SETUP step")
            self.assertTrue(has_scale_step, "Missing SIMILAR_SCALE step")

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(53)
        for modifier in SimilarFiguresScaleGenerator.MODIFIERS:
            result = SimilarFiguresScaleGenerator(modifier).generate()
            codes = [raw.split(DELIM)[0] for raw in result["steps"]]
            self.assertTrue(result["operation"].endswith(f"_{modifier}"))
            self.assertTrue(result["operation"].startswith(
                ("similar_scale_factor_", "similar_missing_side_")))
            if modifier == "distractor":
                self.assertEqual(codes[0], "SELECT_RELEVANT")
            elif modifier == "estimate_first":
                self.assertEqual(codes[0], "ESTIMATE")
                self.assertEqual(codes[-2], "ESTIMATE_CHECK")
            elif modifier == "with_model":
                self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SimilarFiguresScaleGenerator(modifier="bogus")


if __name__ == '__main__':
    unittest.main()
