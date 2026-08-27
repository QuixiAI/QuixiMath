"""Independent checking route for the foundations strand (A9).

Nothing here may import ``logic_common`` or ``set_common``: every routine is
written from the printed dialect and solved by brute force, so a generator
agreeing with this module is real verification rather than self-agreement.

Contents
--------
- A recursive-descent parser for the printed formula dialect
  (:func:`parse_formula`), its canonical printer (:func:`render`), brute-force
  semantics (:func:`truth_column`, :func:`equivalent`, :func:`classify`) and a
  Łukasiewicz parser (:func:`parse_polish`).
- Parsers for the set dialect: rosters, pairs, partitions, nested sets,
  set-builder predicates, and set expressions (``∪ ∩ − Δ ᶜ ×``) with a
  membership-table evaluator.
- Ordinals in Cantor normal form with exponents below ω: :func:`parse_ordinal`
  and :class:`Ordinal` arithmetic.
- Brute-force relation and poset routines (closures, covers, bounds, linear
  extensions, equivalence classes).

ASTs are plain tuples: ``("var", "p")``, ``("const", True)``,
``("not", x)``, ``("and", x, y)``, ``("or", x, y)``, ``("imp", x, y)``,
``("iff", x, y)``, ``("xor", x, y)``, ``("nand", x, y)``.
"""
import itertools
import re
from fractions import Fraction

# ---------------------------------------------------------------------------
# Formula parsing
# ---------------------------------------------------------------------------

NOT = "¬"
AND = "∧"
OR = "∨"
IMP = "→"
IFF = "↔"
XOR = "⊕"
NAND = "↑"

BINARY_OPS = {AND: "and", OR: "or", IMP: "imp", IFF: "iff", XOR: "xor",
              NAND: "nand"}
OP_SYMBOL = {"and": AND, "or": OR, "imp": IMP, "iff": IFF, "xor": XOR,
             "nand": NAND}

_NAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


class ParseError(ValueError):
    """Raised when a string is not in the canonical dialect."""


def _tokenize_formula(text):
    tokens = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace():
            index += 1
            continue
        if char in "()" or char in BINARY_OPS or char == NOT:
            tokens.append(char)
            index += 1
            continue
        match = _NAME_RE.match(text, index)
        if match:
            tokens.append(match.group(0))
            index = match.end()
            continue
        raise ParseError("unexpected character %r at position %d in %r"
                         % (char, index, text))
    return tokens


class _FormulaParser(object):
    """Grammar (``¬`` > ``∧``/``↑`` > ``∨``/``⊕`` > ``→`` > ``↔``)::

        iff   := imp (↔ imp)*
        imp   := disj (→ imp)?          # right associative
        disj  := conj ((∨ | ⊕) conj)*
        conj  := unary ((∧ | ↑) unary)*
        unary := ¬ unary | atom
        atom  := name | T | F | ( iff )
    """

    def __init__(self, tokens, text):
        self.tokens = tokens
        self.text = text
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        token = self.peek()
        if token is None:
            raise ParseError("formula ended early: %r" % self.text)
        self.pos += 1
        return token

    def expect(self, token):
        got = self.take()
        if got != token:
            raise ParseError("expected %r, found %r in %r"
                             % (token, got, self.text))

    def parse(self):
        node = self.iff()
        if self.peek() is not None:
            raise ParseError("trailing text %r in %r"
                             % (self.peek(), self.text))
        return node

    def iff(self):
        node = self.imp()
        while self.peek() == IFF:
            self.take()
            node = ("iff", node, self.imp())
        return node

    def imp(self):
        node = self.disj()
        if self.peek() == IMP:
            self.take()
            return ("imp", node, self.imp())
        return node

    def disj(self):
        node = self.conj()
        while self.peek() in (OR, XOR):
            op = BINARY_OPS[self.take()]
            node = (op, node, self.conj())
        return node

    def conj(self):
        node = self.unary()
        while self.peek() in (AND, NAND):
            op = BINARY_OPS[self.take()]
            node = (op, node, self.unary())
        return node

    def unary(self):
        if self.peek() == NOT:
            self.take()
            return ("not", self.unary())
        return self.atom()

    def atom(self):
        token = self.take()
        if token == "(":
            node = self.iff()
            self.expect(")")
            return node
        if token == "T":
            return ("const", True)
        if token == "F":
            return ("const", False)
        if _NAME_RE.fullmatch(token):
            return ("var", token)
        raise ParseError("unexpected token %r in %r" % (token, self.text))


def parse_formula(text):
    """Parse a printed propositional formula into the oracle AST."""
    return _FormulaParser(_tokenize_formula(text), text).parse()


def render(node, top=True):
    """Canonical printing: every binary subformula but the outermost is
    parenthesized (an independent re-implementation of the §3 convention)."""
    kind = node[0]
    if kind == "var":
        return node[1]
    if kind == "const":
        return "T" if node[1] else "F"
    if kind == "not":
        return NOT + render(node[1], False)
    text = "%s %s %s" % (render(node[1], False), OP_SYMBOL[kind],
                         render(node[2], False))
    return text if top else "(" + text + ")"


def is_canonical_formula(text):
    """True when ``text`` is exactly the canonical printing of what it parses
    to (full parenthesization, single spaces)."""
    try:
        return render(parse_formula(text)) == text.strip()
    except ParseError:
        return False


# ---------------------------------------------------------------------------
# Formula semantics (brute force)
# ---------------------------------------------------------------------------


def formula_variables(node):
    """Sorted tuple of variable names in the AST."""
    found = set()

    def walk(item):
        if item[0] == "var":
            found.add(item[1])
        elif item[0] == "not":
            walk(item[1])
        elif item[0] != "const":
            walk(item[1])
            walk(item[2])

    walk(node)
    return tuple(sorted(found))


def all_assignments(names):
    """Rows in the textbook order: alphabetical variables, ``T`` before ``F``."""
    names = tuple(sorted(names))
    rows = []
    for bits in itertools.product([True, False], repeat=len(names)):
        rows.append(dict(zip(names, bits)))
    return rows


def eval_formula(node, assignment):
    """Truth value of the AST under ``assignment``."""
    kind = node[0]
    if kind == "const":
        return node[1]
    if kind == "var":
        return bool(assignment[node[1]])
    if kind == "not":
        return not eval_formula(node[1], assignment)
    left = eval_formula(node[1], assignment)
    right = eval_formula(node[2], assignment)
    if kind == "and":
        return left and right
    if kind == "or":
        return left or right
    if kind == "imp":
        return (not left) or right
    if kind == "iff":
        return left == right
    if kind == "xor":
        return left != right
    if kind == "nand":
        return not (left and right)
    raise ValueError("unknown node %r" % (node,))


def _as_node(item):
    return parse_formula(item) if isinstance(item, str) else item


def truth_column(formula, names=None):
    """Result column as one string, e.g. ``'TFTT'``."""
    node = _as_node(formula)
    names = tuple(sorted(names)) if names is not None else formula_variables(node)
    return "".join("T" if eval_formula(node, row) else "F"
                   for row in all_assignments(names))


def truth_rows(formula, names=None):
    """``(assignment, value)`` pairs in canonical row order."""
    node = _as_node(formula)
    names = tuple(sorted(names)) if names is not None else formula_variables(node)
    return [(row, eval_formula(node, row)) for row in all_assignments(names)]


def classify(formula):
    """``'tautology'``, ``'contradiction'`` or ``'contingency'``."""
    values = [value for _, value in truth_rows(formula)]
    if all(values):
        return "tautology"
    if not any(values):
        return "contradiction"
    return "contingency"


def equivalent(first, second):
    """Same column over the union of the variables."""
    return first_difference(first, second) is None


def first_difference(first, second):
    """First row (canonical order) where the two formulas differ, else None."""
    left, right = _as_node(first), _as_node(second)
    names = sorted(set(formula_variables(left)) | set(formula_variables(right)))
    for row in all_assignments(names):
        if eval_formula(left, row) != eval_formula(right, row):
            return row
    return None


def row_text(assignment):
    """``'p=T, q=F'``."""
    return ", ".join("%s=%s" % (name, "T" if assignment[name] else "F")
                     for name in sorted(assignment))


def is_nnf(node):
    """True when negation is applied only to atoms and only ∧/∨ remain."""
    kind = node[0]
    if kind in ("var", "const"):
        return True
    if kind == "not":
        return node[1][0] in ("var", "const")
    if kind in ("and", "or"):
        return is_nnf(node[1]) and is_nnf(node[2])
    return False


def is_cnf(node):
    """True when the AST is a conjunction of disjunctions of literals."""
    return all(_is_clause(part, "or") for part in _flatten(node, "and"))


def is_dnf(node):
    """True when the AST is a disjunction of conjunctions of literals."""
    return all(_is_clause(part, "and") for part in _flatten(node, "or"))


def _flatten(node, kind):
    if node[0] == kind:
        return _flatten(node[1], kind) + _flatten(node[2], kind)
    return [node]


def _is_clause(node, kind):
    for literal in _flatten(node, kind):
        if literal[0] in ("var", "const"):
            continue
        if literal[0] == "not" and literal[1][0] in ("var", "const"):
            continue
        return False
    return True


# ---------------------------------------------------------------------------
# Polish (Łukasiewicz) notation
# ---------------------------------------------------------------------------

POLISH_OPS = {"N": "not", "K": "and", "A": "or", "C": "imp", "E": "iff",
              "J": "xor", "D": "nand"}


def parse_polish(text):
    """Parse ``CKpNqr``-style prefix notation into the oracle AST."""
    tokens = [char for char in text if not char.isspace()]
    node, index = _parse_polish(tokens, 0, text)
    if index != len(tokens):
        raise ParseError("trailing symbols in Polish formula %r" % text)
    return node


def _parse_polish(tokens, index, text):
    if index >= len(tokens):
        raise ParseError("Polish formula %r ended early" % text)
    token = tokens[index]
    if token == "1":
        return ("const", True), index + 1
    if token == "0":
        return ("const", False), index + 1
    if token == "N":
        arg, index = _parse_polish(tokens, index + 1, text)
        return ("not", arg), index
    if token in POLISH_OPS:
        left, index = _parse_polish(tokens, index + 1, text)
        right, index = _parse_polish(tokens, index, text)
        return (POLISH_OPS[token], left, right), index
    if token.isalpha() and token.islower():
        return ("var", token), index + 1
    raise ParseError("unexpected Polish symbol %r in %r" % (token, text))


def to_polish(node):
    """Print the oracle AST in Łukasiewicz notation."""
    kind = node[0]
    if kind == "const":
        return "1" if node[1] else "0"
    if kind == "var":
        return node[1]
    if kind == "not":
        return "N" + to_polish(node[1])
    letter = {value: key for key, value in POLISH_OPS.items()}[kind]
    return letter + to_polish(node[1]) + to_polish(node[2])


# ---------------------------------------------------------------------------
# Rosters, pairs, partitions, nested sets
# ---------------------------------------------------------------------------

EMPTY = "∅"
MINUS_SIGNS = "-−–—"
_INT_RE = re.compile(r"[%s]?\d+$" % MINUS_SIGNS)
_FRACTION_RE = re.compile(r"([%s]?\d+)/(\d+)$" % MINUS_SIGNS)


def _atom(text):
    text = text.strip()
    if not text:
        raise ParseError("empty element")
    if _INT_RE.match(text):
        return -int(text[1:]) if text[0] in MINUS_SIGNS else int(text)
    match = _FRACTION_RE.match(text)
    if match:
        numerator = match.group(1)
        if numerator[0] in MINUS_SIGNS:
            numerator = "-" + numerator[1:]
        return Fraction(int(numerator), int(match.group(2)))
    return text


class _SetParser(object):
    """``set := ∅ | { elems }``; ``elem := set | tuple | atom``."""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def peek(self):
        self.skip()
        return self.text[self.pos] if self.pos < len(self.text) else None

    def parse_top(self, want):
        value = self.parse_element(want)
        self.skip()
        if self.pos != len(self.text):
            raise ParseError("trailing text in %r" % self.text)
        return value

    def parse_element(self, want="any"):
        char = self.peek()
        if char is None:
            raise ParseError("unexpected end of %r" % self.text)
        if char == EMPTY:
            self.pos += 1
            return [] if want == "list" else frozenset()
        if char == "{":
            return self.parse_set(want)
        if char == "(":
            return self.parse_tuple()
        return self.parse_atom()

    def parse_set(self, want="any"):
        self.skip()
        self.pos += 1  # '{'
        items = []
        if self.peek() == "}":
            self.pos += 1
        else:
            while True:
                items.append(self.parse_element())
                char = self.peek()
                if char == ",":
                    self.pos += 1
                    continue
                if char == "}":
                    self.pos += 1
                    break
                raise ParseError("expected ',' or '}' in %r" % self.text)
        if want == "list":
            return items
        return frozenset(items)

    def parse_tuple(self):
        self.skip()
        self.pos += 1  # '('
        items = []
        while True:
            items.append(self.parse_element())
            char = self.peek()
            if char == ",":
                self.pos += 1
                continue
            if char == ")":
                self.pos += 1
                break
            raise ParseError("expected ',' or ')' in %r" % self.text)
        return tuple(items)

    def parse_atom(self):
        self.skip()
        start = self.pos
        while (self.pos < len(self.text)
               and self.text[self.pos] not in ",{}()"):
            self.pos += 1
        return _atom(self.text[start:self.pos])


def parse_set(text):
    """Parse ``{1, 2, {3}}`` or ``∅`` into a (possibly nested) frozenset."""
    return _SetParser(text.strip()).parse_top("any")


parse_nested_set = parse_set


def parse_roster(text):
    """Parse a roster into the list of elements **as written** (order kept).

    Duplicates are kept too, so a checker can see them.
    """
    return _SetParser(text.strip()).parse_top("list")


def parse_pair(text):
    """Parse ``(a, b)`` into a tuple."""
    value = _SetParser(text.strip()).parse_top("any")
    if not isinstance(value, tuple):
        raise ParseError("not an ordered pair: %r" % text)
    return value


def parse_pair_roster(text):
    """Parse ``{(1, 2), (2, 3)}`` into the list of pairs as written."""
    items = parse_roster(text)
    for item in items:
        if not isinstance(item, tuple):
            raise ParseError("not a roster of pairs: %r" % text)
    return items


def parse_partition(text):
    """Parse ``{{1, 3}, {2}}`` into the list of blocks as written."""
    items = parse_roster(text)
    blocks = []
    for item in items:
        if not isinstance(item, frozenset):
            raise ParseError("partition block is not a set: %r" % text)
        blocks.append(item)
    return blocks


# ---------------------------------------------------------------------------
# Canonical element order (independent re-implementation of §3)
# ---------------------------------------------------------------------------


def element_key(value):
    """Ints, then strings, then tuples, then sets (depth, elementwise, text)."""
    if isinstance(value, bool):
        return (1, (str(value),))
    if isinstance(value, int):
        return (0, (value,))
    if isinstance(value, Fraction):
        return (0, (float(value),))
    if isinstance(value, str):
        return (1, (value,))
    if isinstance(value, tuple):
        return (2, (len(value),) + tuple(element_key(v) for v in value))
    if isinstance(value, (frozenset, set)):
        members = tuple(element_key(v)
                        for v in sorted(value, key=element_key))
        return (3, (nesting_depth(value), members, element_text(value)))
    raise TypeError("no canonical order for %r" % (value,))


def nesting_depth(value):
    """Atoms 0, ``∅`` 1, ``{∅}`` 2, ..."""
    if not isinstance(value, (frozenset, set)):
        return 0
    if not value:
        return 1
    return 1 + max(nesting_depth(item) for item in value)


def element_text(value):
    """Canonical text of one element."""
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Fraction):
        return (str(value.numerator) if value.denominator == 1
                else "%d/%d" % (value.numerator, value.denominator))
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return "(" + ", ".join(element_text(v) for v in value) + ")"
    if isinstance(value, (frozenset, set)):
        if not value:
            return EMPTY
        return "{" + ", ".join(element_text(v)
                               for v in sorted(value, key=element_key)) + "}"
    raise TypeError("cannot render %r" % (value,))


def roster_text(items):
    """``{1, 2, 3}`` from any iterable of elements."""
    return element_text(frozenset(items))


def roster_order_ok(items):
    """True when ``items`` (as written) are in an accepted canonical order.

    The strand has two canonical orders that agree except on rosters of sets:
    elements sorted by :func:`element_key`, and — for a partition — blocks
    sorted by least element.  Either is accepted.
    """
    listed = list(items)
    if listed == sorted(listed, key=element_key):
        return True
    if listed and all(isinstance(item, (frozenset, set)) and item
                      for item in listed):
        least = [min(block, key=element_key) for block in listed]
        return least == sorted(least, key=element_key)
    return False


def has_duplicates(items):
    """True when the listed elements repeat."""
    listed = list(items)
    seen = []
    for item in listed:
        if item in seen:
            return True
        seen.append(item)
    return False


# ---------------------------------------------------------------------------
# Set-builder notation
# ---------------------------------------------------------------------------

_BUILDER_RE = re.compile(r"^\{\s*(?P<var>[A-Za-z][A-Za-z0-9_]*)\s*∈\s*"
                         r"(?P<domain>[^:]+?)\s*:\s*(?P<cond>.+?)\s*\}$")


def parse_set_builder(text):
    """``{x ∈ ℤ : −3 ≤ x < 4}`` -> ``('x', 'ℤ', '−3 ≤ x < 4')``."""
    match = _BUILDER_RE.match(text.strip())
    if not match:
        raise ParseError("not set-builder notation: %r" % text)
    return match.group("var"), match.group("domain").strip(), \
        match.group("cond")


def eval_set_builder(text, bound=60):
    """Elements of a set-builder expression, canonically ordered.

    The predicate grammar is deliberately small (it mirrors the generators
    that use it): comparison chains (``<``, ``≤``, ``>``, ``≥``, ``=``,
    ``≠``) against integers or ``x``; ``x is even/odd/prime/a perfect
    square``; ``k divides x`` / ``x divides k`` (also with ``∣``); ``x^2``
    on either side of a comparison; and the connectives ``and``, ``or``,
    ``not``.  The candidate range comes from the comparison bounds (the
    domain ``ℕ`` supplies a lower bound of 0).
    """
    var, domain, condition = parse_set_builder(text)
    predicate = _parse_predicate(condition, var)
    if domain in ("ℤ", "Z"):
        low, high = _condition_bounds(condition, var)
    elif domain in ("ℕ", "N"):
        low, high = _condition_bounds(condition, var)
        low = max(low, 0) if low is not None else 0
    else:
        candidates = parse_roster(domain)
        return sorted({item for item in candidates
                       if isinstance(item, int) and predicate(item)})
    if low is None or high is None:
        raise ParseError("cannot bound the candidates of %r" % text)
    if high - low > bound:
        raise ParseError("candidate range too wide in %r" % text)
    return [value for value in range(low, high + 1) if predicate(value)]


_NUM = r"[%s]?\d+" % MINUS_SIGNS
_REL = r"<|>|≤|≥|=|≠"


def _to_int(text):
    text = text.strip()
    if text[0] in MINUS_SIGNS:
        return -int(text[1:])
    return int(text)


def _condition_bounds(condition, var):
    low = high = None
    for match in re.finditer(r"(%s)\s*(%s)\s*%s" % (_NUM, _REL, re.escape(var)),
                             condition):
        value, rel = _to_int(match.group(1)), match.group(2)
        candidate = value + 1 if rel in ("<",) else value
        if rel in ("<", "≤"):
            low = candidate if low is None else max(low, candidate)
    for match in re.finditer(r"%s\s*(%s)\s*(%s)" % (re.escape(var), _REL, _NUM),
                             condition):
        rel, value = match.group(1), _to_int(match.group(2))
        if rel in ("<", "≤"):
            candidate = value - 1 if rel == "<" else value
            high = candidate if high is None else min(high, candidate)
        elif rel in (">", "≥"):
            candidate = value + 1 if rel == ">" else value
            low = candidate if low is None else max(low, candidate)
        elif rel == "=":
            low = high = value
    for match in re.finditer(r"%s\s*(%s)\s*(%s)" % (re.escape(var) + r"\^2",
                                                    _REL, _NUM), condition):
        rel, value = match.group(1), _to_int(match.group(2))
        if rel in ("<", "≤") and value >= 0:
            span = int(abs(value) ** 0.5) + 2
            low = -span if low is None else max(low, -span)
            high = span if high is None else min(high, span)
    return low, high


def _is_prime(value):
    if value < 2:
        return False
    for divisor in range(2, int(value ** 0.5) + 1):
        if value % divisor == 0:
            return False
    return True


def _parse_predicate(condition, var):
    """Compile a set-builder condition into ``value -> bool``."""
    text = condition.strip()
    parts = _split_top(text, " or ")
    if len(parts) > 1:
        subs = [_parse_predicate(part, var) for part in parts]
        return lambda value: any(sub(value) for sub in subs)
    parts = _split_top(text, " and ")
    if len(parts) > 1:
        subs = [_parse_predicate(part, var) for part in parts]
        return lambda value: all(sub(value) for sub in subs)
    if text.lower().startswith("not "):
        sub = _parse_predicate(text[4:], var)
        return lambda value: not sub(value)
    if text.startswith("(") and text.endswith(")"):
        return _parse_predicate(text[1:-1], var)
    return _atomic_predicate(text, var)


def _split_top(text, separator):
    parts = []
    depth = 0
    current = ""
    index = 0
    while index < len(text):
        char = text[index]
        if char in "({":
            depth += 1
        elif char in ")}":
            depth -= 1
        if depth == 0 and text.lower().startswith(separator, index):
            parts.append(current)
            current = ""
            index += len(separator)
            continue
        current += char
        index += 1
    parts.append(current)
    return [part.strip() for part in parts if part.strip()]


def _atomic_predicate(text, var):
    lowered = text.lower()
    escaped = re.escape(var)
    match = re.fullmatch(r"%s\s+is\s+(?:an?\s+)?(.+)" % escaped, lowered)
    if match:
        word = match.group(1).strip()
        if word == "even":
            return lambda value: value % 2 == 0
        if word == "odd":
            return lambda value: value % 2 != 0
        if word == "prime":
            return _is_prime
        if word in ("perfect square", "square"):
            return lambda value: value >= 0 and int(value ** 0.5) ** 2 == value
        if word == "positive":
            return lambda value: value > 0
        if word == "negative":
            return lambda value: value < 0
        raise ParseError("unknown predicate %r" % text)
    match = re.fullmatch(r"(%s)\s*(?:divides|∣)\s*%s" % (_NUM, escaped), text)
    if match:
        divisor = _to_int(match.group(1))
        return lambda value: divisor != 0 and value % divisor == 0
    match = re.fullmatch(r"%s\s*(?:divides|∣)\s*(%s)" % (escaped, _NUM), text)
    if match:
        multiple = _to_int(match.group(1))
        return lambda value: value != 0 and multiple % value == 0
    chain = re.fullmatch(
        r"(%s|%s(?:\^2)?)\s*(%s)\s*(%s|%s(?:\^2)?)(?:\s*(%s)\s*(%s|%s(?:\^2)?))?"
        % (_NUM, escaped, _REL, _NUM, escaped, _REL, _NUM, escaped), text)
    if chain:
        groups = [g for g in chain.groups() if g is not None]
        terms = groups[0::2]
        relations = groups[1::2]

        def predicate(value, terms=terms, relations=relations):
            values = [_term_value(term, var, value) for term in terms]
            for index, relation in enumerate(relations):
                if not _compare(values[index], relation, values[index + 1]):
                    return False
            return True

        return predicate
    raise ParseError("unsupported set-builder condition %r" % text)


def _term_value(term, var, value):
    term = term.strip()
    if term == var:
        return value
    if term == var + "^2":
        return value * value
    return _to_int(term)


def _compare(left, relation, right):
    if relation == "<":
        return left < right
    if relation == "≤":
        return left <= right
    if relation == ">":
        return left > right
    if relation == "≥":
        return left >= right
    if relation == "=":
        return left == right
    if relation == "≠":
        return left != right
    raise ParseError("unknown relation %r" % relation)


# ---------------------------------------------------------------------------
# Set expressions
# ---------------------------------------------------------------------------

SET_UNION = "∪"
SET_INTER = "∩"
SET_DIFF = "−"
SET_SYMDIFF = "Δ"
SET_TIMES = "×"
SET_COMP = "ᶜ"


class _SetExprParser(object):
    """``union := inter ((∪ | − | Δ) inter)*``; ``inter := postfix ((∩ | ×)
    postfix)*``; ``postfix := atom ᶜ*``; ``atom := name | ∅ | U | roster |
    P(expr) | ( union )``."""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def peek(self):
        self.skip()
        return self.text[self.pos] if self.pos < len(self.text) else None

    def parse(self):
        node = self.union()
        self.skip()
        if self.pos != len(self.text):
            raise ParseError("trailing text in set expression %r" % self.text)
        return node

    def union(self):
        node = self.inter()
        while self.peek() in (SET_UNION, SET_DIFF, SET_SYMDIFF, "-"):
            char = self.text[self.pos]
            self.pos += 1
            kind = {SET_UNION: "union", SET_DIFF: "diff", "-": "diff",
                    SET_SYMDIFF: "symdiff"}[char]
            node = (kind, node, self.inter())
        return node

    def inter(self):
        node = self.postfix()
        while self.peek() in (SET_INTER, SET_TIMES):
            char = self.text[self.pos]
            self.pos += 1
            kind = "inter" if char == SET_INTER else "times"
            node = (kind, node, self.postfix())
        return node

    def postfix(self):
        node = self.atom()
        while self.peek() in (SET_COMP, "'"):
            self.pos += 1
            node = ("comp", node)
        return node

    def atom(self):
        char = self.peek()
        if char is None:
            raise ParseError("set expression %r ended early" % self.text)
        if char == "(":
            self.pos += 1
            node = self.union()
            if self.peek() != ")":
                raise ParseError("expected ')' in %r" % self.text)
            self.pos += 1
            return node
        if char == EMPTY:
            self.pos += 1
            return ("literal", frozenset())
        if char == "{":
            start = self.pos
            depth = 0
            while self.pos < len(self.text):
                if self.text[self.pos] == "{":
                    depth += 1
                elif self.text[self.pos] == "}":
                    depth -= 1
                    if depth == 0:
                        self.pos += 1
                        break
                self.pos += 1
            return ("literal", parse_set(self.text[start:self.pos]))
        match = _NAME_RE.match(self.text, self.pos)
        if not match:
            raise ParseError("unexpected %r in set expression %r"
                             % (char, self.text))
        name = match.group(0)
        self.pos = match.end()
        if name == "P" and self.peek() == "(":
            self.pos += 1
            inner = self.union()
            if self.peek() != ")":
                raise ParseError("expected ')' in %r" % self.text)
            self.pos += 1
            return ("power", inner)
        if name == "U":
            return ("universe",)
        return ("name", name)


def parse_set_expression(text):
    """Parse ``(A ∪ B)ᶜ ∩ C`` into an AST."""
    return _SetExprParser(text.strip()).parse()


def set_expression_names(node):
    """Sorted tuple of set names in a set-expression AST."""
    found = set()

    def walk(item):
        if item[0] == "name":
            found.add(item[1])
        elif item[0] in ("comp", "power"):
            walk(item[1])
        elif item[0] in ("union", "inter", "diff", "symdiff", "times"):
            walk(item[1])
            walk(item[2])

    walk(node)
    return tuple(sorted(found))


def eval_set_expression(node, env, universe=None):
    """Evaluate a set-expression AST; ``env`` maps names to iterables."""
    if isinstance(node, str):
        node = parse_set_expression(node)
    kind = node[0]
    if kind == "literal":
        return frozenset(node[1])
    if kind == "universe":
        if universe is None:
            raise ParseError("no universe supplied for U")
        return frozenset(universe)
    if kind == "name":
        if node[1] not in env:
            raise ParseError("no value for set %r" % node[1])
        return frozenset(env[node[1]])
    if kind == "comp":
        if universe is None:
            raise ParseError("no universe supplied for complement")
        return frozenset(universe) - eval_set_expression(node[1], env,
                                                         universe)
    if kind == "power":
        inner = eval_set_expression(node[1], env, universe)
        items = sorted(inner, key=element_key)
        subsets = [frozenset()]
        for item in items:
            subsets += [subset | {item} for subset in subsets]
        return frozenset(subsets)
    left = eval_set_expression(node[1], env, universe)
    right = eval_set_expression(node[2], env, universe)
    if kind == "union":
        return left | right
    if kind == "inter":
        return left & right
    if kind == "diff":
        return left - right
    if kind == "symdiff":
        return left ^ right
    if kind == "times":
        return frozenset((a, b) for a in left for b in right)
    raise ValueError("unknown set node %r" % (node,))


def membership_rows(names):
    """Membership-table rows for ``names``: ``∈`` before ``∉``, alphabetical."""
    return all_assignments(names)


def membership_column(expression, names=None):
    """Whether a generic element lies in the expression, row by row.

    Returns a tuple of booleans over :func:`membership_rows` — the 8-row
    membership table of a three-set identity, computed by brute force.
    """
    node = (parse_set_expression(expression)
            if isinstance(expression, str) else expression)
    names = tuple(sorted(names)) if names else set_expression_names(node)
    out = []
    for row in membership_rows(names):
        env = {name: (frozenset({"x"}) if row[name] else frozenset())
               for name in names}
        out.append("x" in eval_set_expression(node, env, frozenset({"x"})))
    return tuple(out)


# ---------------------------------------------------------------------------
# Ordinals in Cantor normal form (exponents below ω)
# ---------------------------------------------------------------------------


class Ordinal(object):
    """An ordinal below ω^ω: ``terms`` is ``((exponent, coefficient), ...)``
    with strictly decreasing non-negative integer exponents and positive
    coefficients."""

    __slots__ = ("terms",)

    def __init__(self, terms=()):
        cleaned = tuple((int(e), int(c)) for e, c in terms if c)
        for index in range(1, len(cleaned)):
            if cleaned[index - 1][0] <= cleaned[index][0]:
                raise ValueError("Cantor normal form needs decreasing "
                                 "exponents: %r" % (terms,))
        object.__setattr__(self, "terms", cleaned)

    # -- constructors ------------------------------------------------------
    @staticmethod
    def zero():
        return Ordinal(())

    @staticmethod
    def finite(value):
        return Ordinal(((0, value),)) if value else Ordinal(())

    @staticmethod
    def omega_power(exponent, coefficient=1):
        return Ordinal(((exponent, coefficient),)) if coefficient \
            else Ordinal(())

    # -- arithmetic --------------------------------------------------------
    def __add__(self, other):
        if not other.terms:
            return self
        if not self.terms:
            return other
        lead = other.terms[0][0]
        kept = [(e, c) for (e, c) in self.terms if e > lead]
        same = [c for (e, c) in self.terms if e == lead]
        head_coefficient = other.terms[0][1] + (same[0] if same else 0)
        return Ordinal(tuple(kept) + ((lead, head_coefficient),)
                       + other.terms[1:])

    def __mul__(self, other):
        if not self.terms or not other.terms:
            return Ordinal.zero()
        lead_exp, lead_coefficient = self.terms[0]
        out = Ordinal.zero()
        for exponent, coefficient in other.terms:
            if exponent > 0:
                piece = Ordinal(((lead_exp + exponent, coefficient),))
            else:
                piece = Ordinal(((lead_exp, lead_coefficient * coefficient),)
                                + self.terms[1:])
            out = out + piece
        return out

    # -- comparison --------------------------------------------------------
    def _key(self):
        return self.terms

    def __eq__(self, other):
        return isinstance(other, Ordinal) and self.terms == other.terms

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.terms)

    def __lt__(self, other):
        for (e1, c1), (e2, c2) in zip(self.terms, other.terms):
            if e1 != e2:
                return e1 < e2
            if c1 != c2:
                return c1 < c2
        return len(self.terms) < len(other.terms)

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return other <= self

    # -- printing ----------------------------------------------------------
    def __str__(self):
        if not self.terms:
            return "0"
        pieces = []
        for exponent, coefficient in self.terms:
            if exponent == 0:
                pieces.append(str(coefficient))
            else:
                base = "ω" if exponent == 1 else "ω^%d" % exponent
                pieces.append(base if coefficient == 1
                              else "%s·%d" % (base, coefficient))
        return " + ".join(pieces)

    def __repr__(self):
        return "Ordinal(%s)" % self


OMEGA = Ordinal.omega_power(1)


def parse_ordinal(text):
    """Evaluate an ordinal expression: ``(ω + 1) · 2``, ``ω^2·3 + ω + 4``.

    Grammar: ``expr := term ('+' term)*``; ``term := factor ('·' factor)*``;
    ``factor := atom ('^' integer)?``; ``atom := ω | integer | ( expr )``.
    Both ``+`` and ``·`` are left-associative and non-commutative, as ordinal
    arithmetic requires.
    """
    return _OrdinalParser(text.strip()).parse()


class _OrdinalParser(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def peek(self):
        self.skip()
        return self.text[self.pos] if self.pos < len(self.text) else None

    def parse(self):
        value = self.expr()
        self.skip()
        if self.pos != len(self.text):
            raise ParseError("trailing text in ordinal %r" % self.text)
        return value

    def expr(self):
        value = self.term()
        while self.peek() == "+":
            self.pos += 1
            value = value + self.term()
        return value

    def term(self):
        value = self.factor()
        while self.peek() in ("·", "*", "×"):
            self.pos += 1
            value = value * self.factor()
        return value

    def factor(self):
        char = self.peek()
        if char == "(":
            self.pos += 1
            value = self.expr()
            if self.peek() != ")":
                raise ParseError("expected ')' in ordinal %r" % self.text)
            self.pos += 1
            return value
        if char == "ω":
            self.pos += 1
            exponent = 1
            if self.peek() == "^":
                self.pos += 1
                exponent = self.integer()
            return Ordinal.omega_power(exponent)
        return Ordinal.finite(self.integer())

    def integer(self):
        self.skip()
        match = re.compile(r"\d+").match(self.text, self.pos)
        if not match:
            raise ParseError("expected an integer in ordinal %r" % self.text)
        self.pos = match.end()
        return int(match.group(0))


def is_canonical_ordinal(text):
    """True when ``text`` is the canonical Cantor normal form of its value."""
    try:
        return str(parse_ordinal(text)) == text.strip()
    except (ParseError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Brute-force relations and posets
# ---------------------------------------------------------------------------


def brute_reflexive_closure(pairs, elements):
    """``R`` plus the diagonal, by enumeration."""
    out = set(map(tuple, pairs))
    for element in elements:
        out.add((element, element))
    return frozenset(out)


def brute_symmetric_closure(pairs):
    """``R`` plus every flipped pair."""
    out = set()
    for a, b in pairs:
        out.add((a, b))
        out.add((b, a))
    return frozenset(out)


def brute_transitive_closure(pairs):
    """Reachability by breadth-first search from every node (paths ≥ 1)."""
    edges = {}
    for a, b in pairs:
        edges.setdefault(a, set()).add(b)
    out = set()
    for start in list(edges):
        seen = set()
        frontier = list(edges.get(start, ()))
        while frontier:
            node = frontier.pop()
            if node in seen:
                continue
            seen.add(node)
            out.add((start, node))
            frontier.extend(edges.get(node, ()))
    return frozenset(out)


def brute_equivalence_closure(pairs, elements):
    """Closure under reflexivity, symmetry and transitivity."""
    return brute_transitive_closure(
        brute_symmetric_closure(brute_reflexive_closure(pairs, elements)))


def brute_properties(pairs, elements):
    """Relation properties checked by enumerating element tuples."""
    pairs = frozenset(map(tuple, pairs))
    elements = list(elements)
    reflexive = all((a, a) in pairs for a in elements)
    symmetric = all(((b, a) in pairs) or ((a, b) not in pairs)
                    for a in elements for b in elements)
    antisymmetric = all(a == b or not ((a, b) in pairs and (b, a) in pairs)
                        for a in elements for b in elements)
    transitive = all(not ((a, b) in pairs and (b, c) in pairs)
                     or (a, c) in pairs
                     for a in elements for b in elements for c in elements)
    return {"reflexive": reflexive, "symmetric": symmetric,
            "antisymmetric": antisymmetric, "transitive": transitive}


def brute_equivalence_classes(pairs, elements):
    """Blocks by graph search on the symmetric closure."""
    edges = {element: set() for element in elements}
    for a, b in pairs:
        if a in edges and b in edges:
            edges[a].add(b)
            edges[b].add(a)
    seen = set()
    blocks = []
    for element in sorted(elements, key=element_key):
        if element in seen:
            continue
        block = set()
        frontier = [element]
        while frontier:
            node = frontier.pop()
            if node in block:
                continue
            block.add(node)
            frontier.extend(edges[node])
        seen |= block
        blocks.append(sorted(block, key=element_key))
    blocks.sort(key=lambda block: element_key(block[0]))
    return blocks


def brute_cover(pairs, elements):
    """Hasse edges as ``strict − (strict ∘ strict)``."""
    strict = {(a, b) for a, b in pairs if a != b}
    composed = {(a, c) for (a, b) in strict for (b2, c) in strict if b == b2}
    return frozenset(strict - composed)


def brute_linear_extension(pairs, elements):
    """Smallest linear extension, found by enumerating permutations.

    Returns the lexicographically first permutation (in canonical element
    order) that respects the order — the same order the "smallest available
    label" tie-break produces, reached by a completely different route.
    """
    elements = sorted(elements, key=element_key)
    if len(elements) > 8:
        raise ValueError("brute force is limited to 8 elements")
    strict = {(a, b) for a, b in pairs if a != b}
    for candidate in itertools.permutations(elements):
        position = {element: index for index, element in enumerate(candidate)}
        if all(position[a] < position[b] for a, b in strict):
            return list(candidate)
    raise ValueError("no linear extension: the relation has a cycle")


def brute_minimal(pairs, elements):
    """Minimal elements by enumeration."""
    strict = {(a, b) for a, b in pairs if a != b}
    return [e for e in sorted(elements, key=element_key)
            if not any(b == e for _, b in strict)]


def brute_maximal(pairs, elements):
    """Maximal elements by enumeration."""
    strict = {(a, b) for a, b in pairs if a != b}
    return [e for e in sorted(elements, key=element_key)
            if not any(a == e for a, _ in strict)]


def brute_least(pairs, elements):
    """The least element, or ``None``."""
    order = frozenset(map(tuple, pairs))
    for candidate in sorted(elements, key=element_key):
        if all((candidate, other) in order for other in elements):
            return candidate
    return None


def brute_greatest(pairs, elements):
    """The greatest element, or ``None``."""
    order = frozenset(map(tuple, pairs))
    for candidate in sorted(elements, key=element_key):
        if all((other, candidate) in order for other in elements):
            return candidate
    return None


def brute_upper_bounds(pairs, elements, subset):
    """Upper bounds of ``subset``."""
    order = frozenset(map(tuple, pairs))
    return [e for e in sorted(elements, key=element_key)
            if all((item, e) in order for item in subset)]


def brute_lower_bounds(pairs, elements, subset):
    """Lower bounds of ``subset``."""
    order = frozenset(map(tuple, pairs))
    return [e for e in sorted(elements, key=element_key)
            if all((e, item) in order for item in subset)]


def brute_lub(pairs, elements, subset):
    """Least upper bound, chosen among the upper bounds by comparison."""
    order = frozenset(map(tuple, pairs))
    bounds = brute_upper_bounds(pairs, elements, subset)
    for candidate in bounds:
        if all((candidate, other) in order for other in bounds):
            return candidate
    return None


def brute_glb(pairs, elements, subset):
    """Greatest lower bound, chosen among the lower bounds by comparison."""
    order = frozenset(map(tuple, pairs))
    bounds = brute_lower_bounds(pairs, elements, subset)
    for candidate in bounds:
        if all((other, candidate) in order for other in bounds):
            return candidate
    return None


def brute_function_properties(table, codomain):
    """``(injective_witness, surjective_witness)`` by enumeration.

    The injective witness is the first colliding pair of arguments; the
    surjective witness is the first element of the codomain that is missed.
    """
    keys = sorted(table, key=element_key)
    collision = None
    for index, first in enumerate(keys):
        for second in keys[index + 1:]:
            if table[first] == table[second]:
                collision = (first, second, table[first])
                break
        if collision:
            break
    missed = None
    values = set(table.values())
    for value in sorted(codomain, key=element_key):
        if value not in values:
            missed = value
            break
    return collision, missed
