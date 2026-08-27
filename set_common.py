"""Set, relation and order toolkit shared by the foundations strand.

The printing half of ``plans/foundations_plan.md`` §3 (rosters, pairs, partitions,
set-builder, ``card(A)``) plus the finite structures the relation/order
generators walk: matrices, closures with per-pivot Warshall snapshots, cover
relations, bounds, linear extensions, equivalence classes — and the
hereditarily finite sets (Kuratowski pairs, von Neumann numerals, rank).

The independent checking route lives in ``tests/foundations_oracle.py``,
which never imports this module (A9).

Conventions
-----------
- Elements sort with :func:`sort_key`: integers ascending, then strings
  alphabetically, then tuples, then nested sets by depth and text.
- Rosters are ``{1, 2, 3}`` — comma plus one space, no duplicates — and the
  empty set is ``∅``.  Ordered pairs are ``(a, b)``.
- Partitions print as a set of blocks sorted by least element:
  ``{{1, 3}, {2}, {4, 5}}``.
- Cardinality is ``card(A)``; set-builder uses a colon,
  ``{x ∈ ℤ : −3 ≤ x < 4}``.  ASCII ``|`` never appears in this module's
  output.
"""
from fractions import Fraction

EMPTY = "∅"
UNIVERSE = "U"
MINUS = "−"          # U+2212, used inside set-builder conditions
DIVIDES = "∣"        # U+2223, never the ASCII bar
INTEGERS = "ℤ"
NATURALS = "ℕ"
RATIONALS = "ℚ"
REALS = "ℝ"
EMPTY_SET = frozenset()


# ---------------------------------------------------------------------------
# Ordering and rendering
# ---------------------------------------------------------------------------


def is_set(value):
    """True for the set-like values this module renders (frozenset/set)."""
    return isinstance(value, (frozenset, set))


def set_depth(value):
    """Nesting depth: atoms 0, ``∅`` 1, ``{∅}`` 2, ``{{∅}}`` 3."""
    if not is_set(value):
        return 0
    if not value:
        return 1
    return 1 + max(set_depth(item) for item in value)


def sort_key(value):
    """Canonical sort key: ints, then strings, then tuples, then sets."""
    if isinstance(value, bool):
        return (1, (str(value),))
    if isinstance(value, int):
        return (0, (value,))
    if isinstance(value, Fraction):
        return (0, (float(value),))
    if isinstance(value, str):
        return (1, (value,))
    if isinstance(value, tuple):
        return (2, (len(value),) + tuple(sort_key(item) for item in value))
    if is_set(value):
        # Depth first, then element by element (which orders {a} before
        # {a, b}), then the rendered text as a final tie-break.
        members = tuple(sort_key(item)
                        for item in sorted(value, key=sort_key))
        return (3, (set_depth(value), members, roster(value)))
    raise TypeError("no canonical order for %r" % (value,))


def sorted_elements(items):
    """Deduplicated, canonically ordered list of ``items``."""
    seen = []
    for item in items:
        item = frozenset(item) if isinstance(item, set) else item
        if item not in seen:
            seen.append(item)
    return sorted(seen, key=sort_key)


def fmt_int(value, unicode_minus=False):
    """Integer text; ``unicode_minus`` switches ``-3`` to ``−3`` (U+2212)."""
    text = str(value)
    return text.replace("-", MINUS) if unicode_minus else text


def fmt_element(value, unicode_minus=False):
    """Canonical text for one element (int, string, pair, or nested set)."""
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, int):
        return fmt_int(value, unicode_minus)
    if isinstance(value, Fraction):
        return (str(value.numerator) if value.denominator == 1
                else "%d/%d" % (value.numerator, value.denominator))
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return tuple_text(value, unicode_minus)
    if is_set(value):
        return roster(value, unicode_minus)
    raise TypeError("cannot render %r" % (value,))


def roster(items, unicode_minus=False):
    """``{1, 2, 3}`` — sorted, duplicate-free; the empty set is ``∅``."""
    elements = sorted_elements(items)
    if not elements:
        return EMPTY
    return "{" + ", ".join(fmt_element(item, unicode_minus)
                           for item in elements) + "}"


def tuple_text(values, unicode_minus=False):
    """``(a, b)`` — also used for triples and longer tuples."""
    return "(" + ", ".join(fmt_element(item, unicode_minus)
                           for item in values) + ")"


def pair(first, second, unicode_minus=False):
    """``(a, b)``."""
    return tuple_text((first, second), unicode_minus)


def pair_roster(pairs, unicode_minus=False):
    """A relation as a sorted roster of ordered pairs."""
    return roster([tuple(item) for item in pairs], unicode_minus)


relation_text = pair_roster


def partition_text(blocks, unicode_minus=False):
    """``{{1, 3}, {2}, {4, 5}}`` — blocks sorted by least element."""
    cleaned = []
    for block in blocks:
        elements = sorted_elements(block)
        if not elements:
            raise ValueError("a partition block may not be empty")
        cleaned.append(elements)
    cleaned.sort(key=lambda block: sort_key(block[0]))
    if not cleaned:
        return EMPTY
    return "{" + ", ".join(roster(block, unicode_minus)
                           for block in cleaned) + "}"


def card_text(name):
    """``card(A)`` — never bars."""
    return "card(%s)" % name


def card_eq(name, value):
    """``card(A) = 3``."""
    return "%s = %d" % (card_text(name), value)


def set_builder(condition, var="x", domain=INTEGERS):
    """``{x ∈ ℤ : −3 ≤ x < 4}`` — set-builder with a colon."""
    return "{%s ∈ %s : %s}" % (var, domain, condition)


def range_condition(low, high, var="x", low_strict=False, high_strict=True):
    """``−3 ≤ x < 4`` with U+2212 minus signs."""
    low_rel = "<" if low_strict else "≤"
    high_rel = "<" if high_strict else "≤"
    return "%s %s %s %s %s" % (fmt_int(low, True), low_rel, var, high_rel,
                               fmt_int(high, True))


def sequence_text(items, unicode_minus=False):
    """``1, 2, 3, 4, 6, 12`` — an ordered list, order preserved."""
    return ", ".join(fmt_element(item, unicode_minus) for item in items)


def map_text(mapping, unicode_minus=False):
    """``1→b, 2→a, 3→c`` — a finite map, sorted by source element."""
    items = sorted(mapping.items(), key=lambda kv: sort_key(kv[0]))
    return ", ".join("%s→%s" % (fmt_element(k, unicode_minus),
                                fmt_element(v, unicode_minus))
                     for k, v in items)


def matrix_rows(pairs, rows, cols=None):
    """0/1 matrix rows as strings: ``['0 1 1 0', ...]``."""
    matrix = relation_matrix(pairs, rows, cols)
    return [" ".join(str(bit) for bit in row) for row in matrix]


def matrix_text(pairs, rows, cols=None):
    """Matrix rows joined with ``; `` — one pipe-free answer string."""
    return "; ".join(matrix_rows(pairs, rows, cols))


# ---------------------------------------------------------------------------
# Plain set operations (thin wrappers that keep everything a frozenset)
# ---------------------------------------------------------------------------


def as_set(items):
    """``frozenset`` of ``items`` (sets inside are frozen too)."""
    return frozenset(frozenset(i) if isinstance(i, set) else i for i in items)


def union(left, right):
    """``A ∪ B``."""
    return frozenset(left) | frozenset(right)


def intersection(left, right):
    """``A ∩ B``."""
    return frozenset(left) & frozenset(right)


def difference(left, right):
    """``A − B``."""
    return frozenset(left) - frozenset(right)


def symmetric_difference(left, right):
    """``A Δ B``."""
    return frozenset(left) ^ frozenset(right)


def complement(universe, subset):
    """``Aᶜ`` relative to the stated universe."""
    return frozenset(universe) - frozenset(subset)


def cartesian_product(left, right):
    """``A × B`` as a set of ordered pairs."""
    return frozenset((a, b) for a in left for b in right)


def powerset(items):
    """``P(A)`` as a canonically ordered list of frozensets."""
    elements = sorted_elements(items)
    subsets = [EMPTY_SET]
    for element in elements:
        subsets += [subset | {element} for subset in subsets]
    return sorted(subsets, key=sort_key)


# ---------------------------------------------------------------------------
# Hereditarily finite sets
# ---------------------------------------------------------------------------


def set_rank(value):
    """Von Neumann rank: ``rank(∅) = 0``, ``rank(x) = max(rank(e) + 1)``."""
    if not is_set(value):
        raise TypeError("rank is defined for sets, got %r" % (value,))
    if not value:
        return 0
    return max(set_rank(item) + 1 for item in value)


def hf_text(value):
    """Canonical text of a hereditarily finite set (``{∅, {∅}}``)."""
    return roster(value)


def successor(value):
    """``S(x) = x ∪ {x}``."""
    value = frozenset(value)
    return value | {value}


def von_neumann(n):
    """The von Neumann numeral for ``n``: ``0 = ∅``, ``n + 1 = S(n)``."""
    if n < 0:
        raise ValueError("von Neumann numerals are non-negative")
    out = EMPTY_SET
    for _ in range(n):
        out = successor(out)
    return out


def von_neumann_index(value):
    """Inverse of :func:`von_neumann`; ``ValueError`` if not a numeral."""
    value = frozenset(value)
    count = len(value)  # the numeral n has exactly n elements
    if von_neumann(count) != value:
        raise ValueError("%s is not a von Neumann numeral" % hf_text(value))
    return count


def big_union(value):
    """``∪X`` — the union of the members of ``X``."""
    out = set()
    for item in value:
        if not is_set(item):
            raise TypeError("∪X needs a set of sets, found %r" % (item,))
        out |= set(item)
    return frozenset(out)


def is_transitive(value):
    """True when every element of ``value`` is also a subset of it."""
    return transitivity_witness(value) is None


def transitivity_witness(value):
    """First ``(element, missing)`` breaking transitivity, else ``None``.

    Elements are scanned in canonical order, and inside an element its own
    members are scanned in canonical order, so the witness is forced.
    """
    for element in sorted_elements(value):
        if not is_set(element):
            return (element, None)
        for member in sorted_elements(element):
            if member not in value:
                return (element, member)
    return None


def kuratowski(first, second):
    """``(a, b)`` as ``{{a}, {a, b}}``."""
    return frozenset({frozenset({first}), frozenset({first, second})})


def un_kuratowski(value):
    """Decode ``{{a}, {a, b}}`` back to the ordered pair ``(a, b)``."""
    blocks = [frozenset(item) for item in value if is_set(item)]
    if len(blocks) != len(value):
        raise ValueError("not a Kuratowski pair: %s" % hf_text(value))
    if len(blocks) == 1:
        only = blocks[0]
        if len(only) != 1:
            raise ValueError("not a Kuratowski pair: %s" % hf_text(value))
        element = next(iter(only))
        return (element, element)
    if len(blocks) != 2:
        raise ValueError("not a Kuratowski pair: %s" % hf_text(value))
    small, large = sorted(blocks, key=len)
    if len(small) != 1 or len(large) != 2 or not small <= large:
        raise ValueError("not a Kuratowski pair: %s" % hf_text(value))
    first = next(iter(small))
    second = next(iter(large - small))
    return (first, second)


def ackermann_code(value):
    """Ackermann coding of a hereditarily finite set: ``x -> Σ 2^code(e)``."""
    if not is_set(value):
        raise TypeError("Ackermann coding is defined for sets")
    return sum(1 << ackermann_code(item) for item in value)


def ackermann_decode(number):
    """Inverse of :func:`ackermann_code`."""
    if number < 0:
        raise ValueError("Ackermann codes are non-negative")
    out = set()
    index = 0
    while number:
        if number & 1:
            out.add(ackermann_decode(index))
        number >>= 1
        index += 1
    return frozenset(out)


# ---------------------------------------------------------------------------
# Relations
# ---------------------------------------------------------------------------


def as_pairs(pairs):
    """Normalize a relation to a set of 2-tuples."""
    return frozenset((a, b) for a, b in pairs)


def relation_matrix(pairs, rows, cols=None):
    """0/1 matrix of ``pairs`` over ``rows`` × ``cols`` (cols default rows)."""
    cols = rows if cols is None else cols
    pairs = as_pairs(pairs)
    return [[1 if (a, b) in pairs else 0 for b in cols] for a in rows]


def matrix_pairs(matrix, rows, cols=None):
    """Inverse of :func:`relation_matrix`."""
    cols = rows if cols is None else cols
    return frozenset((rows[i], cols[j])
                     for i, row in enumerate(matrix)
                     for j, bit in enumerate(row) if bit)


def compose(first, second):
    """``second ∘ first``: pairs ``(a, c)`` with ``(a, b) ∈ first`` and
    ``(b, c) ∈ second``."""
    first = as_pairs(first)
    second = as_pairs(second)
    return frozenset((a, c) for (a, b) in first for (b2, c) in second
                     if b == b2)


def inverse_relation(pairs):
    """``R⁻¹``."""
    return frozenset((b, a) for (a, b) in as_pairs(pairs))


def domain_of(pairs):
    """The set of first components."""
    return frozenset(a for (a, _) in as_pairs(pairs))


def range_of(pairs):
    """The set of second components."""
    return frozenset(b for (_, b) in as_pairs(pairs))


def restrict(pairs, subset):
    """``R`` restricted to pairs whose first component lies in ``subset``."""
    subset = frozenset(subset)
    return frozenset((a, b) for (a, b) in as_pairs(pairs) if a in subset)


def reflexive_closure(pairs, elements):
    """``R ∪ {(a, a)}``."""
    return as_pairs(pairs) | frozenset((a, a) for a in elements)


def symmetric_closure(pairs):
    """``R ∪ R⁻¹``."""
    return as_pairs(pairs) | inverse_relation(pairs)


def transitive_closure(pairs):
    """``R⁺`` by repeatedly adding composed pairs to a fixed point."""
    current = set(as_pairs(pairs))
    while True:
        new = {(a, c) for (a, b) in current for (b2, c) in current
               if b == b2 and (a, c) not in current}
        if not new:
            return frozenset(current)
        current |= new


def equivalence_closure(pairs, elements):
    """Reflexive, then symmetric, then transitive closure — in that order."""
    return transitive_closure(
        symmetric_closure(reflexive_closure(pairs, elements)))


def warshall(pairs, elements):
    """Warshall's algorithm with one snapshot per pivot.

    Returns ``(closure_pairs, snapshots)`` where ``snapshots`` is a list of
    ``(pivot, matrix)`` — the matrix *after* the pass through that pivot, in
    the order the pivots are listed in ``elements``.
    """
    elements = list(elements)
    index = {element: i for i, element in enumerate(elements)}
    size = len(elements)
    matrix = [[0] * size for _ in range(size)]
    for a, b in as_pairs(pairs):
        matrix[index[a]][index[b]] = 1
    snapshots = []
    for k in range(size):
        for i in range(size):
            if matrix[i][k]:
                for j in range(size):
                    if matrix[k][j]:
                        matrix[i][j] = 1
        snapshots.append((elements[k], [row[:] for row in matrix]))
    return matrix_pairs(matrix, elements), snapshots


def relation_properties(pairs, elements):
    """``{'reflexive': bool, 'symmetric': ..., 'antisymmetric': ...,
    'transitive': ...}``."""
    pairs = as_pairs(pairs)
    elements = list(elements)
    return {
        "reflexive": all((a, a) in pairs for a in elements),
        "symmetric": all((b, a) in pairs for (a, b) in pairs),
        "antisymmetric": all(a == b for (a, b) in pairs if (b, a) in pairs),
        "transitive": all((a, c) in pairs
                          for (a, b) in pairs for (b2, c) in pairs
                          if b == b2),
    }


def property_witness(pairs, elements, prop):
    """First witness (canonical order) that ``prop`` fails, else ``None``.

    ``reflexive`` -> the missing element; ``symmetric``/``antisymmetric`` ->
    the offending pair; ``transitive`` -> the missing pair.
    """
    pairs = as_pairs(pairs)
    ordered = sorted(elements, key=sort_key)
    ordered_pairs = sorted(pairs, key=sort_key)
    if prop == "reflexive":
        for element in ordered:
            if (element, element) not in pairs:
                return element
        return None
    if prop == "symmetric":
        for (a, b) in ordered_pairs:
            if (b, a) not in pairs:
                return (a, b)
        return None
    if prop == "antisymmetric":
        for (a, b) in ordered_pairs:
            if a != b and (b, a) in pairs:
                return (a, b)
        return None
    if prop == "transitive":
        for (a, b) in ordered_pairs:
            for (b2, c) in ordered_pairs:
                if b == b2 and (a, c) not in pairs:
                    return (a, c)
        return None
    raise ValueError("unknown property %r" % prop)


def equivalence_classes(pairs, elements):
    """Blocks of the equivalence relation generated by ``pairs``, via union-find.

    Blocks are canonically sorted inside and ordered by least element — ready
    for :func:`partition_text`.
    """
    ordered = sorted(elements, key=sort_key)
    parent = {element: element for element in ordered}

    def find(item):
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union_(left, right):
        root_l, root_r = find(left), find(right)
        if root_l != root_r:
            parent[root_r] = root_l

    for a, b in as_pairs(pairs):
        if a in parent and b in parent:
            union_(a, b)
    blocks = {}
    for element in ordered:
        blocks.setdefault(find(element), []).append(element)
    out = [sorted(block, key=sort_key) for block in blocks.values()]
    out.sort(key=lambda block: sort_key(block[0]))
    return out


# ---------------------------------------------------------------------------
# Partial orders
# ---------------------------------------------------------------------------


def is_partial_order(pairs, elements):
    """Reflexive, antisymmetric and transitive on ``elements``."""
    props = relation_properties(pairs, elements)
    return props["reflexive"] and props["antisymmetric"] and props["transitive"]


def strict_part(pairs):
    """``<`` from ``≤`` — the order pairs with the diagonal removed."""
    return frozenset((a, b) for (a, b) in as_pairs(pairs) if a != b)


def cover_relation(pairs, elements):
    """Hasse edges: ``a < b`` with no ``c`` strictly between."""
    strict = strict_part(pairs)
    covers = set()
    for (a, b) in strict:
        blocked = any((a, c) in strict and (c, b) in strict
                      for c in elements if c != a and c != b)
        if not blocked:
            covers.add((a, b))
    return frozenset(covers)


def minimal_elements(pairs, elements):
    """Elements with nothing strictly below them, canonically ordered."""
    strict = strict_part(pairs)
    return [e for e in sorted(elements, key=sort_key)
            if not any(b == e for (_, b) in strict)]


def maximal_elements(pairs, elements):
    """Elements with nothing strictly above them, canonically ordered."""
    strict = strict_part(pairs)
    return [e for e in sorted(elements, key=sort_key)
            if not any(a == e for (a, _) in strict)]


def least_element(pairs, elements):
    """The element below everything, or ``None``."""
    order = as_pairs(pairs)
    for candidate in sorted(elements, key=sort_key):
        if all((candidate, other) in order for other in elements):
            return candidate
    return None


def greatest_element(pairs, elements):
    """The element above everything, or ``None``."""
    order = as_pairs(pairs)
    for candidate in sorted(elements, key=sort_key):
        if all((other, candidate) in order for other in elements):
            return candidate
    return None


def upper_bounds(pairs, elements, subset):
    """Elements above every member of ``subset``, canonically ordered."""
    order = as_pairs(pairs)
    return [e for e in sorted(elements, key=sort_key)
            if all((item, e) in order for item in subset)]


def lower_bounds(pairs, elements, subset):
    """Elements below every member of ``subset``, canonically ordered."""
    order = as_pairs(pairs)
    return [e for e in sorted(elements, key=sort_key)
            if all((e, item) in order for item in subset)]


def lub(pairs, elements, subset):
    """Least upper bound of ``subset``, or ``None``."""
    bounds = upper_bounds(pairs, elements, subset)
    return least_element(pairs, bounds) if bounds else None


def glb(pairs, elements, subset):
    """Greatest lower bound of ``subset``, or ``None``."""
    bounds = lower_bounds(pairs, elements, subset)
    return greatest_element(pairs, bounds) if bounds else None


def is_lattice(pairs, elements):
    """True when every pair of elements has both a lub and a glb."""
    elements = list(elements)
    for i, a in enumerate(elements):
        for b in elements[i:]:
            if lub(pairs, elements, [a, b]) is None:
                return False
            if glb(pairs, elements, [a, b]) is None:
                return False
    return True


def linear_extension(pairs, elements):
    """Topological order with the smallest-available-label tie-break.

    At each step the canonically smallest element whose strict predecessors
    are all placed is chosen, so the extension is unique.
    """
    strict = strict_part(pairs)
    remaining = sorted(elements, key=sort_key)
    placed = []
    while remaining:
        for candidate in remaining:
            if all(a in placed for (a, b) in strict if b == candidate):
                placed.append(candidate)
                remaining.remove(candidate)
                break
        else:
            raise ValueError("the relation has a cycle: no linear extension")
    return placed


def divisor_poset(n):
    """``(divisors, ≤ pairs)`` for divisibility on the divisors of ``n``."""
    divisors = [d for d in range(1, n + 1) if n % d == 0]
    pairs = frozenset((a, b) for a in divisors for b in divisors if b % a == 0)
    return divisors, pairs


def subset_poset(base):
    """``(subsets, ⊆ pairs)`` for the power set of ``base``."""
    subsets = powerset(base)
    pairs = frozenset((a, b) for a in subsets for b in subsets if a <= b)
    return subsets, pairs


# ---------------------------------------------------------------------------
# Functions given as tables
# ---------------------------------------------------------------------------


def function_pairs(table):
    """A dict ``{a: f(a)}`` as a relation."""
    return frozenset((key, value) for key, value in table.items())


def injective_witness(table):
    """First colliding ``(a1, a2, value)`` in canonical order, else ``None``."""
    keys = sorted(table, key=sort_key)
    for i, first in enumerate(keys):
        for second in keys[i + 1:]:
            if table[first] == table[second]:
                return (first, second, table[first])
    return None


def surjective_witness(table, codomain):
    """First element of ``codomain`` that is missed, else ``None``."""
    hit = set(table.values())
    for value in sorted(codomain, key=sort_key):
        if value not in hit:
            return value
    return None


def image(table, subset):
    """``f(S)``."""
    return frozenset(table[item] for item in subset if item in table)


def preimage(table, subset):
    """``f⁻¹(T)``."""
    subset = frozenset(subset)
    return frozenset(key for key, value in table.items() if value in subset)
