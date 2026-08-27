"""Analyze finite partial orders from divisibility, inclusion, or Hasse data.

Variants:
- ``hasse_edges`` computes the cover relation.
- ``extremal_elements`` finds minimal/maximal/least/greatest elements.
- ``bounds_lub_glb`` computes bounds and extrema for a two-element subset.
- ``linear_extension`` uses the smallest-available-element tie-break.
- ``lattice_check`` checks every unordered pair for a lub and glb.
- ``chains_antichains`` gives canonical maximum examples by enumeration.

Op-codes:
- ``ORDER_PAIR`` / ``COVER``: justify strict order and Hasse pairs.
- ``MINIMAL`` / ``MAXIMAL`` / ``LEAST`` / ``GREATEST``: order extrema.
- ``UB`` / ``LB`` / ``LUB`` / ``GLB``: bound calculations.
- ``TOPO_PICK``: one forced topological-sort choice.
- ``LATTICE_PAIR``: the lub/glb result for an unordered pair.
- ``CHAIN`` / ``ANTICHAIN``: canonical maximum comparable/incomparable sets.
- ``CHECK``: finite exhaustive verification.
- ``Z``: exact composite, pair-roster, or ordered-sequence answer.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import (cover_relation, divisor_poset, fmt_element, glb,
                        greatest_element, is_lattice, least_element,
                        linear_extension, lub, maximal_elements,
                        minimal_elements, pair, powerset, reflexive_closure,
                        relation_text, roster, sequence_text, sort_key,
                        subset_poset, transitive_closure, upper_bounds,
                        lower_bounds)


FOUNDATIONS = True


LETTERS = tuple("abcdefghijklmnopqrst")
COMPOSITES = tuple(value for value in range(12, 61)
                   if sum(value % divisor == 0
                          for divisor in range(1, value + 1)) >= 5)

QUERIES = {
    "hasse_edges": (
        "Find the Hasse edges of this finite poset.",
        "Remove every transitive order pair and give the cover relation.",
        "List exactly the pairs a ≺ b with no element strictly between.",
        "Compute the cover pairs for the Hasse diagram.",
        "Give the canonical pair roster of immediate order steps.",
    ),
    "extremal_elements": (
        "Find the minimal, maximal, least, and greatest elements.",
        "Classify all four kinds of order extrema.",
        "Use the strict order to determine minima, maxima, bottom, and top.",
        "Report the extremal-element sets and any global extrema.",
        "Analyze the finite poset's minimal and maximal structure.",
    ),
    "bounds_lub_glb": (
        "Find the upper bounds, lower bounds, lub, and glb of Q.",
        "Compute all bounds of Q and identify their least/greatest choices.",
        "Determine sup(Q) and inf(Q) when they exist.",
        "List the common bounds before giving the lub and glb.",
        "Use the finite order to analyze the stated two-element subset.",
    ),
    "linear_extension": (
        "Find the linear extension by choosing the smallest available element.",
        "Topologically sort the poset with the stated canonical tie-break.",
        "At each step pick the least label whose predecessors are placed.",
        "Give the forced lexicographically first linear extension.",
        "Produce the canonical total ordering that extends this poset.",
    ),
    "lattice_check": (
        "Determine whether every pair has both a lub and a glb.",
        "Check whether this finite poset is a lattice.",
        "Test all unordered pairs and give the first failed bound if any.",
        "Classify the poset as a lattice or not with a canonical witness.",
        "Verify the meet-and-join condition throughout the poset.",
    ),
    "chains_antichains": (
        "Find a maximum chain and a maximum antichain.",
        "Enumerate subsets and choose the canonical largest comparable and incomparable sets.",
        "Give lexicographically first maximum chain and antichain witnesses.",
        "Determine the height and width witnesses of this poset.",
        "Find largest chain and antichain subsets with the stated tie-break.",
    ),
}


def explicit_poset():
    elements = tuple(sorted(random.sample(range(1, 61), random.randint(5, 7))))
    edges = {(left, right)
             for index, left in enumerate(elements)
             for right in elements[index + 1:]
             if random.random() < 0.27}
    if not edges:
        edges.add((elements[0], elements[-1]))
    strict = transitive_closure(edges)
    order = reflexive_closure(strict, elements)
    covers = cover_relation(order, elements)
    return elements, order, covers


def make_poset(force_explicit=False):
    family = "explicit" if force_explicit else random.choices(
        ("divisibility", "subset", "explicit"), weights=(1, 1, 8), k=1)[0]
    if family == "divisibility":
        number = random.choice(COMPOSITES)
        elements, order = divisor_poset(number)
        elements = tuple(elements)
        description = (f"Carrier A = {roster(elements)}. "
                       "Order rule: a ≤ b iff a divides b.")
        reason = "divides"
    elif family == "subset":
        base = tuple(sorted(random.sample(LETTERS, 3)))
        elements, order = subset_poset(base)
        elements = tuple(elements)
        description = (f"Base B = {roster(base)}. Carrier A = {roster(elements)}. "
                       "Order rule: X ≤ Y iff X ⊆ Y.")
        reason = "subset"
    else:
        elements, order, covers = explicit_poset()
        description = (f"Carrier A = {roster(elements)}. "
                       f"Hasse edges H = {relation_text(covers)}. "
                       "Order rule: reflexive-transitive closure of H.")
        reason = "reachable"
    return family, elements, frozenset(order), description, reason


def value_text(value):
    return fmt_element(value)


def maximum_chain_antichain(order, elements):
    ordered = tuple(sorted(elements, key=sort_key))
    best_chain = ()
    best_antichain = ()
    for size in range(len(ordered) + 1):
        for subset in itertools.combinations(ordered, size):
            chain = all((first, second) in order or (second, first) in order
                        for first, second in itertools.combinations(subset, 2))
            antichain = all((first, second) not in order
                            and (second, first) not in order
                            for first, second in itertools.combinations(subset, 2))
            if chain and len(subset) > len(best_chain):
                best_chain = subset
            if antichain and len(subset) > len(best_antichain):
                best_antichain = subset
    return best_chain, best_antichain


def extrema_answer(order, elements):
    minima = minimal_elements(order, elements)
    maxima = maximal_elements(order, elements)
    least = least_element(order, elements)
    greatest = greatest_element(order, elements)
    return (f"minimal {roster(minima)}; maximal {roster(maxima)}; "
            f"least {value_text(least) if least is not None else 'none'}; "
            f"greatest {value_text(greatest) if greatest is not None else 'none'}")


class PartialOrderGenerator(ProblemGenerator):
    """Generate finite-poset tasks with canonical witnesses and tie-breaks."""

    VARIANTS = ("hasse_edges", "extremal_elements", "bounds_lub_glb",
                "linear_extension", "lattice_check", "chains_antichains")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        family, elements, order, description, reason = make_poset(
            force_explicit=variant in ("linear_extension", "chains_antichains"))
        query = random.choice(QUERIES[variant])
        steps = []
        if variant == "hasse_edges":
            covers = cover_relation(order, elements)
            for first, second in sorted(order, key=sort_key):
                if first != second:
                    if reason == "divides":
                        why = f"{second} is a multiple of {first}"
                    elif reason == "subset":
                        why = f"{value_text(first)} ⊆ {value_text(second)}"
                    else:
                        why = "reachable in H"
                    steps.append(step("ORDER_PAIR",
                                      f"{value_text(first)} ≤ {value_text(second)}",
                                      why))
            for first, second in sorted(covers, key=sort_key):
                steps.append(step("COVER", value_text(first), value_text(second),
                                  "no c strictly between"))
            answer = relation_text(covers)
            problem = f"{description} {query}"
        elif variant == "extremal_elements":
            minima = minimal_elements(order, elements)
            maxima = maximal_elements(order, elements)
            least = least_element(order, elements)
            greatest = greatest_element(order, elements)
            steps.extend((step("MINIMAL", roster(minima)),
                          step("MAXIMAL", roster(maxima)),
                          step("LEAST", value_text(least) if least is not None else "none"),
                          step("GREATEST", value_text(greatest) if greatest is not None else "none")))
            answer = extrema_answer(order, elements)
            problem = f"{description} {query}"
        elif variant == "bounds_lub_glb":
            subset = tuple(sorted(random.sample(list(elements), 2), key=sort_key))
            uppers = upper_bounds(order, elements, subset)
            lowers = lower_bounds(order, elements, subset)
            least_upper, greatest_lower = (lub(order, elements, subset),
                                           glb(order, elements, subset))
            steps.extend((step("UB", roster(subset), roster(uppers)),
                          step("LB", roster(subset), roster(lowers)),
                          step("LUB", value_text(least_upper)
                               if least_upper is not None else "none"),
                          step("GLB", value_text(greatest_lower)
                               if greatest_lower is not None else "none")))
            answer = (f"lub {value_text(least_upper) if least_upper is not None else 'none'}; "
                      f"glb {value_text(greatest_lower) if greatest_lower is not None else 'none'}")
            problem = f"{description} Q = {roster(subset)}. {query}"
        elif variant == "linear_extension":
            extension = linear_extension(order, elements)
            placed = []
            remaining = list(sorted(elements, key=sort_key))
            strict = {(first, second) for first, second in order if first != second}
            while remaining:
                available = [candidate for candidate in remaining
                             if all(first in placed for first, second in strict
                                    if second == candidate)]
                chosen = available[0]
                steps.append(step("TOPO_PICK", f"available {roster(available)}",
                                  f"pick {value_text(chosen)}"))
                placed.append(chosen)
                remaining.remove(chosen)
            answer = sequence_text(extension)
            problem = f"{description} {query}"
        elif variant == "lattice_check":
            failure = None
            ordered = tuple(sorted(elements, key=sort_key))
            for index, first in enumerate(ordered):
                for second in ordered[index:]:
                    pair_subset = (first, second)
                    pair_lub = lub(order, elements, pair_subset)
                    pair_glb = glb(order, elements, pair_subset)
                    steps.append(step(
                        "LATTICE_PAIR", pair(first, second),
                        f"lub {value_text(pair_lub) if pair_lub is not None else 'none'}",
                        f"glb {value_text(pair_glb) if pair_glb is not None else 'none'}"))
                    if failure is None and (pair_lub is None or pair_glb is None):
                        failure = (first, second,
                                   "lub" if pair_lub is None else "glb")
            lattice = is_lattice(order, elements)
            if lattice:
                answer = "lattice yes"
            else:
                first, second, missing = failure
                answer = f"lattice no; pair {pair(first, second)} lacks {missing}"
            steps.append(step("CHECK", "all unordered pairs",
                              "lattice" if lattice else "first failure recorded"))
            problem = f"{description} {query}"
        else:
            chain, antichain = maximum_chain_antichain(order, elements)
            steps.append(step("CHAIN", roster(chain), f"length {len(chain)}"))
            steps.append(step("ANTICHAIN", roster(antichain),
                              f"size {len(antichain)}"))
            steps.append(step("CHECK", f"all {2 ** len(elements)} subsets",
                              "maximum sizes verified"))
            answer = f"chain {roster(chain)}; antichain {roster(antichain)}"
            problem = f"{description} {query}"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"partial_order_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
