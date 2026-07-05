import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.convolutional_code_viterbi_generator import (
    ConvolutionalCodeViterbiGenerator,
)
from tests.advanced_generator_oracles import convolutional_code_viterbi_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestConvolutionalCodeViterbiGenerator(unittest.TestCase):
    def test_contract_oracle_and_trace(self):
        random.seed(123)
        gen = ConvolutionalCodeViterbiGenerator()
        messages = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             convolutional_code_viterbi_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("CONV_RECEIVED|")
                                for s in result["steps"]))
            messages.add(result["problem"].split("Encode message ", 1)[1]
                         .split(".", 1)[0])
        self.assertGreaterEqual(len(messages), 2)


if __name__ == "__main__":
    unittest.main()
