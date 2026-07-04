import random

from base_generator import ProblemGenerator
from helpers import step, jid


class PartialTraceGenerator(ProblemGenerator):
    """
    Reduced density matrices by tracing out qubit B for two canonical
    two-qubit states.

    Variants:
    - bell_phi_plus: mixed reduced state, entangled.
    - product_plus_zero: pure reduced state, separable.

    Op-codes used:
    - DENSITY_SETUP / OUTER_PRODUCT / PARTIAL_TRACE /
      REDUCED_DENSITY / CHECK
    - Z: reduced density matrix and entanglement verdict
    """

    VARIANTS = ["bell_phi_plus", "product_plus_zero"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "bell_phi_plus":
            problem, steps, answer = self._generate_bell()
        else:
            problem, steps, answer = self._generate_product()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"partial_trace_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_bell(self):
        rho = "[[1/2,0],[0,1/2]]"
        steps = [
            step("DENSITY_SETUP", "state=Phi+",
                 "psi=(ket00 + ket11)/sqrt(2)"),
            step("OUTER_PRODUCT", "rho=1/2(ket00bra00+ket00bra11+ket11bra00+ket11bra11)"),
            step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            step("PARTIAL_TRACE", "ket00bra11", "0"),
            step("PARTIAL_TRACE", "ket11bra00", "0"),
            step("PARTIAL_TRACE", "ket11bra11", "ket1bra1"),
            step("REDUCED_DENSITY", f"rho_A={rho}"),
            step("CHECK", "Tr(rho_A^2)", "1/2", "mixed entangled"),
        ]
        answer = f"rho_A = {rho}; entangled yes"
        problem = (
            "Trace out qubit B for Bell state Phi+ = "
            "(ket00 + ket11)/sqrt(2)."
        )
        return problem, steps, answer

    def _generate_product(self):
        rho = "[[1/2,1/2],[1/2,1/2]]"
        steps = [
            step("DENSITY_SETUP", "state=plus0",
                 "psi=(ket00 + ket10)/sqrt(2)"),
            step("OUTER_PRODUCT", "rho=1/2(ket00bra00+ket00bra10+ket10bra00+ket10bra10)"),
            step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            step("PARTIAL_TRACE", "ket00bra10", "ket0bra1"),
            step("PARTIAL_TRACE", "ket10bra00", "ket1bra0"),
            step("PARTIAL_TRACE", "ket10bra10", "ket1bra1"),
            step("REDUCED_DENSITY", f"rho_A={rho}"),
            step("CHECK", "Tr(rho_A^2)", "1", "pure separable"),
        ]
        answer = f"rho_A = {rho}; entangled no"
        problem = (
            "Trace out qubit B for product state plus0 = "
            "(ket00 + ket10)/sqrt(2)."
        )
        return problem, steps, answer
