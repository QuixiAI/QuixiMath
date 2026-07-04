import random

from base_generator import ProblemGenerator
from helpers import step, jid


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def local_poly_text(coeffs, a):
    base = z_minus(a)
    terms = []
    for power, coef in enumerate(coeffs):
        if coef == 0:
            continue
        abs_coef = abs(coef)
        if power == 0:
            body = str(abs_coef)
        elif power == 1:
            body = base if abs_coef == 1 else f"{abs_coef}{base}"
        else:
            body = f"{base}^{power}" if abs_coef == 1 else \
                f"{abs_coef}{base}^{power}"
        if not terms:
            terms.append(body if coef > 0 else f"-{body}")
        else:
            terms.append(f"+ {body}" if coef > 0 else f"- {body}")
    return " ".join(terms) if terms else "0"


class ResidueGenerator(ProblemGenerator):
    """
    Residues at simple and higher-order poles using local Laurent terms.

    Variants:
    - simple: A/(z-a) plus analytic terms
    - higher_order: numerator over (z-a)^m, read the (z-a)^-1 term

    Op-codes used:
    - RESIDUE_SETUP / LAURENT_TERM / RESIDUE: local expansion
    - POLE_ORDER: order of the pole
    - Z: final residue
    """

    VARIANTS = ["simple", "higher_order"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "simple":
            problem, steps, answer = self._generate_simple()
        else:
            problem, steps, answer = self._generate_higher_order()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"residue_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_simple(self):
        a = random.randint(-5, 5)
        residue = random.choice([v for v in range(-9, 10) if v != 0])
        b = random.randint(-6, 6)
        c = random.randint(-6, 6)
        base = z_minus(a)
        analytic = local_poly_text([b, c], a)
        function = f"{residue}/{base}"
        if analytic != "0":
            function += f" - {analytic[1:]}" if analytic.startswith("-") \
                else f" + {analytic}"
        steps = [
            step("RESIDUE_SETUP", f"a={a}", f"f={function}"),
            step("POLE_ORDER", 1),
            step("LAURENT_TERM", f"{residue}{base}^-1"),
            step("RESIDUE", residue),
        ]
        answer = f"residue = {residue}"
        problem = f"Find the residue at z={a} of f(z) = {function}."
        return problem, steps, answer

    def _generate_higher_order(self):
        a = random.randint(-5, 5)
        order = random.choice([2, 3])
        coeffs = [random.randint(-5, 5) for _ in range(order + 2)]
        coeffs[order - 1] = random.choice([v for v in range(-9, 10)
                                           if v != 0])
        numerator = local_poly_text(coeffs, a)
        base = z_minus(a)
        residue = coeffs[order - 1]
        function = f"({numerator})/{base}^{order}"
        steps = [
            step("RESIDUE_SETUP", f"a={a}", f"f={function}"),
            step("POLE_ORDER", order),
        ]
        for power, coef in enumerate(coeffs):
            laurent_power = power - order
            steps.append(step("LAURENT_TERM",
                              f"{coef}{base}^{laurent_power}"))
        steps.append(step("RESIDUE", residue))
        answer = f"residue = {residue}"
        problem = (
            f"Find the residue at z={a} of f(z) = {function}, whose "
            f"numerator coefficients in powers of {base} are {coeffs}."
        )
        return problem, steps, answer
