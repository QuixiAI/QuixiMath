import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ecdh_generator import ECDHGenerator
from helpers import DELIM
from tests.advanced_generator_oracles import ecdh_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestECDHGenerator(unittest.TestCase):
    def test_contract_oracle_and_shared_check(self):
        random.seed(123)
        gen = ECDHGenerator()
        secrets = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             ecdh_oracle(result["problem"]))
            check = next(s for s in result["steps"] if s.startswith("CHECK|"))
            _, left, right = check.split(DELIM)
            self.assertEqual(left, right)
            secrets.add(result["problem"].split("Alice secret ", 1)[1]
                        .split(".", 1)[0])
        self.assertGreaterEqual(len(secrets), 2)


if __name__ == "__main__":
    unittest.main()
