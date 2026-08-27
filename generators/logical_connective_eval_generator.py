"""Evaluate propositional connectives over independently checkable number facts.

Variants:
- ``and_or`` evaluates a conjunction or disjunction in p and q.
- ``not`` evaluates a negated proposition.
- ``nested`` evaluates a two-level formula in p, q, and r.

Atomic facts cover parity, comparison, divisibility, primality, and digit
count.  Five question phrasings and parameterized facts provide well over
1,000 distinct problem texts.

Op-codes:
- ``DIV_CHECK`` / ``CMP`` / ``COUNT``: show the arithmetic behind an atom.
- ``STMT_EVAL``: record an atomic proposition's truth value.
- ``CONNECTIVE``: evaluate one formula node after its children are known.
- ``Z``: exact composite assignment and formula value.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import And, Not, Or, Var, evaluate, render


FOUNDATIONS = True


QUERIES = (
    "Find the truth value of the expression.",
    "Evaluate the expression from the stated number facts.",
    "Decide whether the displayed compound statement is true or false.",
    "Check each proposition, then evaluate the logical expression.",
    "Determine p, q, and any r first; then give the expression's value.",
)


def _is_prime(value):
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


class LogicalConnectiveEvalGenerator(ProblemGenerator):
    """Generate arithmetic atoms and a forced connective-evaluation trace."""

    VARIANTS = ("and_or", "not", "nested")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _atomic_fact():
        kind = random.choice(("parity", "comparison", "divisibility",
                              "prime", "digits"))
        steps = []
        if kind == "parity":
            value = random.randint(2, 99)
            property_name = random.choice(("even", "odd"))
            truth = (value % 2 == 0) if property_name == "even" else (value % 2 == 1)
            description = f"{value} is {property_name}"
            steps.append(("DIV_CHECK", value, 2, f"remainder {value % 2}"))
        elif kind == "comparison":
            left, right = random.sample(range(2, 80), 2)
            relation = random.choice(("greater than", "less than"))
            truth = left > right if relation == "greater than" else left < right
            description = f"{left} is {relation} {right}"
            actual = ">" if left > right else "<"
            steps.append(("CMP", left, right, actual))
        elif kind == "divisibility":
            value = random.randint(4, 90)
            divisor = random.randint(2, 10)
            truth = value % divisor == 0
            description = f"{value} is divisible by {divisor}"
            steps.append(("DIV_CHECK", value, divisor,
                          f"quotient {value // divisor}, remainder {value % divisor}"))
        elif kind == "prime":
            value = random.randint(1, 50)
            truth = _is_prime(value)
            description = f"{value} is prime"
            if value < 2:
                steps.append(("CMP", value, 2, "<"))
            else:
                for divisor in range(2, math.isqrt(value) + 1):
                    steps.append(("DIV_CHECK", value, divisor,
                                  f"remainder {value % divisor}"))
                    if value % divisor == 0:
                        break
        else:
            value = random.randint(1, 999)
            claimed = random.choice((1, 2, 3))
            actual = len(str(value))
            truth = actual == claimed
            description = f"{value} has {claimed} digits"
            steps.append(("COUNT", f"digits of {value}", actual, ""))
        return description, truth, steps

    @staticmethod
    def _formula(variant):
        p, q, r = Var("p"), Var("q"), Var("r")
        if variant == "not":
            formula = Not(random.choice((p, q)))
            return formula, [formula], ("p", "q")
        if variant == "and_or":
            formula = random.choice((And(p, q), Or(p, q)))
            return formula, [formula], ("p", "q")
        choices = (
            (Or(And(p, Not(q)), r), (Not(q), And(p, Not(q)))),
            (And(Or(p, q), Not(r)), (Or(p, q), Not(r))),
            (Or(Not(p), And(q, r)), (Not(p), And(q, r))),
            (And(Not(p), Or(q, Not(r))), (Not(p), Not(r), Or(q, Not(r)))),
        )
        formula, inner = random.choice(choices)
        return formula, list(inner) + [formula], ("p", "q", "r")

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        formula, evaluation_order, names = self._formula(variant)
        facts = {name: self._atomic_fact() for name in names}
        assignment = {name: facts[name][1] for name in names}
        lets = " ".join(
            f"Let {name}: {facts[name][0]}." for name in names
        )
        formula_text = render(formula)
        problem = (
            f"{lets} Evaluate {formula_text}. {random.choice(QUERIES)}"
        )

        steps = []
        for name in names:
            description, truth, arithmetic = facts[name]
            for op, x, y, z in arithmetic:
                steps.append(step(op, x, y, z))
            steps.append(step("STMT_EVAL", name, description,
                              "T" if truth else "F"))
        for subformula in evaluation_order:
            steps.append(step("CONNECTIVE", render(subformula),
                              "T" if evaluate(subformula, assignment) else "F"))

        answer_parts = [f"{name} = {'T' if assignment[name] else 'F'}"
                        for name in names]
        answer_parts.append(
            f"{formula_text} = {'T' if evaluate(formula, assignment) else 'F'}"
        )
        answer = "; ".join(answer_parts)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"logical_connective_eval_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
