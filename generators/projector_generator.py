import random

from base_generator import ProblemGenerator
from helpers import step, jid


class ProjectorGenerator(ProblemGenerator):
    """
    Verify projector idempotence and completeness relations.

    Variants:
    - plus_projector: P_plus^2 = P_plus for |+><+|.
    - basis_completeness: P0 + P1 = I for the computational basis.

    Op-codes used:
    - PROJECTOR_SETUP / MATRIX_MULT / MATRIX_ADD / CHECK
    - Z: verification result
    """

    VARIANTS = ["plus_projector", "basis_completeness"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "plus_projector":
            problem, steps, answer = self._generate_plus()
        else:
            problem, steps, answer = self._generate_basis()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"projector_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_plus(self):
        p = "[[1/2,1/2],[1/2,1/2]]"
        steps = [
            step("PROJECTOR_SETUP", "P_plus=ket+bra+",
                 f"P={p}"),
            step("MATRIX_MULT", "row1 dot col1", "1/4+1/4", "1/2"),
            step("MATRIX_MULT", "row1 dot col2", "1/4+1/4", "1/2"),
            step("MATRIX_MULT", "row2 dot col1", "1/4+1/4", "1/2"),
            step("MATRIX_MULT", "row2 dot col2", "1/4+1/4", "1/2"),
            step("CHECK", "P^2", p, "idempotent"),
        ]
        answer = "projector yes; P^2 = P"
        problem = "Verify that P_plus=[[1/2,1/2],[1/2,1/2]] is a projector."
        return problem, steps, answer

    def _generate_basis(self):
        p0 = "[[1,0],[0,0]]"
        p1 = "[[0,0],[0,1]]"
        identity = "[[1,0],[0,1]]"
        steps = [
            step("PROJECTOR_SETUP", f"P0={p0}", f"P1={p1}"),
            step("MATRIX_MULT", "P0^2", p0),
            step("MATRIX_MULT", "P1^2", p1),
            step("MATRIX_ADD", "P0+P1", identity),
            step("CHECK", "sum_i Pi", identity, "complete"),
        ]
        answer = "complete yes; P0 + P1 = I"
        problem = "Verify projector completeness for P0=[[1,0],[0,0]] and P1=[[0,0],[0,1]]."
        return problem, steps, answer
