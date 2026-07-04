import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.projector_generator import ProjectorGenerator
from helpers import DELIM


PLUS_RE = re.compile(
    r"Verify that P_plus=\[\[1/2,1/2\],\[1/2,1/2\]\] is a projector\."
)
BASIS_RE = re.compile(
    r"Verify projector completeness for P0=\[\[1,0\],\[0,0\]\] and "
    r"P1=\[\[0,0\],\[0,1\]\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    if PLUS_RE.fullmatch(problem):
        return "plus_projector"
    assert BASIS_RE.fullmatch(problem), problem
    return "basis_completeness"


def expected_flow(example):
    variant = parse_problem(example["problem"])
    if variant == "plus_projector":
        p = "[[1/2,1/2],[1/2,1/2]]"
        answer = "projector yes; P^2 = P"
        steps = [
            make_step("PROJECTOR_SETUP", "P_plus=ket+bra+", f"P={p}"),
            make_step("MATRIX_MULT", "row1 dot col1", "1/4+1/4", "1/2"),
            make_step("MATRIX_MULT", "row1 dot col2", "1/4+1/4", "1/2"),
            make_step("MATRIX_MULT", "row2 dot col1", "1/4+1/4", "1/2"),
            make_step("MATRIX_MULT", "row2 dot col2", "1/4+1/4", "1/2"),
            make_step("CHECK", "P^2", p, "idempotent"),
            make_step("Z", answer),
        ]
    else:
        p0 = "[[1,0],[0,0]]"
        p1 = "[[0,0],[0,1]]"
        identity = "[[1,0],[0,1]]"
        answer = "complete yes; P0 + P1 = I"
        steps = [
            make_step("PROJECTOR_SETUP", f"P0={p0}", f"P1={p1}"),
            make_step("MATRIX_MULT", "P0^2", p0),
            make_step("MATRIX_MULT", "P1^2", p1),
            make_step("MATRIX_ADD", "P0+P1", identity),
            make_step("CHECK", "sum_i Pi", identity, "complete"),
            make_step("Z", answer),
        ]
    return steps, answer


class TestProjectorGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ProjectorGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(100):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_variants_are_available(self):
        for variant in ("plus_projector", "basis_completeness"):
            result = ProjectorGenerator(variant).generate()
            self.assertEqual(result["operation"], f"projector_{variant}")
            self.assertEqual(parse_problem(result["problem"]), variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ProjectorGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(100):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
