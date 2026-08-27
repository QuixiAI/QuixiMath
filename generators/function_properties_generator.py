"""Analyze finite functions presented as complete mapping tables.

Variants:
- ``classify``: injective, surjective, and bijective with first witnesses.
- ``image_preimage``: compute ``f(S)`` and ``f⁻¹(T)``.
- ``compose_tables``: construct ``g ∘ f`` from two tables.
- ``inverse_table``: reverse a bijective table.
- ``fixed_points``: list every ``x`` satisfying ``f(x) = x``.
- ``count_by_property``: count injections, surjections, or bijections.

Op-codes:
- ``MAP``: record one table entry.
- ``COLLISION`` / ``NO_COLLISION``: give the first injectivity witness/check.
- ``MISSED`` / ``NO_MISSED``: give the first surjectivity witness/check.
- ``IMAGE`` / ``PREIMAGE``: expose image and preimage membership.
- ``COMPOSE`` / ``INVERSE_PAIR`` / ``FIXED_CHECK``: derive table results.
- ``COUNT_RULE`` / ``M`` / ``INEX_TERM`` / ``RUNNING_TOTAL``: exact counts.
- ``Z``: exact composite property, roster, table, or integer answer.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import (image, injective_witness, map_text, preimage, roster,
                        surjective_witness)


FOUNDATIONS = True


LETTERS = tuple("abcdefghijklmnopqrstuvwxyz")
UPPER = tuple("CDEGHJKLMNPQRSTVWXYZ")
NUMBERS = tuple(range(1, 31))

QUERIES = {
    "classify": (
        "Classify f as injective, surjective, and bijective.",
        "Use the table to decide all three mapping properties.",
        "Find the first collision or missed value and classify the function.",
        "Determine whether f is one-to-one, onto, or both.",
        "Check injectivity and surjectivity, then report bijectivity.",
    ),
    "image_preimage": (
        "Compute f(S) and f⁻¹(T).",
        "Find the image of S and the preimage of T from the table.",
        "Map S forward and pull T back through f.",
        "Give both requested finite-set images in canonical roster form.",
        "Use the entries of f to evaluate f(S) and f⁻¹(T).",
    ),
    "compose_tables": (
        "Compute the complete table of g ∘ f.",
        "Apply f first and g second for every element of A.",
        "Compose the two finite mapping tables.",
        "Find x ↦ g(f(x)) for all x ∈ A.",
        "Construct the table of the composite function g ∘ f.",
    ),
    "inverse_table": (
        "Compute the table of f⁻¹.",
        "Reverse this bijection to obtain its inverse function.",
        "Swap every input-output pair and give the inverse table.",
        "Construct f⁻¹ from the one-to-one correspondence.",
        "Give the complete mapping table of the inverse bijection.",
    ),
    "fixed_points": (
        "List all fixed points of f.",
        "Find every x ∈ A for which f(x) = x.",
        "Use the table to solve f(x) = x.",
        "Give the fixed-point set in canonical roster form.",
        "Check each input and list those unchanged by f.",
    ),
    "count_by_property": (
        "Count the functions having the stated property.",
        "Use the finite-set sizes to find the exact number of such maps.",
        "How many functions A → B satisfy the named mapping property?",
        "Evaluate the appropriate falling-factorial or inclusion-exclusion count.",
        "Find the exact number of maps with this property.",
    ),
}


def element_text(value):
    return str(value)


def random_set(pool, size):
    return tuple(sorted(random.sample(pool, size)))


def map_steps(label, table):
    return [step("MAP", element_text(key),
                 f"{label}({element_text(key)}) = {element_text(table[key])}")
            for key in sorted(table, key=lambda item: (isinstance(item, str), item))]


def multiplication_chain(factors):
    steps = []
    running = 1
    for factor in factors:
        result = running * factor
        steps.append(step("M", running, factor, result))
        running = result
    return steps, running


class FunctionPropertiesGenerator(ProblemGenerator):
    """Generate exact finite-function reasoning from printed tables."""

    VARIANTS = ("classify", "image_preimage", "compose_tables",
                "inverse_table", "fixed_points", "count_by_property")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _arbitrary_table(domain, codomain):
        return {key: random.choice(codomain) for key in domain}

    def _classification_table(self):
        mode = random.choice(("bijective", "injective", "surjective", "neither"))
        if mode == "bijective":
            size = random.randint(2, 6)
            domain, codomain = random_set(LETTERS, size), random_set(NUMBERS, size)
            outputs = random.sample(codomain, size)
        elif mode == "injective":
            domain_size = random.randint(2, 5)
            domain = random_set(LETTERS, domain_size)
            codomain = random_set(NUMBERS, domain_size + random.randint(1, 3))
            outputs = random.sample(codomain, domain_size)
        elif mode == "surjective":
            codomain_size = random.randint(2, 5)
            domain = random_set(LETTERS,
                                codomain_size + random.randint(1, 3))
            codomain = random_set(NUMBERS, codomain_size)
            outputs = list(random.sample(codomain, codomain_size))
            outputs.extend(random.choice(codomain)
                           for _ in range(len(domain) - codomain_size))
            random.shuffle(outputs)
        else:
            domain = random_set(LETTERS, random.randint(2, 7))
            codomain = random_set(NUMBERS, random.randint(2, 7))
            available = random.sample(codomain, random.randint(1, len(codomain) - 1))
            outputs = [random.choice(available) for _ in domain]
            outputs[1] = outputs[0]
        return domain, codomain, dict(zip(domain, outputs))

    def _classify(self):
        domain, codomain, table = self._classification_table()
        problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                   f"Table f: {map_text(table)}. "
                   f"{random.choice(QUERIES['classify'])}")
        steps = map_steps("f", table)
        collision = injective_witness(table)
        missed = surjective_witness(table, codomain)
        if collision is None:
            steps.append(step("NO_COLLISION", "all outputs distinct"))
            injective_text = "injective yes"
        else:
            first, second, value = collision
            witness = f"f({first}) = f({second}) = {value}"
            steps.append(step("COLLISION", witness))
            injective_text = f"injective no ({witness})"
        if missed is None:
            steps.append(step("NO_MISSED", "all codomain values hit"))
            surjective_text = "surjective yes"
        else:
            steps.append(step("MISSED", element_text(missed)))
            surjective_text = f"surjective no (misses {missed})"
        bijective = collision is None and missed is None
        answer = (f"{injective_text}; {surjective_text}; "
                  f"bijective {'yes' if bijective else 'no'}")
        return problem, steps, answer

    def _image_preimage(self):
        domain = random_set(LETTERS, random.randint(3, 7))
        codomain = random_set(NUMBERS, random.randint(2, 7))
        table = self._arbitrary_table(domain, codomain)
        subset_s = frozenset(random.sample(domain, random.randint(1, len(domain))))
        subset_t = frozenset(random.sample(codomain, random.randint(1, len(codomain))))
        forward, backward = image(table, subset_s), preimage(table, subset_t)
        problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                   f"Table f: {map_text(table)}. S = {roster(subset_s)}. "
                   f"T = {roster(subset_t)}. "
                   f"{random.choice(QUERIES['image_preimage'])}")
        steps = map_steps("f", table)
        for key in sorted(subset_s):
            steps.append(step("IMAGE", element_text(key),
                              element_text(table[key])))
        for value in sorted(subset_t):
            fiber = frozenset(key for key in domain if table[key] == value)
            steps.append(step("PREIMAGE", element_text(value), roster(fiber)))
        answer = f"f(S) = {roster(forward)}; f⁻¹(T) = {roster(backward)}"
        return problem, steps, answer

    def _compose(self):
        domain = random_set(LETTERS, random.randint(2, 6))
        middle = random_set(NUMBERS, random.randint(2, 6))
        codomain = random_set(UPPER, random.randint(2, 6))
        first = self._arbitrary_table(domain, middle)
        second = self._arbitrary_table(middle, codomain)
        composed = {key: second[first[key]] for key in domain}
        problem = (f"A = {roster(domain)}. B = {roster(middle)}. "
                   f"C = {roster(codomain)}. Table f: {map_text(first)}. "
                   f"Table g: {map_text(second)}. "
                   f"{random.choice(QUERIES['compose_tables'])}")
        steps = map_steps("f", first) + map_steps("g", second)
        for key in domain:
            steps.append(step("COMPOSE", element_text(key),
                              f"f({key}) = {first[key]}",
                              f"g({first[key]}) = {composed[key]}"))
        return problem, steps, f"g ∘ f = {map_text(composed)}"

    def _inverse(self):
        size = random.randint(2, 7)
        domain, codomain = random_set(LETTERS, size), random_set(NUMBERS, size)
        table = dict(zip(domain, random.sample(codomain, size)))
        inverse = {value: key for key, value in table.items()}
        problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                   f"Table f: {map_text(table)}. "
                   f"{random.choice(QUERIES['inverse_table'])}")
        steps = map_steps("f", table)
        steps.append(step("NO_COLLISION", "all outputs distinct"))
        for key in sorted(table):
            steps.append(step("INVERSE_PAIR", f"({key}, {table[key]})",
                              f"({table[key]}, {key})"))
        return problem, steps, f"f⁻¹ = {map_text(inverse)}"

    def _fixed_points(self):
        values = random_set(LETTERS, random.randint(2, 8))
        table = self._arbitrary_table(values, values)
        fixed = frozenset(key for key in values if table[key] == key)
        problem = (f"A = {roster(values)}. Table f: {map_text(table)}. "
                   f"{random.choice(QUERIES['fixed_points'])}")
        steps = map_steps("f", table)
        for key in values:
            steps.append(step("FIXED_CHECK", element_text(key),
                              f"f({key}) = {table[key]}",
                              "fixed" if table[key] == key else "not fixed"))
        return problem, steps, roster(fixed)

    def _count(self):
        prop = random.choice(("injective", "surjective", "bijective"))
        if prop == "injective":
            domain_size = random.randint(1, 5)
            codomain_size = random.randint(domain_size, 6)
        elif prop == "surjective":
            codomain_size = random.randint(1, 4)
            domain_size = random.randint(codomain_size, 6)
        else:
            domain_size = codomain_size = random.randint(1, 6)
        domain = random_set(LETTERS, domain_size)
        codomain = random_set(NUMBERS, codomain_size)
        problem = (f"A = {roster(domain)}. B = {roster(codomain)}. "
                   f"Property: {prop}. "
                   f"{random.choice(QUERIES['count_by_property'])}")
        if prop == "injective":
            chain, answer = multiplication_chain(
                range(codomain_size, codomain_size - domain_size, -1))
            steps = [step("COUNT_RULE", "injective",
                          "card(B)!/(card(B)−card(A))!")]
            steps.extend(chain)
        elif prop == "bijective":
            chain, answer = multiplication_chain(range(1, domain_size + 1))
            steps = [step("COUNT_RULE", "bijective", "card(A)!")]
            steps.extend(chain)
        else:
            steps = [step("COUNT_RULE", "surjective",
                          "Σ(−1)^i C(card(B),i)(card(B)−i)^card(A)")]
            running = 0
            for index in range(codomain_size + 1):
                magnitude = (math.comb(codomain_size, index)
                             * (codomain_size - index) ** domain_size)
                signed = magnitude if index % 2 == 0 else -magnitude
                steps.append(step("INEX_TERM", index,
                                  f"{math.comb(codomain_size, index)}×"
                                  f"{codomain_size - index}^{domain_size}",
                                  signed))
                new_total = running + signed
                steps.append(step("RUNNING_TOTAL", running, signed, new_total))
                running = new_total
            answer = running
        return problem, steps, str(answer)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "classify":
            problem, steps, answer = self._classify()
        elif variant == "image_preimage":
            problem, steps, answer = self._image_preimage()
        elif variant == "compose_tables":
            problem, steps, answer = self._compose()
        elif variant == "inverse_table":
            problem, steps, answer = self._inverse()
        elif variant == "fixed_points":
            problem, steps, answer = self._fixed_points()
        else:
            problem, steps, answer = self._count()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"function_properties_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
