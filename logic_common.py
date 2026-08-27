"""Propositional-logic toolkit shared by the foundations strand.

Everything the logic generators need to *build* and *print* formulas lives
here (``plans/foundations_plan.md`` §3 and §4). The matching *checking* route —
an independent recursive-descent parser and brute-force evaluators — lives in
``tests/foundations_oracle.py`` and never imports this module (A9).

Contents
--------
- AST: :class:`Var`, :class:`Const` (``TRUE``/``FALSE``), :class:`Not`,
  :class:`And`, :class:`Or`, :class:`Imp`, :class:`Iff`, :class:`Xor`,
  :class:`Nand`, plus :class:`Meta` (pattern metavariables).
- Canonical printer :func:`render` in three surface dialects
  (:data:`PROPOSITIONAL`, :data:`SET`, :data:`CIRCUIT`).
- Random formula builder :func:`random_formula`.
- Semantics: :func:`evaluate`, :func:`assignments`, :func:`truth_table`,
  :func:`truth_column`, :func:`equivalent`, :func:`classify`.
- Normal forms: :func:`to_nnf`, :func:`to_cnf`, :func:`to_dnf` and their
  canonical clause-set variants.
- :func:`substitute` (uniform substitution), :func:`to_polish` /
  :func:`from_polish` (Łukasiewicz notation).
- A law-rewriting engine: :data:`LAWS`, :func:`simplify`, :func:`obfuscate`.

Notation (canonical, `plans/foundations_plan.md` §3)
----------------------------------------------
Connectives ``¬ ∧ ∨ → ↔ ⊕`` with NAND written ``↑``; precedence
``¬`` > ``∧`` > ``∨`` > ``→`` > ``↔``; **every binary subformula except the
outermost one is parenthesized**, so ``(p ∧ ¬q) → r`` is the only spelling of
that formula.  ASCII ``|`` never appears anywhere in this module's output.
"""
import random as _random_module

# ---------------------------------------------------------------------------
# Variable alphabets
# ---------------------------------------------------------------------------

PROP_VARS = ("p", "q", "r", "s")
ALT_VARS = ("a", "b", "c")
SET_VARS = ("A", "B", "C")
ALPHABETS = {"pqrs": PROP_VARS, "abc": ALT_VARS, "ABC": SET_VARS}

#: Precedence of the canonical connectives (higher binds tighter). The printer
#: fully parenthesizes, so this table documents the parser contract that
#: ``tests/foundations_oracle.py`` implements independently.
PRECEDENCE = {"¬": 5, "∧": 4, "↑": 4, "∨": 3, "⊕": 3, "→": 2, "↔": 1}


# ---------------------------------------------------------------------------
# AST
# ---------------------------------------------------------------------------


class Formula(object):
    """Base class for propositional formulas (immutable, hashable)."""

    __slots__ = ()

    def _key(self):
        raise NotImplementedError

    def __eq__(self, other):
        return isinstance(other, Formula) and self._key() == other._key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return "<%s>" % render(self)

    def __str__(self):
        return render(self)


class Const(Formula):
    """A truth constant: ``TRUE`` prints ``T``, ``FALSE`` prints ``F``."""

    __slots__ = ("value",)

    def __init__(self, value):
        object.__setattr__(self, "value", bool(value))

    def _key(self):
        return ("const", self.value)


class Var(Formula):
    """A propositional variable, e.g. ``Var("p")``."""

    __slots__ = ("name",)

    def __init__(self, name):
        object.__setattr__(self, "name", str(name))

    def _key(self):
        return ("var", self.name)


class Meta(Formula):
    """A pattern metavariable — matches any subformula in a law pattern."""

    __slots__ = ("name",)

    def __init__(self, name):
        object.__setattr__(self, "name", str(name))

    def _key(self):
        return ("meta", self.name)


class Not(Formula):
    """Negation ``¬A``."""

    __slots__ = ("arg",)
    symbol = "¬"

    def __init__(self, arg):
        object.__setattr__(self, "arg", arg)

    def _key(self):
        return ("not", self.arg._key())


class Binary(Formula):
    """Base class of the binary connectives."""

    __slots__ = ("left", "right")
    symbol = "?"

    def __init__(self, left, right):
        object.__setattr__(self, "left", left)
        object.__setattr__(self, "right", right)

    def _key(self):
        return (self.symbol, self.left._key(), self.right._key())


class And(Binary):
    """Conjunction ``A ∧ B``."""

    __slots__ = ()
    symbol = "∧"


class Or(Binary):
    """Disjunction ``A ∨ B``."""

    __slots__ = ()
    symbol = "∨"


class Imp(Binary):
    """Material implication ``A → B``."""

    __slots__ = ()
    symbol = "→"


class Iff(Binary):
    """Biconditional ``A ↔ B``."""

    __slots__ = ()
    symbol = "↔"


class Xor(Binary):
    """Exclusive disjunction ``A ⊕ B``."""

    __slots__ = ()
    symbol = "⊕"


class Nand(Binary):
    """Sheffer stroke ``A ↑ B`` (never the ASCII bar)."""

    __slots__ = ()
    symbol = "↑"


TRUE = Const(True)
FALSE = Const(False)

BINARY_CLASSES = (And, Or, Imp, Iff, Xor, Nand)
CONNECTIVE_BY_SYMBOL = {cls.symbol: cls for cls in BINARY_CLASSES}
CONNECTIVE_BY_SYMBOL["¬"] = Not


def _children(node):
    if isinstance(node, Not):
        return (node.arg,)
    if isinstance(node, Binary):
        return (node.left, node.right)
    return ()


def _rebuild(node, children):
    if isinstance(node, Not):
        return Not(children[0])
    if isinstance(node, Binary):
        return type(node)(children[0], children[1])
    return node


# ---------------------------------------------------------------------------
# Surface dialects
# ---------------------------------------------------------------------------


class Dialect(object):
    """One surface syntax for the same AST.

    ``symbols`` maps a binary class to its infix spelling, ``negation`` is
    either ``("prefix", "¬")`` or ``("postfix", "ᶜ")``, and ``law_names``
    renames a law for this dialect (set algebra says "complement" where
    propositional logic says "negation").
    """

    def __init__(self, name, symbols, negation, true_text, false_text,
                 law_names=None):
        self.name = name
        self.symbols = symbols
        self.negation = negation
        self.true_text = true_text
        self.false_text = false_text
        self.law_names = dict(law_names or {})

    def __repr__(self):
        return "<Dialect %s>" % self.name


PROPOSITIONAL = Dialect(
    "propositional",
    {And: "∧", Or: "∨", Imp: "→", Iff: "↔", Xor: "⊕", Nand: "↑"},
    ("prefix", "¬"),
    "T",
    "F",
)

SET = Dialect(
    "set",
    {And: "∩", Or: "∪"},
    ("postfix", "ᶜ"),
    "U",
    "∅",
    law_names={"negation": "complement"},
)

CIRCUIT = Dialect(
    "circuit",
    {And: "AND", Or: "OR", Xor: "XOR", Nand: "NAND"},
    ("prefix", "NOT "),
    "1",
    "0",
    law_names={"negation": "complement"},
)

DIALECTS = {"propositional": PROPOSITIONAL, "set": SET, "circuit": CIRCUIT}


def render(formula, dialect=PROPOSITIONAL, var_map=None):
    """Canonical text for ``formula``.

    Every binary subformula except the outermost is parenthesized::

        >>> render(Imp(And(Var("p"), Not(Var("q"))), Var("r")))
        '(p ∧ ¬q) → r'

    ``var_map`` renames variables on the way out (``{"p": "A"}``), which is how
    the same law rewrite is shown in the set or circuit dialect.
    """
    return _render(formula, True, dialect, var_map or {})


def _render(node, top, dialect, var_map):
    if isinstance(node, Const):
        return dialect.true_text if node.value else dialect.false_text
    if isinstance(node, Var):
        return var_map.get(node.name, node.name)
    if isinstance(node, Meta):
        return var_map.get(node.name, node.name)
    if isinstance(node, Not):
        inner = _render(node.arg, False, dialect, var_map)
        kind, mark = dialect.negation
        return mark + inner if kind == "prefix" else inner + mark
    if isinstance(node, Binary):
        symbol = dialect.symbols.get(type(node))
        if symbol is None:
            raise ValueError("dialect %s has no symbol for %s"
                             % (dialect.name, type(node).__name__))
        text = "%s %s %s" % (_render(node.left, False, dialect, var_map),
                             symbol,
                             _render(node.right, False, dialect, var_map))
        return text if top else "(" + text + ")"
    raise TypeError("not a formula: %r" % (node,))


def law_label(name, dialect=PROPOSITIONAL):
    """Dialect-specific display name of a law (``negation`` → ``complement``)."""
    return dialect.law_names.get(name, name)


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------


def variables(formula):
    """Sorted tuple of the variable names occurring in ``formula``."""
    found = set()

    def walk(node):
        if isinstance(node, Var):
            found.add(node.name)
        for child in _children(node):
            walk(child)

    walk(formula)
    return tuple(sorted(found))


def metavariables(pattern):
    """Sorted tuple of metavariable names in a law pattern."""
    found = set()

    def walk(node):
        if isinstance(node, Meta):
            found.add(node.name)
        for child in _children(node):
            walk(child)

    walk(pattern)
    return tuple(sorted(found))


def depth(formula):
    """Connective depth: atoms are 0, ``¬p`` is 1, ``(p ∧ q) → r`` is 2."""
    kids = _children(formula)
    if not kids:
        return 0
    return 1 + max(depth(child) for child in kids)


_formula_depth = depth  # module-level alias (``depth`` is shadowed below)


def size(formula):
    """Number of nodes in the AST."""
    return 1 + sum(size(child) for child in _children(formula))


def main_connective(formula):
    """Symbol of the outermost connective, or ``None`` for an atom."""
    if isinstance(formula, Not):
        return "¬"
    if isinstance(formula, Binary):
        return formula.symbol
    return None


def subformulas(formula):
    """Distinct subformulas (atoms and the formula itself included).

    Ordered by node count, then canonical text — a stable, printable order.
    """
    seen = {}

    def walk(node):
        seen[node] = True
        for child in _children(node):
            walk(child)

    walk(formula)
    return sorted(seen, key=lambda f: (size(f), render(f)))


# ---------------------------------------------------------------------------
# Semantics
# ---------------------------------------------------------------------------

_BINARY_EVAL = {
    And: lambda a, b: a and b,
    Or: lambda a, b: a or b,
    Imp: lambda a, b: (not a) or b,
    Iff: lambda a, b: a == b,
    Xor: lambda a, b: a != b,
    Nand: lambda a, b: not (a and b),
}


def evaluate(formula, assignment):
    """Truth value of ``formula`` under ``assignment`` (name -> bool)."""
    if isinstance(formula, Const):
        return formula.value
    if isinstance(formula, Var):
        try:
            return bool(assignment[formula.name])
        except KeyError:
            raise KeyError("no value for variable %r" % formula.name)
    if isinstance(formula, Meta):
        raise ValueError("cannot evaluate a pattern metavariable")
    if isinstance(formula, Not):
        return not evaluate(formula.arg, assignment)
    if isinstance(formula, Binary):
        return _BINARY_EVAL[type(formula)](
            evaluate(formula.left, assignment),
            evaluate(formula.right, assignment))
    raise TypeError("not a formula: %r" % (formula,))


def assignments(names):
    """Truth-table rows for ``names``: alphabetical order, ``T`` before ``F``.

    Two variables give the textbook order ``TT, TF, FT, FF``.
    """
    ordered = tuple(sorted(names))
    rows = []
    total = 1 << len(ordered)
    for index in range(total):
        row = {}
        for position, name in enumerate(ordered):
            bit = (index >> (len(ordered) - 1 - position)) & 1
            row[name] = (bit == 0)
        rows.append(row)
    return rows


def truth_table(formula, names=None):
    """List of ``(assignment, value)`` pairs in canonical row order."""
    names = tuple(sorted(names)) if names is not None else variables(formula)
    return [(row, evaluate(formula, row)) for row in assignments(names)]


def truth_column(formula, names=None):
    """The result column as one string, e.g. ``'TFTT'``."""
    return "".join("T" if value else "F"
                   for _, value in truth_table(formula, names))


def row_text(assignment):
    """``{'p': True, 'q': False}`` -> ``'p=T, q=F'`` (alphabetical)."""
    return ", ".join("%s=%s" % (name, "T" if assignment[name] else "F")
                     for name in sorted(assignment))


def column_text(values):
    """Bool sequence -> ``'TFTT'``."""
    return "".join("T" if value else "F" for value in values)


def _shared_names(*formulas):
    names = set()
    for formula in formulas:
        names.update(variables(formula))
    return tuple(sorted(names))


def equivalent(first, second):
    """True when the two formulas have the same column over their shared vars."""
    return first_difference(first, second) is None


def first_difference(first, second):
    """First assignment (canonical row order) where the two differ, else None."""
    names = _shared_names(first, second)
    for row in assignments(names):
        if evaluate(first, row) != evaluate(second, row):
            return row
    return None


def is_tautology(formula):
    """True when every row is T."""
    return all(value for _, value in truth_table(formula))


def is_contradiction(formula):
    """True when every row is F."""
    return not any(value for _, value in truth_table(formula))


def classify(formula):
    """``'tautology'``, ``'contradiction'`` or ``'contingency'``."""
    values = [value for _, value in truth_table(formula)]
    if all(values):
        return "tautology"
    if not any(values):
        return "contradiction"
    return "contingency"


def models(formula):
    """Assignments making ``formula`` true, in canonical row order."""
    return [row for row, value in truth_table(formula) if value]


# ---------------------------------------------------------------------------
# Substitution
# ---------------------------------------------------------------------------


def substitute(formula, mapping):
    """Uniform substitution: replace every ``Var`` named in ``mapping``.

    The replacement is simultaneous — ``substitute(Iff(p, q), {"p": q,
    "q": p})`` swaps the two variables rather than collapsing them.
    """
    if isinstance(formula, Var):
        return mapping.get(formula.name, formula)
    kids = _children(formula)
    if not kids:
        return formula
    return _rebuild(formula, [substitute(child, mapping) for child in kids])


def rename(formula, name_map):
    """Rename variables (``{"p": "a"}``) without changing structure."""
    return substitute(formula, {old: Var(new) for old, new in name_map.items()})


# ---------------------------------------------------------------------------
# Normal forms
# ---------------------------------------------------------------------------


def remove_derived(formula):
    """Rewrite ``↑``, ``↔``, ``⊕`` and ``→`` away, children first.

    ``A ↑ B`` -> ``¬(A ∧ B)``; ``A ↔ B`` -> ``(A → B) ∧ (B → A)``;
    ``A ⊕ B`` -> ``(A ∨ B) ∧ ¬(A ∧ B)``; ``A → B`` -> ``¬A ∨ B``.
    """
    kids = _children(formula)
    if kids:
        formula = _rebuild(formula, [remove_derived(k) for k in kids])
    if isinstance(formula, Nand):
        return Not(And(formula.left, formula.right))
    if isinstance(formula, Iff):
        left, right = formula.left, formula.right
        return And(Or(Not(left), right), Or(Not(right), left))
    if isinstance(formula, Xor):
        left, right = formula.left, formula.right
        return And(Or(left, right), Not(And(left, right)))
    if isinstance(formula, Imp):
        return Or(Not(formula.left), formula.right)
    return formula


def to_nnf(formula):
    """Negation normal form: only ``∧``, ``∨`` and negated atoms.

    Step 1 removes the derived connectives (:func:`remove_derived`), step 2
    pushes every ``¬`` inward with double negation and De Morgan.
    """
    return _push_negations(remove_derived(formula), False)


def _push_negations(node, negated):
    if isinstance(node, Const):
        return Const(not node.value) if negated else node
    if isinstance(node, (Var, Meta)):
        return Not(node) if negated else node
    if isinstance(node, Not):
        return _push_negations(node.arg, not negated)
    if isinstance(node, And):
        left = _push_negations(node.left, negated)
        right = _push_negations(node.right, negated)
        return Or(left, right) if negated else And(left, right)
    if isinstance(node, Or):
        left = _push_negations(node.left, negated)
        right = _push_negations(node.right, negated)
        return And(left, right) if negated else Or(left, right)
    raise ValueError("call remove_derived first: %s" % render(node))


def evaluate_constants(formula):
    """Fold ``T``/``F`` away with the identity, domination and negation laws."""
    kids = _children(formula)
    if kids:
        formula = _rebuild(formula, [evaluate_constants(k) for k in kids])
    if isinstance(formula, Not) and isinstance(formula.arg, Const):
        return Const(not formula.arg.value)
    if isinstance(formula, And):
        left, right = formula.left, formula.right
        if left == FALSE or right == FALSE:
            return FALSE
        if left == TRUE:
            return right
        if right == TRUE:
            return left
    if isinstance(formula, Or):
        left, right = formula.left, formula.right
        if left == TRUE or right == TRUE:
            return TRUE
        if left == FALSE:
            return right
        if right == FALSE:
            return left
    return formula


def _distribute(formula, outer, inner):
    """Distribute ``outer`` over ``inner`` at the leftmost-outermost redex.

    For CNF ``outer`` is :class:`Or` and ``inner`` is :class:`And`: the redex
    is the first node in pre-order (node, then left subtree, then right
    subtree) that is an ``outer`` with an ``inner`` child; the left child is
    tried first, so ``(a ∧ b) ∨ c`` becomes ``(a ∨ c) ∧ (b ∨ c)`` and
    ``a ∨ (b ∧ c)`` becomes ``(a ∨ b) ∧ (a ∨ c)``.  Repeat to a fixed point.
    """
    while True:
        target = _first_distribution_site(formula, outer, inner)
        if target is None:
            return formula
        path, node = target
        if isinstance(node.left, inner):
            new = inner(outer(node.left.left, node.right),
                        outer(node.left.right, node.right))
        else:
            new = inner(outer(node.left, node.right.left),
                        outer(node.left, node.right.right))
        formula = replace_at(formula, path, new)


def _first_distribution_site(node, outer, inner, path=()):
    if isinstance(node, outer) and (isinstance(node.left, inner)
                                    or isinstance(node.right, inner)):
        return path, node
    for index, child in enumerate(_children(node)):
        found = _first_distribution_site(child, outer, inner, path + (index,))
        if found is not None:
            return found
    return None


def to_cnf(formula):
    """Conjunctive normal form by the stated distribution order.

    1. :func:`remove_derived` (children first), 2. :func:`to_nnf`,
    3. distribute ``∨`` over ``∧`` at the leftmost-outermost redex until none
    remains.  No literals or clauses are dropped — see :func:`canonical_cnf`
    for the deduplicated form.
    """
    return _distribute(to_nnf(formula), Or, And)


def to_dnf(formula):
    """Disjunctive normal form, dual to :func:`to_cnf` (``∧`` over ``∨``)."""
    return _distribute(to_nnf(formula), And, Or)


def _collect(node, cls):
    if isinstance(node, cls):
        return _collect(node.left, cls) + _collect(node.right, cls)
    return [node]


def _fold(parts, cls, empty):
    if not parts:
        return empty
    out = parts[0]
    for part in parts[1:]:
        out = cls(out, part)
    return out


def _literal_key(literal):
    if isinstance(literal, Not):
        return (render(literal.arg), 1)
    return (render(literal), 0)


def cnf_clauses(formula):
    """CNF as a canonical tuple of clauses (tuples of literals).

    Literals inside a clause are sorted by variable then polarity (positive
    first); duplicate literals and duplicate clauses are dropped; clauses
    holding a variable and its negation are dropped (they are ``T``); clauses
    are ordered by length, then by text.
    """
    return _clause_sets(to_cnf(formula), And, Or)


def dnf_terms(formula):
    """DNF as a canonical tuple of terms — dual of :func:`cnf_clauses`."""
    return _clause_sets(to_dnf(formula), Or, And)


def _clause_sets(normal, outer, inner):
    groups = []
    for group in _collect(normal, outer):
        literals = []
        for literal in _collect(group, inner):
            if literal not in literals:
                literals.append(literal)
        if any(Not(lit) in literals for lit in literals):
            continue
        literals.sort(key=_literal_key)
        clause = tuple(literals)
        if clause not in groups:
            groups.append(clause)
    groups.sort(key=lambda c: (len(c), tuple(render(l) for l in c)))
    return tuple(groups)


def canonical_cnf(formula):
    """CNF rebuilt from :func:`cnf_clauses`, left-associated."""
    clauses = cnf_clauses(formula)
    if not clauses:
        return TRUE
    return _fold([_fold(list(c), Or, FALSE) for c in clauses], And, TRUE)


def canonical_dnf(formula):
    """DNF rebuilt from :func:`dnf_terms`, left-associated."""
    terms = dnf_terms(formula)
    if not terms:
        return FALSE
    return _fold([_fold(list(t), And, TRUE) for t in terms], Or, FALSE)


# ---------------------------------------------------------------------------
# Polish (Łukasiewicz) notation
# ---------------------------------------------------------------------------

POLISH_LETTERS = {Not: "N", And: "K", Or: "A", Imp: "C", Iff: "E",
                  Xor: "J", Nand: "D"}
POLISH_CLASSES = {letter: cls for cls, letter in POLISH_LETTERS.items()}
POLISH_TRUE = "1"
POLISH_FALSE = "0"


def to_polish(formula):
    """Prefix (Łukasiewicz) spelling: ``N K A C E`` plus ``J`` (⊕), ``D`` (↑).

    Variables must be lowercase — the uppercase letters are the operators.
    Constants are written ``1`` and ``0``.
    """
    if isinstance(formula, Const):
        return POLISH_TRUE if formula.value else POLISH_FALSE
    if isinstance(formula, (Var, Meta)):
        name = formula.name
        if not name.islower():
            raise ValueError("Polish notation needs lowercase variables, "
                             "got %r" % name)
        return name
    if isinstance(formula, Not):
        return "N" + to_polish(formula.arg)
    if isinstance(formula, Binary):
        return (POLISH_LETTERS[type(formula)] + to_polish(formula.left)
                + to_polish(formula.right))
    raise TypeError("not a formula: %r" % (formula,))


def from_polish(text):
    """Inverse of :func:`to_polish`; spaces are ignored."""
    tokens = [ch for ch in text if not ch.isspace()]
    formula, rest = _parse_polish(tokens, 0)
    if rest != len(tokens):
        raise ValueError("trailing symbols in Polish formula: %r" % text)
    return formula


def _parse_polish(tokens, index):
    if index >= len(tokens):
        raise ValueError("Polish formula ended early")
    token = tokens[index]
    if token == POLISH_TRUE:
        return TRUE, index + 1
    if token == POLISH_FALSE:
        return FALSE, index + 1
    if token == "N":
        arg, index = _parse_polish(tokens, index + 1)
        return Not(arg), index
    if token in POLISH_CLASSES:
        cls = POLISH_CLASSES[token]
        left, index = _parse_polish(tokens, index + 1)
        right, index = _parse_polish(tokens, index)
        return cls(left, right), index
    if token.isalpha() and token.islower():
        return Var(token), index + 1
    raise ValueError("unexpected Polish symbol %r" % token)


# ---------------------------------------------------------------------------
# Random formulas
# ---------------------------------------------------------------------------

ALL_CONNECTIVES = ("¬", "∧", "∨", "→", "↔", "⊕", "↑")
BASIC_CONNECTIVES = ("¬", "∧", "∨", "→", "↔")


def random_formula(depth=2, names=PROP_VARS, connectives=BASIC_CONNECTIVES,
                   rng=None, constants=False, exact_depth=False,
                   use_all=False, attempts=200):
    """A random formula of connective depth at most ``depth``.

    ``names`` is the variable alphabet (:data:`PROP_VARS`, :data:`ALT_VARS`,
    :data:`SET_VARS`, ...), ``connectives`` the allowed symbols.  With
    ``exact_depth`` the depth is exactly ``depth``; with ``use_all`` every
    variable in ``names`` occurs at least once (retried up to ``attempts``
    times).
    """
    rng = rng or _random_module
    names = tuple(names)
    if not names:
        raise ValueError("need at least one variable name")
    binaries = [CONNECTIVE_BY_SYMBOL[symbol] for symbol in connectives
                if symbol != "¬"]
    allow_not = "¬" in connectives
    if not binaries and not allow_not:
        raise ValueError("need at least one connective")

    def leaf():
        if constants and rng.random() < 0.1:
            return TRUE if rng.random() < 0.5 else FALSE
        return Var(rng.choice(names))

    def build(level, forced, top=False):
        if level <= 0:
            return leaf()
        if not forced and not top and rng.random() < 0.15:
            return leaf()
        if allow_not and (not binaries or rng.random() < 0.25):
            return Not(build(level - 1, exact_depth))
        cls = rng.choice(binaries)
        deep = rng.random() < 0.5
        left = build(level - 1 if deep else rng.randint(0, level - 1),
                     exact_depth and deep)
        right = build(level - 1 if not deep else rng.randint(0, level - 1),
                      exact_depth and not deep)
        return cls(left, right)

    for _ in range(attempts):
        formula = build(depth, exact_depth, top=True)
        if use_all and set(variables(formula)) != set(names):
            continue
        if exact_depth and _formula_depth(formula) != depth:
            continue
        return formula
    raise ValueError("could not build a formula meeting the constraints")


# ---------------------------------------------------------------------------
# Positions, pattern matching, law table
# ---------------------------------------------------------------------------


def positions(formula):
    """``(path, node)`` for every subformula, in pre-order.

    A path is a tuple of child indices; ``()`` is the whole formula.
    """
    out = [((), formula)]
    for index, child in enumerate(_children(formula)):
        for path, node in positions(child):
            out.append(((index,) + path, node))
    return out


def node_at(formula, path):
    """The subformula at ``path``."""
    node = formula
    for index in path:
        node = _children(node)[index]
    return node


def replace_at(formula, path, new):
    """Copy of ``formula`` with the subformula at ``path`` replaced."""
    if not path:
        return new
    kids = list(_children(formula))
    kids[path[0]] = replace_at(kids[path[0]], path[1:], new)
    return _rebuild(formula, kids)


def match(pattern, node, bindings=None):
    """Match a law pattern against a formula.

    Returns the metavariable bindings (a dict) or ``None``.  Metavariables
    match any subformula and must match consistently.
    """
    bindings = {} if bindings is None else dict(bindings)
    if isinstance(pattern, Meta):
        bound = bindings.get(pattern.name)
        if bound is None:
            bindings[pattern.name] = node
            return bindings
        return bindings if bound == node else None
    if isinstance(pattern, Const):
        return bindings if pattern == node else None
    if isinstance(pattern, Var):
        return bindings if pattern == node else None
    if type(pattern) is not type(node):
        return None
    kids_p = _children(pattern)
    kids_n = _children(node)
    if len(kids_p) != len(kids_n):
        return None
    for sub_p, sub_n in zip(kids_p, kids_n):
        bindings = match(sub_p, sub_n, bindings)
        if bindings is None:
            return None
    return bindings


def instantiate(pattern, bindings, fresh=None):
    """Build a formula from ``pattern`` and metavariable ``bindings``.

    ``fresh(name)`` supplies a subformula for a metavariable the left side did
    not bind — needed when a law is applied backwards (the inverse of
    absorption introduces a brand new ``B``).
    """
    if isinstance(pattern, Meta):
        if pattern.name in bindings:
            return bindings[pattern.name]
        if fresh is None:
            raise KeyError("unbound metavariable %r" % pattern.name)
        value = fresh(pattern.name)
        bindings[pattern.name] = value
        return value
    kids = _children(pattern)
    if not kids:
        return pattern
    return _rebuild(pattern, [instantiate(k, bindings, fresh) for k in kids])


class Rule(object):
    """One directed pattern pair of a law (``lhs`` -> ``rhs``)."""

    __slots__ = ("law", "key", "lhs", "rhs")

    def __init__(self, law, key, lhs, rhs):
        self.law = law
        self.key = key
        self.lhs = lhs
        self.rhs = rhs

    def flipped(self):
        """The same pattern pair read right-to-left (used by obfuscation)."""
        return Rule(self.law, self.key + "_inverse", self.rhs, self.lhs)

    def __repr__(self):
        return "<Rule %s: %s -> %s>" % (self.key, render(self.lhs),
                                        render(self.rhs))


class Law(object):
    """A named law: a display name plus its ordered pattern pairs."""

    __slots__ = ("name", "rules")

    def __init__(self, name, pairs):
        self.name = name
        self.rules = tuple(Rule(name, key, lhs, rhs)
                           for key, lhs, rhs in pairs)

    def __repr__(self):
        return "<Law %s (%d rules)>" % (self.name, len(self.rules))


_A = Meta("A")
_B = Meta("B")
_C = Meta("C")

#: The law table.  Each entry is stored in its *simplifying* direction; the
#: inverse direction is what :func:`obfuscate` applies.
LAWS = {}
LAW_TABLE = (
    Law("double negation", (
        ("double_negation", Not(Not(_A)), _A),
    )),
    Law("De Morgan", (
        ("de_morgan_and", Not(And(_A, _B)), Or(Not(_A), Not(_B))),
        ("de_morgan_or", Not(Or(_A, _B)), And(Not(_A), Not(_B))),
    )),
    Law("negation", (
        ("negation_and", And(_A, Not(_A)), FALSE),
        ("negation_and_left", And(Not(_A), _A), FALSE),
        ("negation_or", Or(_A, Not(_A)), TRUE),
        ("negation_or_left", Or(Not(_A), _A), TRUE),
    )),
    Law("idempotent", (
        ("idempotent_and", And(_A, _A), _A),
        ("idempotent_or", Or(_A, _A), _A),
    )),
    Law("domination", (
        ("domination_or", Or(_A, TRUE), TRUE),
        ("domination_or_left", Or(TRUE, _A), TRUE),
        ("domination_and", And(_A, FALSE), FALSE),
        ("domination_and_left", And(FALSE, _A), FALSE),
    )),
    Law("identity", (
        ("identity_and", And(_A, TRUE), _A),
        ("identity_and_left", And(TRUE, _A), _A),
        ("identity_or", Or(_A, FALSE), _A),
        ("identity_or_left", Or(FALSE, _A), _A),
    )),
    Law("absorption", (
        ("absorption_and", And(_A, Or(_A, _B)), _A),
        ("absorption_and_left", And(Or(_A, _B), _A), _A),
        ("absorption_or", Or(_A, And(_A, _B)), _A),
        ("absorption_or_left", Or(And(_A, _B), _A), _A),
    )),
    Law("distributive", (
        ("distributive_and_over_or", Or(And(_A, _B), And(_A, _C)),
         And(_A, Or(_B, _C))),
        ("distributive_or_over_and", And(Or(_A, _B), Or(_A, _C)),
         Or(_A, And(_B, _C))),
    )),
    Law("implication elimination", (
        ("implication_elimination", Imp(_A, _B), Or(Not(_A), _B)),
    )),
    Law("biconditional elimination", (
        ("biconditional_elimination", Iff(_A, _B),
         And(Imp(_A, _B), Imp(_B, _A))),
    )),
    Law("contrapositive", (
        ("contrapositive", Imp(_A, _B), Imp(Not(_B), Not(_A))),
    )),
)
for _law in LAW_TABLE:
    LAWS[_law.name] = _law
LAW_NAMES = tuple(law.name for law in LAW_TABLE)

#: Forward order for a full propositional simplification.  Laws are tried in
#: this order and the first match wins, so the rewrite sequence is forced.
#: ``contrapositive`` is deliberately absent: it is an involution and would
#: never terminate as a forward rule.
DEFAULT_LAW_ORDER = (
    "biconditional elimination",
    "implication elimination",
    "double negation",
    "De Morgan",
    "negation",
    "idempotent",
    "domination",
    "identity",
    "absorption",
    "distributive",
)

#: Forward order for the ``∧ ∨ ¬`` fragment — the set-algebra and circuit
#: dialects, which have no ``→`` or ``↔``.
SET_LAW_ORDER = (
    "double negation",
    "De Morgan",
    "negation",
    "idempotent",
    "domination",
    "identity",
    "absorption",
    "distributive",
)


class Rewrite(object):
    """One law application.

    The first three attributes are the ``(law name, before, after)`` triple of
    the *redex*; ``whole_before``/``whole_after`` are the complete formulas, so
    a generator can emit ``LAW|De Morgan|¬(p ∧ q)|¬p ∨ ¬q`` followed by
    ``REWRITE|<whole_after>``.
    """

    __slots__ = ("law", "before", "after", "rule", "path", "whole_before",
                 "whole_after")

    def __init__(self, law, before, after, rule, path, whole_before,
                 whole_after):
        self.law = law
        self.before = before
        self.after = after
        self.rule = rule
        self.path = path
        self.whole_before = whole_before
        self.whole_after = whole_after

    def triple(self, dialect=PROPOSITIONAL):
        """``(law name, before text, after text)`` in the given dialect."""
        return (law_label(self.law, dialect), render(self.before, dialect),
                render(self.after, dialect))

    def __iter__(self):
        return iter((self.law, self.before, self.after))

    def __repr__(self):
        return "<Rewrite %s: %s -> %s>" % (self.law, render(self.before),
                                           render(self.after))


def apply_rule(formula, rule, fresh=None):
    """Apply ``rule`` at the leftmost-outermost redex; ``None`` if it misses."""
    for path, node in positions(formula):
        bindings = match(rule.lhs, node)
        if bindings is None:
            continue
        try:
            new = instantiate(rule.rhs, dict(bindings), fresh)
        except KeyError:
            continue
        if new == node:
            continue
        return Rewrite(rule.law, node, new, rule, path,
                       formula, replace_at(formula, path, new))
    return None


def rewrite_once(formula, order=DEFAULT_LAW_ORDER):
    """The single forced rewrite of ``formula``, or ``None`` if it is done.

    Laws are tried in ``order``; inside a law its pattern pairs are tried in
    the order they are listed; the redex is the leftmost-outermost match.
    """
    for name in order:
        for rule in LAWS[name].rules:
            done = apply_rule(formula, rule)
            if done is not None:
                return done
    return None


def simplify(formula, order=DEFAULT_LAW_ORDER, target=None, max_steps=64):
    """Rewrite to a fixed point, returning the list of :class:`Rewrite` steps.

    Stops early when ``target`` is reached, when no law applies, when a
    formula repeats, or after ``max_steps`` rewrites.
    """
    steps = []
    seen = {formula}
    current = formula
    while len(steps) < max_steps:
        if target is not None and current == target:
            break
        done = rewrite_once(current, order)
        if done is None:
            break
        steps.append(done)
        current = done.whole_after
        if current in seen:
            break
        seen.add(current)
    return steps


def simplified(formula, order=DEFAULT_LAW_ORDER, target=None, max_steps=64):
    """The formula :func:`simplify` lands on."""
    steps = simplify(formula, order, target, max_steps)
    return steps[-1].whole_after if steps else formula


class ObfuscationError(ValueError):
    """Raised when no verified obfuscation was found within the attempts."""


def obfuscate(target, steps=3, order=DEFAULT_LAW_ORDER, rng=None, pool=None,
              attempts=60):
    """Apply inverse laws to ``target`` so that simplifying comes back.

    Each of the ``steps`` moves picks a random inverse of a rule belonging to
    a law in ``order`` and applies it at a random redex; free metavariables on
    the way back (the inverse of absorption invents a ``B``) are drawn from
    ``pool``.  The result is verified: :func:`simplify` with the same ``order``
    must land exactly on ``target``, otherwise another obfuscation is tried.
    """
    rng = rng or _random_module
    if pool is None:
        names = variables(target) or ("p",)
        alphabet = PROP_VARS
        for candidate in ALPHABETS.values():
            if set(names) <= set(candidate):
                alphabet = candidate
                break
        pool = [Var(name) for name in alphabet]
    pool = list(pool)
    inverses = [rule.flipped() for name in order
                for rule in LAWS[name].rules]

    def fresh(_name):
        return rng.choice(pool)

    for _ in range(attempts):
        current = target
        ok = True
        for _ in range(steps):
            options = []
            for rule in inverses:
                for path, node in positions(current):
                    if match(rule.lhs, node) is not None:
                        options.append((rule, path, node))
            if not options:
                ok = False
                break
            rng.shuffle(options)
            applied = False
            for rule, path, node in options:
                bindings = match(rule.lhs, node)
                try:
                    new = instantiate(rule.rhs, dict(bindings), fresh)
                except KeyError:
                    continue
                if new == node or size(new) > 40:
                    continue
                current = replace_at(current, path, new)
                applied = True
                break
            if not applied:
                ok = False
                break
        if not ok or current == target:
            continue
        if simplified(current, order, target=target) == target:
            return current
    raise ObfuscationError(
        "no verified obfuscation of %s after %d attempts"
        % (render(target), attempts))
