import itertools
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dpll_trace_generator import DPLLTraceGenerator
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def parse_formula(problem):
    match = re.search(r"(\([^)]+\)(?: AND \([^)]+\))*)", problem)
    assert match is not None, problem
    clauses = []
    for raw_clause in re.findall(r"\(([^)]+)\)", match.group(1)):
        clauses.append(tuple(raw_clause.split(" OR ")))
    return clauses


def literal_var(literal):
    return literal[4:] if literal.startswith("not ") else literal


def literal_holds(literal, assignment):
    value = assignment[literal_var(literal)]
    return not value if literal.startswith("not ") else value


def oracle(problem):
    clauses = parse_formula(problem)
    variables = sorted({literal_var(lit) for clause in clauses
                        for lit in clause})
    for values in itertools.product([True, False], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(any(literal_holds(lit, assignment) for lit in clause)
               for clause in clauses):
            text = ", ".join(f"{v}={'True' if assignment[v] else 'False'}"
                             for v in variables)
            return f"satisfiable; {text}"
    return "unsatisfiable"


class TestDPLLTraceGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_phrasing(self):
        random.seed(123)
        gen = DPLLTraceGenerator()
        saw = set()
        openings = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 2)[0])
        self.assertEqual(saw, {f"dpll_trace_{v}"
                               for v in DPLLTraceGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            DPLLTraceGenerator("bad")


if __name__ == "__main__":
    unittest.main()
