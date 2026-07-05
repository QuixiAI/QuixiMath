import random

from base_generator import ProblemGenerator
from helpers import step, jid


TEMPLATES = {
    "unit_sat": [
        ("A",),
        ("not A", "B"),
        ("not B", "C"),
    ],
    "branch_sat": [
        ("A", "B"),
        ("not A", "B"),
        ("A", "not B"),
    ],
    "branch_unsat": [
        ("A", "B"),
        ("A", "not B"),
        ("not A", "B"),
        ("not A", "not B"),
    ],
}

PROBLEM_TEMPLATES = [
    ("Use DPLL on CNF {formula}. Variables are tried alphabetically and True "
     "before False. Give the final verdict and assignment if satisfiable."),
    ("Run a DPLL trace for {formula}; branch alphabetically and try True "
     "before False."),
    ("For the CNF formula {formula}, apply DPLL with alphabetical variables "
     "and True-first branching."),
]


def literal_var(literal):
    return literal[4:] if literal.startswith("not ") else literal


def literal_value(literal, assignment):
    var = literal_var(literal)
    if var not in assignment:
        return None
    value = assignment[var]
    return not value if literal.startswith("not ") else value


def clause_text(clause):
    return "(" + " OR ".join(clause) + ")"


def formula_text(clauses):
    return " AND ".join(clause_text(clause) for clause in clauses)


def assignment_text(assignment):
    if not assignment:
        return "none"
    return ", ".join(
        f"{var}={'True' if assignment[var] else 'False'}"
        for var in sorted(assignment)
    )


def simplify_state(clauses, assignment):
    remaining = []
    for clause in clauses:
        values = [literal_value(lit, assignment) for lit in clause]
        if True in values:
            continue
        unresolved = [lit for lit, val in zip(clause, values) if val is None]
        if not unresolved:
            return None
        remaining.append(tuple(unresolved))
    return remaining


def find_unit(clauses):
    for clause in clauses:
        if len(clause) == 1:
            return clause[0]
    return None


def assign_literal(literal, assignment):
    var = literal_var(literal)
    value = not literal.startswith("not ")
    assignment[var] = value
    return var, value


class DPLLTraceGenerator(ProblemGenerator):
    """
    Deterministic DPLL traces for tiny CNF formulas.

    The problem fixes variable order and branch order, so the final trace and
    assignment are unique.

    Op-codes used:
    - DPLL_SETUP / DPLL_STATE / DPLL_UNIT / DPLL_BRANCH / DPLL_ASSIGN
    - DPLL_SIMPLIFY / DPLL_CONFLICT / DPLL_BACKTRACK / DPLL_SAT
    - Z: satisfiable assignment or unsatisfiable verdict
    """

    VARIANTS = ["unit_sat", "branch_sat", "branch_unsat"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        clauses = TEMPLATES[variant]
        variables = sorted({literal_var(lit) for clause in clauses
                            for lit in clause})
        steps = [
            step("DPLL_SETUP", formula_text(clauses),
                 f"variables {', '.join(variables)}", "True first"),
        ]
        result, assignment = self._search(clauses, variables, {}, steps, 0)
        if result:
            answer = f"satisfiable; {assignment_text(assignment)}"
        else:
            answer = "unsatisfiable"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            formula=formula_text(clauses)
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"dpll_trace_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _search(self, clauses, variables, assignment, steps, depth):
        remaining = simplify_state(clauses, assignment)
        steps.append(step("DPLL_STATE", f"depth {depth}",
                          assignment_text(assignment),
                          "conflict" if remaining is None else
                          f"{len(remaining)} clauses left"))
        if remaining is None:
            steps.append(step("DPLL_CONFLICT", assignment_text(assignment)))
            return False, None
        if not remaining:
            steps.append(step("DPLL_SAT", assignment_text(assignment)))
            return True, dict(assignment)

        while True:
            unit = find_unit(remaining)
            if unit is None:
                break
            var, value = assign_literal(unit, assignment)
            steps.append(step("DPLL_UNIT", clause_text((unit,)),
                              f"{var}={'True' if value else 'False'}"))
            remaining = simplify_state(clauses, assignment)
            steps.append(step("DPLL_SIMPLIFY", assignment_text(assignment),
                              "conflict" if remaining is None else
                              f"{len(remaining)} clauses left"))
            if remaining is None:
                steps.append(step("DPLL_CONFLICT", assignment_text(assignment)))
                return False, None
            if not remaining:
                steps.append(step("DPLL_SAT", assignment_text(assignment)))
                return True, dict(assignment)

        branch_var = next(var for var in variables if var not in assignment)
        for value in (True, False):
            trial = dict(assignment)
            trial[branch_var] = value
            steps.append(step("DPLL_BRANCH", f"depth {depth}", branch_var,
                              "True" if value else "False"))
            ok, result = self._search(clauses, variables, trial, steps,
                                      depth + 1)
            if ok:
                return True, result
            steps.append(step("DPLL_BACKTRACK", branch_var,
                              "True" if value else "False"))
        return False, None
