import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.euler_circuit_generator import EulerCircuitGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Hierholzer's algorithm to find an Euler (circuit|path) in the "
    r"connected undirected graph with vertices ([A-Z](?:, [A-Z])*) and edges "
    r"([A-Z]{2}(?:, [A-Z]{2})*)\. Start at ([A-Z]); when extending the "
    r"current walk, choose the alphabetically first unused neighbor\."
)


def edge_key(u, v):
    return tuple(sorted((u, v)))


def edge_name(edge):
    return "".join(edge)


def comma_text(values):
    return ", ".join(values) if values else "none"


def path_text(values):
    return "-".join(values) if values else "empty"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    variant, vertices_text, edges_text, start = match.groups()
    vertices = vertices_text.split(", ")
    edges = sorted(tuple(edge) for edge in edges_text.split(", "))
    return {"variant": variant, "vertices": vertices, "edges": edges,
            "start": start}


def adjacency_lists(vertices, edges):
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    for vertex in vertices:
        adjacency[vertex].sort()
    return adjacency


def degrees(parts):
    adjacency = adjacency_lists(parts["vertices"], parts["edges"])
    return {vertex: len(adjacency[vertex]) for vertex in parts["vertices"]}


def odd_vertices(parts):
    degree_values = degrees(parts)
    return [
        vertex for vertex in parts["vertices"]
        if degree_values[vertex] % 2 == 1
    ]


def is_connected(parts):
    adjacency = adjacency_lists(parts["vertices"], parts["edges"])
    stack = [parts["vertices"][0]]
    seen = {parts["vertices"][0]}
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(parts["vertices"])


def available_neighbors(current, remaining_edges):
    choices = []
    for u, v in remaining_edges:
        if u == current:
            choices.append(v)
        elif v == current:
            choices.append(u)
    return sorted(choices)


def hierholzer_route(parts):
    remaining = set(parts["edges"])
    stack = [parts["start"]]
    route_suffix = []
    while stack:
        current = stack[-1]
        choices = available_neighbors(current, remaining)
        if choices:
            neighbor = choices[0]
            remaining.remove(edge_key(current, neighbor))
            stack.append(neighbor)
        else:
            route_suffix.append(stack.pop())
    return list(reversed(route_suffix))


def trail_edges(route):
    return [edge_key(route[i], route[i + 1]) for i in range(len(route) - 1)]


def oracle_answer(example):
    parts = parse_problem(example["problem"])
    route = hierholzer_route(parts)
    return f"Euler {parts['variant']} = {path_text(route)}"


def check_steps(example):
    parts = parse_problem(example["problem"])
    adjacency = adjacency_lists(parts["vertices"], parts["edges"])
    degree_values = degrees(parts)
    odds = odd_vertices(parts)
    remaining = set(parts["edges"])
    stack = []
    route_suffix = []
    last_traverse = None

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "EDGE_LIST":
            if fields[1] != ", ".join(edge_name(edge) for edge in parts["edges"]):
                return False
        elif op == "CHECK":
            if fields[1:] == ["connected", "yes"]:
                if not is_connected(parts):
                    return False
            elif fields[1] == "degree parity":
                if parts["variant"] == "circuit":
                    if fields[2] != "0 odd vertices -> Euler circuit":
                        return False
                    if odds:
                        return False
                else:
                    if fields[2] != "2 odd vertices -> Euler path":
                        return False
                    if len(odds) != 2:
                        return False
        elif op == "ADJ_LIST":
            vertex = fields[1]
            if fields[2] != comma_text(adjacency[vertex]):
                return False
        elif op == "DEGREE":
            if int(fields[2]) != degree_values[fields[1]]:
                return False
        elif op == "ODD_VERTICES":
            if fields[1:] != [comma_text(odds), str(len(odds))]:
                return False
        elif op == "EULER_START":
            if fields[1] != parts["start"]:
                return False
            if parts["variant"] == "circuit":
                if fields[2] != "alphabetically first vertex":
                    return False
            elif fields[2] != "alphabetically first odd vertex":
                return False
        elif op == "EULER_STACK":
            if fields[1:] != ["initial", path_text([parts["start"]])]:
                return False
            stack = [parts["start"]]
        elif op == "EULER_TRAVERSE":
            current, neighbor = fields[1].split("->")
            if not stack or stack[-1] != current:
                return False
            choices = available_neighbors(current, remaining)
            if not choices or neighbor != choices[0]:
                return False
            edge = edge_key(current, neighbor)
            if fields[2] != edge_name(edge) or edge not in remaining:
                return False
            remaining.remove(edge)
            stack.append(neighbor)
            if fields[3] != f"stack {path_text(stack)}":
                return False
            last_traverse = (len(remaining) + 1, len(remaining))
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
            if last_traverse is None:
                return False
            if (int(fields[1]), int(fields[3])) != last_traverse:
                return False
            last_traverse = None
        elif op == "EULER_BACKTRACK":
            if not stack or fields[1] != stack[-1]:
                return False
            if available_neighbors(stack[-1], remaining):
                return False
            popped = stack.pop()
            route_suffix.append(popped)
            expected = [
                popped,
                f"route suffix {path_text(route_suffix)}",
                f"stack {path_text(stack)}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "EULER_ROUTE":
            route = hierholzer_route(parts)
            if fields[1:] != [path_text(route), f"uses {len(parts['edges'])} edges"]:
                return False
            if sorted(trail_edges(route)) != sorted(parts["edges"]):
                return False
            if parts["variant"] == "circuit" and route[0] != route[-1]:
                return False
            if parts["variant"] == "path":
                if route[0] == route[-1]:
                    return False
                if set((route[0], route[-1])) != set(odds):
                    return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return not remaining and not stack


class TestEulerCircuitGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = EulerCircuitGenerator()

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

    def test_step_content_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_steps(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("circuit", "path"):
            gen = EulerCircuitGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], f"euler_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EulerCircuitGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
