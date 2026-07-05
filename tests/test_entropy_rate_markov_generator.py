import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.entropy_rate_markov_generator import EntropyRateMarkovGenerator
from tests.advanced_generator_oracles import (
    assert_exact_step_arithmetic,
    entropy_rate_markov_oracle,
)
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestEntropyRateMarkovGenerator(unittest.TestCase):
    def test_contract_oracle_and_trace(self):
        random.seed(123)
        gen = EntropyRateMarkovGenerator()
        cases = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             entropy_rate_markov_oracle(result["problem"]))
            assert_exact_step_arithmetic(self, result)
            self.assertTrue(any(s.startswith("STATIONARY|")
                                for s in result["steps"]))
            cases.add(result["problem"].split(", use ", 1)[0])
        self.assertGreaterEqual(len(cases), 2)


if __name__ == "__main__":
    unittest.main()
