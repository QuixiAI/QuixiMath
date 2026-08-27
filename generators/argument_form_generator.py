"""Identify propositional inference rules and classic formal fallacies.

Variants:
- ``named_rule`` generates a valid named argument form.
- ``fallacy`` generates affirming the consequent or denying the antecedent.
- ``truth_table_validity`` mixes valid and invalid symbolic arguments.
- ``english`` renders the four core conditional forms in templated English.

Symbolic schemas receive random depth-two formula substitutions.  Every
record verifies all truth assignments and invalid arguments include the first
counterexample row.  Five phrasings yield more than 100,000 problem texts.

Op-codes:
- ``ARG_SETUP``: state the premises and conclusion.
- ``TRUTH_ROW``: begin one canonical truth assignment.
- ``PREMISES_ALL_T``: determine whether the row tests validity.
- ``CONCLUSION_AT``: evaluate the conclusion on an all-premises-true row.
- ``VALIDITY`` / ``COUNTEREXAMPLE``: record the result.
- ``Z``: exact composite rule/fallacy verdict.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, Imp, Not, Or, Var, assignments, evaluate,
                          random_formula, render, substitute, variables)


FOUNDATIONS = True


x, y, z, w = Var("x"), Var("y"), Var("z"), Var("w")

RULES = {
    "modus ponens": ((Imp(x, y), x), y, True),
    "modus tollens": ((Imp(x, y), Not(y)), Not(x), True),
    "hypothetical syllogism": ((Imp(x, y), Imp(y, z)), Imp(x, z), True),
    "disjunctive syllogism": ((Or(x, y), Not(x)), y, True),
    "simplification": ((And(x, y),), x, True),
    "conjunction": ((x, y), And(x, y), True),
    "addition": ((x,), Or(x, y), True),
    "constructive dilemma": ((And(Imp(x, y), Imp(z, w)), Or(x, z)),
                              Or(y, w), True),
    "affirming the consequent": ((Imp(x, y), y), x, False),
    "denying the antecedent": ((Imp(x, y), Not(x)), Not(y), False),
}

VALID_RULES = tuple(name for name, (_, _, valid) in RULES.items() if valid)
FALLACIES = tuple(name for name, (_, _, valid) in RULES.items() if not valid)

QUERIES = {
    "named_rule": ("Identify the valid inference rule and verify it by truth table.",
                   "Name the argument form after checking every row.",
                   "Determine the rule that makes the conclusion follow.",
                   "Classify this valid symbolic inference.",
                   "Give the rule name supported by the validity test."),
    "fallacy": ("Identify the formal fallacy and give its first counterexample row.",
                "Name the invalid argument form after testing the rows.",
                "Find the classic fallacy and the earliest falsifying assignment.",
                "Classify this invalid conditional inference.",
                "Give the fallacy name together with a truth-table counterexample."),
    "truth_table_validity": ("Decide validity and identify the form.",
                             "Test whether all true-premise rows force the conclusion.",
                             "Give a validity verdict, rule name, and any counterexample.",
                             "Analyze the argument by a complete truth table.",
                             "Determine whether the inference succeeds on every relevant row."),
    "english": ("Identify the rule or fallacy in the argument in words.",
                "Translate the repeated clauses logically and classify the inference.",
                "Decide validity and name this English argument form.",
                "Use the supplied proposition vocabulary to analyze the argument.",
                "Give the rule/fallacy verdict and any counterexample assignment."),
}


def row_text(assignment):
    return ", ".join(f"{name}={'T' if assignment[name] else 'F'}"
                     for name in sorted(assignment))


def first_counterexample(premises, conclusion):
    names = sorted(set().union(*(set(variables(formula)) for formula in premises),
                               set(variables(conclusion))))
    for assignment in assignments(names):
        if all(evaluate(premise, assignment) for premise in premises) and not evaluate(
                conclusion, assignment):
            return assignment
    return None


class ArgumentFormGenerator(ProblemGenerator):
    """Instantiate argument schemas and prove their validity status row by row."""

    VARIANTS = ("named_rule", "fallacy", "truth_table_validity", "english")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _mapping(placeholders):
        output = {}
        used = set()
        for placeholder in placeholders:
            formula = random_formula(depth=2, names=("p", "q", "r", "s"),
                                     connectives=("¬", "∧", "∨"),
                                     exact_depth=True)
            while render(formula) in used:
                formula = random_formula(depth=2, names=("p", "q", "r", "s"),
                                         connectives=("¬", "∧", "∨"),
                                         exact_depth=True)
            output[placeholder] = formula
            used.add(render(formula))
        return output

    @staticmethod
    def _instantiate(label):
        premise_schemas, conclusion_schema, valid = RULES[label]
        names = sorted(set().union(*(set(variables(item)) for item in premise_schemas),
                                   set(variables(conclusion_schema))))
        mapping = ArgumentFormGenerator._mapping(names)
        premises = tuple(substitute(item, mapping) for item in premise_schemas)
        conclusion = substitute(conclusion_schema, mapping)
        if valid or first_counterexample(premises, conclusion) is not None:
            return premises, conclusion
        return ArgumentFormGenerator._instantiate(label)

    @staticmethod
    def _english_sentences():
        while True:
            first = random.choice((
                f"the number is divisible by {random.randint(2, 100)}",
                f"the number is greater than {random.randint(-100, 100)}",
                f"the figure has {random.randint(3, 12)} sides",
                f"the sequence has common difference {random.randint(2, 30)}",
            ))
            second = random.choice((
                f"the result is divisible by {random.randint(2, 100)}",
                f"the result is less than {random.randint(1, 200)}",
                f"the figure is labeled type {random.randint(1, 50)}",
                f"the sequence is labeled class {random.randint(1, 50)}",
            ))
            if first != second:
                return first, second

    @staticmethod
    def _english_argument(label, first, second):
        not_first = f"it is not the case that {first}"
        not_second = f"it is not the case that {second}"
        conditional = f"if {first}, then {second}"
        forms = {
            "modus ponens": ((conditional, first), second),
            "modus tollens": ((conditional, not_second), not_first),
            "affirming the consequent": ((conditional, second), first),
            "denying the antecedent": ((conditional, not_first), not_second),
        }
        return forms[label]

    @staticmethod
    def _truth_steps(premises, conclusion):
        names = sorted(set().union(*(set(variables(formula)) for formula in premises),
                                   set(variables(conclusion))))
        steps = [step("ARG_SETUP", "; ".join(render(item) for item in premises),
                      render(conclusion))]
        for assignment in assignments(names):
            row = row_text(assignment)
            steps.append(step("TRUTH_ROW", row))
            all_true = all(evaluate(item, assignment) for item in premises)
            steps.append(step("PREMISES_ALL_T", row, "yes" if all_true else "no"))
            if all_true:
                steps.append(step("CONCLUSION_AT", row,
                                  "T" if evaluate(conclusion, assignment) else "F"))
        return steps

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "named_rule":
            label = random.choice(VALID_RULES)
        elif variant == "fallacy":
            label = random.choice(FALLACIES)
        elif variant == "truth_table_validity":
            label = random.choice(tuple(RULES))
        else:
            label = random.choice(("modus ponens", "modus tollens",
                                   "affirming the consequent", "denying the antecedent"))

        if variant == "english":
            first, second = self._english_sentences()
            clauses, conclusion_clause = self._english_argument(label, first, second)
            problem = (
                f"Vocabulary: p means \"{first}\"; q means \"{second}\". "
                f"Argument clauses: {'; '.join(clauses)}; therefore {conclusion_clause}. "
                f"{random.choice(QUERIES[variant])}"
            )
            premise_schemas, conclusion_schema, _ = RULES[label]
            mapping = {"x": Var("p"), "y": Var("q")}
            premises = tuple(substitute(item, mapping) for item in premise_schemas)
            conclusion = substitute(conclusion_schema, mapping)
        else:
            premises, conclusion = self._instantiate(label)
            problem = (
                f"Premises: {'; '.join(render(item) for item in premises)}. "
                f"Conclusion: {render(conclusion)}. "
                f"{random.choice(QUERIES[variant])}"
            )

        steps = self._truth_steps(premises, conclusion)
        counterexample = first_counterexample(premises, conclusion)
        if counterexample is None:
            steps.append(step("VALIDITY", "valid", label))
            answer = f"valid; {label}"
        else:
            witness = row_text(counterexample)
            steps.append(step("COUNTEREXAMPLE", witness,
                              "premises all T", "conclusion F"))
            steps.append(step("VALIDITY", "invalid", label))
            answer = f"invalid; {label}; counterexample {witness}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"argument_form_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
