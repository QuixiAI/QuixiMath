import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.einstein_summation_generator import EinsteinSummationGenerator
from helpers import DELIM


CONTRACTION_RE = re.compile(
    r"Given A_ij=(\[\[.*\]\]) and B_jk=(\[\[.*\]\]), compute "
    r"C_ik=A_ij B_jk using Einstein summation\."
)
TRACE_RE = re.compile(
    r"Given T_ij=(\[\[.*\]\]), compute the contraction T_ii\."
)
SYMM_RE = re.compile(
    r"Given T_ij=(\[\[.*\]\]), compute S_ij=\(T_ij\+T_ji\)/2\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def mat(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(str(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ", ".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def parse_problem(problem):
    match = CONTRACTION_RE.fullmatch(problem)
    if match:
        return {
            "variant": "contraction",
            "A": ast.literal_eval(match.group(1)),
            "B": ast.literal_eval(match.group(2)),
        }
    match = TRACE_RE.fullmatch(problem)
    if match:
        return {"variant": "trace", "T": ast.literal_eval(match.group(1))}
    match = SYMM_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "symmetrize", "T": ast.literal_eval(match.group(1))}


def expected_contraction(A, B):
    C = [[0, 0], [0, 0]]
    steps = [
        make_step("EINSTEIN_SETUP", "contract", f"A_ij={mat(A)}",
                  f"B_jk={mat(B)}"),
    ]
    for i in range(2):
        for k in range(2):
            p1 = A[i][0] * B[0][k]
            p2 = A[i][1] * B[1][k]
            C[i][k] = p1 + p2
            steps.extend([
                make_step("M", A[i][0], B[0][k], p1),
                make_step("M", A[i][1], B[1][k], p2),
                make_step("A", p1, p2, C[i][k]),
                make_step("TENSOR_ENTRY", f"C_{i + 1}{k + 1}", C[i][k]),
            ])
    answer = f"C_ik = {mat(C)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_trace(T):
    diagonal = [T[i][i] for i in range(3)]
    partial = diagonal[0] + diagonal[1]
    trace_value = partial + diagonal[2]
    steps = [make_step("EINSTEIN_SETUP", "trace", f"T_ij={mat(T)}")]
    for i, value in enumerate(diagonal, start=1):
        steps.append(make_step("TRACE_ENTRY", f"T_{i}{i}", value))
    steps.extend([
        make_step("A", diagonal[0], diagonal[1], partial),
        make_step("A", partial, diagonal[2], trace_value),
    ])
    answer = f"T_ii = {trace_value}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_symmetrize(T):
    S = [[Fraction(0) for _ in range(2)] for _ in range(2)]
    steps = [make_step("EINSTEIN_SETUP", "symmetrize", f"T_ij={mat(T)}")]
    for i in range(2):
        for j in range(2):
            total = T[i][j] + T[j][i]
            value = Fraction(total, 2)
            S[i][j] = value
            steps.extend([
                make_step("A", T[i][j], T[j][i], total),
                make_step("D", total, 2, fraction_text(value)),
                make_step("TENSOR_ENTRY", f"S_{i + 1}{j + 1}",
                          fraction_text(value)),
            ])
    answer = f"S_ij = {matrix_text(S)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "contraction":
        return expected_contraction(parts["A"], parts["B"])
    if parts["variant"] == "trace":
        return expected_trace(parts["T"])
    return expected_symmetrize(parts["T"])


class TestEinsteinSummationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EinsteinSummationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in EinsteinSummationGenerator.VARIANTS:
            result = EinsteinSummationGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"einstein_summation_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EinsteinSummationGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
