import unittest
import random
import re
import sys
import os
from math import prod

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.prime_factorization_generator import PrimeFactorizationGenerator
from helpers import DELIM


class TestPrimeFactorizationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Ensure deterministic tests
        self.gen = PrimeFactorizationGenerator()

    @staticmethod
    def number_from_problem(problem):
        values = {int(value) for value in re.findall(r"\d+", problem)}
        if len(values) != 1:
            raise AssertionError(problem)
        return values.pop()

    @staticmethod
    def is_prime_oracle(value):
        return (value >= 2 and all(value % divisor
                                   for divisor in range(
                                       2, int(value ** 0.5) + 1)))

    def test_factorization_correctness(self):
        """A9 oracle: reconstruct n from the text and factor independently."""
        for _ in range(500):
            res = self.gen.generate()
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            n = self.number_from_problem(res["problem"])
            factors = [int(p) for p in res["final_answer"].split(" × ")]
            self.assertEqual(prod(factors), n, res["problem"])
            self.assertTrue(all(self.is_prime_oracle(p) for p in factors),
                            res["final_answer"])

    def test_trial_division_trace(self):
        for _ in range(300):
            result = self.gen.generate()
            current = self.number_from_problem(result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "CHECK":
                    match = re.fullmatch(r"(\d+) mod (\d+)", fields[1])
                    self.assertIsNotNone(match, raw_step)
                    dividend, divisor = map(int, match.groups())
                    self.assertEqual(dividend, current, raw_step)
                    self.assertTrue(self.is_prime_oracle(divisor), raw_step)
                    self.assertEqual(dividend % divisor, int(fields[2]),
                                     raw_step)
                    self.assertNotEqual(int(fields[2]), 0, raw_step)
                elif fields[0] == "PF_STEP":
                    dividend, divisor, quotient = map(int, fields[1:])
                    self.assertEqual(dividend, current, raw_step)
                    self.assertEqual(dividend // divisor, quotient, raw_step)
                    self.assertEqual(dividend % divisor, 0, raw_step)
                    current = quotient
                elif fields[0] == "PF_PRIME":
                    self.assertEqual(int(fields[1]), current, raw_step)
                    self.assertTrue(self.is_prime_oracle(current), raw_step)

    def test_output_contract_and_pipe_safety(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
