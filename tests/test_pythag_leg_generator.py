import unittest
import random
import sys
import os
import math
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pythag_leg_generator import (
    MODIFIERS, PythagoreanLegGenerator, PythagoreanWordProblemGenerator,
)
from helpers import DELIM


def clean(problem):
    return re.sub(r"^An unrelated note mentions \d+ unrelated items\. ", "", problem)


def leg_oracle(problem):
    match = re.fullmatch(
        r"In right triangle [A-Z]{3}, hypotenuse [A-Z]{2} is (\d+) "
        r"units and leg [A-Z]{2} is (\d+) units\. Find leg [A-Z]{2}\.",
        problem,
    )
    assert match, problem
    hypotenuse, known_leg = map(int, match.groups())
    square = hypotenuse * hypotenuse - known_leg * known_leg
    root = math.isqrt(square)
    assert root * root == square, problem
    return f"{root} units"


def word_oracle(problem):
    ladder_height = re.match(
        r"A (\d+)-foot ladder is placed against a wall\. The base of "
        r"the ladder is (\d+) feet from the wall\.",
        problem,
    )
    if ladder_height:
        hypotenuse, leg = map(int, ladder_height.groups())
        return f"{math.isqrt(hypotenuse ** 2 - leg ** 2)} feet"
    ladder_base = re.match(
        r"A (\d+)-foot ladder reaches (\d+) feet up a wall\.", problem
    )
    if ladder_base:
        hypotenuse, leg = map(int, ladder_base.groups())
        return f"{math.isqrt(hypotenuse ** 2 - leg ** 2)} feet"
    rectangle = re.match(
        r"A rectangle has a length of (\d+) units and a width of "
        r"(\d+) units\.",
        problem,
    )
    if rectangle:
        a, b = map(int, rectangle.groups())
        return f"{math.isqrt(a * a + b * b)} units"
    distance = re.match(
        r"A person walks (\d+) meters east and then (\d+) meters north\.",
        problem,
    )
    assert distance, problem
    a, b = map(int, distance.groups())
    return f"{math.isqrt(a * a + b * b)} meters"


class TestPythagoreanLegGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = PythagoreanLegGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "pythagorean_find_leg")
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("right triangle", result["problem"].lower())
            self.assertIn("hypotenuse", result["problem"].lower())

            has_setup = any(s.startswith(f"PYTHAG_SETUP{DELIM}") for s in result["steps"])
            has_formula = any(s.startswith(f"PYTHAG_FORMULA{DELIM}") for s in result["steps"])
            has_root = any(s.startswith(f"PYTHAG_ROOT{DELIM}") for s in result["steps"])

            self.assertTrue(has_setup, "Missing PYTHAG_SETUP step")
            self.assertTrue(has_formula, "Missing PYTHAG_FORMULA step")
            self.assertTrue(has_root, "Missing PYTHAG_ROOT step")

    def test_answer_is_valid(self):
        """A9 oracle: recover both known sides from the prompt."""
        for _ in range(500):
            result = self.generator.generate()
            self.assertEqual(leg_oracle(result["problem"]),
                             result["final_answer"], result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "PYTHAG_SQUARE":
                    self.assertEqual(int(fields[1]) ** 2, int(fields[2]),
                                     raw_step)
                elif fields[0] == "PYTHAG_ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)


class TestPythagoreanWordProblemGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.generator = PythagoreanWordProblemGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("pythagorean_word_problem_"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_context = any(s.startswith(f"PYTHAG_CONTEXT{DELIM}") for s in result["steps"])
            has_model = any(s.startswith(f"PYTHAG_MODEL{DELIM}") for s in result["steps"])
            self.assertTrue(has_context, "Missing PYTHAG_CONTEXT step")
            self.assertTrue(has_model, "Missing PYTHAG_MODEL step")

    def test_oracle_from_word_problem_text(self):
        """A9 oracle: independently solve every real-world context."""
        for _ in range(600):
            result = self.generator.generate()
            self.assertTrue(
                result["final_answer"].endswith(word_oracle(clean(result["problem"]))),
                result["problem"])

    def test_pipe_safety_both_generators(self):
        for generator in (PythagoreanLegGenerator(), self.generator):
            for _ in range(200):
                result = generator.generate()
                for raw_step in result["steps"]:
                    self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                         raw_step)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(52)
        for modifier in MODIFIERS:
            result = PythagoreanWordProblemGenerator(modifier).generate()
            codes = [raw.split(DELIM)[0] for raw in result["steps"]]
            self.assertEqual(result["operation"], f"pythagorean_word_problem_{modifier}")
            if modifier == "distractor":
                self.assertEqual(codes[0], "SELECT_RELEVANT")
            elif modifier == "estimate_first":
                self.assertEqual(codes[0], "ESTIMATE")
                self.assertEqual(codes[-2], "ESTIMATE_CHECK")
            elif modifier == "with_model":
                self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            PythagoreanWordProblemGenerator("bogus")


if __name__ == '__main__':
    unittest.main()
