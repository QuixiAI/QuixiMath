"""Construct integers as equivalence classes of natural-number pairs.

Variants:
- ``equivalence_check`` tests ``(a,b) ~ (c,d)`` by ``a+d=b+c``.
- ``canonical_representative`` reduces a pair to ``(n,0)`` or ``(0,n)``.
- ``add`` applies ``(a,b)+(c,d)=(a+c,b+d)`` and reduces.
- ``multiply`` applies ``(a,b)(c,d)=(ac+bd,ad+bc)`` and reduces.
- ``order`` tests ``[a,b]≤[c,d]`` by ``a+d≤b+c``.

Operands range over large nonnegative integers, with five phrasings per
variant, so the problem space is unbounded while each operation stays exact.

Op-codes:
- ``PAIR_RULE``: state the quotient construction rule being applied.
- ``A`` / ``M``: emit every integer addition or multiplication.
- ``REDUCE``: subtract the common coordinate to reach canonical form.
- ``CMP``: compare the two cross-sums for order.
- ``CHECK``: compare pair arithmetic with ordinary integer values.
- ``Z``: composite equivalence, canonical pair/value, or order verdict.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "equivalence_check": (
        "Decide whether the pairs represent the same integer.",
        "Apply the cross-sum equivalence test.",
        "Check the defining relation and give a composite verdict.",
        "Determine whether the two pairs lie in one equivalence class.",
        "Compare a+d with b+c exactly.",
    ),
    "canonical_representative": (
        "Reduce the pair to its canonical representative.",
        "Subtract the common coordinate and state the represented integer.",
        "Give the unique representative with one coordinate zero.",
        "Find the canonical pair for this equivalence class.",
        "Normalize the pair and verify its ordinary integer value.",
    ),
    "add": (
        "Add the pair representatives and reduce the result.",
        "Apply coordinatewise addition, then give canonical form.",
        "Compute the sum in the quotient construction.",
        "Add the represented integers using only the pair rule.",
        "Find the canonical pair and ordinary value of the sum.",
    ),
    "multiply": (
        "Multiply the pair representatives and reduce the result.",
        "Apply the quotient multiplication rule, then canonicalize.",
        "Compute the product in the integer-pair construction.",
        "Multiply the represented integers using only pair arithmetic.",
        "Find the canonical pair and ordinary value of the product.",
    ),
    "order": (
        "Decide the order relation between the represented integers.",
        "Apply the cross-sum definition of ≤.",
        "Compare the two equivalence classes and give their values.",
        "Determine whether the first represented integer is at most the second.",
        "Use a+d≤b+c to certify the order verdict.",
    ),
}


def pair_text(first, second):
    return f"({first}, {second})"


def signed(value):
    return str(value).replace("-", "−")


def canonical(first, second):
    common = min(first, second)
    return first - common, second - common


def pair_value(pair):
    return pair[0] - pair[1]


def random_pair():
    return random.randint(0, 200), random.randint(0, 200)


class IntegersAsPairsGenerator(ProblemGenerator):
    """Generate exact quotient-construction arithmetic for integers."""

    VARIANTS = ("equivalence_check", "canonical_representative", "add",
                "multiply", "order")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _equivalence(self):
        first = random_pair()
        if random.choice((True, False)):
            shift = random.randint(0, 200)
            second = first[0] + shift, first[1] + shift
        else:
            second = random_pair()
            while pair_value(second) == pair_value(first):
                second = random_pair()
        left = first[0] + second[1]
        right = first[1] + second[0]
        equivalent = left == right
        problem = (f"Pairs: {pair_text(*first)} and {pair_text(*second)}. "
                   "Definition: (a, b) ~ (c, d) iff a + d = b + c. "
                   f"{random.choice(QUERIES['equivalence_check'])}")
        steps = [step("PAIR_RULE", "(a, b) ~ (c, d)", "a + d = b + c"),
                 step("A", first[0], second[1], left),
                 step("A", first[1], second[0], right),
                 step("CHECK", f"{left} {'=' if equivalent else '≠'} {right}")]
        answer = (f"equivalent: {'yes' if equivalent else 'no'} "
                  f"({left} {'=' if equivalent else '≠'} {right})")
        return problem, steps, answer

    def _canonical(self):
        original = random_pair()
        reduced = canonical(*original)
        value = pair_value(original)
        problem = (f"Pair: {pair_text(*original)}. Equivalence: "
                   "(a, b) ~ (c, d) iff a + d = b + c. "
                   f"{random.choice(QUERIES['canonical_representative'])}")
        steps = [step("PAIR_RULE", "subtract min(a, b) from both coordinates"),
                 step("REDUCE", pair_text(*original), pair_text(*reduced)),
                 step("CHECK", "value a − b", signed(value))]
        return problem, steps, f"{pair_text(*reduced)} ~ {signed(value)}"

    def _add(self):
        first, second = random_pair(), random_pair()
        raw = first[0] + second[0], first[1] + second[1]
        reduced = canonical(*raw)
        value = pair_value(raw)
        problem = (f"Add {pair_text(*first)} + {pair_text(*second)}. Rule: "
                   "(a, b) + (c, d) = (a + c, b + d). "
                   f"{random.choice(QUERIES['add'])}")
        steps = [step("PAIR_RULE", "(a, b) + (c, d)", "(a + c, b + d)"),
                 step("A", first[0], second[0], raw[0]),
                 step("A", first[1], second[1], raw[1]),
                 step("REDUCE", pair_text(*raw), pair_text(*reduced)),
                 step("CHECK", f"{signed(pair_value(first))} + "
                      f"{signed(pair_value(second))}", signed(value))]
        return problem, steps, f"{pair_text(*reduced)} ~ {signed(value)}"

    def _multiply(self):
        first, second = random_pair(), random_pair()
        ac, bd = first[0] * second[0], first[1] * second[1]
        ad, bc = first[0] * second[1], first[1] * second[0]
        raw = ac + bd, ad + bc
        reduced = canonical(*raw)
        value = pair_value(raw)
        problem = (f"Multiply {pair_text(*first)} · {pair_text(*second)}. "
                   "Rule: (a, b) · (c, d) = (ac + bd, ad + bc). "
                   f"{random.choice(QUERIES['multiply'])}")
        steps = [step("PAIR_RULE", "(a, b) · (c, d)",
                      "(ac + bd, ad + bc)"),
                 step("M", first[0], second[0], ac),
                 step("M", first[1], second[1], bd),
                 step("A", ac, bd, raw[0]),
                 step("M", first[0], second[1], ad),
                 step("M", first[1], second[0], bc),
                 step("A", ad, bc, raw[1]),
                 step("REDUCE", pair_text(*raw), pair_text(*reduced)),
                 step("CHECK", f"{signed(pair_value(first))} · "
                      f"{signed(pair_value(second))}", signed(value))]
        return problem, steps, f"{pair_text(*reduced)} ~ {signed(value)}"

    def _order(self):
        first, second = random_pair(), random_pair()
        left = first[0] + second[1]
        right = first[1] + second[0]
        result = left <= right
        first_value, second_value = pair_value(first), pair_value(second)
        problem = (f"Compare classes [{first[0]}, {first[1]}] and "
                   f"[{second[0]}, {second[1]}]. Definition: [a, b] ≤ [c, d] "
                   "iff a + d ≤ b + c. "
                   f"{random.choice(QUERIES['order'])}")
        steps = [step("PAIR_RULE", "[a, b] ≤ [c, d]", "a + d ≤ b + c"),
                 step("A", first[0], second[1], left),
                 step("A", first[1], second[0], right),
                 step("CMP", left, right, "≤" if result else ">"),
                 step("CHECK", signed(first_value), signed(second_value),
                      "≤" if result else ">")]
        answer = (f"{'true' if result else 'false'}; {signed(first_value)} "
                  f"{'≤' if result else '>'} {signed(second_value)} "
                  f"({left} {'≤' if result else '>'} {right})")
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "equivalence_check":
            problem, steps, answer = self._equivalence()
        elif variant == "canonical_representative":
            problem, steps, answer = self._canonical()
        elif variant == "add":
            problem, steps, answer = self._add()
        elif variant == "multiply":
            problem, steps, answer = self._multiply()
        else:
            problem, steps, answer = self._order()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"integers_as_pairs_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
