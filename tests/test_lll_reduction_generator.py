import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lll_reduction_generator import LLLReductionGenerator
from tests.advanced_generator_oracles import lll_reduction_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestLLLReductionGenerator(unittest.TestCase):
    def test_contract_oracle_and_formatting(self):
        random.seed(123)
        gen = LLLReductionGenerator()
        bases = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             lll_reduction_oracle(result["problem"]))
            self.assertFalse(any("--" in s for s in result["steps"]))
            self.assertTrue(any(s.startswith("LLL_DONE|")
                                for s in result["steps"]))
            bases.add(result["problem"].split("basis ", 1)[1]
                      .split(".", 1)[0])
        self.assertGreaterEqual(len(bases), 2)


if __name__ == "__main__":
    unittest.main()
