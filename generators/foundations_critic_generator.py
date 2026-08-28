"""Critic records for truth tables, membership tables, and proofs.

Variants: ``truth_table_error``, ``membership_table_error``,
``missing_justification``, and ``missing_line``. Op-codes: ``VERIFY``,
``FLAG``, ``ROW``, ``CLASSIFY``, ``MEMBER_ROW``, ``TABLE_COMPARE``, ``MP``,
``APPLY``, ``CHECK``, and ``Z``. Every worked solution has exactly one seeded
error or blank, and all answers identify its numbered step.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, Imp, Not, Or, evaluate, random_formula, render,
                          variables)


FOUNDATIONS = True
FORMULA_NAMES = tuple("abcdefghjkmnpqrst")

QUERIES = {
    "truth_table_error": (
        "Find the first wrong row and repair the truth column and classification.",
        "Check the worked table in order, then correct its propagated verdict.",
        "Identify the seeded truth-value error and redo the conclusion.",
        "Audit each row and report the exact first bad step.",
        "Correct the one erroneous row and the classification based on it.",
    ),
    "membership_table_error": (
        "Find the wrong membership row and repair the identity verdict.",
        "Audit the table in order and correct its propagated conclusion.",
        "Identify the seeded membership error and redo the comparison.",
        "Check both columns row by row and report the first bad step.",
        "Correct the one false membership entry and the resulting verdict.",
    ),
    "missing_justification": (
        "Fill the blank justification and identify its numbered step.",
        "Recover the exact rule and line citations for the blank.",
        "Determine the missing natural-deduction annotation.",
        "Check the proof prefix and supply the unique justification.",
        "Report the blank step and its exact rule citation.",
    ),
    "missing_line": (
        "Reconstruct the blank formula from its stated rule and citations.",
        "Determine the unique missing derived line.",
        "Use the annotation to recover the blank proof formula.",
        "Check the cited premises and fill the numbered line.",
        "Report the blank step and its exact canonical formula.",
    ),
}


def truth_letter(value):
    return "T" if value else "F"


def assignment_text(names, values):
    return ", ".join(f"{name}={truth_letter(value)}"
                     for name, value in zip(names, values))


def roster_text(values):
    ordered = sorted(values)
    return ("∅" if not ordered else
            "{" + ", ".join(map(str, ordered)) + "}")


def random_proposition():
    names = random.sample(FORMULA_NAMES, 3)
    return random_formula(depth=random.choice((2, 3)), names=names,
                          connectives=("¬", "∧", "∨", "→"),
                          exact_depth=True, use_all=True)


def proof_instance(allow_disjunction=True):
    while True:
        first, second = random_proposition(), random_proposition()
        if render(first) != render(second):
            break
    case = random.randrange(4 if allow_disjunction else 3)
    if case == 0:
        lines = (Imp(first, second), first, second)
        justification = "MP 1,2"
    elif case == 1:
        lines = (first, second, And(first, second))
        justification = "∧I 1,2"
    elif case == 2:
        lines = (And(first, second), first)
        justification = "∧E 1"
    else:
        lines = (first, Or(first, second))
        justification = "∨I 1"
    return lines, justification


class FoundationsCriticGenerator(ProblemGenerator):
    """Generate deterministic critic exercises for the foundations strand."""

    VARIANTS = ("truth_table_error", "membership_table_error",
                "missing_justification", "missing_line")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _truth_table_error(self):
        core = random_proposition()
        correct_class = random.choice(("tautology", "contradiction"))
        formula = (Or(core, Not(core)) if correct_class == "tautology"
                   else And(core, Not(core)))
        names = variables(formula)
        rows = list(itertools.product((True, False), repeat=len(names)))
        values = [evaluate(formula, dict(zip(names, row))) for row in rows]
        bad_index = random.randrange(len(rows))
        shown_values = list(values)
        shown_values[bad_index] = not shown_values[bad_index]
        shown = [f"{index + 1}) row {assignment_text(names, row)} gives "
                 f"{truth_letter(shown_values[index])}"
                 for index, row in enumerate(rows)]
        shown.append(f"{len(rows) + 1}) classification: contingent")
        problem = ("A worked truth table has one wrong row; the final "
                   "classification follows the displayed column. "
                   f"Formula: {render(formula)}. Variable order: "
                   f"{', '.join(names)}; T rows precede F rows.\n" +
                   "\n".join(shown) + "\n" +
                   random.choice(QUERIES["truth_table_error"]))
        line = bad_index + 1
        column = "".join(truth_letter(value) for value in values)
        answer = f"step {line}; column {column}; {correct_class}"
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.append(step("FLAG", line, truth_letter(values[bad_index])))
        steps.append(step("ROW", assignment_text(names, rows[bad_index]),
                          truth_letter(values[bad_index])))
        steps.append(step("CLASSIFY", column, correct_class))
        return problem, steps, answer

    def _membership_table_error(self):
        start = random.randint(-100000, 99990)
        universe = tuple(range(start, start + random.randint(4, 8)))
        sets = {name: {value for value in universe if random.choice((True, False))}
                for name in "ABC"}
        left = {x for x in sets["A"] if x in sets["B"] or x in sets["C"]}
        right = ((sets["A"] & sets["B"]) | (sets["A"] & sets["C"]))
        bad_index = random.randrange(len(universe))
        shown = []
        for index, value in enumerate(universe):
            left_value = value in left
            right_value = value in right
            if index == bad_index:
                right_value = not right_value
            shown.append(f"{index + 1}) x={value}: left "
                         f"{truth_letter(left_value)}; right "
                         f"{truth_letter(right_value)}")
        shown.append(f"{len(universe) + 1}) verdict: not equal; differ at "
                     f"x={universe[bad_index]}")
        problem = ("A worked membership table has one wrong entry; the final "
                   "verdict follows the displayed columns. Identity: "
                   "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C). "
                   f"U={roster_text(universe)}; A={roster_text(sets['A'])}; "
                   f"B={roster_text(sets['B'])}; C={roster_text(sets['C'])}.\n" +
                   "\n".join(shown) + "\n" +
                   random.choice(QUERIES["membership_table_error"]))
        line = bad_index + 1
        value = universe[bad_index]
        correct = truth_letter(value in right)
        answer = f"step {line}; identity; columns match"
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.append(step("FLAG", line, f"right {correct}"))
        steps.append(step("MEMBER_ROW", f"x={value}",
                          f"left {correct}", f"right {correct}"))
        steps.append(step("TABLE_COMPARE", "match"))
        return problem, steps, answer

    def _proof_blank(self, justification_blank):
        formulas, justification = proof_instance(
            allow_disjunction=justification_blank)
        blank_index = len(formulas) - 1
        shown = []
        for index, formula in enumerate(formulas):
            number = index + 1
            if index < blank_index:
                shown.append(f"{number}) {render(formula)} [premise]")
            elif justification_blank:
                shown.append(f"{number}) {render(formula)} [____]")
            else:
                shown.append(f"{number}) ____ [{justification}]")
        variant = ("missing_justification" if justification_blank
                   else "missing_line")
        problem = ("Natural-deduction proof with one blank.\n" +
                   "\n".join(shown) + "\n" + random.choice(QUERIES[variant]))
        line = blank_index + 1
        missing = justification if justification_blank else render(formulas[-1])
        answer = f"step {line}; {missing}"
        steps = [step("VERIFY", index, "ok") for index in range(1, line)]
        steps.append(step("FLAG", line, missing))
        opcode = "MP" if justification.startswith("MP") else "APPLY"
        steps.append(step(opcode, justification, render(formulas[-1])))
        steps.append(step("CHECK", f"line {line}", render(formulas[-1])))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "truth_table_error":
            problem, steps, answer = self._truth_table_error()
        elif variant == "membership_table_error":
            problem, steps, answer = self._membership_table_error()
        else:
            problem, steps, answer = self._proof_blank(
                variant == "missing_justification")
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"foundations_critic_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
