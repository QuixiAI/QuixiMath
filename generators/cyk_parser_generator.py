import random

from base_generator import ProblemGenerator
from helpers import step, jid


RULES = {
    "S": [("A", "B"), ("A", "C")],
    "C": [("S", "B")],
    "A": [("a",)],
    "B": [("b",)],
}

STRINGS = ["ab", "aabb", "aaabbb", "abb", "aba", "aaabb"]

PROBLEM_TEMPLATES = [
    ("Use CYK on grammar {grammar}; string {string}. Fill the table and "
     "decide whether S derives the string."),
    ("Run the CYK parser for string {string} with grammar {grammar}. Report "
     "the top cell and accept/reject."),
    ("For the CNF grammar {grammar} and input {string}, compute the CYK table "
     "and decide membership."),
]


def set_text(values):
    ordered = sorted(values)
    return "{" + ",".join(ordered) + "}" if ordered else "{}"


def grammar_text(rules):
    clauses = []
    for lhs in sorted(rules):
        rhs_text = " or ".join(" ".join(rhs) for rhs in rules[lhs])
        clauses.append(f"{lhs}->{rhs_text}")
    return "; ".join(clauses)


def reverse_rules(rules):
    out = {}
    for lhs, alternatives in rules.items():
        for rhs in alternatives:
            out.setdefault(rhs, set()).add(lhs)
    return out


def cyk_table(text, rules):
    rev = reverse_rules(rules)
    n = len(text)
    table = [[set() for _ in range(n)] for _ in range(n)]
    for i, ch in enumerate(text):
        table[i][i] = set(rev.get((ch,), set()))
    for span in range(2, n + 1):
        for i in range(0, n - span + 1):
            j = i + span - 1
            cell = set()
            for k in range(i, j):
                for left in table[i][k]:
                    for right in table[k + 1][j]:
                        cell.update(rev.get((left, right), set()))
            table[i][j] = cell
    return table


class CYKParserGenerator(ProblemGenerator):
    """
    CYK parsing for a small Chomsky-normal-form grammar.

    The grammar has exact terminal and binary rules; strings are short enough
    to show every table cell on a blackboard.

    Op-codes used:
    - CYK_SETUP / CYK_RULE / CYK_TERMINAL: grammar and base row
    - CYK_SPAN / CYK_SPLIT / CYK_COMBINE / CYK_CELL: table filling
    - CHECK: final S-membership check
    - Z: accept/reject result and top cell
    """

    def generate(self) -> dict:
        text = random.choice(STRINGS)
        rev = reverse_rules(RULES)
        n = len(text)
        table = [[set() for _ in range(n)] for _ in range(n)]
        steps = [
            step("CYK_SETUP", f"string {text}", f"length {n}"),
        ]
        for lhs in sorted(RULES):
            rhs_text = " or ".join(" ".join(rhs) for rhs in RULES[lhs])
            steps.append(step("CYK_RULE", lhs, rhs_text))

        for i, ch in enumerate(text):
            table[i][i] = set(rev.get((ch,), set()))
            steps.append(step("CYK_TERMINAL", f"cell {i + 1},{i + 1}",
                              ch, set_text(table[i][i])))

        for span in range(2, n + 1):
            steps.append(step("CYK_SPAN", span))
            for i in range(0, n - span + 1):
                j = i + span - 1
                cell = set()
                for k in range(i, j):
                    left = table[i][k]
                    right = table[k + 1][j]
                    steps.append(step("CYK_SPLIT", f"cell {i + 1},{j + 1}",
                                      f"{i + 1},{k + 1} x {k + 2},{j + 1}",
                                      f"{set_text(left)} x {set_text(right)}"))
                    found = set()
                    for lvar in left:
                        for rvar in right:
                            parents = rev.get((lvar, rvar), set())
                            if parents:
                                found.update(parents)
                                steps.append(step("CYK_COMBINE",
                                                  f"{lvar} {rvar}",
                                                  set_text(parents),
                                                  f"cell {i + 1},{j + 1}"))
                    cell.update(found)
                table[i][j] = cell
                steps.append(step("CYK_CELL", f"{i + 1},{j + 1}",
                                  set_text(cell)))

        top = table[0][n - 1]
        status = "accepted" if "S" in top else "rejected"
        steps.append(step("CHECK", "S in top cell", status))
        answer = f"{status}; top cell = {set_text(top)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            grammar=grammar_text(RULES),
            string=text,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="cyk_parser_membership",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
