import os
import random
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.turing_machine_trace_generator import TuringMachineTraceGenerator
from tests.advanced_generator_oracles import turing_machine_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


class TestTuringMachineTraceGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = TuringMachineTraceGenerator()
        saw = set()
        openings = set()
        for _ in range(200):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             turing_machine_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("TM_CONFIG|")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith("CHECK|")
                                for s in result["steps"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
        self.assertEqual(saw, {f"turing_machine_trace_{v}"
                               for v in TuringMachineTraceGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in TuringMachineTraceGenerator.VARIANTS:
            result = TuringMachineTraceGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"turing_machine_trace_{variant}")
            self.assertEqual(result["final_answer"],
                             turing_machine_oracle(result["problem"]))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            TuringMachineTraceGenerator("bad")


if __name__ == "__main__":
    unittest.main()
