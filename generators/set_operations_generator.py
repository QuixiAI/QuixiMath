"""Finite set algebra, power sets, products, complements, and rewrites.

Variants:
- ``algebra``: union, intersection, and difference over letter sets.
- ``power_set``: list every subset of a 2–4 element set.
- ``cartesian_product``: list all ordered pairs.
- ``complement``: compute Aᶜ inside a stated finite universe.
- ``symmetric_difference``: compute A Δ B.
- ``integer_elements``: perform one set operation on integer rosters.
- ``two_step``: evaluate a nested expression inside-out.

The expanded element banks and five phrasings yield more than 100,000
problem texts while retaining hand-sized sets.

Op-codes:
- ``SET_SETUP``: define the input sets and requested operation.
- ``ELEMENT_SCAN``: make an element-by-element membership decision.
- ``SUBEXPR`` / ``REWRITE``: evaluate and replace one inner expression.
- ``SUBSET_SIZE`` / ``POWER_SET_RESULT``: construct a power set by size.
- ``CART_PAIR`` / ``CARTESIAN_RESULT``: construct an ordered-pair roster.
- ``COUNT`` / ``M`` / ``E``: expose cardinality arithmetic.
- ``Z``: exact canonical set result.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import pair_roster, roster


FOUNDATIONS = True


LETTERS = list("abcdefghijklmnopqrst")
DIGITS = list(range(1, 21))

QUERIES = {
    "algebra": ("Evaluate the stated set operation.",
                "Scan the elements and give the resulting roster.",
                "Compute the requested combination of A and B.",
                "Use membership tests to find the result set.",
                "Write the operation's value in canonical roster form."),
    "power_set": ("Find the power set P(S).",
                  "List every subset of S, grouped by size.",
                  "Construct P(S) from the empty subset through S itself.",
                  "Enumerate all subsets and give the power set.",
                  "Use the subset sizes to write P(S)."),
    "cartesian_product": ("Find A × B.",
                          "List every ordered pair in the Cartesian product.",
                          "Pair each element of A with every element of B.",
                          "Construct the complete ordered-pair roster A × B.",
                          "Compute the Cartesian product and its pairs."),
    "complement": ("Find Aᶜ relative to U.",
                   "List the universe elements that are not in A.",
                   "Compute the complement of A in the stated universe.",
                   "Scan U and write Aᶜ as a roster.",
                   "Remove A from U to obtain the complement."),
    "symmetric_difference": ("Find A Δ B.",
                             "List the elements that belong to exactly one of A and B.",
                             "Compute the symmetric difference.",
                             "Keep elements in A or B but not both.",
                             "Use membership scans to write A Δ B."),
    "integer_elements": ("Evaluate the stated integer-set operation.",
                         "Compute the result and write a sorted integer roster.",
                         "Test the integer memberships for the requested operation.",
                         "Find the value of the displayed set combination.",
                         "Apply the operation to A and B."),
    "two_step": ("Evaluate the set expression inside-out.",
                 "Compute the inner operation, rewrite, then finish.",
                 "Show the intermediate roster and find the final set.",
                 "Follow the parentheses to evaluate the two-step expression.",
                 "Reduce one subexpression at a time."),
}


def fmt_set(values):
    return roster(values)


def ordered(values, universe):
    return [value for value in universe if value in values]


def subsets(values):
    return [list(combo) for size in range(len(values) + 1)
            for combo in itertools.combinations(values, size)]


def fmt_power_set(values):
    return "{" + ", ".join(fmt_set(subset) for subset in subsets(values)) + "}"


def fmt_pairs(values_a, values_b):
    return pair_roster((a, b) for a in values_a for b in values_b)


class SetOperationsGenerator(ProblemGenerator):
    """Generate complete finite-set scratchpads in the shared set dialect."""

    VARIANTS = ("algebra", "power_set", "cartesian_product", "complement",
                "symmetric_difference", "integer_elements", "two_step")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _subset(pool, min_size=1, max_size=6):
        size = random.randint(min_size, max_size)
        return sorted(random.sample(pool, size), key=pool.index)

    @staticmethod
    def _scan_steps(candidates, values_a, values_b, result):
        steps = []
        for element in candidates:
            steps.append(step("ELEMENT_SCAN", element,
                              f"in A={'yes' if element in values_a else 'no'}, "
                              f"in B={'yes' if element in values_b else 'no'}",
                              "keep" if element in result else "skip"))
        return steps

    def _algebra(self, integer=False):
        if integer:
            pool = list(range(-30, 31))
            values_a = sorted(random.sample(pool, random.randint(3, 8)))
            values_b = sorted(random.sample(pool, random.randint(3, 8)))
        else:
            pool = LETTERS
            values_a = self._subset(pool)
            values_b = self._subset(pool)
        operation = random.choice(("union", "intersection", "difference"))
        if operation == "union":
            result_set, symbol = set(values_a) | set(values_b), "∪"
        elif operation == "intersection":
            result_set, symbol = set(values_a) & set(values_b), "∩"
        else:
            result_set, symbol = set(values_a) - set(values_b), "−"
        candidates = sorted(set(values_a) | set(values_b),
                            key=(None if integer else pool.index))
        result = ordered(result_set, candidates)
        variant = "integer_elements" if integer else "algebra"
        problem = (f"A = {fmt_set(values_a)}. B = {fmt_set(values_b)}. "
                   f"Operation: A {symbol} B. {random.choice(QUERIES[variant])}")
        steps = [step("SET_SETUP", f"A = {fmt_set(values_a)}",
                      f"B = {fmt_set(values_b)}", f"A {symbol} B")]
        steps.extend(self._scan_steps(candidates, values_a, values_b, result))
        steps.append(step("COUNT", "result size", len(result)))
        return problem, steps, fmt_set(result)

    def _power_set(self):
        values = self._subset(LETTERS, 2, 4)
        all_subsets = subsets(values)
        problem = f"S = {fmt_set(values)}. {random.choice(QUERIES['power_set'])}"
        steps = [step("SET_SETUP", f"S = {fmt_set(values)}", "power set"),
                 step("E", 2, len(values), len(all_subsets))]
        for size in range(len(values) + 1):
            group = [fmt_set(subset) for subset in all_subsets if len(subset) == size]
            steps.append(step("SUBSET_SIZE", size, ", ".join(group)))
        result = fmt_power_set(values)
        steps.append(step("POWER_SET_RESULT", result))
        return problem, steps, f"P(S) = {result}"

    def _cartesian(self):
        values_a = self._subset(LETTERS, 1, 3)
        values_b = self._subset(DIGITS, 1, 3)
        problem = (f"A = {fmt_set(values_a)}. B = {fmt_set(values_b)}. "
                   f"{random.choice(QUERIES['cartesian_product'])}")
        result = fmt_pairs(values_a, values_b)
        steps = [step("SET_SETUP", f"A = {fmt_set(values_a)}",
                      f"B = {fmt_set(values_b)}", "A × B"),
                 step("M", len(values_a), len(values_b),
                      len(values_a) * len(values_b))]
        for first in values_a:
            for second in values_b:
                steps.append(step("CART_PAIR", first, second,
                                  f"({first}, {second})"))
        steps.append(step("CARTESIAN_RESULT", result))
        return problem, steps, f"A × B = {result}"

    def _complement(self):
        high = random.randint(8, 30)
        universe = list(range(1, high + 1))
        values_a = sorted(random.sample(universe, random.randint(2, high - 2)))
        result = [value for value in universe if value not in values_a]
        problem = (f"U = {fmt_set(universe)}. A = {fmt_set(values_a)}. "
                   f"{random.choice(QUERIES['complement'])}")
        steps = [step("SET_SETUP", f"U = {fmt_set(universe)}",
                      f"A = {fmt_set(values_a)}", "Aᶜ")]
        for value in universe:
            steps.append(step("ELEMENT_SCAN", value,
                              f"in A={'yes' if value in values_a else 'no'}",
                              "skip" if value in values_a else "keep"))
        steps.append(step("COUNT", "result size", len(result)))
        return problem, steps, fmt_set(result)

    def _symmetric_difference(self):
        values_a = self._subset(LETTERS)
        values_b = self._subset(LETTERS)
        candidates = ordered(set(values_a) | set(values_b), LETTERS)
        result = ordered(set(values_a) ^ set(values_b), LETTERS)
        problem = (f"A = {fmt_set(values_a)}. B = {fmt_set(values_b)}. "
                   f"{random.choice(QUERIES['symmetric_difference'])}")
        steps = [step("SET_SETUP", f"A = {fmt_set(values_a)}",
                      f"B = {fmt_set(values_b)}", "A Δ B")]
        steps.extend(self._scan_steps(candidates, values_a, values_b, result))
        steps.append(step("COUNT", "result size", len(result)))
        return problem, steps, fmt_set(result)

    def _two_step(self):
        pool = list(range(1, 41))
        values_a = sorted(random.sample(pool, random.randint(3, 7)))
        values_b = sorted(random.sample(pool, random.randint(3, 7)))
        values_c = sorted(random.sample(pool, random.randint(3, 7)))
        form = random.choice(("(A ∪ B) − C", "(A ∩ B) ∪ C",
                              "A Δ (B − C)", "(A − B) ∩ C"))
        if form == "(A ∪ B) − C":
            inner_label, inner = "A ∪ B", set(values_a) | set(values_b)
            result, rewritten = inner - set(values_c), f"{fmt_set(inner)} − C"
        elif form == "(A ∩ B) ∪ C":
            inner_label, inner = "A ∩ B", set(values_a) & set(values_b)
            result, rewritten = inner | set(values_c), f"{fmt_set(inner)} ∪ C"
        elif form == "A Δ (B − C)":
            inner_label, inner = "B − C", set(values_b) - set(values_c)
            result, rewritten = set(values_a) ^ inner, f"A Δ {fmt_set(inner)}"
        else:
            inner_label, inner = "A − B", set(values_a) - set(values_b)
            result, rewritten = inner & set(values_c), f"{fmt_set(inner)} ∩ C"
        result_values = sorted(result)
        problem = (f"A = {fmt_set(values_a)}. B = {fmt_set(values_b)}. "
                   f"C = {fmt_set(values_c)}. Expression: {form}. "
                   f"{random.choice(QUERIES['two_step'])}")
        steps = [step("SET_SETUP", f"A = {fmt_set(values_a)}",
                      f"B = {fmt_set(values_b)}", f"C = {fmt_set(values_c)}"),
                 step("SUBEXPR", inner_label, fmt_set(inner)),
                 step("REWRITE", rewritten),
                 step("SUBEXPR", form, fmt_set(result_values)),
                 step("REWRITE", fmt_set(result_values)),
                 step("COUNT", "result size", len(result_values))]
        return problem, steps, fmt_set(result_values)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "algebra":
            problem, steps, answer = self._algebra()
        elif variant == "power_set":
            problem, steps, answer = self._power_set()
        elif variant == "cartesian_product":
            problem, steps, answer = self._cartesian()
        elif variant == "complement":
            problem, steps, answer = self._complement()
        elif variant == "symmetric_difference":
            problem, steps, answer = self._symmetric_difference()
        elif variant == "integer_elements":
            problem, steps, answer = self._algebra(integer=True)
        else:
            problem, steps, answer = self._two_step()
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"set_operations_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
