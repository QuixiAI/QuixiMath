"""Shared numeric helpers and experiment objects for the probability strand.

This module is the single home of the exact-rendering helpers that the
probability, statistics, and applied strands share (see
``plans/probability_plan.md`` §4 and ``plans/statistics_plan.md`` §4):

- ``dec`` / ``exact`` / ``p4`` / ``pct`` / ``money`` / ``prob_txt`` /
  ``odds_txt`` — canonical answer renderings (DESIGN.md "Probability
  answers").
- ``phi`` / ``phi_table`` — the supplied standard-normal excerpt with decoy
  rows, byte-identical to ``NormalTableGenerator._table`` (Principle 5: no
  unstated lookups).
- ``supplied_constant`` — the inline ``e^-2 = 0.1353`` form.
- ``NP_BANK`` — (n, p) pairs whose ``npq`` is a perfect square, so every
  half-integer continuity-corrected z has at most two decimals.
- ``Coin`` / ``Die`` / ``Spinner`` / ``Bag`` / ``NumberedCards`` /
  ``LetterTiles`` / ``Menu`` / ``Product`` — experiment objects: a canonical
  outcome enumerator in the §3 order (H before T, numbers ascending, spinner
  sectors as printed, bag colors as listed), a roster printer, and three
  prose renderers each.
- ``Predicate`` and the named event tests (``even``, ``multiple_of`` …) with
  printable names, ``WeightedSpace`` (atoms with Fraction weights,
  ``measure`` / ``given`` / validity) and ``TwoWayTable`` (the
  ``<row>=<v> and <col>=<w>: n`` prose form).

Generator-side only: the oracle modules under ``tests/`` never import this
file (A9: the oracle must be an independent route).
"""
import itertools
import math
import random
import re
from fractions import Fraction

# ---------------------------------------------------------------------------
# Number rendering (canonical, A0)
# ---------------------------------------------------------------------------


def dec(fr):
    """Exact decimal string for a Fraction whose denominator is
    2^a·5^b: 33/10 -> '3.3', 1331/1000 -> '1.331'. Raises on any other
    denominator (use ``exact`` when a fraction fallback is wanted)."""
    fr = Fraction(fr)
    num, den = fr.numerator, fr.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    if den != 1:
        raise ValueError(f"{fr} does not terminate")
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


def terminates(fr):
    """True when ``Fraction(fr)`` has a 2^a·5^b denominator."""
    d = Fraction(fr).denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    fr = Fraction(fr)
    return dec(fr) if terminates(fr) else str(fr)


def prob_txt(fr):
    """Probability / moment rendering: lowest-terms fraction, integers plain."""
    fr = Fraction(fr)
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


def p4(x):
    """Renders a probability with 4 decimals: 0.0968."""
    return f"{float(x):.4f}"


def pct(fr):
    """Percent rendering: ``pct(Fraction(3, 8))`` -> '37.5%'. The value must
    terminate as a percent."""
    return dec(Fraction(fr) * 100) + "%"


def money(fr):
    """Money rendering: two decimals, cents exact: ``$20.06``."""
    fr = Fraction(fr)
    if (fr * 100).denominator != 1:
        raise ValueError(f"{fr} is not a whole number of cents")
    cents = int(fr * 100)
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def odds_txt(fr):
    """Odds ``a:b`` in lowest terms for probability ``fr``."""
    fr = Fraction(fr)
    against = 1 - fr
    a, b = fr.numerator * against.denominator, against.numerator * fr.denominator
    g = math.gcd(a, b) or 1
    return f"{a // g}:{b // g}"


# ---------------------------------------------------------------------------
# Supplied constants (Principle 5)
# ---------------------------------------------------------------------------


def phi(z):
    """Standard normal CDF rounded to 4 decimals (table convention)."""
    return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)


def phi_table(zs, decoys=2):
    """Renders the standard-normal excerpt for the needed |z| values plus
    decoy rows. Byte-identical to ``NormalTableGenerator._table`` for
    ``decoys=2``: decoys sit at ``min+0.2`` and ``max+0.3`` (rounded to a
    tenth, kept only inside (0, 3.4])."""
    need = sorted({abs(float(z)) for z in zs})
    extra = []
    if decoys >= 1:
        extra.append(round(need[0] + 0.2, 1))
    if decoys >= 2:
        extra.append(round(need[-1] + 0.3, 1))
    rows = sorted(set(need + [d for d in extra if 0 < d <= 3.4]))
    cells = "; ".join(f"z={z:.2f}: {p4(phi(z))}" for z in rows)
    return f"Standard normal table, Φ(z) = P(Z < z): {cells}"


def supplied_constant(label, value, places=4):
    """Inline supplied-constant form: ``supplied_constant('e^-2',
    math.exp(-2))`` -> 'e^-2 = 0.1353'."""
    return f"{label} = {float(value):.{places}f}"


# ---------------------------------------------------------------------------
# Exactness banks
# ---------------------------------------------------------------------------

# (n, p) with npq a perfect square whose root is in {2, 5, 10, 20}
# (plans/probability_plan.md, NormalApproxBinomialGenerator).
NP_BANK = [
    (16, Fraction(1, 2)), (18, Fraction(1, 3)), (18, Fraction(2, 3)),
    (100, Fraction(1, 2)), (180, Fraction(1, 6)), (180, Fraction(5, 6)),
    (400, Fraction(1, 2)), (450, Fraction(1, 3)), (450, Fraction(2, 3)),
    (625, Fraction(1, 5)), (625, Fraction(4, 5)), (720, Fraction(1, 6)),
    (720, Fraction(5, 6)), (1600, Fraction(1, 2)),
]


def binomial_sigma(n, p):
    """Integer sqrt(npq) for a bank pair; raises if not a perfect square."""
    npq = Fraction(n) * p * (1 - p)
    if npq.denominator != 1:
        raise ValueError(f"npq not integral for {(n, p)}")
    root = math.isqrt(npq.numerator)
    if root * root != npq.numerator:
        raise ValueError(f"npq not a perfect square for {(n, p)}")
    return root


def is_perfect_square(fr):
    """True when ``Fraction(fr)`` is the square of a rational."""
    fr = Fraction(fr)
    if fr < 0:
        return False
    n, d = fr.numerator, fr.denominator
    return math.isqrt(n) ** 2 == n and math.isqrt(d) ** 2 == d


def sqrt_fraction(fr):
    """Exact rational square root of a perfect-square Fraction."""
    fr = Fraction(fr)
    if not is_perfect_square(fr):
        raise ValueError(f"{fr} is not a perfect square")
    return Fraction(math.isqrt(fr.numerator), math.isqrt(fr.denominator))


# ---------------------------------------------------------------------------
# Rendering conventions for events (plans/probability_plan.md §3)
# ---------------------------------------------------------------------------


def roster(items):
    """Event roster in the foundations set dialect: ``{1, 2, 3}`` / ``∅``.
    ``items`` must already be in enumeration order."""
    items = list(items)
    return "{" + ", ".join(str(i) for i in items) + "}" if items else "∅"


def given(a, b):
    """Conditioning text: ``P(A given B)`` — never a bar."""
    return f"P({a} given {b})"


def leading_digit_round(fr):
    """Leading-digit rounding used by ESTIMATE steps: 4653 -> 5000,
    0.0372 -> 0.04, 120/1.5 handled by caller. Returns a Fraction."""
    fr = Fraction(fr)
    if fr == 0:
        return fr
    sign = -1 if fr < 0 else 1
    fr = abs(fr)
    k = 0
    while fr >= 10:
        fr /= 10
        k += 1
    while fr < 1:
        fr *= 10
        k -= 1
    lead = int(fr + Fraction(1, 2))
    return sign * Fraction(lead) * Fraction(10) ** k




# ---------------------------------------------------------------------------
# Outcomes and named events (plans/probability_plan.md §3)
# ---------------------------------------------------------------------------

VOWELS = "AEIOU"
ORDINALS = ("first", "second", "third", "fourth", "fifth", "sixth",
            "seventh", "eighth")
TIMES_WORDS = {1: "once", 2: "twice", 3: "three times", 4: "four times",
               5: "five times", 6: "six times", 7: "seven times",
               8: "eight times"}
INT_RE = re.compile(r"-?\d+")


def plural(word, count):
    """English plural for the experiment renderers: 1 marble, 3 marbles."""
    if count == 1:
        return word
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def listing(items):
    """Comma listing used inside experiment clauses.

    Deliberately never uses ' and ': ``Product`` joins component clauses with
    ' and ', and the oracle splits there."""
    return ", ".join(str(i) for i in items)


class Outcome:
    """One point of a sample space: the printed label plus its components.

    Equality and hashing are by label, so outcomes drop into rosters, sets,
    and comparisons against plain strings.
    """

    __slots__ = ("label", "parts")

    def __init__(self, label, parts=None):
        self.label = str(label)
        self.parts = (tuple(str(p) for p in parts) if parts is not None
                      else (self.label,))

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Outcome({self.label!r}, {self.parts!r})"

    def __eq__(self, other):
        if isinstance(other, Outcome):
            return self.label == other.label
        return self.label == other

    def __hash__(self):
        return hash(self.label)

    def numbers(self):
        """The integer components of the outcome, in order."""
        return [int(p) for p in self.parts if INT_RE.fullmatch(p)]


def as_outcome(value):
    """Coerces a label to an ``Outcome``; ``'(3, 4)'`` splits into parts."""
    if isinstance(value, Outcome):
        return value
    text = str(value)
    matched = re.fullmatch(r"\((.+)\)", text)
    if matched:
        return Outcome(text, [p.strip() for p in matched.group(1).split(",")])
    return Outcome(text)


class Predicate:
    """A named event test, printable in problem text and EVENT steps."""

    def __init__(self, name, test):
        self.name = name
        self.test = test

    def __call__(self, outcome):
        return bool(self.test(as_outcome(outcome)))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Predicate({self.name!r})"

    def __and__(self, other):
        return Predicate(f"{self.name} and {other.name}",
                         lambda o: self(o) and other(o))

    def __or__(self, other):
        return Predicate(f"{self.name} or {other.name}",
                         lambda o: self(o) or other(o))

    def __invert__(self):
        return Predicate(f"not {self.name}", lambda o: not self(o))


def _sole_number(outcome):
    """The single integer component of an outcome (raises on compounds)."""
    nums = outcome.numbers()
    if len(nums) != 1:
        raise ValueError(f"{outcome.label} has {len(nums)} numeric parts; "
                         "wrap the test with component(index, predicate)")
    return nums[0]


def _sole_letter(outcome):
    """The single letter component of an outcome (raises on compounds)."""
    if len(outcome.parts) != 1 or len(outcome.parts[0]) != 1:
        raise ValueError(f"{outcome.label} is not a single letter; "
                         "wrap the test with component(index, predicate)")
    return outcome.parts[0].upper()


even = Predicate("even", lambda o: _sole_number(o) % 2 == 0)
odd = Predicate("odd", lambda o: _sole_number(o) % 2 != 0)
vowel = Predicate("a vowel", lambda o: _sole_letter(o) in VOWELS)
doubles = Predicate("doubles",
                    lambda o: len(o.parts) > 1 and len(set(o.parts)) == 1)


def multiple_of(k):
    """Event ``a multiple of k`` on the outcome's number."""
    return Predicate(f"a multiple of {k}", lambda o: _sole_number(o) % k == 0)


def greater_than(k):
    """Event ``greater than k``."""
    return Predicate(f"greater than {k}", lambda o: _sole_number(o) > k)


def at_least(k):
    """Event ``at least k``."""
    return Predicate(f"at least {k}", lambda o: _sole_number(o) >= k)


def less_than(k):
    """Event ``less than k``."""
    return Predicate(f"less than {k}", lambda o: _sole_number(o) < k)


def at_most(k):
    """Event ``at most k``."""
    return Predicate(f"at most {k}", lambda o: _sole_number(o) <= k)


def colour(name):
    """Event ``red``: every drawn object has that color (name or initial)."""
    keys = {str(name).lower(), str(name)[:1].lower()}
    return Predicate(str(name),
                     lambda o: all(p.lower() in keys for p in o.parts))


color = colour  # American spelling used by the generator prose


def sum_equals(k):
    """Event ``a sum of k`` over the numeric components."""
    return Predicate(f"a sum of {k}", lambda o: sum(o.numbers()) == k)


def at_least_one(face):
    """Event ``at least one H``: some component equals ``face``."""
    return Predicate(f"at least one {face}",
                     lambda o: any(p == str(face) for p in o.parts))


def component(index, predicate):
    """Applies a predicate to one component: ``the first is even``."""
    return Predicate(f"the {ORDINALS[index]} is {predicate.name}",
                     lambda o: predicate(Outcome(o.parts[index])))


# ---------------------------------------------------------------------------
# Experiment objects (plans/probability_plan.md §4)
# ---------------------------------------------------------------------------


class Experiment:
    """A finite experiment: canonical enumerator, roster printer, prose.

    Subclasses set ``PHRASINGS`` and define one ``_clause_<style>`` method per
    phrasing. A clause is a lower-case verb phrase with no ' and ' in it, so
    ``Product`` can join component clauses with ' and ' and the oracle can
    split them again. ``outcomes()`` lists the printed outcomes in §3
    enumeration order; ``items()`` lists the equally likely labelled objects
    behind them (they differ only for ``Bag`` and ``LetterTiles``).
    """

    PHRASINGS = ()
    REPEATABLE = False
    kind = "experiment"

    def outcomes(self):
        """Printed outcomes in enumeration order."""
        raise NotImplementedError

    def items(self):
        """Equally likely labelled objects behind the printed outcomes."""
        return self.outcomes()

    def size(self):
        """Number of equally likely items."""
        return len(self.items())

    def labels(self):
        """Printed outcome labels in enumeration order."""
        return [o.label for o in self.outcomes()]

    def roster_text(self):
        """The sample space as a roster: ``{H, T}``."""
        return roster(self.outcomes())

    def event(self, predicate):
        """Items satisfying ``predicate``, in enumeration order."""
        return [o for o in self.items() if predicate(o)]

    def event_roster(self, predicate):
        """Roster of the printed outcomes satisfying ``predicate``."""
        return roster([o for o in self.outcomes() if predicate(o)])

    def probability(self, predicate):
        """Exact probability of an event, as a Fraction."""
        return Fraction(len(self.event(predicate)), self.size())

    def weighted(self):
        """The experiment as a ``WeightedSpace`` over its printed outcomes."""
        return WeightedSpace.uniform(self.labels())

    def key(self):
        """Identity used by ``Product`` to detect repeated trials."""
        return (type(self).__name__,)

    def style(self, style=None):
        """Validates a phrasing name, or draws one from ``random``."""
        if style is None:
            return random.choice(self.PHRASINGS)
        if style not in self.PHRASINGS:
            raise ValueError(f"style must be one of {self.PHRASINGS} or None")
        return style

    def clause(self, style=None):
        """Lower-case verb phrase for one phrasing."""
        return getattr(self, f"_clause_{self.style(style)}")()

    def prose(self, style=None):
        """One sentence describing the experiment."""
        text = self.clause(style)
        return text[0].upper() + text[1:] + "."


class Coin(Experiment):
    """A fair coin. Outcomes ``H`` then ``T`` (§3 fixes the order)."""

    PHRASINGS = ("flip", "toss", "chance")
    REPEATABLE = True
    kind = "coin"

    def outcomes(self):
        return [Outcome("H"), Outcome("T")]

    def _clause_flip(self):
        return "a fair coin is flipped"

    def _clause_toss(self):
        return "a fair coin is tossed"

    def _clause_chance(self):
        return "a coin equally likely to land heads or tails is flipped"


class Die(Experiment):
    """A fair die with faces 1..n, enumerated ascending."""

    PHRASINGS = ("roll", "faces", "throw")
    REPEATABLE = True
    kind = "die"

    def __init__(self, sides=6):
        if sides < 2:
            raise ValueError("a die needs at least 2 faces")
        self.sides = sides

    def outcomes(self):
        return [Outcome(v) for v in range(1, self.sides + 1)]

    def key(self):
        return ("Die", self.sides)

    def _clause_roll(self):
        return f"a fair {self.sides}-sided die is rolled"

    def _clause_faces(self):
        return f"a fair die with faces numbered 1 to {self.sides} is rolled"

    def _clause_throw(self):
        return f"a fair {self.sides}-sided die is thrown"


class Spinner(Experiment):
    """A spinner with equal sectors, enumerated in the order printed."""

    PHRASINGS = ("spin", "arrow", "wheel")
    REPEATABLE = True
    kind = "spinner"

    def __init__(self, labels):
        labels = [str(v) for v in labels]
        if len(labels) < 2:
            raise ValueError("a spinner needs at least 2 sectors")
        if len(set(labels)) != len(labels):
            raise ValueError(f"spinner sectors must be distinct: {labels}")
        self.sector_labels = labels

    def outcomes(self):
        return [Outcome(v) for v in self.sector_labels]

    def key(self):
        return ("Spinner", tuple(self.sector_labels))

    def _clause_spin(self):
        return (f"a spinner with {len(self.sector_labels)} equal sectors "
                f"labelled {listing(self.sector_labels)} is spun")

    def _clause_arrow(self):
        return ("the arrow of a fair spinner with equal sectors "
                f"{listing(self.sector_labels)} is spun")

    def _clause_wheel(self):
        return (f"a wheel with {len(self.sector_labels)} equal sections "
                f"marked {listing(self.sector_labels)} is spun")


class Bag(Experiment):
    """A bag of colored objects; one object is drawn at random.

    Outcomes are the color codes in the order the problem lists the colors
    (§3): the upper-case initials when those are distinct, otherwise the full
    color names. ``items()`` is one labelled object per unit of count
    (``R1, R2, R3, B1, …``), which is the equally likely space.
    """

    PHRASINGS = ("bag", "jar", "urn")
    CONTAINERS = {"bag": ("a bag", "marble"), "jar": ("a jar", "counter"),
                  "urn": ("an urn", "ball")}
    kind = "bag"

    def __init__(self, counts):
        pairs = (list(counts.items()) if isinstance(counts, dict)
                 else [tuple(pair) for pair in counts])
        if not pairs:
            raise ValueError("a bag needs at least one color")
        names = [str(name) for name, _ in pairs]
        if len(set(names)) != len(names):
            raise ValueError(f"bag colors must be distinct: {names}")
        for name, count in pairs:
            if int(count) < 1:
                raise ValueError(f"count for {name} must be positive")
        self.counts = [(str(name), int(count)) for name, count in pairs]

    @property
    def colors(self):
        """Color names in the order the problem lists them."""
        return [name for name, _ in self.counts]

    colours = colors

    @property
    def total(self):
        """Number of objects in the bag."""
        return sum(count for _, count in self.counts)

    def code(self, name):
        """Printed code for a color: ``R`` when initials are distinct."""
        initials = [c[:1].upper() for c in self.colors]
        if len(set(initials)) == len(initials):
            return str(name)[:1].upper()
        return str(name)

    def outcomes(self):
        return [Outcome(self.code(name), (name,)) for name, _ in self.counts]

    def items(self):
        out = []
        for name, count in self.counts:
            for index in range(1, count + 1):
                out.append(Outcome(f"{self.code(name)}{index}", (name,)))
        return out

    def weighted(self):
        return WeightedSpace([(self.code(name), Fraction(count, self.total))
                              for name, count in self.counts])

    def key(self):
        return ("Bag", tuple(self.counts))

    def _inventory(self, item):
        return listing(f"{count} {name} {plural(item, count)}"
                       for name, count in self.counts)

    def _clause_bag(self):
        return ("one marble is drawn at random from a bag holding "
                f"{self._inventory('marble')}")

    def _clause_jar(self):
        return ("a counter is taken without looking from a jar of "
                f"{self._inventory('counter')}")

    def _clause_urn(self):
        return ("one ball is drawn at random from an urn containing "
                f"{self._inventory('ball')}")


class NumberedCards(Experiment):
    """Cards numbered ``start`` through ``start + count - 1``, ascending."""

    PHRASINGS = ("cards", "tickets", "tags")
    kind = "cards"

    def __init__(self, count, start=1):
        if count < 2:
            raise ValueError("need at least 2 cards")
        self.count = count
        self.start = start

    @property
    def high(self):
        """The largest number on a card."""
        return self.start + self.count - 1

    def outcomes(self):
        return [Outcome(v) for v in range(self.start, self.high + 1)]

    def key(self):
        return ("NumberedCards", self.start, self.count)

    def _clause_cards(self):
        return ("one card is drawn at random from cards numbered "
                f"{self.start} to {self.high}")

    def _clause_tickets(self):
        return ("a ticket is picked without looking from tickets numbered "
                f"{self.start} to {self.high}")

    def _clause_tags(self):
        return ("one tag is chosen at random from tags numbered "
                f"{self.start} to {self.high}")


class LetterTiles(Experiment):
    """Letter tiles spelling a word; one tile is drawn at random.

    Outcomes are the distinct letters in the order they first appear;
    ``items()`` is one tile per letter of the word (repeated letters are
    numbered ``I1, I2``), which is the equally likely space.
    """

    PHRASINGS = ("tiles", "letters", "word")
    kind = "tiles"

    def __init__(self, word):
        word = str(word).upper()
        if not word.isalpha() or len(word) < 2:
            raise ValueError(f"word must be 2+ letters: {word!r}")
        self.word = word

    def outcomes(self):
        seen = []
        for letter in self.word:
            if letter not in seen:
                seen.append(letter)
        return [Outcome(letter) for letter in seen]

    def items(self):
        out = []
        used = {}
        for letter in self.word:
            if self.word.count(letter) == 1:
                out.append(Outcome(letter, (letter,)))
            else:
                used[letter] = used.get(letter, 0) + 1
                out.append(Outcome(f"{letter}{used[letter]}", (letter,)))
        return out

    def weighted(self):
        return WeightedSpace([(o.label, Fraction(self.word.count(o.label),
                                                 len(self.word)))
                              for o in self.outcomes()])

    def key(self):
        return ("LetterTiles", self.word)

    def _clause_tiles(self):
        return f"one tile is drawn at random from tiles spelling {self.word}"

    def _clause_letters(self):
        return f"a letter is chosen at random from the letters of {self.word}"

    def _clause_word(self):
        return ("one lettered tile is picked without looking from the word "
                f"{self.word}")


class Menu(Experiment):
    """One choice per stage; outcomes join the choices with ' + '.

    ``Menu([('sandwich', ['ham', 'tuna']), ('drink', ['milk', 'juice'])])``
    enumerates ``ham + milk, ham + juice, tuna + milk, tuna + juice`` —
    stages in the order listed, options in the order printed.
    """

    PHRASINGS = ("menu", "combo", "order")
    kind = "menu"

    def __init__(self, stages):
        stages = [(str(name), [str(v) for v in options])
                  for name, options in stages]
        if len(stages) < 2:
            raise ValueError("a menu needs at least 2 stages")
        for name, options in stages:
            if len(options) < 1:
                raise ValueError(f"stage {name} has no options")
        self.stages = stages

    def stage_counts(self):
        """(stage name, number of options) pairs, for FCP steps."""
        return [(name, len(options)) for name, options in self.stages]

    def outcomes(self):
        pools = [options for _, options in self.stages]
        return [Outcome(product_label(combo, "plus"), combo)
                for combo in itertools.product(*pools)]

    def key(self):
        return ("Menu", tuple((n, tuple(o)) for n, o in self.stages))

    def _stage_text(self):
        return "; ".join(f"one {name} from {listing(options)}"
                         for name, options in self.stages)

    def _clause_menu(self):
        return f"a meal is chosen at random with {self._stage_text()}"

    def _clause_combo(self):
        return f"a combo is formed by choosing {self._stage_text()}"

    def _clause_order(self):
        return f"an order is made at random by picking {self._stage_text()}"


def product_label(parts, join="auto"):
    """Compound outcome label in the §3 dialect.

    ``concat`` gives ``H1`` / ``HH`` / ``RB``, ``pair`` gives ``(3, 4)``,
    ``plus`` gives ``ham + milk``. ``auto`` picks ``pair`` when every
    component is an integer and there are at least two of them, else
    ``concat``.
    """
    parts = [str(p) for p in parts]
    if join == "auto":
        join = ("pair" if len(parts) > 1 and all(INT_RE.fullmatch(p)
                                                 for p in parts)
                else "concat")
    if join == "concat":
        return "".join(parts)
    if join == "pair":
        return "(" + ", ".join(parts) + ")"
    if join == "plus":
        return " + ".join(parts)
    raise ValueError(f"join must be auto, concat, pair or plus: {join!r}")


def product_space(components, join="auto", use_items=False):
    """Outcomes of a compound experiment, in §3 enumeration order.

    Components may be experiments or plain outcome lists. Labels follow
    ``product_label``; the parts of the compound outcome are the flattened
    parts of its components, so the named predicates keep working.
    """
    pools = []
    for comp in components:
        if isinstance(comp, Experiment):
            pools.append(list(comp.items() if use_items else comp.outcomes()))
        else:
            pools.append([as_outcome(o) for o in comp])
    out = []
    for combo in itertools.product(*pools):
        label = product_label([o.label for o in combo], join)
        parts = tuple(p for o in combo for p in o.parts)
        out.append(Outcome(label, parts))
    return out


class Product(Experiment):
    """A compound experiment: several component experiments run in order.

    ``Product([Coin(), Spinner([1, 2, 3])])`` enumerates
    ``H1, H2, H3, T1, T2, T3``; ``Product([Die(), Die()])`` enumerates
    ``(1, 1), (1, 2), …``; ``Product([Coin(), Coin()])`` enumerates
    ``HH, HT, TH, TT``.
    """

    kind = "product"

    def __init__(self, components, join="auto"):
        components = list(components)
        if len(components) < 2:
            raise ValueError("a product needs at least 2 components")
        self.components = components
        self.join = join

    @property
    def PHRASINGS(self):
        """Phrasings of the first component (products mix styles)."""
        return self.components[0].PHRASINGS

    def outcomes(self):
        return product_space(self.components, self.join)

    def items(self):
        return product_space(self.components, self.join, use_items=True)

    def key(self):
        return ("Product", tuple(c.key() for c in self.components), self.join)

    def repeated(self):
        """True when every component is the same repeatable experiment."""
        first = self.components[0]
        return (first.REPEATABLE
                and all(c.key() == first.key() for c in self.components))

    def clause(self, style=None):
        if self.repeated():
            first = self.components[0]
            times = TIMES_WORDS[len(self.components)]
            return f"{first.clause(style)} {times}"
        if style is not None and not any(style in comp.PHRASINGS
                                         for comp in self.components):
            raise ValueError(f"no component has the phrasing {style!r}")
        return " and ".join(
            comp.clause(style if style in comp.PHRASINGS else None)
            for comp in self.components)


# ---------------------------------------------------------------------------
# Weighted spaces (P as a measure on atoms)
# ---------------------------------------------------------------------------


class WeightedSpace:
    """Atoms with Fraction weights: a probability measure on a finite set.

    ``measure`` adds the weights of an event, ``given`` renormalizes onto a
    conditioning event (conditioning as a renormalized measure), and
    ``validity_report`` produces the composite verdict the axioms generators
    answer with (``valid; sum = 1`` / ``invalid; sum = 9/8``).
    """

    def __init__(self, weights):
        pairs = (list(weights.items()) if isinstance(weights, dict)
                 else [tuple(pair) for pair in weights])
        if not pairs:
            raise ValueError("a weighted space needs at least one atom")
        self.atoms = [str(atom) for atom, _ in pairs]
        if len(set(self.atoms)) != len(self.atoms):
            raise ValueError(f"atoms must be distinct: {self.atoms}")
        self.weights = {str(atom): Fraction(w) for atom, w in pairs}

    @classmethod
    def uniform(cls, atoms):
        """Equally likely atoms."""
        atoms = [str(a) for a in atoms]
        return cls([(a, Fraction(1, len(atoms))) for a in atoms])

    @classmethod
    def from_counts(cls, counts):
        """Weights from counts: ``[('red', 3), ('blue', 5)]`` -> 3/8, 5/8."""
        pairs = (list(counts.items()) if isinstance(counts, dict)
                 else [tuple(pair) for pair in counts])
        total = sum(int(n) for _, n in pairs)
        return cls([(a, Fraction(int(n), total)) for a, n in pairs])

    def __len__(self):
        return len(self.atoms)

    def weight(self, atom):
        """Weight of one atom."""
        return self.weights[str(atom)]

    def total(self):
        """Sum of all weights (1 for a valid space)."""
        return sum(self.weights.values(), Fraction(0))

    def members(self, event):
        """Atoms in an event: a predicate, an iterable, or one atom label."""
        if callable(event):
            return [a for a in self.atoms if event(as_outcome(a))]
        if isinstance(event, (str, Outcome)):
            event = [event]
        wanted = {str(a) for a in event}
        unknown = wanted - set(self.atoms)
        if unknown:
            raise ValueError(f"not atoms of this space: {sorted(unknown)}")
        return [a for a in self.atoms if a in wanted]

    def measure(self, event):
        """P(event): the sum of its atoms' weights."""
        return sum((self.weights[a] for a in self.members(event)),
                   Fraction(0))

    def given(self, event):
        """The renormalized measure P(· given event) on the event's atoms."""
        members = self.members(event)
        mass = sum((self.weights[a] for a in members), Fraction(0))
        if mass == 0:
            raise ValueError("cannot condition on a probability-zero event")
        return WeightedSpace([(a, self.weights[a] / mass) for a in members])

    def is_valid(self):
        """True when weights are non-negative and sum to 1."""
        return self.total() == 1 and all(w >= 0 for w in self.weights.values())

    def validity_report(self):
        """Composite verdict: ``valid; sum = 1`` or the failing reason."""
        for atom in self.atoms:
            weight = self.weights[atom]
            if weight < 0:
                return f"invalid; P({atom}) = {prob_txt(weight)} < 0"
        total = self.total()
        if total != 1:
            return f"invalid; sum = {prob_txt(total)}"
        return "valid; sum = 1"

    def validate(self):
        """Raises unless the weights are a probability measure."""
        if not self.is_valid():
            raise ValueError(self.validity_report())
        return self

    def roster_text(self):
        """Roster of the atoms in enumeration order."""
        return roster(self.atoms)

    def event_roster(self, event):
        """Roster of an event's atoms."""
        return roster(self.members(event))

    def weight_lines(self, template="P({atom}) = {value}", sep="; "):
        """Weighted atoms in prose: ``P(a) = 1/10; P(b) = 1/5``."""
        return sep.join(
            template.format(atom=a, value=prob_txt(self.weights[a]))
            for a in self.atoms)


# ---------------------------------------------------------------------------
# Two-way tables (the ConditionalProbabilityGenerator prose form)
# ---------------------------------------------------------------------------


class TwoWayTable:
    """Counts cross-classified by two variables.

    ``cells_text`` renders the established prose form used (and parsed) by
    ``ConditionalProbabilityGenerator``: ``<row>=<v> and <col>=<w>: n``,
    cells joined with ``'; '``.
    """

    def __init__(self, row_name, row_values, col_name, col_values, cells):
        self.row_name = str(row_name)
        self.col_name = str(col_name)
        self.row_values = [str(v) for v in row_values]
        self.col_values = [str(v) for v in col_values]
        self.cells = {(str(r), str(c)): int(n) for (r, c), n in cells.items()}
        missing = [(r, c) for r in self.row_values for c in self.col_values
                   if (r, c) not in self.cells]
        if missing:
            raise ValueError(f"missing cells: {missing}")
        if self.grand_total() <= 0:
            raise ValueError("table total must be positive")

    @classmethod
    def random_counts(cls, row_name, row_values, col_name, col_values,
                      low=4, high=28):
        """A table with random cell counts (deterministic given ``random``)."""
        cells = {(str(r), str(c)): random.randint(low, high)
                 for r in row_values for c in col_values}
        return cls(row_name, row_values, col_name, col_values, cells)

    def count(self, row_value, col_value):
        """One cell count."""
        return self.cells[(str(row_value), str(col_value))]

    def row_total(self, row_value):
        """Total of one row."""
        return sum(self.count(row_value, c) for c in self.col_values)

    def col_total(self, col_value):
        """Total of one column."""
        return sum(self.count(r, col_value) for r in self.row_values)

    def grand_total(self):
        """Total of every cell."""
        return sum(self.cells.values())

    def cell_label(self, row_value, col_value):
        """``sport=yes and pet=yes`` — the joint-event label."""
        return (f"{self.row_name}={row_value} and "
                f"{self.col_name}={col_value}")

    def cells_text(self, order="row"):
        """Cells in prose, row-major by default, column-major on request."""
        if order == "row":
            pairs = [(r, c) for r in self.row_values for c in self.col_values]
        elif order == "column":
            pairs = [(r, c) for c in self.col_values for r in self.row_values]
        else:
            raise ValueError("order must be 'row' or 'column'")
        return "; ".join(f"{self.cell_label(r, c)}: {self.count(r, c)}"
                         for r, c in pairs)

    def sentence(self, subject="students", order="row"):
        """The table as one sentence of problem text."""
        return (f"A two-way table for {subject} has counts: "
                f"{self.cells_text(order)}.")

    def total_work(self, counts, total):
        """``12 + 18 = 30`` — the arithmetic for a TABLE_TOTAL step."""
        return " + ".join(str(n) for n in counts) + f" = {total}"

    def row_total_work(self, row_value):
        """TABLE_TOTAL work for one row."""
        counts = [self.count(row_value, c) for c in self.col_values]
        return self.total_work(counts, self.row_total(row_value))

    def col_total_work(self, col_value):
        """TABLE_TOTAL work for one column."""
        counts = [self.count(r, col_value) for r in self.row_values]
        return self.total_work(counts, self.col_total(col_value))

    def joint(self, row_value, col_value):
        """P(row=v and col=w)."""
        return Fraction(self.count(row_value, col_value), self.grand_total())

    def marginal_row(self, row_value):
        """P(row=v)."""
        return Fraction(self.row_total(row_value), self.grand_total())

    def marginal_col(self, col_value):
        """P(col=w)."""
        return Fraction(self.col_total(col_value), self.grand_total())

    def col_given_row(self, col_value, row_value):
        """P(col=w given row=v)."""
        return Fraction(self.count(row_value, col_value),
                        self.row_total(row_value))

    def row_given_col(self, row_value, col_value):
        """P(row=v given col=w)."""
        return Fraction(self.count(row_value, col_value),
                        self.col_total(col_value))

    def union(self, row_value, col_value):
        """P(row=v or col=w)."""
        hits = (self.row_total(row_value) + self.col_total(col_value)
                - self.count(row_value, col_value))
        return Fraction(hits, self.grand_total())

    def given_text(self, target, condition):
        """``P(pet=yes given sport=yes)`` — never a bar."""
        return given(target, condition)


__all__ = [
    "dec", "terminates", "exact", "prob_txt", "p4", "pct", "money",
    "odds_txt", "phi", "phi_table", "supplied_constant", "NP_BANK",
    "binomial_sigma", "is_perfect_square", "sqrt_fraction", "roster",
    "given", "leading_digit_round", "random",
    "VOWELS", "ORDINALS", "TIMES_WORDS", "plural", "listing",
    "Outcome", "as_outcome", "Predicate", "even", "odd", "vowel", "doubles",
    "multiple_of", "greater_than", "at_least", "less_than", "at_most",
    "colour", "color", "sum_equals", "at_least_one", "component",
    "Experiment", "Coin", "Die", "Spinner", "Bag", "NumberedCards",
    "LetterTiles", "Menu", "Product", "product_label", "product_space",
    "WeightedSpace", "TwoWayTable",
]
