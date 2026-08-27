"""Identify and apply elementary equality and operation properties.

Variants:
- ``identify`` names a property and verifies both sides arithmetically.
- ``apply`` rewrites an expression with a requested property.
- ``equality_chain`` follows substitution/transitivity to a numeric value.

Five phrasings per variant and randomized hand-friendly operands yield well
over 1,000 problem texts.

Op-codes:
- ``PROPERTY_MATCH``: match a named property schema to the concrete instance.
- ``REWRITE``: show the requested equivalent expression.
- ``A`` / ``M``: make every arithmetic action explicit.
- ``CHECK``: compare the two evaluated sides or confirm an equality chain.
- ``Z``: exact composite answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "identify": (
        "Name the property that justifies this equality.",
        "Which operation property is illustrated?",
        "Identify the property and verify the common value.",
        "State why the two sides are equal, then evaluate them.",
        "Give the property name together with the value of both sides.",
    ),
    "apply": (
        "Rewrite the expression using the named property.",
        "Apply the requested property and evaluate the result.",
        "Give an equivalent expression in the requested form.",
        "Use the property to rewrite, then check the value.",
        "Show the property-based rewrite and its numerical value.",
    ),
    "equality_chain": (
        "Use the equality chain to find the requested variable.",
        "Follow substitution and transitivity to determine the value.",
        "Which number must the first variable equal?",
        "Complete the chain of equal quantities.",
        "Use the given equalities to report the first variable's value.",
    ),
}


PROPERTY_NAMES = {
    "commutative_add": "commutative property of addition",
    "associative_add": "associative property of addition",
    "distributive": "distributive property",
    "identity_add": "additive identity property",
    "identity_multiply": "multiplicative identity property",
}


class OperationPropertiesGenerator(ProblemGenerator):
    """Generate structural property matches with complete arithmetic checks."""

    VARIANTS = ("identify", "apply", "equality_chain")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _case():
        kind = random.choice(tuple(PROPERTY_NAMES))
        if kind == "commutative_add":
            a, b = (random.randint(2, 99) for _ in range(2))
            left, right = f"{a} + {b}", f"{b} + {a}"
            pattern = "a + b = b + a"
            value = a + b
            arithmetic = [step("A", a, b, value), step("A", b, a, value)]
        elif kind == "associative_add":
            a, b, c = (random.randint(2, 50) for _ in range(3))
            left, right = f"({a} + {b}) + {c}", f"{a} + ({b} + {c})"
            pattern = "(a + b) + c = a + (b + c)"
            value = a + b + c
            arithmetic = [
                step("A", a, b, a + b), step("A", a + b, c, value),
                step("A", b, c, b + c), step("A", a, b + c, value),
            ]
        elif kind == "distributive":
            a = random.randint(2, 12)
            b, c = (random.randint(2, 30) for _ in range(2))
            left = f"{a} × ({b} + {c})"
            right = f"{a} × {b} + {a} × {c}"
            pattern = "a × (b + c) = a × b + a × c"
            value = a * (b + c)
            arithmetic = [
                step("A", b, c, b + c), step("M", a, b + c, value),
                step("M", a, b, a * b), step("M", a, c, a * c),
                step("A", a * b, a * c, value),
            ]
        elif kind == "identity_add":
            a = random.randint(2, 9999)
            left, right = f"{a} + 0", str(a)
            pattern = "a + 0 = a"
            value = a
            arithmetic = [step("A", a, 0, value)]
        else:
            a = random.randint(2, 9999)
            left, right = f"{a} × 1", str(a)
            pattern = "a × 1 = a"
            value = a
            arithmetic = [step("M", a, 1, value)]
        return kind, left, right, pattern, value, arithmetic

    def _identify(self):
        kind, left, right, pattern, value, arithmetic = self._case()
        equality = f"{left} = {right}"
        problem = f"Equality: {equality}. {random.choice(QUERIES['identify'])}"
        steps = [step("PROPERTY_MATCH", PROPERTY_NAMES[kind], pattern, equality)]
        steps.extend(arithmetic)
        steps.append(step("CHECK", "left", value, f"right = {value}"))
        answer = f"{PROPERTY_NAMES[kind]}; both sides = {value}"
        return problem, steps, answer

    def _apply(self):
        kind, left, right, pattern, value, arithmetic = self._case()
        property_name = PROPERTY_NAMES[kind]
        problem = (
            f"Expression: {left}. Requested property: {property_name}. "
            f"{random.choice(QUERIES['apply'])}"
        )
        steps = [step("PROPERTY_MATCH", property_name, pattern, left),
                 step("REWRITE", left, right)]
        steps.extend(arithmetic)
        steps.append(step("CHECK", left, value, f"rewrite = {value}"))
        answer = f"rewritten: {right}; value = {value}; property = {property_name}"
        return problem, steps, answer

    def _equality_chain(self):
        variables = random.sample(("a", "b", "c", "m", "n", "x", "y", "z"),
                                  random.choice((2, 3, 4)))
        value = random.randint(2, 9999)
        facts = [f"{left} = {right}"
                 for left, right in zip(variables, variables[1:])]
        facts.append(f"{variables[-1]} = {value}")
        problem = (
            f"Facts: {'; '.join(facts)}. Find {variables[0]}. "
            f"{random.choice(QUERIES['equality_chain'])}"
        )
        steps = [step("PROPERTY_MATCH", "transitive property of equality",
                      "if a = b and b = c, then a = c", "; ".join(facts))]
        for variable in reversed(variables):
            steps.append(step("REWRITE", f"{variable} = {value}"))
        steps.append(step("CHECK", variables[0], value, "chain complete"))
        answer = f"{variables[0]} = {value}; transitive property of equality"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "identify":
            problem, steps, answer = self._identify()
        elif variant == "apply":
            problem, steps, answer = self._apply()
        else:
            problem, steps, answer = self._equality_chain()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"operation_properties_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
