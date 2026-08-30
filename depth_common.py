"""Shared infrastructure for the depth strand (``plans/depth_plan.md``).

The strand's contract, enforced here and in ``tests/test_depth_conventions.py``:

- **Depth tiers** — every depth generator draws a tier (``d50``/``d100``/
  ``d200``), appends it to the operation string, and must produce a serial
  dependency chain at least as long as the tier floor.
- **Serial chaining** — the :class:`Chain` emitter guarantees, mechanically,
  that each chained step's first payload field is the rendering of the
  previous step's result, so the conventions test can measure dependency
  depth structurally instead of trusting the generator.
- **Milestones** — ``MILESTONE|k|<invariant>|<value>`` steps recompute a
  running invariant every 10-15 chain links.  (The names ``CHECKPOINT``,
  ``CHECK_POINT`` and ``INVARIANT`` are deliberately not used: the latter
  two already exist with different field semantics, and ``CHECKPOINT``
  differs from ``CHECK_POINT`` by a single underscore.)
- **Bounded intermediates** — chains never let values grow with depth; the
  constructors here (modular orbits, bounded ledgers, geometric-decay
  contractive orbits) are the sanctioned patterns.

Exact arithmetic only, as everywhere in the repo.
"""
import random
import re
from fractions import Fraction

from helpers import step

# ---------------------------------------------------------------------------
# Depth tiers (plans/depth_plan.md §3)
# ---------------------------------------------------------------------------

#: tier -> (inclusive chain-length window) used when a generator draws N.
DEPTH_TIERS = {
    "d50": (40, 70),
    "d100": (85, 130),
    "d200": (170, 260),
}

#: The conventions-test floor per tier (the low end of the window).
TIER_FLOORS = {tier: window[0] for tier, window in DEPTH_TIERS.items()}

#: Default draw weights: the corpus skews long without letting the
#: token-heavy d200 records dominate.
TIER_WEIGHTS = (("d50", 50), ("d100", 35), ("d200", 15))

#: Hard cap on one record's rendered size (problem + steps + answer).
MAX_RECORD_CHARS = 16_000

#: Milestones appear every SPACING chain links (inclusive window).
MILESTONE_SPACING = (10, 15)

_TIER_SUFFIX = re.compile(r"_(d50|d100|d200|d400)$")


def pick_tier(rng=random):
    """Draw a tier by the standard weights."""
    tiers = [t for t, _ in TIER_WEIGHTS]
    weights = [w for _, w in TIER_WEIGHTS]
    return rng.choices(tiers, weights=weights, k=1)[0]


def tier_target(tier, rng=random):
    """A chain-length target inside the tier's window."""
    lo, hi = DEPTH_TIERS[tier]
    return rng.randint(lo, hi)


def tier_of(operation):
    """The tier suffix carried by an operation string, or ``None``."""
    match = _TIER_SUFFIX.search(operation)
    return match.group(1) if match else None


#: Difficulty bump per tier (plans/depth_plan.md §3), applied by each
#: generator via :func:`tier_difficulty` — ``stamp_metadata`` lets
#: generator-provided values win over the class's CURRICULUM entry.
_TIER_BUMP = {"d50": 0, "d100": 1, "d200": 2, "d400": 2}


def tier_difficulty(base, tier):
    """The class's base difficulty bumped for the tier, capped at 5."""
    return min(5, base + _TIER_BUMP[tier])


# ---------------------------------------------------------------------------
# The chain emitter
# ---------------------------------------------------------------------------

class Chain:
    """Running-state step emitter that enforces operand chaining.

    Every :meth:`apply` renders the CURRENT value as the step's first
    payload field, the operand second, the NEW value last — so consecutive
    chained steps are linked by exact string equality, which is what the
    conventions test measures.  Interleaved :meth:`milestone` steps do not
    break the measured chain (the test skips ``MILESTONE`` rows).

    ``render`` turns state into step text (default ``str``); override it
    for money (cents -> ``$12.34``) or fractions.
    """

    def __init__(self, start, render=str, milestone_spacing=None, rng=random):
        self.render = render
        self.value = start
        self.steps = []
        self.links = 0
        self._rng = rng
        if milestone_spacing is True:
            milestone_spacing = MILESTONE_SPACING
        self._spacing = milestone_spacing
        self._next_milestone = (self._draw_spacing()
                                if milestone_spacing is not None else None)
        self._invariant = None

    def _draw_spacing(self):
        lo, hi = self._spacing
        return self.links + self._rng.randint(lo, hi)

    def set_invariant(self, describe, compute):
        """Install the milestone invariant.

        ``describe`` is the short text for the MILESTONE step's second
        field; ``compute(value, links)`` returns the invariant's current
        value (rendered with ``str``).
        """
        self._invariant = (describe, compute)

    def apply(self, op, operand, result, extra=None):
        """Emit ``op|<current>|<operand>[|extra]|<result>`` and advance.

        The NEW value is always the LAST field — the conventions test
        links steps by ``fields[1] == previous last field``, so an
        annotation must never displace the result from last position.
        """
        fields = [self.render(self.value), operand]
        if extra is not None:
            fields.append(extra)
        fields.append(self.render(result))
        self.steps.append(step(op, *fields))
        self.value = result
        self.links += 1
        if (self._next_milestone is not None and self._invariant is not None
                and self.links >= self._next_milestone):
            self.milestone()
            self._next_milestone = self._draw_spacing()

    def milestone(self):
        """Emit ``MILESTONE|<links>|<invariant>|<value>`` for the state now."""
        if self._invariant is None:
            raise ValueError("set_invariant() before emitting milestones")
        describe, compute = self._invariant
        self.steps.append(step("MILESTONE", self.links, describe,
                               compute(self.value, self.links)))


# ---------------------------------------------------------------------------
# Bounded-state constructors
# ---------------------------------------------------------------------------

def modular_orbit(a, b, m, x0, n):
    """``[x0, x1, ..., xn]`` under ``x -> (a*x + b) mod m``."""
    orbit = [x0 % m]
    for _ in range(n):
        orbit.append((a * orbit[-1] + b) % m)
    return orbit


def find_cycle(f, x0, limit=100_000):
    """Floyd tortoise-and-hare: ``(mu, lam)`` — cycle start and length.

    Raises ``ValueError`` if no cycle is found within ``limit`` steps
    (cannot happen for a function on a finite set probed long enough).
    """
    tortoise, hare = f(x0), f(f(x0))
    steps_taken = 0
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(f(hare))
        steps_taken += 1
        if steps_taken > limit:
            raise ValueError("no cycle within limit")
    mu = 0
    tortoise = x0
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    lam = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        lam += 1
    return mu, lam


def contractive_orbit(a_den, fixed_point, n, delta=1):
    """Exact geometric decay toward ``fixed_point``: integers throughout.

    The map is ``x -> fixed_point + (x - fixed_point)/a_den`` started at
    ``fixed_point + delta * a_den**n``, so ``x_k = F + delta*a_den**(n-k)``
    is an integer for every ``k <= n`` and lands exactly on ``F + delta``.

    Values scale as ``a_den**n``, so callers MUST keep them bounded:
    a ``ValueError`` is raised if the starting value's offset exceeds
    ``10**6``.  This constructor therefore suits shallow chains or chain
    *segments*, never a full d200 chain on its own (use modular state for
    those).
    """
    offset = delta * a_den ** n
    if abs(offset) > 10 ** 6:
        raise ValueError("contractive orbit would exceed the value bound")
    return [fixed_point + delta * a_den ** (n - k) for k in range(n + 1)]


def cents_ledger(start_cents, n, rng=random, low=0, high=1_000_00):
    """``n`` ledger events keeping the balance inside ``[low, high]``.

    Returns ``[(kind, amount_cents, balance_cents), ...]`` where kind is
    ``deposit`` or ``withdrawal``; amounts are multiples of 25 cents so
    every balance is exact and hand-friendly.
    """
    balance = start_cents
    events = []
    for _ in range(n):
        headroom = high - balance
        floor_room = balance - low
        if headroom < 25 and floor_room < 25:
            raise ValueError("ledger bounds leave no legal move")
        choices = []
        if headroom >= 25:
            choices.append("deposit")
        if floor_room >= 25:
            choices.append("withdrawal")
        kind = rng.choice(choices)
        room = headroom if kind == "deposit" else floor_room
        amount = rng.randrange(25, min(room, 200_00) + 1, 25)
        balance += amount if kind == "deposit" else -amount
        events.append((kind, amount, balance))
    return events


# ---------------------------------------------------------------------------
# Shared text helpers
# ---------------------------------------------------------------------------

#: Phrasings that state the chain length; every template must embed the
#: count through one of these shapes so :func:`parse_count` inverts it.
_COUNT_PATTERNS = (
    re.compile(r"\b(\d+)\s+(?:times|iterations|applications|steps|terms|payments|"
               r"periods|events|rows|instructions|conversions|digits)\b"),
    re.compile(r"\b(?:iterate|apply|run|repeat|unroll|accumulate|execute)"
               r"(?:\s+\S+){0,3}?\s+(\d+)\s"),
    re.compile(r"\bfirst\s+(\d+)\b"),
)


def parse_count(text):
    """The chain length N stated in problem text, or ``None``."""
    for pattern in _COUNT_PATTERNS:
        match = pattern.search(text)
        if match:
            return int(match.group(1))
    return None


def cents_txt(cents):
    """Exact cents -> house money format (``$12.34``, ``-$0.75``)."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"
