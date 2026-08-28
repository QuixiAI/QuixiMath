"""Check and find isomorphisms of finite binary structures.

Variants: ``check_given_map``, ``find_map``, and
``non_isomorphic_invariant``. Structures are directed graphs, relations, or
strict finite posets. Op-codes: ``INVARIANT``, ``TRY``, ``REJECT``,
``EDGE_CHECK``, ``ACCEPT``, ``CHECK``, and ``Z``. Random labels and relations
give an unbounded problem space.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True
KINDS = ("directed graph", "relation", "strict poset")
LETTERS = tuple("abcdefghjkmnpqrstuvwxyz")

QUERIES = {
    "check_given_map": (
        "Decide whether the displayed bijection is an isomorphism.",
        "Check whether f preserves and reflects every related pair.",
        "Verify the proposed structure isomorphism exactly.",
        "Test the given relabelling against the two relations.",
        "Classify f and give the first pair discrepancy when it fails.",
    ),
    "find_map": (
        "Find the first isomorphism in the required lexicographic order.",
        "Search the bijections canonically and report the first one that works.",
        "Use degree pruning, then return the lexicographically first isomorphism.",
        "Determine the canonical relation-preserving bijection.",
        "Test maps in the stated order and give the first isomorphism.",
    ),
    "non_isomorphic_invariant": (
        "Give the first invariant in the stated order that proves non-isomorphism.",
        "Compare the invariants canonically and stop at the first difference.",
        "Certify non-isomorphism with the earliest displayed invariant.",
        "Identify the first structural count that differs.",
        "Use the ordered invariant test to rule out an isomorphism.",
    ),
}


def relation_text(edges, order):
    if not edges:
        return "∅"
    position = {value: index for index, value in enumerate(order)}
    pairs = sorted(edges, key=lambda edge: (position[edge[0]],
                                            position[edge[1]]))
    return "{" + ", ".join(f"({a}, {b})" for a, b in pairs) + "}"


def points_text(points):
    return "{" + ", ".join(str(point) for point in points) + "}"


def map_text(mapping, left):
    return ", ".join(f"{value}→{mapping[value]}" for value in left)


def pair_text(pair):
    return f"({pair[0]}, {pair[1]})"


def random_labels(size):
    left = tuple(sorted(random.sample(range(1, 10000), size)))
    right = tuple(sorted(random.sample(LETTERS, size)))
    return left, right


def transitive_closure(edges, nodes):
    result = set(edges)
    changed = True
    while changed:
        changed = False
        for a, b in tuple(result):
            for c, d in tuple(result):
                if b == c and a != d and (a, d) not in result:
                    result.add((a, d))
                    changed = True
    return result


def random_relation(nodes, kind):
    if kind == "strict poset":
        linear = list(nodes)
        random.shuffle(linear)
        edges = {(linear[i], linear[j])
                 for i in range(len(nodes)) for j in range(i + 1, len(nodes))
                 if random.random() < 0.38}
        return transitive_closure(edges, nodes)
    return {(a, b) for a in nodes for b in nodes if random.random() < 0.34}


def rename(edges, mapping):
    return {(mapping[a], mapping[b]) for a, b in edges}


def degrees(edges, nodes):
    return {node: (sum((node, other) in edges for other in nodes),
                   sum((other, node) in edges for other in nodes))
            for node in nodes}


def first_discrepancy(left, right, mapping, left_nodes):
    for a in left_nodes:
        for b in left_nodes:
            source = (a, b) in left
            target_pair = (mapping[a], mapping[b])
            if source != (target_pair in right):
                return (a, b), target_pair, source
    return None


def canonical_map(left_edges, right_edges, left_nodes, right_nodes):
    left_degrees = degrees(left_edges, left_nodes)
    right_degrees = degrees(right_edges, right_nodes)
    rejected = []
    for permutation in itertools.permutations(right_nodes):
        mapping = dict(zip(left_nodes, permutation))
        mismatch = next((node for node in left_nodes
                         if left_degrees[node] != right_degrees[mapping[node]]),
                        None)
        if mismatch is not None:
            rejected.append((mapping, f"degree mismatch at {mismatch}"))
            continue
        discrepancy = first_discrepancy(
            left_edges, right_edges, mapping, left_nodes)
        if discrepancy is not None:
            rejected.append((mapping, f"pair mismatch at {discrepancy[0]}"))
            continue
        return mapping, rejected
    raise ValueError("constructed structures are not isomorphic")


def invariant_values(edges, nodes):
    out_degrees = sorted(sum((node, other) in edges for other in nodes)
                         for node in nodes)
    two_cycles = sum((a, b) in edges and (b, a) in edges
                     for index, a in enumerate(nodes)
                     for b in nodes[index + 1:])
    fixed = sum((node, node) in edges for node in nodes)
    return len(nodes), out_degrees, two_cycles, fixed


class StructureIsomorphismGenerator(ProblemGenerator):
    """Generate exact finite-structure isomorphism exercises."""

    VARIANTS = ("check_given_map", "find_map", "non_isomorphic_invariant")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _structure_prefix(kind, left, left_edges, right, right_edges):
        return (f"Structure kind: {kind}. Left points: {points_text(left)}; "
                f"left relation: {relation_text(left_edges, left)}. Right "
                f"points: {points_text(right)}; right relation: "
                f"{relation_text(right_edges, right)}.")

    def _check_given_map(self):
        size = random.choice((3, 4))
        left, right = random_labels(size)
        kind = random.choice(KINDS)
        left_edges = random_relation(left, kind)
        permutation = random.sample(right, size)
        mapping = dict(zip(left, permutation))
        right_edges = rename(left_edges, mapping)
        if random.choice((True, False)):
            toggle = random.choice([(a, b) for a in right for b in right])
            if toggle in right_edges:
                right_edges.remove(toggle)
            else:
                right_edges.add(toggle)
        discrepancy = first_discrepancy(
            left_edges, right_edges, mapping, left)
        displayed_map = map_text(mapping, left)
        problem = (self._structure_prefix(
            kind, left, left_edges, right, right_edges) +
            f" Given bijection: f = {displayed_map}. " +
            random.choice(QUERIES["check_given_map"]))
        steps = [step("TRY", f"f = {displayed_map}")]
        if discrepancy is None:
            for a in left:
                for b in left:
                    target = (mapping[a], mapping[b])
                    status = "present" if (a, b) in left_edges else "absent"
                    steps.append(step("EDGE_CHECK", f"({a}, {b})",
                                      f"({target[0]}, {target[1]})", status))
            answer = f"isomorphism; f = {displayed_map}"
            steps.append(step("ACCEPT", answer))
        else:
            source, target, source_present = discrepancy
            target_status = "absent" if source_present else "present"
            answer = (f"not an isomorphism; pair {pair_text(source)} maps to "
                      f"{pair_text(target)}, "
                      f"which is {target_status}")
            steps.append(step("EDGE_CHECK", pair_text(source),
                              pair_text(target),
                              "mismatch"))
            steps.append(step("REJECT", f"f = {displayed_map}", answer))
        return problem, steps, answer

    def _find_map(self):
        size = random.choice((3, 4))
        left, right = random_labels(size)
        kind = random.choice(KINDS)
        left_edges = random_relation(left, kind)
        hidden = dict(zip(left, random.sample(right, size)))
        right_edges = rename(left_edges, hidden)
        mapping, rejected = canonical_map(
            left_edges, right_edges, left, right)
        problem = (self._structure_prefix(
            kind, left, left_edges, right, right_edges) +
            " Test bijections in lexicographic order of the right-side image "
            "tuple. " + random.choice(QUERIES["find_map"]))
        steps = [step("REJECT", f"f = {map_text(candidate, left)}", reason)
                 for candidate, reason in rejected]
        displayed_map = map_text(mapping, left)
        steps.append(step("TRY", f"f = {displayed_map}"))
        for a in left:
            for b in left:
                target = (mapping[a], mapping[b])
                status = "present" if (a, b) in left_edges else "absent"
                steps.append(step("EDGE_CHECK", f"({a}, {b})",
                                  f"({target[0]}, {target[1]})", status))
        answer = f"isomorphic; f = {displayed_map}"
        steps.append(step("ACCEPT", answer))
        return problem, steps, answer

    def _non_isomorphic(self):
        case = random.randrange(4)
        left_size = 3
        right_size = 4 if case == 0 else 3
        left, _ = random_labels(left_size)
        _, right = random_labels(right_size)
        kind = random.choice(KINDS if case < 2 else KINDS[:2])
        if case == 0:
            left_edges = random_relation(left, kind)
            right_edges = random_relation(right, kind)
        elif case == 1:
            left_edges = random_relation(left, kind)
            while True:
                right_edges = random_relation(right, kind)
                if invariant_values(left_edges, left)[1] != invariant_values(right_edges, right)[1]:
                    break
        else:
            cycle_pair = ({(1, 0), (0, 0)}, {(0, 1), (1, 0)})
            fixed_pair = ({(0, 0)}, {(0, 1)})
            template_left, template_right = cycle_pair if case == 2 else fixed_pair
            left_edges = {(left[a], left[b]) for a, b in template_left}
            right_edges = {(right[a], right[b]) for a, b in template_right}
        left_values = invariant_values(left_edges, left)
        right_values = invariant_values(right_edges, right)
        labels = ("sizes", "out-degree multisets", "directed 2-cycle counts",
                  "fixed-point counts")
        index = next(i for i, values in enumerate(zip(left_values, right_values))
                     if values[0] != values[1])
        left_value, right_value = left_values[index], right_values[index]
        answer = (f"not isomorphic; {labels[index]} differ "
                  f"({left_value} vs {right_value})")
        problem = (self._structure_prefix(
            kind, left, left_edges, right, right_edges) +
            " Invariant order: sizes; out-degree multisets; directed 2-cycle "
            "counts; fixed-point counts. " +
            random.choice(QUERIES["non_isomorphic_invariant"]))
        steps = [step("INVARIANT", labels[i], left_values[i], right_values[i])
                 for i in range(index + 1)]
        steps.append(step("CHECK", "first differing invariant", answer))
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "check_given_map":
            problem, steps, answer = self._check_given_map()
        elif variant == "find_map":
            problem, steps, answer = self._find_map()
        else:
            problem, steps, answer = self._non_isomorphic()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"structure_isomorphism_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
