"""Build propositional truth-table columns one row and subformula at a time.

Variants:
- ``column`` computes the result column of a 2–3 variable formula.
- ``classify`` labels it tautology, contradiction, or contingency.
- ``equivalence`` compares two formulas and gives the first differing row.
- ``two_variable`` provides a deliberately smaller p/q entry point.

Random canonical formulas through depth three and five phrasings give a
problem space above 100,000.

Op-codes:
- ``TT_SETUP``: fix variables and canonical row order.
- ``TRUTH_ROW``: begin one concrete truth assignment.
- ``EVAL_SUB``: evaluate one subformula after its children.
- ``TT_COLUMN``: collect a formula's result column.
- ``CLASSIFY``: classify a completed column.
- ``COUNTEREXAMPLE``: record the first row on which formulas differ.
- ``Z``: exact column or composite verdict.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, Not, Or, equivalent, evaluate, first_difference,
                          random_formula, render, variables)


FOUNDATIONS = True


QUERIES = {
    "column": ("Compute the result column.",
               "Evaluate the formula on every row and give its column.",
               "Build the truth-table output in the stated row order.",
               "Find the sequence of T and F values for the formula.",
               "Complete the formula column."),
    "classify": ("Classify the formula and include its result column.",
                 "Decide whether it is a tautology, contradiction, or contingency.",
                 "Use the completed column to classify the formula.",
                 "Give the truth classification together with the column.",
                 "Evaluate all rows, then state the formula type."),
    "equivalence": ("Decide whether the formulas are equivalent.",
                    "Compare their columns and give the first differing row if any.",
                    "Test logical equivalence row by row.",
                    "Determine whether both formulas have the same truth table.",
                    "Give an equivalence verdict with its column or counterexample."),
    "two_variable": ("Compute the two-variable result column.",
                     "Evaluate the four canonical p/q rows.",
                     "Complete this introductory truth table.",
                     "Give the formula values in TT, TF, FT, FF order.",
                     "Find the four-entry output column."),
}


def assignments(names):
    return [dict(zip(names, bits))
            for bits in itertools.product((True, False), repeat=len(names))]


def row_text(assignment, names):
    return ", ".join(f"{name}={'T' if assignment[name] else 'F'}" for name in names)


def column(formula, names):
    return "".join("T" if evaluate(formula, row) else "F"
                   for row in assignments(names))


def postorder_subformulas(formula):
    ordered = []
    seen = set()

    def visit(node):
        if hasattr(node, "arg"):
            visit(node.arg)
        elif hasattr(node, "left"):
            visit(node.left)
            visit(node.right)
        text = render(node)
        if text not in seen and (hasattr(node, "arg") or hasattr(node, "left")):
            seen.add(text)
            ordered.append(node)

    visit(formula)
    return ordered


class TruthTableGenerator(ProblemGenerator):
    """Generate canonical truth tables with independent per-node evaluations."""

    VARIANTS = ("column", "classify", "equivalence", "two_variable")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _formula(names, max_depth=3):
        return random_formula(depth=max_depth, names=names,
                              connectives=("¬", "∧", "∨", "→", "↔"),
                              exact_depth=True, use_all=True)

    @staticmethod
    def _table_steps(formula, names, label="formula"):
        rows = assignments(names)
        steps = [step("TT_SETUP", f"variables {', '.join(names)}", len(rows))]
        for index, assignment in enumerate(rows, 1):
            row = row_text(assignment, names)
            steps.append(step("TRUTH_ROW", f"row {index}", row))
            for subformula in postorder_subformulas(formula):
                steps.append(step("EVAL_SUB", row,
                                  f"{label}: {render(subformula)}",
                                  "T" if evaluate(subformula, assignment) else "F"))
        result = column(formula, names)
        steps.append(step("TT_COLUMN", label, result))
        return steps, result

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        names = ("p", "q") if variant == "two_variable" else tuple(
            ("p", "q", "r")[:random.choice((2, 3))]
        )
        formula = self._formula(names, 3)
        if variant == "classify":
            target = random.choice(("tautology", "contradiction", "contingency"))
            if target == "tautology":
                formula = Or(formula, Not(formula))
            elif target == "contradiction":
                formula = And(formula, Not(formula))
            else:
                while len(set(column(formula, names))) != 2:
                    formula = self._formula(names)
        row_order = ", ".join(
            "".join("T" if row[name] else "F" for name in names)
            for row in assignments(names)
        )
        if variant == "equivalence":
            if random.choice((True, False)):
                second = Not(Not(formula))
            else:
                second = self._formula(names)
                while equivalent(formula, second):
                    second = self._formula(names)
            problem = (
                f"Formula 1: {render(formula)}. Formula 2: {render(second)}. "
                f"Variables: {', '.join(names)}. Row order: {row_order}. "
                f"{random.choice(QUERIES[variant])}"
            )
            steps, first_column = self._table_steps(formula, names, "formula 1")
            second_steps, second_column = self._table_steps(second, names, "formula 2")
            steps.extend(second_steps)
            if first_column == second_column:
                answer = f"equivalent; column {first_column}"
            else:
                differing = first_difference(formula, second)
                witness = row_text(differing, names)
                steps.append(step("COUNTEREXAMPLE", witness,
                                  f"formula 1={'T' if evaluate(formula, differing) else 'F'}",
                                  f"formula 2={'T' if evaluate(second, differing) else 'F'}"))
                answer = f"not equivalent; differ at {witness}"
        else:
            problem = (
                f"Formula: {render(formula)}. Variables: {', '.join(names)}. "
                f"Row order: {row_order}. {random.choice(QUERIES[variant])}"
            )
            steps, result = self._table_steps(formula, names)
            if variant == "classify":
                if set(result) == {"T"}:
                    classification = "tautology"
                elif set(result) == {"F"}:
                    classification = "contradiction"
                else:
                    classification = "contingency"
                steps.append(step("CLASSIFY", classification,
                                  f"T at {result.count('T')} of {len(result)} rows"))
                answer = f"{classification}; {result}"
            else:
                answer = result
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"truth_table_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
