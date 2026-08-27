"""Independent oracle machinery for the applied-reasoning strand (A9).

Nothing here may import ``applied_common`` or ``prob_common``: the point of an
oracle is a *second* implementation. The tests read the problem text only,
invert the surface rendering with their own grammar, and re-solve by a route
the generator does not use (job-size LCM instead of reciprocal sums, interval
endpoints instead of propagation rules, digit counting instead of the
generator's rounding loop).

Contents
--------
- text parsing: :func:`numbers_in`, :func:`parse_quantity`, :func:`parse_table`
- template inversion: :func:`invert_work_rate` (one regex set per surface
  rendering of ``applied_common.WORK_RATE_TOGETHER``)
- alternate-route solvers: :func:`solve_work_rate_lcm`
- magnitude: :func:`leading_digit_estimate`, :func:`order_of_magnitude`
- measurement: :class:`Interval` with exact rational endpoints
- rendering used for comparisons: :func:`decimal_text`, :func:`hours_text`
"""
import math
import re
from collections import namedtuple
from fractions import Fraction

# ---------------------------------------------------------------------------
# Number and text parsing
# ---------------------------------------------------------------------------

NUMBER_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?(?:/\d+)?")


def to_fraction(token):
    """Exact value of a number token: ``'12'``, ``'1.5'``, ``'3/8'``,
    ``'1,200'``."""
    token = token.strip().replace(",", "").replace("$", "")
    if "/" in token:
        num, den = token.split("/", 1)
        return Fraction(to_fraction(num), to_fraction(den))
    if "." in token:
        sign = -1 if token.startswith("-") else 1
        token = token.lstrip("+-")
        whole, frac = token.split(".", 1)
        return sign * (Fraction(int(whole or 0)) + Fraction(int(frac), 10 ** len(frac)))
    return Fraction(int(token))


def numbers_in(text):
    """Every number in ``text`` as ``(token, Fraction)`` pairs, in order."""
    out = []
    for match in NUMBER_RE.finditer(text):
        token = match.group(0)
        try:
            out.append((token.replace(",", ""), to_fraction(token)))
        except (ValueError, ZeroDivisionError):
            continue
    return out


def number_tokens(text):
    """The bare number strings of ``text`` (comma separators removed)."""
    return [token for token, _ in numbers_in(text)]


def parse_quantity(text):
    """``'6 hours'`` -> ``(Fraction(6), 'hours')``; ``'$2.50'`` ->
    ``(Fraction(5, 2), '$')``; ``'40%'`` -> ``(Fraction(40), '%')``."""
    text = text.strip().rstrip(".")
    money = re.fullmatch(r"\$(-?[\d,]+(?:\.\d+)?)", text)
    if money:
        return to_fraction(money.group(1)), "$"
    percent = re.fullmatch(r"(-?[\d,.]+)%", text)
    if percent:
        return to_fraction(percent.group(1)), "%"
    match = re.fullmatch(r"(-?[\d,]+(?:\.\d+)?(?:/\d+)?)\s*(.*)", text)
    if not match:
        raise ValueError(f"not a quantity: {text!r}")
    return to_fraction(match.group(1)), match.group(2).strip()


def parse_table(text):
    """Rows of a table embedded in problem text.

    The strand writes tables as ``intro — label: value; label: value.`` (an
    ASCII bar would break the step dialect). Returns ``[(label, value), …]``
    over every such run found in ``text``.
    """
    rows = []
    for sentence in re.split(r"(?<=[.?])\s+", text):
        body = sentence.split("—", 1)[1] if "—" in sentence else sentence
        if ":" not in body:
            continue
        for cell in body.split(";"):
            cell = cell.strip().rstrip(".").strip()
            if cell.count(":") != 1:
                continue
            label, value = (part.strip() for part in cell.split(":"))
            if label and value:
                rows.append((label, value))
    return rows


def table_lookup(text, label):
    """The value cell of the row whose label matches ``label`` (case
    insensitive), or ``None``."""
    for row_label, value in parse_table(text):
        if row_label.lower() == label.lower():
            return value
    return None


# ---------------------------------------------------------------------------
# Rendering (independent of prob_common)
# ---------------------------------------------------------------------------


def decimal_text(value):
    """Exact minimal-digit decimal text, by repeated ×10 rather than by
    factoring the denominator: ``Fraction(21, 2)`` -> ``'10.5'``. Falls back
    to ``n/d`` when the value does not terminate."""
    fr = Fraction(value)
    if fr.denominator == 1:
        return str(fr.numerator)
    scaled, places = fr, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        return f"{fr.numerator}/{fr.denominator}"
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if fr < 0 else "") + text


def hours_text(value):
    """``'2 hours'`` / ``'1 hour'`` / ``'10.5 hours'``."""
    text = decimal_text(value)
    return f"{text} hour" if Fraction(value) == 1 else f"{text} hours"


# ---------------------------------------------------------------------------
# Template inversion: applied_common.WORK_RATE_TOGETHER
# ---------------------------------------------------------------------------

WorkRateStory = namedtuple(
    "WorkRateStory", "rendering a_hours b_hours verb job")

_HOURS = r"(\d+(?:\.\d+)?) hours?"
_WORKER_A = r"([A-Za-z]+ A)"
_WORKER_B = r"([A-Za-z]+ B)"
_JOB = r"([a-z][a-z ]*?)"

_QUANTITY_A = re.compile(
    _WORKER_A + r" alone can ([a-z]+) the " + _JOB + r" in " + _HOURS + r"\.")
_QUANTITY_B = re.compile(_WORKER_B + r" alone can [a-z]+ it in " + _HOURS + r"\.")

_QUESTION_HEAD = re.compile(
    r"How long do " + _WORKER_A + r" and " + _WORKER_B
    + r" take to ([a-z]+) the " + _JOB + r" together\?")
_QUESTION_A = re.compile(_WORKER_A + r" alone takes " + _HOURS + r"\.")
_QUESTION_B = re.compile(_WORKER_B + r" alone takes " + _HOURS + r"\.")

_TABLE_INTRO = re.compile(r"Times to ([a-z]+) the " + _JOB + r" alone —")

_NARRATIVE_A = re.compile(_WORKER_A + r" would need " + _HOURS + r" alone\.")
_NARRATIVE_B = re.compile(_WORKER_B + r" would need " + _HOURS + r" alone\.")
_NARRATIVE_JOB = re.compile(r"How long until the " + _JOB + r" is done\?")

_COMPARISON_A = re.compile(
    r"It takes " + _HOURS + r" for " + _WORKER_A + r" to ([a-z]+) the " + _JOB + r"\.")
_COMPARISON_B = re.compile(
    _WORKER_B + r" needs only " + _HOURS + r" for the same job\.")


def _hours(match, group):
    return None if match is None else Fraction(to_fraction(match.group(group)))


def _invert_quantity_first(text):
    a, b = _QUANTITY_A.search(text), _QUANTITY_B.search(text)
    if a is None and b is None:
        return None
    verb = a.group(2) if a else None
    job = a.group(3) if a else None
    return WorkRateStory("quantity_first", _hours(a, 4), _hours(b, 2), verb, job)


def _invert_question_first(text):
    head = _QUESTION_HEAD.search(text)
    if head is None:
        return None
    a, b = _QUESTION_A.search(text), _QUESTION_B.search(text)
    return WorkRateStory("question_first", _hours(a, 2), _hours(b, 2),
                         head.group(3), head.group(4))


def _invert_table(text):
    intro = _TABLE_INTRO.search(text)
    if intro is None:
        return None
    times = {}
    for label, value in parse_table(text):
        match = re.fullmatch(r"[A-Za-z]+ ([AB])", label)
        if match:
            amount, unit_name = parse_quantity(value)
            if unit_name.startswith("hour"):
                times[match.group(1)] = amount
    return WorkRateStory("table", times.get("A"), times.get("B"),
                         intro.group(1), intro.group(2))


def _invert_narrative(text):
    a, b = _NARRATIVE_A.search(text), _NARRATIVE_B.search(text)
    job = _NARRATIVE_JOB.search(text)
    if job is None:
        return None
    return WorkRateStory("narrative", _hours(a, 2), _hours(b, 2), None,
                         job.group(1))


def _invert_comparison(text):
    a, b = _COMPARISON_A.search(text), _COMPARISON_B.search(text)
    if a is None and b is None:
        return None
    return WorkRateStory("comparison", _hours(a, 1), _hours(b, 2),
                         a.group(3) if a else None, a.group(4) if a else None)


_WORK_RATE_INVERTERS = (
    _invert_quantity_first,
    _invert_question_first,
    _invert_table,
    _invert_narrative,
    _invert_comparison,
)


def invert_work_rate(text, partial=False):
    """Inverts a ``work_rate_together`` story back to its slot values.

    Returns a :class:`WorkRateStory` (``rendering`` names the surface form) or
    ``None`` when the text is not one. With ``partial=True`` a story that is
    missing one of its two times still comes back, with ``None`` in that slot
    — that is how the missing-information records are checked.
    """
    for invert in _WORK_RATE_INVERTERS:
        story = invert(text)
        if story is None:
            continue
        if story.a_hours is not None and story.b_hours is not None:
            return story
        if partial:
            return story
    return None


def solve_work_rate_lcm(a_hours, b_hours):
    """Alternate route: size the job as ``lcm(a, b)`` units so both rates are
    whole numbers, add them, and divide. Never touches ``1/a + 1/b``.

    ``lcm(6, 3) = 6`` units: A does 1 unit/h, B does 2 units/h, together 3
    units/h, so 6 ÷ 3 = 2 hours.
    """
    a, b = int(a_hours), int(b_hours)
    if a <= 0 or b <= 0:
        raise ValueError("times must be positive")
    job = a * b // math.gcd(a, b)
    per_hour = job // a + job // b
    return Fraction(job, per_hour)


# ---------------------------------------------------------------------------
# Magnitude
# ---------------------------------------------------------------------------


def leading_digit_estimate(value):
    """Leading-digit rounding, by digit counting rather than by the
    generator's scaling loop: ``4653 -> 5000``, ``0.0372 -> 0.04``,
    ``Fraction(21, 2) -> 10``. Half rounds up."""
    fr = Fraction(value)
    if fr == 0:
        return Fraction(0)
    sign = 1 if fr > 0 else -1
    fr = abs(fr)
    power = len(str(fr.numerator)) - len(str(fr.denominator))
    while Fraction(10) ** power > fr:
        power -= 1
    while Fraction(10) ** (power + 1) <= fr:
        power += 1
    scale = Fraction(10) ** power
    lead = fr / scale
    rounded = (2 * lead.numerator + lead.denominator) // (2 * lead.denominator)
    if rounded == 10:
        rounded, scale = 1, scale * 10
    return sign * rounded * scale


def order_of_magnitude(value):
    """``k`` such that ``10^k <= abs(value) < 10^(k+1)``."""
    fr = abs(Fraction(value))
    if fr == 0:
        raise ValueError("no order of magnitude for 0")
    power = len(str(fr.numerator)) - len(str(fr.denominator))
    while Fraction(10) ** power > fr:
        power -= 1
    while Fraction(10) ** (power + 1) <= fr:
        power += 1
    return power


# ---------------------------------------------------------------------------
# Interval arithmetic (measurement uncertainty, tolerances, true ranges)
# ---------------------------------------------------------------------------


class Interval:
    """A closed interval with exact rational endpoints.

    Arithmetic is endpoint arithmetic — the oracle route for
    ``MeasurementUncertaintyGenerator``: multiply every corner and keep the
    extremes, rather than applying a propagation rule.
    """

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        lo, hi = Fraction(lo), Fraction(hi)
        if lo > hi:
            raise ValueError(f"empty interval [{lo}, {hi}]")
        self.lo, self.hi = lo, hi

    @classmethod
    def from_tolerance(cls, center, tolerance):
        """``12.5 ± 0.2`` -> ``[12.3, 12.7]``."""
        center, tolerance = Fraction(center), Fraction(tolerance)
        return cls(center - tolerance, center + tolerance)

    @classmethod
    def from_rounding(cls, shown, place):
        """True range of a displayed value: ``3.4`` to the nearest ``0.1`` ->
        ``[3.35, 3.45]`` (the upper end is exclusive in prose; the endpoints
        are what the arithmetic needs)."""
        shown, place = Fraction(shown), Fraction(place)
        return cls(shown - place / 2, shown + place / 2)

    def __eq__(self, other):
        return isinstance(other, Interval) and (self.lo, self.hi) == (other.lo, other.hi)

    def __hash__(self):
        return hash((self.lo, self.hi))

    def __repr__(self):
        return f"Interval({self.lo}, {self.hi})"

    def __contains__(self, value):
        return self.lo <= Fraction(value) <= self.hi

    @property
    def width(self):
        return self.hi - self.lo

    @property
    def midpoint(self):
        return (self.lo + self.hi) / 2

    def __add__(self, other):
        other = _as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other):
        other = _as_interval(other)
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other):
        other = _as_interval(other)
        corners = [self.lo * other.lo, self.lo * other.hi,
                   self.hi * other.lo, self.hi * other.hi]
        return Interval(min(corners), max(corners))

    def __truediv__(self, other):
        other = _as_interval(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError("divisor interval spans 0")
        corners = [self.lo / other.lo, self.lo / other.hi,
                   self.hi / other.lo, self.hi / other.hi]
        return Interval(min(corners), max(corners))

    __radd__ = __add__
    __rmul__ = __mul__

    def text(self, render=None):
        """``[97.17, 102.87]`` with the strand's number rendering."""
        render = render or decimal_text
        return f"[{render(self.lo)}, {render(self.hi)}]"


def _as_interval(value):
    return value if isinstance(value, Interval) else Interval(value, value)


def percent_error(measured, true_value):
    """``abs(m − t)/t`` as an exact Fraction (times 100 for percent)."""
    measured, true_value = Fraction(measured), Fraction(true_value)
    if true_value == 0:
        raise ZeroDivisionError("percent error needs a nonzero true value")
    return abs(measured - true_value) / abs(true_value)
