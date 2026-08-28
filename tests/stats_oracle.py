"""Independent parsers and exact routines for the statistics strand (A9).

Every statistics test recomputes a generator's ``final_answer`` **from the
problem text alone**: it parses the rendered display with the parsers here
and re-derives the answer with the exact routines here. This module is
deliberately written from the *rendering specification* in
``plans/statistics_plan.md`` §3, not from ``stats_common.py`` — it must never
import ``stats_common`` or ``prob_common``, so that a bug shared between a
renderer and its parser cannot hide.

Parsers (all raise ``ValueError`` on anything that does not fit the grammar):

- ``parse_dot_plot`` / ``parse_line_plot`` — rows back to counts and data
- ``parse_tally`` — ``////\\ //`` back to counts
- ``parse_stem_leaf`` — stems, leaves and the key line back to values
- ``parse_box_plot`` — the ASCII columns back to five numbers and outliers
- ``parse_two_way`` — the aligned table back to labels and cells
- ``parse_bins`` — ``0-9: 3; 10-19: 5``
- ``parse_phi_table`` / ``parse_inverse_z`` / ``parse_inline_constants``
- ``find_displays`` / ``parse_display`` — the grammar sweep the conventions
  test runs over every problem

Exact routines: ``mean``, ``median``, ``variance``, ``sd``, ``five_summary``,
``iqr``, ``enumerate_samples``, ``binomial_tail``, ``chi_terms``, ``anova``,
``nearest_rank``.
"""
import itertools
import math
import re
from fractions import Fraction

BAR = "∣"          # U+2223, the display separator (never ASCII '|')
MARK = "●"
BOX_PREFIX = 7

# ---------------------------------------------------------------------------
# Number reading
# ---------------------------------------------------------------------------

_DECIMAL = re.compile(r"-?\d+(?:\.\d+)?")
_FRACTION_LABEL = re.compile(r"^(-)?(?:(\d+)(?: (\d+)/(\d+))?|(\d+)/(\d+))$")


def read_number(text):
    """'12' -> 12, '2.5' -> Fraction(5, 2), '3/4' -> Fraction(3, 4),
    '1 1/4' -> Fraction(5, 4)."""
    text = text.strip()
    m = _FRACTION_LABEL.match(text)
    if not m:
        raise ValueError(f"not a number: {text!r}")
    sign = -1 if m.group(1) else 1
    if m.group(5):
        value = Fraction(int(m.group(5)), int(m.group(6)))
    else:
        value = Fraction(int(m.group(2)))
        if m.group(3):
            value += Fraction(int(m.group(3)), int(m.group(4)))
    return sign * value


def read_decimal(text):
    """Exact Fraction for a plain decimal literal ('0.0228')."""
    text = text.strip()
    if not re.fullmatch(r"-?\d+(?:\.\d+)?", text):
        raise ValueError(f"not a decimal: {text!r}")
    if "." not in text:
        return Fraction(int(text))
    whole, frac = text.split(".")
    sign = -1 if whole.startswith("-") else 1
    whole = whole.lstrip("+-") or "0"
    return sign * (Fraction(int(whole)) + Fraction(int(frac), 10 ** len(frac)))


def is_square(fr):
    """True when the Fraction is the square of a rational."""
    fr = Fraction(fr)
    if fr < 0:
        return False
    return (math.isqrt(fr.numerator) ** 2 == fr.numerator
            and math.isqrt(fr.denominator) ** 2 == fr.denominator)


def exact_sqrt(fr):
    fr = Fraction(fr)
    if not is_square(fr):
        raise ValueError(f"{fr} has no rational square root")
    return Fraction(math.isqrt(fr.numerator), math.isqrt(fr.denominator))


def parse_number_list(text, label=None):
    """The comma-separated data list out of a sentence. With ``label`` the
    list is the one introduced by ``label:`` ('before: 12, 15, 17')."""
    if label is not None:
        m = re.search(re.escape(label) + r"\s*:\s*([-\d ,./]+)", text)
        if not m:
            raise ValueError(f"no list labelled {label!r}")
        body = m.group(1)
    else:
        m = re.search(r"(-?\d[\d ,./]*\d)", text)
        if not m:
            raise ValueError("no data list found")
        body = m.group(1)
    out = []
    for chunk in body.split(","):
        chunk = chunk.strip().rstrip(".")
        if chunk:
            out.append(read_number(chunk))
    if not out:
        raise ValueError("empty data list")
    return out


# ---------------------------------------------------------------------------
# Display parsers
# ---------------------------------------------------------------------------


def _plot_rows(text):
    """[(label, marks)] for the rows of a ``label ∣ ● ●`` display."""
    rows = []
    for line in text.splitlines():
        if BAR not in line:
            if line.strip():
                continue
            continue
        left, right = line.split(BAR, 1)
        rows.append((left.strip(), right.strip()))
    if not rows:
        raise ValueError("no plot rows found")
    return rows


def _mark_count(marks):
    if marks and set(marks.split(" ")) - {MARK}:
        raise ValueError(f"unexpected marks: {marks!r}")
    return 0 if not marks else marks.count(MARK)


def parse_dot_plot(text):
    """``{value: count}`` from a dot plot. Rows must run over every integer
    from the smallest to the largest, empty rows included."""
    counts = {}
    order = []
    for label, marks in _plot_rows(text):
        if not re.fullmatch(r"-?\d+", label):
            raise ValueError(f"dot-plot row label is not an integer: {label!r}")
        value = int(label)
        if value in counts:
            raise ValueError(f"repeated dot-plot row {value}")
        counts[value] = _mark_count(marks)
        order.append(value)
    if order != list(range(order[0], order[-1] + 1)):
        raise ValueError(f"dot-plot rows are not consecutive: {order}")
    if counts[order[0]] == 0 or counts[order[-1]] == 0:
        raise ValueError("dot-plot end rows must hold data")
    return counts


def dot_plot_data(text):
    """The sorted data list a dot plot stands for."""
    counts = parse_dot_plot(text)
    return [v for v in sorted(counts) for _ in range(counts[v])]


def parse_line_plot(text):
    """``{Fraction: count}`` from a fraction line plot. Rows must be evenly
    spaced by the plot's unit."""
    counts = {}
    order = []
    for label, marks in _plot_rows(text):
        value = read_number(label)
        if value in counts:
            raise ValueError(f"repeated line-plot row {label}")
        counts[value] = _mark_count(marks)
        order.append(value)
    if len(order) > 1:
        unit = order[1] - order[0]
        if unit <= 0:
            raise ValueError("line-plot rows must ascend")
        for a, b in zip(order, order[1:]):
            if b - a != unit:
                raise ValueError(f"line-plot rows are not evenly spaced: {order}")
    return counts


def line_plot_data(text):
    counts = parse_line_plot(text)
    return [v for v in sorted(counts) for _ in range(counts[v])]


def parse_tally(text):
    """``{category: count}`` from a tally table. A group of five is exactly
    four slashes and a crossing backslash."""
    counts = {}
    labels = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"tally row without a colon: {line!r}")
        cat, marks = line.split(":", 1)
        cat, marks = cat.strip(), marks.strip()
        total = 0
        for group in marks.split(" ") if marks else []:
            if group == "////" + "\\":
                total += 5
            elif re.fullmatch(r"/{1,4}", group):
                total += len(group)
            else:
                raise ValueError(f"bad tally group {group!r} in {line!r}")
        counts[cat] = total
        labels.append(cat)
    if not counts:
        raise ValueError("no tally rows found")
    if labels != sorted(labels):
        raise ValueError(f"tally rows are not alphabetical: {labels}")
    return counts


def parse_stem_leaf(text):
    """The sorted values a stem-and-leaf plot stands for. Uses the key line
    to decide the place value, checks the header, that stems are contiguous
    and that leaves ascend."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines or BAR not in lines[0] or "Leaves" not in lines[0]:
        raise ValueError("stem-and-leaf plot needs a 'Stem ∣ Leaves' header")
    key_lines = [ln for ln in lines if ln.startswith("Key:")]
    if len(key_lines) != 1:
        raise ValueError("stem-and-leaf plot needs exactly one key line")
    m = re.fullmatch(r"Key: (\d+) " + BAR + r" (\d) means (\d+(?:\.\d)?)",
                     key_lines[0].strip())
    if not m:
        raise ValueError(f"bad key line: {key_lines[0]!r}")
    k_stem, k_leaf, k_value = int(m.group(1)), int(m.group(2)), m.group(3)
    decimal = "." in k_value
    scale = Fraction(1, 10) if decimal else 1
    place = Fraction(1) if decimal else Fraction(10)
    if k_stem * place + k_leaf * scale != read_decimal(k_value):
        raise ValueError(f"key line does not agree with itself: {key_lines[0]!r}")

    stems, values = [], []
    for line in lines[1:]:
        if line.startswith("Key:"):
            continue
        left, right = line.split(BAR, 1)
        stem = int(left.strip())
        leaves = right.split()
        if any(not re.fullmatch(r"\d", x) for x in leaves):
            raise ValueError(f"leaves must be single digits: {line!r}")
        digits = [int(x) for x in leaves]
        if digits != sorted(digits):
            raise ValueError(f"leaves are not ascending: {line!r}")
        stems.append(stem)
        values.extend(stem * place + d * scale for d in digits)
    if not stems:
        raise ValueError("no stem rows found")
    if stems != list(range(stems[0], stems[-1] + 1)):
        raise ValueError(f"stems are not contiguous: {stems}")
    if not values:
        raise ValueError("stem-and-leaf plot has no leaves")
    return sorted(values)


def parse_box_plot(text):
    """``{label: {'min','q1','median','q3','max','outliers'}}`` read off the
    ASCII columns, plus ``'scale'``. Column c of a plot line stands for
    ``scale_start + c - 7``; the tick line is checked against the scale."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 3:
        raise ValueError("a box plot needs a scale, a tick line and a plot")
    scale_line, tick_line = lines[0], lines[1]
    if not scale_line.startswith("Scale: "):
        raise ValueError("box plot must start with 'Scale: '")
    ticks = []
    body = scale_line[BOX_PREFIX:]
    for col in range(0, len(body), 5):
        cell = body[col:col + 5].strip()
        if not cell:
            raise ValueError(f"missing tick label at column {col}")
        ticks.append(int(cell))
    if any(t % 5 for t in ticks):
        raise ValueError(f"tick labels must be multiples of 5: {ticks}")
    if any(b - a != 5 for a, b in zip(ticks, ticks[1:])):
        raise ValueError(f"ticks must step by 5: {ticks}")
    start = ticks[0]
    expected_ticks = " " * BOX_PREFIX + "+" + "----+" * (len(ticks) - 1)
    if tick_line != expected_ticks:
        raise ValueError(f"bad tick line: {tick_line!r}")

    out = {"scale": (ticks[0], ticks[-1])}
    for line in lines[2:]:
        if ":" not in line[:BOX_PREFIX]:
            raise ValueError(f"plot line needs a label prefix: {line!r}")
        label = line[:BOX_PREFIX].split(":")[0].strip()
        cells = line[BOX_PREFIX:]
        pos = {}
        outliers = []
        for col, ch in enumerate(cells):
            value = start + col
            if ch == " ":
                continue
            if ch == "o":
                outliers.append(value)
            elif ch in "*[]:":
                pos.setdefault(ch, []).append(value)
            elif ch in "-=":
                pos.setdefault(ch, []).append(value)
            else:
                raise ValueError(f"unexpected box-plot character {ch!r}")
        stars = pos.get("*", [])
        if len(stars) != 2:
            raise ValueError(f"box plot needs exactly two '*': {line!r}")
        if len(pos.get("[", [])) != 1 or len(pos.get("]", [])) != 1:
            raise ValueError(f"box plot needs one '[' and one ']': {line!r}")
        if len(pos.get(":", [])) != 1:
            raise ValueError(f"box plot needs exactly one ':': {line!r}")
        mn, mx = stars
        q1, q3 = pos["["][0], pos["]"][0]
        med = pos[":"][0]
        if not (mn < q1 < med < q3 < mx):
            raise ValueError(f"box plot is not strictly ordered: {line!r}")
        inside = sorted(pos.get("=", []))
        if inside != [v for v in range(q1 + 1, q3) if v != med]:
            raise ValueError(f"box fill does not match the quartiles: {line!r}")
        whisk = sorted(pos.get("-", []))
        want = ([v for v in range(mn + 1, q1)]
                + [v for v in range(q3 + 1, mx)])
        if whisk != want:
            raise ValueError(f"whiskers do not reach the '*' marks: {line!r}")
        out[label] = {"min": mn, "q1": q1, "median": Fraction(med),
                      "q3": q3, "max": mx, "outliers": outliers}
    if len(out) < 2:
        raise ValueError("no box-plot rows found")
    return out


def box_plot_summary(text, label=None):
    """The five-number summary of one plot (the only one, by default)."""
    parsed = parse_box_plot(text)
    plots = {k: v for k, v in parsed.items() if k != "scale"}
    if label is None:
        if len(plots) != 1:
            raise ValueError("more than one plot — name the one you want")
        label = next(iter(plots))
    p = plots[label]
    return (p["min"], p["q1"], p["median"], p["q3"], p["max"])


def parse_two_way(text):
    """``(row_labels, col_labels, cells)`` from an aligned two-way table.
    Cells are read out of the columns the header labels end in, so row
    labels that end in a digit ('Grade 9') stay intact."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("a two-way table needs a header and a body")
    header = lines[0]
    col_labels, ends = [], []
    for m in re.finditer(r"\S+(?: \S+)*?(?=\s{2,}|$)", header):
        if m.start() == 0:
            continue                 # the corner label, not a column
        col_labels.append(m.group(0))
        ends.append(m.end())
    if not col_labels:
        raise ValueError("no column headers found")
    row_labels, cells = [], []
    for line in lines[1:]:
        row = []
        first = len(line)
        for end in ends:
            if end > len(line):
                raise ValueError(f"row is shorter than the header: {line!r}")
            j = end
            while j > 0 and line[j - 1] != " ":
                j -= 1
            cell = line[j:end].strip()
            if not cell:
                raise ValueError(f"missing cell before column {end}: {line!r}")
            first = min(first, j)
            row.append(cell)
        label = line[:first].strip()
        if not label:
            raise ValueError(f"row without a label: {line!r}")
        row_labels.append(label)
        cells.append(row)
    return row_labels, col_labels, cells


def two_way_counts(text):
    """``{(row, col): int}`` for the body cells, skipping Total margins."""
    row_labels, col_labels, cells = parse_two_way(text)
    out = {}
    for r, row in zip(row_labels, cells):
        for c, value in zip(col_labels, row):
            if r == "Total" or c == "Total":
                continue
            out[(r, c)] = int(value)
    return out


_BIN = re.compile(r"(\d+)\s*-\s*(\d+)\s*:\s*(\d+)")


def parse_bins(text):
    """``[((lo, hi), count)]`` from ``0-9: 3; 10-19: 5``. Bins must be
    contiguous, equal width and a multiple of 5 wide."""
    found = [(int(a), int(b), int(c)) for a, b, c in _BIN.findall(text)]
    if not found:
        raise ValueError("no histogram bins found")
    width = found[0][1] - found[0][0] + 1
    if width % 5:
        raise ValueError(f"bin width {width} is not a multiple of 5")
    for lo, hi, _ in found:
        if hi - lo + 1 != width:
            raise ValueError(f"bin {lo}-{hi} does not have width {width}")
    for (lo1, _, _), (lo2, _, _) in zip(found, found[1:]):
        if lo2 - lo1 != width:
            raise ValueError(f"bins {lo1} and {lo2} are not contiguous")
    return [((lo, hi), c) for lo, hi, c in found]


_PHI_ROW = re.compile(r"z=(-?\d+(?:\.\d+)?): (\d\.\d{4})")


def parse_phi_table(text):
    """``{Fraction z: Fraction Φ(z)}`` from the inline standard-normal
    excerpt."""
    if "Standard normal table" not in text:
        raise ValueError("no Φ excerpt found")
    rows = _PHI_ROW.findall(text)
    if not rows:
        raise ValueError("Φ excerpt has no rows")
    out = {}
    for z, p in rows:
        if float(z) < 0:
            raise ValueError("negative z is never tabulated")
        out[read_decimal(z)] = read_decimal(p)
    if len(out) != len(rows):
        raise ValueError("repeated Φ rows")
    return out


_INV_ROW = re.compile(r"(\d+(?:\.\d+)?)(?:st|nd|rd|th)"
                      r"(?: percentile)? z = (-?\d+(?:\.\d+)?)")


def parse_inverse_z(text):
    """``{Fraction percentile: Fraction z}`` from
    ``Selected z-scores: 80th percentile z = 0.84; 90th z = 1.28; …``."""
    if "Selected z-scores:" not in text:
        raise ValueError("no inverse-normal excerpt found")
    body = text.split("Selected z-scores:", 1)[1]
    body = body.split("\n", 1)[0]
    rows = _INV_ROW.findall(body)
    if not rows:
        raise ValueError("inverse-normal excerpt has no rows")
    out = {}
    for p, z in rows:
        key = read_decimal(p)
        if key in out:
            raise ValueError(f"repeated percentile {p}")
        if not 0 < key < 100:
            raise ValueError(f"percentile out of range: {p}")
        out[key] = read_decimal(z)
    if sorted(out) != list(out):
        raise ValueError("percentiles must ascend")
    return out


_CONSTANTS = (
    ("F", re.compile(r"F critical value = (\d+(?:\.\d+)?) \(df (\d+), (\d+)\)")),
    ("chi2", re.compile(r"χ² critical value = (\d+(?:\.\d+)?) \(df = (\d+)\)")),
    ("t", re.compile(r"t\* = (-?\d+(?:\.\d+)?) \(df = (\d+)\)")),
    ("z", re.compile(r"z\* = (-?\d+(?:\.\d+)?)")),
)


def parse_inline_constants(text):
    """``[(kind, value, df)]`` for every inline supplied constant:
    ``z* = 1.96``, ``t* = 2.262 (df = 9)``,
    ``χ² critical value = 5.991 (df = 2)``,
    ``F critical value = 4.26 (df 2, 9)``."""
    out = []
    for kind, pattern in _CONSTANTS:
        for m in pattern.finditer(text):
            if kind == "F":
                out.append((kind, read_decimal(m.group(1)),
                            (int(m.group(2)), int(m.group(3)))))
            elif kind in ("chi2", "t"):
                out.append((kind, read_decimal(m.group(1)), int(m.group(2))))
            else:
                out.append((kind, read_decimal(m.group(1)), None))
    return out


# ---------------------------------------------------------------------------
# The grammar sweep: find every rendered display in a problem and parse it
# ---------------------------------------------------------------------------

PARSERS = {
    "dot_plot": parse_dot_plot,
    "line_plot": parse_line_plot,
    "tally": parse_tally,
    "stem_leaf": parse_stem_leaf,
    "box_plot": parse_box_plot,
    "two_way": parse_two_way,
    "bins": parse_bins,
    "phi_table": parse_phi_table,
    "inverse_z": parse_inverse_z,
}

_TALLY_LINE = re.compile(r"^[^:\s][^:]*:(?:$| [/\\ ]+$)")
_BOX_LINE = re.compile(r"^[A-Za-z][A-Za-z0-9 ]{0,5}: *[-*\[\]:=o ]*$")
_NUMERIC_CELL = re.compile(r"-?\d+(?:\.\d+)?%?|\?")


def _is_two_way_header(line):
    return (line.startswith(" ") and line.strip()
            and not any(_NUMERIC_CELL.fullmatch(tok) for tok in line.split()))


def _is_two_way_row(line):
    toks = line.split()
    return len(toks) >= 3 and _NUMERIC_CELL.fullmatch(toks[-1]) is not None


def find_displays(problem):
    """``[(kind, block_text)]`` for every rendered display in a problem.

    The conventions test parses each block with ``parse_display``: a display
    that does not parse is a broken rendering (or an undocumented new one).
    """
    lines = problem.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("Scale: "):
            j = i + 1
            if j < len(lines) and lines[j].startswith(" " * BOX_PREFIX + "+"):
                j += 1
                while j < len(lines) and _BOX_LINE.match(lines[j]):
                    j += 1
            out.append(("box_plot", "\n".join(lines[i:j])))
            i = j
            continue
        if BAR in line and "Leaves" in line:
            j = i + 1
            while j < len(lines) and BAR in lines[j] \
                    and not lines[j].startswith("Key:"):
                j += 1
            if j < len(lines) and lines[j].startswith("Key:"):
                j += 1
            out.append(("stem_leaf", "\n".join(lines[i:j])))
            i = j
            continue
        if BAR in line:
            j = i
            while j < len(lines) and BAR in lines[j]:
                j += 1
            block = "\n".join(lines[i:j])
            labels = [ln.split(BAR, 1)[0].strip() for ln in lines[i:j]]
            kind = ("dot_plot" if all(re.fullmatch(r"-?\d+", x) for x in labels)
                    else "line_plot")
            out.append((kind, block))
            i = j
            continue
        if _TALLY_LINE.match(line) and "/" in line:
            j = i
            while j < len(lines) and _TALLY_LINE.match(lines[j]):
                j += 1
            out.append(("tally", "\n".join(lines[i:j])))
            i = j
            continue
        if _is_two_way_header(line) and i + 1 < len(lines) \
                and _is_two_way_row(lines[i + 1]):
            j = i + 1
            while j < len(lines) and _is_two_way_row(lines[j]):
                j += 1
            out.append(("two_way", "\n".join(lines[i:j])))
            i = j
            continue
        if "Standard normal table" in line:
            out.append(("phi_table", line))
        if "Selected z-scores:" in line:
            out.append(("inverse_z", line))
        if _BIN.search(line):
            out.append(("bins", line))
        i += 1
    return out


def parse_display(kind, text):
    """Parse one block found by ``find_displays``; raises on a bad grammar."""
    return PARSERS[kind](text)


# ---------------------------------------------------------------------------
# Exact statistical routines
# ---------------------------------------------------------------------------


def mean(values):
    values = [Fraction(v) for v in values]
    if not values:
        raise ValueError("mean of an empty list")
    return sum(values, Fraction(0)) / len(values)


def median(values):
    s = sorted(Fraction(v) for v in values)
    n = len(s)
    if not n:
        raise ValueError("median of an empty list")
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def mode(values):
    """Every most-frequent value, ascending (empty when all counts tie)."""
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    top = max(counts.values())
    if min(counts.values()) == top:
        return []
    return sorted(v for v, c in counts.items() if c == top)


def variance(values, sample=False):
    """Σ(x - x̄)² / n, or / (n - 1) when ``sample``; exact."""
    values = [Fraction(v) for v in values]
    n = len(values)
    if n < 2:
        raise ValueError("variance needs at least two values")
    m = mean(values)
    ss = sum((v - m) ** 2 for v in values)
    return ss / (n - 1 if sample else n)


def sd(values, sample=False, exact=True):
    """√variance — a Fraction when the variance is a perfect-square
    rational. With ``exact=False`` a float comes back instead."""
    var = variance(values, sample=sample)
    if not exact:
        return math.sqrt(var)
    return exact_sqrt(var)


def five_summary(values):
    """``(min, Q1, median, Q3, max)`` by the median-exclusive-halves rule
    stated in every problem that uses it."""
    s = sorted(Fraction(v) for v in values)
    n = len(s)
    if n < 4:
        raise ValueError("a five-number summary needs at least four values")
    half = n // 2
    lower, upper = (s[:half], s[half + 1:]) if n % 2 else (s[:half], s[half:])
    return (s[0], median(lower), median(s), median(upper), s[-1])


def iqr(values):
    _, q1, _, q3, _ = five_summary(values)
    return q3 - q1


def outliers(values):
    """Values outside the 1.5×IQR fences, ascending."""
    _, q1, _, q3, _ = five_summary(values)
    spread = Fraction(3, 2) * (q3 - q1)
    lo, hi = q1 - spread, q3 + spread
    return sorted(Fraction(v) for v in values
                  if Fraction(v) < lo or Fraction(v) > hi)


def nearest_rank(values, k):
    """The k-th percentile by the nearest-rank rule, position
    ``ceil(k·n/100)`` in the sorted list."""
    s = sorted(values)
    n = len(s)
    pos = Fraction(k) * n / 100
    idx = -((-pos.numerator) // pos.denominator)
    return s[max(1, min(idx, n)) - 1]


def percentile_rank(values, target):
    """Percent of values strictly below ``target``."""
    s = list(values)
    return Fraction(100 * sum(1 for v in s if v < target), len(s))


def enumerate_samples(pop, n, replace=False):
    """Every equally likely sample of size ``n``: ordered tuples with
    replacement, index-combinations without (so a repeated population value
    still counts once per copy)."""
    pop = list(pop)
    idx = range(len(pop))
    combos = (itertools.product(idx, repeat=n) if replace
              else itertools.combinations(idx, n))
    return [tuple(pop[i] for i in combo) for combo in combos]


def sampling_distribution(pop, n, replace=False, statistic=mean):
    """``{value: Fraction probability}`` of a statistic over every sample."""
    samples = enumerate_samples(pop, n, replace)
    total = len(samples)
    out = {}
    for s in samples:
        key = statistic(s)
        out[key] = out.get(key, Fraction(0)) + Fraction(1, total)
    return dict(sorted(out.items()))


def binomial_pmf(n, k, p):
    p = Fraction(p)
    return Fraction(math.comb(n, k)) * p ** k * (1 - p) ** (n - k)


def binomial_tail(n, k, p, tail="ge"):
    """Exact ``P(X >= k)`` (``tail='ge'``) or ``P(X <= k)`` (``'le'``)."""
    p = Fraction(p)
    rng = range(k, n + 1) if tail == "ge" else range(0, k + 1)
    if tail not in ("ge", "le"):
        raise ValueError("tail must be 'ge' or 'le'")
    return sum((binomial_pmf(n, i, p) for i in rng), Fraction(0))


def chi_terms(observed, expected):
    """``([(O - E)²/E], total)`` exactly."""
    if len(observed) != len(expected):
        raise ValueError("observed and expected must line up")
    terms = [Fraction(o - e) ** 2 / Fraction(e)
             for o, e in zip(observed, expected)]
    return terms, sum(terms, Fraction(0))


def chi_expected(table):
    """Row×column expected counts from a two-way table of ints."""
    rows = [sum(r) for r in table]
    cols = [sum(r[j] for r in table) for j in range(len(table[0]))]
    total = sum(rows)
    return [[Fraction(r * c, total) for c in cols] for r in rows]


def anova(groups):
    """One-way ANOVA from the raw groups, by the definition (not by a
    shortcut): group means, SSB, SSW, SST, df, MS, F — all exact."""
    groups = [[Fraction(v) for v in g] for g in groups]
    k = len(groups)
    if k < 2 or any(len(g) < 2 for g in groups):
        raise ValueError("ANOVA needs at least two groups of two")
    n_total = sum(len(g) for g in groups)
    grand = sum((sum(g, Fraction(0)) for g in groups), Fraction(0)) / n_total
    means = [mean(g) for g in groups]
    ssb = sum(len(g) * (m - grand) ** 2 for g, m in zip(groups, means))
    ssw = sum(sum((v - m) ** 2 for v in g) for g, m in zip(groups, means))
    sst = sum(sum((v - grand) ** 2 for v in g) for g in groups)
    df_b, df_w = k - 1, n_total - k
    msb, msw = ssb / df_b, ssw / df_w
    return {
        "group_means": means, "grand_mean": grand,
        "ssb": ssb, "ssw": ssw, "sst": sst,
        "df": (df_b, df_w), "msb": msb, "msw": msw,
        "f": msb / msw if msw else None,
    }


# ---------------------------------------------------------------------------
# Study-design scenarios: keyword -> label (plans/statistics_plan.md §5, S5)
# ---------------------------------------------------------------------------

# Each cue phrase belongs to exactly one label, and every scenario template
# contains exactly one cue — the oracle inverts the scenario grammar instead
# of trusting the generator. Extend the banks as StudyDesignGenerator grows;
# ``cue_conflicts`` keeps them disjoint.
SAMPLING_CUES = {
    "numbered every": "SRS",
    "drew names from a hat": "SRS",
    "random number generator": "SRS",
    "from each grade": "stratified",
    "from each department": "stratified",
    "within every age group": "stratified",
    "every 5th": "systematic",
    "every 10th": "systematic",
    "every 20th": "systematic",
    "picked 4 whole classrooms": "cluster",
    "selected 3 entire neighborhoods": "cluster",
    "all members of the chosen teams": "cluster",
    "the first 30 people she met": "convenience",
    "whoever was already in the lobby": "convenience",
    "students in her own class": "convenience",
    "invited viewers to call in": "voluntary response",
    "posted an online poll": "voluntary response",
    "asked listeners to text": "voluntary response",
}

BIAS_CUES = {
    "only households with a landline": "undercoverage",
    "left out the night shift": "undercoverage",
    "only 12 of the 200 mailed forms came back": "nonresponse",
    "most people never replied": "nonresponse",
    "invited viewers to call in": "voluntary response",
    "asked listeners to text": "voluntary response",
    "the first 30 people she met": "convenience",
    "Do you agree that the unfair fee should be removed": "leading question",
    "Shouldn't the school do more": "leading question",
}

DESIGN_CUES = {
    "the researcher assigned": "experiment",
    "randomly assigned each plot": "experiment",
    "gave half the group": "experiment",
    "recorded what each shopper already": "observational",
    "observed without intervening": "observational",
    "compared existing records": "observational",
}

CUE_BANKS = {
    "sampling_method": SAMPLING_CUES,
    "bias": BIAS_CUES,
    "study_type": DESIGN_CUES,
}


def label_from_scenario(text, bank):
    """The label of the single cue phrase in ``text``; raises unless exactly
    one cue matches (the scenario grammar guarantees exactly one)."""
    hits = {label for cue, label in bank.items() if cue.lower() in text.lower()}
    if len(hits) != 1:
        raise ValueError(f"expected exactly one cue, matched {sorted(hits)}")
    return hits.pop()


def cue_conflicts(bank):
    """Cue phrases that are a substring of another cue with a different
    label — a scenario containing one would match two labels."""
    bad = []
    for cue, label in bank.items():
        for other, other_label in bank.items():
            if cue != other and label != other_label \
                    and cue.lower() in other.lower():
                bad.append((cue, other))
    return bad


# ---------------------------------------------------------------------------
# Fisher information from expected squared scores (S6)
# ---------------------------------------------------------------------------

def fisher_from_score(family, parameter):
    """Independent score-variance identities for the Phase 6 families.

    ``parameter`` is p for Bernoulli / geometric, lambda for Poisson /
    exponential, and known sigma-squared for ``normal_mu``. This deliberately
    does not use the generator's negative-expected-Hessian formulas.
    """
    parameter = Fraction(parameter)
    if family == "bernoulli":
        p = parameter
        score_one = 1 / p
        score_zero = -1 / (1 - p)
        return p * score_one ** 2 + (1 - p) * score_zero ** 2
    if family == "poisson":
        # score = (X-lambda)/lambda; Var(X) = lambda.
        return parameter / parameter ** 2
    if family == "exponential":
        # score = E[X] - X and Var(X) = 1/lambda^2.
        return 1 / parameter ** 2
    if family == "normal_mu":
        # score = (X-mu)/sigma^2; Var(X) = sigma^2.
        return parameter / parameter ** 2
    if family == "geometric":
        # Y=X-1 has Var(Y)=(1-p)/p^2; score is centered Y/(1-p).
        p = parameter
        return ((1 - p) / p ** 2) / (1 - p) ** 2
    raise ValueError(f"unknown Fisher family {family!r}")


def sufficient_statistic(family, data):
    """Independent family-to-statistic table for S6 factorization tests."""
    data = tuple(Fraction(value) for value in data)
    if family == "uniform":
        return max(data)
    if family == "normal_two":
        return (sum(data, Fraction(0)),
                sum((value ** 2 for value in data), Fraction(0)))
    if family in {"bernoulli", "poisson", "exponential", "geometric",
                  "normal_mu"}:
        return sum(data, Fraction(0))
    raise ValueError(f"unknown sufficient-statistic family {family!r}")
