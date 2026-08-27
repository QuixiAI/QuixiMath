"""Shared infrastructure for the applied-reasoning strand (``plans/applied_plan.md`` §4).

This module is to Strand M/N/J/L/R/D/G/X what ``prob_common.py`` is to the
probability strand: the single home of the pieces every applied generator
reuses, so that stories, distractors, estimates and scenarios look the same
everywhere and are policed by one conventions test.

What lives here
---------------
- ``CONTEXTS`` — the shared story bank (people, shops, trips, workshops,
  gardens, recipes, classrooms, sports, small businesses, labs) with names,
  items (units and hand-friendly price ranges), per-context phrase fragments
  and per-context distractor sentences.
- A **story-template engine**: a :class:`Template` is a set of typed
  :class:`Slot` s (ranges/constraints plus the human ``phrase`` the
  missing-information answer quotes), five or more surface
  :class:`Rendering` s (quantity-first, question-first, data-in-a-table, …),
  a canonical model string, and a solver returning ``(steps, answer)``.
  :func:`render_problem` renders one; :func:`inject_distractors` plants one or
  two irrelevant numbers and returns the matching ``SELECT_RELEVANT`` step;
  :func:`missing_answer` produces the canonical
  ``insufficient information; need <slot phrase>`` string.
- ``METHOD_WORDS`` — the banned-phrase list behind the strand's defining rule
  (the problem text names no method), with :func:`method_word_hits`.
- :func:`estimate_first` — wraps a step list with ``ESTIMATE`` first and
  ``ESTIMATE_CHECK`` immediately before ``Z`` (leading-digit rounding, so the
  estimate is deterministic).
- :func:`reject_step` — ``REJECT|candidate|reason`` for nonphysical roots,
  orientations and options.
- :class:`Scenario` — threads shared state through a list of sub-procedures,
  emits ``PART|k|<question>`` markers and assembles ``Q1 …; Q2 …``.
- One fully worked example template, :data:`WORK_RATE_TOGETHER` (the "two
  hoses" template of ``plans/applied_plan.md`` §5), exercising the engine end to
  end. No generator is registered here: generators declare their own
  templates in ``generators/`` and are wired up the usual three ways.

Answer rendering (``dec``/``exact``/``pct``/``money``) is re-exported from
``prob_common`` — one canonical rendering per shape across all four strands.
The oracle side (``tests/applied_oracle.py``) never imports this module: A9
requires the test to invert the templates by an independent route.
"""
import math
import random
import re
import string
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from helpers import step
from prob_common import (dec, exact, leading_digit_round, money, pct,
                         prob_txt, terminates)

# ---------------------------------------------------------------------------
# Rendering helpers (A0 plus the applied additions of plans/applied_plan.md §3)
# ---------------------------------------------------------------------------

#: Units that are symbols or compounds and never take a plural ``s``.
SYMBOL_UNITS = frozenset({
    "%", "$", "°", "km/h", "m/s", "mph", "km", "m", "cm", "mm", "kg", "g",
    "mg", "L", "mL", "m²", "cm²", "km²", "m³", "cm³", "h", "min", "s",
})


def _plural(word):
    """English plural for the simple nouns the context bank uses."""
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def num_txt(value):
    """Canonical number text for story data and answers: exact, minimal
    digits (``6``, ``1.5``, ``3/8`` when the fraction does not terminate)."""
    if isinstance(value, str):
        return value
    return exact(Fraction(value))


def frac_txt(value):
    """Lowest-terms fraction rendering used by rate steps: ``1/6``, ``3/2``,
    ``2``. (``prob_common.prob_txt`` under the applied strand's name.)"""
    return prob_txt(value)


def unit(value, name, plural=None):
    """A quantity with its unit, pluralised: ``unit(2, 'hour')`` -> ``'2
    hours'``; ``unit(48, 'km/h')`` -> ``'48 km/h'``; ``unit(1, 'tile')`` ->
    ``'1 tile'``."""
    text = num_txt(value)
    if name in SYMBOL_UNITS or "/" in name or not name[:1].isalpha():
        return f"{text} {name}"
    singular = isinstance(value, (int, float, Fraction)) and abs(Fraction(value)) == 1
    if singular or text == "1":
        return f"{text} {name}"
    return f"{text} {plural or _plural(name)}"


def cap(text):
    """Capitalises the first letter only (leaves 'hose A' -> 'Hose A')."""
    return text[:1].upper() + text[1:]


# ---------------------------------------------------------------------------
# The context bank (plans/applied_plan.md §3: contexts come from one shared bank)
# ---------------------------------------------------------------------------

NAMES = (
    "Ada", "Ana", "Ben", "Chi", "Dara", "Eli", "Fatima", "Gus", "Hana",
    "Ivan", "Jo", "Kofi", "Lena", "Leo", "Mia", "Milo", "Nadia", "Noor",
    "Omar", "Pia", "Quinn", "Rosa", "Sam", "Tariq", "Theo", "Uma", "Vik",
    "Wren", "Yara", "Zane",
)


@dataclass(frozen=True)
class Item:
    """A purchasable/measurable thing with a hand-friendly price range.

    Prices are held in whole cents on a ``step`` grid so every price divides
    well (plans/applied_plan.md §3: "prices in cents that divide well").
    """
    singular: str
    plural: str
    measure: str = ""          # "kg", "L", "" for countables
    price_lo: int = 100        # cents
    price_hi: int = 500        # cents
    price_step: int = 25       # cents

    def price(self, rng=random):
        """A price in dollars as a :class:`Fraction`, on the cent grid."""
        lo = self.price_lo // self.price_step
        hi = self.price_hi // self.price_step
        return Fraction(rng.randint(lo, hi) * self.price_step, 100)

    def count_text(self, n):
        """``3 notebooks`` / ``1 notebook``."""
        return unit(n, self.singular, self.plural)


@dataclass(frozen=True)
class Distractor:
    """An irrelevant number to plant in a story.

    ``sentence`` and ``label`` are format strings taking ``{value}``; the
    label is what the ``SELECT_RELEVANT`` step lists as ignored, so it always
    quotes the number exactly as the story shows it.
    """
    sentence: str
    label: str
    lo: int
    hi: int
    kind: str = "count"        # "count" | "money"
    grid: int = 1              # sampling grid (cents for money)

    def draw(self, rng=random):
        """Returns ``(sentence, label)`` for one freshly drawn value."""
        raw = rng.randint(self.lo // self.grid, self.hi // self.grid) * self.grid
        value = money(Fraction(raw, 100)) if self.kind == "money" else str(raw)
        return self.sentence.format(value=value), self.label.format(value=value)


@dataclass(frozen=True)
class Context:
    """One story world: where it happens, who is in it, what it sells or
    measures, which phrase fragments its templates may draw on, and which
    irrelevant numbers fit in it.

    ``fragments`` is deliberately open: the engine never interprets it, and
    templates document which keys they need. The key every modeling template
    uses so far is ``"work"`` — ``(device, verb, job_noun)`` triples such as
    ``("hose", "fill", "pool")``.
    """
    key: str
    label: str
    settings: Tuple[str, ...]
    agents: Tuple[str, ...]
    items: Tuple[Item, ...]
    fragments: Mapping[str, Tuple] = field(default_factory=dict)
    distractors: Tuple[Distractor, ...] = ()

    def item(self, rng=random):
        return rng.choice(self.items)

    def setting(self, rng=random):
        return rng.choice(self.settings)

    def agent(self, rng=random):
        return rng.choice(self.agents)

    def fragment(self, key, rng=random):
        return rng.choice(self.fragments[key])


CONTEXTS = {
    "people": Context(
        key="people", label="everyday life",
        settings=("the block party", "the corner of Maple Street",
                  "the community hall", "the front yard"),
        agents=("neighbour", "cousin", "friend", "flatmate"),
        items=(Item("apple", "apples", "", 50, 200),
               Item("paperback", "paperbacks", "", 500, 2000, 50),
               Item("bus ticket", "bus tickets", "", 150, 400)),
        fragments={
            "work": (("neighbour", "rake", "yard"),
                     ("cousin", "clear", "driveway"),
                     ("friend", "wash", "car")),
            "opener": ("On Saturday", "After lunch", "Before the rain"),
        },
        distractors=(
            Distractor("The house number is {value}.", "{value} house number", 12, 240),
            Distractor("The walk to the shops takes {value} minutes.",
                       "{value} minutes of walking", 5, 40),
            Distractor("There are {value} chairs on the porch.", "{value} chairs", 2, 12),
        ),
    ),
    "shop": Context(
        key="shop", label="a shop",
        settings=("the corner shop", "the campus store", "the market stall",
                  "the stationery aisle"),
        agents=("clerk", "shopper", "shopkeeper", "stocker"),
        items=(Item("notebook", "notebooks", "", 150, 400),
               Item("pencil pack", "pencil packs", "", 200, 500),
               Item("mug", "mugs", "", 300, 900),
               Item("tote bag", "tote bags", "", 400, 1200, 50)),
        fragments={
            "work": (("clerk", "restock", "shelf"),
                     ("scanner", "tag", "carton"),
                     ("packer", "pack", "order")),
            "opener": ("On a quiet morning", "Before opening", "During the rush"),
        },
        distractors=(
            Distractor("The shop has been open for {value} years.", "{value} years open", 2, 30),
            Distractor("There are {value} other items on the shelf.", "{value} other items", 3, 40),
            Distractor("The monthly rent is {value}.", "{value} rent", 80000, 200000, "money", 5000),
        ),
    ),
    "trip": Context(
        key="trip", label="a trip",
        settings=("the coast road", "the highway rest stop", "the ferry queue",
                  "the mountain pass"),
        agents=("driver", "passenger", "guide", "rider"),
        items=(Item("snack box", "snack boxes", "", 150, 500),
               Item("map", "maps", "", 200, 800),
               Item("litre of fuel", "litres of fuel", "L", 100, 200, 5)),
        fragments={
            "work": (("driver", "load", "van"),
                     ("crew", "unload", "trailer"),
                     ("ferry", "clear", "queue")),
            "opener": ("At dawn", "Just after the border", "Halfway through the day"),
        },
        distractors=(
            Distractor("The route passes {value} tunnels.", "{value} tunnels", 2, 9),
            Distractor("The car radio has {value} presets.", "{value} radio presets", 4, 18),
            Distractor("The toll for the bridge is {value}.", "{value} toll", 150, 900, "money", 25),
        ),
    ),
    "workshop": Context(
        key="workshop", label="a workshop",
        settings=("the school woodshop", "the repair bench", "the maker space",
                  "the back of the garage"),
        agents=("carpenter", "apprentice", "technician", "volunteer"),
        items=(Item("pine board", "pine boards", "m", 300, 1500, 25),
               Item("hinge", "hinges", "", 100, 400),
               Item("sandpaper sheet", "sandpaper sheets", "", 50, 200)),
        fragments={
            "work": (("sander", "sand", "floor"),
                     ("painter", "paint", "wall"),
                     ("cutter", "cut", "stack of boards")),
            "opener": ("Before the deadline", "On build night", "After the delivery"),
        },
        distractors=(
            Distractor("The bench is {value} cm wide.", "{value} cm of bench", 60, 240),
            Distractor("There are {value} clamps on the rack.", "{value} clamps", 3, 24),
            Distractor("A replacement blade costs {value}.", "{value} blade", 400, 3000, "money", 50),
        ),
    ),
    "garden": Context(
        key="garden", label="a garden",
        settings=("the community garden", "the allotment", "the back garden",
                  "the greenhouse"),
        agents=("gardener", "volunteer", "grower", "steward"),
        items=(Item("seed packet", "seed packets", "", 100, 350),
               Item("tomato plant", "tomato plants", "", 200, 600),
               Item("compost bag", "compost bags", "kg", 400, 1200, 50)),
        fragments={
            "work": (("hose", "fill", "pond"),
                     ("sprinkler", "water", "bed"),
                     ("pump", "empty", "rain barrel")),
            "opener": ("Early in the season", "After the frost", "On watering day"),
        },
        distractors=(
            Distractor("There are {value} rose bushes along the path.", "{value} rose bushes", 3, 24),
            Distractor("The fence is {value} m long.", "{value} m of fence", 12, 90),
            Distractor("A packet of bulbs costs {value}.", "{value} bulbs", 200, 900, "money", 25),
        ),
    ),
    "recipe": Context(
        key="recipe", label="a kitchen",
        settings=("the bakery kitchen", "the school canteen", "the home kitchen",
                  "the market cafe"),
        agents=("baker", "cook", "helper", "server"),
        items=(Item("kilogram of flour", "kilograms of flour", "kg", 100, 400, 25),
               Item("block of butter", "blocks of butter", "g", 200, 800, 25),
               Item("kilogram of sugar", "kilograms of sugar", "kg", 100, 350, 25)),
        fragments={
            "work": (("mixer", "mix", "batch of dough"),
                     ("oven", "bake", "tray of rolls"),
                     ("helper", "ice", "tray of buns")),
            "opener": ("Before service", "For the weekend order", "On bake day"),
        },
        distractors=(
            Distractor("The oven holds {value} trays.", "{value} trays", 2, 12),
            Distractor("The recipe card is {value} years old.", "{value} years", 2, 60),
            Distractor("A jar of jam costs {value}.", "{value} jam", 250, 900, "money", 25),
        ),
    ),
    "classroom": Context(
        key="classroom", label="a classroom",
        settings=("Room 12", "the library corner", "the science room",
                  "the after-school club"),
        agents=("teacher", "student", "librarian", "helper"),
        items=(Item("worksheet pack", "worksheet packs", "", 200, 600),
               Item("glue stick", "glue sticks", "", 75, 300, 25),
               Item("marker", "markers", "", 50, 250, 25)),
        fragments={
            "work": (("volunteer", "grade", "stack of quizzes"),
                     ("student", "sort", "box of books"),
                     ("printer", "print", "set of booklets")),
            "opener": ("Before the bell", "During free period", "On report day"),
        },
        distractors=(
            Distractor("There are {value} desks in the room.", "{value} desks", 12, 34),
            Distractor("The lesson lasts {value} minutes.", "{value} minutes of lesson", 35, 90, "count", 5),
            Distractor("The class trip costs {value} per student.", "{value} trip cost", 500, 3000, "money", 50),
        ),
    ),
    "sports": Context(
        key="sports", label="a sports club",
        settings=("the athletics track", "the club pitch", "the swimming pool",
                  "the training ground"),
        agents=("coach", "player", "groundskeeper", "timekeeper"),
        items=(Item("match ticket", "match tickets", "", 500, 3000, 50),
               Item("water bottle", "water bottles", "L", 200, 800, 25),
               Item("roll of grip tape", "rolls of grip tape", "m", 300, 900, 25)),
        fragments={
            "work": (("groundskeeper", "line", "pitch"),
                     ("roller", "roll", "outfield"),
                     ("hose", "fill", "pool")),
            "opener": ("Before the fixture", "On match day", "After training"),
        },
        distractors=(
            Distractor("The squad has {value} players.", "{value} players", 11, 30),
            Distractor("The stand seats {value} people.", "{value} seats", 200, 4000, "count", 50),
            Distractor("A season pass costs {value}.", "{value} season pass", 4000, 20000, "money", 500),
        ),
    ),
    "business": Context(
        key="business", label="a small business",
        settings=("the candle workshop", "the print studio", "the corner bakery",
                  "the market stand"),
        agents=("owner", "partner", "assistant", "supplier"),
        items=(Item("candle", "candles", "", 400, 1600, 50),
               Item("jam jar", "jam jars", "", 300, 900, 25),
               Item("printed tee", "printed tees", "", 800, 2400, 50)),
        fragments={
            "work": (("printer", "print", "batch of orders"),
                     ("packer", "pack", "day of orders"),
                     ("machine", "label", "run of jars")),
            "opener": ("In the first week", "Ahead of the fair", "On restock day"),
        },
        distractors=(
            Distractor("The stall has {value} shelves.", "{value} shelves", 2, 12),
            Distractor("The business is {value} months old.", "{value} months old", 4, 60),
            Distractor("The market fee is {value} per day.", "{value} market fee", 1000, 6000, "money", 250),
        ),
    ),
    "lab": Context(
        key="lab", label="a lab",
        settings=("the school lab", "the water-testing bench", "the field station",
                  "the prep room"),
        agents=("technician", "student", "researcher", "assistant"),
        items=(Item("test tube", "test tubes", "mL", 100, 500, 25),
               Item("pack of filter paper", "packs of filter paper", "", 200, 800, 25),
               Item("reagent bottle", "reagent bottles", "L", 600, 2400, 50)),
        fragments={
            "work": (("pump", "drain", "tank"),
                     ("filter", "clear", "sample batch"),
                     ("technician", "log", "tray of samples")),
            "opener": ("At the start of the session", "Before the readings",
                       "Once the samples arrive"),
        },
        distractors=(
            Distractor("The bench holds {value} racks.", "{value} racks", 2, 14),
            Distractor("The room is kept at {value} degrees.", "{value} degrees", 16, 24),
            Distractor("A box of gloves costs {value}.", "{value} gloves", 500, 2500, "money", 50),
        ),
    ),
}

CONTEXT_KEYS = tuple(CONTEXTS)


def context(key=None, rng=random):
    """One :class:`Context` by key, or a random one."""
    if key is None:
        key = rng.choice(CONTEXT_KEYS)
    return CONTEXTS[key]


def pick_name(rng=random):
    return rng.choice(NAMES)


# ---------------------------------------------------------------------------
# METHOD_WORDS — the strand's defining rule (plans/applied_plan.md §3)
# ---------------------------------------------------------------------------

#: Bare words that only ever appear when a procedure is being named.
FORMULA_WORDS = (
    "formula", "theorem", "algorithm", "method", "lemma", "corollary",
)

#: Named procedures, rules and skills.
NAMED_METHODS = (
    "pythagoras", "pythagorean", "bayes", "euclid", "l'hopital", "l'hôpital",
    "foil", "descartes", "cramer", "newton's", "gaussian elimination",
    "simpson's paradox", "regression to the mean", "square-cube law",
    "square cube law", "law of sines", "law of cosines",
    "law of large numbers", "law of total probability", "chain rule",
    "product rule", "quotient rule", "power rule", "zero product property",
    "distributive property", "order of operations", "pemdas", "bodmas",
    "completing the square", "complete the square", "synthetic division",
    "long division", "prime factorization", "prime factorisation",
    "least common multiple", "greatest common factor", "lcm", "gcf", "gcd",
    "discriminant", "combination", "permutation", "factorial", "n choose k",
    "binomial coefficient", "expected value", "harmonic mean",
    "closing speed", "dimensional analysis", "cross multiply",
    "cross-multiply", "cross multiplication", "substitution method",
    "elimination method", "unit rate", "unit price", "work rate",
    "work-rate", "interior angle sum",
)

#: Instruction phrases that hand the procedure to the reader.
INSTRUCTION_PHRASES = (
    "set up a proportion", "set up the proportion", "solve the proportion",
    "write a proportion", "use the rule", "using the rule", "apply the rule",
    "by the rule", "use proportional reasoning", "use the same rule",
)

#: Generator, variant and modifier names (they belong in ``operation``, never
#: in the story).
SKILL_NAMES = (
    "distractor", "estimate first", "estimate_first", "with model",
    "with_model", "scaffolded", "select relevant", "select_relevant",
    "missing information", "multi step word", "integer puzzle",
    "percent chain", "money life", "geometry in context", "systems word",
    "quadratic word", "growth comparison", "optimization in context",
    "rate of change", "mental strategy", "magnitude comparison",
    "rounding effect", "measurement uncertainty", "method discrimination",
    "assumption check", "qualitative reasoning", "plausibility critic",
    "risk communication", "statistical literacy", "index and growth",
    "decision under uncertainty", "representation translation",
    "formula derivation", "spatial packing", "spatial description",
)

#: The banned-phrase list scanned by ``tests/test_applied_conventions.py``.
METHOD_WORDS = tuple(sorted(set(
    FORMULA_WORDS + NAMED_METHODS + INSTRUCTION_PHRASES + SKILL_NAMES)))

#: Phrases a problem may state because they *supply* a tool the reader could
#: not otherwise know (a rounding rule, an approximation), the same exemption
#: the strand grants to supplied table values. They are removed before the
#: banned list is scanned.
ALLOWED_PHRASES = (
    "rule of 70",
    "significant figures",
    "significant figure",
)


def strip_allowed(text, extra=()):
    """Removes the supplied-tool phrases before a method-word scan."""
    lowered = text.lower()
    for phrase in tuple(ALLOWED_PHRASES) + tuple(extra):
        lowered = lowered.replace(phrase.lower(), " ")
    return lowered


def method_word_hits(text, extra_allowed=()):
    """Banned method phrases present in ``text`` (case-insensitive, after the
    supplied-tool allowances are stripped). Empty list means the text names no
    method — the rule every applied generator must satisfy."""
    lowered = strip_allowed(text, extra_allowed)
    return [phrase for phrase in METHOD_WORDS if phrase in lowered]


# ---------------------------------------------------------------------------
# Step helpers shared by every applied generator
# ---------------------------------------------------------------------------


def select_relevant_step(used, ignored=(), needed=()):
    """``SELECT_RELEVANT|used: 6 hours, 3 hours|ignored: $40 wage``.

    ``needed`` renders the missing-information form
    ``SELECT_RELEVANT|used: 3, $20|needed: the price of a notebook``; passing
    both puts ``ignored:`` first and ``needed:`` second (the
    ``extra_and_missing`` variant).
    """
    if isinstance(used, str):
        used = [used]
    if isinstance(ignored, str):
        ignored = [ignored]
    if isinstance(needed, str):
        needed = [needed]
    fields = [f"used: {', '.join(str(u) for u in used)}"]
    if ignored:
        fields.append(f"ignored: {', '.join(str(i) for i in ignored)}")
    if needed:
        fields.append(f"needed: {', '.join(str(n) for n in needed)}")
    return step("SELECT_RELEVANT", *fields)


def reject_step(candidate, reason):
    """``REJECT|t = -1|negative time`` — nonphysical roots, orientations and
    options are shown, not silently dropped (A2)."""
    return step("REJECT", candidate, reason)


def define_var_step(letter, meaning):
    """``DEFINE_VAR|b|Ben's age``."""
    return step("DEFINE_VAR", letter, meaning)


def model_eq_step(equation, source_phrase):
    """``MODEL_EQ|b + (2b + 3) = 27|together add to 27`` — the equation and
    the phrase in the story that licenses it."""
    return step("MODEL_EQ", equation, source_phrase)


def estimate_first(steps, exact_value, work, render=None):
    """Wraps a step list in the estimate-then-compute habit (DESIGN.md
    "Estimate-then-compute"): ``ESTIMATE|<rounding work>|<estimate>`` first
    and ``ESTIMATE_CHECK|<estimate>|<exact>|<verdict>`` immediately before
    ``Z``.

    The estimate is ``prob_common.leading_digit_round(exact_value)`` so it is
    deterministic. ``work`` is the human rounding line ("120 ÷ 1.5 ≈ 120 ÷
    2"); ``render`` formats both numbers (defaults to :func:`num_txt`, pass
    :func:`prob_common.money` for money answers). The answer is unchanged: a
    new list is returned and ``steps`` is not mutated.
    """
    render = render or num_txt
    value = Fraction(exact_value)
    est = leading_digit_round(value)
    est_txt, exact_txt = render(est), render(value)
    close = value == est or abs(value - est) * 2 <= abs(value)
    verdict = (f"{exact_txt} ≈ {est_txt} ✓" if close
               else f"{exact_txt} vs {est_txt}; estimate off, recheck")
    out = [step("ESTIMATE", work, est_txt)]
    check = step("ESTIMATE_CHECK", est_txt, exact_txt, verdict)
    steps = list(steps)
    if steps and steps[-1].split("|", 1)[0] == "Z":
        out.extend(steps[:-1])
        out.append(check)
        out.append(steps[-1])
    else:
        out.extend(steps)
        out.append(check)
    return out


# ---------------------------------------------------------------------------
# The story-template engine (plans/applied_plan.md §4)
# ---------------------------------------------------------------------------

MISSING_PREFIX = "insufficient information; need "


def missing_answer(slot, fields=None):
    """The canonical missing-information answer (plans/applied_plan.md §3, §9):
    ``insufficient information; need the price of a notebook``.

    Accepts a :class:`Slot` or a phrase. A slot phrase may be a format string
    over the story's fields ("the time the second {device} takes alone"), in
    which case pass the story's ``fields``.
    """
    phrase = slot.phrase if isinstance(slot, Slot) else str(slot)
    if fields:
        phrase = phrase.format(**fields)
    return MISSING_PREFIX + phrase


def with_model_answer(model, variable, value_text):
    """The ``with_model`` composite: ``1/6 + 1/3 = 1/t; t = 2 hours``."""
    return f"{model}; {variable} = {value_text}"


@dataclass(frozen=True)
class Slot:
    """One typed quantity in a story.

    ``phrase`` is the human name the missing-information answer quotes ("the
    price of a notebook"); it may be a format string over the story's fields
    ("the time the second {device} takes alone"). ``kind`` selects the
    rendering (``quantity`` with a unit, ``money``, ``percent``, ``count``,
    ``plain``).
    """
    name: str
    phrase: str
    unit: str = ""
    plural: str = ""
    kind: str = "quantity"

    def text(self, value):
        """The slot's value as it appears in the story: ``6 hours``,
        ``$2.50``, ``15%``, ``3 notebooks``."""
        if self.kind == "money":
            return money(value)
        if self.kind == "percent":
            return f"{num_txt(value)}%"
        if self.unit:
            return unit(value, self.unit, self.plural or None)
        return num_txt(value)


@dataclass(frozen=True)
class Line:
    """One sentence (``role='data'``/``'setup'``/``'question'``) or table row
    (``role='row'``) of a surface rendering.

    ``text`` is a format string over the story's fields; ``slots`` names the
    template slots it carries, so hiding a slot (missing-information records)
    drops exactly the lines that would have revealed it.
    """
    text: str
    slots: Tuple[str, ...] = ()
    role: str = "data"


@dataclass(frozen=True)
class Rendering:
    """One surface form of a template. ``row_intro`` introduces the table when
    the rendering has ``row`` lines ("Times to fill the pool alone —")."""
    key: str
    lines: Tuple[Line, ...]
    row_intro: str = ""


def _fields_in(fmt):
    """Format-field names referenced by a format string."""
    return {name for _, name, _, _ in string.Formatter().parse(fmt) if name}


@dataclass(frozen=True)
class Template:
    """A story template: slots, five or more surface renderings, a canonical
    model string, a solver and the metadata the conventions test reads.

    - ``sampler(rng) -> dict`` draws slot values (built backward from the
      exact answer, as the rest of the repo does).
    - ``scene(ctx, rng) -> dict`` supplies the non-numeric fields the
      renderings use (actors, verbs, places).
    - ``solver(values, fields) -> (steps, answer)`` is the canonical route,
      ending with ``Z|<answer>``.
    - ``model(values, fields) -> str`` is the canonical model equation used by
      the ``with_model`` modifier and by the ``MODEL_EQ`` step.
    """
    key: str
    slots: Tuple[Slot, ...]
    renderings: Tuple[Rendering, ...]
    sampler: Callable
    scene: Callable
    solver: Callable
    model: Callable
    variable: str = "x"
    answer_unit: str = ""
    contexts: Tuple[str, ...] = ()
    skills: Tuple[str, ...] = ()

    def __post_init__(self):
        names = {s.name for s in self.slots}
        if len(names) != len(self.slots):
            raise ValueError(f"{self.key}: duplicate slot names")
        if len(self.renderings) < 5:
            raise ValueError(
                f"{self.key}: {len(self.renderings)} renderings; the strand "
                "requires at least 5 (plans/applied_plan.md §3)")
        keys = {r.key for r in self.renderings}
        if len(keys) != len(self.renderings):
            raise ValueError(f"{self.key}: duplicate rendering keys")
        for rendering in self.renderings:
            questions = [ln for ln in rendering.lines if ln.role == "question"]
            if len(questions) != 1:
                raise ValueError(
                    f"{self.key}/{rendering.key}: exactly one question line "
                    f"required, found {len(questions)}")
            seen = set()
            for line in rendering.lines:
                declared = set(line.slots)
                if not declared <= names:
                    raise ValueError(
                        f"{self.key}/{rendering.key}: unknown slots "
                        f"{sorted(declared - names)}")
                referenced = _fields_in(line.text) & names
                if referenced != declared:
                    raise ValueError(
                        f"{self.key}/{rendering.key}: line references "
                        f"{sorted(referenced)} but declares {sorted(declared)}")
                seen |= declared
            if seen != names:
                raise ValueError(
                    f"{self.key}/{rendering.key}: rendering omits slots "
                    f"{sorted(names - seen)}")
            if any(ln.role == "row" for ln in rendering.lines) and not rendering.row_intro:
                raise ValueError(f"{self.key}/{rendering.key}: rows need a row_intro")
            if _fields_in(rendering.row_intro) & names:
                raise ValueError(
                    f"{self.key}/{rendering.key}: the row intro may not carry "
                    "slot values (they must sit on droppable rows)")
        for key in self.contexts:
            if key not in CONTEXTS:
                raise ValueError(f"{self.key}: unknown context {key!r}")

    def slot(self, name):
        for slot in self.slots:
            if slot.name == name:
                return slot
        raise KeyError(name)

    def rendering(self, key):
        for rendering in self.renderings:
            if rendering.key == key:
                return rendering
        raise KeyError(key)

    @property
    def rendering_keys(self):
        return tuple(r.key for r in self.renderings)

    def sample_values(self, rng=random):
        return self.sampler(rng)

    def supports_hiding(self, rendering, hidden):
        """True when every hidden slot sits on lines of its own, so dropping
        them removes the value without orphaning another slot."""
        hidden = set(hidden)
        if not hidden:
            return True
        dropped = False
        for line in rendering.lines:
            slots = set(line.slots)
            if slots & hidden:
                if slots - hidden:
                    return False
                dropped = True
        return dropped


@dataclass
class Story:
    """A rendered problem: its text, the values behind it, and enough
    provenance for the generator to build steps and for the tests to check
    them."""
    template: Template
    rendering: str
    context: Context
    values: Dict[str, object]
    fields: Dict[str, str]
    parts: List[Tuple[str, str]]
    hidden: Tuple[str, ...] = ()
    ignored: Tuple[str, ...] = ()

    @property
    def text(self):
        return " ".join(text for _, text in self.parts)

    @property
    def visible_slots(self):
        return tuple(s for s in self.template.slots if s.name not in self.hidden)

    def used_labels(self):
        """The story's relevant numbers, as the ``SELECT_RELEVANT`` step lists
        them: ``['6 hours', '3 hours']``."""
        return [s.text(self.values[s.name]) for s in self.visible_slots]

    def slot_phrase(self, name):
        """The slot's human phrase, resolved against this story's fields."""
        return self.template.slot(name).phrase.format(**self.fields)

    def missing_answer(self, name=None):
        """``insufficient information; need <slot phrase>`` for the hidden
        slot (or for ``name``)."""
        if name is None:
            if len(self.hidden) != 1:
                raise ValueError("name the slot: the story hides "
                                 f"{len(self.hidden)} slots")
            name = self.hidden[0]
        return MISSING_PREFIX + self.slot_phrase(name)

    def solve(self):
        """The canonical route: ``(steps, answer)``, ending with ``Z``."""
        return self.template.solver(self.values, self.fields)

    def model(self):
        """The canonical model string for the ``with_model`` modifier."""
        return self.template.model(self.values, self.fields)


def _assemble(row_intro, lines):
    """Joins rendered lines, collapsing consecutive ``row`` lines into one
    ``intro — a: 1; b: 2.`` segment."""
    parts = []
    rows = []
    for role, text in lines:
        if role == "row":
            rows.append(text)
            continue
        if rows:
            parts.append(("data", f"{row_intro} " + "; ".join(rows) + "."))
            rows = []
        parts.append((role, text))
    if rows:
        parts.append(("data", f"{row_intro} " + "; ".join(rows) + "."))
    return parts


def render_problem(template, values=None, ctx=None, rendering=None, hide=(),
                   rng=random):
    """Renders one problem from a template.

    ``hide`` names slots to leave out of the story (missing-information
    records); only renderings that can drop them cleanly are used. Returns a
    :class:`Story`.
    """
    if ctx is None:
        keys = template.contexts or CONTEXT_KEYS
        ctx = CONTEXTS[rng.choice(keys)]
    elif isinstance(ctx, str):
        ctx = CONTEXTS[ctx]
    if values is None:
        values = template.sample_values(rng)
    hide = tuple(hide)
    for name in hide:
        template.slot(name)  # KeyError on a typo
    if rendering is None:
        usable = [r for r in template.renderings
                  if template.supports_hiding(r, hide)]
        if not usable:
            raise ValueError(
                f"{template.key}: no rendering can hide {sorted(hide)}")
        rendering = rng.choice(usable)
    else:
        if isinstance(rendering, str):
            rendering = template.rendering(rendering)
        if not template.supports_hiding(rendering, hide):
            raise ValueError(
                f"{template.key}/{rendering.key} cannot hide {sorted(hide)}")

    fields = dict(template.scene(ctx, rng))
    for slot in template.slots:
        fields[slot.name] = slot.text(values[slot.name])
    lines = [(line.role, line.text.format(**fields))
             for line in rendering.lines
             if not (set(line.slots) & set(hide))]
    return Story(template=template, rendering=rendering.key, context=ctx,
                 values=dict(values), fields=fields,
                 parts=_assemble(rendering.row_intro.format(**fields), lines),
                 hidden=hide)


def inject_distractors(story, count=1, rng=random):
    """Plants ``count`` (1 or 2) irrelevant numbers in the story and returns
    ``(new_story, select_relevant_step)``.

    The sentences go in just before the question, so the story still ends with
    what it asks. Values that would collide with a number already in the text
    are redrawn, so the ``ignored`` field names exactly one number of the
    problem. The answer is unchanged (plans/applied_plan.md §3).
    """
    if not 1 <= count <= 2:
        raise ValueError("distractor count must be 1 or 2")
    pool = list(story.context.distractors)
    if len(pool) < count:
        raise ValueError(f"context {story.context.key} has too few distractors")
    rng.shuffle(pool)
    text = story.text
    sentences, labels = [], []
    for distractor in pool:
        if len(sentences) == count:
            break
        for _ in range(12):
            sentence, label = distractor.draw(rng)
            numbers = set(_number_strings(label))
            if numbers and not (numbers & set(_number_strings(text))):
                sentences.append(sentence)
                labels.append(label)
                text = f"{text} {sentence}"
                break
    if len(sentences) != count:
        raise ValueError(f"could not place {count} distractors without a clash")

    parts = list(story.parts)
    where = next((i for i, (role, _) in enumerate(parts) if role == "question"),
                 len(parts))
    for offset, sentence in enumerate(sentences):
        parts.insert(where + offset, ("data", sentence))
    new_story = replace(story, parts=parts, ignored=tuple(labels))
    return new_story, select_relevant_step(story.used_labels(), ignored=labels)


_NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _number_strings(text):
    """Number tokens of a string, comma-separators removed."""
    return [m.group(0).replace(",", "") for m in _NUMBER_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Scenario harness (Strand X)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Part:
    """One sub-question of a scenario.

    ``solve(state) -> (steps, answer_text)``; ``state`` is a plain dict shared
    by every part, so later parts read what earlier ones wrote (the scenario's
    thread of meaning). ``question`` is the short label of the ``PART`` marker
    and ``skills`` names the procedures this part composes.
    """
    question: str
    solve: Callable
    key: str = ""
    skills: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ScenarioResult:
    steps: List[str]
    answer: str
    state: Dict[str, object]
    questions: Tuple[str, ...]
    skills: Optional[List[str]] = None


class Scenario:
    """Threads shared state through a list of :class:`Part` s, emitting
    ``PART|k|<question>`` before each and assembling the composite answer
    ``Q1 …; Q2 …`` (plans/applied_plan.md §4, §5 Strand X).

    ``skills`` is optional record metadata: the union of the parts' skills in
    order, or an explicit list. ``validate_example`` ignores extra keys, so a
    generator may attach it to its record as ``skills=result.skills``.
    """

    def __init__(self, parts, skills=None):
        self.parts = tuple(parts)
        if not self.parts:
            raise ValueError("a scenario needs at least one part")
        self._skills = list(skills) if skills is not None else None

    @property
    def skills(self):
        if self._skills is not None:
            return list(self._skills)
        out = []
        for part in self.parts:
            for skill in part.skills:
                if skill not in out:
                    out.append(skill)
        return out or None

    def run(self, state=None):
        """Runs every part in order. Returns a :class:`ScenarioResult` whose
        ``steps`` end with ``Z|<composite answer>``."""
        shared = dict(state or {})
        steps, answers = [], []
        for index, part in enumerate(self.parts, start=1):
            steps.append(step("PART", index, part.question))
            part_steps, value = part.solve(shared)
            steps.extend(part_steps)
            value = str(value)
            answers.append(f"Q{index} {value}")
            shared[f"q{index}"] = value
            if part.key:
                shared[part.key] = value
        answer = "; ".join(answers)
        steps.append(step("Z", answer))
        return ScenarioResult(steps=steps, answer=answer, state=shared,
                              questions=tuple(p.question for p in self.parts),
                              skills=self.skills)


# ---------------------------------------------------------------------------
# Worked example: the "two hoses" work-rate template (plans/applied_plan.md §5)
# ---------------------------------------------------------------------------
# Kept here so the engine is exercised end to end by tests/test_applied_common
# and tests/applied_oracle. WorkRateGenerator (Phase 1) will import it; this
# module registers no generator.


def _work_rate_pairs(max_hours=36):
    """``(slow, fast)`` hour pairs whose together-time is a whole or half
    hour — built backward from the exact answer, so the scratchpad never needs
    a calculator."""
    pairs = []
    for fast in range(2, max_hours + 1):
        for slow in range(fast + 1, max_hours + 1):
            together = Fraction(slow * fast, slow + fast)
            if together >= 1 and (together * 2).denominator == 1:
                pairs.append((slow, fast))
    return tuple(pairs)


#: Hand-friendly (slow, fast) hour pairs for the work-rate template.
WORK_RATE_PAIRS = _work_rate_pairs()


def _work_rate_sample(rng=random):
    slow, fast = rng.choice(WORK_RATE_PAIRS)
    return {"a_hours": slow, "b_hours": fast}


def _work_rate_scene(ctx, rng=random):
    device, verb, job_noun = ctx.fragment("work", rng)
    return {
        "device": device,
        "verb": verb,
        "job_noun": job_noun,
        "first": f"{device} A",
        "second": f"{device} B",
        "first_cap": cap(f"{device} A"),
        "second_cap": cap(f"{device} B"),
        "name": pick_name(rng),
        "place": ctx.setting(rng),
        "opener": ctx.fragment("opener", rng),
    }


def _work_rate_together(values):
    """The exact together-time in hours."""
    return 1 / (Fraction(1, int(values["a_hours"])) + Fraction(1, int(values["b_hours"])))


def _work_rate_model(values, fields):
    return f"1/{int(values['a_hours'])} + 1/{int(values['b_hours'])} = 1/t"


def _work_rate_solve(values, fields):
    """Canonical route: each worker's rate, add the rates over a common
    denominator, then divide one whole job by the combined rate."""
    a, b = int(values["a_hours"]), int(values["b_hours"])
    job = fields.get("job_noun", "job")
    rate_a, rate_b = Fraction(1, a), Fraction(1, b)
    total = rate_a + rate_b
    lcd = a * b // math.gcd(a, b)
    na, nb = lcd // a, lcd // b
    time = 1 / total
    answer = unit(time, "hour")
    steps = [
        step("RATE", fields.get("first", "worker A"), f"1/{a} {job} per hour"),
        step("RATE", fields.get("second", "worker B"), f"1/{b} {job} per hour"),
        step("L", a, b, lcd),
        step("C", f"1/{a}", f"{na}/{lcd}"),
        step("C", f"1/{b}", f"{nb}/{lcd}"),
        step("A", f"{na}/{lcd}", f"{nb}/{lcd}", f"{na + nb}/{lcd}"),
        step("RATE_SUM", f"1/{a} + 1/{b}", frac_txt(total)),
        step("MODEL_EQ", f"({frac_txt(total)}) · t = 1", f"one whole {job}"),
        step("D", 1, frac_txt(total), num_txt(time)),
        step("CHECK", "work_done",
             f"{frac_txt(time * rate_a)} + {frac_txt(time * rate_b)}", "1"),
        step("Z", answer),
    ]
    return steps, answer


WORK_RATE_TOGETHER = Template(
    key="work_rate_together",
    slots=(
        Slot("a_hours", "the time the first {device} takes alone", unit="hour"),
        Slot("b_hours", "the time the second {device} takes alone", unit="hour"),
    ),
    renderings=(
        Rendering("quantity_first", (
            Line("{first_cap} alone can {verb} the {job_noun} in {a_hours}.",
                 ("a_hours",)),
            Line("{second_cap} alone can {verb} it in {b_hours}.", ("b_hours",)),
            Line("Working together, how long do they take to {verb} the "
                 "{job_noun}?", (), "question"),
        )),
        Rendering("question_first", (
            Line("How long do {first} and {second} take to {verb} the "
                 "{job_noun} together?", (), "question"),
            Line("{first_cap} alone takes {a_hours}.", ("a_hours",)),
            Line("{second_cap} alone takes {b_hours}.", ("b_hours",)),
        )),
        Rendering("table", (
            Line("{first}: {a_hours}", ("a_hours",), "row"),
            Line("{second}: {b_hours}", ("b_hours",), "row"),
            Line("With both working at once, how long does it take?", (),
                 "question"),
        ), row_intro="Times to {verb} the {job_noun} alone —"),
        Rendering("narrative", (
            Line("{opener} at {place}, {name} starts {first} and {second} "
                 "at the same moment.", (), "setup"),
            Line("{first_cap} would need {a_hours} alone.", ("a_hours",)),
            Line("{second_cap} would need {b_hours} alone.", ("b_hours",)),
            Line("How long until the {job_noun} is done?", (), "question"),
        )),
        Rendering("comparison", (
            Line("It takes {a_hours} for {first} to {verb} the {job_noun}.",
                 ("a_hours",)),
            Line("{second_cap} needs only {b_hours} for the same job.",
                 ("b_hours",)),
            Line("Running both together, how long does the job take?", (),
                 "question"),
        )),
    ),
    sampler=_work_rate_sample,
    scene=_work_rate_scene,
    solver=_work_rate_solve,
    model=_work_rate_model,
    variable="t",
    answer_unit="hours",
    contexts=CONTEXT_KEYS,
    skills=("unit_rate", "fraction_addition", "reciprocal_solve"),
)

#: Every template Phase 0 ships. Generators keep their own registries.
TEMPLATES = (WORK_RATE_TOGETHER,)


__all__ = [
    # rendering
    "dec", "exact", "terminates", "pct", "money", "leading_digit_round",
    "num_txt", "frac_txt", "unit", "cap", "SYMBOL_UNITS",
    # context bank
    "NAMES", "Item", "Distractor", "Context", "CONTEXTS", "CONTEXT_KEYS",
    "context", "pick_name",
    # no-method-words rule
    "METHOD_WORDS", "FORMULA_WORDS", "NAMED_METHODS", "INSTRUCTION_PHRASES",
    "SKILL_NAMES", "ALLOWED_PHRASES", "strip_allowed", "method_word_hits",
    # step helpers
    "select_relevant_step", "reject_step", "define_var_step",
    "model_eq_step", "estimate_first",
    # template engine
    "Slot", "Line", "Rendering", "Template", "Story", "render_problem",
    "inject_distractors", "missing_answer", "with_model_answer",
    "MISSING_PREFIX",
    # scenarios
    "Part", "Scenario", "ScenarioResult",
    # worked example
    "WORK_RATE_PAIRS", "WORK_RATE_TOGETHER", "TEMPLATES",
]
