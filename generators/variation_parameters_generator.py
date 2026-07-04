import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def ode_lhs(p, q):
    return fmt_terms([(1, "y''"), (p, "y'"), (q, "y")])


def char_poly(p, q):
    return fmt_terms([(1, "r^2"), (p, "r"), (q, "")])


def exp_txt(rate):
    if rate == 0:
        return "1"
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_txt(coeff, rate):
    if rate == 0:
        return str(coeff)
    if coeff == 1:
        return exp_txt(rate)
    if coeff == -1:
        return f"-{exp_txt(rate)}"
    return f"{coeff}{exp_txt(rate)}"


def factor_txt(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def hom_symbolic(r1, r2):
    return f"C1{exp_txt(r1)} + C2{exp_txt(r2)}"


def signed_join(terms):
    return fmt_terms(terms)


def solution_txt(r1, r2, A_part, k):
    return "y = " + signed_join([
        (1, f"C1{exp_txt(r1)}"),
        (1, f"C2{exp_txt(r2)}"),
        (A_part, exp_txt(k)),
    ])


class VariationParametersGenerator(ProblemGenerator):
    """
    Variation of parameters for second-order constant-coefficient ODEs.
    The forcing is exponential and not part of the complementary solution, so
    the Wronskian and u1/u2 integrals are exact by hand.

    Variant:
    - exponential_forcing

    Op-codes used:
    - ODE_SETUP (established): equation and method
    - CHAR_EQ / FACTOR / CHAR_ROOTS / HOM_SOL: fundamental solutions
    - DERIV_FORM / WRONSKIAN: compute W[y1,y2]
    - VOP_FORM: variation-of-parameters u1', u2' formulas
    - D / A (established): coefficient arithmetic
    - ANTIDERIV / PARTICULAR / SOL_FORM: build y_p and full solution
    - Z: general solution
    """

    VARIANTS = ["exponential_forcing"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        nonzero = [-4, -3, -2, -1, 1, 2, 3, 4]
        r1, r2 = sorted(random.sample(nonzero, 2))
        d = r2 - r1
        k_choices = [v for v in nonzero if v not in (r1, r2)]
        k = random.choice(k_choices)
        scale = random.choice([-3, -2, -1, 1, 2, 3])
        A_part = d * scale
        p = -(r1 + r2)
        q = r1 * r2
        rhs_coeff = A_part * (k - r1) * (k - r2)
        rate1 = k - r1
        rate2 = k - r2
        u1_prime_coeff = -rhs_coeff // d
        u2_prime_coeff = rhs_coeff // d
        u1_coeff = u1_prime_coeff // rate1
        u2_coeff = u2_prime_coeff // rate2
        answer = solution_txt(r1, r2, A_part, k)
        rhs = coeff_exp_txt(rhs_coeff, k)
        wronskian = coeff_exp_txt(d, r1 + r2)

        steps = [
            step("ODE_SETUP", f"{ode_lhs(p, q)} = {rhs}",
                 "variation of parameters"),
            step("CHAR_EQ", "assume y=e^(rx)", f"{char_poly(p, q)} = 0"),
            step("FACTOR", char_poly(p, q),
                 f"{factor_txt(r1)}{factor_txt(r2)} = 0"),
            step("CHAR_ROOTS", f"r1 = {r1}, r2 = {r2}",
                 "fundamental solutions"),
            step("HOM_SOL", "y1, y2", f"y1 = {exp_txt(r1)}, "
                 f"y2 = {exp_txt(r2)}"),
            step("DERIV_FORM", "y1', y2'",
                 f"y1' = {coeff_exp_txt(r1, r1)}, "
                 f"y2' = {coeff_exp_txt(r2, r2)}"),
            step("WRONSKIAN", "y1*y2' - y1'*y2", wronskian),
            step("VOP_FORM", "u1' = -y2*g/W",
                 f"{-rhs_coeff}/{d} * {exp_txt(rate1)}"),
            step("D", -rhs_coeff, d, u1_prime_coeff),
            step("VOP_FORM", "u2' = y1*g/W",
                 f"{rhs_coeff}/{d} * {exp_txt(rate2)}"),
            step("D", rhs_coeff, d, u2_prime_coeff),
            step("ANTIDERIV", f"{coeff_exp_txt(u1_prime_coeff, rate1)} dx",
                 coeff_exp_txt(u1_coeff, rate1)),
            step("D", u1_prime_coeff, rate1, u1_coeff),
            step("ANTIDERIV", f"{coeff_exp_txt(u2_prime_coeff, rate2)} dx",
                 coeff_exp_txt(u2_coeff, rate2)),
            step("D", u2_prime_coeff, rate2, u2_coeff),
            step("A", u1_coeff, u2_coeff, A_part),
            step("PARTICULAR", "u1*y1 + u2*y2",
                 coeff_exp_txt(A_part, k)),
            step("SOL_FORM", answer),
            step("Z", answer),
        ]
        problem = (
            f"Solve {ode_lhs(p, q)} = {rhs} by variation of parameters."
        )
        return dict(
            problem_id=jid(),
            operation="variation_parameters_exponential_forcing",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
