import itertools
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.resolution_proof_generator import ResolutionProofGenerator
from tests.advanced_generator_oracles import resolution_proof_oracle
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def clauses_from_problem(problem):
    return [tuple(raw.split(" OR "))
            for raw in re.findall(r"C\d+=\(([^)]*)\)", problem)]


def satisfies(clauses, assignment):
    for clause in clauses:
        clause_value = False
        for literal in clause:
            if literal.startswith("not "):
                clause_value |= not assignment[literal[4:]]
            else:
                clause_value |= assignment[literal]
        if not clause_value:
            return False
    return True


class TestResolutionProofGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = ResolutionProofGenerator()
        saw = set()
        openings = set()
        for _ in range(120):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"],
                             resolution_proof_oracle(result["problem"]))
            self.assertTrue(any(s.startswith("RES_EMPTY|")
                                for s in result["steps"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 1)[0])
        self.assertEqual(saw, {f"resolution_proof_{v}"
                               for v in ResolutionProofGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_explicit_variants(self):
        for variant in ResolutionProofGenerator.VARIANTS:
            result = ResolutionProofGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"resolution_proof_{variant}")
            self.assertEqual(result["final_answer"],
                             resolution_proof_oracle(result["problem"]))

    def test_problem_cnf_is_unsatisfiable_by_brute_force(self):
        for _ in range(300):
            result = ResolutionProofGenerator().generate()
            clauses = clauses_from_problem(result["problem"])
            variables = sorted({literal.removeprefix("not ")
                                for clause in clauses for literal in clause})
            has_model = False
            for values in itertools.product((False, True),
                                            repeat=len(variables)):
                assignment = dict(zip(variables, values))
                if satisfies(clauses, assignment):
                    has_model = True
                    break
            self.assertFalse(has_model, result["problem"])

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            ResolutionProofGenerator("bad")


if __name__ == "__main__":
    unittest.main()
