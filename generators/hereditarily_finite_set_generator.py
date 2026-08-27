"""Work with hereditarily finite sets and von Neumann constructions.

Variants:
- ``kuratowski_encode`` / ``kuratowski_decode`` convert ordered pairs.
- ``von_neumann_numeral`` writes a finite ordinal as a nested set.
- ``successor`` computes ``S(X) = X ∪ {X}``.
- ``big_union`` computes ``∪X`` for a displayed set of sets.
- ``transitive_check`` checks every element-subset condition in canonical order.
- ``rank`` computes von Neumann rank recursively.

Ackermann-decoded operands, pair choices, set families, and five phrasings give
an unbounded class-level problem space. The intentionally tiny numeral variant
is down-weighted but remains directly selectable.

Op-codes:
- ``NEST``: show one nesting/construction level.
- ``UNION_ELEMENT``: show what one member contributes to a big union.
- ``TRANSITIVE_CHECK``: test one element against ``X``.
- ``RANK``: give the recursively computed rank of one nested set.
- ``CHECK``: verify decoding or the defining set equation.
- ``Z``: canonical nested set, ordered pair, integer, or composite verdict.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import (ackermann_decode, big_union, hf_text, kuratowski,
                        set_rank, sorted_elements, successor,
                        transitivity_witness, tuple_text, un_kuratowski,
                        von_neumann)


FOUNDATIONS = True


QUERIES = {
    "kuratowski_encode": (
        "Encode the ordered pair by the Kuratowski definition.",
        "Write (a, b) as {{a}, {a, b}} in canonical nested-set form.",
        "Construct the exact hereditarily finite set representing the pair.",
        "Apply the displayed ordered-pair definition.",
        "Give the canonical Kuratowski encoding.",
    ),
    "kuratowski_decode": (
        "Decode the Kuratowski set into its ordered pair.",
        "Recover a from the singleton and b from the two-element block.",
        "Identify the exact ordered pair represented by K.",
        "Invert the displayed Kuratowski construction.",
        "Give the canonical pair decoded from the nested set.",
    ),
    "von_neumann_numeral": (
        "Write the number as a von Neumann numeral.",
        "Construct the finite ordinal from all smaller numerals.",
        "Give the canonical nested-set representation of n.",
        "Build n from ∅ by repeated set successor.",
        "Express the displayed integer as a von Neumann ordinal.",
    ),
    "successor": (
        "Compute the set successor S(X) = X ∪ {X}.",
        "Adjoin X itself as one new member.",
        "Construct the canonical successor of the displayed set.",
        "Apply the von Neumann successor operation to X.",
        "Give X ∪ {X} in canonical nested-set order.",
    ),
    "big_union": (
        "Compute the big union ∪X.",
        "Collect every member contributed by every element of X.",
        "Flatten one set level and give the canonical result.",
        "Form the union of all sets belonging to X.",
        "Evaluate ∪X without dropping duplicate contributions prematurely.",
    ),
    "transitive_check": (
        "Decide whether X is transitive and give the first violation if not.",
        "Check in canonical order that every element is a subset of X.",
        "Determine transitivity with an explicit certificate.",
        "Test every member-subset condition until the first failure.",
        "Give the canonical transitivity verdict for X.",
    ),
    "rank": (
        "Compute the von Neumann rank of X.",
        "Use rank(X) = max(rank(e) + 1) over the elements.",
        "Find the nesting rank recursively.",
        "Evaluate the rank of every required substructure.",
        "Give the exact finite rank of the displayed set.",
    ),
}


def random_hf(max_bit=31):
    """A sparse Ackermann set: huge space with at most five outer members."""
    if random.random() < 0.002:
        return frozenset()
    count = random.randint(1, 5)
    indices = random.sample(range(max_bit + 1), count)
    return frozenset(ackermann_decode(index) for index in indices)


def rank_steps(value):
    steps = []
    seen = set()

    def visit(item):
        for child in sorted_elements(item):
            visit(child)
        if item not in seen:
            seen.add(item)
            steps.append(step("RANK", hf_text(item), set_rank(item)))

    visit(value)
    return steps


class HereditarilyFiniteSetGenerator(ProblemGenerator):
    """Generate exact exercises on pure finite sets."""

    VARIANTS = ("kuratowski_encode", "kuratowski_decode",
                "von_neumann_numeral", "successor", "big_union",
                "transitive_check", "rank")
    WEIGHTS = (0.35, 0.35, 0.001, 0.05, 0.219, 0.01, 0.02)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _encode(self):
        first, second = random_hf(), random_hf()
        singleton = frozenset({first})
        doubleton = frozenset({first, second})
        encoded = kuratowski(first, second)
        pair_text = tuple_text((first, second))
        problem = (f"Ordered pair: {pair_text}. Definition: "
                   "(a, b) = {{a}, {a, b}}. "
                   f"{random.choice(QUERIES['kuratowski_encode'])}")
        steps = [step("NEST", "{a}", hf_text(singleton)),
                 step("NEST", "{a, b}", hf_text(doubleton)),
                 step("NEST", "{{a}, {a, b}}", hf_text(encoded)),
                 step("CHECK", pair_text, "encoded by singleton/intersection")]
        return problem, steps, hf_text(encoded)

    def _decode(self):
        first, second = random_hf(), random_hf()
        encoded = kuratowski(first, second)
        decoded = un_kuratowski(encoded)
        problem = (f"K = {hf_text(encoded)}. Definition: "
                   "(a, b) = {{a}, {a, b}}. "
                   f"{random.choice(QUERIES['kuratowski_decode'])}")
        blocks = sorted_elements(encoded)
        steps = [step("NEST", f"block {index}", hf_text(block))
                 for index, block in enumerate(blocks, 1)]
        answer = tuple_text(decoded)
        steps.append(step("CHECK", answer, hf_text(kuratowski(*decoded))))
        return problem, steps, answer

    def _numeral(self):
        number = random.randint(0, 5)
        value = von_neumann(number)
        problem = (f"n = {number}. Definition: 0 = ∅ and "
                   "S(k) = k ∪ {k}. "
                   f"{random.choice(QUERIES['von_neumann_numeral'])}")
        steps = [step("NEST", index, hf_text(von_neumann(index)))
                 for index in range(number + 1)]
        steps.append(step("CHECK", f"card(n)={len(value)}", f"n={number}"))
        return problem, steps, hf_text(value)

    def _successor(self):
        value = random_hf()
        result = successor(value)
        problem = (f"X = {hf_text(value)}. Definition: S(X) = X ∪ {{X}}. "
                   f"{random.choice(QUERIES['successor'])}")
        steps = [step("NEST", "X", hf_text(value)),
                 step("NEST", "{X}", hf_text(frozenset({value}))),
                 step("NEST", "X ∪ {X}", hf_text(result)),
                 step("CHECK", "X ⊆ S(X)", "X ∈ S(X)")]
        return problem, steps, hf_text(result)

    def _union(self):
        members = {random_hf() for _ in range(random.randint(2, 5))}
        value = frozenset(members)
        result = big_union(value)
        problem = (f"X = {hf_text(value)}. "
                   f"{random.choice(QUERIES['big_union'])}")
        steps = []
        for member in sorted_elements(value):
            steps.append(step("UNION_ELEMENT", hf_text(member),
                              f"contributes {hf_text(member)}"))
        steps.append(step("CHECK", "flatten one level", hf_text(result)))
        return problem, steps, hf_text(result)

    def _transitive(self):
        if random.choice((True, False)):
            value = von_neumann(random.randint(0, 5))
        else:
            value = random_hf()
        witness = transitivity_witness(value)
        problem = (f"X = {hf_text(value)}. A set is transitive iff every "
                   "element of X is a subset of X. "
                   f"{random.choice(QUERIES['transitive_check'])}")
        steps = []
        for element in sorted_elements(value):
            is_subset = element <= value
            steps.append(step("TRANSITIVE_CHECK", hf_text(element),
                              f"subset of X={'yes' if is_subset else 'no'}"))
            if not is_subset:
                break
        if witness is None:
            answer = "transitive: yes (every element is a subset of X)"
        else:
            element, missing = witness
            answer = (f"transitive: no ({hf_text(element)} ∈ X but "
                      f"{hf_text(missing)} ∉ X)")
        return problem, steps, answer

    def _rank(self):
        value = random_hf()
        result = set_rank(value)
        problem = (f"X = {hf_text(value)}. Use rank(∅) = 0 and "
                   "rank(X) = max(rank(e) + 1 : e ∈ X). "
                   f"{random.choice(QUERIES['rank'])}")
        steps = rank_steps(value)
        steps.append(step("CHECK", f"rank(X)={result}"))
        return problem, steps, str(result)

    def generate(self):
        variant = self.variant or random.choices(
            self.VARIANTS, weights=self.WEIGHTS, k=1)[0]
        if variant == "kuratowski_encode":
            problem, steps, answer = self._encode()
        elif variant == "kuratowski_decode":
            problem, steps, answer = self._decode()
        elif variant == "von_neumann_numeral":
            problem, steps, answer = self._numeral()
        elif variant == "successor":
            problem, steps, answer = self._successor()
        elif variant == "big_union":
            problem, steps, answer = self._union()
        elif variant == "transitive_check":
            problem, steps, answer = self._transitive()
        else:
            problem, steps, answer = self._rank()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"hereditarily_finite_set_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
