import random

from base_generator import ProblemGenerator
from helpers import step, jid


class UncertaintyGenerator(ProblemGenerator):
    """
    Uncertainty product for a particle in a 1D box with L=1 and hbar=1.

    Uses supplied expectation formulas:
    <x>=1/2, <x^2>=1/3 - 1/(2 n^2 pi^2),
    <p>=0, <p^2>=n^2 pi^2.

    Op-codes used:
    - UNCERTAINTY_SETUP / FORMULA / VARIANCE / PRODUCT / CHECK
    - E / M (established/shared): exact integer arithmetic
    - Z: exact symbolic uncertainty product
    """

    def generate(self) -> dict:
        n = random.randint(1, 200)
        n_sq = n * n
        two_n_sq = 2 * n_sq
        product_inside = f"{n_sq}pi^2/12 - 1/2"
        answer = f"Delta x Delta p = sqrt({product_inside})"
        steps = [
            step("UNCERTAINTY_SETUP", "particle in a box",
                 "L=1, hbar=1", f"n={n}"),
            step("FORMULA", "<x>=1/2",
                 "<x^2>=1/3 - 1/(2 n^2 pi^2)"),
            step("FORMULA", "<p>=0", "<p^2>=n^2 pi^2"),
            step("E", n, 2, n_sq),
            step("M", 2, n_sq, two_n_sq),
            step("VARIANCE", "Delta x^2",
                 f"1/12 - 1/({two_n_sq}pi^2)"),
            step("VARIANCE", "Delta p^2", f"{n_sq}pi^2"),
            step("PRODUCT", "Delta x^2 * Delta p^2", product_inside),
            step("CHECK", "Heisenberg lower bound", ">= 1/4", "holds"),
        ]
        steps.append(step("Z", answer))
        problem = (
            f"For a particle in a 1D box with L=1 and hbar=1 in state "
            f"n={n}, use the supplied expectation formulas to compute "
            f"Delta x Delta p exactly."
        )
        return dict(
            problem_id=jid(),
            operation="uncertainty_particle_box",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
