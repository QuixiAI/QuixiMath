import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.simplex_generator import SimplexGenerator
from helpers import DELIM


# c2 = 1 renders without the coefficient (y, not 1y), so its group is optional
PROBLEM_RE = re.compile(
    r"Use the simplex method to maximize z = (\d+)x \+ (\d*)y "
    r"subject to x <= (\d+), y <= (\d+), x >= 0, y >= 0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    c1 = int(match.group(1))
    c2 = int(match.group(2)) if match.group(2) else 1
    x_bound, y_bound = int(match.group(3)), int(match.group(4))
    return c1, c2, x_bound, y_bound


def expected_flow(example):
    c1, c2, x_bound, y_bound = parse_problem(example["problem"])
    zx = c1 * x_bound
    zy = c2 * y_bound
    z_value = zx + zy
    y_term = "y" if c2 == 1 else f"{c2}y"
    steps = [
        make_step("SIMPLEX_SETUP", f"max z={c1}x+{y_term}",
                  f"x<={x_bound}", f"y<={y_bound}"),
        make_step("TABLEAU", "initial",
                  f"s1: x + s1 = {x_bound}",
                  f"s2: y + s2 = {y_bound}"),
        make_step("TABLEAU", "z row", f"-{c1}x - {y_term} + z = 0"),
        make_step("ENTER", "x", f"most negative reduced cost -{c1}"),
        make_step("D", x_bound, 1, x_bound),
        make_step("RATIO", "s1 row", f"{x_bound}/1", x_bound),
        make_step("PIVOT", "row=s1", "column=x", "pivot=1"),
        make_step("ROW_OP", f"z <- z + {c1}*s1"),
        make_step("M", c1, x_bound, zx),
        make_step("TABLEAU", "after x pivot",
                  f"x={x_bound} - s1",
                  f"z row: -{y_term} + {c1}s1 + z = {zx}"),
        make_step("ENTER", "y", f"remaining negative reduced cost -{c2}"),
        make_step("D", y_bound, 1, y_bound),
        make_step("RATIO", "s2 row", f"{y_bound}/1", y_bound),
        make_step("PIVOT", "row=s2", "column=y", "pivot=1"),
        make_step("ROW_OP", f"z <- z + {c2}*s2"),
        make_step("M", c2, y_bound, zy),
        make_step("A", zx, zy, z_value),
        make_step("TABLEAU", "final",
                  f"x={x_bound}, y={y_bound}",
                  f"z={z_value}"),
        make_step("CHECK", "reduced costs for x,y are 0",
                  "optimal tableau"),
    ]
    answer = f"x={x_bound}, y={y_bound}, max z={z_value}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestSimplexGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SimplexGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "simplex_two_variable_tableau")
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

    def test_solution_is_feasible_and_optimal_for_box(self):
        for _ in range(300):
            result = self.gen.generate()
            c1, c2, x_bound, y_bound = parse_problem(result["problem"])
            answer = f"x={x_bound}, y={y_bound}, max z={c1*x_bound+c2*y_bound}"
            self.assertEqual(result["final_answer"], answer)

    def test_enough_unique_problems_for_sampling(self):
        problems = {self.gen.generate()["problem"] for _ in range(500)}
        self.assertGreaterEqual(len(problems), 200)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
