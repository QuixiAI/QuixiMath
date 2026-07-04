import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


VARIANTS = ["cosine_distance_matrix", "analogy_arithmetic"]
LABELS = ["A", "B", "C"]
BASE_VECTORS = [
    (3, 4), (4, 3), (5, 12), (12, 5), (8, 15), (7, 24),
    (4, -3), (12, -5), (-3, 4), (-5, 12),
]


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


def norm(vector):
    return math.isqrt(vector[0] * vector[0] + vector[1] * vector[1])


def squared_distance(left, right):
    dx = left[0] - right[0]
    dy = left[1] - right[1]
    return dx * dx + dy * dy


class EmbeddingSimilarityGenerator(ProblemGenerator):
    """
    Embedding cosine similarities, distance matrices, and analogy arithmetic.

    Variants:
    - cosine_distance_matrix: compute cosine similarities and squared distances
      for three 2D embeddings.
    - analogy_arithmetic: compute king - man + woman and choose the nearest
      candidate by squared distance.

    Op-codes used:
    - EMBED_SETUP / VECTOR_NORM / DOT / COSINE / DIST2
    - ANALOGY_SETUP / ANALOGY_VECTOR / NEAREST
    - CHECK (established): compare candidate distances
    - S / E / A / M / D (established/shared): exact dot products, distances,
      cosines, and analogy vector arithmetic
    - Z: matrices or analogy target and nearest candidate
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "cosine_distance_matrix":
            problem, steps, answer = self._generate_cosine_distance()
        else:
            problem, steps, answer = self._generate_analogy()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"embedding_similarity_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_cosine_distance(self):
        vectors = random.sample(BASE_VECTORS, 3)
        norms = [norm(vector) for vector in vectors]
        steps = [
            step("EMBED_SETUP", embeddings_text(LABELS, vectors)),
        ]
        for label, vector, value in zip(LABELS, vectors, norms):
            x2 = vector[0] ** 2
            y2 = vector[1] ** 2
            square_sum = x2 + y2
            steps.extend([
                step("E", vector[0], 2, x2),
                step("E", vector[1], 2, y2),
                step("A", x2, y2, square_sum),
                step("ROOT", f"sqrt({square_sum})", value),
                step("VECTOR_NORM", label, value),
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
                pair = f"{LABELS[row]},{LABELS[col]}"
                steps.extend([
                    step("M", left[0], right[0], dot_x),
                    step("M", left[1], right[1], dot_y),
                    step("A", dot_x, dot_y, dot),
                    step("DOT", pair, dot),
                    step("M", norms[row], norms[col], denom),
                    step("D", dot, denom, fraction_text(cos_value)),
                    step("COSINE", pair, fraction_text(cos_value)),
                    step("S", left[0], right[0], dx),
                    step("E", dx, 2, dx2),
                    step("S", left[1], right[1], dy),
                    step("E", dy, 2, dy2),
                    step("A", dx2, dy2, dist2),
                    step("DIST2", pair, dist2),
                ])
                cosine_row.append(cos_value)
                distance_row.append(Fraction(dist2))
            cosine.append(cosine_row)
            distances.append(distance_row)

        answer = (
            f"cos={matrix_text(cosine)}; dist2={matrix_text(distances)}"
        )
        problem = (
            f"For embeddings {embeddings_text(LABELS, vectors)}, compute the "
            "cosine similarity matrix and squared Euclidean distance matrix."
        )
        return problem, steps, answer

    def _generate_analogy(self):
        man = (random.randint(-4, 4), random.randint(-4, 4))
        gender = random.choice([(0, 2), (0, -2), (2, 0), (-2, 0)])
        royalty = random.choice([(3, 0), (-3, 0), (0, 3), (0, -3)])
        woman = (man[0] + gender[0], man[1] + gender[1])
        king = (man[0] + royalty[0], man[1] + royalty[1])
        queen = (woman[0] + royalty[0], woman[1] + royalty[1])
        candidates = {
            "queen": queen,
            "prince": (king[0] - gender[0], king[1] - gender[1]),
            "duchess": (queen[0] + 1, queen[1] + 2),
        }
        steps = [
            step("ANALOGY_SETUP", f"man={vector_text(man)}",
                 f"woman={vector_text(woman)}", f"king={vector_text(king)}"),
        ]
        diff = []
        target = []
        for coord in range(2):
            delta = king[coord] - man[coord]
            value = delta + woman[coord]
            steps.append(step("S", king[coord], man[coord], delta))
            steps.append(step("A", delta, woman[coord], value))
            diff.append(delta)
            target.append(value)
        target = tuple(target)
        steps.append(step("ANALOGY_VECTOR", "king-man+woman",
                          vector_text(target)))

        distances = {}
        for name, vector in candidates.items():
            dx = target[0] - vector[0]
            dy = target[1] - vector[1]
            dx2 = dx ** 2
            dy2 = dy ** 2
            dist2 = dx2 + dy2
            steps.extend([
                step("S", target[0], vector[0], dx),
                step("E", dx, 2, dx2),
                step("S", target[1], vector[1], dy),
                step("E", dy, 2, dy2),
                step("A", dx2, dy2, dist2),
                step("DIST2", name, dist2),
            ])
            distances[name] = dist2
        nearest = min(distances, key=lambda name: (distances[name], name))
        ordered = ",".join(
            f"{name}:{distances[name]}" for name in sorted(distances)
        )
        steps.extend([
            step("CHECK", "nearest distance", ordered, f"nearest={nearest}"),
            step("NEAREST", nearest, vector_text(candidates[nearest])),
        ])
        answer = f"target={vector_text(target)}; nearest={nearest}"
        candidate_text = ", ".join(
            f"{name}={vector_text(vector)}" for name, vector in candidates.items()
        )
        problem = (
            f"Given embeddings man={vector_text(man)}, woman={vector_text(woman)}, "
            f"king={vector_text(king)}, and candidates {candidate_text}, compute "
            "king - man + woman and choose the nearest candidate by squared "
            "distance."
        )
        return problem, steps, answer
