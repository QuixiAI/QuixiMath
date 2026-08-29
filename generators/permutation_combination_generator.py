import math
import random
from fractions import Fraction

from applied_common import apply_applied_modifier
from base_generator import ProblemGenerator
from helpers import step, jid


APPLIED = True
#: Modifiers apply only to the ``word`` variant — the other three are
#: symbolic drills with no story to add a distractor or estimate to.
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")


def product_steps(factors):
    """Running-product M steps for a list of factors; returns steps and
    the product. No step for a single factor."""
    steps = []
    run = factors[0]
    for f in factors[1:]:
        steps.append(step("M", run, f, run * f))
        run *= f
    return steps, run


class PermutationCombinationGenerator(ProblemGenerator):
    """
    Factorials, permutations, and combinations with the factorial
    arithmetic written out as running products — the by-hand way.
    Combinations reuse the permutation count and divide by r!. All
    answers are exact integers.

    Variants:
    - factorial:   n! as 1·2·3·…·n
    - permutation: P(n,r) = n·(n-1)·…·(n-r+1)
    - combination: C(n,r) = P(n,r)/r!
    - word:        a word problem that first decides order (arrange →
                   permutation) vs. no order (choose → combination)

    Op-codes used:
    - FACT_SETUP / PERM_SETUP / COMB_SETUP: the expression and goal
    - FACT_FORMULA / PERM_FORMULA / COMB_FORMULA: the formula
    - IDENTIFY: for the word problem, whether order matters
    - REWRITE / M / D (established): the running products and divide
    - Z: the exact count
    """

    VARIANTS = ["factorial", "permutation", "combination", "word"]
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    def _perm_steps(self, n, r):
        """Steps computing P(n,r) and its value (numerator product)."""
        factors = list(range(n, n - r, -1))
        steps = [step("REWRITE",
                      " · ".join(str(f) for f in factors))]
        prod_steps, value = product_steps(factors)
        return steps + prod_steps, value, factors

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "factorial":
            n = random.randint(3, 14)
            start = random.randint(1, 10000)
            factors = list(range(1, n + 1))
            steps = [step("FACT_SETUP", f"{n}!", "expand the factorial"),
                     step("FACT_FORMULA",
                          f"{n}! = " + "·".join(str(f) for f in factors))]
            prod_steps, value = product_steps(factors)
            steps += prod_steps
            answer = str(value)
            problem = (f"Evaluate {n}!, the number of linear orders of "
                       f"the labeled items a_{start} through "
                       f"a_{start + n - 1}.")
        elif variant == "permutation":
            n = random.randint(4, 18)
            r = random.randint(2, min(8, n))
            start = random.randint(1, 2000)
            steps = [step("PERM_SETUP", f"P({n}, {r})",
                          "n!/(n-r)!"),
                     step("PERM_FORMULA",
                          f"P(n, r) = n·(n-1)···(n-r+1), {r} factors")]
            body, value, _ = self._perm_steps(n, r)
            steps += body
            answer = str(value)
            problem = (f"How many ordered arrangements are there of "
                       f"{r} items chosen from {n}? Compute P({n}, {r}) "
                       f"for the items a_{start} through "
                       f"a_{start + n - 1}.")
        elif variant == "combination":
            n = random.randint(4, 18)
            r = random.randint(2, min(8, n - 1))
            start = random.randint(1, 2000)
            steps = [step("COMB_SETUP", f"C({n}, {r})",
                          "n!/(r!·(n-r)!)"),
                     step("COMB_FORMULA", "C(n, r) = P(n, r)/r!")]
            body, numer, _ = self._perm_steps(n, r)
            steps += body
            r_fact_steps, rfact = product_steps(list(range(1, r + 1)))
            steps.append(step("REWRITE",
                              f"{r}! = " +
                              "·".join(str(f) for f in range(1, r + 1))))
            steps += r_fact_steps
            value = numer // rfact
            steps.append(step("D", numer, rfact, value))
            answer = str(value)
            problem = (f"How many ways can {r} items be chosen from "
                       f"{n} when order does not matter? Compute "
                       f"C({n}, {r}) for the items a_{start} through "
                       f"a_{start + n - 1}.")
        else:
            n = random.randint(4, 16)
            r = random.randint(2, min(7, n - 1))
            start = random.randint(1, 2000)
            order = random.random() < 0.5
            if order:
                steps = [
                    step("PERM_SETUP", f"arrange {r} of {n}",
                         "order matters"),
                    step("IDENTIFY", "order matters", "use P(n, r)"),
                    step("PERM_FORMULA",
                         f"P(n, r) = n·(n-1)···(n-r+1), {r} factors"),
                ]
                body, value, _ = self._perm_steps(n, r)
                steps += body
                problem = (f"In how many ways can {r} people be "
                           f"seated in a row of {r} chairs, chosen "
                           f"from a group of {n}? The people are labeled "
                           f"p_{start} through p_{start + n - 1}.")
                model = "P(n, r) = n·(n − 1)···(n − r + 1)"
            else:
                steps = [
                    step("COMB_SETUP", f"choose {r} of {n}",
                         "order does not matter"),
                    step("IDENTIFY", "order does not matter",
                         "use C(n, r)"),
                    step("COMB_FORMULA", "C(n, r) = P(n, r)/r!"),
                ]
                body, numer, _ = self._perm_steps(n, r)
                steps += body
                r_fact_steps, rfact = product_steps(list(range(1, r + 1)))
                steps.append(step("REWRITE",
                                  f"{r}! = " +
                                  "·".join(str(f) for f in range(1, r + 1))))
                steps += r_fact_steps
                value = numer // rfact
                steps.append(step("D", numer, rfact, value))
                problem = (f"In how many ways can a committee of {r} "
                           f"be chosen from a group of {n}? The people "
                           f"are labeled p_{start} through "
                           f"p_{start + n - 1}.")
                model = "C(n, r) = P(n, r)/r!"
            answer = str(value)
        steps.append(step("Z", answer))

        result = dict(
            problem_id=jid(),
            operation=f"permutation_combination_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
        if variant != "word":
            return result
        modifier = self.modifier or random.choice(self.MODIFIERS)
        used = [f"n = {n}", f"r = {r}"]
        return apply_applied_modifier(result, modifier, used, Fraction(value), model, renderer=str)
