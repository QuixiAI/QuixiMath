import ast
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gamma_matrix_generator import GammaMatrixGenerator
from helpers import DELIM


MATRIX = r"(\[\[.*?\]\])"
ANTI_RE = re.compile(
    rf"Given (gamma[013])={MATRIX} and (gamma[013])={MATRIX} with "
    r"eta_([013])([013])=(-?\d+), compute entry \((\d+),(\d+)\) "
    r"of \{(gamma[013]),(gamma[013])\}="
    r"(gamma[013])\*(gamma[013])\+(gamma[013])\*(gamma[013])\."
)
TRACE_RE = re.compile(
    rf"Given (gamma[013])={MATRIX} and (gamma[013])={MATRIX} with "
    r"eta_([013])([013])=(-?\d+), compute Tr\((gamma[013])\*(gamma[013])\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def dot_expr(row, col):
    return " + ".join(f"{a}*{b}" for a, b in zip(row, col))


def dot_value(row, col):
    return sum(a * b for a, b in zip(row, col))


def parse_problem(problem):
    match = ANTI_RE.fullmatch(problem)
    if match:
        left = match.group(1)
        left_matrix = ast.literal_eval(match.group(2))
        right = match.group(3)
        right_matrix = ast.literal_eval(match.group(4))
        assert match.group(5) == left[-1]
        assert match.group(6) == right[-1]
        for group_no, expected in ((10, left), (11, right),
                                   (12, left), (13, right),
                                   (14, right), (15, left)):
            assert match.group(group_no) == expected
        return {
            "variant": "anticommutator_entry",
            "left": left,
            "right": right,
            "matrices": {left: left_matrix, right: right_matrix},
            "eta": int(match.group(7)),
            "row": int(match.group(8)) - 1,
            "col": int(match.group(9)) - 1,
        }
    match = TRACE_RE.fullmatch(problem)
    assert match is not None, problem
    left = match.group(1)
    left_matrix = ast.literal_eval(match.group(2))
    right = match.group(3)
    right_matrix = ast.literal_eval(match.group(4))
    assert match.group(5) == left[-1]
    assert match.group(6) == right[-1]
    assert match.group(8) == left
    assert match.group(9) == right
    return {
        "variant": "trace",
        "left": left,
        "right": right,
        "matrices": {left: left_matrix, right: right_matrix},
        "eta": int(match.group(7)),
    }


def dot_step(product_name, left_matrix, right_matrix, row, col):
    row_values = left_matrix[row]
    col_values = [right_matrix[k][col] for k in range(4)]
    return make_step(
        "DOT4", product_name, f"({row + 1},{col + 1})",
        dot_expr(row_values, col_values), dot_value(row_values, col_values)
    )


def expected_anticommutator(parts):
    left = parts["left"]
    right = parts["right"]
    matrices = parts["matrices"]
    row = parts["row"]
    col = parts["col"]
    eta = parts["eta"]
    ab_name = f"{left}{right}"
    ba_name = f"{right}{left}"
    steps = [
        make_step("GAMMA_SETUP", "anticommutator_entry",
                  f"{left},{right}", f"entry=({row + 1},{col + 1})"),
        make_step("MATRIX_PRODUCT", ab_name, f"{left}*{right}"),
        dot_step(ab_name, matrices[left], matrices[right], row, col),
        make_step("MATRIX_PRODUCT", ba_name, f"{right}*{left}"),
        dot_step(ba_name, matrices[right], matrices[left], row, col),
    ]
    ab = int(steps[2].split(DELIM)[4])
    ba = int(steps[4].split(DELIM)[4])
    total = ab + ba
    expected = 2 * eta if row == col else 0
    steps.extend([
        make_step("MATRIX_ENTRY_SUM", f"({row + 1},{col + 1})",
                  f"{ab} + {ba}", total),
        make_step("CLIFFORD_EXPECT", f"2*eta={2 * eta}",
                  f"I_entry={1 if row == col else 0}", expected),
        make_step("CHECK", "anticommutator entry",
                  f"computed={total}", f"expected={expected}"),
    ])
    answer = f"{{{left},{right}}}_({row + 1},{col + 1}) = {total}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_trace(parts):
    left = parts["left"]
    right = parts["right"]
    matrices = parts["matrices"]
    eta = parts["eta"]
    product_name = f"{left}{right}"
    steps = [
        make_step("GAMMA_SETUP", "trace", f"{left},{right}",
                  "Tr(product)"),
        make_step("MATRIX_PRODUCT", product_name, f"{left}*{right}"),
    ]
    trace_total = 0
    for index in range(4):
        raw_dot = dot_step(product_name, matrices[left], matrices[right],
                           index, index)
        steps.append(raw_dot)
        entry = int(raw_dot.split(DELIM)[4])
        next_total = trace_total + entry
        steps.append(
            make_step("TRACE_ADD", product_name,
                      f"({index + 1},{index + 1})",
                      f"{trace_total} + {entry}", next_total)
        )
        trace_total = next_total
    expected = 4 * eta
    steps.extend([
        make_step("TRACE_EXPECT", f"4*eta_{left[-1]}{right[-1]}",
                  eta, expected),
        make_step("CHECK", "trace theorem",
                  f"computed={trace_total}", f"expected={expected}"),
    ])
    answer = f"Tr({left}*{right}) = {trace_total}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "anticommutator_entry":
        return expected_anticommutator(parts)
    return expected_trace(parts)


class TestGammaMatrixGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GammaMatrixGenerator()

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

    def test_dot_and_trace_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "DOT4":
                    terms = fields[3].split(" + ")
                    total = 0
                    for term in terms:
                        left, right = term.split("*")
                        total += int(left) * int(right)
                    self.assertEqual(total, int(fields[4]), raw_step)
                elif fields[0] == "MATRIX_ENTRY_SUM":
                    left, right = fields[2].split(" + ")
                    self.assertEqual(int(left) + int(right),
                                     int(fields[3]), raw_step)
                elif fields[0] == "TRACE_ADD":
                    left, right = fields[3].split(" + ")
                    self.assertEqual(int(left) + int(right),
                                     int(fields[4]), raw_step)

    def test_checks_are_satisfied(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] != "CHECK":
                    continue
                computed = int(fields[2].removeprefix("computed="))
                expected = int(fields[3].removeprefix("expected="))
                self.assertEqual(computed, expected, raw_step)

    def test_variants_are_available(self):
        for variant in GammaMatrixGenerator.VARIANTS:
            result = GammaMatrixGenerator(variant).generate()
            self.assertEqual(result["operation"], f"gamma_matrix_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GammaMatrixGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(100)}
        self.assertEqual(
            seen,
            {"gamma_matrix_anticommutator_entry", "gamma_matrix_trace"},
        )


if __name__ == "__main__":
    unittest.main()
