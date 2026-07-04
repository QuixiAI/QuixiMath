import unittest
import random
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.simple_probability_generator import SimpleProbabilityGenerator
from helpers import DELIM


class TestSimpleProbabilityGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = SimpleProbabilityGenerator()

    def test_probability_correctness(self):
        """A9 oracle: the answer is the exact reduced fraction, never a
        rounded decimal, and never a degenerate certainty."""
        from fractions import Fraction
        for _ in range(500):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            # Extract favorable/total
            words = res["problem"].split()
            favorable = int(words[4])
            total = int(words[9])
            expected = Fraction(favorable, total)
            answer = Fraction(res["final_answer"])
            self.assertEqual(answer, expected, res["problem"])
            # rendered in lowest terms
            num, den = (int(x) for x in res["final_answer"].split("/"))
            self.assertEqual(Fraction(num, den), expected)
            self.assertEqual((num, den),
                             (expected.numerator, expected.denominator))
            self.assertLess(answer, 1)
            self.assertGreater(answer, 0)


if __name__ == "__main__":
    unittest.main()
