"""Construct finite relation closures with explicit added pairs and matrices.

Variants:
- ``reflexive`` adds exactly the missing diagonal pairs.
- ``symmetric`` adds exactly the missing reverse pairs.
- ``transitive_warshall`` shows the matrix after every ordered pivot.
- ``transitive_by_paths`` adds the first available two-edge consequence.
- ``equivalence_closure`` applies reflexive, symmetric, then transitive closure.

Op-codes:
- ``REL_SETUP``: define the finite carrier and starting relation.
- ``CLOSURE_ADD``: add one pair for reflexivity or symmetry.
- ``WARSHALL_K``: show the complete matrix after one pivot pass.
- ``PATH``: record a two-edge path and the transitive pair it forces.
- ``CHECK``: verify the requested closure property at the fixed point.
- ``Z``: exact canonical closure pair roster.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import (equivalence_closure, matrix_rows, reflexive_closure,
                        relation_text, roster, symmetric_closure,
                        transitive_closure, warshall)


FOUNDATIONS = True


QUERIES = {
    "reflexive": (
        "Find the reflexive closure of R on A.",
        "Add every missing diagonal pair and give the closure.",
        "Construct the smallest reflexive relation containing R.",
        "Complete the loops required for reflexivity.",
        "Compute R with exactly the missing (a, a) pairs added.",
    ),
    "symmetric": (
        "Find the symmetric closure of R.",
        "Add every missing reverse pair and give the closure.",
        "Construct the smallest symmetric relation containing R.",
        "Complete each directed pair with its reverse.",
        "Compute R ∪ R⁻¹ in canonical pair order.",
    ),
    "transitive_warshall": (
        "Find the transitive closure using Warshall's ordered pivots.",
        "Run one Warshall pass per element of A and give the final relation.",
        "Compute reachability with the stated row and pivot order.",
        "Show every pivot matrix before reporting the transitive closure.",
        "Use Warshall's algorithm to construct R⁺.",
    ),
    "transitive_by_paths": (
        "Find the transitive closure by adding forced two-edge paths.",
        "Add the first missing path consequence until no pair is missing.",
        "Compute R⁺ one composable path at a time.",
        "Close the relation transitively using ordered path additions.",
        "Repeat a→b and b→c imply a→c to a fixed point.",
    ),
    "equivalence_closure": (
        "Find the equivalence closure in reflexive-symmetric-transitive order.",
        "Add loops, then reverses, then all forced path pairs.",
        "Construct the smallest equivalence relation containing R.",
        "Apply the three equivalence closures in the stated order.",
        "Complete R to a reflexive, symmetric, transitive relation.",
    ),
}


def random_carrier():
    return tuple(sorted(random.sample(range(1, 41), random.randint(3, 5))))


def random_pairs(values, probability=0.25):
    return frozenset((first, second) for first in values for second in values
                     if random.random() < probability)


def path_trace(pairs):
    current = set(pairs)
    trace = []
    while True:
        options = sorted((first, middle, last)
                         for first, middle in current
                         for middle_two, last in current
                         if middle == middle_two and (first, last) not in current)
        if not options:
            return frozenset(current), trace
        first, middle, last = options[0]
        current.add((first, last))
        trace.append((first, middle, last))


class RelationClosureGenerator(ProblemGenerator):
    """Generate exact closure records on small finite directed graphs."""

    VARIANTS = ("reflexive", "symmetric", "transitive_warshall",
                "transitive_by_paths", "equivalence_closure")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _relation_for(values, variant):
        if variant == "reflexive":
            relation = set(random_pairs(values))
            missing = random.choice(values)
            relation.discard((missing, missing))
            return frozenset(relation)
        if variant == "symmetric":
            relation = set(random_pairs(values))
            first, second = random.sample(values, 2)
            relation.add((first, second))
            relation.discard((second, first))
            return frozenset(relation)
        if variant in ("transitive_warshall", "transitive_by_paths"):
            first, middle, last = random.sample(values, 3)
            relation = set(random_pairs(values, 0.18))
            relation.add((first, middle))
            relation.add((middle, last))
            relation.discard((first, last))
            return frozenset(relation)
        relation = random_pairs(values, 0.2)
        if relation:
            return relation
        first, second = random.sample(values, 2)
        return frozenset({(first, second)})

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        values = random_carrier()
        relation = self._relation_for(values, variant)
        problem = (f"A = {roster(values)}. R = {relation_text(relation)}. "
                   f"{random.choice(QUERIES[variant])}")
        steps = [step("REL_SETUP", f"A = {roster(values)}",
                      f"R = {relation_text(relation)}")]
        if variant == "reflexive":
            result = reflexive_closure(relation, values)
            for pair in sorted(result - relation):
                steps.append(step("CLOSURE_ADD", f"({pair[0]}, {pair[1]})",
                                  "reflexive"))
            steps.append(step("CHECK", "reflexive", "no missing loop"))
        elif variant == "symmetric":
            result = symmetric_closure(relation)
            for pair in sorted(result - relation):
                steps.append(step("CLOSURE_ADD", f"({pair[0]}, {pair[1]})",
                                  "symmetric"))
            steps.append(step("CHECK", "symmetric", "no missing reverse"))
        elif variant == "transitive_warshall":
            result, snapshots = warshall(relation, values)
            for pivot, _matrix in snapshots:
                rows = matrix_rows(result if pivot == values[-1] else
                                   _matrix_to_pairs(_matrix, values), values)
                steps.append(step("WARSHALL_K", f"k={pivot}", "; ".join(rows)))
            steps.append(step("CHECK", "transitive", "no missing pair"))
        elif variant == "transitive_by_paths":
            result, trace = path_trace(relation)
            for first, middle, last in trace:
                steps.append(step("PATH", f"{first}→{middle}→{last}",
                                  f"add ({first}, {last})"))
            steps.append(step("CHECK", "transitive", "no missing pair"))
        else:
            current = set(relation)
            reflexive = reflexive_closure(current, values)
            for pair in sorted(reflexive - current):
                steps.append(step("CLOSURE_ADD", f"({pair[0]}, {pair[1]})",
                                  "reflexive"))
            current = set(reflexive)
            symmetric = symmetric_closure(current)
            for pair in sorted(symmetric - current):
                steps.append(step("CLOSURE_ADD", f"({pair[0]}, {pair[1]})",
                                  "symmetric"))
            result, trace = path_trace(symmetric)
            for first, middle, last in trace:
                steps.append(step("PATH", f"{first}→{middle}→{last}",
                                  f"add ({first}, {last})"))
            # Keep the shared helper as a final implementation cross-check.
            if result != equivalence_closure(relation, values):
                raise RuntimeError("equivalence closure algorithms disagree")
            steps.append(step("CHECK", "equivalence", "all three properties"))
        answer = relation_text(result)
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"relation_closure_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }


def _matrix_to_pairs(matrix, values):
    return frozenset((values[row], values[column])
                     for row in range(len(values))
                     for column in range(len(values)) if matrix[row][column])
