"""Find the first counterexample under an explicitly stated scan order.

Variants:
- ``arithmetic_claim`` scans multiples for a false divisibility implication.
- ``algebraic_claim`` scans an integer polynomial claimed always to be prime.
- ``set_claim`` enumerates subset pairs for a false set identity.

Every instance is retained only when its first counterexample occurs within
12 trials.  Five phrasings and parameterized claims provide more than 100,000
problem texts.

Op-codes:
- ``TRY`` / ``REJECT`` / ``ACCEPT``: walk the stated candidate order.
- ``DIV_CHECK`` / ``M`` / ``A``: expose arithmetic tests.
- ``SET_SIDE``: evaluate one side of a proposed set identity.
- ``COUNTEREXAMPLE``: record the first failing candidate and witness.
- ``Z``: exact composite counterexample answer.
"""
import itertools
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


QUERIES = {
    "arithmetic_claim": (
        "Find the first counterexample in the stated scan order.",
        "Test eligible multiples from least to greatest and stop at the first failure.",
        "Refute the universal divisibility claim with its smallest scanned witness.",
        "Search the listed domain in order for the earliest counterexample.",
        "Give the first multiple that makes the implication false.",
    ),
    "algebraic_claim": (
        "Find the first counterexample among n = L, L+1, and so on.",
        "Evaluate consecutive inputs and stop at the first composite output.",
        "Refute the prime-value claim with the earliest scanned n.",
        "Search upward from the lower bound for the first failure.",
        "Give the smallest n in the stated scan whose polynomial value is composite.",
    ),
    "set_claim": (
        "Find the first counterexample in the stated subset-pair order.",
        "Enumerate pairs until the two sides first differ.",
        "Refute the set identity with the earliest ordered pair of subsets.",
        "Search the canonical subset-pair order for a failing witness.",
        "Give the first A and B for which the proposed identity is false.",
    ),
}


def first_factor(value):
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return divisor
    return None


def subsets(values):
    result = []
    for size in range(len(values) + 1):
        result.extend(frozenset(combo) for combo in itertools.combinations(values, size))
    return result


class CounterexampleSearchGenerator(ProblemGenerator):
    """Generate bounded searches whose answer is forced by the problem text."""

    VARIANTS = ("arithmetic_claim", "algebraic_claim", "set_claim")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _arithmetic(self):
        while True:
            divisor_a, divisor_b = random.sample(range(2, 16), 2)
            if divisor_a % divisor_b != 0:
                break
        lower = random.randint(1, 999)
        first_multiple = ((lower + divisor_a - 1) // divisor_a) * divisor_a
        candidates = [first_multiple + index * divisor_a for index in range(12)]
        counterexample = next(value for value in candidates
                              if value % divisor_b != 0)
        problem = (
            f"Claim: every multiple n of {divisor_a} with n ≥ {lower} is also "
            f"divisible by {divisor_b}. Scan eligible multiples in increasing order. "
            f"{random.choice(QUERIES['arithmetic_claim'])}"
        )
        steps = []
        for value in candidates:
            remainder = value % divisor_b
            steps.append(step("DIV_CHECK", value, divisor_b,
                              f"quotient {value // divisor_b}, remainder {remainder}"))
            failed = remainder != 0
            steps.append(step("TRY", f"n = {value}",
                              "claim fails" if failed else "claim holds"))
            if failed:
                steps.append(step("ACCEPT", f"n = {value}", "counterexample"))
                break
            steps.append(step("REJECT", f"n = {value}", "not a counterexample"))
        witness = (f"{counterexample} is divisible by {divisor_a} but not by "
                   f"{divisor_b}")
        steps.append(step("COUNTEREXAMPLE", f"n = {counterexample}", witness))
        answer = f"n = {counterexample} ({witness})"
        return problem, steps, answer

    def _algebraic(self):
        while True:
            lower = random.randint(0, 30)
            coefficient = random.randint(1, 12)
            constant = random.randint(2, 80)
            rows = []
            for value in range(lower, lower + 12):
                output = value * value + coefficient * value + constant
                factor = first_factor(output)
                rows.append((value, output, factor))
                if factor is not None:
                    break
            if rows[-1][2] is not None:
                break
        problem = (
            f"Claim: for every integer n ≥ {lower}, n^2 + {coefficient}n + "
            f"{constant} is prime. "
            f"Scan consecutive integers in increasing order. "
            f"{random.choice(QUERIES['algebraic_claim'])}"
        )
        steps = []
        for value, output, factor in rows:
            square = value * value
            linear = coefficient * value
            partial = square + linear
            steps.extend((step("M", value, value, square),
                          step("M", coefficient, value, linear),
                          step("A", square, linear, partial),
                          step("A", partial, constant, output)))
            trial_divisors = [divisor for divisor in range(2, math.isqrt(output) + 1)
                              if first_factor(divisor) is None]
            for divisor in trial_divisors:
                steps.append(step("DIV_CHECK", output, divisor,
                                  f"remainder {output % divisor}"))
                if output % divisor == 0:
                    break
            failed = factor is not None
            steps.append(step("TRY", f"n = {value}",
                              "claim fails" if failed else "claim holds"))
            if failed:
                steps.append(step("ACCEPT", f"n = {value}", "counterexample"))
                break
            steps.append(step("REJECT", f"n = {value}", "not a counterexample"))
        value, output, factor = rows[-1]
        quotient = output // factor
        witness = f"{output} = {factor} × {quotient}"
        steps.append(step("COUNTEREXAMPLE", f"n = {value}", witness))
        answer = f"n = {value} ({witness})"
        return problem, steps, answer

    @staticmethod
    def _set_sides(kind, values_a, values_b):
        if kind == "difference_commutes":
            return values_a - values_b, values_b - values_a
        if kind == "union_equals_intersection":
            return values_a | values_b, values_a & values_b
        return values_a ^ values_b, values_a | values_b

    def _set(self):
        kind = random.choice(("difference_commutes", "union_equals_intersection",
                              "symdiff_equals_union"))
        size = random.randint(2, 3 if kind == "symdiff_equals_union" else 5)
        universe = tuple(sorted(random.sample(range(1, 201), size)))
        claim_text = {
            "difference_commutes": "A − B = B − A",
            "union_equals_intersection": "A ∪ B = A ∩ B",
            "symdiff_equals_union": "A Δ B = A ∪ B",
        }[kind]
        ordered_subsets = subsets(universe)
        rows = []
        for values_a in ordered_subsets:
            for values_b in ordered_subsets:
                left, right = self._set_sides(kind, values_a, values_b)
                rows.append((values_a, values_b, left, right))
                if left != right:
                    break
            if rows[-1][2] != rows[-1][3]:
                break
        if len(rows) > 12:
            raise AssertionError("set counterexample exceeded the 12-trial bound")
        problem = (
            f"Universe U = {roster(universe)}. Claim: for all subsets A and B of U, "
            f"{claim_text}. Enumerate subsets by size then lexicographically; "
            f"enumerate A first, then B. {random.choice(QUERIES['set_claim'])}"
        )
        steps = []
        for values_a, values_b, left, right in rows:
            steps.extend((step("SET_SIDE", "left", roster(left)),
                          step("SET_SIDE", "right", roster(right))))
            failed = left != right
            steps.append(step("TRY", f"A = {roster(values_a)}",
                              f"B = {roster(values_b)}",
                              "claim fails" if failed else "claim holds"))
            if failed:
                steps.append(step("ACCEPT", "subset pair", "counterexample"))
                break
            steps.append(step("REJECT", "subset pair", "not a counterexample"))
        values_a, values_b, left, right = rows[-1]
        witness = (f"A = {roster(values_a)}; B = {roster(values_b)}; "
                   f"left = {roster(left)}; right = {roster(right)}")
        steps.append(step("COUNTEREXAMPLE", "set pair", witness))
        answer = witness
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "arithmetic_claim":
            problem, steps, answer = self._arithmetic()
        elif variant == "algebraic_claim":
            problem, steps, answer = self._algebraic()
        else:
            problem, steps, answer = self._set()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"counterexample_search_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
