"""Compute standard operations on finite relations from pair rosters.

Variants:
- ``inverse`` reverses every pair of ``R ⊆ A × B``.
- ``composition`` computes ``S ∘ R`` for ``R ⊆ A × B``, ``S ⊆ B × C``.
- ``matrix`` writes the 0/1 incidence matrix in the stated row/column order.
- ``domain_range`` extracts the first- and second-coordinate sets.
- ``restriction`` keeps pairs whose first coordinate lies in a stated subset.

Op-codes:
- ``REL_SETUP``: define carriers, relations, and requested operation.
- ``INVERSE_PAIR`` / ``COMPOSE_PAIR``: derive resulting ordered pairs.
- ``MATRIX_ROW``: emit one row of the 0/1 relation matrix.
- ``DOMAIN`` / ``RANGE``: emit coordinate projections.
- ``RESTRICT_CHECK``: test a pair against the restricted domain.
- ``Z``: exact canonical pair roster, matrix, or composite projection answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import (compose, domain_of, inverse_relation, matrix_rows,
                        relation_text, restrict, roster, range_of)


FOUNDATIONS = True


LETTERS = tuple("abcdefghijklmnopqrstuv")
NUMBERS = tuple(range(1, 31))
UPPER = tuple("CDEGHJKLMNPQRSTVWXYZ")

QUERIES = {
    "inverse": (
        "Compute the inverse relation R⁻¹.",
        "Reverse every ordered pair and give the canonical relation roster.",
        "Find R⁻¹ as a subset of B × A.",
        "Swap the coordinates of all pairs in R.",
        "Construct the complete inverse of the finite relation.",
    ),
    "composition": (
        "Compute S ∘ R.",
        "Follow every matching middle coordinate to compose the relations.",
        "Find all pairs (a, c) connected through some b ∈ B.",
        "Compose R first and S second, then give the canonical roster.",
        "Construct the finite relation S ∘ R.",
    ),
    "matrix": (
        "Write the 0/1 matrix of R in the stated A-row, B-column order.",
        "Convert the pair roster into its incidence matrix.",
        "Give one binary row for each element of A.",
        "Record 1 exactly where the ordered pair belongs to R.",
        "Find the matrix representation of the relation.",
    ),
    "domain_range": (
        "Find the domain and range of R.",
        "List all first coordinates and all second coordinates that occur.",
        "Compute both coordinate projections of the relation.",
        "Extract dom(R) and ran(R) from the pair roster.",
        "Give the finite domain and range in canonical roster form.",
    ),
    "restriction": (
        "Restrict R to inputs in D.",
        "Keep exactly the pairs whose first coordinate lies in D.",
        "Compute the domain restriction R↾D.",
        "Filter the relation by the stated subset of A.",
        "Give the restricted relation as a canonical pair roster.",
    ),
}


def random_set(pool, low=2, high=5):
    size = random.randint(low, high)
    return tuple(sorted(random.sample(pool, size)))


def random_relation(left, right):
    pairs = [(first, second) for first in left for second in right]
    count = random.randint(1, max(1, len(pairs) - 1))
    return frozenset(random.sample(pairs, count))


class RelationOperationsGenerator(ProblemGenerator):
    """Generate exact relation operations on hand-sized finite carriers."""

    VARIANTS = ("inverse", "composition", "matrix", "domain_range",
                "restriction")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _binary_relation(self, variant):
        left, right = random_set(LETTERS), random_set(NUMBERS)
        relation = random_relation(left, right)
        base = (f"A = {roster(left)}. B = {roster(right)}. "
                f"R = {relation_text(relation)}.")
        steps = [step("REL_SETUP", f"A = {roster(left)}",
                      f"B = {roster(right)}", f"R = {relation_text(relation)}")]
        if variant == "inverse":
            result = inverse_relation(relation)
            for first, second in sorted(relation):
                steps.append(step("INVERSE_PAIR", f"({first}, {second})",
                                  f"({second}, {first})"))
            answer = relation_text(result)
            problem = f"{base} {random.choice(QUERIES[variant])}"
        elif variant == "matrix":
            rows = matrix_rows(relation, left, right)
            for label, row in zip(left, rows):
                steps.append(step("MATRIX_ROW", label, row))
            answer = "; ".join(rows)
            problem = f"{base} {random.choice(QUERIES[variant])}"
        elif variant == "domain_range":
            domain, range_values = domain_of(relation), range_of(relation)
            steps.append(step("DOMAIN", roster(domain)))
            steps.append(step("RANGE", roster(range_values)))
            answer = f"domain = {roster(domain)}; range = {roster(range_values)}"
            problem = f"{base} {random.choice(QUERIES[variant])}"
        else:
            subset = frozenset(random.sample(left, random.randint(1, len(left))))
            result = restrict(relation, subset)
            problem = (f"{base} D = {roster(subset)}. "
                       f"{random.choice(QUERIES[variant])}")
            steps.append(step("REL_SETUP", f"D = {roster(subset)}",
                              "restrict first coordinate"))
            for first, second in sorted(relation):
                keep = first in subset
                steps.append(step("RESTRICT_CHECK", f"({first}, {second})",
                                  f"{first} in D={'yes' if keep else 'no'}",
                                  "keep" if keep else "skip"))
            answer = relation_text(result)
        return problem, steps, answer

    def _composition(self):
        left, middle, right = (random_set(LETTERS, 2, 4),
                               random_set(NUMBERS, 2, 4),
                               random_set(UPPER, 2, 4))
        while True:
            first = random_relation(left, middle)
            second = random_relation(middle, right)
            result = compose(first, second)
            if result:
                break
        problem = (f"A = {roster(left)}. B = {roster(middle)}. "
                   f"C = {roster(right)}. R = {relation_text(first)}. "
                   f"S = {relation_text(second)}. "
                   f"{random.choice(QUERIES['composition'])}")
        steps = [step("REL_SETUP", f"A = {roster(left)}",
                      f"B = {roster(middle)}", f"C = {roster(right)}"),
                 step("REL_SETUP", f"R = {relation_text(first)}",
                      f"S = {relation_text(second)}", "S ∘ R")]
        for first_left, shared in sorted(first):
            for second_left, last in sorted(second):
                if shared == second_left:
                    steps.append(step("COMPOSE_PAIR",
                                      f"({first_left}, {shared})",
                                      f"({second_left}, {last})",
                                      f"({first_left}, {last})"))
        return problem, steps, relation_text(result)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "composition":
            problem, steps, answer = self._composition()
        else:
            problem, steps, answer = self._binary_relation(variant)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"relation_operations_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
