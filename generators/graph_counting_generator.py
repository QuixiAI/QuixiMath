import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B", "C", "D", "E", "F"]


def matrix_text(matrix):
    return "[" + ", ".join(str(row) for row in matrix) + "]"


def edge_text(edges):
    return ", ".join(f"{u}{v}" for u, v in edges)


def random_simple_graph():
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    possible = [(vertices[i], vertices[j])
                for i in range(n) for j in range(i + 1, n)]
    m = random.randint(n - 1, min(len(possible), n + 3))
    edges = sorted(random.sample(possible, m))
    return vertices, edges


def random_adjacency_matrix():
    n = random.randint(3, 4)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                row.append(1 if random.random() < 0.45 else 0)
        matrix.append(row)
    if sum(sum(row) for row in matrix) == 0:
        matrix[0][1] = 1
    return matrix


def length_two_count(matrix, start, end):
    return sum(matrix[start][mid] * matrix[mid][end]
               for mid in range(len(matrix)))


class GraphCountingGenerator(ProblemGenerator):
    """
    Graph counting by degree sums and adjacency-matrix powers.

    Variants:
    - degree_sequence: compute degrees and verify the handshake lemma
    - walk_count: count length-2 directed walks using an A^2 entry

    Op-codes used:
    - GRAPH_SETUP: vertices/edges or matrix context
    - EDGE_COUNT: number of undirected edges
    - DEGREE: one vertex degree
    - DEGREE_SEQUENCE: sorted degree sequence
    - MATRIX_ROW: one row of an adjacency matrix
    - WALK_GOAL / WALK_TERM / WALK_ENTRY: matrix-power walk count
    - A / M / CHECK (established): arithmetic and handshake verification
    - Z: exact count result
    """

    VARIANTS = ["degree_sequence", "walk_count"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "degree_sequence":
            vertices, edges = random_simple_graph()
            edge_count = len(edges)
            neighbors = {vertex: [] for vertex in vertices}
            for u, v in edges:
                neighbors[u].append(v)
                neighbors[v].append(u)
            degrees = {vertex: len(neighbors[vertex]) for vertex in vertices}
            sequence = sorted(degrees.values(), reverse=True)
            steps = [
                step("GRAPH_SETUP", f"vertices {', '.join(vertices)}",
                     f"edges {edge_text(edges)}"),
                step("EDGE_COUNT", "m", edge_count),
            ]
            running = 0
            for vertex in vertices:
                neighbor_text = ", ".join(sorted(neighbors[vertex])) or "none"
                degree = degrees[vertex]
                steps.append(step("DEGREE", vertex, neighbor_text, degree))
                new_running = running + degree
                steps.append(step("A", running, degree, new_running))
                running = new_running
            double_edges = 2 * edge_count
            steps.extend([
                step("M", 2, edge_count, double_edges),
                step("CHECK", "sum degrees = 2m",
                     f"{running} = {double_edges}"),
                step("DEGREE_SEQUENCE", ", ".join(str(v) for v in sequence)),
            ])
            answer = (
                f"degree sequence = [{', '.join(str(v) for v in sequence)}]; "
                f"degree sum = {running}"
            )
            problem = (
                f"In the undirected graph with vertices {', '.join(vertices)} "
                f"and edges {edge_text(edges)}, find the degree sequence and "
                f"verify the handshake count."
            )
        else:
            matrix = random_adjacency_matrix()
            positive_pairs = [
                (i, j)
                for i in range(len(matrix))
                for j in range(len(matrix))
                if length_two_count(matrix, i, j) > 0
            ]
            attempts = 0
            while not positive_pairs and attempts < 10:
                matrix = random_adjacency_matrix()
                positive_pairs = [
                    (i, j)
                    for i in range(len(matrix))
                    for j in range(len(matrix))
                    if length_two_count(matrix, i, j) > 0
                ]
                attempts += 1
            n = len(matrix)
            if positive_pairs and random.random() < 0.8:
                start_idx, end_idx = random.choice(positive_pairs)
                start, end = start_idx + 1, end_idx + 1
            else:
                start = random.randint(1, n)
                end = random.randint(1, n)
            steps = [
                step("GRAPH_SETUP", "directed adjacency matrix",
                     f"{n} vertices"),
            ]
            for idx, row in enumerate(matrix, start=1):
                steps.append(step("MATRIX_ROW", f"row {idx}",
                                  ", ".join(str(v) for v in row)))
            steps.append(step("WALK_GOAL", "length 2",
                              f"{start} to {end}"))
            running = 0
            for mid in range(1, n + 1):
                left = matrix[start - 1][mid - 1]
                right = matrix[mid - 1][end - 1]
                product = left * right
                steps.append(step("M", left, right, product))
                steps.append(step("WALK_TERM", f"via {mid}",
                                  f"A[{start},{mid}]*A[{mid},{end}]",
                                  product))
                new_running = running + product
                steps.append(step("A", running, product, new_running))
                running = new_running
            steps.append(step("WALK_ENTRY", f"A^2[{start},{end}]", running))
            answer = f"walks = {running}"
            problem = (
                f"For the directed graph with adjacency matrix A = "
                f"{matrix_text(matrix)}, how many walks of length 2 go from "
                f"vertex {start} to vertex {end}?"
            )

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"graph_counting_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
