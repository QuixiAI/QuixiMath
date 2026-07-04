import random
from base_generator import ProblemGenerator
from helpers import step, jid


class MidpointGenerator(ProblemGenerator):
    """
    Midpoint of a segment, both directions:
    - midpoint: average the coordinates (parities matched so the
      midpoint is a lattice point)
    - endpoint: given one endpoint and the midpoint, double back to
      the missing endpoint

    Op-codes used:
    - MID_FORMULA: M = ((x1 + x2)/2, (y1 + y2)/2)
    - A / S / M / D: coordinate arithmetic (established)
    - Z: '(x, y)'
    """

    VARIANTS = ["midpoint", "endpoint"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        mx, my = random.randint(-8, 8), random.randint(-8, 8)
        dx = random.choice([v for v in range(-7, 8) if v != 0])
        dy = random.choice([v for v in range(-7, 8) if v != 0])
        x1, y1 = mx - dx, my - dy
        x2, y2 = mx + dx, my + dy

        if variant == "midpoint":
            steps = [
                step("MID_FORMULA", "M = ((x1 + x2)/2, (y1 + y2)/2)"),
                step("A", x1, x2, x1 + x2),
                step("D", x1 + x2, 2, mx),
                step("A", y1, y2, y1 + y2),
                step("D", y1 + y2, 2, my),
            ]
            answer = f"({mx}, {my})"
            problem = (f"Find the midpoint of the segment from "
                       f"({x1}, {y1}) to ({x2}, {y2}).")
        else:
            steps = [
                step("MID_FORMULA", "M = ((x1 + x2)/2, (y1 + y2)/2)"),
                step("REWRITE", "x2 = 2·mx - x1; y2 = 2·my - y1"),
                step("M", 2, mx, 2 * mx),
                step("S", 2 * mx, x1, x2),
                step("M", 2, my, 2 * my),
                step("S", 2 * my, y1, y2),
            ]
            answer = f"({x2}, {y2})"
            problem = (f"The midpoint of a segment is ({mx}, {my}) and "
                       f"one endpoint is ({x1}, {y1}). Find the other "
                       f"endpoint.")
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"midpoint_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
