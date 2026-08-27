import random
from fractions import Fraction
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


PHASE_FACTORS = tuple(sorted({
    Fraction(numerator, denominator)
    for denominator in range(1, 301)
    for numerator in range(0, 2 * denominator)
}))


def phase_text(value):
    """Render a nonnegative exact multiple of pi."""
    value = Fraction(value)
    if value == 0:
        return "0"
    if value.denominator == 1:
        return "π" if value == 1 else f"{value.numerator}π"
    head = "π" if value.numerator == 1 else f"{value.numerator}π"
    return f"{head}/{value.denominator}"


class PartialTraceGenerator(ProblemGenerator):
    """
    Reduced density matrices by tracing out qubit B for exact two-qubit
    state families.

    Variants:
    - bell_phi_plus: phase-shifted Phi Bell family; mixed and entangled.
    - product_plus_zero: phase-shifted plus state tensor ket0; separable.
    - schmidt_diagonal: sqrt(a)ket00 ± sqrt(b)ket11 with exact weights.

    Op-codes used:
    - DENSITY_SETUP / OUTER_PRODUCT / PARTIAL_TRACE /
      REDUCED_DENSITY / CHECK
    - Z: reduced density matrix and entanglement verdict
    """

    VARIANTS = ["bell_phi_plus", "product_plus_zero", "schmidt_diagonal"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "bell_phi_plus":
            problem, steps, answer = self._generate_bell()
        elif variant == "product_plus_zero":
            problem, steps, answer = self._generate_product()
        else:
            problem, steps, answer = self._generate_schmidt()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"partial_trace_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_bell(self):
        phase = phase_text(random.choice(PHASE_FACTORS))
        positive_phase = f"e^(i{phase})"
        negative_phase = f"e^(-i{phase})"
        psi = f"(ket00 + {positive_phase}ket11)/sqrt(2)"
        rho = "[[1/2,0],[0,1/2]]"
        steps = [
            step("DENSITY_SETUP", "state=Phi_phase", f"psi={psi}"),
            step("OUTER_PRODUCT",
                 f"rho=1/2(ket00bra00+{negative_phase}ket00bra11+"
                 f"{positive_phase}ket11bra00+ket11bra11)"),
            step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            step("PARTIAL_TRACE", "ket00bra11", "0"),
            step("PARTIAL_TRACE", "ket11bra00", "0"),
            step("PARTIAL_TRACE", "ket11bra11", "ket1bra1"),
            step("REDUCED_DENSITY", f"rho_A={rho}"),
            step("CHECK", "Tr(rho_A^2)", "1/2", "mixed entangled"),
        ]
        answer = f"rho_A = {rho}; entangled yes"
        problem = (
            f"Trace out qubit B for phase-shifted Bell state Phi({phase}) "
            f"= {psi}."
        )
        return problem, steps, answer

    def _generate_schmidt(self):
        # sqrt(a)ket00 ± sqrt(b)ket11, normalized by sqrt(a+b); a != b so
        # this never duplicates the Bell variant
        while True:
            a = random.randint(1, 250)
            b = random.randint(1, 250)
            if a != b and gcd(a, b) == 1:
                break
        sign = random.choice(["+", "-"])
        total = a + b
        pa, pb = Fraction(a, total), Fraction(b, total)
        purity = pa * pa + pb * pb
        rho = f"[[{pa},0],[0,{pb}]]"
        psi = f"(sqrt({a})ket00 {sign} sqrt({b})ket11)/sqrt({total})"
        cross = f"sqrt({a * b})/{total}"
        steps = [
            step("DENSITY_SETUP", "state=Schmidt", f"psi={psi}"),
            step("OUTER_PRODUCT",
                 f"rho={pa}ket00bra00 {sign} {cross}(ket00bra11+ket11bra00) + {pb}ket11bra11"),
            step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            step("PARTIAL_TRACE", "ket00bra11", "0"),
            step("PARTIAL_TRACE", "ket11bra00", "0"),
            step("PARTIAL_TRACE", "ket11bra11", "ket1bra1"),
            step("REDUCED_DENSITY", f"rho_A={rho}"),
            step("CHECK", "Tr(rho_A^2)", str(purity), "mixed entangled"),
        ]
        answer = f"rho_A = {rho}; entangled yes"
        problem = f"Trace out qubit B for the state psi = {psi}."
        return problem, steps, answer

    def _generate_product(self):
        phase = phase_text(random.choice(PHASE_FACTORS))
        positive_phase = f"e^(i{phase})"
        negative_phase = f"e^(-i{phase})"
        psi = f"(ket00 + {positive_phase}ket10)/sqrt(2)"
        rho = (f"[[1/2,{negative_phase}/2],"
               f"[{positive_phase}/2,1/2]]")
        steps = [
            step("DENSITY_SETUP", "state=plus_phase_0", f"psi={psi}"),
            step("OUTER_PRODUCT",
                 f"rho=1/2(ket00bra00+{negative_phase}ket00bra10+"
                 f"{positive_phase}ket10bra00+ket10bra10)"),
            step("PARTIAL_TRACE", "ket00bra00", "ket0bra0"),
            step("PARTIAL_TRACE", "ket00bra10", "ket0bra1"),
            step("PARTIAL_TRACE", "ket10bra00", "ket1bra0"),
            step("PARTIAL_TRACE", "ket10bra10", "ket1bra1"),
            step("REDUCED_DENSITY", f"rho_A={rho}"),
            step("CHECK", "Tr(rho_A^2)", "1", "pure separable"),
        ]
        answer = f"rho_A = {rho}; entangled no"
        problem = (
            f"Trace out qubit B for phase-shifted product state "
            f"plus({phase})0 = {psi}."
        )
        return problem, steps, answer
