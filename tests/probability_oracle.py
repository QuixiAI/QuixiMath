"""Independent parsers and brute-force solvers for the probability strand.

A9 requires the oracle to reach the answer by a different route than the
generator, so **this module never imports ``prob_common``** — every rule it
needs (enumeration order, compound labels, color codes, the supplied-constant
and two-way-table prose forms) is re-implemented here from the conventions in
``plans/probability_plan.md`` §3, and every probability comes back as an exact
``fractions.Fraction`` computed by brute-force enumeration.

Entry points:

- ``parse_experiment(text)`` -> the components described by a problem
  sentence; ``sample_space`` / ``item_space`` enumerate them.
- ``probability(points, test)`` -> Fraction by counting.
- ``parse_roster`` / ``parse_weights`` / ``parse_two_way`` / ``parse_pmf`` /
  ``parse_cdf`` / ``parse_transition_rows`` / ``parse_supplied`` /
  ``parse_phi_table`` -> the printed data structures.
- ``solve_linear(matrix, rhs)`` -> Gaussian elimination over Fraction.
"""
import itertools
import re
from collections import namedtuple
from fractions import Fraction

VOWELS = "AEIOU"
INT_RE = re.compile(r"-?\d+")
#: One printed value: a percent, a fraction, or a decimal/integer.
VALUE = r"-?\d+(?:\.\d+)?%|-?\d+/\d+|-?\d+(?:\.\d+)?"

#: One enumerated point: its printed label and its component parts.
Point = namedtuple("Point", "label parts")

TIMES = {"once": 1, "twice": 2, "three times": 3, "four times": 4,
         "five times": 5, "six times": 6, "seven times": 7,
         "eight times": 8}


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


def number(text):
    """Exact Fraction from '3/8', '0.375', '37.5%', '5', '-1/8'."""
    text = str(text).strip()
    if text.endswith("%"):
        return Fraction(text[:-1].strip()) / 100
    return Fraction(text)


def numbers_in(text):
    """Every fraction/decimal/percent token in ``text``, left to right."""
    return [number(tok) for tok in re.findall(VALUE, str(text))]


# ---------------------------------------------------------------------------
# Printed data structures
# ---------------------------------------------------------------------------


def parse_rosters(text):
    """Every ``{a, b, c}`` roster in ``text``, as lists of item strings."""
    out = []
    for body in re.findall(r"\{([^{}]*)\}", str(text)):
        body = body.strip()
        out.append([] if not body else [i.strip() for i in body.split(",")])
    return out


def parse_roster(text):
    """The first roster in ``text`` (``∅`` and ``{}`` give an empty list)."""
    rosters = parse_rosters(text)
    if not rosters:
        if "∅" in str(text):
            return []
        raise ValueError(f"no roster in {text!r}")
    return rosters[0]


def parse_weights(text):
    """Weighted atoms: ``P(a) = 1/10; P(b) = 1/5`` -> {'a': 1/10, ...}.

    Atom labels are single tokens; ``P(X=1)`` style rows are ignored here
    (use ``parse_pmf``)."""
    out = {}
    for atom, value in re.findall(
            r"P\(\s*([^)=,]+?)\s*\)\s*=\s*(" + VALUE + ")", str(text)):
        out[atom.strip()] = number(value)
    return out


def parse_pmf(text):
    """A pmf table: ``P(X=1) = 1/8``, ``P(S=0) = 1/8`` or ``P(0,1) = 1/8``.

    Keys are the inside of the parentheses with spaces normalized, so
    ``P(X=1)`` -> ``'X=1'`` and ``P(0, 1)`` -> ``'0,1'``."""
    out = {}
    for key, value in re.findall(
            r"P\(\s*([^)]+?)\s*\)\s*=\s*(" + VALUE + ")", str(text)):
        out[re.sub(r"\s+", "", key)] = number(value)
    return out


def parse_cdf(text):
    """A cdf table: ``F(1) = 1/8; F(2) = 1/2`` -> {'1': 1/8, '2': 1/2}."""
    out = {}
    for key, value in re.findall(
            r"F\(\s*([^)]+?)\s*\)\s*=\s*(" + VALUE + ")", str(text)):
        out[key.strip()] = number(value)
    return out


def parse_two_way(text):
    """Two-way table cells printed as ``<row>=<v> and <col>=<w>: n``.

    Returns ``(row_name, col_name, cells)`` with ``cells`` keyed by
    ``(row_value, col_value)``."""
    found = re.findall(
        r"(\w[\w ]*?)=([\w.+-]+) and (\w[\w ]*?)=([\w.+-]+):\s*(\d+)",
        str(text))
    if not found:
        raise ValueError("no two-way table cells found")
    row_name, col_name = found[0][0].strip(), found[0][2].strip()
    cells = {}
    for rname, rvalue, cname, cvalue, count in found:
        if rname.strip() != row_name or cname.strip() != col_name:
            raise ValueError("inconsistent table variable names")
        cells[(rvalue, cvalue)] = int(count)
    return row_name, col_name, cells


def two_way_totals(cells):
    """(row totals, column totals, grand total) for parsed table cells."""
    rows, cols = {}, {}
    for (rvalue, cvalue), count in cells.items():
        rows[rvalue] = rows.get(rvalue, 0) + count
        cols[cvalue] = cols.get(cvalue, 0) + count
    return rows, cols, sum(cells.values())


def parse_transition_rows(text):
    """Markov rows printed as ``P1 = (1/2, 1/4, 1/4)`` -> {'1': [...]}}."""
    out = {}
    for name, body in re.findall(r"P(\w+)\s*=\s*\(([^)]*)\)", str(text)):
        out[name] = [number(v) for v in body.split(",")]
    return out


def parse_supplied(text):
    """Supplied constants: ``e^-2 = 0.1353`` -> {'e^-2': 1353/10000}."""
    out = {}
    for label, value in re.findall(
            r"(e\^\(?-?[\d./]+\)?)\s*=\s*(\d+\.\d+)", str(text)):
        out[label] = Fraction(value)
    return out


def parse_phi_table(text):
    """The Φ excerpt: ``z=1.50: 0.9332`` -> {'1.50': Fraction(9332, 10000)}."""
    return {z: Fraction(v)
            for z, v in re.findall(r"z=(\d+\.\d{2}):\s*(0\.\d{4})", str(text))}


# ---------------------------------------------------------------------------
# Experiment prose
# ---------------------------------------------------------------------------


def _color_codes(colors):
    """Printed codes for bag colors: initials when distinct, else names."""
    initials = [c[:1].upper() for c in colors]
    if len(set(initials)) == len(initials):
        return initials
    return list(colors)


def _clause_component(clause):
    """One component (kind, outcome labels, item labels) from a clause."""
    text = clause.strip().rstrip(".")
    if re.search(r"\bcoins?\b", text):
        return {"kind": "coin", "outcomes": ["H", "T"], "items": ["H", "T"],
                "parts": ["H", "T"]}
    sided = re.search(r"(\d+)-sided die", text)
    faces = re.search(r"faces numbered (\d+) to (\d+)", text)
    if sided or faces:
        if sided:
            values = [str(v) for v in range(1, int(sided.group(1)) + 1)]
        else:
            lo, hi = int(faces.group(1)), int(faces.group(2))
            values = [str(v) for v in range(lo, hi + 1)]
        return {"kind": "die", "outcomes": values, "items": values,
                "parts": values}
    spun = re.search(r"(?:sectors|sections)(?: labelled| marked)? "
                     r"([^;]+?) is spun", text)
    if spun:
        values = [v.strip() for v in spun.group(1).split(",")]
        return {"kind": "spinner", "outcomes": values, "items": values,
                "parts": values}
    inventory = re.findall(r"(\d+) ([a-z]+) (?:marbles?|counters?|balls?)",
                           text)
    if inventory:
        colors = [name for _, name in inventory]
        counts = [int(n) for n, _ in inventory]
        codes = _color_codes(colors)
        items, parts = [], []
        for code, color, count in zip(codes, colors, counts):
            for index in range(1, count + 1):
                items.append(f"{code}{index}")
                parts.append(color)
        return {"kind": "bag", "outcomes": codes, "items": items,
                "parts": parts, "outcome_parts": colors}
    cards = re.search(r"(?:cards|tickets|tags) numbered (\d+) to (\d+)", text)
    if cards:
        lo, hi = int(cards.group(1)), int(cards.group(2))
        values = [str(v) for v in range(lo, hi + 1)]
        return {"kind": "cards", "outcomes": values, "items": values,
                "parts": values}
    word = re.search(r"(?:spelling|letters of|word) ([A-Z]{2,})", text)
    if word:
        letters = list(word.group(1))
        distinct = []
        for letter in letters:
            if letter not in distinct:
                distinct.append(letter)
        items, used = [], {}
        for letter in letters:
            if letters.count(letter) == 1:
                items.append(letter)
            else:
                used[letter] = used.get(letter, 0) + 1
                items.append(f"{letter}{used[letter]}")
        return {"kind": "tiles", "outcomes": distinct, "items": items,
                "parts": letters, "outcome_parts": distinct}
    stages = re.findall(r"one ([\w ]+?) from ([^;]+)", text)
    if stages:
        pools = [[v.strip() for v in options.split(",")]
                 for _, options in stages]
        labels = [" + ".join(combo) for combo in itertools.product(*pools)]
        return {"kind": "menu", "outcomes": labels, "items": labels,
                "parts": labels, "pools": pools,
                "stages": [name.strip() for name, _ in stages]}
    raise ValueError(f"unrecognized experiment clause: {clause!r}")


def _experiment_sentence(text):
    """The sentence of ``text`` that describes the experiment."""
    for sentence in re.split(r"(?<=[.?])\s+", str(text).replace("\n", " ")):
        try:
            _clause_component(sentence.split(" and ")[0])
        except ValueError:
            continue
        return sentence.strip()
    raise ValueError(f"no experiment sentence in {text!r}")


def parse_experiment(text):
    """Components of the experiment described in ``text``, in order.

    Repeated trials (``a fair coin is flipped twice``) expand into one
    component per trial."""
    sentence = _experiment_sentence(text)
    components = []
    for clause in sentence.split(" and "):
        clause = clause.strip().rstrip(".")
        times = 1
        for word, count in TIMES.items():
            if clause.endswith(" " + word):
                clause, times = clause[:-(len(word) + 1)], count
                break
        component = _clause_component(clause)
        components.extend([component] * times)
    return components


def _label(parts):
    """Compound label in the §3 dialect: ``(3, 4)`` for numbers, else
    glued."""
    if len(parts) > 1 and all(INT_RE.fullmatch(p) for p in parts):
        return "(" + ", ".join(parts) + ")"
    return "".join(parts)


def _space(components, field):
    """Product of one field of each component, as ``Point``s."""
    pools = []
    for comp in components:
        labels = comp[field]
        if field == "items":
            parts = comp["parts"]
        else:
            parts = comp.get("outcome_parts", comp[field])
        pools.append(list(zip(labels, parts)))
    points = []
    for combo in itertools.product(*pools):
        labels = [label for label, _ in combo]
        parts = tuple(part for _, part in combo)
        points.append(Point(_label(labels) if len(labels) > 1 else labels[0],
                            parts))
    return points


def sample_space(components):
    """Printed outcomes of a compound experiment, in enumeration order."""
    return _space(components, "outcomes")


def item_space(components):
    """Equally likely labelled objects, in enumeration order."""
    return _space(components, "items")


def outcomes_from_text(text):
    """Printed outcome labels for the experiment described in ``text``."""
    return [p.label for p in sample_space(parse_experiment(text))]


def items_from_text(text):
    """Equally likely item labels for the experiment described in ``text``."""
    return [p.label for p in item_space(parse_experiment(text))]


# ---------------------------------------------------------------------------
# Brute-force enumeration
# ---------------------------------------------------------------------------


def probability(points, test):
    """P(event) by counting equally likely points."""
    points = list(points)
    hits = sum(1 for p in points if test(p))
    return Fraction(hits, len(points))


def weighted_probability(weights, test):
    """P(event) on atoms carrying Fraction weights."""
    return sum((Fraction(w) for atom, w in dict(weights).items()
                if test(atom)), Fraction(0))


def draws_with_replacement(items, k):
    """All ordered draws of ``k`` items with replacement."""
    return [tuple(c) for c in itertools.product(items, repeat=k)]


def draws_without_replacement(items, k):
    """All ordered draws of ``k`` distinct items."""
    return list(itertools.permutations(items, k))


def unordered_draws(items, k):
    """All unordered draws of ``k`` distinct items."""
    return list(itertools.combinations(items, k))


def counts_to_items(counts):
    """``[('red', 2), ('blue', 1)]`` -> ['red1', 'red2', 'blue1']."""
    out = []
    for name, count in counts:
        out.extend(f"{name}{i}" for i in range(1, int(count) + 1))
    return out


def is_vowel(letter):
    """True for A, E, I, O, U."""
    return str(letter).upper() in VOWELS


# ---------------------------------------------------------------------------
# Exact linear algebra
# ---------------------------------------------------------------------------


def solve_linear(matrix, rhs):
    """Gaussian elimination over Fraction; returns the unique solution.

    Raises ValueError when the system is singular or not square."""
    size = len(matrix)
    if any(len(row) != size for row in matrix) or len(rhs) != size:
        raise ValueError("solve_linear needs a square system")
    rows = [[Fraction(v) for v in row] + [Fraction(rhs[i])]
            for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = next((r for r in range(col, size) if rows[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular system")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        lead = rows[col][col]
        rows[col] = [v / lead for v in rows[col]]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [v - factor * w for v, w in zip(rows[r], rows[col])]
    return [row[size] for row in rows]
