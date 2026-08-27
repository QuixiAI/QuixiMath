"""Build deterministic propositional semantic tableaux.

Variants:
- ``validity`` starts from ``¬φ`` and decides whether every branch closes.
- ``satisfiability`` starts from ``φ`` and returns the leftmost model.
- ``countermodel`` uses a guaranteed non-tautology and returns the leftmost
  saturated assignment that falsifies it.

The engine converts its root to NNF, expands α-rules before β-rules, chooses
the oldest line then the leftmost branch, and assigns every unmentioned
variable ``F``. Random depth-2/3 formulas provide an unbounded problem space.

Op-codes:
- ``TABLEAU_ROOT``: state line 1 of the tree.
- ``ALPHA``: add both conjuncts to one branch.
- ``BETA``: split on a disjunction, left child first.
- ``BRANCH_CLOSE``: identify complementary literals.
- ``BRANCH_OPEN``: give a saturated branch assignment.
- ``CHECK``: verify the source under the selected assignment.
- ``Z``: closed/open verdict with canonical model or countermodel.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from logic_common import (And, Not, Or, Var, assignments, evaluate,
                          random_formula, render, to_nnf, variables)


FOUNDATIONS = True


NAME_BANK = tuple("abcdefghijklmnopqrstuvwx")

QUERIES = {
    "validity": (
        "Build the tableau and decide whether the formula is valid.",
        "Expand the truth tree under the stated policy and test validity.",
        "Determine whether the negated root closes on every branch.",
        "Use the semantic tableau to certify validity or give a countermodel.",
        "Complete the canonical validity tableau.",
    ),
    "satisfiability": (
        "Build the tableau and decide whether the formula is satisfiable.",
        "Expand the truth tree and give the leftmost model if one exists.",
        "Determine whether at least one saturated branch remains open.",
        "Use the semantic tableau to certify satisfiability or contradiction.",
        "Complete the canonical satisfiability tableau.",
    ),
    "countermodel": (
        "Build the tableau and report the leftmost countermodel.",
        "Expand the negated root and extract its canonical open assignment.",
        "Find the first saturated branch that falsifies the source formula.",
        "Use the semantic tableau to exhibit a countermodel.",
        "Complete the canonical countermodel tableau.",
    ),
}


def assignment_text(assignment):
    return ", ".join(f"{name}={'T' if assignment[name] else 'F'}"
                     for name in sorted(assignment))


def literal(node):
    if isinstance(node, Var):
        return node.name, True
    if isinstance(node, Not) and isinstance(node.arg, Var):
        return node.arg.name, False
    return None


def branch_contradiction(branch):
    seen = {}
    for item in branch["formulas"]:
        value = literal(item["formula"])
        if value is None:
            continue
        name, sign = value
        if name in seen and seen[name] != sign:
            return name
        seen[name] = sign
    return None


def branch_assignment(branch, names):
    result = {name: False for name in names}
    for item in branch["formulas"]:
        value = literal(item["formula"])
        if value is not None:
            result[value[0]] = value[1]
    return result


def tableau(root, names):
    """Return a canonical expansion trace and final ordered branches."""
    next_line = 2
    branches = [{
        "id": "1",
        "formulas": [{"line": 1, "formula": root, "expanded": False}],
        "closed": False,
    }]
    steps = [step("TABLEAU_ROOT", render(root))]

    def close_new_branches():
        for branch in branches:
            if branch["closed"]:
                continue
            name = branch_contradiction(branch)
            if name is not None:
                branch["closed"] = True
                steps.append(step("BRANCH_CLOSE", branch["id"],
                                  f"{name}, ¬{name}"))

    close_new_branches()
    while True:
        chosen = None
        for rule_type, cls in (("ALPHA", And), ("BETA", Or)):
            candidates = []
            for branch_index, branch in enumerate(branches):
                if branch["closed"]:
                    continue
                for item_index, item in enumerate(branch["formulas"]):
                    if not item["expanded"] and isinstance(item["formula"], cls):
                        candidates.append((item["line"], branch_index,
                                           item_index, rule_type))
            if candidates:
                chosen = min(candidates, key=lambda value: (value[0], value[1]))
                break
        if chosen is None:
            break
        _, branch_index, item_index, rule_type = chosen
        branch = branches[branch_index]
        item = branch["formulas"][item_index]
        item["expanded"] = True
        formula = item["formula"]
        if rule_type == "ALPHA":
            first_line, second_line = next_line, next_line + 1
            next_line += 2
            branch["formulas"].extend([
                {"line": first_line, "formula": formula.left, "expanded": False},
                {"line": second_line, "formula": formula.right, "expanded": False},
            ])
            steps.append(step("ALPHA", f"line {item['line']}",
                              f"{first_line}: {render(formula.left)}; "
                              f"{second_line}: {render(formula.right)}"))
        else:
            left_line, right_line = next_line, next_line + 1
            next_line += 2
            common = [dict(existing) for existing in branch["formulas"]]
            left_branch = {
                "id": branch["id"] + "L", "closed": False,
                "formulas": [dict(existing) for existing in common] + [
                    {"line": left_line, "formula": formula.left,
                     "expanded": False}],
            }
            right_branch = {
                "id": branch["id"] + "R", "closed": False,
                "formulas": [dict(existing) for existing in common] + [
                    {"line": right_line, "formula": formula.right,
                     "expanded": False}],
            }
            branches[branch_index:branch_index + 1] = [left_branch, right_branch]
            steps.append(step("BETA", f"line {item['line']}",
                              f"{left_branch['id']}: {left_line}: "
                              f"{render(formula.left)}",
                              f"{right_branch['id']}: {right_line}: "
                              f"{render(formula.right)}"))
        close_new_branches()

    for branch in branches:
        if not branch["closed"]:
            assignment = branch_assignment(branch, names)
            steps.append(step("BRANCH_OPEN", branch["id"],
                              assignment_text(assignment)))
    return steps, branches


class SemanticTableauGenerator(ProblemGenerator):
    """Generate truth trees with a forced expansion and branch order."""

    VARIANTS = ("validity", "satisfiability", "countermodel")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _formula(require_countermodel=False):
        while True:
            count = random.choice((2, 3))
            names = tuple(random.sample(NAME_BANK, count))
            source = random_formula(
                depth=random.choice((2, 3)), names=names,
                connectives=("¬", "∧", "∨", "→"), exact_depth=True,
                use_all=True,
            )
            if (not require_countermodel
                    or any(not evaluate(source, row) for row in assignments(names))):
                return source

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        source = self._formula(require_countermodel=(variant == "countermodel"))
        names = tuple(sorted(variables(source)))
        if variant in ("validity", "countermodel"):
            root = to_nnf(Not(source))
            task = "test validity using a tableau rooted at ¬φ"
        else:
            root = to_nnf(source)
            task = "test satisfiability using a tableau rooted at φ"
        policy = ("expand α before β; within a rule class use the oldest line "
                  "first and the leftmost branch first")
        problem = (f"Formula: {render(source)}. Task: {task}. Policy: {policy}. "
                   f"{random.choice(QUERIES[variant])}")
        steps, branches = tableau(root, names)
        open_branches = [branch for branch in branches if not branch["closed"]]
        if not open_branches:
            answer = ("closed; valid" if variant in ("validity", "countermodel")
                      else "closed; unsatisfiable")
            steps.append(step("CHECK", "all branches closed", answer))
        else:
            assignment = branch_assignment(open_branches[0], names)
            rendered_assignment = assignment_text(assignment)
            value = evaluate(source, assignment)
            if variant == "satisfiability":
                answer = f"open; satisfiable; model {rendered_assignment}"
                steps.append(step("CHECK", render(source), "T",
                                  rendered_assignment))
            else:
                answer = f"open; countermodel {rendered_assignment}"
                steps.append(step("CHECK", render(source), "F",
                                  rendered_assignment))
            assert value == (variant == "satisfiability")
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"semantic_tableau_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
