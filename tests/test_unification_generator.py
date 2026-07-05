import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.unification_generator import UnificationGenerator
from tests.advanced_generator_oracles import unification_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestUnificationGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = UnificationGenerator()
        saw = set()
        openings = set()
        for _ in range(160):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             unification_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("UNIFY_PAIR|")
                                for s in result["steps"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
        self.assertEqual(saw, {f"unification_{v}"
                               for v in UnificationGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in UnificationGenerator.VARIANTS:
            result = UnificationGenerator(variant).generate()
            self.assertEqual(result["operation"], f"unification_{variant}")
            self.assertEqual(result["final_answer"],
                             unification_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            UnificationGenerator("bad")


if __name__ == "__main__":
    unittest.main()
