"""Ordinal add, multiply, compare, and normalize exercises.

Variants are ``add``, ``multiply``, ``compare``, and ``normal_form``.  Traces
use ``CNF``, ``ORD_RULE``, ``ORD_CMP``, ``REWRITE``, and ordinary exact
arithmetic op-codes for coefficient and exponent calculations.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "add": (
        "Give the sum in canonical Cantor normal form.",
        "Perform the noncommutative ordinal addition.",
        "Apply absorption and report the canonical sum.",
        "Compute left plus right as an ordinal.",
        "Normalize the ordinal sum.",
    ),
    "multiply": (
        "Give the product in canonical Cantor normal form.",
        "Perform the noncommutative ordinal multiplication.",
        "Apply the ordinal product rules and normalize.",
        "Compute left times right as an ordinal.",
        "Determine the canonical ordinal product.",
    ),
    "compare": (
        "State the correct comparison using <, =, or >.",
        "Compare the canonical forms lexicographically.",
        "Determine which ordinal is larger, or state equality.",
        "Use the first differing Cantor-normal-form term.",
        "Report the ordering relation between the two ordinals.",
    ),
    "normal_form": (
        "Convert the expression to canonical Cantor normal form.",
        "Normalize the given ordinal expression.",
        "Apply ordinal absorption and multiplication rules as needed.",
        "Rewrite the expression as a decreasing-power ω sum.",
        "Evaluate and canonically format the ordinal.",
    ),
}


def cnf_text(terms):
    if not terms:
        return "0"
    pieces = []
    for exponent, coefficient in terms:
        if exponent == 0:
            pieces.append(str(coefficient))
        else:
            base = "ω" if exponent == 1 else f"ω^{exponent}"
            pieces.append(base if coefficient == 1
                          else f"{base}·{coefficient}")
    return " + ".join(pieces)


def cnf_add(left, right):
    """Independent tuple implementation of ordinal addition below ω^ω."""
    if not right:
        return left
    if not left:
        return right
    lead = right[0][0]
    kept = tuple(term for term in left if term[0] > lead)
    matching = next((coefficient for exponent, coefficient in left
                     if exponent == lead), 0)
    first = (lead, matching + right[0][1])
    return kept + (first,) + right[1:]


def cnf_multiply(left, right):
    """Independent tuple implementation of ordinal multiplication."""
    if not left or not right:
        return ()
    lead_exponent, lead_coefficient = left[0]
    result = ()
    for exponent, coefficient in right:
        if exponent:
            piece = ((lead_exponent + exponent, coefficient),)
        else:
            piece = ((lead_exponent, lead_coefficient * coefficient),) + left[1:]
        result = cnf_add(result, piece)
    return result


def cnf_compare(left, right):
    if left == right:
        return 0
    return -1 if left < right else 1


def random_cnf(max_exponent=3, require_infinite=False):
    while True:
        terms = tuple((exponent, random.randint(1, 5))
                      for exponent in range(max_exponent, -1, -1)
                      if random.random() < 0.55)
        if terms and (not require_infinite or terms[0][0] > 0):
            return terms


def addition_steps(left, right, result):
    lead = right[0][0]
    lower = [term for term in left if term[0] < lead]
    matching = next((coefficient for exponent, coefficient in left
                     if exponent == lead), 0)
    steps = [step("CNF", cnf_text(left)), step("CNF", cnf_text(right))]
    if lower:
        steps.append(step("ORD_RULE", "absorption",
                          f"left terms below exponent {lead} disappear"))
    else:
        steps.append(step("ORD_RULE", "addition",
                          f"retain left terms above exponent {lead}"))
    if matching:
        steps.append(step("A", matching, right[0][1],
                          matching + right[0][1]))
        steps.append(step("ORD_RULE", "coefficient merge",
                          f"combine exponent {lead} coefficients"))
    steps.append(step("REWRITE", cnf_text(result)))
    steps.append(step("CHECK", "canonical CNF", cnf_text(result)))
    return steps


def multiplication_steps(left, right, result):
    lead_exponent, lead_coefficient = left[0]
    steps = [step("CNF", cnf_text(left)), step("CNF", cnf_text(right))]
    if len(right) > 1:
        steps.append(step("ORD_RULE", "left distributive",
                          "expand over the right Cantor sum"))
    for exponent, coefficient in right:
        if exponent:
            total_exponent = lead_exponent + exponent
            steps.append(step("A", lead_exponent, exponent, total_exponent))
            steps.append(step("ORD_RULE", "limit multiplication",
                              f"leading exponent becomes {total_exponent}",
                              f"coefficient {coefficient}"))
        else:
            combined = lead_coefficient * coefficient
            steps.append(step("M", lead_coefficient, coefficient, combined))
            steps.append(step("ORD_RULE", "finite right factor",
                              f"repeat the left ordinal {coefficient} times"))
    steps.append(step("REWRITE", cnf_text(result)))
    steps.append(step("CHECK", "canonical CNF", cnf_text(result)))
    return steps


class OrdinalArithmeticGenerator(ProblemGenerator):
    """Generate exact ordinal arithmetic below ω^ω."""

    VARIANTS = ("add", "multiply", "compare", "normal_form")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _add(self):
        left, right = random_cnf(), random_cnf()
        result = cnf_add(left, right)
        problem = ("Using ordinal arithmetic, compute the sum. "
                   f"Left operand: {cnf_text(left)}. "
                   f"Right operand: {cnf_text(right)}. "
                   f"{random.choice(QUERIES['add'])}")
        return problem, addition_steps(left, right, result), cnf_text(result)

    def _multiply(self):
        left = random_cnf()
        maximum_right_exponent = max(0, 3 - left[0][0])
        right = random_cnf(maximum_right_exponent)
        result = cnf_multiply(left, right)
        problem = ("Using ordinal arithmetic, compute the product. "
                   f"Left operand: {cnf_text(left)}. "
                   f"Right operand: {cnf_text(right)}. "
                   f"{random.choice(QUERIES['multiply'])}")
        return (problem, multiplication_steps(left, right, result),
                cnf_text(result))

    def _compare(self):
        left, right = random_cnf(), random_cnf()
        comparison = cnf_compare(left, right)
        symbol = "<" if comparison < 0 else ">" if comparison > 0 else "="
        problem = ("Compare two ordinals in Cantor normal form. "
                   f"Left ordinal: {cnf_text(left)}. "
                   f"Right ordinal: {cnf_text(right)}. "
                   f"{random.choice(QUERIES['compare'])}")
        steps = [step("CNF", cnf_text(left)), step("CNF", cnf_text(right))]
        if left == right:
            steps.append(step("ORD_CMP", "canonical forms", "equal"))
        else:
            difference = None
            for first, second in zip(left, right):
                if first[0] != second[0]:
                    relation = "<" if first[0] < second[0] else ">"
                    difference = step("ORD_CMP", "first differing exponents",
                                      f"{first[0]} {relation} {second[0]}")
                    break
                if first[1] != second[1]:
                    relation = "<" if first[1] < second[1] else ">"
                    difference = step("ORD_CMP",
                                      f"coefficients at exponent {first[0]}",
                                      f"{first[1]} {relation} {second[1]}")
                    break
            if difference is None:
                relation = "<" if len(left) < len(right) else ">"
                difference = step("ORD_CMP", "remaining lower terms",
                                  f"left {relation} right")
            steps.append(difference)
        answer = f"{cnf_text(left)} {symbol} {cnf_text(right)}"
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def _normal_form(self):
        mode = random.randrange(4)
        if mode == 0:
            left, right = random_cnf(), random_cnf()
            expression = f"({cnf_text(left)}) + ({cnf_text(right)})"
            result = cnf_add(left, right)
            rule = "evaluate parenthesized ordinal sum"
        elif mode == 1:
            finite = random.randint(1, 9)
            infinite = random_cnf(require_infinite=True)
            expression = f"{finite} + ({cnf_text(infinite)})"
            result = cnf_add(((0, finite),), infinite)
            rule = "absorb the finite left term"
        elif mode == 2:
            left = random_cnf()
            factor = random.randint(2, 5)
            expression = f"({cnf_text(left)}) · {factor}"
            result = cnf_multiply(left, ((0, factor),))
            rule = "expand the finite right factor"
        else:
            first, second, third = random_cnf(), random_cnf(), random_cnf()
            expression = (f"(({cnf_text(first)}) + ({cnf_text(second)})) + "
                          f"({cnf_text(third)})")
            result = cnf_add(cnf_add(first, second), third)
            rule = "evaluate additions from the inner parentheses outward"
        problem = ("Convert an ordinal expression to Cantor normal form. "
                   f"Expression: {expression}. "
                   f"{random.choice(QUERIES['normal_form'])}")
        steps = [step("ORD_RULE", "normalization", rule),
                 step("REWRITE", f"{expression} = {cnf_text(result)}"),
                 step("CNF", cnf_text(result)),
                 step("CHECK", "canonical CNF", cnf_text(result))]
        return problem, steps, cnf_text(result)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "add":
            problem, steps, answer = self._add()
        elif variant == "multiply":
            problem, steps, answer = self._multiply()
        elif variant == "compare":
            problem, steps, answer = self._compare()
        else:
            problem, steps, answer = self._normal_form()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"ordinal_arithmetic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
