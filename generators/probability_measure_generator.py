"""Apply finite probability measures to sets, identities, and conditioning.

Variants: ``set_expression``, ``derive_identity``, ``monotonicity``,
``inclusion_exclusion_three``, ``union_bound_compare``, and ``renormalize``.
Op-codes: ``WEIGHT``, ``SUBEXPR``, ``MEASURE``, ``AXIOM``, ``IE_FORMULA``,
``RENORMALIZE``, ``A``, ``S``, ``D``, ``CMP``, ``CHECK``, and ``Z``.
Random weighted atoms, events, expressions, and five phrasings give an
unbounded problem space.
"""
import random
import string
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
EXPRESSIONS = {
    "union_complement_or_intersection": "(A ∪ B)ᶜ ∪ (A ∩ B)",
    "symmetric_differences": "(A − B) ∪ (B − A)",
    "exclusive_membership": "(A ∩ Bᶜ) ∪ (Aᶜ ∩ B)",
    "union_minus_intersection": "(A ∪ B) − (A ∩ B)",
    "matching_membership": "(A ∩ B) ∪ (Aᶜ ∩ Bᶜ)",
}
QUERIES = {
    "set_expression": (
        "Evaluate the set expression and find its probability.",
        "Reduce the displayed set operations, then measure the resulting event.",
        "Find the event roster and add its atomic weights.",
        "Use the finite measure to compute the exact value of the expression.",
        "Determine the set first and its probability second.",
    ),
    "derive_identity": (
        "Verify P(B − A) = P(B) − P(A ∩ B) numerically.",
        "Measure both sides of the set-difference identity.",
        "Compute P(B − A), P(B), and P(A ∩ B), then compare.",
        "Use disjoint additivity to demonstrate the displayed identity.",
        "Report both exact sides of the probability identity.",
    ),
    "monotonicity": (
        "Verify monotonicity for A ⊆ B using the given weights.",
        "Compute both measures and show that the subset has no larger probability.",
        "Apply the monotonicity axiom to the displayed nested events.",
        "Measure A and B, then state their exact inequality.",
        "Confirm P(A) ≤ P(B) from the atomic weights.",
    ),
    "inclusion_exclusion_three": (
        "Use three-set inclusion-exclusion to find P(A ∪ B ∪ C).",
        "Measure every required intersection and compute the three-event union.",
        "Apply the full singles-minus-pairs-plus-triple formula.",
        "Find the exact probability that at least one of A, B, and C occurs.",
        "Determine the union measure from all seven component measures.",
    ),
    "union_bound_compare": (
        "Compute P(A ∪ B) and compare it with the union bound P(A) + P(B).",
        "Verify Boole's inequality numerically for these two events.",
        "Measure the union and the sum of the individual probabilities.",
        "Show the exact union is no greater than the sum bound.",
        "Report both sides of the two-event union-bound comparison.",
    ),
    "renormalize": (
        "Condition on B and give the renormalized weight of every atom in B.",
        "Build the conditional measure on B by dividing each included weight by P(B).",
        "Renormalize the atomic probabilities onto the displayed event B.",
        "Find all nonzero probabilities under P(· given B) and state that the others are zero.",
        "Compute the conditional atom distribution and verify that it sums to 1.",
    ),
}


def _random_event(universe, minimum=1, maximum=None):
    maximum = maximum if maximum is not None else len(universe) - 1
    return frozenset(random.sample(universe, random.randint(minimum, maximum)))


def _measure_steps(label, members, universe, weights):
    ordered = [atom for atom in universe if atom in members]
    values = [weights[atom] for atom in ordered]
    steps = []
    if len(values) >= 2:
        running = values[0]
        for value in values[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(value),
                              prob_txt(running + value)))
            running += value
    total = sum(values, Fraction())
    steps.append(step("MEASURE", label, roster(ordered), prob_txt(total)))
    return steps, total


def _expression_path(kind, universe, set_a, set_b):
    if kind == "union_complement_or_intersection":
        union = set_a | set_b
        outside = universe - union
        inter = set_a & set_b
        return [("A ∪ B", union), ("(A ∪ B)ᶜ", outside),
                ("A ∩ B", inter), (EXPRESSIONS[kind], outside | inter)]
    if kind == "symmetric_differences":
        left, right = set_a - set_b, set_b - set_a
        return [("A − B", left), ("B − A", right),
                (EXPRESSIONS[kind], left | right)]
    if kind == "exclusive_membership":
        left, right = set_a & (universe - set_b), (universe - set_a) & set_b
        return [("Bᶜ", universe - set_b), ("A ∩ Bᶜ", left),
                ("Aᶜ", universe - set_a), ("Aᶜ ∩ B", right),
                (EXPRESSIONS[kind], left | right)]
    if kind == "union_minus_intersection":
        union, inter = set_a | set_b, set_a & set_b
        return [("A ∪ B", union), ("A ∩ B", inter),
                (EXPRESSIONS[kind], union - inter)]
    inter = set_a & set_b
    outside = (universe - set_a) & (universe - set_b)
    return [("A ∩ B", inter), ("Aᶜ", universe - set_a),
            ("Bᶜ", universe - set_b), ("Aᶜ ∩ Bᶜ", outside),
            (EXPRESSIONS[kind], inter | outside)]


class ProbabilityMeasureGenerator(ProblemGenerator):
    """Generate exact calculations for finite probability measures."""

    VARIANTS = ("set_expression", "derive_identity", "monotonicity",
                "inclusion_exclusion_three", "union_bound_compare",
                "renormalize")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _space(variant):
        atoms = tuple(string.ascii_lowercase[:random.randint(5, 8)])
        counts = [random.randint(1, 50) for _ in atoms]
        total = sum(counts)
        weights = {atom: Fraction(count, total)
                   for atom, count in zip(atoms, counts)}
        universe = frozenset(atoms)
        if variant == "monotonicity":
            set_b = _random_event(atoms, 2, len(atoms) - 1)
            set_a = frozenset(random.sample(tuple(sorted(set_b)),
                                            random.randint(1, len(set_b) - 1)))
        elif variant == "union_bound_compare":
            while True:
                set_a, set_b = _random_event(atoms), _random_event(atoms)
                if (sum((weights[atom] for atom in set_a), Fraction()) +
                        sum((weights[atom] for atom in set_b), Fraction()) <= 1):
                    break
        else:
            set_a = _random_event(atoms)
            set_b = _random_event(atoms, 2 if variant == "renormalize" else 1)
        set_c = _random_event(atoms) if variant == "inclusion_exclusion_three" else None
        weight_text = "; ".join(
            f"P({atom}) = {prob_txt(weights[atom])}" for atom in atoms)
        prefix = (f"Ω = {roster(atoms)}. Weights: {weight_text}. "
                  f"A = {roster(sorted(set_a))}. B = {roster(sorted(set_b))}.")
        if set_c is not None:
            prefix += f" C = {roster(sorted(set_c))}."
        steps = [step("WEIGHT", atom, prob_txt(weights[atom])) for atom in atoms]
        return atoms, universe, weights, set_a, set_b, set_c, prefix, steps

    @classmethod
    def _set_expression(cls):
        atoms, universe, weights, set_a, set_b, _, prefix, steps = cls._space(
            "set_expression")
        kind = random.choice(tuple(EXPRESSIONS))
        path = _expression_path(kind, universe, set_a, set_b)
        for label, members in path:
            steps.append(step("SUBEXPR", label, roster(
                atom for atom in atoms if atom in members)))
        result = path[-1][1]
        steps.append(step("AXIOM", "finite additivity",
                          "P(E) = sum of the weights of atoms in E"))
        measure_steps, value = _measure_steps(EXPRESSIONS[kind], result,
                                              atoms, weights)
        steps.extend(measure_steps)
        return f"{prefix} Expression: {EXPRESSIONS[kind]}.", steps, prob_txt(value)

    @classmethod
    def _derive_identity(cls):
        atoms, _, weights, set_a, set_b, _, prefix, steps = cls._space(
            "derive_identity")
        difference, intersection = set_b - set_a, set_a & set_b
        left_steps, left = _measure_steps("B − A", difference, atoms, weights)
        b_steps, p_b = _measure_steps("B", set_b, atoms, weights)
        i_steps, p_inter = _measure_steps("A ∩ B", intersection, atoms, weights)
        steps.extend(left_steps + b_steps + i_steps)
        steps.append(step("AXIOM", "disjoint additivity",
                          "B = (B − A) ∪ (A ∩ B) with disjoint parts"))
        steps.append(step("S", prob_txt(p_b), prob_txt(p_inter),
                          prob_txt(p_b - p_inter)))
        steps.append(step("CHECK", "identity sides", prob_txt(left),
                          prob_txt(p_b - p_inter)))
        answer = (f"P(B − A) = {prob_txt(left)}; "
                  f"P(B) − P(A ∩ B) = {prob_txt(p_b - p_inter)}")
        return prefix, steps, answer

    @classmethod
    def _monotonicity(cls):
        atoms, _, weights, set_a, set_b, _, prefix, steps = cls._space(
            "monotonicity")
        a_steps, p_a = _measure_steps("A", set_a, atoms, weights)
        b_steps, p_b = _measure_steps("B", set_b, atoms, weights)
        steps.extend(a_steps + b_steps)
        steps.append(step("AXIOM", "monotonicity", "A ⊆ B implies P(A) ≤ P(B)"))
        steps.append(step("CMP", prob_txt(p_a), prob_txt(p_b), "≤"))
        answer = (f"A ⊆ B; P(A) = {prob_txt(p_a)} ≤ "
                  f"P(B) = {prob_txt(p_b)}")
        return prefix, steps, answer

    @classmethod
    def _inclusion_exclusion(cls):
        atoms, _, weights, set_a, set_b, set_c, prefix, steps = cls._space(
            "inclusion_exclusion_three")
        events = (("A", set_a), ("B", set_b), ("C", set_c),
                  ("A ∩ B", set_a & set_b), ("A ∩ C", set_a & set_c),
                  ("B ∩ C", set_b & set_c),
                  ("A ∩ B ∩ C", set_a & set_b & set_c))
        measures = {}
        for label, members in events:
            event_steps, measures[label] = _measure_steps(label, members,
                                                          atoms, weights)
            steps.extend(event_steps)
        steps.append(step("IE_FORMULA",
                          "P(A ∪ B ∪ C) = singles − pairs + triple"))
        running = measures["A"] + measures["B"]
        steps.append(step("A", prob_txt(measures["A"]), prob_txt(measures["B"]),
                          prob_txt(running)))
        steps.append(step("A", prob_txt(running), prob_txt(measures["C"]),
                          prob_txt(running + measures["C"])))
        running += measures["C"]
        for label in ("A ∩ B", "A ∩ C", "B ∩ C"):
            steps.append(step("S", prob_txt(running), prob_txt(measures[label]),
                              prob_txt(running - measures[label])))
            running -= measures[label]
        triple = measures["A ∩ B ∩ C"]
        steps.append(step("A", prob_txt(running), prob_txt(triple),
                          prob_txt(running + triple)))
        running += triple
        steps.append(step("MEASURE", "A ∪ B ∪ C",
                          roster(atom for atom in atoms
                                 if atom in set_a | set_b | set_c),
                          prob_txt(running)))
        return prefix, steps, prob_txt(running)

    @classmethod
    def _union_bound(cls):
        atoms, _, weights, set_a, set_b, _, prefix, steps = cls._space(
            "union_bound_compare")
        a_steps, p_a = _measure_steps("A", set_a, atoms, weights)
        b_steps, p_b = _measure_steps("B", set_b, atoms, weights)
        u_steps, union = _measure_steps("A ∪ B", set_a | set_b, atoms, weights)
        steps.extend(a_steps + b_steps + u_steps)
        bound = p_a + p_b
        steps.extend([step("AXIOM", "union bound", "P(A ∪ B) ≤ P(A) + P(B)"),
                      step("A", prob_txt(p_a), prob_txt(p_b), prob_txt(bound)),
                      step("CMP", prob_txt(union), prob_txt(bound), "≤")])
        answer = (f"P(A ∪ B) = {prob_txt(union)} ≤ "
                  f"P(A) + P(B) = {prob_txt(bound)}")
        return prefix, steps, answer

    @classmethod
    def _renormalize(cls):
        atoms, _, weights, _, set_b, _, prefix, steps = cls._space("renormalize")
        measure_steps, mass = _measure_steps("B", set_b, atoms, weights)
        steps.extend(measure_steps)
        conditioned = []
        for atom in atoms:
            if atom not in set_b:
                continue
            value = weights[atom] / mass
            steps.append(step("D", prob_txt(weights[atom]), prob_txt(mass),
                              prob_txt(value)))
            steps.append(step("RENORMALIZE", atom,
                              f"({prob_txt(weights[atom])})/({prob_txt(mass)})",
                              prob_txt(value)))
            conditioned.append((atom, value))
        running = conditioned[0][1]
        for _, value in conditioned[1:]:
            steps.append(step("A", prob_txt(running), prob_txt(value),
                              prob_txt(running + value)))
            running += value
        steps.append(step("CHECK", "conditional weights sum", prob_txt(running)))
        answer = "; ".join(f"{atom}: {prob_txt(value)}"
                           for atom, value in conditioned) + "; others 0"
        return prefix, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "set_expression":
            prefix, steps, answer = self._set_expression()
        elif variant == "derive_identity":
            prefix, steps, answer = self._derive_identity()
        elif variant == "monotonicity":
            prefix, steps, answer = self._monotonicity()
        elif variant == "inclusion_exclusion_three":
            prefix, steps, answer = self._inclusion_exclusion()
        elif variant == "union_bound_compare":
            prefix, steps, answer = self._union_bound()
        else:
            prefix, steps, answer = self._renormalize()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_measure_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
