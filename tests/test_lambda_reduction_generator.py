import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lambda_reduction_generator import LambdaReductionGenerator
from helpers import DELIM
from tests.advanced_generator_oracles import lambda_reduction_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestLambdaReductionGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = LambdaReductionGenerator()
        saw = set()
        openings = set()
        for _ in range(160):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             lambda_reduction_oracle(result["problem"]))
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "REWRITE":
                    self.assertNotIn("applied", fields[1])
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
        self.assertEqual(saw, {f"lambda_reduction_{v}"
                               for v in LambdaReductionGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in LambdaReductionGenerator.VARIANTS:
            result = LambdaReductionGenerator(variant).generate()
            self.assertEqual(result["operation"], f"lambda_reduction_{variant}")
            self.assertEqual(result["final_answer"],
                             lambda_reduction_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            LambdaReductionGenerator("bad")


if __name__ == "__main__":
    unittest.main()
