import random
from base_generator import ProblemGenerator
from helpers import step, jid


class EulerCharacteristicGenerator(ProblemGenerator):
    """
    Euler characteristic V - E + F: compute it for named polyhedra
    (sphere-family solids give 2), recover a missing count from
    V - E + F = 2, and see the torus break the rule with 0.

    Op-codes used:
    - EULER_SETUP: the solid and its counts (solid, goal)
    - EULER_FORMULA: χ = V - E + F (established *_FORMULA shape)
    - S / A: the arithmetic, left to right (established)
    - EULER_NOTE: what the value says about the surface (value, meaning)
    - Z: final answer
    """

    SOLIDS = {
        "tetrahedron": (4, 6, 4),
        "cube": (8, 12, 6),
        "octahedron": (6, 12, 8),
        "dodecahedron": (20, 30, 12),
        "icosahedron": (12, 30, 20),
        "square pyramid": (5, 8, 5),
        "pentagonal pyramid": (6, 10, 6),
        "triangular prism": (6, 9, 5),
        "pentagonal prism": (10, 15, 7),
        "hexagonal prism": (12, 18, 8),
    }

    VARIANTS = ["compute", "find_missing", "torus"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "compute":
            name, (V, E, F) = random.choice(list(self.SOLIDS.items()))
            steps = [
                step("EULER_SETUP",
                     f"{name}: V = {V}, E = {E}, F = {F}", "V - E + F"),
                step("EULER_FORMULA", "χ = V - E + F"),
                step("S", V, E, V - E),
                step("A", V - E, F, 2),
                step("EULER_NOTE", 2,
                     "sphere-family polyhedron: χ is always 2"),
                step("Z", 2),
            ]
            problem = (f"A {name} has {V} vertices, {E} edges, and {F} "
                       f"faces. Compute V - E + F.")
            answer = "2"
        elif variant == "find_missing":
            name, (V, E, F) = random.choice(list(self.SOLIDS.items()))
            missing = random.choice(["V", "E", "F"])
            steps = [step("EULER_FORMULA", "V - E + F = 2")]
            if missing == "E":
                steps.insert(0, step("EULER_SETUP",
                                     f"convex polyhedron: V = {V}, "
                                     f"F = {F}", "E"))
                steps.append(step("A", V, F, V + F))
                steps.append(step("S", V + F, 2, E))
                answer = f"E = {E}"
                problem = (f"A convex polyhedron has {V} vertices and "
                           f"{F} faces. How many edges does it have?")
            elif missing == "V":
                steps.insert(0, step("EULER_SETUP",
                                     f"convex polyhedron: E = {E}, "
                                     f"F = {F}", "V"))
                steps.append(step("A", 2, E, 2 + E))
                steps.append(step("S", 2 + E, F, V))
                answer = f"V = {V}"
                problem = (f"A convex polyhedron has {E} edges and {F} "
                           f"faces. How many vertices does it have?")
            else:
                steps.insert(0, step("EULER_SETUP",
                                     f"convex polyhedron: V = {V}, "
                                     f"E = {E}", "F"))
                steps.append(step("A", 2, E, 2 + E))
                steps.append(step("S", 2 + E, V, F))
                answer = f"F = {F}"
                problem = (f"A convex polyhedron has {V} vertices and "
                           f"{E} edges. How many faces does it have?")
        else:
            nm = random.choice([9, 12, 16, 20, 25, 30, 36])
            V, E, F = nm, 2 * nm, nm
            steps = [
                step("EULER_SETUP",
                     f"polyhedral torus grid: V = {V}, E = {E}, "
                     f"F = {F}", "V - E + F"),
                step("EULER_FORMULA", "χ = V - E + F"),
                step("S", V, E, V - E),
                step("A", V - E, F, 0),
                step("EULER_NOTE", 0,
                     "the torus has a hole: χ = 0, not 2"),
                step("Z", 0),
            ]
            problem = (f"A doughnut-shaped (torus) surface is divided "
                       f"into a grid with {V} vertices, {E} edges, and "
                       f"{F} faces. Compute V - E + F.")
            answer = "0"
        if variant == "find_missing":
            steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"euler_characteristic_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
