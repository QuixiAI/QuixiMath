import math
import random

from base_generator import ProblemGenerator
from helpers import step, jid


class CountingClassicsGenerator(ProblemGenerator):
    """
    Classic counting principles and identities.

    Variants:
    - pigeonhole: minimum objects to force k in one of m boxes.
    - catalan: balanced strings/lattice-path Catalan counts.
    - vandermonde: evaluate both sides of Vandermonde's identity.
    - hockey_stick: evaluate a hockey-stick binomial sum.

    Op-codes used:
    - COUNT_SETUP / COMB_SETUP / IDENTITY
    - A / S / M / D (established)
    - Z: exact count or composite identity value
    """

    VARIANTS = ["pigeonhole", "catalan", "vandermonde", "hockey_stick"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "pigeonhole":
            boxes = random.randint(2, 80)
            k = random.randint(2, 30)
            max_without = boxes * (k - 1)
            value = max_without + 1
            steps = [
                step("COUNT_SETUP", f"{boxes} boxes", f"force {k} in one box"),
                step("S", k, 1, k - 1),
                step("M", boxes, k - 1, max_without),
                step("A", max_without, 1, value),
            ]
            answer = f"minimum = {value}"
            problem = (
                f"What is the minimum number of objects needed to guarantee "
                f"at least {k} objects in one of {boxes} boxes?"
            )
        elif variant == "catalan":
            n = random.randint(2, 25)
            choose = math.comb(2 * n, n)
            value = choose // (n + 1)
            steps = [
                step("COUNT_SETUP", f"Catalan C_{n}"),
                step("COMB_SETUP", f"C({2 * n}, {n})", choose),
                step("D", choose, n + 1, value),
            ]
            answer = f"Catalan C_{n} = {value}"
            problem = f"How many balanced parenthesis strings are there with {n} pairs?"
        elif variant == "vandermonde":
            r = random.randint(3, 25)
            s = random.randint(3, 25)
            n = random.randint(2, min(r + s, 25))
            value = math.comb(r + s, n)
            steps = [
                step("IDENTITY", "Vandermonde",
                     f"Σ C({r},i)C({s},{n}-i) = C({r+s},{n})"),
                step("COMB_SETUP", f"C({r + s}, {n})", value),
            ]
            answer = f"sum = {value}; C({r+s},{n}) = {value}"
            problem = (
                f"Use Vandermonde's identity to evaluate "
                f"Σ_{{i}} C({r},i)C({s},{n}-i)."
            )
        else:
            r = random.randint(1, 20)
            n = random.randint(r + 3, r + 90)
            value = math.comb(n + 1, r + 1)
            steps = [
                step("IDENTITY", "hockey-stick",
                     f"Σ i={r}..{n} C(i,{r}) = C({n+1},{r+1})"),
                step("COMB_SETUP", f"C({n + 1}, {r + 1})", value),
            ]
            answer = f"sum = {value}; C({n+1},{r+1}) = {value}"
            problem = f"Use the hockey-stick identity to evaluate Σ_{{i={r}}}^{{{n}}} C(i,{r})."
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"counting_classics_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
