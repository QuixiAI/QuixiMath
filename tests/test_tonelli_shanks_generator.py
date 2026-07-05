import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.tonelli_shanks_generator import TonelliShanksGenerator
from tests.advanced_generator_oracles import tonelli_shanks_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestTonelliShanksGenerator(unittest.TestCase):
    def test_contract_oracle_and_trace(self):
        random.seed(123)
        gen = TonelliShanksGenerator()
        primes = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             tonelli_shanks_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("TS_FACTOR|")
                                for s in result["steps"]))
            primes.add(result["final_answer"].rsplit(" ", 1)[1])
        self.assertGreaterEqual(len(primes), 2)


if __name__ == "__main__":
    unittest.main()
