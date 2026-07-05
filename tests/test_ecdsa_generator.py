import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ecdsa_generator import ECDSAGenerator
from tests.advanced_generator_oracles import ecdsa_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestECDSAGenerator(unittest.TestCase):
    def test_contract_oracle_and_verification(self):
        random.seed(123)
        gen = ECDSAGenerator()
        signatures = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             ecdsa_oracle(result["problem"]))
            self.assertIn("verification = valid", result["final_answer"])
            self.assertTrue(any(s.startswith("ECDSA_VERIFY|")
                                for s in result["steps"]))
            signatures.add(result["final_answer"])
        self.assertGreaterEqual(len(signatures), 2)


if __name__ == "__main__":
    unittest.main()
