import random
from itertools import combinations

from base_generator import ProblemGenerator
from helpers import step, jid


VARS3 = ["A", "B", "C"]
VARS2 = ["A", "B"]

VAR_SETS = {
    2: [("A", "B"), ("P", "Q"), ("X", "Y"), ("U", "V"), ("S", "T"),
        ("M", "N"), ("C", "D"), ("J", "K")],
    3: [("A", "B", "C"), ("B", "C", "D"), ("C", "D", "E"), ("J", "K", "L"),
        ("K", "L", "M"), ("L", "M", "N"), ("P", "Q", "R"), ("Q", "R", "S"),
        ("R", "S", "T"), ("U", "V", "W"), ("V", "W", "X"), ("W", "X", "Y"),
        ("X", "Y", "Z")],
    4: [("A", "B", "C", "D"), ("B", "C", "D", "E"), ("J", "K", "L", "M"),
        ("K", "L", "M", "N"), ("P", "Q", "R", "S"), ("Q", "R", "S", "T"),
        ("U", "V", "W", "X"), ("V", "W", "X", "Y"), ("W", "X", "Y", "Z")],
}

# Function names never collide with a variable letter (F, G, H are kept out
# of VAR_SETS) so a parser can always tell them apart.
FUNC_NAMES = ["f", "g", "h", "F", "G", "H"]

GRAY2 = ["00", "01", "11", "10"]

# Phrasings. Every template takes {fn} (function name), {vs} (comma-joined
# variables), {table} (rendered truth table) and {n} (variable count).
# LIST templates take a row-by-row table rendering; SPEC templates take the
# "1 exactly on these rows" rendering.
DNF_LIST_TEMPLATES = [
    "Truth table for {fn}({vs}): {table}. Write a disjunctive normal form "
    "(DNF).",
    "A logic circuit computes {fn}({vs}) with truth table {table}. Write the "
    "disjunctive normal form (DNF).",
    "The Boolean function {fn}({vs}) is given by the table {table}. Express "
    "{fn} in disjunctive normal form (DNF).",
    "The rows of the truth table of {fn}({vs}) read {table}. Give the DNF "
    "(sum of minterms) for {fn}.",
    "For the Boolean function {fn}({vs}) the truth table is {table}. Write "
    "{fn} as a disjunctive normal form (DNF).",
    "A {n}-input gate network realises {fn}({vs}); its truth table is "
    "{table}. State the DNF (sum of minterms).",
]
DNF_SPEC_TEMPLATES = [
    "The Boolean function {fn}({vs}) satisfies: {table}. Write a disjunctive "
    "normal form (DNF) for {fn}.",
    "Define {fn}({vs}) so that {table}. Give the DNF (sum of minterms) for "
    "{fn}.",
    "A Boolean function {fn}({vs}) is described this way: {table}. Write its "
    "disjunctive normal form (DNF).",
    "Suppose {fn}({vs}) is the {n}-variable function with {table}. Give the "
    "DNF (sum of minterms).",
]
CNF_LIST_TEMPLATES = [
    "Truth table for {fn}({vs}): {table}. Write a conjunctive normal form "
    "(CNF).",
    "A logic circuit computes {fn}({vs}) with truth table {table}. Write the "
    "conjunctive normal form (CNF).",
    "The Boolean function {fn}({vs}) is given by the table {table}. Express "
    "{fn} in conjunctive normal form (CNF).",
    "The rows of the truth table of {fn}({vs}) read {table}. Give the CNF "
    "(product of maxterms) for {fn}.",
    "For the Boolean function {fn}({vs}) the truth table is {table}. Write "
    "{fn} as a conjunctive normal form (CNF).",
    "A {n}-input gate network realises {fn}({vs}); its truth table is "
    "{table}. State the CNF (product of maxterms).",
]
CNF_SPEC_TEMPLATES = [
    "The Boolean function {fn}({vs}) satisfies: {table}. Write a conjunctive "
    "normal form (CNF) for {fn}.",
    "Define {fn}({vs}) so that {table}. Give the CNF (product of maxterms) "
    "for {fn}.",
    "A Boolean function {fn}({vs}) is described this way: {table}. Write its "
    "conjunctive normal form (CNF).",
    "Suppose {fn}({vs}) is the {n}-variable function with {table}. Give the "
    "CNF (product of maxterms).",
]
KMAP_LIST_TEMPLATES = [
    "Use a {n}-variable Karnaugh map to simplify {fn}({vs}) with truth table "
    "{table}.",
    "Simplify {fn}({vs}) with a {n}-variable Karnaugh map; the truth table is "
    "{table}. Give the minimal sum-of-products form.",
    "A {n}-variable Karnaugh map is filled in for {fn}({vs}) from the truth "
    "table {table}. Write the minimal sum-of-products expression.",
    "Minimize {fn}({vs}) using a {n}-variable Karnaugh map. The truth table "
    "is {table}.",
    "The truth table of {fn}({vs}) is {table}. Group the ones on a "
    "{n}-variable Karnaugh map and write the minimal sum-of-products form.",
    "A designer draws a {n}-variable Karnaugh map for {fn}({vs}) with truth "
    "table {table}. What minimal sum-of-products expression comes out?",
]
KMAP_SPEC_TEMPLATES = [
    "Minimize {fn}({vs}) with a {n}-variable Karnaugh map, where {table}.",
    "A {n}-variable Karnaugh map is drawn for {fn}({vs}): {table}. Give the "
    "minimal sum-of-products form.",
    "On a {n}-variable Karnaugh map for {fn}({vs}), {table}. Write the "
    "minimal sum-of-products expression.",
    "Group the ones of {fn}({vs}) on a {n}-variable Karnaugh map, given that "
    "{table}. Give the minimal sum-of-products form.",
]


def bit_rows(width):
    return [format(value, f"0{width}b") for value in range(2 ** width)]


def assignment_text(bits, variables):
    return ", ".join(f"{var}={bit}" for var, bit in zip(variables, bits))


def minterm(bits, variables):
    terms = [var if bit == "1" else f"NOT {var}"
             for var, bit in zip(variables, bits)]
    return " AND ".join(terms)


def maxterm(bits, variables):
    terms = [var if bit == "0" else f"NOT {var}"
             for var, bit in zip(variables, bits)]
    return " OR ".join(terms)


def join_terms(terms, connector, identity):
    if not terms:
        return identity
    if len(terms) == 1:
        return terms[0]
    return f" {connector} ".join(f"({term})" for term in terms)


def format_kmap_terms(terms):
    """Join simplified product terms; parenthesize only compound ones."""
    if len(terms) == 1:
        return terms[0]
    rendered = [f"({term})" if " AND " in term else term for term in terms]
    return " OR ".join(rendered)


def truth_table_text(values_by_row):
    return ", ".join(f"{row}->{values_by_row[row]}"
                     for row in sorted(values_by_row))


def func_values_text(values_by_row, fname):
    return ", ".join(f"{fname}({','.join(row)})={values_by_row[row]}"
                     for row in sorted(values_by_row))


def spec_text(values_by_row, variables, fname, focus):
    selected = [row for row in sorted(values_by_row)
                if values_by_row[row] == focus]
    return (f"{fname} = {focus} exactly on the rows {''.join(variables)} = "
            f"{', '.join(selected)}; {fname} = {1 - focus} on every other row")


def random_truth_values(width=3, focus=1, low=2, high=6):
    """Random truth table with between ``low`` and ``high`` ``focus`` rows."""
    rows = bit_rows(width)
    count = random.randint(low, min(high, len(rows) - 1))
    chosen = set(random.sample(rows, count))
    return {row: (focus if row in chosen else 1 - focus) for row in rows}


# --- Karnaugh-map machinery ------------------------------------------------
# Cubes are tuples of "0"/"1"/"-" (a dash means the variable dropped out).

def combine_cubes(left, right):
    diff = [i for i in range(len(left)) if left[i] != right[i]]
    if len(diff) != 1:
        return None
    index = diff[0]
    if left[index] == "-" or right[index] == "-":
        return None
    merged = list(left)
    merged[index] = "-"
    return tuple(merged)


def prime_implicants(ones):
    """Quine-McCluskey prime implicants of the given one-rows."""
    current = {tuple(row) for row in ones}
    primes = set()
    while current:
        used = set()
        nxt = set()
        ordered = sorted(current)
        for left, right in combinations(ordered, 2):
            merged = combine_cubes(left, right)
            if merged is not None:
                nxt.add(merged)
                used.add(left)
                used.add(right)
        primes |= set(ordered) - used
        current = nxt
    return sorted(primes)


def cube_cells(cube):
    cells = [""]
    for char in cube:
        if char == "-":
            cells = [cell + bit for cell in cells for bit in "01"]
        else:
            cells = [cell + char for cell in cells]
    return set(cells)


def cube_literals(cube):
    return sum(1 for char in cube if char != "-")


def cube_term(cube, variables):
    literals = [variables[i] if char == "1" else f"NOT {variables[i]}"
                for i, char in enumerate(cube) if char != "-"]
    return " AND ".join(literals)


def cube_key(cube):
    """Canonical ordering: fewer literals first, then variables, then sign."""
    indices = tuple(i for i, char in enumerate(cube) if char != "-")
    signs = tuple(int(char) for char in cube if char != "-")
    return (len(indices), indices, signs)


def minimal_cover(ones, max_terms=4, max_primes=12):
    """Unique minimum-cost sum-of-products cover, or None.

    Cost is (number of terms, total literals). Returns None when no cover of
    at most ``max_terms`` prime implicants exists, when the map has too many
    prime implicants to be hand-friendly, or when the cheapest cover is not
    unique (so the expected answer would be ambiguous).
    """
    target = set(ones)
    if not target:
        return None
    primes = prime_implicants(target)
    if len(primes) > max_primes:
        return None
    covers = {cube: cube_cells(cube) for cube in primes}
    best = None
    best_cost = None
    ties = 0
    for size in range(1, min(max_terms, len(primes)) + 1):
        for combo in combinations(primes, size):
            covered = set()
            for cube in combo:
                covered |= covers[cube]
            if covered != target:
                continue
            cost = (size, sum(cube_literals(cube) for cube in combo))
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best = combo
                ties = 1
            elif cost == best_cost:
                ties += 1
        if best is not None:
            break
    if best is None or ties != 1:
        return None
    return sorted(best, key=cube_key)


def kmap_layout(variables):
    """(row variables, row codes, column variables, column codes)."""
    width = len(variables)
    if width == 2:
        return variables[:1], ["0", "1"], variables[1:], ["0", "1"]
    if width == 3:
        return variables[:1], ["0", "1"], variables[1:], list(GRAY2)
    return variables[:2], list(GRAY2), variables[2:], list(GRAY2)


class BooleanAlgebraGenerator(ProblemGenerator):
    """
    Boolean truth-table normal forms and Karnaugh-map simplification.

    Variants:
    - dnf: build disjunctive normal form from the 1 rows
    - cnf: build conjunctive normal form from the 0 rows
    - kmap: simplify a 2-, 3- or 4-variable truth table with a Karnaugh map

    Op-codes used:
    - BOOL_SETUP: variables and requested form
    - TRUTH_ROW: one truth-table row
    - MINTERM / MAXTERM: row-to-term conversion
    - DNF_FORM / CNF_FORM: assembled normal form
    - KMAP_SETUP / KMAP_ROW / KMAP_GROUP / KMAP_SIMPLIFY: Karnaugh map trace
    - CHECK: substitute one row back into the answer
    - Z: exact Boolean expression
    """

    VARIANTS = ["dnf", "cnf", "kmap"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # -- problem text ------------------------------------------------------
    def _render_problem(self, variant, values, variables, fname, focus):
        width = len(variables)
        vs = ",".join(variables)
        if variant == "dnf":
            list_templates, spec_templates = (DNF_LIST_TEMPLATES,
                                              DNF_SPEC_TEMPLATES)
        elif variant == "cnf":
            list_templates, spec_templates = (CNF_LIST_TEMPLATES,
                                              CNF_SPEC_TEMPLATES)
        else:
            list_templates, spec_templates = (KMAP_LIST_TEMPLATES,
                                              KMAP_SPEC_TEMPLATES)
        style = random.choice(["arrow", "funcvals", "spec"])
        if style == "arrow":
            table = truth_table_text(values)
            template = random.choice(list_templates)
        elif style == "funcvals":
            table = func_values_text(values, fname)
            template = random.choice(list_templates)
        else:
            table = spec_text(values, variables, fname, focus)
            template = random.choice(spec_templates)
        return template.format(fn=fname, vs=vs, table=table, n=width)

    # -- variants ----------------------------------------------------------
    def _normal_form(self, variant):
        width = random.choice([3, 3, 4])
        variables = list(random.choice(VAR_SETS[width]))
        fname = random.choice(FUNC_NAMES)
        focus = 1 if variant == "dnf" else 0
        high = 6 if width == 3 else 5
        values = random_truth_values(width, focus, 2, high)
        rows = bit_rows(width)
        form_name = "DNF" if variant == "dnf" else "CNF"

        steps = [
            step("BOOL_SETUP", f"variables {', '.join(variables)}",
                 f"{form_name} from {fname}={focus} rows"),
        ]
        terms = []
        focus_rows = []
        for row in rows:
            value = values[row]
            steps.append(step("TRUTH_ROW", assignment_text(row, variables),
                              f"{fname}={value}"))
            if value == focus:
                focus_rows.append(row)
                if variant == "dnf":
                    term = minterm(row, variables)
                    steps.append(step("MINTERM", row, term))
                else:
                    term = maxterm(row, variables)
                    steps.append(step("MAXTERM", row, term))
                terms.append(term)

        if variant == "dnf":
            expression = join_terms(terms, "OR", "0")
            steps.append(step("DNF_FORM", expression))
        else:
            expression = join_terms(terms, "AND", "1")
            steps.append(step("CNF_FORM", expression))
        answer = f"{form_name} = {expression}"

        if random.random() < 0.5:
            probe = random.choice(focus_rows)
            steps.append(step(
                "CHECK", "substitute",
                f"{fname}({','.join(probe)}) from {form_name} = {focus}",
                f"{fname}({','.join(probe)}) from table = {focus}",
            ))

        problem = self._render_problem(variant, values, variables, fname,
                                       focus)
        return problem, steps, answer

    def _kmap(self):
        for _ in range(400):
            width = random.choice([2, 3, 3, 4, 4, 4, 4, 4])
            variables = list(random.choice(VAR_SETS[width]))
            rows = bit_rows(width)
            if width == 2:
                count = random.randint(1, 3)
            elif width == 3:
                count = random.randint(2, 6)
            else:
                count = random.randint(3, 9)
            ones = set(random.sample(rows, count))
            cover = minimal_cover(ones)
            if cover is None:
                continue
            values = {row: int(row in ones) for row in rows}
            fname = random.choice(FUNC_NAMES)
            row_vars, row_codes, col_vars, col_codes = kmap_layout(variables)
            row_label = "".join(row_vars)
            col_label = "".join(col_vars)
            steps = [
                step("BOOL_SETUP", f"variables {', '.join(variables)}",
                     "K-map simplify"),
                step("KMAP_SETUP",
                     "rows " + ",".join(f"{row_label}={code}"
                                        for code in row_codes),
                     "columns " + ",".join(f"{col_label}={code}"
                                           for code in col_codes)),
            ]
            for row_code in row_codes:
                cells = [values[row_code + col_code] for col_code in col_codes]
                steps.append(step("KMAP_ROW", f"{row_label}={row_code}",
                                  ", ".join(str(cell) for cell in cells)))
            terms = []
            for cube in cover:
                cells = ", ".join(sorted(cube_cells(cube)))
                term = cube_term(cube, variables)
                terms.append(term)
                steps.append(step("KMAP_GROUP", cells, term))
            expression = format_kmap_terms(terms)
            steps.append(step("KMAP_SIMPLIFY", expression))
            answer = f"simplified = {expression}"
            if random.random() < 0.5:
                ones_text = ", ".join(sorted(ones))
                steps.append(step(
                    "CHECK", "truth_table",
                    f"expression is 1 on {ones_text}",
                    f"table is 1 on {ones_text}",
                ))
            problem = self._render_problem("kmap", values, variables, fname, 1)
            return problem, steps, answer
        raise RuntimeError("could not build a Karnaugh map instance")

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant in ("dnf", "cnf"):
            problem, steps, answer = self._normal_form(variant)
        else:
            problem, steps, answer = self._kmap()

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"boolean_algebra_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
