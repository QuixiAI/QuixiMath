import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.hermitian_check_generator import HermitianCheckGenerator
from helpers import DELIM


HERM_RE = re.compile(
    r"Check whether A=\[\[(-?\d+),(-?\d+)\],\[\2,\1\]\] is Hermitian "
    r"and find its eigenvalues\."
)
UNITARY_RE = re.compile(
    r"Check whether U=\[\[([^,]+),([^]]+)\],\[([^,]+),([^]]+)\]\] "
    r"is unitary\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = HERM_RE.fullmatch(problem)
    if match:
        return {"variant": "hermitian", "a": int(match.group(1)),
                "b": int(match.group(2))}
    match = UNITARY_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "unitary", "c": Fraction(match.group(1)),
            "neg_s": Fraction(match.group(2)),
            "s": Fraction(match.group(3)),
            "c2": Fraction(match.group(4))}


def expected_hermitian(parts):
    a = parts["a"]
    b = parts["b"]
    lam1 = a + b
    lam2 = a - b
    matrix = f"[[{a},{b}],[{b},{a}]]"
    answer = f"Hermitian yes; eigenvalues = {lam1}, {lam2}"
    steps = [
        make_step("MATRIX_SETUP", "hermitian", f"A={matrix}"),
        make_step("ADJOINT", f"A^dagger={matrix}"),
        make_step("CHECK", "A = A^dagger", "yes", "Hermitian"),
        make_step("A", a, b, lam1),
        make_step("S", a, b, lam2),
        make_step("CHECK", "eigenvalues real", f"{lam1},{lam2}", "real"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_unitary(parts):
    c = parts["c"]
    s = parts["s"]
    neg_s = parts["neg_s"]
    c_sq = c ** 2
    s_sq = s ** 2
    norm = c_sq + s_sq
    left_off = c * neg_s
    right_off = s * c
    offdiag = left_off + right_off
    matrix = (
        f"[[{fraction_text(c)},{fraction_text(neg_s)}],"
        f"[{fraction_text(s)},{fraction_text(c)}]]"
    )
    adjoint = (
        f"[[{fraction_text(c)},{fraction_text(s)}],"
        f"[{fraction_text(neg_s)},{fraction_text(c)}]]"
    )
    answer = "unitary yes; U^dagger U = I"
    steps = [
        make_step("MATRIX_SETUP", "unitary", f"U={matrix}"),
        make_step("ADJOINT", f"U^dagger={adjoint}"),
        make_step("E", fraction_text(c), 2, fraction_text(c_sq)),
        make_step("E", fraction_text(s), 2, fraction_text(s_sq)),
        make_step("A", fraction_text(c_sq), fraction_text(s_sq),
                  fraction_text(norm)),
        make_step("M", fraction_text(c), fraction_text(neg_s),
                  fraction_text(left_off)),
        make_step("M", fraction_text(s), fraction_text(c),
                  fraction_text(right_off)),
        make_step("A", fraction_text(left_off), fraction_text(right_off),
                  fraction_text(offdiag)),
        make_step("CHECK", "U^dagger U", "I", "unitary"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "hermitian":
        return expected_hermitian(parts)
    return expected_unitary(parts)


class TestHermitianCheckGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = HermitianCheckGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("hermitian", "unitary"):
            gen = HermitianCheckGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"hermitian_check_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            HermitianCheckGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
