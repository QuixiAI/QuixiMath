import itertools
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.boolean_algebra_generator import BooleanAlgebraGenerator
from helpers import DELIM


VARS3 = ["A", "B", "C"]
VARS2 = ["A", "B"]

HEADER_RE = re.compile(r"([A-Za-z])\(([A-Z](?:,[A-Z])+)\)")
ARROW_RE = re.compile(r"([01]+)->([01])")
FUNCVAL_RE = re.compile(r"[A-Za-z]\(([01](?:,[01])+)\)=([01])")
SPEC_RE = re.compile(
    r"([A-Za-z]) = ([01]) exactly on the rows ([A-Z]+) = "
    r"((?:[01]+, )*[01]+); [A-Za-z] = [01] on every other row"
)


def bit_rows(width):
    return [format(value, f"0{width}b") for value in range(2 ** width)]


# --- problem parsing (works for every phrasing) ----------------------------

def parse_problem(problem):
    header = HEADER_RE.search(problem)
    assert header is not None, problem
    fname = header.group(1)
    variables = header.group(2).split(",")
    width = len(variables)
    rows = bit_rows(width)

    if "Karnaugh" in problem:
        variant = "kmap"
    elif "DNF" in problem or "disjunctive" in problem:
        variant = "dnf"
    else:
        assert "CNF" in problem or "conjunctive" in problem, problem
        variant = "cnf"

    spec = SPEC_RE.search(problem)
    if spec is not None:
        assert spec.group(1) == fname, problem
        assert spec.group(3) == "".join(variables), problem
        focus = int(spec.group(2))
        listed = spec.group(4).split(", ")
        for row in listed:
            assert row in rows, problem
        values = {row: (focus if row in listed else 1 - focus)
                  for row in rows}
    else:
        pairs = FUNCVAL_RE.findall(problem)
        if pairs:
            values = {row.replace(",", ""): int(value)
                      for row, value in pairs}
        else:
            pairs = ARROW_RE.findall(problem)
            assert pairs, problem
            values = {row: int(value) for row, value in pairs}
        assert sorted(values) == rows, problem
    return {
        "variant": variant,
        "fname": fname,
        "variables": variables,
        "values": values,
    }


# --- boolean expression parsing / evaluation -------------------------------

def parse_literal(text):
    text = text.strip()
    if text.startswith("NOT "):
        return (text[4:], False)
    return (text, True)


def parse_group(text, inner):
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return [parse_literal(piece) for piece in text.split(f" {inner} ")]


def parse_expression(expr, outer, inner):
    return [parse_group(part, inner) for part in expr.split(f" {outer} ")]


def eval_expression(groups, outer, assignment):
    """outer='OR' -> sum of products; outer='AND' -> product of sums."""
    results = []
    for group in groups:
        literal_values = [assignment[var] if positive else 1 - assignment[var]
                          for var, positive in group]
        if outer == "OR":
            results.append(int(all(literal_values)))
        else:
            results.append(int(any(literal_values)))
    if outer == "OR":
        return int(any(results))
    return int(all(results))


def truth_table_of(groups, outer, variables):
    table = {}
    for row in bit_rows(len(variables)):
        assignment = {var: int(bit) for var, bit in zip(variables, row)}
        table[row] = eval_expression(groups, outer, assignment)
    return table


# --- independent K-map minimisation (brute force over all cubes) -----------

def cube_cells(cube):
    cells = [""]
    for char in cube:
        if char == "-":
            cells = [cell + bit for cell in cells for bit in "01"]
        else:
            cells = [cell + char for cell in cells]
    return frozenset(cells)


def cube_key(cube):
    indices = tuple(i for i, char in enumerate(cube) if char != "-")
    signs = tuple(int(char) for char in cube if char != "-")
    return (len(indices), indices, signs)


def cube_term(cube, variables):
    return " AND ".join(
        variables[i] if char == "1" else f"NOT {variables[i]}"
        for i, char in enumerate(cube) if char != "-"
    )


def term_to_cube(group, variables):
    cube = ["-"] * len(variables)
    for var, positive in group:
        cube[variables.index(var)] = "1" if positive else "0"
    return tuple(cube)


def brute_force_min_cover(ones, width):
    """Minimum-cost SOP cover by exhaustive search over every cube.

    Independent of the generator's Quine-McCluskey route: it enumerates all
    3**width cubes, keeps those contained in the one-set, drops non-maximal
    ones by containment, then searches covers by increasing size.
    """
    target = frozenset(ones)
    implicants = []
    for cube in itertools.product("01-", repeat=width):
        cells = cube_cells(cube)
        if cells <= target:
            implicants.append((cube, cells))
    maximal = [
        (cube, cells) for cube, cells in implicants
        if not any(cells < other for _, other in implicants)
    ]
    best = None
    ties = 0
    for size in range(1, len(maximal) + 1):
        best_cost = None
        for combo in itertools.combinations(maximal, size):
            covered = frozenset().union(*(cells for _, cells in combo))
            if covered != target:
                continue
            cost = (size, sum(sum(1 for char in cube if char != "-")
                              for cube, _ in combo))
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best = [cube for cube, _ in combo]
                ties = 1
            elif cost == best_cost:
                ties += 1
        if best is not None:
            break
    assert best is not None, ones
    return sorted(best, key=cube_key), ties


def format_kmap_terms(terms):
    if len(terms) == 1:
        return terms[0]
    rendered = [f"({term})" if " AND " in term else term for term in terms]
    return " OR ".join(rendered)


def join_terms(terms, connector, identity):
    if not terms:
        return identity
    if len(terms) == 1:
        return terms[0]
    return f" {connector} ".join(f"({term})" for term in terms)


def minterm(bits, variables):
    return " AND ".join(var if bit == "1" else f"NOT {var}"
                        for var, bit in zip(variables, bits))


def maxterm(bits, variables):
    return " OR ".join(var if bit == "0" else f"NOT {var}"
                       for var, bit in zip(variables, bits))


def oracle_answer(example):
    """Recompute the final answer from the problem text alone."""
    parts = parse_problem(example["problem"])
    values = parts["values"]
    variables = parts["variables"]
    rows = bit_rows(len(variables))
    if parts["variant"] == "dnf":
        terms = [minterm(row, variables) for row in rows if values[row] == 1]
        return f"DNF = {join_terms(terms, 'OR', '0')}"
    if parts["variant"] == "cnf":
        terms = [maxterm(row, variables) for row in rows if values[row] == 0]
        return f"CNF = {join_terms(terms, 'AND', '1')}"
    ones = {row for row, value in values.items() if value == 1}
    cover, ties = brute_force_min_cover(ones, len(variables))
    assert ties == 1, example["problem"]
    terms = [cube_term(cube, variables) for cube in cover]
    return f"simplified = {format_kmap_terms(terms)}"


def check_answer_semantics(example):
    """Evaluate the answer expression itself and compare to the table."""
    parts = parse_problem(example["problem"])
    values = parts["values"]
    variables = parts["variables"]
    answer = example["final_answer"]
    if answer.startswith("DNF = "):
        groups = parse_expression(answer[6:], "OR", "AND")
        assert truth_table_of(groups, "OR", variables) == values, answer
        ones = [row for row in values if values[row] == 1]
        assert len(groups) == len(ones), answer
        for group in groups:
            assert len(group) == len(variables), answer
    elif answer.startswith("CNF = "):
        groups = parse_expression(answer[6:], "AND", "OR")
        assert truth_table_of(groups, "AND", variables) == values, answer
        zeros = [row for row in values if values[row] == 0]
        assert len(groups) == len(zeros), answer
        for group in groups:
            assert len(group) == len(variables), answer
    else:
        assert answer.startswith("simplified = "), answer
        groups = parse_expression(answer[13:], "OR", "AND")
        assert truth_table_of(groups, "OR", variables) == values, answer
        ones = {row for row, value in values.items() if value == 1}
        cover, ties = brute_force_min_cover(ones, len(variables))
        assert ties == 1, answer
        answer_cubes = sorted((term_to_cube(group, variables)
                               for group in groups), key=cube_key)
        assert answer_cubes == cover, answer
    return True


def assignment_text(bits, variables):
    return ", ".join(f"{var}={bit}" for var, bit in zip(variables, bits))


def check_step_content(example):
    parts = parse_problem(example["problem"])
    values = parts["values"]
    variables = parts["variables"]
    fname = parts["fname"]
    rows = bit_rows(len(variables))
    answer = example["final_answer"]
    seen = set()
    row_label = col_label = None
    row_codes = col_codes = None
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        seen.add(op)
        if op == "BOOL_SETUP":
            if fields[1] != "variables " + ", ".join(variables):
                return False
            if parts["variant"] == "kmap":
                if fields[2] != "K-map simplify":
                    return False
            else:
                form = parts["variant"].upper()
                focus = "1" if form == "DNF" else "0"
                if fields[2] != f"{form} from {fname}={focus} rows":
                    return False
        elif op == "TRUTH_ROW":
            pieces = fields[1].split(", ")
            if len(pieces) != len(variables):
                return False
            bits = ""
            for var, piece in zip(variables, pieces):
                match = re.fullmatch(rf"{var}=([01])", piece)
                if match is None:
                    return False
                bits += match.group(1)
            if fields[2] != f"{fname}={values[bits]}":
                return False
        elif op == "MINTERM":
            row = fields[1]
            if values[row] != 1 or fields[2] != minterm(row, variables):
                return False
        elif op == "MAXTERM":
            row = fields[1]
            if values[row] != 0 or fields[2] != maxterm(row, variables):
                return False
        elif op == "DNF_FORM":
            if fields[1] != oracle_answer(example).replace("DNF = ", "", 1):
                return False
        elif op == "CNF_FORM":
            if fields[1] != oracle_answer(example).replace("CNF = ", "", 1):
                return False
        elif op == "KMAP_SETUP":
            head, _, body = fields[1].partition(" ")
            if head != "rows":
                return False
            row_pairs = [piece.split("=") for piece in body.split(",")]
            row_label = row_pairs[0][0]
            row_codes = [pair[1] for pair in row_pairs]
            if any(pair[0] != row_label for pair in row_pairs):
                return False
            head, _, body = fields[2].partition(" ")
            if head != "columns":
                return False
            col_pairs = [piece.split("=") for piece in body.split(",")]
            col_label = col_pairs[0][0]
            col_codes = [pair[1] for pair in col_pairs]
            if any(pair[0] != col_label for pair in col_pairs):
                return False
            if row_label + col_label != "".join(variables):
                return False
            grid = {r + c for r in row_codes for c in col_codes}
            if grid != set(rows):
                return False
        elif op == "KMAP_ROW":
            if row_codes is None:
                return False
            label, _, code = fields[1].partition("=")
            if label != row_label or code not in row_codes:
                return False
            expected = ", ".join(str(values[code + col])
                                 for col in col_codes)
            if fields[2] != expected:
                return False
        elif op == "KMAP_GROUP":
            cells = fields[1].split(", ")
            if sorted(cells) != cells:
                return False
            if any(values[cell] != 1 for cell in cells):
                return False
            group = parse_group(fields[2], "AND")
            cube = term_to_cube(group, variables)
            if cube_cells(cube) != frozenset(cells):
                return False
        elif op == "KMAP_SIMPLIFY":
            if fields[1] != oracle_answer(example).replace(
                    "simplified = ", "", 1):
                return False
        elif op == "CHECK":
            if fields[1] == "substitute":
                match = re.fullmatch(
                    rf"{fname}\(([01,]+)\) from (DNF|CNF) = ([01])",
                    fields[2])
                if match is None:
                    return False
                row = match.group(1).replace(",", "")
                if values[row] != int(match.group(3)):
                    return False
                if fields[3] != (f"{fname}({match.group(1)}) from table = "
                                 f"{match.group(3)}"):
                    return False
            elif fields[1] == "truth_table":
                ones = ", ".join(sorted(row for row in rows
                                        if values[row] == 1))
                if fields[2] != f"expression is 1 on {ones}":
                    return False
                if fields[3] != f"table is 1 on {ones}":
                    return False
            else:
                return False
        elif op == "Z":
            if fields[1:] != [answer]:
                return False
        else:
            return False
    if parts["variant"] == "kmap":
        required = {"BOOL_SETUP", "KMAP_SETUP", "KMAP_ROW", "KMAP_GROUP",
                    "KMAP_SIMPLIFY", "Z"}
    else:
        required = {"BOOL_SETUP", "TRUTH_ROW", "Z",
                    "MINTERM" if parts["variant"] == "dnf" else "MAXTERM",
                    "DNF_FORM" if parts["variant"] == "dnf" else "CNF_FORM"}
    return required <= seen


class TestBooleanAlgebraGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BooleanAlgebraGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_answer_expression_matches_truth_table(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_answer_semantics(result), result["problem"])

    def test_step_content(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_content(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("dnf", "cnf", "kmap"):
            gen = BooleanAlgebraGenerator(variant)
            for _ in range(80):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"boolean_algebra_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)
                self.assertEqual(result["final_answer"], oracle_answer(result),
                                 result["problem"])

    def test_widths_and_phrasings_are_varied(self):
        widths = set()
        starts = set()
        var_sets = set()
        func_names = set()
        for _ in range(600):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            widths.add(len(parts["variables"]))
            var_sets.add(tuple(parts["variables"]))
            func_names.add(parts["fname"])
            starts.add(result["problem"].split(" ")[0])
        self.assertGreaterEqual(len(widths), 3)
        self.assertGreaterEqual(len(starts), 4)
        self.assertGreaterEqual(len(var_sets), 6)
        self.assertGreaterEqual(len(func_names), 3)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BooleanAlgebraGenerator("bogus")

    def test_deterministic_under_seed(self):
        random.seed(2024)
        first = [self.gen.generate() for _ in range(20)]
        random.seed(2024)
        second = [self.gen.generate() for _ in range(20)]
        self.assertEqual([ex["problem"] for ex in first],
                         [ex["problem"] for ex in second])
        self.assertEqual([ex["steps"] for ex in first],
                         [ex["steps"] for ex in second])

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertNotIn(DELIM, result["problem"])
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
