import ast
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.graph_counting_generator import GraphCountingGenerator
from helpers import DELIM


DEGREE_RE = re.compile(
    r"In the undirected graph with vertices ([A-Z](?:, [A-Z])*) and edges "
    r"([A-Z]{2}(?:, [A-Z]{2})*), find the degree sequence and verify the "
    r"handshake count\."
)
WALK_RE = re.compile(
    r"For the directed graph with adjacency matrix A = (\[\[.*\]\]), how "
    r"many walks of length 2 go from vertex (\d+) to vertex (\d+)\?"
)


def parse_problem(problem):
    match = DEGREE_RE.fullmatch(problem)
    if match:
        vertices = match.group(1).split(", ")
        edges = [tuple(edge) for edge in match.group(2).split(", ")]
        return {"variant": "degree_sequence", "vertices": vertices,
                "edges": edges}
    match = WALK_RE.fullmatch(problem)
    assert match is not None, problem
    matrix = ast.literal_eval(match.group(1))
    start, end = map(int, match.groups()[1:])
    return {"variant": "walk_count", "matrix": matrix,
            "start": start, "end": end}


def degree_parts(parts):
    vertices = parts["vertices"]
    neighbors = {vertex: set() for vertex in vertices}
    for u, v in parts["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    degrees = {vertex: len(neighbors[vertex]) for vertex in vertices}
    sequence = sorted(degrees.values(), reverse=True)
    degree_sum = sum(sequence)
    return neighbors, degrees, sequence, degree_sum


def walk_count(parts):
    matrix = parts["matrix"]
    start = parts["start"] - 1
    end = parts["end"] - 1
    total = 0
    for mid in range(len(matrix)):
        total += matrix[start][mid] * matrix[mid][end]
    return total


def oracle_answer(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "degree_sequence":
        _, _, sequence, degree_sum = degree_parts(parts)
        seq_text = ", ".join(str(value) for value in sequence)
        return f"degree sequence = [{seq_text}]; degree sum = {degree_sum}"
    return f"walks = {walk_count(parts)}"


def check_step_arithmetic(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "degree_sequence":
        neighbors, degrees, sequence, degree_sum = degree_parts(parts)
        edge_count = len(parts["edges"])
    else:
        matrix = parts["matrix"]

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "EDGE_COUNT":
            if fields[1:] != ["m", str(edge_count)]:
                return False
        elif op == "DEGREE":
            vertex = fields[1]
            expected_neighbors = ", ".join(sorted(neighbors[vertex])) or "none"
            if fields[2:] != [expected_neighbors, str(degrees[vertex])]:
                return False
        elif op == "DEGREE_SEQUENCE":
            if fields[1] != ", ".join(str(value) for value in sequence):
                return False
        elif op == "MATRIX_ROW":
            row_index = int(fields[1].split()[1]) - 1
            expected = ", ".join(str(value) for value in matrix[row_index])
            if fields[2] != expected:
                return False
        elif op == "WALK_TERM":
            mid = int(fields[1].split()[1])
            start = parts["start"]
            end = parts["end"]
            expected_label = f"A[{start},{mid}]*A[{mid},{end}]"
            if fields[2] != expected_label:
                return False
            product = matrix[start - 1][mid - 1] * matrix[mid - 1][end - 1]
            if int(fields[3]) != product:
                return False
        elif op == "WALK_ENTRY":
            if fields[1] != f"A^2[{parts['start']},{parts['end']}]":
                return False
            if int(fields[2]) != walk_count(parts):
                return False
        elif op == "CHECK":
            if parts["variant"] == "degree_sequence":
                if fields[1] != "sum degrees = 2m":
                    return False
                if fields[2] != f"{degree_sum} = {2 * edge_count}":
                    return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return True


class TestGraphCountingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GraphCountingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("degree_sequence", "walk_count"):
            gen = GraphCountingGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"graph_counting_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GraphCountingGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
