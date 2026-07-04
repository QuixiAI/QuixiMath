import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


def cf_text(partials):
    if len(partials) == 1:
        return f"[{partials[0]}]"
    return f"[{partials[0]}; {', '.join(str(v) for v in partials[1:])}]"


def frac_text(num, den):
    return f"{num}/{den}"


def convergent_text(convergents):
    return ", ".join(frac_text(num, den) for num, den in convergents)


def continued_fraction(num, den):
    partials = []
    x, y = num, den
    divisions = []
    while y:
        q = x // y
        r = x - q * y
        divisions.append((x, y, q, r))
        partials.append(q)
        x, y = y, r
    return partials, divisions


class ContinuedFractionGenerator(ProblemGenerator):
    """
    Simple continued fractions and convergents for positive rationals.

    Op-codes used:
    - CF_SETUP / CF_PARTIAL / CF_RESULT: Euclidean quotient expansion
    - CONV_INIT / CONV_STEP / CONVERGENT: convergent recurrence
    - EUCLID_DIV / M / S / A (established/shared): arithmetic
    - Z: continued fraction and all convergents
    """

    def generate(self) -> dict:
        while True:
            den = random.randint(12, 160)
            num = random.randint(den + 1, 6 * den)
            if gcd(num, den) == 1:
                break

        partials, divisions = continued_fraction(num, den)
        steps = [
            step("CF_SETUP", frac_text(num, den)),
        ]
        for idx, (x, y, q, r) in enumerate(divisions):
            product = q * y
            steps.append(step("EUCLID_DIV", x, y, q, r))
            steps.append(step("M", q, y, product))
            steps.append(step("S", x, product, r))
            steps.append(step("CF_PARTIAL", f"a_{idx}", q))
        steps.append(step("CF_RESULT", cf_text(partials)))

        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0
        steps.append(step("CONV_INIT", "h_-2=0,h_-1=1",
                          "k_-2=1,k_-1=0"))
        convergents = []
        for idx, partial in enumerate(partials):
            h_prod = partial * h_prev1
            h = h_prod + h_prev2
            k_prod = partial * k_prev1
            k = k_prod + k_prev2
            steps.append(step("M", partial, h_prev1, h_prod))
            steps.append(step("A", h_prod, h_prev2, h))
            steps.append(step("M", partial, k_prev1, k_prod))
            steps.append(step("A", k_prod, k_prev2, k))
            steps.append(step("CONV_STEP", f"i={idx}", f"h={h}", f"k={k}"))
            steps.append(step("CONVERGENT", f"i={idx}", frac_text(h, k)))
            convergents.append((h, k))
            h_prev2, h_prev1 = h_prev1, h
            k_prev2, k_prev1 = k_prev1, k

        answer = (
            f"continued fraction = {cf_text(partials)}; "
            f"convergents = {convergent_text(convergents)}"
        )
        problem = (
            f"Find the simple continued fraction for {frac_text(num, den)} "
            f"and list all convergents."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="continued_fraction",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
