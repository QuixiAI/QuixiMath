import unittest
import sys
import os
import random
from math import isqrt

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.divisibility_classification_generator import DivisibilityClassificationGenerator
from helpers import DELIM


class TestDivisibilityClassificationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Use seed for deterministic tests
        self.gen = DivisibilityClassificationGenerator()

    def test_classification_correctness(self):
        # Run multiple tests to verify correctness across different numbers
        import re
        for _ in range(500):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            n = int(res["problem"].split()[1])
            answer = res["final_answer"]
            # Simple primality check
            prime = True
            for d in range(2, isqrt(n) + 1):
                if n % d == 0:
                    prime = False
                    break
            if prime:
                self.assertEqual(answer, "prime", f"Number {n} should be prime")
            else:
                # composite answers carry a verifiable witness pair
                match = re.fullmatch(r"composite \((\d+) × (\d+)\)", answer)
                self.assertIsNotNone(match, f"Number {n}: {answer}")
                self.assertEqual(int(match.group(1)) * int(match.group(2)), n)

    def test_trial_division_stops_at_first_factor(self):
        # Human flow: only the last DIV_CHECK may have remainder 0
        for _ in range(300):
            res = self.gen.generate()
            div_checks = [s for s in res["steps"]
                          if s.startswith(f"DIV_CHECK{DELIM}")]
            for check in div_checks[:-1]:
                self.assertFalse(
                    check.endswith(f"{DELIM}0"),
                    f"kept checking after finding a factor: {res['steps']}")


if __name__ == "__main__":
    unittest.main()
