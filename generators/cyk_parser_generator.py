import random

from base_generator import ProblemGenerator
from helpers import step, jid


# Nonterminal names other than the start symbol S, and the terminal alphabet
# they can rewrite to. Everything is a single character so the CYK table stays
# blackboard sized.
NONTERMINAL_POOL = ["A", "B", "C", "D", "E", "T", "U", "V", "X", "Y", "Z"]
TERMINAL_POOL = ["a", "b", "c", "d", "e"]

PROBLEM_TEMPLATES = [
    ("Use CYK on grammar {grammar}; string {string}. Fill the table and "
     "decide whether S derives the string."),
    ("Run the CYK parser for string {string} with grammar {grammar}. Report "
     "the top cell and accept/reject."),
    ("For the CNF grammar {grammar} and input {string}, compute the CYK table "
     "and decide membership."),
    ("A parser uses the CNF grammar {grammar}. Fill the CYK table for the "
     "input {string} and say whether S derives it."),
    ("Given the Chomsky-normal-form rules {grammar}, apply the CYK algorithm "
     "to the word {string} and report the top cell with accept or reject."),
    ("Does S derive the string {string} under the CNF grammar {grammar}? "
     "Build the CYK table, then give the top cell."),
]


def set_text(values):
    ordered = sorted(values)
    return "{" + ",".join(ordered) + "}" if ordered else "{}"


def grammar_text(rules):
    clauses = []
    for lhs in sorted(rules):
        alternatives = sorted(rules[lhs], key=lambda rhs: (len(rhs), rhs))
        rhs_text = " or ".join(" ".join(rhs) for rhs in alternatives)
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


def random_grammar():
    """A random Chomsky-normal-form grammar with S as start symbol."""
    others = random.sample(NONTERMINAL_POOL, random.randint(2, 3))
    nonterminals = ["S"] + others
    terminals = random.sample(TERMINAL_POOL, random.randint(2, 3))
    rules = {name: [] for name in nonterminals}

    # Every terminal is produced by at least one nonterminal.
    for terminal in terminals:
        owners = random.sample(others, random.randint(1, min(2, len(others))))
        for owner in owners:
            if (terminal,) not in rules[owner]:
                rules[owner].append((terminal,))

    for _ in range(random.randint(2, 4)):
        lhs = random.choice(nonterminals)
        pair = (random.choice(nonterminals), random.choice(nonterminals))
        if pair not in rules[lhs]:
            rules[lhs].append(pair)

    if not any(len(rhs) == 2 for rhs in rules["S"]):
        rules["S"].append((random.choice(nonterminals),
                           random.choice(nonterminals)))

    # No nonterminal may be left with an empty right-hand side.
    for name in nonterminals:
        if not rules[name]:
            rules[name].append((random.choice(terminals),))
    return rules, terminals


def derive(rules, symbol, length, failures):
    """Random terminal string of exactly ``length`` derived from ``symbol``."""
    key = (symbol, length)
    if key in failures:
        return None
    if length == 1:
        options = [rhs[0] for rhs in rules[symbol] if len(rhs) == 1]
        if not options:
            failures.add(key)
            return None
        return random.choice(options)
    binaries = [rhs for rhs in rules[symbol] if len(rhs) == 2]
    random.shuffle(binaries)
    splits = list(range(1, length))
    random.shuffle(splits)
    for left, right in binaries:
        for cut in splits:
            head = derive(rules, left, cut, failures)
            if head is None:
                continue
            tail = derive(rules, right, length - cut, failures)
            if tail is None:
                continue
            return head + tail
    failures.add(key)
    return None


def random_string(terminals, length):
    return "".join(random.choice(terminals) for _ in range(length))


class CYKParserGenerator(ProblemGenerator):
    """
    CYK parsing for a small Chomsky-normal-form grammar.

    The grammar is built at random (2-4 nonterminals besides S, 2-3
    terminals, exact terminal and binary rules) and the input string is short
    enough to show every table cell on a blackboard. Roughly half the strings
    are derived from the grammar (accepted) and half are drawn at random and
    verified to be outside the language.

    Op-codes used:
    - CYK_SETUP / CYK_RULE / CYK_TERMINAL: grammar and base row
    - CYK_SPAN / CYK_SPLIT / CYK_COMBINE / CYK_CELL: table filling
    - CHECK: final S-membership check
    - Z: accept/reject result and top cell
    """

    def _instance(self):
        for _ in range(200):
            rules, terminals = random_grammar()
            n = random.choice([3, 3, 4, 4, 5])
            # The grammar must generate *something* of this length, so the
            # table is never vacuous.
            sample = derive(rules, "S", n, set())
            if sample is None:
                continue
            if random.random() < 0.5:
                return rules, sample
            # A near miss (one letter changed) makes a far better rejected
            # instance than an unrelated random string.
            near = [sample[:i] + other + sample[i + 1:]
                    for i in range(n) for other in terminals
                    if other != sample[i]]
            random.shuffle(near)
            for text in near + [random_string(terminals, n)
                                for _ in range(6)]:
                if "S" not in cyk_table(text, rules)[0][n - 1]:
                    return rules, text
        raise RuntimeError("could not build a CYK instance")

    def generate(self) -> dict:
        rules, text = self._instance()
        rev = reverse_rules(rules)
        n = len(text)
        table = [[set() for _ in range(n)] for _ in range(n)]
        steps = [
            step("CYK_SETUP", f"string {text}", f"length {n}"),
        ]
        for lhs in sorted(rules):
            alternatives = sorted(rules[lhs], key=lambda rhs: (len(rhs), rhs))
            rhs_text = " or ".join(" ".join(rhs) for rhs in alternatives)
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
                    for lvar in sorted(left):
                        for rvar in sorted(right):
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
            grammar=grammar_text(rules),
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
