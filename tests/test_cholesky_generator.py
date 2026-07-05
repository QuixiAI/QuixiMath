import random
import unittest

from generators.cholesky_generator import CholeskyGenerator
from tests.new_generator_test_utils import (
    assert_contract,
    assert_pipe_safe,
    oracle_cholesky,
)


class TestCholeskyGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CholeskyGenerator()

    def test_output_contract(self):
        assert_contract(self, self.gen.generate())

    def test_oracle_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(oracle_cholesky(result),
                            (result["problem"], result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(200):
            assert_pipe_safe(self, self.gen.generate())


if __name__ == "__main__":
    unittest.main()
