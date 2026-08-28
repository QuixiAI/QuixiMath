"""Explicit bijections witnessing countability of standard sets."""
from fractions import Fraction
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "nat_to_int": (
        "Complete the requested integer lookup under f.",
        "Use the parity rule to find the requested value.",
        "Evaluate the indicated direction of the bijection.",
        "Determine the matching natural number and integer.",
        "Apply the piecewise correspondence exactly.",
    ),
    "nat_to_evens": (
        "Complete the requested even-number lookup under e.",
        "Find the corresponding natural number or even number.",
        "Apply the doubling bijection in the indicated direction.",
        "Evaluate the stated doubling correspondence.",
        "Determine the matching entry under e.",
    ),
    "nat_to_squares": (
        "Complete both perfect-square lookups under s.",
        "Find the requested image and preimage.",
        "Apply the square bijection in both indicated directions.",
        "Evaluate the forward and inverse squaring correspondences.",
        "Determine both matching entries under s.",
    ),
    "calkin_wilf": (
        "Find the requested positive rational.",
        "Follow the binary path to determine the term.",
        "Evaluate the indexed Calkin–Wilf entry.",
        "Use each remaining binary digit to update the fraction.",
        "Determine the fraction at the stated index.",
    ),
    "hilbert_hotel": (
        "Find both requested destination rooms.",
        "Apply the reassignment to the two specified guests.",
        "Determine where the existing guest and new guest are placed.",
        "Use the even-odd room split for both requests.",
        "Report the two rooms assigned by the scheme.",
    ),
}


def int_text(value):
    return str(value).replace("-", "−")


def fraction_text(value):
    value = Fraction(value)
    return (int_text(value.numerator) if value.denominator == 1
            else f"{int_text(value.numerator)}/{value.denominator}")


def nat_to_int(value):
    return value // 2 if value % 2 == 0 else -(value + 1) // 2


def int_to_nat(value):
    return 2 * value if value >= 0 else -2 * value - 1


def calkin_wilf(index):
    numerator, denominator = 1, 1
    for bit in bin(index)[3:]:
        if bit == "0":
            denominator = numerator + denominator
        else:
            numerator = numerator + denominator
    return Fraction(numerator, denominator)


class CountabilityBijectionGenerator(ProblemGenerator):
    """Generate calculations with concrete bijections to countable sets."""

    VARIANTS = ("nat_to_int", "nat_to_evens", "nat_to_squares",
                "calkin_wilf", "hilbert_hotel")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _nat_to_int(self):
        rule = ("Define f: ℕ → ℤ by f(n) = n/2 when n is even and "
                "f(n) = −(n + 1)/2 when n is odd. ")
        steps = [step("BIJECTION_RULE", "f(n)",
                      "n/2 if even; −(n + 1)/2 if odd")]
        if random.choice((True, False)):
            natural = random.randint(0, 2000)
            integer = nat_to_int(natural)
            problem = (rule + f"Evaluation request: n = {natural}. "
                       f"{random.choice(QUERIES['nat_to_int'])}")
            if natural % 2 == 0:
                steps.extend([step("CASE", f"{natural} even", "use n/2"),
                              step("D", natural, 2, integer)])
            else:
                successor = natural + 1
                half = successor // 2
                steps.extend([step("CASE", f"{natural} odd",
                                   "use −(n + 1)/2"),
                              step("A", natural, 1, successor),
                              step("D", successor, 2, half),
                              step("NEGATE", half, integer)])
            answer = f"f({natural}) = {int_text(integer)}"
        else:
            integer = random.randint(-1000, 1000)
            natural = int_to_nat(integer)
            problem = (rule + f"Inverse request: z = {int_text(integer)}. "
                       f"{random.choice(QUERIES['nat_to_int'])}")
            if integer >= 0:
                steps.extend([step("CASE", f"{int_text(integer)} ≥ 0",
                                   "inverse is 2z"),
                              step("M", 2, integer, natural)])
            else:
                doubled = -2 * integer
                steps.extend([step("CASE", f"{int_text(integer)} < 0",
                                   "inverse is −2z − 1"),
                              step("M", -2, integer, doubled),
                              step("S", doubled, 1, natural)])
            answer = f"f⁻¹({int_text(integer)}) = {natural}"
        steps.append(step("CHECK", natural, int_text(integer)))
        return problem, steps, answer

    def _nat_to_evens(self):
        natural = random.randint(0, 5000)
        even = 2 * natural
        rule = "Define e from ℕ to the nonnegative even integers by e(n) = 2n. "
        steps = [step("BIJECTION_RULE", "e(n)", "2n")]
        if random.choice((True, False)):
            problem = (rule + f"Evaluation request: n = {natural}. "
                       f"{random.choice(QUERIES['nat_to_evens'])}")
            steps.append(step("M", 2, natural, even))
            answer = f"e({natural}) = {even}"
        else:
            problem = (rule + f"Inverse request: even value = {even}. "
                       f"{random.choice(QUERIES['nat_to_evens'])}")
            steps.append(step("D", even, 2, natural))
            answer = f"e⁻¹({even}) = {natural}"
        steps.append(step("CHECK", natural, even))
        return problem, steps, answer

    def _nat_to_squares(self):
        natural = random.randint(0, 500)
        inverse_natural = random.randint(0, 500)
        square = natural * natural
        inverse_square = inverse_natural * inverse_natural
        rule = "Define s from ℕ to the perfect squares by s(n) = n². "
        steps = [step("BIJECTION_RULE", "s(n)", "n²")]
        problem = (rule + f"Evaluation request: n = {natural}; inverse "
                   f"request: square value = {inverse_square}. "
                   f"{random.choice(QUERIES['nat_to_squares'])}")
        steps.extend([step("M", natural, natural, square),
                      step("ROOT", inverse_square, inverse_natural),
                      step("CHECK", natural, square),
                      step("CHECK", inverse_natural, inverse_square)])
        answer = (f"s({natural}) = {square}; "
                  f"s⁻¹({inverse_square}) = {inverse_natural}")
        return problem, steps, answer

    def _calkin_wilf(self):
        index = random.randint(1, 65535)
        binary = bin(index)[2:]
        numerator, denominator = 1, 1
        problem = ("For n ≥ 1, the Calkin–Wilf binary walk starts at 1/1, "
                   "skips the leading 1 of n in binary, then sends bit 0: "
                   "a/b → a/(a + b) and bit 1: a/b → (a + b)/b. "
                   f"Index: n = {index}. "
                   f"{random.choice(QUERIES['calkin_wilf'])}")
        steps = [step("BIJECTION_RULE", "0", "a/b → a/(a + b)"),
                 step("BIJECTION_RULE", "1", "a/b → (a + b)/b"),
                 step("BINARY", index, binary),
                 step("CW_START", "leading 1", "1/1")]
        for bit in binary[1:]:
            total = numerator + denominator
            before = f"{numerator}/{denominator}"
            steps.append(step("A", numerator, denominator, total))
            if bit == "0":
                denominator = total
            else:
                numerator = total
            steps.append(step("CW_STEP", f"bit {bit}", before,
                              f"{numerator}/{denominator}"))
        value = Fraction(numerator, denominator)
        answer = f"term {index} = {fraction_text(value)}"
        steps.append(step("CHECK", index, fraction_text(value)))
        return problem, steps, answer

    def _hilbert_hotel(self):
        existing = random.randint(0, 1500)
        newcomer = random.randint(0, 1500)
        existing_room = 2 * existing
        newcomer_room = 2 * newcomer + 1
        problem = ("A hotel has rooms and guest labels in ℕ. To admit "
                   "countably many new guests, move the existing guest from "
                   "room n to room 2n and place new guest n in room 2n + 1. "
                   f"Existing room request: {existing}; new guest request: "
                   f"{newcomer}. {random.choice(QUERIES['hilbert_hotel'])}")
        doubled_new = 2 * newcomer
        steps = [step("BIJECTION_RULE", "existing n", "room 2n"),
                 step("M", 2, existing, existing_room),
                 step("BIJECTION_RULE", "new guest n", "room 2n + 1"),
                 step("M", 2, newcomer, doubled_new),
                 step("A", doubled_new, 1, newcomer_room),
                 step("CHECK", f"even room {existing_room}",
                      f"odd room {newcomer_room}")]
        answer = (f"existing room {existing} → {existing_room}; "
                  f"new guest {newcomer} → {newcomer_room}")
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "nat_to_int":
            problem, steps, answer = self._nat_to_int()
        elif variant == "nat_to_evens":
            problem, steps, answer = self._nat_to_evens()
        elif variant == "nat_to_squares":
            problem, steps, answer = self._nat_to_squares()
        elif variant == "calkin_wilf":
            problem, steps, answer = self._calkin_wilf()
        else:
            problem, steps, answer = self._hilbert_hotel()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"countability_bijection_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
