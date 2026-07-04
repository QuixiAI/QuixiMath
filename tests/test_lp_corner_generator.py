import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.lp_corner_generator import LPCornerGenerator, vertex_text
from helpers import DELIM


# coefficient 1 is rendered without the digit (x, not 1x), so the
# coefficient groups are optional
PROBLEM_RE = re.compile(
    r"Use the corner-point method to maximize z = (\d*)x \+ (\d*)y "
    r"subject to 0 <= x <= (\d+), 0 <= y <= (\d+), and x \+ y <= "
    r"(\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(int(match.group(i)) if match.group(i) else 1
                 for i in range(1, 6))


def objective_value(c1, c2, vertex):
    x_value, y_value = vertex
    return c1 * x_value + c2 * y_value


def expected_flow(example):
    c1, c2, x_bound, y_bound, diagonal = parse_problem(example["problem"])
    y_on_right = diagonal - x_bound
    x_on_top = diagonal - y_bound
    vertices = [
        (0, 0),
        (x_bound, 0),
        (x_bound, y_on_right),
        (x_on_top, y_bound),
        (0, y_bound),
    ]
    values = [objective_value(c1, c2, vertex) for vertex in vertices]
    best_value = max(values)
    best_vertex = vertices[values.index(best_value)]
    x_term_text = "x" if c1 == 1 else f"{c1}x"
    y_term_text = "y" if c2 == 1 else f"{c2}y"
    steps = [
        make_step("LP_CORNER_SETUP", f"max z={x_term_text}+{y_term_text}",
                  f"0<=x<={x_bound}, 0<=y<={y_bound}",
                  f"x+y<={diagonal}"),
        make_step("VERTEX_SOLVE", "x=0", "y=0"),
        make_step("VERTEX", vertex_text(0, 0)),
        make_step("VERTEX_SOLVE", f"x={x_bound}", "y=0"),
        make_step("VERTEX", vertex_text(x_bound, 0)),
        make_step("VERTEX_SOLVE", f"x={x_bound}", f"x+y={diagonal}"),
        make_step("S", diagonal, x_bound, y_on_right),
        make_step("VERTEX", vertex_text(x_bound, y_on_right)),
        make_step("VERTEX_SOLVE", f"y={y_bound}", f"x+y={diagonal}"),
        make_step("S", diagonal, y_bound, x_on_top),
        make_step("VERTEX", vertex_text(x_on_top, y_bound)),
        make_step("VERTEX_SOLVE", "x=0", f"y={y_bound}"),
        make_step("VERTEX", vertex_text(0, y_bound)),
    ]
    for vertex, value in zip(vertices, values):
        x_value, y_value = vertex
        x_term = c1 * x_value
        y_term = c2 * y_value
        steps += [
            make_step("OBJECTIVE", f"at {vertex_text(x_value, y_value)}"),
            make_step("M", c1, x_value, x_term),
            make_step("M", c2, y_value, y_term),
            make_step("A", x_term, y_term, value),
        ]
    steps.append(make_step("CHECK", f"max value {best_value}",
                           f"at {vertex_text(*best_vertex)}"))
    answer = (
        f"optimal vertex={vertex_text(*best_vertex)}, "
        f"max z={best_value}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestLPCornerGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LPCornerGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "lp_corner_point")
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

    def test_vertices_are_feasible(self):
        for _ in range(300):
            result = self.gen.generate()
            _, _, x_bound, y_bound, diagonal = parse_problem(result["problem"])
            vertex_matches = re.findall(r"VERTEX\|\((\d+),(\d+)\)",
                                        "\n".join(result["steps"]))
            for x_raw, y_raw in vertex_matches:
                x_value = int(x_raw)
                y_value = int(y_raw)
                self.assertGreaterEqual(x_value, 0)
                self.assertGreaterEqual(y_value, 0)
                self.assertLessEqual(x_value, x_bound)
                self.assertLessEqual(y_value, y_bound)
                self.assertLessEqual(x_value + y_value, diagonal)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
