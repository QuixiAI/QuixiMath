"""Shared infrastructure for the statistics strand (``plans/statistics_plan.md`` §4).

This module is the generator-side home of everything the statistics
generators share: the exact-rendering helpers (re-exported from
``prob_common``), the deviation-pattern library that makes means and
standard deviations exact by construction, the perfect-square standard-error
banks, the text renderings of every data display in ``plans/statistics_plan.md``
§3, and the small statistical routines (five-number summary, nearest rank)
whose rule is stated in the problem text.

Design rules this module encodes:

- **One rendering per display type, fixed forever.** Dot plots, fraction
  line plots and stem-and-leaf use ``∣`` (U+2223) and ``●``; box plots use a
  7-character prefix, ``+`` ticks every 5 units, one character per unit and
  the symbols ``* [ : ] = - o``; tallies use ``////\\`` for a group of five;
  histogram bins are inclusive integer ranges.
- **Pipe safety.** No rendering ever emits an ASCII ``|`` — that byte is the
  step delimiter and nothing else.
- **Exactness by construction, never by rounding.** ``patterns()`` supplies
  zero-sum integer deviations whose sum of squares divides to a perfect
  square, and the SE banks supply the (p, n) / (n1, n2) / (s, n) combinations
  whose standard errors are rational.

The oracle modules under ``tests/`` never import this file (A9: the oracle
must be an independent route).
"""
import math
import random
from collections import namedtuple
from fractions import Fraction
from functools import lru_cache

from helpers import step
from prob_common import (
    NP_BANK,
    dec,
    exact,
    is_perfect_square,
    money,
    p4,
    pct,
    phi,
    phi_table,
    sqrt_fraction,
    supplied_constant,
    terminates,
)

# ---------------------------------------------------------------------------
# Display characters (plans/statistics_plan.md §3 / §9 — fixed forever)
# ---------------------------------------------------------------------------

BAR = "∣"      # ∣ U+2223 DIVIDES — the display separator, never ASCII '|'
MARK = "●"     # ● — one observation on a dot plot / line plot
TALLY_FIVE = "////\\"  # a completed group of five


# ---------------------------------------------------------------------------
# Answer-shape helpers (plans/statistics_plan.md §3)
# ---------------------------------------------------------------------------


def num_txt(value):
    """Canonical number rendering for a statistic: integers plain,
    terminating decimals minimal, everything else a reduced fraction."""
    return exact(Fraction(value))


def text_list(pairs, sep="; "):
    """``key: value`` pairs joined with ``; `` — the text-list answer shape
    for anything table-shaped (``6: 2; 7: 0; 8: 4``). ``pairs`` may be a
    mapping (rendered in ascending key order) or an ordered sequence of
    pairs (rendered in the order given)."""
    if hasattr(pairs, "items"):
        pairs = sorted(pairs.items())
    return sep.join(f"{k}: {v}" for k, v in pairs)


def frac_label(value):
    """Fraction label in lowest terms, mixed when improper: ``1/4``, ``1``,
    ``1 1/4``, ``-3/4``."""
    fr = Fraction(value)
    sign = "-" if fr < 0 else ""
    fr = abs(fr)
    whole, rem = divmod(fr.numerator, fr.denominator)
    if rem == 0:
        return f"{sign}{whole}"
    if whole == 0:
        return f"{sign}{rem}/{fr.denominator}"
    return f"{sign}{whole} {rem}/{fr.denominator}"


def ordinal(k):
    """``80`` -> '80th', ``1`` -> '1st', ``97.5`` -> '97.5th'."""
    fr = Fraction(k)
    if fr.denominator != 1:
        return f"{num_txt(fr)}th"
    n = int(fr)
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


# The procedural rules that must be stated in the problem before they are
# applied (plans/statistics_plan.md §3 "Rule-dependent statistics"). Quote one with
# a RULE|name|statement step.
RULES = {
    "box plot": ("* = min/max, [ ] = Q1/Q3, : = median, o = outlier, "
                 "1 char per unit"),
    "quartiles": "Q1 and Q3 are the medians of the halves below and above "
                 "the median",
    "nearest rank": "position = ceil(k·n/100) in the sorted list",
    "percentile rank": "percent of values strictly below",
    "outliers": "outside Q1 - 1.5·IQR to Q3 + 1.5·IQR",
    "median class": "the first class whose cumulative frequency reaches n/2",
    "trimmed mean": "remove the lowest p% and the highest p%",
    "conservative df": "df = min(n1 - 1, n2 - 1)",
    "10% condition": "n ≤ N/10",
    "large counts": "np ≥ 10 and n(1 - p) ≥ 10",
    "68-95-99.7": "68% within 1 sd, 95% within 2 sd, 99.7% within 3 sd",
    "bootstrap interval": "nearest rank on the sorted list of statistics",
}


# ---------------------------------------------------------------------------
# The deviation-pattern library (plans/statistics_plan.md §3 "Exactness by
# construction")
# ---------------------------------------------------------------------------

MAX_PATTERN_ABS = 12  # enumeration guard; the plan's default is 8


def pattern_ss(pattern):
    """Σd² for a deviation pattern."""
    return sum(d * d for d in pattern)


@lru_cache(maxsize=None)
def _zero_sum_patterns(n, max_abs):
    """Every non-decreasing zero-sum integer tuple of length ``n`` with
    ``abs(d) <= max_abs``, excluding the all-zero tuple. Cached."""
    out = []
    prefix = []

    def rec(start, slots, total):
        if slots == 0:
            if total == 0 and any(prefix):
                out.append((tuple(prefix), pattern_ss(prefix)))
            return
        for v in range(start, max_abs + 1):
            if total + v * slots > 0:
                break                      # even all-``v`` overshoots
            if total + max_abs * slots < 0:
                continue                   # even all-max cannot reach 0
            prefix.append(v)
            rec(v, slots - 1, total + v)
            prefix.pop()

    rec(-max_abs, n, 0)
    return tuple(out)


@lru_cache(maxsize=None)
def patterns(n, *, pop_square=False, sample_square=False, ss=None, max_abs=8):
    """Cached zero-sum integer deviation patterns of length ``n``.

    Data built as ``mean + d_i`` from one of these patterns has exactly the
    stated mean. Filters:

    - ``pop_square``   — ``SS/n`` is the square of a rational (population
      standard deviation is exact).
    - ``sample_square`` — ``SS/(n - 1)`` is the square of a rational (sample
      standard deviation is exact), e.g. ``(-3, 1, 1, 1)`` for n = 4
      (SS 12 -> s = 2) or ``(-3, -3, 1, 1, 4)`` for n = 5 (SS 36 -> s = 3).
    - ``ss``           — keep only patterns with exactly this Σd² (used for
      the Sxx banks of ``SlopeInferenceGenerator``).

    Patterns come back in canonical non-decreasing order; use
    ``sample_from_pattern`` to shuffle them into a data set. Returns a tuple,
    so the result is safe to cache and to index randomly.
    """
    if not 3 <= n <= 8:
        raise ValueError(f"pattern length must be 3..8, got {n}")
    if not 1 <= max_abs <= MAX_PATTERN_ABS:
        raise ValueError(f"max_abs must be 1..{MAX_PATTERN_ABS}, got {max_abs}")
    if ss is not None and ss < 0:
        raise ValueError("ss must be non-negative")
    out = []
    for pat, s in _zero_sum_patterns(n, max_abs):
        if ss is not None and s != ss:
            continue
        if pop_square and not is_perfect_square(Fraction(s, n)):
            continue
        if sample_square and not is_perfect_square(Fraction(s, n - 1)):
            continue
        out.append(pat)
    return tuple(out)


def sample_from_pattern(mean, pattern, shuffle=True):
    """``mean + d`` for each deviation, shuffled by default.

    ``mean`` may be an int (data come back as ints) or a Fraction / decimal
    string (data come back as Fractions), so a mean of 12.5 is as easy as a
    mean of 12."""
    if isinstance(mean, int):
        data = [mean + d for d in pattern]
    else:
        m = Fraction(mean)
        data = [m + d for d in pattern]
    if shuffle:
        random.shuffle(data)
    return data


# ---------------------------------------------------------------------------
# Perfect-square standard-error banks (plans/statistics_plan.md §3)
# ---------------------------------------------------------------------------

# (p, n, SE) with p(1 - p)/n a perfect-square rational: SE = √(p(1-p)/n).
PROP_SE_BANK = (
    (Fraction(1, 2), 100, Fraction(1, 20)),
    (Fraction(1, 5), 400, Fraction(1, 50)),
    (Fraction(1, 10), 900, Fraction(1, 100)),
    (Fraction(2, 5), 600, Fraction(1, 50)),
    (Fraction(1, 2), 400, Fraction(1, 40)),
    (Fraction(1, 2), 2500, Fraction(1, 100)),
    (Fraction(1, 5), 1600, Fraction(1, 100)),
    (Fraction(4, 5), 1600, Fraction(1, 100)),
    (Fraction(9, 10), 900, Fraction(1, 100)),
    (Fraction(3, 5), 600, Fraction(1, 50)),
)

# (n1, n2, 1/n1 + 1/n2) with the sum a perfect-square rational.
N_PAIR_BANK = (
    (8, 8, Fraction(1, 4)),
    (18, 18, Fraction(1, 9)),
    (50, 50, Fraction(1, 25)),
    (5, 20, Fraction(1, 4)),
    (20, 80, Fraction(1, 16)),
    (10, 90, Fraction(1, 9)),
    (32, 32, Fraction(1, 16)),
    (72, 72, Fraction(1, 36)),
    (6, 12, Fraction(1, 4)),
    (45, 180, Fraction(1, 36)),
)

# (s1, n1, s2, n2, s1²/n1 + s2²/n2) with the sum a perfect square.
TWO_SAMPLE_SE_BANK = (
    (12, 9, 6, 4, 25),
    (15, 25, 16, 16, 25),
    (18, 36, 12, 9, 25),
    (20, 25, 9, 9, 25),
    (4, 4, 12, 12, 16),
    (4, 16, 15, 15, 16),
    (3, 9, 12, 6, 25),
    (4, 4, 24, 18, 36),
)

# (s1, s2, pooled s) with (s1² + s2²)/2 a perfect square — pooled variance
# with n1 = n2. Unequal n uses s1 = s2 instead.
POOLED_S_PAIRS = (
    (1, 7, 5),
    (5, 5, 5),
    (7, 17, 13),
    (7, 23, 17),
    (2, 14, 10),
)

# ((p1, n1), (p2, n2), SE) with p1q1/n1 + p2q2/n2 a perfect-square rational —
# the difference-of-proportions interval (plans/statistics_plan.md §5,
# ConfidenceIntervalGenerator ⟲ diff_props_ci).
DIFF_PROP_SE_BANK = (
    ((Fraction(1, 2), 200), (Fraction(1, 2), 200), Fraction(1, 20)),
    ((Fraction(1, 5), 800), (Fraction(1, 5), 800), Fraction(1, 50)),
    ((Fraction(1, 2), 800), (Fraction(1, 2), 800), Fraction(1, 40)),
    ((Fraction(1, 10), 1800), (Fraction(1, 10), 1800), Fraction(1, 100)),
    ((Fraction(3, 5), 1200), (Fraction(3, 5), 1200), Fraction(1, 50)),
    ((Fraction(1, 10), 25), (Fraction(1, 5), 25), Fraction(1, 10)),
    ((Fraction(1, 10), 25), (Fraction(3, 10), 75), Fraction(2, 25)),
    ((Fraction(1, 10), 25), (Fraction(1, 2), 400), Fraction(13, 200)),
    ((Fraction(1, 10), 25), (Fraction(7, 10), 75), Fraction(2, 25)),
    ((Fraction(1, 10), 25), (Fraction(4, 5), 25), Fraction(1, 10)),
    ((Fraction(1, 10), 50), (Fraction(9, 10), 50), Fraction(3, 50)),
    ((Fraction(1, 5), 50), (Fraction(3, 10), 525), Fraction(3, 50)),
    ((Fraction(1, 5), 50), (Fraction(2, 5), 75), Fraction(2, 25)),
    ((Fraction(3, 10), 25), (Fraction(2, 5), 150), Fraction(1, 10)),
    ((Fraction(3, 10), 50), (Fraction(7, 10), 300), Fraction(7, 100)),
)


def prop_se(p, n):
    """Exact √(p(1 - p)/n); raises when it is not rational."""
    return sqrt_fraction(Fraction(p) * (1 - Fraction(p)) / n)


def search_prop_se(n_max=2500, ps=None, se_max=Fraction(1, 10)):
    """Build-time search that verifies / extends ``PROP_SE_BANK``: every
    ``(p, n, SE)`` with ``p(1 - p)/n`` a perfect-square rational, ``p`` a
    tenth or a twentieth, and ``SE`` at most ``se_max``."""
    if ps is None:
        ps = [Fraction(k, 10) for k in range(1, 10)]
        ps += [Fraction(k, 20) for k in range(1, 20, 2)]
    found = []
    for p in sorted(set(Fraction(x) for x in ps)):
        pq = p * (1 - p)
        for n in range(2, n_max + 1):
            v = pq / n
            if is_perfect_square(v):
                se = sqrt_fraction(v)
                if 0 < se <= se_max and terminates(se):
                    found.append((p, n, se))
    return found


def search_n_pair_se(n_max=200):
    """``(n1, n2, 1/n1 + 1/n2)`` with the sum a perfect-square rational."""
    found = []
    for n1 in range(2, n_max + 1):
        for n2 in range(n1, n_max + 1):
            v = Fraction(1, n1) + Fraction(1, n2)
            if is_perfect_square(v):
                found.append((n1, n2, v))
    return found


def search_two_sample_se(s_max=25, n_max=100):
    """``(s1, n1, s2, n2, s1²/n1 + s2²/n2)`` with each term an integer and
    the sum a perfect square, so ``√(s1²/n1 + s2²/n2)`` is an integer."""
    terms = []
    for s in range(1, s_max + 1):
        for n in range(2, n_max + 1):
            if s * s % n == 0:
                terms.append((s, n, s * s // n))
    found = []
    for i, (s1, n1, v1) in enumerate(terms):
        for s2, n2, v2 in terms[i:]:
            total = v1 + v2
            if math.isqrt(total) ** 2 == total:
                found.append((s1, n1, s2, n2, total))
                # A bank may deliberately put either sample first.  Return
                # both orders so the search really verifies every banked row
                # instead of depending on the implementation's loop order.
                if (s1, n1) != (s2, n2):
                    found.append((s2, n2, s1, n1, total))
    return found


def search_pooled_pairs(s_max=30):
    """``(s1, s2, pooled s)`` with ``(s1² + s2²)/2`` a perfect square."""
    found = []
    for s1 in range(1, s_max + 1):
        for s2 in range(s1, s_max + 1):
            v = Fraction(s1 * s1 + s2 * s2, 2)
            if v.denominator == 1 and is_perfect_square(v):
                found.append((s1, s2, int(sqrt_fraction(v))))
    return found


def search_diff_prop_se(n_max=2500, ps=None, step_n=25,
                        se_max=Fraction(1, 10)):
    """``((p1, n1), (p2, n2), SE)`` with ``p1q1/n1 + p2q2/n2`` a
    perfect-square rational — the build-time table search the plan calls for
    (n ≤ 2500)."""
    if ps is None:
        ps = [Fraction(k, 10) for k in range(1, 10)]
    ns = list(range(step_n, n_max + 1, step_n))
    cells = [(p, n, Fraction(p) * (1 - Fraction(p)) / n)
             for p in sorted(set(Fraction(x) for x in ps)) for n in ns]
    found = []
    for i, (p1, n1, v1) in enumerate(cells):
        for p2, n2, v2 in cells[i:]:
            total = v1 + v2
            if is_perfect_square(total):
                se = sqrt_fraction(total)
                if 0 < se <= se_max and terminates(se):
                    found.append(((p1, n1), (p2, n2), se))
    return found


def verify_se_tables():
    """Recomputes every banked standard error from its definition. Raises
    ``ValueError`` on the first row that does not hold; returns True."""
    for p, n, se in PROP_SE_BANK:
        if sqrt_fraction(Fraction(p) * (1 - Fraction(p)) / n) != se:
            raise ValueError(f"PROP_SE_BANK bad row: {(p, n, se)}")
    for n1, n2, v in N_PAIR_BANK:
        if Fraction(1, n1) + Fraction(1, n2) != v or not is_perfect_square(v):
            raise ValueError(f"N_PAIR_BANK bad row: {(n1, n2, v)}")
    for s1, n1, s2, n2, v in TWO_SAMPLE_SE_BANK:
        got = Fraction(s1 * s1, n1) + Fraction(s2 * s2, n2)
        if got != v or not is_perfect_square(got):
            raise ValueError(f"TWO_SAMPLE_SE_BANK bad row: {(s1, n1, s2, n2)}")
    for s1, s2, sp in POOLED_S_PAIRS:
        got = Fraction(s1 * s1 + s2 * s2, 2)
        if got != sp * sp:
            raise ValueError(f"POOLED_S_PAIRS bad row: {(s1, s2, sp)}")
    for (p1, n1), (p2, n2), se in DIFF_PROP_SE_BANK:
        got = (Fraction(p1) * (1 - Fraction(p1)) / n1
               + Fraction(p2) * (1 - Fraction(p2)) / n2)
        if not is_perfect_square(got) or sqrt_fraction(got) != se:
            raise ValueError(f"DIFF_PROP_SE_BANK bad row: {((p1, n1), (p2, n2))}")
    return True


# ---------------------------------------------------------------------------
# Display renderings (plans/statistics_plan.md §3) — every one is parsed back by
# ``tests/stats_oracle.py``.
# ---------------------------------------------------------------------------


def _as_counts(data):
    """A ``{value: count}`` dict from either raw data or a count mapping."""
    if hasattr(data, "items"):
        counts = {k: int(v) for k, v in data.items()}
    else:
        counts = {}
        for v in data:
            counts[v] = counts.get(v, 0) + 1
    if not counts:
        raise ValueError("no data to display")
    if any(c < 0 for c in counts.values()):
        raise ValueError("counts must be non-negative")
    return counts


def _plot_rows(labels, counts, title=None, mark=MARK):
    width = max(len(lab) for lab in labels)
    lines = [title] if title else []
    for lab, c in zip(labels, counts):
        marks = " ".join([mark] * c)
        lines.append(f"{lab.rjust(width)} {BAR} {marks}".rstrip())
    return "\n".join(lines)


def render_dot_plot(data, title=None, mark=MARK):
    """Dot plot: one row per integer from min to max **including empty
    rows**, the value right-aligned, then ``∣``, then ``●`` marks separated
    by single spaces.

    ```
    Dot plot of quiz scores (each ● is one student):
     6 ∣ ● ●
     7 ∣
     8 ∣ ● ● ● ●
    ```
    """
    counts = _as_counts(data)
    keys = sorted(counts)
    if any(int(k) != k for k in keys):
        raise ValueError("dot plot values must be integers")
    values = list(range(int(keys[0]), int(keys[-1]) + 1))
    labels = [str(v) for v in values]
    return _plot_rows(labels, [counts.get(v, 0) for v in values], title, mark)


def render_line_plot(data, unit, title=None, mark=MARK):
    """Fraction line plot: the dot-plot layout with fraction labels in
    lowest terms (``1/4``, ``1/2``, ``3/4``, ``1``, ``1 1/4``) and a row at
    every multiple of ``unit`` from the smallest to the largest value."""
    unit = Fraction(unit)
    if unit <= 0:
        raise ValueError("unit must be positive")
    counts = _as_counts([Fraction(v) for v in data] if not hasattr(data, "items")
                        else {Fraction(k): v for k, v in data.items()})
    keys = sorted(counts)
    for k in keys:
        if (k / unit).denominator != 1:
            raise ValueError(f"{frac_label(k)} is not a multiple of the unit")
    lo, hi = keys[0], keys[-1]
    rows = int((hi - lo) / unit) + 1
    values = [lo + i * unit for i in range(rows)]
    labels = [frac_label(v) for v in values]
    return _plot_rows(labels, [counts.get(v, 0) for v in values], title, mark)


def tally_marks(count):
    """``7`` -> ``////\\ //`` — completed groups of five, then the leftovers."""
    if count < 0:
        raise ValueError("count must be non-negative")
    groups = [TALLY_FIVE] * (count // 5)
    if count % 5:
        groups.append("/" * (count % 5))
    return " ".join(groups)


def render_tally(counts, title=None):
    """Tally table, one row per category in alphabetical order:
    ``Red: ////\\ //``."""
    items = counts.items() if hasattr(counts, "items") else counts
    lines = [title] if title else []
    for cat, c in sorted(items):
        if ":" in str(cat):
            raise ValueError(f"category {cat!r} may not contain ':'")
        lines.append(f"{cat}: {tally_marks(int(c))}".rstrip())
    return "\n".join(lines)


def _stem_leaf(value, decimal):
    if decimal:
        fr = Fraction(value)
        scaled = fr * 10
        if scaled.denominator != 1:
            raise ValueError(f"{value} needs exactly one decimal place")
        n = int(scaled)
    else:
        fr = Fraction(value)
        if fr.denominator != 1:
            raise ValueError(f"{value} is not an integer")
        n = int(fr)
    if n < 0:
        raise ValueError("stem-and-leaf values must be non-negative")
    return divmod(n, 10)


def stem_leaf_value(stem, leaf, decimal=False):
    """The value a ``stem ∣ leaf`` cell stands for."""
    return (Fraction(stem) + Fraction(leaf, 10) if decimal
            else Fraction(stem * 10 + leaf))


def render_stem_leaf(values, decimal=False, key=None, title=None):
    """Stem-and-leaf plot with the header, **every** stem from lowest to
    highest (empty stems kept), ascending space-separated leaves, and a key
    line that is always present.

    ```
    Stem ∣ Leaves
       1 ∣ 2 5 7
       2 ∣ 0 3 3
       3 ∣
       4 ∣ 1
    Key: 2 ∣ 3 means 23
    ```

    ``decimal=True`` splits x.y data instead (``Key: 2 ∣ 3 means 2.3``).
    ``key`` overrides the (stem, leaf) pair the key line quotes; by default
    the first leaf of the first non-empty stem."""
    pairs = sorted(_stem_leaf(v, decimal) for v in values)
    if not pairs:
        raise ValueError("no data to display")
    stems = list(range(pairs[0][0], pairs[-1][0] + 1))
    leaves = {s: [] for s in stems}
    for s, leaf in pairs:
        leaves[s].append(leaf)
    width = max(4, max(len(str(s)) for s in stems))
    lines = [title] if title else []
    lines.append(f"{'Stem'.rjust(width)} {BAR} Leaves")
    for s in stems:
        row = " ".join(str(x) for x in leaves[s])
        lines.append(f"{str(s).rjust(width)} {BAR} {row}".rstrip())
    k_stem, k_leaf = key if key is not None else pairs[0]
    shown = num_txt(stem_leaf_value(k_stem, k_leaf, decimal))
    if decimal and "." not in shown:
        shown = f"{shown}.0"
    lines.append(f"Key: {k_stem} {BAR} {k_leaf} means {shown}")
    return "\n".join(lines)


def stem_leaf_list(values, decimal=False):
    """The text-list answer form of a stem-and-leaf plot:
    ``1: 2 5 7; 2: 0 3 3; 3: none; 4: 1``."""
    pairs = sorted(_stem_leaf(v, decimal) for v in values)
    stems = list(range(pairs[0][0], pairs[-1][0] + 1))
    rows = {s: [] for s in stems}
    for s, leaf in pairs:
        rows[s].append(leaf)
    return text_list([(s, " ".join(str(x) for x in rows[s]) or "none")
                      for s in stems])


BOX_PREFIX = 7  # "Scale: ", "Plot:  ", "Plot A:" are all 7 characters


def box_scale(values, start=None, end=None):
    """The (start, end) of a box-plot scale: the largest multiple of 5 at or
    below the smallest drawn value, the smallest multiple of 5 strictly
    above the largest (so the last tick is always past the data, as in the
    plan's illustration), at most 41 columns wide."""
    lo, hi = min(values), max(values)
    if start is None:
        start = (lo // 5) * 5
    if end is None:
        end = (hi // 5) * 5 + 5
        if end <= start:
            end = start + 5
    if start % 5 or end % 5:
        raise ValueError("box-plot scale ends must be multiples of 5")
    if start > lo or end < hi:
        raise ValueError("box-plot scale does not cover the data")
    if end - start > 40:
        raise ValueError("box-plot scale wider than 40 units")
    if max(len(str(start)), len(str(end))) > 4:
        raise ValueError("box-plot tick labels must be at most 4 characters")
    return start, end


def _box_line(label, summary, outliers, start, end):
    mn, q1, med, q3, mx = [int(v) for v in summary]
    if not (mn < q1 < med < q3 < mx):
        raise ValueError(f"box plot needs min < Q1 < median < Q3 < max: {summary}")
    cells = [" "] * (end - start + 1)
    for v in range(mn + 1, q1):
        cells[v - start] = "-"
    for v in range(q3 + 1, mx):
        cells[v - start] = "-"
    for v in range(q1 + 1, q3):
        cells[v - start] = "="
    cells[med - start] = ":"
    cells[q1 - start] = "["
    cells[q3 - start] = "]"
    cells[mn - start] = "*"
    cells[mx - start] = "*"
    for o in outliers:
        o = int(o)
        if mn <= o <= mx:
            raise ValueError(f"outlier {o} is inside the whiskers")
        cells[o - start] = "o"
    prefix = f"{label}:".ljust(BOX_PREFIX)
    if len(prefix) != BOX_PREFIX:
        raise ValueError(f"box-plot label {label!r} is too long")
    return (prefix + "".join(cells)).rstrip()


def render_box_plots(items, scale=None):
    """Two or more box plots stacked under one scale. ``items`` is a
    sequence of ``(label, summary)`` or ``(label, summary, outliers)``."""
    rows = [(it[0], it[1], it[2] if len(it) > 2 else ()) for it in items]
    drawn = [v for _, summary, outs in rows
             for v in list(summary) + list(outs)]
    start, end = box_scale(drawn, *(scale if scale else (None, None)))
    ticks = list(range(start, end + 1, 5))
    scale_line = ("Scale: " + "".join(str(t).ljust(5) for t in ticks)).rstrip()
    tick_line = " " * BOX_PREFIX + "+" + "----+" * (len(ticks) - 1)
    lines = [scale_line, tick_line]
    for label, summary, outs in rows:
        lines.append(_box_line(label, summary, outs, start, end))
    return "\n".join(lines)


def render_box_plot(summary, outliers=(), label="Plot", scale=None):
    """One box plot: the scale line, the ``+`` tick line, and the plot line.

    ```
    Scale: 0    5    10   15   20
           +----+----+----+----+
    Plot:     *-[==:===]--*
    ```
    (min 3, Q1 5, median 8, Q3 12, max 15). ``*`` marks the whisker ends,
    ``[`` / ``]`` the quartiles, ``:`` the median, ``=`` the inside of the
    box, ``-`` the whiskers and ``o`` each outlier — one character per unit,
    ticks every 5 units."""
    return render_box_plots([(label, summary, outliers)], scale=scale)


def render_two_way(row_labels, col_labels, cells, totals=False, corner="",
                   missing="?", row_totals=None, col_totals=None,
                   grand_total=None):
    """Space-aligned two-way table with an optional ``Total`` row and column.

    ```
               Yes   No   Total
    Grade 9     12    8      20
    Grade 10    15   15      30
    Total       27   23      50
    ```

    A ``None`` cell renders as ``missing`` (the fill-in-the-cell variant);
    supply ``row_totals`` / ``col_totals`` / ``grand_total`` when the margins
    cannot be summed because of it."""
    rows = [list(r) for r in cells]
    if len(rows) != len(row_labels) or any(len(r) != len(col_labels) for r in rows):
        raise ValueError("cells must be len(row_labels) x len(col_labels)")
    headers = list(col_labels)
    body = [[missing if v is None else str(v) for v in r] for r in rows]
    labels = list(row_labels)
    if totals:
        if row_totals is None:
            row_totals = [sum(r) for r in rows]
        if col_totals is None:
            col_totals = [sum(r[j] for r in rows) for j in range(len(headers))]
        if grand_total is None:
            grand_total = sum(col_totals)
        headers.append("Total")
        for r, t in zip(body, row_totals):
            r.append(str(t))
        labels.append("Total")
        body.append([str(t) for t in col_totals] + [str(grand_total)])
    label_w = max([len(corner)] + [len(str(x)) for x in labels])
    widths = [max(len(str(h)), max(len(r[j]) for r in body))
              for j, h in enumerate(headers)]
    lines = [str(corner).ljust(label_w)
             + "".join(str(h).rjust(w + 3) for h, w in zip(headers, widths))]
    for lab, row in zip(labels, body):
        lines.append(str(lab).ljust(label_w)
                     + "".join(v.rjust(w + 3) for v, w in zip(row, widths)))
    return "\n".join(line.rstrip() for line in lines)


def bin_label(lo, width):
    """Inclusive integer bin label: ``bin_label(10, 10)`` -> '10-19'."""
    return f"{lo}-{lo + width - 1}"


def bin_counts(values, width, start=0):
    """Ordered ``[(label, count)]`` over inclusive integer bins of ``width``
    from ``start``, with every bin between the first and last kept."""
    if width <= 0 or width % 5:
        raise ValueError("bin width must be a positive multiple of 5")
    vals = [int(v) for v in values]
    if min(vals) < start:
        raise ValueError("a value falls below the first bin")
    idx = [(v - start) // width for v in vals]
    out = []
    for i in range(min(idx), max(idx) + 1):
        out.append((bin_label(start + i * width, width), idx.count(i)))
    return out


def render_bins(bins, sep="; "):
    """Histogram bins as a text list: ``0-9: 3; 10-19: 5``. Pass
    ``sep=', '`` for the in-prose form the frequency tables use."""
    return text_list(bins if not hasattr(bins, "items") else list(bins.items()),
                     sep=sep)


# Percentile -> z, the inverse-normal table supplied inline
# (plans/statistics_plan.md §3 "Other supplied constants").
INVERSE_Z = {
    80: "0.84", 90: "1.28", 95: "1.645", 97.5: "1.96", 99: "2.33",
}
# Percentiles whose z has a terminating reciprocal, for the variants that
# divide by z (InverseNormalGenerator.sigma_from_cutoff).
INVERSE_Z_DIVIDABLE = {
    78.8: "0.8", 89.4: "1.25", 90: "1.28", 94.5: "1.6", 99.4: "2.5",
}


def inverse_z_table(percentiles, decoys=1, table=None):
    """The inline inverse-normal excerpt, with decoy rows:

    ``Selected z-scores: 80th percentile z = 0.84; 90th z = 1.28;
    95th z = 1.645; 97.5th z = 1.96; 99th z = 2.33``

    Only the first row spells out "percentile". Decoys are the unused rows
    of ``table`` nearest the requested ones, so the excerpt never advertises
    which row the procedure needs."""
    table = dict(INVERSE_Z if table is None else table)
    need = sorted({float(p) for p in percentiles})
    for p in need:
        if p not in {float(k) for k in table}:
            raise ValueError(f"no z tabulated for the {ordinal(p)} percentile")
    unused = sorted(k for k in table if float(k) not in need)
    unused.sort(key=lambda k: (min(abs(float(k) - p) for p in need), float(k)))
    rows = sorted(set(need) | {float(k) for k in unused[:max(0, decoys)]})
    lookup = {float(k): v for k, v in table.items()}
    cells = []
    for i, p in enumerate(rows):
        label = ordinal(Fraction(str(p)) if p % 1 else int(p))
        word = "percentile z" if i == 0 else "z"
        cells.append(f"{label} {word} = {lookup[p]}")
    return "Selected z-scores: " + "; ".join(cells)


def critical_value(label, value, df=None):
    """Inline supplied critical value: ``z* = 1.96``,
    ``t* = 2.262 (df = 9)``, ``χ² critical value = 5.991 (df = 2)``,
    ``F critical value = 4.26 (df 2, 9)``."""
    text = f"{label} = {value}"
    if df is None:
        return text
    if isinstance(df, (tuple, list)):
        return f"{text} (df {df[0]}, {df[1]})"
    return f"{text} (df = {df})"


# ---------------------------------------------------------------------------
# Small statistical routines whose rule is stated in the problem
# ---------------------------------------------------------------------------

# Sizes whose halves have odd length, so both quartiles are actual data
# points (median-exclusive halves) — from FiveNumberSummaryGenerator.
SUMMARY_SIZES = [7, 10, 11, 14, 15]


def five_summary(data, halves=False):
    """``(min, Q1, median, Q3, max)`` by the median-exclusive-halves rule
    already used by ``FiveNumberSummaryGenerator``: the median splits the
    sorted data (and is excluded from both halves when n is odd), and each
    quartile is that half's median. With ``halves=True`` the two halves come
    back as well. The median is a ``Fraction``; the quartiles are data points
    when ``len(data)`` is one of ``SUMMARY_SIZES``."""
    s = sorted(Fraction(v) for v in data)
    n = len(s)
    if n < 4:
        raise ValueError("a five-number summary needs at least 4 values")
    if n % 2:
        med = s[n // 2]
        lo_half, hi_half = s[:n // 2], s[n // 2 + 1:]
    else:
        med = Fraction(s[n // 2 - 1] + s[n // 2], 2)
        lo_half, hi_half = s[:n // 2], s[n // 2:]
    q1 = _half_median(lo_half)
    q3 = _half_median(hi_half)
    out = (s[0], q1, med, q3, s[-1])
    return out + (lo_half, hi_half) if halves else out


def _half_median(half):
    m = len(half)
    if m % 2:
        return half[m // 2]
    return Fraction(half[m // 2 - 1] + half[m // 2], 2)


def iqr(data):
    """Q3 - Q1 under the same rule."""
    _, q1, _, q3, _ = five_summary(data)
    return q3 - q1


def outlier_fences(data):
    """``(Q1 - 1.5·IQR, Q3 + 1.5·IQR)`` — the 1.5×IQR rule."""
    _, q1, _, q3, _ = five_summary(data)
    spread = Fraction(3, 2) * (q3 - q1)
    return q1 - spread, q3 + spread


def nearest_rank_position(n, k):
    """``ceil(k·n/100)`` — the nearest-rank position, clamped to 1..n."""
    pos = Fraction(k) * n / 100
    pos = -((-pos.numerator) // pos.denominator)
    return max(1, min(int(pos), n))


def nearest_rank(sorted_values, k):
    """The ``k``-th percentile by the nearest-rank rule: the value at
    position ``ceil(k·n/100)`` of the sorted list (1-indexed)."""
    values = list(sorted_values)
    if values != sorted(values):
        raise ValueError("nearest_rank expects sorted values")
    return values[nearest_rank_position(len(values), k) - 1]


def percentile_rank(sorted_values, value):
    """Percent of values strictly below ``value``, as a Fraction of 100."""
    values = list(sorted_values)
    below = sum(1 for v in values if v < value)
    return Fraction(100 * below, len(values))


# ---------------------------------------------------------------------------
# Context bank (plans/statistics_plan.md §3 "Phrasing")
# ---------------------------------------------------------------------------

Context = namedtuple("Context", "key label unit unit_one item lo hi")

CONTEXTS = (
    Context("quiz_scores", "quiz scores", "points", "point", "student", 5, 20),
    Context("plant_heights", "plant heights", "cm", "cm", "plant", 8, 40),
    Context("commute_times", "commute times", "minutes", "minute",
            "commuter", 15, 60),
    Context("battery_life", "battery lifetimes", "hours", "hour",
            "battery", 6, 40),
    Context("package_weights", "package weights", "grams", "gram",
            "package", 200, 600),
    Context("daily_sales", "daily sales", "items", "item", "day", 20, 90),
    Context("rainfall", "daily rainfall", "mm", "mm", "day", 2, 30),
    Context("ages", "ages", "years", "year", "member", 8, 60),
    Context("shoe_sizes", "shoe sizes", "", "", "customer", 5, 13),
    Context("points_per_game", "points per game", "points", "point",
            "game", 4, 30),
    Context("reading_minutes", "reading minutes", "minutes", "minute",
            "reader", 10, 60),
    Context("pencil_lengths", "pencil lengths", "inches", "inch",
            "pencil", 2, 8),
)

CONTEXTS_BY_KEY = {c.key: c for c in CONTEXTS}


def context(key=None):
    """One entry of the context bank — a named one, or a random one."""
    if key is None:
        return random.choice(CONTEXTS)
    return CONTEXTS_BY_KEY[key]


def with_unit(text, ctx, singular=False):
    """``with_unit(12, ctx)`` -> '12 minutes'; unitless contexts return the
    number alone."""
    unit = ctx.unit_one if singular else ctx.unit
    return f"{text} {unit}" if unit else str(text)


# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------


def running_sum_steps(values, op="A"):
    """The ``A`` chain four statistics generators write by hand:
    ``A|12|15|27``, ``A|27|17|44``, … Returns ``(steps, total)``; a
    one-element list produces no steps."""
    vals = [Fraction(v) for v in values]
    if not vals:
        return [], Fraction(0)
    steps = []
    run = vals[0]
    for v in vals[1:]:
        steps.append(step(op, num_txt(run), num_txt(v), num_txt(run + v)))
        run += v
    return steps, run


def dev_rows(data, mean, op="DEV_ROW"):
    """One ``DEV_ROW|x|x - mean|(x - mean)^2`` per value, plus Σd²."""
    m = Fraction(mean)
    steps, ss = [], Fraction(0)
    for v in data:
        d = Fraction(v) - m
        steps.append(step(op, num_txt(v), num_txt(d), num_txt(d * d)))
        ss += d * d
    return steps, ss


__all__ = [
    # re-exported numerics (prob_common owns them)
    "dec", "exact", "terminates", "p4", "pct", "money", "phi", "phi_table",
    "supplied_constant", "NP_BANK", "is_perfect_square", "sqrt_fraction",
    # answer shapes
    "num_txt", "text_list", "frac_label", "ordinal", "RULES",
    # pattern library
    "patterns", "pattern_ss", "sample_from_pattern", "MAX_PATTERN_ABS",
    # standard-error banks
    "PROP_SE_BANK", "N_PAIR_BANK", "TWO_SAMPLE_SE_BANK", "POOLED_S_PAIRS",
    "DIFF_PROP_SE_BANK", "prop_se", "search_prop_se", "search_n_pair_se",
    "search_two_sample_se", "search_pooled_pairs", "search_diff_prop_se",
    "verify_se_tables",
    # renderings
    "BAR", "MARK", "TALLY_FIVE", "BOX_PREFIX",
    "render_dot_plot", "render_line_plot", "render_tally", "tally_marks",
    "render_stem_leaf", "stem_leaf_list", "stem_leaf_value",
    "render_box_plot", "render_box_plots", "box_scale", "render_two_way",
    "render_bins", "bin_label", "bin_counts",
    "INVERSE_Z", "INVERSE_Z_DIVIDABLE", "inverse_z_table", "critical_value",
    # statistics
    "SUMMARY_SIZES", "five_summary", "iqr", "outlier_fences",
    "nearest_rank", "nearest_rank_position", "percentile_rank",
    # contexts and steps
    "Context", "CONTEXTS", "CONTEXTS_BY_KEY", "context", "with_unit",
    "running_sum_steps", "dev_rows",
]
