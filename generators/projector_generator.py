import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid

# Pythagorean (a, b, c) triples give exact unit vectors (a/c, b/c)
TRIPLES = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13),
           (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25),
           (20, 21, 29), (21, 20, 29)]


class ProjectorGenerator(ProblemGenerator):
    """
    Verify projector idempotence and completeness relations.

    Variants:
    - plus_projector: P^2 = P for the projector onto an exact unit
      vector (a/c, b/c) built from a Pythagorean triple.
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
        # projector onto the exact unit vector v = (a/c, b/c)
        a, b, c = random.choice(TRIPLES)
        aa = Fraction(a * a, c * c)
        ab = Fraction(a * b, c * c)
        bb = Fraction(b * b, c * c)
        p = f"[[{aa},{ab}],[{ab},{bb}]]"
        # P^2 entries: idempotence follows from aa + bb = 1
        e11 = aa * aa + ab * ab
        e12 = aa * ab + ab * bb
        e22 = ab * ab + bb * bb
        steps = [
            step("PROJECTOR_SETUP", f"v=({Fraction(a, c)}, {Fraction(b, c)})",
                 f"P=vv^T={p}"),
            step("MATRIX_MULT", "row1 dot col1",
                 f"{aa}*{aa}+{ab}*{ab}", str(e11)),
            step("MATRIX_MULT", "row1 dot col2",
                 f"{aa}*{ab}+{ab}*{bb}", str(e12)),
            step("MATRIX_MULT", "row2 dot col2",
                 f"{ab}*{ab}+{bb}*{bb}", str(e22)),
            step("CHECK", "P^2", p, "idempotent"),
        ]
        answer = "projector yes; P^2 = P"
        problem = f"Verify that P={p} is a projector."
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
