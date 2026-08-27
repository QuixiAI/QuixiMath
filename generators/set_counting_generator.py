"""Count finite sets, maps, relations, and partitions exactly.

Variants:
- ``subsets``, ``k_subsets``, ``subsets_containing``.
- ``functions``, ``injections``, ``bijections``.
- ``relations``, ``reflexive_relations``, ``symmetric_relations``.
- ``partitions`` (Bell numbers through six elements).

Op-codes:
- ``COUNT_RULE``: state the counting family and exact formula.
- ``A`` / ``S`` / ``M`` / ``D`` / ``E``: expose integer arithmetic.
- ``STIRLING_CELL``: construct one Stirling number of the second kind.
- ``BELL_ROW``: show a complete Stirling row and its Bell-number sum.
- ``Z``: exact integer count.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


LETTERS = tuple("abcdefghijklmnopqrstuvwxyz")
NUMBERS = tuple(range(1, 31))

QUERIES = {
    "subsets": (
        "How many subsets does A have?",
        "Count every possible subset of A, including ∅ and A.",
        "Find card(P(A)).",
        "How many choices of elements form a subset of A?",
        "Use the independent include-or-exclude choices to count the subsets.",
    ),
    "k_subsets": (
        "How many k-element subsets of A are there?",
        "Count the subsets of A having exactly k elements.",
        "Evaluate C(card(A), k).",
        "How many unordered selections of k distinct elements can be made?",
        "Use the binomial coefficient to count the requested subsets.",
    ),
    "subsets_containing": (
        "How many subsets of A contain every element of R?",
        "Count the subsets that include the required set R.",
        "Fix all elements of R and count the remaining subset choices.",
        "How many subsets S satisfy R ⊆ S ⊆ A?",
        "Count the supersets of R that remain inside A.",
    ),
    "functions": (
        "How many functions are there from A to B?",
        "Count all maps A → B.",
        "Give the number of assignments of one B-value to each A-element.",
        "Use card(B)^card(A) to count the functions.",
        "How many total functions have domain A and codomain B?",
    ),
    "injections": (
        "How many injective functions are there from A to B?",
        "Count the one-to-one maps A → B.",
        "Assign distinct codomain values to every domain element.",
        "Use the falling factorial to count injections from A into B.",
        "How many functions A → B never repeat an output?",
    ),
    "bijections": (
        "How many bijections are there from A to B?",
        "Count the one-to-one and onto maps A → B.",
        "How many perfect pairings of A with B are possible?",
        "Use a factorial to count the bijections between these equal-size sets.",
        "How many invertible functions have domain A and codomain B?",
    ),
    "relations": (
        "How many binary relations from A to B are possible?",
        "Count all subsets of A × B.",
        "How many relations R ⊆ A × B can be formed?",
        "Choose independently whether each ordered pair belongs to a relation.",
        "Find the total number of relations between A and B.",
    ),
    "reflexive_relations": (
        "How many reflexive relations on A are possible?",
        "Count relations on A that contain every diagonal pair.",
        "Fix the required loops and choose all other ordered pairs freely.",
        "How many R ⊆ A × A satisfy aRa for every a ∈ A?",
        "Find the number of reflexive binary relations on A.",
    ),
    "symmetric_relations": (
        "How many symmetric relations on A are possible?",
        "Count relations where each off-diagonal pair is chosen with its reverse.",
        "Choose the diagonal entries and unordered off-diagonal pairs.",
        "How many R on A satisfy aRb exactly when bRa?",
        "Find the number of symmetric binary relations on A.",
    ),
    "partitions": (
        "How many set partitions does A have?",
        "Count the ways to divide A into nonempty unlabeled blocks.",
        "Find the Bell number for card(A).",
        "Use Stirling rows to count all partitions of A.",
        "How many equivalence-class decompositions of A are possible?",
    ),
}


def random_letter_set(min_size=1, max_size=8):
    size = random.randint(min_size, max_size)
    return tuple(sorted(random.sample(LETTERS, size)))


def random_number_set(min_size=1, max_size=8):
    size = random.randint(min_size, max_size)
    return tuple(sorted(random.sample(NUMBERS, size)))


def multiplication_chain(factors):
    steps = []
    running = 1
    for factor in factors:
        result = running * factor
        steps.append(step("M", running, factor, result))
        running = result
    return steps, running


def stirling_rows(n):
    rows = [[1]]
    for size in range(1, n + 1):
        prior = rows[-1]
        row = [0] * (size + 1)
        for blocks in range(1, size + 1):
            same = prior[blocks] if blocks < len(prior) else 0
            new = prior[blocks - 1]
            row[blocks] = blocks * same + new
        rows.append(row)
    return rows


class SetCountingGenerator(ProblemGenerator):
    """Generate exact finite combinatorics with explicit arithmetic chains."""

    VARIANTS = ("subsets", "k_subsets", "subsets_containing", "functions",
                "injections", "bijections", "relations",
                "reflexive_relations", "symmetric_relations", "partitions")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _subsets(self, variant):
        values = random_letter_set(2 if variant != "subsets" else 1, 8)
        size = len(values)
        if variant == "subsets":
            problem = f"A = {roster(values)}. {random.choice(QUERIES[variant])}"
            answer = 2 ** size
            steps = [step("COUNT_RULE", "subsets", "2^card(A)"),
                     step("E", 2, size, answer)]
        elif variant == "k_subsets":
            chosen = random.randint(1, size - 1)
            problem = (f"A = {roster(values)}. k = {chosen}. "
                       f"{random.choice(QUERIES[variant])}")
            numerator_steps, numerator = multiplication_chain(
                range(size, size - chosen, -1))
            denominator_steps, denominator = multiplication_chain(
                range(1, chosen + 1))
            answer = numerator // denominator
            steps = [step("COUNT_RULE", "k-subsets",
                          "C(n,k) = n(n−1)…(n−k+1)/k!")]
            steps.extend(numerator_steps)
            steps.extend(denominator_steps)
            steps.append(step("D", numerator, denominator, answer))
        else:
            required_size = random.randint(1, size - 1)
            required = tuple(sorted(random.sample(values, required_size)))
            free = size - required_size
            answer = 2 ** free
            problem = (f"A = {roster(values)}. R = {roster(required)}. "
                       f"{random.choice(QUERIES[variant])}")
            steps = [step("COUNT_RULE", "subsets containing R",
                          "2^(card(A)−card(R))"),
                     step("S", size, required_size, free),
                     step("E", 2, free, answer)]
        return problem, steps, answer

    def _maps(self, variant):
        if variant == "bijections":
            domain = random_letter_set(1, 8)
            codomain = tuple(sorted(random.sample(NUMBERS, len(domain))))
        elif variant == "injections":
            domain = random_letter_set(1, 7)
            codomain = random_number_set(len(domain), 10)
        else:
            domain = random_letter_set(1, 8)
            codomain = random_number_set(1, 8)
        m, n = len(domain), len(codomain)
        problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                   f"{random.choice(QUERIES[variant])}")
        if variant == "functions":
            answer = n ** m
            steps = [step("COUNT_RULE", "functions", "card(B)^card(A)"),
                     step("E", n, m, answer)]
        elif variant == "injections":
            chain, answer = multiplication_chain(range(n, n - m, -1))
            steps = [step("COUNT_RULE", "injections",
                          "card(B)(card(B)−1)…(card(B)−card(A)+1)")]
            steps.extend(chain)
        else:
            chain, answer = multiplication_chain(range(1, m + 1))
            steps = [step("COUNT_RULE", "bijections", "card(A)!")]
            steps.extend(chain)
        return problem, steps, answer

    def _relations(self, variant):
        domain = random_letter_set(1, 6 if variant == "relations" else 8)
        m = len(domain)
        if variant == "relations":
            codomain = random_number_set(1, 6)
            n = len(codomain)
            problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                       f"{random.choice(QUERIES[variant])}")
            exponent = m * n
            answer = 2 ** exponent
            steps = [step("COUNT_RULE", "relations", "2^(card(A)·card(B))"),
                     step("M", m, n, exponent), step("E", 2, exponent, answer)]
        elif variant == "reflexive_relations":
            problem = f"A = {roster(domain)}. {random.choice(QUERIES[variant])}"
            square = m * m
            exponent = square - m
            answer = 2 ** exponent
            steps = [step("COUNT_RULE", "reflexive relations",
                          "2^(card(A)^2−card(A))"),
                     step("E", m, 2, square), step("S", square, m, exponent),
                     step("E", 2, exponent, answer)]
        else:
            problem = f"A = {roster(domain)}. {random.choice(QUERIES[variant])}"
            plus_one = m + 1
            product = m * plus_one
            exponent = product // 2
            answer = 2 ** exponent
            steps = [step("COUNT_RULE", "symmetric relations",
                          "2^(card(A)(card(A)+1)/2)"),
                     step("A", m, 1, plus_one), step("M", m, plus_one, product),
                     step("D", product, 2, exponent), step("E", 2, exponent, answer)]
        return problem, steps, answer

    def _partitions(self):
        values = random_letter_set(1, 6)
        size = len(values)
        rows = stirling_rows(size)
        problem = f"A = {roster(values)}. {random.choice(QUERIES['partitions'])}"
        steps = [step("COUNT_RULE", "partitions", "Bell(card(A))")]
        for current in range(1, size + 1):
            row = rows[current]
            prior = rows[current - 1]
            for blocks in range(1, current + 1):
                same = prior[blocks] if blocks < len(prior) else 0
                new = prior[blocks - 1]
                steps.append(step(
                    "STIRLING_CELL", f"S({current},{blocks})",
                    f"{blocks}×{same}+{new}", row[blocks]))
            bell = sum(row)
            steps.append(step("BELL_ROW", f"n={current}",
                              " ".join(str(value) for value in row[1:]), bell))
        return problem, steps, sum(rows[size])

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("subsets", "k_subsets", "subsets_containing"):
            problem, steps, answer = self._subsets(variant)
        elif variant in ("functions", "injections", "bijections"):
            problem, steps, answer = self._maps(variant)
        elif variant in ("relations", "reflexive_relations",
                         "symmetric_relations"):
            problem, steps, answer = self._relations(variant)
        else:
            problem, steps, answer = self._partitions()
        answer_text = str(answer)
        steps.append(step("Z", answer_text))
        return {
            "problem_id": jid(),
            "operation": f"set_counting_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer_text,
        }
