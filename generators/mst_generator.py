import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B", "C", "D", "E", "F"]


def make_weighted_graph():
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    weights = random.sample(range(1, 25), 2 * n)
    weight_iter = iter(weights)
    edges = {}

    for i in range(1, n):
        u = vertices[i]
        v = random.choice(vertices[:i])
        edges[tuple(sorted((u, v)))] = next(weight_iter)

    possible = [
        (vertices[i], vertices[j])
        for i in range(n)
        for j in range(i + 1, n)
        if (vertices[i], vertices[j]) not in edges
    ]
    for edge in random.sample(possible, random.randint(1, min(n, len(possible)))):
        edges[edge] = next(weight_iter)

    edge_items = sorted(edges.items())
    adjacency = {vertex: {} for vertex in vertices}
    for (u, v), weight in edge_items:
        adjacency[u][v] = weight
        adjacency[v][u] = weight
    return vertices, edge_items, adjacency


def edge_name(edge):
    u, v = edge
    return f"{u}{v}"


def edge_list_text(edge_items):
    return ", ".join(f"{edge_name(edge)}={weight}"
                     for edge, weight in edge_items)


def answer_text(edges, weight):
    edge_text = ", ".join(edge_name(edge) for edge in sorted(edges))
    return f"MST weight = {weight}; edges = {edge_text}"


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


class MSTGenerator(ProblemGenerator):
    """
    Minimum spanning tree traces by Kruskal and Prim.

    Variants:
    - kruskal: sort all edges, accept if no cycle
    - prim: grow a cut from a start vertex

    Op-codes used:
    - MST_SETUP / EDGE_WEIGHT: graph setup
    - SORT_EDGES: Kruskal edge ordering
    - EDGE_CONSIDER / MST_ADD / CYCLE_REJECT: Kruskal decisions
    - PRIM_START / PRIM_CANDIDATES / EDGE_CHOOSE: Prim decisions
    - MST_SET: current accepted edges
    - A (established): running MST weight
    - Z: final MST edge set and weight
    """

    VARIANTS = ["kruskal", "prim"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        vertices, edge_items, adjacency = make_weighted_graph()
        steps = [
            step("MST_SETUP", "weighted undirected graph",
                 f"vertices {', '.join(vertices)}"),
        ]
        for edge, weight in edge_items:
            steps.append(step("EDGE_WEIGHT", edge_name(edge), weight))

        accepted = []
        total = 0
        if variant == "kruskal":
            ordered = sorted(edge_items, key=lambda item: (item[1], item[0]))
            steps.append(step("SORT_EDGES", ", ".join(
                f"{edge_name(edge)}={weight}" for edge, weight in ordered
            )))
            dsu = DSU(vertices)
            for edge, weight in ordered:
                u, v = edge
                steps.append(step("EDGE_CONSIDER", edge_name(edge),
                                  f"weight {weight}"))
                if dsu.union(u, v):
                    accepted.append(edge)
                    new_total = total + weight
                    steps.append(step("A", total, weight, new_total))
                    total = new_total
                    steps.append(step("MST_ADD", edge_name(edge),
                                      f"total {total}"))
                    steps.append(step("MST_SET", ", ".join(
                        edge_name(item) for item in sorted(accepted)
                    )))
                    if len(accepted) == len(vertices) - 1:
                        break
                else:
                    steps.append(step("CYCLE_REJECT", edge_name(edge),
                                      "endpoints already connected"))
            problem = (
                f"Find a minimum spanning tree for the weighted undirected "
                f"graph with vertices {', '.join(vertices)} and edges "
                f"{edge_list_text(edge_items)} using Kruskal's algorithm."
            )
        else:
            start = random.choice(vertices)
            visited = {start}
            steps.append(step("PRIM_START", start))
            while len(visited) < len(vertices):
                candidates = []
                for u in sorted(visited, key=vertices.index):
                    for v, weight in adjacency[u].items():
                        if v not in visited:
                            candidates.append((weight, tuple(sorted((u, v)))))
                candidates.sort(key=lambda item: (item[0], item[1]))
                steps.append(step("PRIM_CANDIDATES",
                                  f"visited {', '.join(sorted(visited, key=vertices.index))}",
                                  ", ".join(
                                      f"{edge_name(edge)}={weight}"
                                      for weight, edge in candidates
                                  )))
                weight, edge = candidates[0]
                u, v = edge
                new_vertex = v if u in visited else u
                steps.append(step("EDGE_CHOOSE", edge_name(edge),
                                  f"weight {weight}",
                                  f"add {new_vertex}"))
                accepted.append(edge)
                visited.add(new_vertex)
                new_total = total + weight
                steps.append(step("A", total, weight, new_total))
                total = new_total
                steps.append(step("MST_ADD", edge_name(edge),
                                  f"total {total}"))
                steps.append(step("MST_SET", ", ".join(
                    edge_name(item) for item in sorted(accepted)
                )))
            problem = (
                f"Find a minimum spanning tree for the weighted undirected "
                f"graph with vertices {', '.join(vertices)} and edges "
                f"{edge_list_text(edge_items)} using Prim's algorithm starting "
                f"at {start}."
            )

        answer = answer_text(accepted, total)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"mst_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
