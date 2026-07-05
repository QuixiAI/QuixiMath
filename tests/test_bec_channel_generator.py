import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.bec_channel_generator import BECChannelGenerator
from tests.advanced_generator_oracles import (
    assert_exact_step_arithmetic,
    bec_channel_oracle,
)
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestBECChannelGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_arithmetic(self):
        random.seed(123)
        gen = BECChannelGenerator()
        saw = set()
        for _ in range(160):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             bec_channel_oracle(result["problem"]))
            assert_exact_step_arithmetic(self, result)
            saw.add(result["operation"])
        self.assertEqual(saw, {f"bec_channel_{v}"
                               for v in BECChannelGenerator.VARIANTS})

    def test_explicit_variants(self):
        for variant in BECChannelGenerator.VARIANTS:
            result = BECChannelGenerator(variant).generate()
            self.assertEqual(result["operation"], f"bec_channel_{variant}")
            self.assertEqual(result["final_answer"],
                             bec_channel_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            BECChannelGenerator("bad")


if __name__ == "__main__":
    unittest.main()
