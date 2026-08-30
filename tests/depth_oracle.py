"""Independent verification routes for the depth strand.

Never imports ``depth_common`` — every function here re-derives its result
by a different route than the generators use (closed forms instead of
iteration, Brent instead of Floyd), so a generator agreeing with this
module is genuine verification, not self-agreement (A9).
"""
import os
import re
import sys
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from helpers import DELIM  # noqa: E402


# ---------------------------------------------------------------------------
# Closed forms (vs the generators' term-by-term iteration)
# ---------------------------------------------------------------------------

def affine_orbit_value(a, b, m, x0, n):
    """``x_n`` for ``x -> (a*x + b) mod m`` via the closed form.

    ``x_n = a^n x0 + b (a^n - 1)/(a - 1)`` computed exactly over the
    integers before the final reduction (no modular division needed), so
    it never touches the generator's iteration loop.
    """
    if a == 1:
        return (x0 + n * b) % m
    an = pow(a, n)  # exact big-int power, not mod — divide first, then reduce
    geometric = (an - 1) // (a - 1)
    return (an * x0 + b * geometric) % m


def geometric_partial_sum(a, r, n):
    """``a + a r + ... + a r^(n-1)`` exactly, by the closed form."""
    a, r = Fraction(a), Fraction(r)
    if r == 1:
        return a * n
    return a * (1 - r ** n) / (1 - r)


def brent_cycle(f, x0, limit=100_000):
    """Brent's algorithm: ``(mu, lam)`` — independent of Floyd."""
    power = lam = 1
    tortoise, hare = x0, f(x0)
    steps_taken = 0
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1
        steps_taken += 1
        if steps_taken > limit:
            raise ValueError("no cycle within limit")
    tortoise = hare = x0
    for _ in range(lam):
        hare = f(hare)
    mu = 0
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    return mu, lam


# ---------------------------------------------------------------------------
# Trace-structure measurement (used by the conventions test and by
# per-class tests that assert their traces really chain)
# ---------------------------------------------------------------------------

#: Steps that interleave with a chain without breaking measured depth.
NON_CHAIN_OPS = {"MILESTONE", "Z", "CHECK"}


def chain_depth(steps):
    """Length of the longest serial dependency run in a trace.

    Two consecutive non-``NON_CHAIN_OPS`` steps are linked when the later
    step's first payload field string-equals the earlier step's last
    field.  ``MILESTONE``/``CHECK``/``Z`` rows are skipped, not breaks.
    """
    best = current = 0
    previous_result = None
    for raw in steps:
        fields = raw.split(DELIM)
        op = fields[0]
        if op in NON_CHAIN_OPS:
            continue
        if len(fields) < 3:
            previous_result = fields[-1] if len(fields) > 1 else None
            current = 0
            continue
        if previous_result is not None and fields[1] == previous_result:
            current += 1
        else:
            current = 1
        best = max(best, current)
        previous_result = fields[-1]
    return best


def milestone_violations(steps):
    """Structural problems with a trace's MILESTONE rows.

    Checks shape (``MILESTONE|k|<desc>|<value>``), strictly increasing
    integer positions, and spacing between consecutive milestones within
    5..25 chain steps.  Value *correctness* is per-class (the invariant's
    semantics live there); this is the shared shape check.
    """
    bad = []
    positions = []
    chain_steps_seen = 0
    last_position = None
    for raw in steps:
        fields = raw.split(DELIM)
        if fields[0] != "MILESTONE":
            if fields[0] not in NON_CHAIN_OPS:
                chain_steps_seen += 1
            continue
        if len(fields) != 4:
            bad.append(f"milestone needs 3 payload fields: {raw}")
            continue
        if not fields[1].isdigit():
            bad.append(f"milestone position not an integer: {raw}")
            continue
        position = int(fields[1])
        positions.append(position)
        if last_position is not None:
            gap = position - last_position
            if not 5 <= gap <= 25:
                bad.append(f"milestone spacing {gap} outside 5..25: {raw}")
            if position <= last_position:
                bad.append(f"milestone positions not increasing: {raw}")
        last_position = position
    if positions and positions[-1] > chain_steps_seen:
        bad.append(
            f"milestone position {positions[-1]} exceeds the "
            f"{chain_steps_seen} chain steps present")
    return bad


def record_chars(example):
    """Rendered size of one record, for the 16k cap."""
    return (len(str(example.get("problem", "")))
            + sum(len(s) for s in example.get("steps", []))
            + len(str(example.get("final_answer", ""))))


# ---------------------------------------------------------------------------
# Text parsing (independent regexes, not depth_common's)
# ---------------------------------------------------------------------------

_N_RE = re.compile(
    r"\b(\d+)\s+(?:times|iterations|steps|terms|payments|periods|events|"
    r"rows|instructions|conversions|digits)\b|"
    r"\b(?:iterate|apply|run|repeat|unroll|accumulate|execute)"
    r"(?:\s+\S+){0,3}?\s+(\d+)\s|"
    r"\bfirst\s+(\d+)\b")


def parse_count(text):
    """The stated chain length N, or ``None`` (independent implementation)."""
    match = _N_RE.search(text)
    if not match:
        return None
    return int(next(g for g in match.groups() if g))
