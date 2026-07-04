import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.polynomial_long_division_generator import poly_txt


class HornerEvaluationGenerator(ProblemGenerator):
    """
    Evaluates a polynomial at x = r by Horner's method: write the
    nested form, then run the multiply-add rhythm across the
    coefficients. The record closes with a CHECK evaluating one term
    directly (A1) so the nested result is corroborated.

    This is the same table as synthetic division - the final cell is
    P(r) - which is the bridge the curriculum wants.

    Op-codes used:
    - HORNER_SETUP: the polynomial and the evaluation point
      (polynomial, x = r)
    - REWRITE: the nested (Horner) form
    - COEFFS: the coefficient row (established)
    - SYN_DROP: bring down the lead (established)
    - M / A: multiply by r, add the next coefficient (established)
    - EVAL: P(r) read from the final cell (established)
    - CHECK: direct evaluation of the leading term as corroboration
      (established)
    - Z: final answer
    """

    def generate(self) -> dict:
        var = "x"
        r = random.choice([v for v in range(-4, 5) if v != 0])
        deg = random.choice([3, 3, 4])
        while True:
            coefs = [random.choice([v for v in range(-5, 6) if v != 0])
                     for _ in range(deg + 1)]
            if abs(coefs[0]) <= 3:
                break

        poly = poly_txt(coefs, var)
        # nested form: ((a x + b)x + c)x + d, hiding a unit lead
        nested = {1: "", -1: "-"}.get(coefs[0], str(coefs[0]))
        for c in coefs[1:]:
            sign = "+" if c >= 0 else "-"
            nested = f"({nested}{var} {sign} {abs(c)})"
        nested = nested[1:-1]  # outermost parens are unnecessary
        value = 0
        for c in coefs:
            value = value * r + c

        steps = [
            step("HORNER_SETUP", poly, f"{var} = {r}"),
            step("REWRITE", nested),
            step("COEFFS", ", ".join(str(c) for c in coefs)),
            step("SYN_DROP", coefs[0]),
        ]
        acc = coefs[0]
        for c in coefs[1:]:
            steps.append(step("M", r, acc, r * acc))
            steps.append(step("A", r * acc, c, r * acc + c))
            acc = r * acc + c
        steps.append(step("EVAL", f"P({r})", acc))
        lead = coefs[0] * r ** deg
        steps.append(step("CHECK", "leading term",
                          f"{coefs[0]}·({r})^{deg} = {lead}", lead))
        steps.append(step("Z", acc))

        return dict(
            problem_id=jid(),
            operation="horner_evaluation",
            problem=(f"Use Horner's method to evaluate "
                     f"P({var}) = {poly} at {var} = {r}."),
            steps=steps,
            final_answer=str(acc),
        )
