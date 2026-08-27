"""Rewrite formulas with named equivalence laws and exact current expressions.

Variants:
- ``simplify`` reverses 2–4 laws from a stated canonical target family.
- ``to_cnf`` performs a forced OR-over-AND distribution.
- ``to_dnf`` performs a forced AND-over-OR distribution.
- ``nand_only`` recursively replaces NOT/AND/OR by Sheffer NAND ``↑``.
- ``implication_free`` eliminates every ``→`` and ``↔`` in forced order.

All rewrites end with a truth-column check.  Random subformulas, inverse-law
paths, and five phrasings provide more than 100,000 problem texts.

Op-codes:
- ``LAW``: name one law and show its local before/after expressions.
- ``REWRITE``: display the whole current expression after that move.
- ``CHECK``: compare exact truth columns of source and answer.
- ``Z``: exact canonical target.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, FALSE, Imp, Nand, Not, Or, TRUE, Var, Xor,
                          assignments, evaluate, obfuscate, positions,
                          random_formula, render, replace_at, simplify,
                          variables)


FOUNDATIONS = True


p, q, r = Var("p"), Var("q"), Var("r")
TARGETS = (p, Not(p), And(p, q), Or(p, q), Imp(p, q), Xor(p, q), TRUE, FALSE,
           And(And(p, q), r), Or(Or(p, q), r))

QUERIES = {
    "simplify": ("Simplify to the equivalent member of the stated target family.",
                 "Apply the named laws in forced order and identify the target.",
                 "Reduce the formula law by law to its canonical family member.",
                 "Find the unique equivalent target and show every rewrite.",
                 "Use equivalence laws to reach the canonical result."),
    "to_cnf": ("Distribute ∨ over ∧ to obtain CNF.",
               "Apply the stated distribution and give conjunctive normal form.",
               "Rewrite the formula as a conjunction of disjunction clauses.",
               "Perform the forced CNF distribution.",
               "Convert this expression to CNF with one named law step."),
    "to_dnf": ("Distribute ∧ over ∨ to obtain DNF.",
               "Apply the stated distribution and give disjunctive normal form.",
               "Rewrite the formula as a disjunction of conjunction terms.",
               "Perform the forced DNF distribution.",
               "Convert this expression to DNF with one named law step."),
    "nand_only": ("Rewrite the formula using ↑ only.",
                  "Replace every connective by the stated Sheffer identities.",
                  "Convert the expression to an equivalent ↑-only formula.",
                  "Eliminate ¬, ∧, and ∨ in favor of ↑.",
                  "Give the recursive Sheffer-only rewrite."),
    "implication_free": ("Eliminate every implication and biconditional.",
                         "Rewrite the formula using only ¬, ∧, and ∨.",
                         "Apply implication elimination in forced order.",
                         "Remove → and ↔ one occurrence at a time.",
                         "Give the equivalent implication-free expression."),
}


def truth_column(formula, names=None):
    names = variables(formula) if names is None else tuple(sorted(names))
    return "".join("T" if evaluate(formula, row) else "F"
                   for row in assignments(names))


def _is_nand_fragment(formula):
    if isinstance(formula, Var):
        return True
    if isinstance(formula, Nand):
        return (_is_nand_fragment(formula.left)
                and _is_nand_fragment(formula.right))
    return False


def nand_convert(formula):
    """Convert the leftmost ready subformula after its children (postorder)."""
    current = formula
    trace = []
    while not _is_nand_fragment(current):
        chosen = None
        for path, node in positions(current):
            if isinstance(node, Not) and _is_nand_fragment(node.arg):
                chosen = (path, node)
                break
            if (isinstance(node, (And, Or))
                    and _is_nand_fragment(node.left)
                    and _is_nand_fragment(node.right)):
                chosen = (path, node)
                break
        if chosen is None:
            raise ValueError("nand conversion expects only ¬, ∧, ∨")
        path, before = chosen
        if isinstance(before, Not):
            law = "Sheffer negation"
            after = Nand(before.arg, before.arg)
        elif isinstance(before, And):
            law = "Sheffer conjunction"
            joined = Nand(before.left, before.right)
            after = Nand(joined, joined)
        else:
            law = "Sheffer disjunction"
            after = Nand(Nand(before.left, before.left),
                         Nand(before.right, before.right))
        current = replace_at(current, path, after)
        trace.append((law, before, after, current))
    return current, trace


class LogicalEquivalenceLawsGenerator(ProblemGenerator):
    """Generate forced law traces whose answers are independently truth-checkable."""

    VARIANTS = ("simplify", "to_cnf", "to_dnf", "nand_only",
                "implication_free")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _literal():
        atom = Var(random.choice(("p", "q", "r", "s", "t", "u")))
        return Not(atom) if random.choice((True, False)) else atom

    def _simplify(self):
        while True:
            target = random.choice(TARGETS)
            try:
                source = obfuscate(target, steps=random.randint(2, 4))
            except ValueError:
                continue
            rewrites = simplify(source, target=target)
            if rewrites and rewrites[-1].whole_after == target:
                break
        family_text = "; ".join(render(item) for item in TARGETS)
        problem = (f"Formula: {render(source)}. Target family: {family_text}. "
                   f"{random.choice(QUERIES['simplify'])}")
        steps = []
        for rewrite in rewrites:
            steps.append(step("LAW", rewrite.law, render(rewrite.before),
                              render(rewrite.after)))
            steps.append(step("REWRITE", render(rewrite.whole_after)))
        return source, target, problem, steps

    def _normal_form(self, variant):
        first, second, third = self._literal(), self._literal(), self._literal()
        if variant == "to_cnf":
            if random.choice((True, False)):
                source = Or(first, And(second, third))
                target = And(Or(first, second), Or(first, third))
            else:
                source = Or(And(second, third), first)
                target = And(Or(second, first), Or(third, first))
            law = "distributive ∨ over ∧"
        else:
            if random.choice((True, False)):
                source = And(first, Or(second, third))
                target = Or(And(first, second), And(first, third))
            else:
                source = And(Or(second, third), first)
                target = Or(And(second, first), And(third, first))
            law = "distributive ∧ over ∨"
        problem = f"Formula: {render(source)}. {random.choice(QUERIES[variant])}"
        steps = [step("LAW", law, render(source), render(target)),
                 step("REWRITE", render(target))]
        return source, target, problem, steps

    def _nand_only(self):
        source = random_formula(depth=3, names=("p", "q", "r"),
                                connectives=("¬", "∧", "∨"),
                                exact_depth=True, use_all=True)
        target, trace = nand_convert(source)
        problem = f"Formula: {render(source)}. {random.choice(QUERIES['nand_only'])}"
        steps = []
        for law, before, after, whole_after in trace:
            steps.append(step("LAW", law, render(before), render(after)))
            steps.append(step("REWRITE", render(whole_after)))
        return source, target, problem, steps

    def _implication_free(self):
        while True:
            source = random_formula(depth=3, names=("p", "q", "r"),
                                    connectives=("¬", "∧", "∨", "→", "↔"),
                                    exact_depth=True, use_all=True)
            rewrites = simplify(source, order=("biconditional elimination",
                                               "implication elimination"))
            if rewrites:
                target = rewrites[-1].whole_after
                break
        problem = (f"Formula: {render(source)}. "
                   f"{random.choice(QUERIES['implication_free'])}")
        steps = []
        for rewrite in rewrites:
            steps.append(step("LAW", rewrite.law, render(rewrite.before),
                              render(rewrite.after)))
            steps.append(step("REWRITE", render(rewrite.whole_after)))
        return source, target, problem, steps

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "simplify":
            source, target, problem, steps = self._simplify()
        elif variant in ("to_cnf", "to_dnf"):
            source, target, problem, steps = self._normal_form(variant)
        elif variant == "nand_only":
            source, target, problem, steps = self._nand_only()
        else:
            source, target, problem, steps = self._implication_free()
        names = sorted(set(variables(source)) | set(variables(target)))
        source_column = truth_column(source, names)
        target_column = truth_column(target, names)
        steps.append(step("CHECK", "truth columns", source_column, target_column))
        answer = render(target)
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"logical_equivalence_laws_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
