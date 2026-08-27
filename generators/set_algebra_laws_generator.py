"""Rewrite symbolic set expressions with named algebra laws.

Variants:
- ``simplify`` reverses 2–4 laws from a pairwise-distinct target family.
- ``dual_of_logic`` translates a propositional identity under ``p↦A``.
- ``to_union_of_intersections`` performs a forced distribution step.

Op-codes:
- ``LAW``: name one set law and show its local before/after expressions.
- ``REWRITE``: display the complete current expression after that law.
- ``CHECK``: compare exact eight-row membership columns.
- ``Z``: exact canonical target expression in the set dialect.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, FALSE, Not, Or, SET, SET_LAW_ORDER, TRUE, Var,
                          assignments, evaluate, obfuscate, rename, render,
                          simplify, variables)


FOUNDATIONS = True


SET_NAMES = tuple("ABCDEGHJKLMNPQRSTVWXYZ")

QUERIES = {
    "simplify": (
        "Simplify to the equivalent member of the stated target family.",
        "Apply the named set laws in forced order and identify the target.",
        "Reduce the expression law by law to its canonical family member.",
        "Find the unique equivalent target and show every rewrite.",
        "Use set-algebra laws to reach the canonical result.",
    ),
    "dual_of_logic": (
        "Translate the logic identity and give the simplified set expression.",
        "Use the stated proposition-to-set correspondence to apply the law.",
        "Read the Boolean identity in the set dialect and simplify.",
        "Apply the logic/set duality to the displayed expression.",
        "Give the set-algebra target corresponding to the logic identity.",
    ),
    "to_union_of_intersections": (
        "Distribute ∩ over ∪ to obtain a union of intersections.",
        "Apply the forced distribution and give the expanded set form.",
        "Rewrite the expression as a union of intersection terms.",
        "Perform the stated set-distributive law once.",
        "Convert this expression to union-of-intersections form.",
    ),
}


def target_family(first, second, third):
    return (first, Not(first), And(first, second), Or(first, second),
            TRUE, FALSE, And(And(first, second), third),
            Or(Or(first, second), third))


def membership_column(formula, names):
    return "".join("1" if evaluate(formula, row) else "0"
                   for row in assignments(names))


p, q = Var("p"), Var("q")
DUAL_TEMPLATES = (
    (And(p, Or(p, q)), p, "absorption"),
    (Or(p, And(p, q)), p, "absorption"),
    (Not(And(p, q)), Or(Not(p), Not(q)), "De Morgan"),
    (Not(Or(p, q)), And(Not(p), Not(q)), "De Morgan"),
    (And(p, p), p, "idempotent"),
    (Or(p, p), p, "idempotent"),
    (And(p, TRUE), p, "identity"),
    (Or(p, FALSE), p, "identity"),
)


class SetAlgebraLawsGenerator(ProblemGenerator):
    """Generate forced set-law traces with independent membership checks."""

    VARIANTS = ("simplify", "dual_of_logic", "to_union_of_intersections")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _simplify(self, names):
        first, second, third = map(Var, names)
        family = target_family(first, second, third)
        while True:
            target = random.choice(family)
            try:
                source = obfuscate(
                    target, steps=random.randint(2, 4), order=SET_LAW_ORDER,
                    pool=[first, second, third],
                )
            except ValueError:
                continue
            rewrites = simplify(source, order=SET_LAW_ORDER, target=target)
            if rewrites and rewrites[-1].whole_after == target:
                break
        family_text = "; ".join(render(item, SET) for item in family)
        problem = (f"Set names: {', '.join(names)} are arbitrary subsets of U. "
                   f"Expression: {render(source, SET)}. "
                   f"Target family: {family_text}. "
                   f"{random.choice(QUERIES['simplify'])}")
        steps = []
        for rewrite in rewrites:
            law, before, after = rewrite.triple(SET)
            steps.append(step("LAW", law, before, after))
            steps.append(step("REWRITE", render(rewrite.whole_after, SET)))
        return source, target, problem, steps

    def _dual(self, names):
        abstract_source, abstract_target, law = random.choice(DUAL_TEMPLATES)
        mapping = {"p": names[0], "q": names[1]}
        source = rename(abstract_source, mapping)
        target = rename(abstract_target, mapping)
        problem = (f"Set names: {', '.join(names)} are arbitrary subsets of U. "
                   f"Correspondence: p↦{names[0]}, q↦{names[1]}. "
                   f"Logic identity: {render(abstract_source)} ≡ "
                   f"{render(abstract_target)}. Set expression: {render(source, SET)}. "
                   f"{random.choice(QUERIES['dual_of_logic'])}")
        steps = [step("LAW", law, render(source, SET), render(target, SET)),
                 step("REWRITE", render(target, SET))]
        return source, target, problem, steps

    def _distribution(self, names):
        first, second, third = map(Var, names)
        literals = [first, second, third]
        literals = [Not(item) if random.choice((True, False)) else item
                    for item in literals]
        if random.choice((True, False)):
            source = And(literals[0], Or(literals[1], literals[2]))
            target = Or(And(literals[0], literals[1]),
                        And(literals[0], literals[2]))
        else:
            source = And(Or(literals[1], literals[2]), literals[0])
            target = Or(And(literals[1], literals[0]),
                        And(literals[2], literals[0]))
        problem = (f"Set names: {', '.join(names)} are arbitrary subsets of U. "
                   f"Expression: {render(source, SET)}. "
                   f"{random.choice(QUERIES['to_union_of_intersections'])}")
        steps = [step("LAW", "distributive ∩ over ∪", render(source, SET),
                      render(target, SET)), step("REWRITE", render(target, SET))]
        return source, target, problem, steps

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        names = random.sample(SET_NAMES, 3)
        if variant == "simplify":
            source, target, problem, steps = self._simplify(names)
        elif variant == "dual_of_logic":
            source, target, problem, steps = self._dual(names)
        else:
            source, target, problem, steps = self._distribution(names)
        check_names = sorted(set(variables(source)) | set(variables(target))
                             | set(names))
        source_column = membership_column(source, check_names)
        target_column = membership_column(target, check_names)
        steps.append(step("CHECK", "membership columns", source_column,
                          target_column))
        answer = render(target, SET)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"set_algebra_laws_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
