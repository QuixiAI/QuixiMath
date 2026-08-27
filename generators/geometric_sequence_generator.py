import math
import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


def wrap(v):
    """Parenthesizes negative or fractional values for display."""
    t = str(v)
    return f"({t})" if (isinstance(v, Fraction) and v.denominator != 1) \
        or v < 0 else t


def _fracs(max_q, proper=True):
    """Reduced fractions ±p/q, q ≤ max_q; proper keeps abs(r) < 1."""
    out = []
    for q in range(2, max_q + 1):
        top = q if proper else 3 * q
        for p in range(1, top):
            if p == q or math.gcd(p, q) != 1:
                continue
            if proper and p > q:
                continue
            out.append(Fraction(p, q))
            out.append(Fraction(-p, q))
    return out


INT_RATIOS = [Fraction(v) for v in (2, -2, 3, -3, 4, -4, 5, -5, 6, -6,
                                    10, -10)]
PROPER_RATIOS = _fracs(12)                       # abs(r) < 1
IMPROPER_RATIOS = [f for f in _fracs(5, proper=False) if abs(f) > 1]

NAMES = ["Maya", "Diego", "Priya", "Owen", "Lena", "Marcus", "Ines",
         "Tariq", "Nora", "Felix", "Amara", "Jonas", "Rosa", "Kenji",
         "Hana", "Luis", "Ada", "Bianca", "Omar", "Sasha"]

SYMBOLS = ["a", "b", "c", "g", "t", "u", "v", "w"]

MAX_TERM = 4000
MAX_NUM = 10 ** 6
MAX_DEN = 10 ** 4


def _size_ok(value):
    """Keeps answers hand-sized: bounded numerator and denominator."""
    return abs(value.numerator) <= MAX_NUM and value.denominator <= MAX_DEN


def _draw(ratios, k_choices):
    """Random (a, r, k) with k integer opening terms, all bounded."""
    r = random.choice(ratios)
    k = random.choice(k_choices)
    base = r.denominator ** (k - 1)
    growth = abs(r) ** (k - 1)
    cap = MAX_TERM if abs(r) < 1 else int(Fraction(MAX_TERM) / growth)
    m_max = cap // base
    if m_max < 1:
        return None
    a = base * random.choice([-1, 1]) * random.randint(1, m_max)
    return Fraction(a), r, k


def _ordinal(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


class GeometricSequenceGenerator(ProblemGenerator):
    """
    Geometric sequences shown as three to five opening terms: the nth
    term, a partial sum, the infinite sum when |r| < 1, and a blanked-out
    missing term.

    The common ratio is computed from one pair and verified on a second
    pair (A1). Infinite sums state the convergence condition before
    summing. All shown terms are integers by construction; later terms
    and sums may be exact fractions.

    Op-codes used:
    - SEQ_SETUP: the shown terms and the goal (established)
    - COMMON_RATIO: ratio of consecutive terms (work, value)
    - CHECK: verify r on another consecutive pair (established)
    - CONVERGE_CHECK: abs(r) < 1 so the infinite series converges
      (comparison, verdict)
    - SEQ_FORMULA / SEQ_APPLY: state then instantiate (established)
    - E / S / M / D: the arithmetic, exact fractions where needed
    - Z: final answer (integer or reduced fraction)
    """

    VARIANTS = ["nth_term", "partial_sum", "infinite_sum", "missing_term"]

    # Kept for backwards compatibility with callers that read the table.
    FRACTION_RS = [
        (Fraction(1, 2), [8, 16, 24, 32, 40, 48, -8, -16, -24, -32]),
        (Fraction(-1, 2), [8, 16, 24, 32, 40, 48, -8, -16, -24, -32]),
        (Fraction(1, 3), [27, 54, 81, 108, 135, -27, -54, -81]),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    # ---- phrasing ----------------------------------------------------------

    def _opening(self, shown, name, sym, series=False):
        """One sentence introducing the listed terms."""
        word = "series" if series else "sequence"
        tail = " forever" if series else ""
        return random.choice([
            f"The geometric {word} {shown} continues{tail}.",
            (f"A geometric {word} begins {shown} and continues in the "
             f"same way{tail}."),
            f"{name} writes the geometric {word} {shown} on the board.",
            f"Consider the geometric {word} {shown} whose pattern continues.",
            (f"Each term of the {word} {shown} is a fixed multiple of the "
             f"term before it."),
            f"Let {sym}_n be the geometric {word} {shown} with n starting at 1.",
            f"{name} extends the geometric pattern {shown} indefinitely.",
            f"The numbers {shown} form a geometric {word}.",
        ])

    def _goal(self, variant, n, sym):
        if variant == "nth_term":
            return random.choice([
                f"Find term {n}.",
                f"What is the {_ordinal(n)} term?",
                f"Find the {_ordinal(n)} term of the sequence.",
                f"Determine the value of term {n}.",
                f"Which number appears as term {n}?",
            ])
        if variant == "partial_sum":
            return random.choice([
                f"Find the sum of the first {n} terms.",
                f"What is the total of its first {n} terms?",
                f"Add up the first {n} terms.",
                f"Compute the sum S_{n} of the first {n} terms.",
                f"Determine the sum of terms 1 through {n}.",
            ])
        if variant == "infinite_sum":
            return random.choice([
                "Find the sum of the infinite series.",
                "What value does the infinite sum approach?",
                "Compute the total of all the terms.",
                "Evaluate the infinite sum.",
                "Find the limit of its partial sums.",
            ])
        return random.choice([
            "Find the missing term.",
            "What number belongs in the blank?",
            "Determine the term hidden by the blank.",
            "Supply the missing value.",
            "Which number completes the sequence?",
        ])

    # ---- generation --------------------------------------------------------

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        name = random.choice(NAMES)
        sym = random.choice(SYMBOLS)

        for _ in range(200):
            built = self._build(variant)
            if built is not None:
                break
        else:  # pragma: no cover - the pools always yield a draw
            raise RuntimeError("could not draw a geometric sequence")
        t, r, k, n, answer, steps, shown_items = built

        shown = ", ".join(shown_items) + ", ..."
        steps[0] = step("SEQ_SETUP", shown, steps[0].split("|", 2)[2])
        problem = (self._opening(shown, name, sym,
                                 series=(variant == "infinite_sum"))
                   + " " + self._goal(variant, n, sym))

        return dict(
            problem_id=jid(),
            operation=f"geometric_sequence_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _build(self, variant):
        """Draws one instance; returns None when the draw is out of range."""
        if variant == "infinite_sum":
            drawn = _draw(PROPER_RATIOS, [3, 4, 5])
        elif variant == "partial_sum":
            pool = (INT_RATIOS if random.random() < 0.7
                    else PROPER_RATIOS + IMPROPER_RATIOS)
            drawn = _draw(pool, [3, 4, 5])
        elif variant == "missing_term":
            pool = (INT_RATIOS if random.random() < 0.6
                    else PROPER_RATIOS + IMPROPER_RATIOS)
            drawn = _draw(pool, [4, 5])
        else:
            pool = (INT_RATIOS if random.random() < 0.6
                    else PROPER_RATIOS + IMPROPER_RATIOS)
            drawn = _draw(pool, [3, 4, 5])
        if drawn is None:
            return None
        a, r, k = drawn
        t = [a * r ** i for i in range(k)]
        if any(x.denominator != 1 for x in t):
            return None
        shown_items = [str(x.numerator) for x in t]

        if variant == "nth_term":
            return self._nth_term(t, r, k, shown_items)
        if variant == "partial_sum":
            return self._partial_sum(t, r, k, shown_items)
        if variant == "infinite_sum":
            return self._infinite_sum(t, r, k, shown_items)
        return self._missing_term(t, r, k, shown_items)

    def _ratio_steps(self, goal, t, r, i=0, j=None):
        """SEQ_SETUP placeholder plus the ratio and its verification."""
        steps = [step("SEQ_SETUP", "terms", goal)]
        steps.append(step("COMMON_RATIO",
                          f"{t[i + 1].numerator}/{wrap(t[i].numerator)}", r))
        if j is None:
            j = i + 1
        steps.append(step("CHECK", "ratio",
                          f"{t[j + 1].numerator}/"
                          f"{wrap(t[j].numerator)} = {r}", r))
        return steps

    def _nth_term(self, t, r, k, shown_items):
        options = []
        for n in range(k + 1, 13):
            value = t[0] * r ** (n - 1)
            if _size_ok(value) and abs(value) <= MAX_NUM:
                options.append((n, value))
        if not options:
            return None
        n, value = random.choice(options)
        steps = self._ratio_steps(f"term {n}", t, r)
        steps.append(step("SEQ_FORMULA", "a_n = a_1·r^(n - 1)"))
        steps.append(step("SEQ_APPLY",
                          f"a_{n} = {t[0].numerator}·{wrap(r)}^{n - 1}"))
        steps.append(step("E", wrap(r), n - 1, r ** (n - 1)))
        steps.append(step("M", t[0].numerator, r ** (n - 1), value))
        answer = str(value)
        steps.append(step("Z", answer))
        return t, r, k, n, answer, steps, shown_items

    def _partial_sum(self, t, r, k, shown_items):
        options = []
        for n in range(max(3, k), 10):
            total = t[0] * (r ** n - 1) / (r - 1)
            if _size_ok(total) and _size_ok(r ** n):
                options.append((n, total))
        if not options:
            return None
        n, total = random.choice(options)
        rn = r ** n
        num = t[0] * (rn - 1)
        den = r - 1
        steps = self._ratio_steps(f"sum of first {n} terms", t, r)
        steps.append(step("SEQ_FORMULA", "S_n = a_1(r^n - 1)/(r - 1)"))
        steps.append(step("SEQ_APPLY",
                          f"S_{n} = {t[0].numerator}·({wrap(r)}^{n} - 1)/"
                          f"({wrap(r)} - 1)"))
        steps.append(step("E", wrap(r), n, rn))
        steps.append(step("S", rn, 1, rn - 1))
        steps.append(step("M", t[0].numerator, rn - 1, num))
        steps.append(step("S", r, 1, den))
        if den != 1:
            steps.append(step("D", num, den, total))
        answer = str(total)
        steps.append(step("Z", answer))
        return t, r, k, n, answer, steps, shown_items

    def _infinite_sum(self, t, r, k, shown_items):
        total = t[0] / (1 - r)
        if not _size_ok(total):
            return None
        steps = self._ratio_steps("sum of the infinite series", t, r)
        steps.append(step("CONVERGE_CHECK", f"abs(r) = {abs(r)} < 1",
                          "converges"))
        steps.append(step("SEQ_FORMULA", "S = a_1/(1 - r)"))
        steps.append(step("SEQ_APPLY",
                          f"S = {t[0].numerator}/(1 - {wrap(r)})"))
        steps.append(step("S", 1, r, 1 - r))
        steps.append(step("D", t[0].numerator, 1 - r, total))
        answer = str(total)
        steps.append(step("Z", answer))
        return t, r, k, None, answer, steps, shown_items

    def _missing_term(self, t, r, k, shown_items):
        hidden = random.randint(1, k - 1)
        value = t[hidden]
        shown_items = list(shown_items)
        shown_items[hidden] = "__"
        # A visible adjacent pair gives r; a second one verifies it.
        pairs = [i for i in range(k - 1)
                 if i != hidden and i + 1 != hidden]
        if not pairs:
            return None
        i = pairs[0]
        steps = [step("SEQ_SETUP", "terms", f"the missing term {hidden + 1}")]
        steps.append(step("COMMON_RATIO",
                          f"{t[i + 1].numerator}/{wrap(t[i].numerator)}", r))
        if len(pairs) > 1:
            j = pairs[1]
            steps.append(step("CHECK", "ratio",
                              f"{t[j + 1].numerator}/"
                              f"{wrap(t[j].numerator)} = {r}", r))
        steps.append(step("SEQ_FORMULA", "a_n = a_(n - 1)·r"))
        if hidden - 1 >= 0 and shown_items[hidden - 1] != "__":
            src = t[hidden - 1].numerator
            steps.append(step("SEQ_APPLY",
                              f"a_{hidden + 1} = {src}·{wrap(r)}"))
            steps.append(step("M", src, r, value))
        else:
            src = t[hidden + 1].numerator
            steps.append(step("SEQ_APPLY",
                              f"a_{hidden + 1} = {src}/{wrap(r)}"))
            steps.append(step("D", src, r, value))
        nxt = hidden + 1
        if nxt < k:
            steps.append(step("CHECK", "ratio",
                              f"{t[nxt].numerator}/{wrap(value.numerator)}"
                              f" = {r}", r))
        answer = str(value)
        steps.append(step("Z", answer))
        return t, r, k, hidden + 1, answer, steps, shown_items
