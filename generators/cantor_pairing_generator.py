"""Cantor pairing, unpairing, and diagonal enumeration exercises."""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "pair": (
        "Compute the paired natural number.",
        "Evaluate the Cantor pairing value.",
        "Find the image of the ordered pair.",
        "Determine the natural number assigned to this pair.",
        "Apply the formula and report π(m, n).",
    ),
    "unpair": (
        "Recover the ordered pair.",
        "Invert the pairing value.",
        "Find the unique natural-number coordinates.",
        "Use triangular-number bounds to unpair z.",
        "Determine (m, n) from the encoded value.",
    ),
    "diagonal_enumeration": (
        "Complete the requested diagonal-enumeration lookup.",
        "Use the stated walk to match the position and pair.",
        "Determine the requested entry in the diagonal listing.",
        "Find the corresponding position-pair match.",
        "Apply the zero-indexed diagonal order.",
    ),
}


def pair_text(first, second):
    return f"({first}, {second})"


def triangular(value):
    return value * (value + 1) // 2


def cantor_pair(first, second):
    diagonal = first + second
    return triangular(diagonal) + second


def pairing_steps(first, second):
    diagonal = first + second
    successor = diagonal + 1
    product = diagonal * successor
    start = product // 2
    paired = start + second
    return [step("PAIRING", pair_text(first, second),
                 "(m + n)(m + n + 1)/2 + n"),
            step("A", first, second, diagonal),
            step("A", diagonal, 1, successor),
            step("M", diagonal, successor, product),
            step("D", product, 2, start),
            step("A", start, second, paired)]


def unpair(value):
    diagonal = 0
    while triangular(diagonal + 1) <= value:
        diagonal += 1
    second = value - triangular(diagonal)
    first = diagonal - second
    return first, second, diagonal


def unpairing_steps(value):
    first, second, diagonal = unpair(value)
    start = triangular(diagonal)
    next_start = triangular(diagonal + 1)
    product = diagonal * (diagonal + 1)
    next_product = (diagonal + 1) * (diagonal + 2)
    return [step("PAIRING", "z = T_w + n", "T_w = w(w + 1)/2"),
            step("M", diagonal, diagonal + 1, product),
            step("D", product, 2, start),
            step("TRY", f"w={diagonal}", f"{start} ≤ {value}", "ok"),
            step("M", diagonal + 1, diagonal + 2, next_product),
            step("D", next_product, 2, next_start),
            step("REJECT", f"w={diagonal + 1}",
                 f"{next_start} > {value}"),
            step("S", value, start, second),
            step("S", diagonal, second, first),
            step("UNPAIR", value, pair_text(first, second))]


class CantorPairingGenerator(ProblemGenerator):
    """Generate exact instances of Cantor's bijection ℕ × ℕ → ℕ."""

    VARIANTS = ("pair", "unpair", "diagonal_enumeration")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _pair(self):
        first, second = random.randint(0, 200), random.randint(0, 200)
        paired = cantor_pair(first, second)
        problem = ("Cantor pairing uses π(m, n) = "
                   "(m + n)(m + n + 1)/2 + n. "
                   f"Input pair: {pair_text(first, second)}. "
                   f"{random.choice(QUERIES['pair'])}")
        steps = pairing_steps(first, second)
        steps.append(step("CHECK", f"π({first}, {second}) = {paired}"))
        return problem, steps, f"π({first}, {second}) = {paired}"

    def _unpair(self):
        first, second = random.randint(0, 200), random.randint(0, 200)
        paired = cantor_pair(first, second)
        problem = ("Cantor pairing uses π(m, n) = "
                   "(m + n)(m + n + 1)/2 + n. "
                   f"Encoded value: z = {paired}. "
                   f"{random.choice(QUERIES['unpair'])}")
        steps = unpairing_steps(paired)
        steps.append(step("CHECK", pair_text(first, second), paired))
        return problem, steps, f"z = {paired} ↔ {pair_text(first, second)}"

    def _diagonal_enumeration(self):
        first, second = random.randint(0, 120), random.randint(0, 120)
        paired = cantor_pair(first, second)
        prefix = ("The zero-indexed diagonal walk of ℕ × ℕ starts "
                  "(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), ... . ")
        if random.choice((True, False)):
            problem = (prefix + f"Requested pair: {pair_text(first, second)}. "
                       "Find its position. "
                       f"{random.choice(QUERIES['diagonal_enumeration'])}")
            steps = pairing_steps(first, second)
        else:
            problem = (prefix + f"Requested position: {paired}. "
                       "Find the pair at that position. "
                       f"{random.choice(QUERIES['diagonal_enumeration'])}")
            steps = unpairing_steps(paired)
        diagonal = first + second
        steps.append(step("DIAGONAL", f"w={diagonal}",
                          f"start={triangular(diagonal)}",
                          f"offset={second}"))
        answer = f"position {paired}: {pair_text(first, second)}"
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "pair":
            problem, steps, answer = self._pair()
        elif variant == "unpair":
            problem, steps, answer = self._unpair()
        else:
            problem, steps, answer = self._diagonal_enumeration()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"cantor_pairing_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
