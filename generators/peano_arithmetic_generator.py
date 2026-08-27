"""Evaluate Peano arithmetic by the displayed primitive recursions.

Variants:
- ``addition`` unfolds ``a + 0`` / ``a + S(b)`` for two or three terms.
- ``multiplication`` unfolds multiplication into repeated addition.
- ``exponentiation`` unfolds powers into repeated multiplication.
- ``leq_witness`` uses ``a ≤ b`` iff ``a + c = b`` for some ``c``.
- ``predecessor_monus`` evaluates truncated subtraction by predecessor.

Operands are at most 6, answers stay hand-sized, and decimal, compact-successor,
and nested-successor input spellings combine with three-term expressions and
five phrasings. The problem space is intentionally moderate (the capacity
probe estimates roughly 18,000 texts) because the curriculum caps numerals at
6; this is the plan's documented small-space exception to the 100,000 gate.

Op-codes:
- ``PEANO_EQ``: apply one successor recursion equation.
- ``PEANO_BASE``: apply a zero/base equation.
- ``FOLD``: rebuild a compact successor numeral from an evaluated layer.
- ``WITNESS`` / ``NO_WITNESS``: certify or reject ``≤``.
- ``CHECK``: verify the result in decimal arithmetic.
- ``Z``: compact successor numeral and decimal value, or composite order fact.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "addition": (
        "Compute by primitive recursion on each right operand.",
        "Unfold every successor in the stated left-to-right expression.",
        "Use only the supplied Peano addition equations.",
        "Evaluate the sum and fold the resulting successor numeral.",
        "Show the complete recursive addition trace.",
    ),
    "multiplication": (
        "Compute by primitive recursion and repeated addition.",
        "Unfold every multiplication successor in left-to-right order.",
        "Use only the supplied Peano multiplication equations.",
        "Evaluate the product and fold the resulting successor numeral.",
        "Show the complete recursive multiplication trace.",
    ),
    "exponentiation": (
        "Compute by primitive recursion on the exponent.",
        "Unfold the power into the stated multiplication recurrence.",
        "Use only the supplied Peano exponentiation equations.",
        "Evaluate the exponent sum first, then recursively form the power.",
        "Show the complete recursive exponentiation trace.",
    ),
    "leq_witness": (
        "Decide the order statement and give the least witness when it exists.",
        "Use the existential addition definition of ≤.",
        "Find c with a + c = b or prove that no Peano c works.",
        "Give a composite order verdict with its addition certificate.",
        "Check the comparison from the supplied Peano definition.",
    ),
    "predecessor_monus": (
        "Compute the truncated subtraction by predecessor recursion.",
        "Unfold every right-hand successor using the monus equations.",
        "Apply pred at each recursive subtraction layer.",
        "Evaluate the left-to-right monus expression in Peano form.",
        "Show the complete predecessor/monus trace.",
    ),
}


def compact(number):
    return "S" * number + "0"


def nested(number):
    result = "0"
    for _ in range(number):
        result = f"S({result})"
    return result


def display(number):
    return random.choice((str(number), compact(number), nested(number)))


def answer_text(number):
    return f"{compact(number)} = {number}"


def addition_trace(first, second):
    steps = []
    for current in range(second, 0, -1):
        steps.append(step("PEANO_EQ",
                          f"{compact(first)} + {compact(current)}",
                          f"S({compact(first)} + {compact(current - 1)})"))
    steps.append(step("PEANO_BASE", f"{compact(first)} + 0",
                      compact(first)))
    for amount in range(1, second + 1):
        steps.append(step("FOLD", f"S({compact(first + amount - 1)})",
                          compact(first + amount)))
    return steps, first + second


def multiplication_trace(first, second):
    steps = []
    for current in range(second, 0, -1):
        steps.append(step("PEANO_EQ",
                          f"{compact(first)} · {compact(current)}",
                          f"{compact(first)} · {compact(current - 1)} + "
                          f"{compact(first)}"))
    steps.append(step("PEANO_BASE", f"{compact(first)} · 0", "0"))
    running = 0
    for _ in range(second):
        previous = running
        running += first
        steps.append(step("FOLD", f"{compact(previous)} + {compact(first)}",
                          compact(running)))
    return steps, running


class PeanoArithmeticGenerator(ProblemGenerator):
    """Generate exact recursive arithmetic over successor numerals."""

    VARIANTS = ("addition", "multiplication", "exponentiation",
                "leq_witness", "predecessor_monus")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _addition(self):
        count = random.choice((2, 3))
        operands = [random.randint(0, 6) for _ in range(count)]
        shown = [display(value) for value in operands]
        expression = " + ".join(shown)
        problem = (f"Expression: {expression}. Rules: a + 0 = a; "
                   "a + S(b) = S(a + b). Evaluation order: left to right. "
                   f"{random.choice(QUERIES['addition'])}")
        steps = []
        running = operands[0]
        for operand in operands[1:]:
            trace, running = addition_trace(running, operand)
            steps.extend(trace)
        steps.append(step("CHECK", "decimal",
                          f"{' + '.join(map(str, operands))} = {running}"))
        return problem, steps, answer_text(running)

    def _multiplication(self):
        while True:
            count = random.choice((2, 3))
            operands = [random.randint(0, 6) for _ in range(count)]
            product = 1
            for value in operands:
                product *= value
            if product <= 60:
                break
        expression = " · ".join(display(value) for value in operands)
        problem = (f"Expression: {expression}. Rules: a · 0 = 0; "
                   "a · S(b) = a · b + a. Evaluation order: left to right. "
                   f"{random.choice(QUERIES['multiplication'])}")
        steps = []
        running = operands[0]
        for operand in operands[1:]:
            trace, running = multiplication_trace(running, operand)
            steps.extend(trace)
        steps.append(step("CHECK", "decimal",
                          f"{' · '.join(map(str, operands))} = {running}"))
        return problem, steps, answer_text(running)

    def _exponentiation(self):
        while True:
            base = random.randint(0, 6)
            first_exp, second_exp = random.randint(0, 3), random.randint(0, 3)
            exponent = first_exp + second_exp
            value = base ** exponent
            if value <= 80:
                break
        expression = (f"{display(base)} ^ "
                      f"({display(first_exp)} + {display(second_exp)})")
        problem = (f"Expression: {expression}. Rules: a^0 = S0; "
                   "a^S(b) = a^b · a; addition uses a + 0 = a and "
                   "a + S(b) = S(a + b). "
                   f"{random.choice(QUERIES['exponentiation'])}")
        steps, exponent_check = addition_trace(first_exp, second_exp)
        assert exponent_check == exponent
        for current in range(exponent, 0, -1):
            steps.append(step("PEANO_EQ", f"{compact(base)}^{compact(current)}",
                              f"{compact(base)}^{compact(current - 1)} · "
                              f"{compact(base)}"))
        steps.append(step("PEANO_BASE", f"{compact(base)}^0", "S0"))
        running = 1
        for _ in range(exponent):
            previous = running
            running *= base
            steps.append(step("FOLD", f"{compact(previous)} · {compact(base)}",
                              compact(running)))
        steps.append(step("CHECK", "decimal",
                          f"{base}^({first_exp} + {second_exp}) = {running}"))
        return problem, steps, answer_text(running)

    def _leq(self):
        first, second = random.randint(0, 6), random.randint(0, 6)
        problem = (f"Comparison: {display(first)} ≤ {display(second)}. "
                   "Definition: a ≤ b iff there exists c with a + c = b. "
                   f"{random.choice(QUERIES['leq_witness'])}")
        steps = []
        if first <= second:
            witness = second - first
            trace, total = addition_trace(first, witness)
            steps.extend(trace)
            steps.append(step("WITNESS", f"c={compact(witness)}",
                              f"{compact(first)} + {compact(witness)} = "
                              f"{compact(total)}"))
            answer = (f"true; witness c = {compact(witness)} "
                      f"({first} + {witness} = {second})")
        else:
            steps.append(step("NO_WITNESS", f"{first} > {second}",
                              "successor addition cannot decrease a"))
            answer = f"false; no c ({first} > {second})"
        steps.append(step("CHECK", "decimal", f"{first} ≤ {second} is "
                          f"{'true' if first <= second else 'false'}"))
        return problem, steps, answer

    def _monus(self):
        count = random.choice((2, 3))
        operands = [random.randint(0, 6) for _ in range(count)]
        problem = (f"Expression: {' ∸ '.join(display(v) for v in operands)}. "
                   "Rules: pred(0) = 0; pred(S(n)) = n; a ∸ 0 = a; "
                   "a ∸ S(b) = pred(a ∸ b). Evaluation order: left to right. "
                   f"{random.choice(QUERIES['predecessor_monus'])}")
        steps = []
        running = operands[0]
        for operand in operands[1:]:
            start = running
            for current in range(operand, 0, -1):
                steps.append(step("PEANO_EQ",
                                  f"{compact(start)} ∸ {compact(current)}",
                                  f"pred({compact(start)} ∸ "
                                  f"{compact(current - 1)})"))
            steps.append(step("PEANO_BASE", f"{compact(start)} ∸ 0",
                              compact(start)))
            for _ in range(operand):
                previous = running
                running = max(0, running - 1)
                steps.append(step("FOLD", f"pred({compact(previous)})",
                                  compact(running)))
        decimal = " ∸ ".join(map(str, operands))
        steps.append(step("CHECK", "decimal", f"{decimal} = {running}"))
        return problem, steps, answer_text(running)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "addition":
            problem, steps, answer = self._addition()
        elif variant == "multiplication":
            problem, steps, answer = self._multiplication()
        elif variant == "exponentiation":
            problem, steps, answer = self._exponentiation()
        elif variant == "leq_witness":
            problem, steps, answer = self._leq()
        else:
            problem, steps, answer = self._monus()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"peano_arithmetic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
