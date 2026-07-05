import random
from fractions import Fraction
from math import comb

from base_generator import ProblemGenerator
from helpers import step, jid


EPSILONS = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)]


def ftxt(value):
    return str(Fraction(value))


class BECChannelGenerator(ProblemGenerator):
    """
    Binary erasure channel capacity and block erasure probabilities.

    Op-codes used:
    - BEC_SETUP / BEC_FORMULA
    - S / M / E / COMB
    - Z: exact capacity or block probability
    """

    VARIANTS = ["capacity", "no_erasure", "exactly_one_erasure"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        eps = random.choice(EPSILONS)
        q = 1 - eps
        n = random.randint(3, 6)
        steps = [step("BEC_SETUP", f"epsilon={ftxt(eps)}")]
        steps.append(step("S", 1, ftxt(eps), ftxt(q)))
        if variant == "capacity":
            steps.append(step("BEC_FORMULA", "C=1-epsilon"))
            answer = f"C = {ftxt(q)} bits/use"
            task = "Find the channel capacity."
        elif variant == "no_erasure":
            prob = q ** n
            steps.append(step("BEC_FORMULA", "P(no erasures)=(1-epsilon)^n"))
            steps.append(step("E", ftxt(q), n, ftxt(prob)))
            answer = f"P(no erasures in {n}) = {ftxt(prob)}"
            task = f"Find the probability of no erasures in n={n} uses."
        else:
            prob = Fraction(comb(n, 1)) * eps * (q ** (n - 1))
            steps.append(step("BEC_FORMULA",
                              "P(exactly one)=C(n,1)*epsilon*(1-epsilon)^(n-1)"))
            steps.append(step("COMB", f"C({n},1)", n))
            steps.append(step("E", ftxt(q), n - 1, ftxt(q ** (n - 1))))
            steps.append(step("M", n, ftxt(eps), ftxt(n * eps)))
            steps.append(step("M", ftxt(n * eps), ftxt(q ** (n - 1)),
                              ftxt(prob)))
            answer = f"P(exactly one erasure in {n}) = {ftxt(prob)}"
            task = f"Find the probability of exactly one erasure in n={n} uses."
        problem = (
            f"A binary erasure channel has erasure probability epsilon={ftxt(eps)}. "
            f"{task}"
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"bec_channel_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
