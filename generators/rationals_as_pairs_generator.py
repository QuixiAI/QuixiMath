"""Construct rational numbers from integer/positive-denominator pairs.

Variants:
- ``equivalence_check`` tests ``(a,b) ~ (c,d)`` by ``ad=bc``.
- ``add`` applies ``(ad+bc,bd)`` and reduces.
- ``multiply`` applies ``(ac,bd)`` and reduces.
- ``canonical_form`` normalizes one pair with Euclid's algorithm.
- ``order`` compares cross products because denominators are positive.

Large signed numerators, positive denominators, operators, and five phrasings
make the problem space unbounded while all calculations use exact integers.

Op-codes:
- ``PAIR_RULE``: state the rational-pair rule.
- ``M`` / ``A``: emit cross-products and numerator arithmetic.
- ``GCD_START`` / ``GCD_DIV`` / ``GCD_DONE``: run Euclid explicitly.
- ``REDUCE``: divide a raw pair by its positive gcd.
- ``CMP`` / ``CHECK``: compare cross-products and verify exact fractions.
- ``Z``: composite equivalence, reduced pair/fraction, or order verdict.
"""
from fractions import Fraction
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "equivalence_check": (
        "Decide whether the pairs represent the same rational number.",
        "Apply the cross-product equivalence test.",
        "Check the defining relation and give a composite verdict.",
        "Determine whether the pairs lie in one rational equivalence class.",
        "Compare ad with bc exactly.",
    ),
    "add": (
        "Add the rational-pair representatives and reduce.",
        "Apply the common-denominator pair rule, then canonicalize.",
        "Compute the exact sum in the quotient construction.",
        "Add using pair arithmetic and show the Euclidean reduction.",
        "Give the reduced pair and ordinary fraction of the sum.",
    ),
    "multiply": (
        "Multiply the rational-pair representatives and reduce.",
        "Apply coordinatewise multiplication, then canonicalize.",
        "Compute the exact product in the quotient construction.",
        "Multiply using pair arithmetic and show the Euclidean reduction.",
        "Give the reduced pair and ordinary fraction of the product.",
    ),
    "canonical_form": (
        "Reduce the pair to canonical rational form.",
        "Use Euclid's algorithm and keep the denominator positive.",
        "Find the lowest-terms representative of this class.",
        "Normalize the pair and state its ordinary fraction.",
        "Give the positive-denominator canonical representative.",
    ),
    "order": (
        "Decide the displayed rational order statement.",
        "Compare the exact cross-products.",
        "Use positive denominators to certify the order verdict.",
        "Determine the relation between the represented rationals.",
        "Give a composite verdict with both cross-products.",
    ),
}


def int_text(value):
    return str(value).replace("-", "−")


def pair_text(numerator, denominator):
    return f"({int_text(numerator)}, {denominator})"


def fraction_text(value):
    if value.denominator == 1:
        return int_text(value.numerator)
    return f"{int_text(value.numerator)}/{value.denominator}"


def random_pair():
    return random.randint(-200, 200), random.randint(1, 200)


def euclid_steps(numerator, denominator):
    first, second = abs(numerator), denominator
    steps = [step("GCD_START", first, second)]
    a, b = first, second
    while b:
        quotient, remainder = divmod(a, b)
        steps.append(step("GCD_DIV", a, b, quotient, remainder))
        a, b = b, remainder
    gcd = a or 1
    steps.append(step("GCD_DONE", gcd))
    return gcd, steps


def reduced_answer(numerator, denominator):
    value = Fraction(numerator, denominator)
    pair = pair_text(value.numerator, value.denominator)
    return value, pair, f"{pair} = {fraction_text(value)}"


class RationalsAsPairsGenerator(ProblemGenerator):
    """Generate exact quotient-construction arithmetic for rationals."""

    VARIANTS = ("equivalence_check", "add", "multiply", "canonical_form",
                "order")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _equivalence(self):
        first = random_pair()
        if random.choice((True, False)):
            multiplier = random.randint(1, 100)
            second = first[0] * multiplier, first[1] * multiplier
        else:
            second = random_pair()
            while first[0] * second[1] == first[1] * second[0]:
                second = random_pair()
        left, right = first[0] * second[1], first[1] * second[0]
        result = left == right
        problem = (f"Pairs: {pair_text(*first)} and {pair_text(*second)}. "
                   "Definition: (a, b) ~ (c, d) iff ad = bc, with b,d > 0. "
                   f"{random.choice(QUERIES['equivalence_check'])}")
        steps = [step("PAIR_RULE", "(a, b) ~ (c, d)", "ad = bc"),
                 step("M", first[0], second[1], left),
                 step("M", first[1], second[0], right),
                 step("CHECK", f"{int_text(left)} "
                      f"{'=' if result else '≠'} {int_text(right)}")]
        answer = (f"equivalent: {'yes' if result else 'no'} "
                  f"({int_text(left)} {'=' if result else '≠'} "
                  f"{int_text(right)})")
        return problem, steps, answer

    def _canonical(self):
        original = random_pair()
        value, reduced, answer = reduced_answer(*original)
        gcd, steps = euclid_steps(*original)
        problem = (f"Pair: {pair_text(*original)}. Canonical form has positive "
                   "denominator and gcd(abs(a), b) = 1. "
                   f"{random.choice(QUERIES['canonical_form'])}")
        steps.insert(0, step("PAIR_RULE", "divide both coordinates by gcd"))
        steps.append(step("REDUCE", pair_text(*original), reduced,
                          f"divide by {gcd}"))
        steps.append(step("CHECK", fraction_text(value)))
        return problem, steps, answer

    def _add(self):
        first, second = random_pair(), random_pair()
        ad, bc = first[0] * second[1], first[1] * second[0]
        numerator, denominator = ad + bc, first[1] * second[1]
        value, reduced, answer = reduced_answer(numerator, denominator)
        gcd, gcd_trace = euclid_steps(numerator, denominator)
        problem = (f"Add {pair_text(*first)} + {pair_text(*second)}. Rule: "
                   "(a, b) + (c, d) = (ad + bc, bd). "
                   f"{random.choice(QUERIES['add'])}")
        steps = [step("PAIR_RULE", "(a, b) + (c, d)", "(ad + bc, bd)"),
                 step("M", first[0], second[1], ad),
                 step("M", first[1], second[0], bc),
                 step("A", ad, bc, numerator),
                 step("M", first[1], second[1], denominator)]
        steps.extend(gcd_trace)
        steps.append(step("REDUCE", pair_text(numerator, denominator), reduced,
                          f"divide by {gcd}"))
        steps.append(step("CHECK", fraction_text(Fraction(*first)), "+",
                          fraction_text(Fraction(*second)), fraction_text(value)))
        return problem, steps, answer

    def _multiply(self):
        first, second = random_pair(), random_pair()
        numerator, denominator = first[0] * second[0], first[1] * second[1]
        value, reduced, answer = reduced_answer(numerator, denominator)
        gcd, gcd_trace = euclid_steps(numerator, denominator)
        problem = (f"Multiply {pair_text(*first)} · {pair_text(*second)}. Rule: "
                   "(a, b) · (c, d) = (ac, bd). "
                   f"{random.choice(QUERIES['multiply'])}")
        steps = [step("PAIR_RULE", "(a, b) · (c, d)", "(ac, bd)"),
                 step("M", first[0], second[0], numerator),
                 step("M", first[1], second[1], denominator)]
        steps.extend(gcd_trace)
        steps.append(step("REDUCE", pair_text(numerator, denominator), reduced,
                          f"divide by {gcd}"))
        steps.append(step("CHECK", fraction_text(Fraction(*first)), "·",
                          fraction_text(Fraction(*second)), fraction_text(value)))
        return problem, steps, answer

    def _order(self):
        first, second = random_pair(), random_pair()
        operator = random.choice(("<", "≤"))
        left, right = first[0] * second[1], first[1] * second[0]
        result = left < right if operator == "<" else left <= right
        problem = (f"Statement: {pair_text(*first)} {operator} "
                   f"{pair_text(*second)}. Denominators are positive; compare "
                   f"ad {operator} bc. {random.choice(QUERIES['order'])}")
        steps = [step("PAIR_RULE", f"a/b {operator} c/d",
                      f"ad {operator} bc"),
                 step("M", first[0], second[1], left),
                 step("M", first[1], second[0], right),
                 step("CMP", int_text(left), int_text(right),
                      "true" if result else "false"),
                 step("CHECK", fraction_text(Fraction(*first)), operator,
                      fraction_text(Fraction(*second)))]
        answer = (f"{'true' if result else 'false'}; {int_text(left)} "
                  f"{operator} {int_text(right)} is "
                  f"{'true' if result else 'false'}")
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "equivalence_check":
            problem, steps, answer = self._equivalence()
        elif variant == "add":
            problem, steps, answer = self._add()
        elif variant == "multiply":
            problem, steps, answer = self._multiply()
        elif variant == "canonical_form":
            problem, steps, answer = self._canonical()
        else:
            problem, steps, answer = self._order()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"rationals_as_pairs_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
