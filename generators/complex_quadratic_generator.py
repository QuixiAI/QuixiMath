import math
import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.complex_number_ops_generator import cx


VARIABLES = ["x", "y", "z", "t", "u", "v", "w", "s", "m", "n"]

TEMPLATES = [
    "Solve: {eq}.",
    "Solve for {var}: {eq}.",
    "Find all solutions of {eq}.",
    "Determine the complex roots of {eq}.",
    "Solve the equation {eq} over the complex numbers.",
    "Use the quadratic formula to solve {eq}.",
    "The equation {eq} has no real solutions. Find its two complex roots.",
]

# |p| stays small when the leading coefficient grows so the arithmetic
# (b^2 - 4ac and the division by 2a) remains pencil-and-paper sized.
LEAD_RANGE = {1: 20, 2: 11, 3: 8}


def poly_text(lead, b, const, var):
    """Render lead*var^2 + b*var + const with the usual sign conventions."""
    out = f"{'' if lead == 1 else lead}{var}^2"
    if b:
        coef = "" if abs(b) == 1 else str(abs(b))
        out += f" {'+' if b > 0 else '-'} {coef}{var}"
    if const:
        out += f" {'+' if const > 0 else '-'} {abs(const)}"
    return out


class ComplexQuadraticGenerator(ProblemGenerator):
    """
    Solves quadratics with negative discriminant by the quadratic formula,
    producing complex conjugate roots.

    Variants:
    - gaussian: roots p ± qi with integers p, q (discriminant -4a^2 q^2)
    - radical:  roots p ± i√k with k squarefree (discriminant -4a^2 k)

    The equation is built from the roots, so the discriminant is negative by
    construction and the division by 2a is always exact. Instances vary in
    leading coefficient (1-3), root size, variable letter, and whether the
    equation is already in standard form or has a non-zero constant on the
    right-hand side that must be moved first.

    Op-codes used:
    - EQ_SETUP: the equation (established)
    - S / REWRITE: move the right-hand constant across, then restate the
      equation in standard form (established)
    - DISC: discriminant work and value (established)
    - DISC_CLASSIFY: negative discriminant -> two complex conjugate
      roots (established)
    - SQRT_NEG: square root of a negative number in i-form
      (radicand work, value)
    - ROOT_SIMPLIFY: pull the square factor out of i√n (established)
    - Q1 / Q2: each root from the formula (-b, sqrt_disc, denom, root)
      (established shapes from QuadraticGenerator)
    - Z: 'x = p + qi or x = p - qi' (roots with + listed first)
    """

    VARIANTS = ["gaussian", "radical"]
    SQUAREFREE = [n for n in range(2, 47)
                  if all(n % (f * f) for f in range(2, math.isqrt(n) + 1))]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        var = random.choice(VARIABLES)
        A = random.choice(list(LEAD_RANGE))
        span = LEAD_RANGE[A]
        p = random.randint(-span, span)
        B = -2 * A * p

        if variant == "gaussian":
            q = random.randint(1, 12)
            k = q * q
        else:
            k = random.choice(self.SQUAREFREE)
        C = A * (p * p + k)
        disc = -4 * A * A * k

        shift = random.choice([s for s in range(-9, 10) if s != 0] + [0] * 3)
        eq = f"{poly_text(A, B, C, var)} = 0"
        display_eq = (eq if shift == 0
                      else f"{poly_text(A, B, C + shift, var)} = {shift}")

        wb = f"({B})" if B < 0 else str(B)
        steps = [step("EQ_SETUP", display_eq, "solve")]
        if shift != 0:
            steps.append(step("S", C + shift, shift, C))
            steps.append(step("REWRITE", eq))
        steps.extend([
            step("DISC", f"{wb}^2 - 4({A})({C})", disc),
            step("DISC_CLASSIFY", f"{disc} < 0",
                 "two complex conjugate roots"),
        ])

        if variant == "gaussian":
            sqrt_txt = cx(0, 2 * A * q)
            root_hi, root_lo = cx(p, q), cx(p, -q)
            steps.append(step("SQRT_NEG", f"√({disc})", sqrt_txt))
        else:
            sqrt_txt = f"{2 * A}i√{k}"
            imag = f"i√{k}"
            root_hi = f"{p} + {imag}" if p != 0 else imag
            root_lo = f"{p} - {imag}" if p != 0 else f"-{imag}"
            steps.append(step("SQRT_NEG", f"√({disc})", f"i√{-disc}"))
            steps.append(step("ROOT_SIMPLIFY", sqrt_txt))

        answer = f"{var} = {root_hi} or {var} = {root_lo}"
        steps.append(step("Q1", -B, sqrt_txt, 2 * A, root_hi))
        steps.append(step("Q2", -B, sqrt_txt, 2 * A, root_lo))
        steps.append(step("Z", answer))

        problem = random.choice(TEMPLATES).format(eq=display_eq, var=var)

        return dict(
            problem_id=jid(),
            operation="quadratic_complex_roots",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
