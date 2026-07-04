import itertools
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mst_generator import MSTGenerator
from helpers import DELIM


KRUSKAL_RE = re.compile(
    r"Find a minimum spanning tree for the weighted undirected graph with "
    r"vertices ([A-Z](?:, [A-Z])*) and edges "
    r"([A-Z]{2}=\d+(?:, [A-Z]{2}=\d+)*) using Kruskal's algorithm\."
)
PRIM_RE = re.compile(
    r"Find a minimum spanning tree for the weighted undirected graph with "
    r"vertices ([A-Z](?:, [A-Z])*) and edges "
    r"([A-Z]{2}=\d+(?:, [A-Z]{2}=\d+)*) using Prim's algorithm starting "
    r"at ([A-Z])\."
)


class DSU:
    def __init__(self, vertices):
        self.parent = {vertex: vertex for vertex in vertices}

    def find(self, vertex):
        while self.parent[vertex] != vertex:
            vertex = self.parent[vertex]
        return vertex

    def union(self, left, right):
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return False
        if root_left > root_right:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        return True


def edge_name(edge):
    return "".join(edge)


def parse_edges(text):
    edges = {}
    for item in text.split(", "):
        name, weight = item.split("=")
        edges[tuple(name)] = int(weight)
    return edges


def parse_problem(problem):
    match = KRUSKAL_RE.fullmatch(problem)
    if match:
        vertices = match.group(1).split(", ")
        return {"variant": "kruskal", "vertices": vertices,
                "edges": parse_edges(match.group(2)), "start": None}
    match = PRIM_RE.fullmatch(problem)
    assert match is not None, problem
    vertices = match.group(1).split(", ")
    return {"variant": "prim", "vertices": vertices,
            "edges": parse_edges(match.group(2)), "start": match.group(3)}


def is_tree(vertices, edges):
    dsu = DSU(vertices)
    for u, v in edges:
        if not dsu.union(u, v):
            return False
    root = dsu.find(vertices[0])
    return all(dsu.find(vertex) == root for vertex in vertices)


def oracle_mst(parts):
    vertices = parts["vertices"]
    edge_items = sorted(parts["edges"].items())
    best = None
    for combo in itertools.combinations(edge_items, len(vertices) - 1):
        edges = [edge for edge, _ in combo]
        if not is_tree(vertices, edges):
            continue
        weight = sum(weight for _, weight in combo)
        edge_names = tuple(edge_name(edge) for edge in sorted(edges))
        score = (weight, edge_names)
        if best is None or score < best[0]:
            best = (score, edges)
    assert best is not None
    return best[1], best[0][0]


def oracle_answer(example):
    edges, weight = oracle_mst(parse_problem(example["problem"]))
    return (
        f"MST weight = {weight}; edges = "
        + ", ".join(edge_name(edge) for edge in sorted(edges))
    )


def adjacency(parts):
    adj = {vertex: {} for vertex in parts["vertices"]}
    for (u, v), weight in parts["edges"].items():
        adj[u][v] = weight
        adj[v][u] = weight
    return adj


def check_trace(example):
    parts = parse_problem(example["problem"])
    vertices = parts["vertices"]
    weights = parts["edges"]
    accepted = []
    total = 0
    pending_edge = None
    pending_weight = None
    pending_total = None

    if parts["variant"] == "kruskal":
        dsu = DSU(vertices)
    else:
        visited = set()
        adj = adjacency(parts)

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "EDGE_WEIGHT":
            edge = tuple(fields[1])
            if weights[edge] != int(fields[2]):
                return False
        elif op == "SORT_EDGES":
            expected = ", ".join(
                f"{edge_name(edge)}={weight}"
                for edge, weight in sorted(weights.items(),
                                           key=lambda item: (item[1], item[0]))
            )
            if fields[1] != expected:
                return False
        elif op == "EDGE_CONSIDER":
            pending_edge = tuple(fields[1])
            pending_weight = weights[pending_edge]
            if fields[2] != f"weight {pending_weight}":
                return False
        elif op == "CYCLE_REJECT":
            edge = tuple(fields[1])
            if edge != pending_edge or dsu.find(edge[0]) != dsu.find(edge[1]):
                return False
        elif op == "PRIM_START":
            visited = {fields[1]}
            if fields[1] != parts["start"]:
                return False
        elif op == "PRIM_CANDIDATES":
            expected_visited = ", ".join(
                vertex for vertex in vertices if vertex in visited
            )
            if fields[1] != f"visited {expected_visited}":
                return False
            candidates = []
            for u in [vertex for vertex in vertices if vertex in visited]:
                for v, weight in adj[u].items():
                    if v not in visited:
                        candidates.append((weight, tuple(sorted((u, v)))))
            candidates.sort(key=lambda item: (item[0], item[1]))
            expected = ", ".join(
                f"{edge_name(edge)}={weight}" for weight, edge in candidates
            )
            if fields[2] != expected:
                return False
        elif op == "EDGE_CHOOSE":
            pending_edge = tuple(fields[1])
            pending_weight = weights[pending_edge]
            if fields[2] != f"weight {pending_weight}":
                return False
            u, v = pending_edge
            new_vertex = v if u in visited else u
            if fields[3] != f"add {new_vertex}":
                return False
        elif op == "A":
            left, right, value = map(int, fields[1:])
            if left + right != value:
                return False
            if left != total or right != pending_weight:
                return False
            pending_total = value
        elif op == "MST_ADD":
            edge = tuple(fields[1])
            if edge != pending_edge or fields[2] != f"total {pending_total}":
                return False
            if parts["variant"] == "kruskal":
                if not dsu.union(edge[0], edge[1]):
                    return False
            else:
                u, v = edge
                new_vertex = v if u in visited else u
                visited.add(new_vertex)
            accepted.append(edge)
            total = pending_total
        elif op == "MST_SET":
            expected = ", ".join(edge_name(edge) for edge in sorted(accepted))
            if fields[1] != expected:
                return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return True


class TestMSTGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MSTGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_trace_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(check_trace(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("kruskal", "prim"):
            gen = MSTGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["operation"], f"mst_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MSTGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
