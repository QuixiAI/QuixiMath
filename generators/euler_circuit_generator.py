import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B", "C", "D", "E", "F"]


def edge_key(u, v):
    return tuple(sorted((u, v)))


def edge_name(edge):
    return "".join(edge)


def edge_list_text(edges):
    return ", ".join(edge_name(edge) for edge in edges)


def comma_text(values):
    return ", ".join(values) if values else "none"


def path_text(values):
    return "-".join(values) if values else "empty"


def adjacency_lists(vertices, edges):
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    for vertex in vertices:
        adjacency[vertex].sort()
    return adjacency


def degree_map(vertices, edges):
    adjacency = adjacency_lists(vertices, edges)
    return {vertex: len(adjacency[vertex]) for vertex in vertices}


def odd_vertices(vertices, edges):
    degrees = degree_map(vertices, edges)
    return [vertex for vertex in vertices if degrees[vertex] % 2 == 1]


def is_connected(vertices, edges):
    adjacency = adjacency_lists(vertices, edges)
    stack = [vertices[0]]
    seen = {vertices[0]}
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(vertices)


def fallback_graph(variant):
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    if variant == "circuit":
        edges = {
            edge_key(vertices[i], vertices[(i + 1) % n])
            for i in range(n)
        }
    else:
        edges = {
            edge_key(vertices[i], vertices[i + 1])
            for i in range(n - 1)
        }
    if n >= 5 and random.random() < 0.7:
        triangle = [
            edge_key(vertices[0], vertices[2]),
            edge_key(vertices[2], vertices[4]),
            edge_key(vertices[0], vertices[4]),
        ]
        if all(edge not in edges for edge in triangle):
            edges.update(triangle)
    return vertices, sorted(edges)


def random_euler_graph(variant):
    for _ in range(500):
        n = random.randint(4, 6)
        vertices = LABELS[:n]
        possible = [
            (vertices[i], vertices[j])
            for i in range(n)
            for j in range(i + 1, n)
        ]
        min_edges = n if variant == "circuit" else n - 1
        max_edges = min(len(possible), n + 5)
        edge_count = random.randint(min_edges, max_edges)
        edges = sorted(random.sample(possible, edge_count))
        if not is_connected(vertices, edges):
            continue
        odds = odd_vertices(vertices, edges)
        if variant == "circuit" and len(odds) == 0:
            return vertices, edges
        if variant == "path" and len(odds) == 2:
            return vertices, edges
    return fallback_graph(variant)


def available_neighbors(current, remaining_edges):
    choices = []
    for u, v in remaining_edges:
        if u == current:
            choices.append(v)
        elif v == current:
            choices.append(u)
    return sorted(choices)


def hierholzer_route(start, edges):
    remaining = set(edges)
    stack = [start]
    route_suffix = []
    trace = [("stack", "initial", list(stack))]

    while stack:
        current = stack[-1]
        choices = available_neighbors(current, remaining)
        if choices:
            neighbor = choices[0]
            edge = edge_key(current, neighbor)
            old_remaining = len(remaining)
            remaining.remove(edge)
            stack.append(neighbor)
            trace.append(("traverse", current, neighbor, edge,
                          old_remaining, len(remaining), list(stack)))
        else:
            popped = stack.pop()
            route_suffix.append(popped)
            trace.append(("backtrack", popped, list(route_suffix),
                          list(stack)))
    return list(reversed(route_suffix)), trace


class EulerCircuitGenerator(ProblemGenerator):
    """
    Euler path and circuit construction with degree-parity checks.

    Variants:
    - circuit: connected graph with zero odd-degree vertices
    - path: connected graph with exactly two odd-degree vertices

    Op-codes used:
    - GRAPH_SETUP / EDGE_LIST / ADJ_LIST: graph setup
    - DEGREE / ODD_VERTICES / CHECK: Euler existence criterion
    - EULER_START / EULER_STACK / EULER_TRAVERSE / EULER_BACKTRACK /
      EULER_ROUTE: Hierholzer construction trace
    - EDGE_COUNT / S (established): unused-edge count arithmetic
    - Z: final Euler trail
    """

    VARIANTS = ["circuit", "path"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        vertices, edges = random_euler_graph(variant)
        adjacency = adjacency_lists(vertices, edges)
        degrees = {vertex: len(adjacency[vertex]) for vertex in vertices}
        odds = [vertex for vertex in vertices if degrees[vertex] % 2 == 1]

        if variant == "circuit":
            start = vertices[0]
            target = "Euler circuit"
            start_reason = "alphabetically first vertex"
            parity_text = "0 odd vertices -> Euler circuit"
        else:
            start = sorted(odds)[0]
            target = "Euler path"
            start_reason = "alphabetically first odd vertex"
            parity_text = "2 odd vertices -> Euler path"

        route, trace = hierholzer_route(start, edges)
        steps = [
            step("GRAPH_SETUP", "connected undirected graph",
                 f"vertices {comma_text(vertices)}"),
            step("EDGE_LIST", edge_list_text(edges)),
            step("CHECK", "connected", "yes"),
            step("EDGE_COUNT", "unused", len(edges)),
        ]
        for vertex in vertices:
            steps.append(step("ADJ_LIST", vertex, comma_text(adjacency[vertex])))
            steps.append(step("DEGREE", vertex, degrees[vertex]))
        steps.extend([
            step("ODD_VERTICES", comma_text(odds), len(odds)),
            step("CHECK", "degree parity", parity_text),
            step("EULER_START", start, start_reason),
        ])

        for item in trace:
            if item[0] == "stack":
                _, label, stack = item
                steps.append(step("EULER_STACK", label, path_text(stack)))
            elif item[0] == "traverse":
                _, current, neighbor, edge, old_remaining, new_remaining, stack = item
                steps.append(step("EULER_TRAVERSE", f"{current}->{neighbor}",
                                  edge_name(edge), f"stack {path_text(stack)}"))
                steps.append(step("S", old_remaining, 1, new_remaining))
            else:
                _, popped, route_suffix, stack = item
                steps.append(step("EULER_BACKTRACK", popped,
                                  f"route suffix {path_text(route_suffix)}",
                                  f"stack {path_text(stack)}"))

        route_string = path_text(route)
        steps.append(step("EULER_ROUTE", route_string, f"uses {len(edges)} edges"))
        answer = f"{target} = {route_string}"
        problem = (
            f"Use Hierholzer's algorithm to find an {target} in the connected "
            f"undirected graph with vertices {comma_text(vertices)} and edges "
            f"{edge_list_text(edges)}. Start at {start}; when extending the "
            f"current walk, choose the alphabetically first unused neighbor."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"euler_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
