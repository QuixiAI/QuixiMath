import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.baby_step_giant_step_generator import BabyStepGiantStepGenerator
from tests.advanced_generator_oracles import baby_step_giant_step_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestBabyStepGiantStepGenerator(unittest.TestCase):
    def test_contract_oracle_and_trace(self):
        random.seed(123)
        gen = BabyStepGiantStepGenerator()
        groups = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             baby_step_giant_step_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("BSGS_MATCH|")
                                for s in result["steps"]))
            groups.add(result["problem"].split(" modulo ", 1)[1]
                       .split(",", 1)[0])
        self.assertGreaterEqual(len(groups), 2)


if __name__ == "__main__":
    unittest.main()
