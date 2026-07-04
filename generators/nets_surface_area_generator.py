import random
from base_generator import ProblemGenerator
from helpers import step, jid


class NetsSurfaceAreaGenerator(ProblemGenerator):
    """
    Surface area from a net described textually as a list of faces.
    Each face's area is computed, pairs are doubled explicitly, and the
    areas are accumulated left to right.

    Variants:
    - cube:       6 squares s by s
    - rect_prism: three pairs of rectangles
    - tri_prism:  2 right-triangle faces (legs 3k, 4k) + 3 rectangles
                  (sides 3k, 4k, 5k by the length)
    - pyramid:    1 square base + 4 identical triangles

    Op-codes used:
    - NET_SETUP: the face list and the goal (faces, goal)
    - M / D / A: face areas, halving for triangles, doubling pairs,
      and the running total (established)
    - Z: 'N square units'
    """

    VARIANTS = ["cube", "rect_prism", "tri_prism", "pyramid"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        steps = []
        areas = []

        if variant == "cube":
            s = random.randint(2, 12)
            faces = f"6 squares {s} by {s}"
            steps.append(step("NET_SETUP", faces, "total surface area"))
            steps.append(step("M", s, s, s * s))
            steps.append(step("M", 6, s * s, 6 * s * s))
            total = 6 * s * s
        elif variant == "rect_prism":
            l, w, h = (random.randint(2, 12) for _ in range(3))
            faces = (f"2 rectangles {l} by {w}; 2 rectangles {l} by {h}; "
                     f"2 rectangles {w} by {h}")
            steps.append(step("NET_SETUP", faces, "total surface area"))
            for a, b in ((l, w), (l, h), (w, h)):
                steps.append(step("M", a, b, a * b))
                steps.append(step("M", 2, a * b, 2 * a * b))
                areas.append(2 * a * b)
            total = self._accumulate(steps, areas)
        elif variant == "tri_prism":
            k = random.randint(1, 4)
            a, b, c = 3 * k, 4 * k, 5 * k
            L = random.randint(3, 12)
            faces = (f"2 right triangles with legs {a} and {b}; "
                     f"rectangles {a} by {L}, {b} by {L}, and {c} by {L}")
            steps.append(step("NET_SETUP", faces, "total surface area"))
            steps.append(step("M", a, b, a * b))
            steps.append(step("D", a * b, 2, a * b // 2))
            steps.append(step("M", 2, a * b // 2, a * b))
            areas.append(a * b)
            for side in (a, b, c):
                steps.append(step("M", side, L, side * L))
                areas.append(side * L)
            total = self._accumulate(steps, areas)
        else:
            s = random.choice([2, 4, 6, 8, 10, 12])
            slant = random.randint(3, 12)
            faces = (f"1 square {s} by {s}; 4 triangles with base {s} "
                     f"and height {slant}")
            steps.append(step("NET_SETUP", faces, "total surface area"))
            steps.append(step("M", s, s, s * s))
            areas.append(s * s)
            steps.append(step("M", s, slant, s * slant))
            steps.append(step("D", s * slant, 2, s * slant // 2))
            steps.append(step("M", 4, s * slant // 2, 2 * s * slant))
            areas.append(2 * s * slant)
            total = self._accumulate(steps, areas)

        answer = f"{total} square units"
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="net_surface_area",
            problem=(f"A net consists of: {faces}. All lengths are in "
                     f"the same unit. Find the total surface area."),
            steps=steps,
            final_answer=answer,
        )

    @staticmethod
    def _accumulate(steps, areas):
        total = areas[0]
        for v in areas[1:]:
            steps.append(step("A", total, v, total + v))
            total += v
        return total
