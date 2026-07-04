import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SegmentPartitionGenerator(ProblemGenerator):
    """
    Partition a segment in a given ratio m:n from the first endpoint:
    P = A + (m/(m+n))·(B - A), each coordinate worked as difference,
    scaled fraction, then shift. Differences are divisible by m + n by
    construction, so every step stays in integers.

    Op-codes used:
    - SECTION_SETUP: endpoints, ratio, and direction (given, goal)
    - SECTION_FORMULA: the section formula (established *_FORMULA shape)
    - A / S / M / D: the coordinate arithmetic (established)
    - Z: '(x, y)'
    """

    def generate(self) -> dict:
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        total = m + n
        x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
        tx = random.choice([v for v in range(-4, 5) if v != 0])
        ty = random.choice([v for v in range(-4, 5) if v != 0])
        x2, y2 = x1 + total * tx, y1 + total * ty
        px, py = x1 + m * tx, y1 + m * ty

        steps = [
            step("SECTION_SETUP",
                 f"A({x1}, {y1}), B({x2}, {y2}); ratio {m}:{n} from A",
                 "point P"),
            step("SECTION_FORMULA",
                 "P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))"),
            step("A", m, n, total),
            step("S", x2, x1, total * tx),
            step("M", m, total * tx, m * total * tx),
            step("D", m * total * tx, total, m * tx),
            step("A", x1, m * tx, px),
            step("S", y2, y1, total * ty),
            step("M", m, total * ty, m * total * ty),
            step("D", m * total * ty, total, m * ty),
            step("A", y1, m * ty, py),
            step("Z", f"({px}, {py})"),
        ]

        return dict(
            problem_id=jid(),
            operation="segment_partition",
            problem=(f"Point P divides the segment from A({x1}, {y1}) "
                     f"to B({x2}, {y2}) in the ratio {m}:{n} "
                     f"(measured from A). Find P."),
            steps=steps,
            final_answer=f"({px}, {py})",
        )
