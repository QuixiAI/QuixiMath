"""Evaluate nested finite-set expressions one operation at a time.

Variants:
- ``with_complement`` combines relative complements with binary operations.
- ``two_step`` contains exactly two binary set operations.
- ``three_step`` contains exactly three binary set operations.
- ``symmetric_difference`` centers ``Δ`` in a two- or three-step expression.

Op-codes:
- ``SET_SETUP``: define the universe and the three named sets.
- ``SUBEXPR``: evaluate the next deepest-leftmost operation.
- ``ELEMENT_SCAN``: test one universe element in that operation.
- ``REWRITE``: replace the evaluated subexpression in the whole expression.
- ``Z``: exact sorted result roster (or ``∅``).
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import roster


FOUNDATIONS = True


QUERIES = {
    "with_complement": (
        "Evaluate the complemented set expression from the inside out.",
        "Take every complement relative to U and reduce one operation at a time.",
        "Compute the expression, showing each complement and binary operation.",
        "Use U for complements and give the final canonical roster.",
        "Follow the parentheses and complement marks to evaluate the expression.",
    ),
    "two_step": (
        "Evaluate the two-step expression from the inside out.",
        "Compute the parenthesized operation, rewrite, and finish.",
        "Reduce both set operations in the forced order.",
        "Show the intermediate roster before giving the final result.",
        "Scan U for each of the two operations and evaluate the expression.",
    ),
    "three_step": (
        "Evaluate all three operations from the deepest-leftmost one outward.",
        "Reduce this three-step set expression in the stated order.",
        "Show every intermediate roster and current-expression rewrite.",
        "Follow the parentheses through three set operations.",
        "Scan U at each stage and give the final sorted roster.",
    ),
    "symmetric_difference": (
        "Evaluate the expression and treat Δ as membership in exactly one side.",
        "Compute the symmetric difference after its inner operation.",
        "Reduce the Δ expression from the inside out.",
        "Use element scans to evaluate the symmetric-difference expression.",
        "Find the elements on exactly one side at the Δ stage.",
    ),
}


SYMBOLS = {"union": "∪", "inter": "∩", "diff": "−", "symdiff": "Δ"}


def name(value):
    return ("name", value)


def comp(value):
    return ("comp", value)


def binary(kind, left, right):
    return (kind, left, right)


A, B, C = name("A"), name("B"), name("C")

EXPRESSIONS = {
    "with_complement": (
        binary("inter", comp(binary("union", A, B)), C),
        binary("inter", A, comp(binary("diff", B, C))),
        binary("diff", binary("symdiff", A, comp(B)), C),
        binary("union", comp(A), binary("inter", B, C)),
        binary("symdiff", comp(binary("inter", A, B)), C),
    ),
    "two_step": (
        binary("inter", binary("union", A, B), C),
        binary("diff", A, binary("inter", B, C)),
        binary("union", binary("symdiff", A, B), C),
        binary("inter", A, binary("union", B, C)),
        binary("symdiff", binary("diff", A, B), C),
    ),
    "three_step": (
        binary("symdiff", binary("diff", binary("union", A, B), C), A),
        binary("union", binary("inter", A, B), binary("diff", C, A)),
        binary("symdiff", A, binary("diff", binary("union", B, C), A)),
        binary("union", binary("diff", A, binary("inter", B, C)), C),
        binary("inter", binary("union", A, B), binary("symdiff", C, A)),
    ),
    "symmetric_difference": (
        binary("symdiff", A, binary("diff", B, C)),
        binary("symdiff", binary("union", A, B), C),
        binary("symdiff", A, binary("inter", B, C)),
        binary("symdiff", binary("symdiff", A, B), C),
        binary("symdiff", binary("diff", A, B), binary("diff", C, A)),
    ),
}


def render(node, top=True):
    kind = node[0]
    if kind == "name":
        return node[1]
    if kind == "literal":
        return roster(node[1])
    if kind == "comp":
        child = render(node[1], False)
        return f"{child}ᶜ"
    text = f"{render(node[1], False)} {SYMBOLS[kind]} {render(node[2], False)}"
    return text if top else f"({text})"


def evaluate(node, env, universe):
    kind = node[0]
    if kind == "name":
        return frozenset(env[node[1]])
    if kind == "literal":
        return node[1]
    if kind == "comp":
        return universe - evaluate(node[1], env, universe)
    left, right = evaluate(node[1], env, universe), evaluate(node[2], env, universe)
    if kind == "union":
        return left | right
    if kind == "inter":
        return left & right
    if kind == "diff":
        return left - right
    if kind == "symdiff":
        return left ^ right
    raise ValueError(f"unknown set operation {kind}")


def is_atom(node):
    return node[0] in ("name", "literal")


def first_ready(node, path=()):
    kind = node[0]
    if is_atom(node):
        return None
    if kind == "comp":
        child_ready = first_ready(node[1], path + (1,))
        if child_ready is not None:
            return child_ready
        return path, node
    left_ready = first_ready(node[1], path + (1,))
    if left_ready is not None:
        return left_ready
    right_ready = first_ready(node[2], path + (2,))
    if right_ready is not None:
        return right_ready
    return path, node


def replace_at(node, path, replacement):
    if not path:
        return replacement
    index = path[0]
    values = list(node)
    values[index] = replace_at(values[index], path[1:], replacement)
    return tuple(values)


class SetExpressionGenerator(ProblemGenerator):
    """Generate nested set evaluation records over a stated finite universe."""

    VARIANTS = ("with_complement", "two_step", "three_step",
                "symmetric_difference")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _proper_subset(universe):
        return frozenset(random.sample(tuple(universe),
                                       random.randint(2, len(universe) - 2)))

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        universe = frozenset(range(1, random.randint(8, 16) + 1))
        env = {key: self._proper_subset(universe) for key in "ABC"}
        expression = random.choice(EXPRESSIONS[variant])
        problem = (f"U = {roster(universe)}. A = {roster(env['A'])}. "
                   f"B = {roster(env['B'])}. C = {roster(env['C'])}. "
                   f"Expression: {render(expression)}. "
                   f"{random.choice(QUERIES[variant])}")
        steps = [step("SET_SETUP", f"U = {roster(universe)}",
                      f"A = {roster(env['A'])}", f"B = {roster(env['B'])}",
                      f"C = {roster(env['C'])}")]
        current = expression
        while not is_atom(current):
            path, subexpression = first_ready(current)
            result = evaluate(subexpression, env, universe)
            steps.append(step("SUBEXPR", render(subexpression), roster(result)))
            kind = subexpression[0]
            if kind == "comp":
                operand = evaluate(subexpression[1], env, universe)
                for element in sorted(universe):
                    steps.append(step(
                        "ELEMENT_SCAN", element,
                        f"operand={'yes' if element in operand else 'no'}",
                        "keep" if element in result else "skip"))
            else:
                left = evaluate(subexpression[1], env, universe)
                right = evaluate(subexpression[2], env, universe)
                for element in sorted(universe):
                    steps.append(step(
                        "ELEMENT_SCAN", element,
                        f"left={'yes' if element in left else 'no'}, "
                        f"right={'yes' if element in right else 'no'}",
                        "keep" if element in result else "skip"))
            current = replace_at(current, path, ("literal", result))
            steps.append(step("REWRITE", render(current)))
        answer = roster(current[1])
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"set_expression_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
