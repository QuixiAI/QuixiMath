import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt
from generators.factor_trinomial_generator import binomial, pair_search
from generators.complex_number_ops_generator import cx


class PolynomialZerosGenerator(ProblemGenerator):
    """
    Finds all zeros of a monic cubic from one given zero: synthetic
    division deflates to a quadratic (the R = 0 cell confirms the given
    zero), then the quadratic is finished off.

    Variants:
    - factorable: the quadratic factors over the integers - the usual
      TRY/REJECT/ACCEPT pair sweep, then zero-product
    - complex:    the quadratic has negative discriminant - DISC,
      SQRT_NEG, Q1/Q2, conjugate pair

    Op-codes used:
    - EQ_SETUP: the equation and the given zero (established)
    - SYNDIV_SETUP / COEFFS / SYN_DROP / M / A / SYN_ROW / R:
      the deflation (established)
    - REWRITE: the deflated quadratic (established)
    - FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT / ZERO_PRODUCT:
      factorable path (established)
    - DISC / DISC_CLASSIFY / SQRT_NEG / Q1 / Q2: complex path
      (established)
    - Z: all three zeros
    """

    VARIANTS = ["factorable", "complex"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["factorable", "factorable", "complex"])
        var = "x"

        while True:
            if variant == "factorable":
                roots = random.sample(range(-6, 7), 3)
                given = random.choice(roots)
                others = sorted(r for r in roots if r != given)
                B = -(others[0] + others[1])
                C = others[0] * others[1]
                if C == 0:
                    continue
            else:
                given = random.choice([v for v in range(-4, 5) if v != 0])
                p = random.randint(-3, 3)
                q = random.randint(1, 4)
                B = -2 * p
                C = p * p + q * q
            # dividend = (x - given)(x^2 + Bx + C)
            coefs = [1, B - given, C - given * B, -given * C]
            if 0 not in coefs:
                break

        poly = poly_txt(coefs, var)
        quad = poly_txt([1, B, C], var)

        steps = [
            step("EQ_SETUP", f"{poly} = 0",
                 f"find all zeros; given {var} = {given}"),
            step("SYNDIV_SETUP", poly, f"r = {given}"),
            step("COEFFS", ", ".join(str(c) for c in coefs)),
            step("SYN_DROP", coefs[0]),
        ]
        bottom = [coefs[0]]
        for c in coefs[1:]:
            prod = given * bottom[-1]
            steps.append(step("M", given, bottom[-1], prod))
            steps.append(step("A", c, prod, c + prod))
            bottom.append(c + prod)
        steps.append(step("SYN_ROW", ", ".join(str(v) for v in bottom)))
        steps.append(step("R", 0))
        steps.append(step("REWRITE", f"{quad} = 0"))

        if variant == "factorable":
            m, n = pair_search(steps, C, B)
            f1, f2 = binomial(var, m), binomial(var, n)
            steps.append(step("REWRITE", f"{f1}{f2} = 0"))
            steps.append(step("ZERO_PRODUCT", f"{f1}{f2} = 0",
                              f"{f1[1:-1]} = 0 or {f2[1:-1]} = 0"))
            zeros = sorted([given, others[0], others[1]])
            # A0 convention: multiple roots ascending, joined with ' or '
            answer = " or ".join(f"{var} = {z}" for z in zeros)
        else:
            disc = B * B - 4 * C
            wb = f"({B})" if B < 0 else str(B)
            steps.append(step("DISC", f"{wb}^2 - 4(1)({C})", disc))
            steps.append(step("DISC_CLASSIFY", f"{disc} < 0",
                              "two complex conjugate roots"))
            steps.append(step("SQRT_NEG", f"√({disc})", f"{2 * q}i"))
            hi, lo = cx(p, q), cx(p, -q)
            steps.append(step("Q1", -B, f"{2 * q}i", 2, hi))
            steps.append(step("Q2", -B, f"{2 * q}i", 2, lo))
            answer = f"{var} = {given} or {var} = {hi} or {var} = {lo}"
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="polynomial_all_zeros",
            problem=(f"Given that {var} = {given} is a zero, find all "
                     f"zeros of P({var}) = {poly}."),
            steps=steps,
            final_answer=answer,
        )
