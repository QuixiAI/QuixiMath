import random

from base_generator import ProblemGenerator
from helpers import step, jid


def term_txt(coeff, power):
    if power == 0:
        return str(abs(coeff))
    body = "x" if power == 1 else f"x^{power}"
    return body if abs(coeff) == 1 else f"{abs(coeff)}{body}"


def poly_txt(coeffs):
    pieces = []
    for power, coeff in enumerate(coeffs):
        if coeff == 0:
            continue
        body = term_txt(coeff, power)
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def left_txt(k):
    if k == 1:
        return "y' = y"
    if k == -1:
        return "y' = -y"
    return f"y' = {k}y"


def coeff_var_txt(k, var):
    if k == 1:
        return var
    if k == -1:
        return f"-{var}"
    return f"{k}{var}"


class SeriesSolutionGenerator(ProblemGenerator):
    """
    Power-series solutions of differential equations by coefficient matching.

    Variant:
    - first_order_exp: y' = ky, y(0)=120, through x^5

    Op-codes used:
    - ODE_SETUP (established): equation, initial value, requested order
    - SERIES_ASSUME: power-series form
    - DERIV_SERIES: differentiated series
    - COEFF_MATCH: equation after matching powers
    - RECURRENCE: coefficient recurrence
    - INITIAL_COEFF / COEFF: generated coefficients
    - M / D (established): recurrence arithmetic
    - Z: truncated series
    """

    VARIANTS = ["first_order_exp"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        k = random.choice([-3, -2, -1, 1, 2, 3])
        a0 = 120 * random.randint(1, 60)
        coeffs = [a0]
        steps = [
            step("ODE_SETUP", f"{left_txt(k)}, y(0) = {a0}",
                 "power series through x^5"),
            step("SERIES_ASSUME", "y", "sum a_n x^n"),
            step("DERIV_SERIES", "y'",
                 "sum (n+1)a_(n+1)x^n"),
            step("REWRITE", coeff_var_txt(k, "y"),
                 f"sum {coeff_var_txt(k, 'a_n')} x^n"),
            step("COEFF_MATCH", "x^n",
                 f"(n+1)a_(n+1) = {coeff_var_txt(k, 'a_n')}"),
            step("RECURRENCE", "a_(n+1)",
                 f"{coeff_var_txt(k, 'a_n')}/(n+1)"),
            step("INITIAL_COEFF", "a_0", a0),
        ]
        for n in range(5):
            prod = k * coeffs[n]
            next_coeff = prod // (n + 1)
            coeffs.append(next_coeff)
            steps.extend([
                step("M", k, coeffs[n], prod),
                step("D", prod, n + 1, next_coeff),
                step("COEFF", f"a_{n + 1}", next_coeff),
            ])
        answer = f"y = {poly_txt(coeffs)} + O(x^6)"
        steps.append(step("Z", answer))
        problem = (
            f"Find the power-series solution through x^5 for {left_txt(k)} "
            f"with y(0) = {a0}."
        )
        return dict(
            problem_id=jid(),
            operation="series_solution_first_order_exp",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
