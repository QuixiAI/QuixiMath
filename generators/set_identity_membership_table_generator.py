"""Verify or refute set identities with complete membership tables.

Variants:
- ``verify_identity`` samples the full bank of true identities.
- ``refute_identity`` perturbs one connective in a true identity.
- ``de_morgan`` uses the two complement laws.
- ``distributive`` uses the two distributive laws.
- ``difference_laws`` uses difference and symmetric-difference identities.

Op-codes:
- ``MEMBER_ROW``: state one of the eight membership assignments.
- ``EVAL_SUB``: evaluate a non-atomic subexpression on that row.
- ``SIDE``: record the left or right membership result.
- ``TABLE_COMPARE``: report matching columns or the first differing row.
- ``Z``: composite identity verdict and counterexample row when needed.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


SET_NAMES = tuple("ABCDEGHJKLMNPQRSTVWXYZ")
SYMBOLS = {"union": "∪", "inter": "∩", "diff": "−", "symdiff": "Δ"}

QUERIES = {
    "verify_identity": (
        "Use the eight-row membership table to verify or refute the claim.",
        "Compare the two membership columns for all possible element statuses.",
        "Determine whether this equation is an identity of arbitrary sets.",
        "Build the complete membership table and classify the claim.",
        "Test every membership row and report whether the columns match.",
    ),
    "refute_identity": (
        "Find the first membership row that refutes the perturbed claim.",
        "Use a complete table to expose the changed connective.",
        "Determine why this near-identity fails for arbitrary sets.",
        "Compare the columns and give the first counterexample row.",
        "Refute the claim by its earliest differing membership assignment.",
    ),
    "de_morgan": (
        "Verify this De Morgan identity with all eight membership rows.",
        "Check the complement law by comparing both membership columns.",
        "Use a membership table to establish the De Morgan equation.",
        "Evaluate both sides of this complement identity row by row.",
        "Confirm the stated De Morgan law for arbitrary subsets of U.",
    ),
    "distributive": (
        "Verify the distributive identity with a membership table.",
        "Compare both sides of the distribution on all eight rows.",
        "Use element membership to establish the distributive law.",
        "Check every row of this set-distribution equation.",
        "Determine whether the two distributed expressions always agree.",
    ),
    "difference_laws": (
        "Verify this difference law by its complete membership table.",
        "Check both sides of the set-difference equation row by row.",
        "Use the eight element-status cases to classify the difference claim.",
        "Compare the membership columns of these difference expressions.",
        "Determine whether this difference identity holds for arbitrary sets.",
    ),
}


def name(value):
    return ("name", value)


def comp(value):
    return ("comp", value)


def op(kind, left, right):
    return (kind, left, right)


def render(node, top=True):
    if node[0] == "name":
        return node[1]
    if node[0] == "comp":
        return f"{render(node[1], False)}ᶜ"
    text = f"{render(node[1], False)} {SYMBOLS[node[0]]} {render(node[2], False)}"
    return text if top else f"({text})"


def evaluate(node, row):
    kind = node[0]
    if kind == "name":
        return row[node[1]]
    if kind == "comp":
        return not evaluate(node[1], row)
    left, right = evaluate(node[1], row), evaluate(node[2], row)
    if kind == "union":
        return left or right
    if kind == "inter":
        return left and right
    if kind == "diff":
        return left and not right
    if kind == "symdiff":
        return left != right
    raise ValueError(f"unknown set operation {kind}")


def operation_nodes(node):
    if node[0] == "name":
        return []
    if node[0] == "comp":
        return operation_nodes(node[1]) + [node]
    return operation_nodes(node[1]) + operation_nodes(node[2]) + [node]


def identity_bank(first, second, third):
    a, b, c = map(name, (first, second, third))
    de_morgan = (
        (comp(op("union", a, b)), op("inter", comp(a), comp(b))),
        (comp(op("inter", a, b)), op("union", comp(a), comp(b))),
    )
    distributive = (
        (op("inter", a, op("union", b, c)),
         op("union", op("inter", a, b), op("inter", a, c))),
        (op("union", a, op("inter", b, c)),
         op("inter", op("union", a, b), op("union", a, c))),
    )
    difference = (
        (op("diff", a, op("union", b, c)),
         op("inter", op("diff", a, b), op("diff", a, c))),
        (op("diff", a, op("inter", b, c)),
         op("union", op("diff", a, b), op("diff", a, c))),
        (op("diff", op("union", a, b), c),
         op("union", op("diff", a, c), op("diff", b, c))),
        (op("diff", op("inter", a, b), c),
         op("inter", op("diff", a, c), op("diff", b, c))),
        (op("diff", a, op("diff", b, c)),
         op("union", op("diff", a, b), op("inter", a, c))),
        (op("symdiff", a, b),
         op("union", op("diff", a, b), op("diff", b, a))),
    )
    refuted = (
        (de_morgan[0][0], op("union", comp(a), comp(b))),
        (de_morgan[1][0], op("inter", comp(a), comp(b))),
        (distributive[0][0],
         op("inter", op("inter", a, b), op("inter", a, c))),
        (distributive[1][0],
         op("union", op("union", a, b), op("union", a, c))),
        (difference[0][0],
         op("union", op("diff", a, b), op("diff", a, c))),
        (difference[1][0],
         op("inter", op("diff", a, b), op("diff", a, c))),
        (difference[2][0],
         op("inter", op("diff", a, c), op("diff", b, c))),
        (difference[-1][0],
         op("inter", op("diff", a, b), op("diff", b, a))),
    )
    return {"de_morgan": de_morgan, "distributive": distributive,
            "difference_laws": difference,
            "verify_identity": de_morgan + distributive + difference,
            "refute_identity": refuted}


def row_text(row, spaced=False):
    if spaced:
        return ", ".join(
            f"x {'∈' if row[name] else '∉'} {name}" for name in sorted(row))
    return ", ".join(
        f"x{'∈' if row[name] else '∉'}{name}" for name in sorted(row))


class SetIdentityMembershipTableGenerator(ProblemGenerator):
    """Generate exact eight-row membership proofs and refutations."""

    VARIANTS = ("verify_identity", "refute_identity", "de_morgan",
                "distributive", "difference_laws")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        chosen = random.sample(SET_NAMES, 3)
        left, right = random.choice(identity_bank(*chosen)[variant])
        problem = (f"Set names: {', '.join(chosen)} are arbitrary subsets of U. "
                   f"Claim: {render(left)} = {render(right)}. "
                   f"{random.choice(QUERIES[variant])}")
        names = sorted(chosen)
        steps = []
        first_difference = None
        for values in itertools.product((True, False), repeat=3):
            row = dict(zip(names, values))
            compact = row_text(row)
            steps.append(step("MEMBER_ROW", compact))
            for side, expression in (("left", left), ("right", right)):
                for node in operation_nodes(expression):
                    steps.append(step("EVAL_SUB", compact, render(node),
                                      "∈" if evaluate(node, row) else "∉"))
                steps.append(step("SIDE", side,
                                  "∈" if evaluate(expression, row) else "∉"))
            if evaluate(left, row) != evaluate(right, row):
                if first_difference is None:
                    first_difference = dict(row)
        if first_difference is None:
            steps.append(step("TABLE_COMPARE", "match"))
            answer = "identity; columns match"
        else:
            failure = row_text(first_difference, spaced=True)
            steps.append(step("TABLE_COMPARE", "differ", failure))
            answer = f"not an identity; fails at {failure}"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"set_identity_membership_table_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
