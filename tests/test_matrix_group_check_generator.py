import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.matrix_group_check_generator import MatrixGroupCheckGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Check whether M=\[\[([^,]+),([^]]+)\],\[([^,]+),([^]]+)\]\] "
    r"is a member of (SO2|SU2)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "c": Fraction(match.group(1)),
        "neg_s": Fraction(match.group(2)),
        "s": Fraction(match.group(3)),
        "c2": Fraction(match.group(4)),
        "group": match.group(5).lower(),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    c = parts["c"]
    s = parts["s"]
    neg_s = parts["neg_s"]
    c_sq = c ** 2
    s_sq = s ** 2
    norm = c_sq + s_sq
    det_left = c * c
    det_right = neg_s * s
    det = det_left - det_right
    matrix = (
        f"[[{fraction_text(c)},{fraction_text(neg_s)}],"
        f"[{fraction_text(s)},{fraction_text(c)}]]"
    )
    product_label = "R^T R" if parts["group"] == "so2" else "U^dagger U"
    adjoint_label = "R^T" if parts["group"] == "so2" else "U^dagger"
    matrix_symbol = "R" if parts["group"] == "so2" else "U"
    answer = (
        f"{parts['group'].upper()} member yes; "
        f"{adjoint_label} {matrix_symbol} = I, det = 1"
    )
    steps = [
        make_step("MATRIX_GROUP_SETUP", parts["group"].upper(),
                  f"M={matrix}"),
        make_step("E", fraction_text(c), 2, fraction_text(c_sq)),
        make_step("E", fraction_text(s), 2, fraction_text(s_sq)),
        make_step("A", fraction_text(c_sq), fraction_text(s_sq),
                  fraction_text(norm)),
        make_step("CHECK", product_label, "I", "metric preserved"),
        make_step("M", fraction_text(c), fraction_text(c),
                  fraction_text(det_left)),
        make_step("M", fraction_text(neg_s), fraction_text(s),
                  fraction_text(det_right)),
        make_step("S", fraction_text(det_left), fraction_text(det_right),
                  fraction_text(det)),
        make_step("CHECK", "det M", fraction_text(det), "special"),
        make_step("Z", answer),
    ]
    return steps, answer


class TestMatrixGroupCheckGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MatrixGroupCheckGenerator()

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
        for variant in ("so2", "su2"):
            result = MatrixGroupCheckGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"matrix_group_check_{variant}")
            self.assertEqual(parse_problem(result["problem"])["group"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MatrixGroupCheckGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
