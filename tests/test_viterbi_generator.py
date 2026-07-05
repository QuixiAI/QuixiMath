import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.viterbi_generator import ViterbiGenerator
from tests.advanced_generator_oracles import viterbi_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestViterbiGenerator(unittest.TestCase):
    def test_contract_oracle_and_trace(self):
        random.seed(123)
        gen = ViterbiGenerator()
        observations = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             viterbi_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("VITERBI_BACKTRACE|")
                                for s in result["steps"]))
            observations.add(result["problem"].split("observations ", 1)[1]
                             .split(" ", 1)[0])
        self.assertGreaterEqual(len(observations), 2)


if __name__ == "__main__":
    unittest.main()
