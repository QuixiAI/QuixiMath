import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.embedding_similarity_generator import EmbeddingSimilarityGenerator
from helpers import DELIM


COS_RE = re.compile(
    r"For embeddings (.+), compute the cosine similarity matrix and squared "
    r"Euclidean distance matrix\."
)
EMBED_RE = re.compile(r"([ABC])=\(([^,]+),([^)]+)\)")
ANALOGY_RE = re.compile(
    r"Given embeddings man=(\([^)]+\)), woman=(\([^)]+\)), "
    r"king=(\([^)]+\)), and candidates (.+), compute king - man \+ woman "
    r"and choose the nearest candidate by squared distance\."
)
CANDIDATE_RE = re.compile(r"(\w+)=(\([^)]+\))")
LABELS = ["A", "B", "C"]


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def vector_text(vector):
    return "(" + ",".join(fraction_text(value) for value in vector) + ")"


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def embeddings_text(labels, vectors):
    return ", ".join(
        f"{label}={vector_text(vector)}"
        for label, vector in zip(labels, vectors)
    )


def parse_vector(raw):
    left, right = raw.strip("()").split(",")
    return (int(left), int(right))


def norm(vector):
    return math.isqrt(vector[0] * vector[0] + vector[1] * vector[1])


def expected_cosine(problem):
    raw = COS_RE.fullmatch(problem).group(1)
    parsed = EMBED_RE.findall(raw)
    labels = [label for label, _, _ in parsed]
    vectors = [(int(x), int(y)) for _, x, y in parsed]
    norms = [norm(vector) for vector in vectors]
    steps = [
        make_step("EMBED_SETUP", embeddings_text(labels, vectors)),
    ]
    for label, vector, value in zip(labels, vectors, norms):
        x2 = vector[0] ** 2
        y2 = vector[1] ** 2
        square_sum = x2 + y2
        steps.extend([
            make_step("E", vector[0], 2, x2),
            make_step("E", vector[1], 2, y2),
            make_step("A", x2, y2, square_sum),
            make_step("ROOT", f"sqrt({square_sum})", value),
            make_step("VECTOR_NORM", label, value),
        ])

    cosine = []
    distances = []
    for row, left in enumerate(vectors):
        cosine_row = []
        distance_row = []
        for col, right in enumerate(vectors):
            dot_x = left[0] * right[0]
            dot_y = left[1] * right[1]
            dot = dot_x + dot_y
            denom = norms[row] * norms[col]
            cos_value = Fraction(dot, denom)
            dx = left[0] - right[0]
            dy = left[1] - right[1]
            dx2 = dx ** 2
            dy2 = dy ** 2
            dist2 = dx2 + dy2
            pair = f"{labels[row]},{labels[col]}"
            steps.extend([
                make_step("M", left[0], right[0], dot_x),
                make_step("M", left[1], right[1], dot_y),
                make_step("A", dot_x, dot_y, dot),
                make_step("DOT", pair, dot),
                make_step("M", norms[row], norms[col], denom),
                make_step("D", dot, denom, fraction_text(cos_value)),
                make_step("COSINE", pair, fraction_text(cos_value)),
                make_step("S", left[0], right[0], dx),
                make_step("E", dx, 2, dx2),
                make_step("S", left[1], right[1], dy),
                make_step("E", dy, 2, dy2),
                make_step("A", dx2, dy2, dist2),
                make_step("DIST2", pair, dist2),
            ])
            cosine_row.append(cos_value)
            distance_row.append(Fraction(dist2))
        cosine.append(cosine_row)
        distances.append(distance_row)
    answer = f"cos={matrix_text(cosine)}; dist2={matrix_text(distances)}"
    return steps, answer


def expected_analogy(problem):
    match = ANALOGY_RE.fullmatch(problem)
    man = parse_vector(match.group(1))
    woman = parse_vector(match.group(2))
    king = parse_vector(match.group(3))
    candidates = {
        name: parse_vector(raw)
        for name, raw in CANDIDATE_RE.findall(match.group(4))
    }
    steps = [
        make_step("ANALOGY_SETUP", f"man={vector_text(man)}",
                  f"woman={vector_text(woman)}", f"king={vector_text(king)}"),
    ]
    target = []
    for coord in range(2):
        delta = king[coord] - man[coord]
        value = delta + woman[coord]
        steps.append(make_step("S", king[coord], man[coord], delta))
        steps.append(make_step("A", delta, woman[coord], value))
        target.append(value)
    target = tuple(target)
    steps.append(make_step("ANALOGY_VECTOR", "king-man+woman",
                           vector_text(target)))

    distances = {}
    for name, vector in candidates.items():
        dx = target[0] - vector[0]
        dy = target[1] - vector[1]
        dx2 = dx ** 2
        dy2 = dy ** 2
        dist2 = dx2 + dy2
        steps.extend([
            make_step("S", target[0], vector[0], dx),
            make_step("E", dx, 2, dx2),
            make_step("S", target[1], vector[1], dy),
            make_step("E", dy, 2, dy2),
            make_step("A", dx2, dy2, dist2),
            make_step("DIST2", name, dist2),
        ])
        distances[name] = dist2
    nearest = min(distances, key=lambda name: (distances[name], name))
    ordered = ",".join(
        f"{name}:{distances[name]}" for name in sorted(distances)
    )
    steps.extend([
        make_step("CHECK", "nearest distance", ordered, f"nearest={nearest}"),
        make_step("NEAREST", nearest, vector_text(candidates[nearest])),
    ])
    answer = f"target={vector_text(target)}; nearest={nearest}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if COS_RE.fullmatch(problem):
        steps, answer = expected_cosine(problem)
    elif ANALOGY_RE.fullmatch(problem):
        steps, answer = expected_analogy(problem)
    else:
        raise AssertionError(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestEmbeddingSimilarityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = EmbeddingSimilarityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_variants_are_available(self):
        for variant in EmbeddingSimilarityGenerator.VARIANTS:
            result = EmbeddingSimilarityGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"embedding_similarity_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            EmbeddingSimilarityGenerator("bogus")

    def test_arithmetic_steps(self):
        for _ in range(200):
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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    radicand = int(fields[1][5:-1])
                    self.assertEqual(math.isqrt(radicand), int(fields[2]),
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
