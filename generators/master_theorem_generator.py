import random

from base_generator import ProblemGenerator
from helpers import step, jid


def pow_txt(power):
    return "n" if power == 1 else f"n^{power}"


def term_txt(coeff, power):
    body = pow_txt(power)
    return body if coeff == 1 else f"{coeff}{body}"


class MasterTheoremGenerator(ProblemGenerator):
    """
    Recurrence growth by the Master Theorem and subtract-and-conquer sums.

    Variants:
    - master_case1: a=b^p with p<k, so f(n) dominates.
    - master_case2: a=b^k, so the balanced case adds log n.
    - master_case3: a=b^p with p>k, so the recursive work dominates.
    - subtract: T(n)=T(n-1)+n^k, summed as a power series order.

    Op-codes used:
    - REC_SETUP: recurrence
    - LOG_EXACT: exact log_b(a)
    - COMPARE / MASTER_CASE / SUM_ORDER
    - Z: composite case and Θ-bound
    """

    VARIANTS = ["master_case1", "master_case2", "master_case3", "subtract"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        steps = []
        if variant == "subtract":
            k = random.randint(1, 9)
            coeff = random.randint(1, 30)
            bound = f"Θ({pow_txt(k + 1)})"
            steps = [
                step("REC_SETUP", f"T(n) = T(n-1) + {term_txt(coeff, k)}"),
                step("REWRITE", f"T(n) = T(1) + {coeff}Σ i^{k}"),
                step("SUM_ORDER", f"Σ i^{k}", pow_txt(k + 1)),
            ]
            answer = f"subtract; {bound}"
            problem = (
                f"Solve the recurrence T(n) = T(n-1) + {term_txt(coeff, k)} "
                "in Θ notation."
            )
        else:
            b = random.randint(2, 12)
            coeff = random.randint(1, 30)
            if variant == "master_case1":
                k = random.randint(2, 9)
                p = random.randint(0, k - 1)
                case = "case 1"
                bound = f"Θ({pow_txt(k)})"
                relation = "<"
            elif variant == "master_case2":
                k = random.randint(1, 9)
                p = k
                case = "case 2"
                bound = f"Θ({pow_txt(k)} log n)"
                relation = "="
            else:
                k = random.randint(1, 7)
                p = random.randint(k + 1, k + 5)
                case = "case 3"
                bound = f"Θ({pow_txt(p)})"
                relation = ">"
            a = b ** p
            steps = [
                step("REC_SETUP", f"T(n) = {a}T(n/{b}) + {term_txt(coeff, k)}"),
                step("LOG_EXACT", f"log_{b}({a})", p),
                step("COMPARE", f"{p} {relation} {k}",
                     f"log_b(a) {relation} k"),
                step("MASTER_CASE", case, bound),
            ]
            answer = f"{case}; {bound}"
            problem = (
                f"Use the Master Theorem to solve T(n) = {a}T(n/{b}) + "
                f"{term_txt(coeff, k)} in Θ notation."
            )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"master_theorem_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
