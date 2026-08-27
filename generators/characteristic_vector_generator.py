"""Encode finite sets as characteristic vectors and operate bitwise.

Variants:
- ``encode`` writes a set's vector in the stated universe order.
- ``decode`` converts a supplied bit string back to a roster.
- ``bitwise_op`` computes intersection, union, difference, or symmetric
  difference by aligned vector operations.
- ``duality`` presents the set operation and its Boolean-vector counterpart.

Op-codes:
- ``BIT``: record one element's membership bit in each input set.
- ``BITWISE``: align operand strings and apply ``∧``, ``∨``, ``⊕``, or ``¬``.
- ``DECODE``: convert a result string to its exact set roster.
- ``CHECK``: compare direct set and decoded-bit results.
- ``Z``: exact bit string, roster, or composite ``bits = roster`` answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


LETTERS = tuple("abcdefghijklmnopqrstuvwxyz")

QUERIES = {
    "encode": (
        "Encode A as a characteristic vector in U-order.",
        "Write one membership bit for each listed universe element.",
        "Convert the roster A into its ordered 0/1 string.",
        "Find χ_A using the displayed order of U.",
        "Scan U from left to right and give A's bit vector.",
    ),
    "decode": (
        "Decode v into its represented subset of U.",
        "List exactly the universe elements marked by 1.",
        "Convert the characteristic bit string to a canonical roster.",
        "Recover the finite set represented by v.",
        "Read the 1-bits in U-order and give the subset.",
    ),
    "bitwise_op": (
        "Evaluate the set expression by aligned characteristic-vector operations.",
        "Compute the result bits, then decode them to a roster.",
        "Use Boolean operations on χ_A and χ_B to find the set.",
        "Translate the set operation into bits and evaluate it.",
        "Give both the resulting vector and its decoded subset.",
    ),
    "duality": (
        "Verify the displayed set/Boolean duality and give the common result.",
        "Compute both descriptions and decode their matching vector.",
        "Use membership bits to demonstrate the stated correspondence.",
        "Check that the set operation and vector operation agree elementwise.",
        "Find the shared result of the set and Boolean forms.",
    ),
}


OPERATIONS = {
    "A ∩ B": ("∧", lambda left, right: left & right),
    "A ∪ B": ("∨", lambda left, right: left | right),
    "A Δ B": ("⊕", lambda left, right: left ^ right),
    "A − B": ("∧ ¬right", lambda left, right: left - right),
    "A ∩ Bᶜ": ("∧ ¬right", lambda left, right: left - right),
}


DUALITIES = {
    "A ∩ B": "χ_A ∧ χ_B",
    "A ∪ B": "χ_A ∨ χ_B",
    "A Δ B": "χ_A ⊕ χ_B",
    "Aᶜ": "¬χ_A",
}


def bits(universe, subset):
    return "".join("1" if element in subset else "0" for element in universe)


def random_subset(universe):
    return frozenset(element for element in universe if random.choice((True, False)))


def bit_steps(universe, first, second=None):
    out = []
    for element in universe:
        fields = [element, f"A={1 if element in first else 0}"]
        if second is not None:
            fields.append(f"B={1 if element in second else 0}")
        out.append(step("BIT", *fields))
    return out


class CharacteristicVectorGenerator(ProblemGenerator):
    """Generate exact set/vector conversions in an explicit finite order."""

    VARIANTS = ("encode", "decode", "bitwise_op", "duality")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _universe():
        return tuple(sorted(random.sample(LETTERS, random.randint(5, 11))))

    def _encode(self, universe):
        subset = random_subset(universe)
        vector = bits(universe, subset)
        problem = (f"Ordered universe U = {roster(universe)}. A = {roster(subset)}. "
                   f"{random.choice(QUERIES['encode'])}")
        steps = bit_steps(universe, subset)
        steps.append(step("CHECK", "vector length", len(vector), len(universe)))
        return problem, steps, vector

    def _decode(self, universe):
        vector = "".join(random.choice("01") for _ in universe)
        subset = frozenset(element for element, bit in zip(universe, vector)
                           if bit == "1")
        problem = (f"Ordered universe U = {roster(universe)}. Vector v = {vector}. "
                   f"{random.choice(QUERIES['decode'])}")
        steps = [step("BIT", element, f"v={bit}")
                 for element, bit in zip(universe, vector)]
        steps.append(step("DECODE", vector, roster(subset)))
        return problem, steps, roster(subset)

    def _bitwise(self, universe, variant):
        first, second = random_subset(universe), random_subset(universe)
        if variant == "duality":
            expression = random.choice(tuple(DUALITIES))
            if expression == "Aᶜ":
                result = frozenset(universe) - first
                boolean = DUALITIES[expression]
                result_bits = bits(universe, result)
                bit_op = ("¬", bits(universe, first), result_bits)
            else:
                symbol, function = OPERATIONS[expression]
                result = function(first, second)
                boolean = DUALITIES[expression]
                result_bits = bits(universe, result)
                bit_op = (symbol, bits(universe, first), bits(universe, second),
                          result_bits)
            extra = f" Set operation: {expression}. Boolean form: {boolean}."
        else:
            expression = random.choice(tuple(OPERATIONS))
            symbol, function = OPERATIONS[expression]
            result = function(first, second)
            result_bits = bits(universe, result)
            bit_op = (symbol, bits(universe, first), bits(universe, second),
                      result_bits)
            extra = f" Expression: {expression}."
        problem = (f"Ordered universe U = {roster(universe)}. "
                   f"A = {roster(first)}. B = {roster(second)}.{extra} "
                   f"{random.choice(QUERIES[variant])}")
        steps = bit_steps(universe, first, second)
        steps.append(step("BITWISE", *bit_op))
        steps.append(step("DECODE", result_bits, roster(result)))
        steps.append(step("CHECK", "direct set result", roster(result),
                          "decoded bits match"))
        return problem, steps, f"{result_bits} = {roster(result)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        universe = self._universe()
        if variant == "encode":
            problem, steps, answer = self._encode(universe)
        elif variant == "decode":
            problem, steps, answer = self._decode(universe)
        else:
            problem, steps, answer = self._bitwise(universe, variant)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"characteristic_vector_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
