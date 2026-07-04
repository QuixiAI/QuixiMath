import random

from base_generator import ProblemGenerator
from helpers import step, jid


TRIPLES = [
    (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
    (20, 21, 29), (9, 40, 41), (12, 35, 37),
]


def vector_text(values):
    return "[" + ",".join(str(value) for value in values) + "]"


class FourVectorGenerator(ProblemGenerator):
    """
    Four-vector arithmetic with signature (+,-,-,-).

    Variants:
    - dot_product: p.q = p0 q0 - p1 q1 - p2 q2 - p3 q3.
    - mass_shell: E^2 = p^2 + m^2 in c=1 units.

    Op-codes used:
    - FOUR_VECTOR_SETUP / ROOT
    - M / A / S / E (established/shared): exact arithmetic
    - Z: dot product or energy
    """

    VARIANTS = ["dot_product", "mass_shell"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "dot_product":
            problem, steps, answer = self._generate_dot_product()
        else:
            problem, steps, answer = self._generate_mass_shell()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"four_vector_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_dot_product(self):
        p = [random.randint(-8, 8) for _ in range(4)]
        q = [random.randint(-8, 8) for _ in range(4)]
        time_part = p[0] * q[0]
        spatial = [p[i] * q[i] for i in range(1, 4)]
        spatial_sum = spatial[0] + spatial[1]
        spatial_total = spatial_sum + spatial[2]
        dot = time_part - spatial_total
        steps = [
            step("FOUR_VECTOR_SETUP", "signature=+---",
                 f"p={vector_text(p)}", f"q={vector_text(q)}"),
            step("M", p[0], q[0], time_part),
        ]
        for i in range(1, 4):
            steps.append(step("M", p[i], q[i], spatial[i - 1]))
        steps.extend([
            step("A", spatial[0], spatial[1], spatial_sum),
            step("A", spatial_sum, spatial[2], spatial_total),
            step("S", time_part, spatial_total, dot),
        ])
        answer = f"p.q = {dot}"
        problem = (
            f"Using signature (+---), compute the Minkowski dot product "
            f"p.q for p={vector_text(p)} and q={vector_text(q)}."
        )
        return problem, steps, answer

    def _generate_mass_shell(self):
        momentum, mass, energy = random.choice(TRIPLES)
        if random.choice([True, False]):
            momentum, mass = mass, momentum
        p_sq = momentum ** 2
        m_sq = mass ** 2
        e_sq = p_sq + m_sq
        steps = [
            step("FOUR_VECTOR_SETUP", "mass_shell", "c=1",
                 f"p={momentum}, m={mass}"),
            step("E", momentum, 2, p_sq),
            step("E", mass, 2, m_sq),
            step("A", p_sq, m_sq, e_sq),
            step("ROOT", f"sqrt({e_sq})", energy),
        ]
        answer = f"E = {energy}"
        problem = (
            f"In units c=1, solve E^2 = p^2 + m^2 for momentum "
            f"p={momentum} and mass m={mass}."
        )
        return problem, steps, answer
