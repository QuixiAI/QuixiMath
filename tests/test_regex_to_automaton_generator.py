import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.regex_to_automaton_generator import RegexToAutomatonGenerator
from tests.advanced_generator_oracles import regex_to_automaton_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestRegexToAutomatonGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = RegexToAutomatonGenerator()
        saw = set()
        openings = set()
        for _ in range(200):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             regex_to_automaton_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("REGEX_TRANSITION|")
                                for s in result["steps"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
        self.assertEqual(saw, {f"regex_to_automaton_{v}"
                               for v in RegexToAutomatonGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in RegexToAutomatonGenerator.VARIANTS:
            result = RegexToAutomatonGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"regex_to_automaton_{variant}")
            self.assertEqual(result["final_answer"],
                             regex_to_automaton_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            RegexToAutomatonGenerator("bad")


if __name__ == "__main__":
    unittest.main()
