import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.reed_solomon_generator import ReedSolomonGenerator
from tests.advanced_generator_oracles import (
    assert_exact_step_arithmetic,
    reed_solomon_oracle,
)
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestReedSolomonGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_arithmetic(self):
        random.seed(123)
        gen = ReedSolomonGenerator()
        saw = set()
        for _ in range(160):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             reed_solomon_oracle(result["problem"]))
            if result["operation"].endswith("_encode"):
                assert_exact_step_arithmetic(self, result)
            saw.add(result["operation"])
        self.assertEqual(saw, {f"reed_solomon_{v}"
                               for v in ReedSolomonGenerator.VARIANTS})

    def test_explicit_variants(self):
        for variant in ReedSolomonGenerator.VARIANTS:
            result = ReedSolomonGenerator(variant).generate()
            self.assertEqual(result["operation"], f"reed_solomon_{variant}")
            self.assertEqual(result["final_answer"],
                             reed_solomon_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            ReedSolomonGenerator("bad")


if __name__ == "__main__":
    unittest.main()
