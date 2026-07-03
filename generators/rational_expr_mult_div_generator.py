import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.factor_trinomial_generator import binomial, pair_search
from generators.rational_expr_simplify_generator import trinomial_txt


class RationalExprMultDivGenerator(ProblemGenerator):
    """
    Multiplies and divides rational expressions. Built from binomial
    constants so that after factoring both trinomials and multiplying
    across, exactly two factors cancel, leaving a binomial over a binomial:

        (x+A)(x+B)   (x+C)      (x+B)
        ---------- · ------  =  -----
        (x+C)(x+D)   (x+A)      (x+D)

    Division inverts the second fraction first (the classic I step from the
    fraction generators), then proceeds as multiplication.

    Op-codes used:
    - POLY_SETUP / REWRITE / FACTOR_PAIR_GOAL / TRY / REJECT / ACCEPT
    - I: invert the divisor fraction (original, inverted)
    - FORM_IDENTIFY: the fraction rule (name, formula)
    - CANCEL: cancel one common factor (factor, result)
    - Z: final answer
    """

    def __init__(self, operation=None):
        if operation is not None and operation not in ("multiply", "divide"):
            raise ValueError("operation must be 'multiply', 'divide', or None")
        self.op_choice = operation

    def generate(self) -> dict:
        op = self.op_choice or random.choice(["multiply", "divide"])
        var = random.choice(["x", "x", "x", "y", "n"])

        while True:
            consts = random.sample(
                [v for v in range(-8, 9) if v != 0], 4)
            A, B, C, D = consts
            if A + B != 0 and C + D != 0:
                break

        tri1 = trinomial_txt(var, A + B, A * B)     # (x+A)(x+B)
        tri2 = trinomial_txt(var, C + D, C * D)     # (x+C)(x+D)
        fA, fB = binomial(var, A), binomial(var, B)
        fC, fD = binomial(var, C), binomial(var, D)

        second_num, second_den = (fC, fA) if op == "multiply" else (fA, fC)
        sym = "·" if op == "multiply" else "÷"
        original = (f"({tri1})/({tri2}) {sym} "
                    f"({second_num.strip('()')})/({second_den.strip('()')})")

        steps = [step("POLY_SETUP", original)]
        if op == "divide":
            steps.append(step("FORM_IDENTIFY", "divide_fractions",
                              "a/b ÷ c/d = a/b · d/c"))
            steps.append(step("I",
                              f"{second_num}/{second_den}",
                              f"{second_den}/{second_num}"))
        pair_search(steps, A * B, A + B)
        steps.append(step("REWRITE",
                          f"({fA}{fB})/({tri2}) · {fC}/{fA}"))
        pair_search(steps, C * D, C + D)
        steps.append(step("REWRITE",
                          f"({fA}{fB})/({fC}{fD}) · {fC}/{fA}"))
        steps.append(step("FORM_IDENTIFY", "multiply_fractions",
                          "a/b · c/d = ac/(bd)"))
        combined = f"({fA}{fB}{fC})/({fC}{fD}{fA})"
        steps.append(step("REWRITE", combined))
        after_first = f"({fB}{fC})/({fC}{fD})"
        steps.append(step("CANCEL", fA, after_first))
        answer = f"{fB}/{fD}"
        steps.append(step("CANCEL", fC, answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"rational_expr_{op}",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )
