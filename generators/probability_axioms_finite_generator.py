"""Apply nonnegativity, normalization, and additivity on finite spaces.

Variants: ``missing_weight``, ``event_sum``, ``valid_assignment``,
``complement_from_weights``, and ``disjoint_union``. Op-codes: ``WEIGHT``,
``AXIOM``, ``EVENT``, ``A``, ``S``, ``COMPLEMENT``, ``CHECK``, and ``Z``.
Backward-built rational weights, atom labels, and five phrasings give an
unbounded problem space.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import jid, step
from prob_common import prob_txt, roster


PROBABILITY = True
QUERIES = {
    "missing_weight": (
        "Find x, then compute the probability of the odd-labelled event.",
        "Use normalization to recover x and add the odd atom weights.",
        "Complete the finite distribution and find P(odd).",
        "Determine the missing weight before evaluating the stated event.",
        "Apply total probability one, then finite additivity.",
    ),
    "event_sum": (
        "Find P(A) by adding its atom weights.",
        "Use finite additivity on the displayed event roster.",
        "Sum the disjoint outcome probabilities belonging to A.",
        "Compute the exact measure of event A.",
        "Evaluate P(A) from the finite weight table.",
    ),
    "valid_assignment": (
        "Decide whether the displayed weights form a probability assignment.",
        "Check nonnegativity and total probability one.",
        "Validate or reject the finite model with an exact sum certificate.",
        "Apply the finite probability axioms to classify the weights.",
        "Report validity together with the total weight.",
    ),
    "complement_from_weights": (
        "Find P(Aᶜ) from the atom weights.",
        "Sum the atoms outside A and verify the complement rule.",
        "Compute the exact measure of the complementary event.",
        "Use both direct addition and one minus P(A).",
        "Evaluate P(Aᶜ) in the finite model.",
    ),
    "disjoint_union": (
        "Find P(A ∪ B) using finite additivity.",
        "Add the weights of the two disjoint events.",
        "Compute the exact probability of the displayed disjoint union.",
        "Use P(A ∪ B) = P(A) + P(B).",
        "Evaluate the union measure from the atom table.",
    ),
}


def composition(total, size):
    cuts = sorted(random.sample(range(1, total), size - 1))
    points = (0, *cuts, total)
    return tuple(points[index + 1] - points[index] for index in range(size))


def finite_model(size=None):
    size = size or random.randint(3, 6)
    denominator = random.randint(max(12, size + 1), 200)
    start = random.randint(-10000, 10000)
    atoms = tuple(range(start, start + size))
    weights = tuple(Fraction(value, denominator)
                    for value in composition(denominator, size))
    return atoms, weights


def weight_text(atoms, weights, missing=None):
    return "; ".join(
        f"P({atom}) = {'x' if index == missing else prob_txt(weights[index])}"
        for index, atom in enumerate(atoms))


def weight_steps(atoms, weights, missing=None):
    return [step("WEIGHT", atom,
                 "x" if index == missing else prob_txt(weights[index]))
            for index, atom in enumerate(atoms)]


class ProbabilityAxiomsFiniteGenerator(ProblemGenerator):
    """Generate exact finite probability-axiom exercises."""

    VARIANTS = ("missing_weight", "event_sum", "valid_assignment",
                "complement_from_weights", "disjoint_union")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _missing():
        atoms, weights = finite_model()
        missing = random.randrange(len(atoms))
        known_sum = sum((weight for index, weight in enumerate(weights)
                         if index != missing), Fraction())
        odd_indices = [index for index, atom in enumerate(atoms) if atom % 2]
        event_value = sum((weights[index] for index in odd_indices), Fraction())
        event = tuple(atoms[index] for index in odd_indices)
        prefix = (f"Outcomes Ω = {roster(atoms)}. Weights: "
                  f"{weight_text(atoms, weights, missing)}. Event odd = "
                  f"{roster(event)}.")
        steps = weight_steps(atoms, weights, missing)
        steps.extend([step("AXIOM", "total probability", "Σ P(ω) = 1"),
                      step("A", " + ".join(
                          prob_txt(weight) for index, weight in enumerate(weights)
                          if index != missing), prob_txt(known_sum)),
                      step("S", "1", prob_txt(known_sum),
                           prob_txt(weights[missing])),
                      step("EVENT", "odd", roster(event), len(event)),
                      step("AXIOM", "additivity", "sum weights in odd"),
                      step("A", " + ".join(
                          prob_txt(weights[index]) for index in odd_indices),
                           prob_txt(event_value)),
                      step("CHECK", "all weights", "sum = 1")])
        answer = (f"x = {prob_txt(weights[missing])}; P(odd) = "
                  f"{prob_txt(event_value)}")
        return prefix, steps, answer

    @staticmethod
    def _event_sum():
        atoms, weights = finite_model()
        indices = sorted(random.sample(range(len(atoms)),
                                       random.randint(1, len(atoms) - 1)))
        event = tuple(atoms[index] for index in indices)
        value = sum((weights[index] for index in indices), Fraction())
        prefix = (f"Outcomes Ω = {roster(atoms)}. Weights: "
                  f"{weight_text(atoms, weights)}. Event A = {roster(event)}.")
        steps = weight_steps(atoms, weights)
        steps.extend([step("EVENT", "A", roster(event), len(event)),
                      step("AXIOM", "finite additivity", "sum atom weights"),
                      step("A", " + ".join(
                          prob_txt(weights[index]) for index in indices),
                           prob_txt(value)),
                      step("CHECK", f"0 ≤ {prob_txt(value)} ≤ 1")])
        return prefix, steps, f"P(A) = {prob_txt(value)}"

    @staticmethod
    def _validity():
        atoms, weights = finite_model()
        valid = random.choice((True, False))
        if not valid:
            index = random.randrange(len(weights))
            increment = Fraction(random.randint(1, 20), 200)
            if weights[index] + increment >= 1:
                index = min(range(len(weights)), key=lambda i: weights[i])
            mutable = list(weights)
            mutable[index] += increment
            weights = tuple(mutable)
        total = sum(weights, Fraction())
        prefix = (f"Outcomes Ω = {roster(atoms)}. Candidate weights: "
                  f"{weight_text(atoms, weights)}.")
        steps = weight_steps(atoms, weights)
        steps.extend([step("AXIOM", "nonnegativity", "every weight ≥ 0"),
                      step("A", " + ".join(map(prob_txt, weights)),
                           prob_txt(total)),
                      step("AXIOM", "normalization", "sum must equal 1"),
                      step("CHECK", "sum", prob_txt(total))])
        answer = ("valid; sum = 1" if total == 1 else
                  f"invalid; sum = {prob_txt(total)}")
        return prefix, steps, answer

    @staticmethod
    def _complement():
        atoms, weights = finite_model()
        indices = sorted(random.sample(range(len(atoms)),
                                       random.randint(1, len(atoms) - 1)))
        event = tuple(atoms[index] for index in indices)
        outside = tuple(atom for atom in atoms if atom not in event)
        event_value = sum((weights[index] for index in indices), Fraction())
        complement_value = 1 - event_value
        prefix = (f"Outcomes Ω = {roster(atoms)}. Weights: "
                  f"{weight_text(atoms, weights)}. Event A = {roster(event)}.")
        steps = weight_steps(atoms, weights)
        steps.extend([step("EVENT", "Aᶜ", roster(outside), len(outside)),
                      step("A", " + ".join(
                          prob_txt(weight) for atom, weight in zip(atoms, weights)
                          if atom not in event), prob_txt(complement_value)),
                      step("COMPLEMENT", "1 − P(A)",
                           f"1 − {prob_txt(event_value)}",
                           prob_txt(complement_value)),
                      step("CHECK", "direct sum equals complement rule")])
        return prefix, steps, f"P(Aᶜ) = {prob_txt(complement_value)}"

    @staticmethod
    def _disjoint_union():
        atoms, weights = finite_model(size=random.randint(4, 6))
        shuffled = list(range(len(atoms)))
        random.shuffle(shuffled)
        split = random.randint(1, len(atoms) - 2)
        second_end = random.randint(split + 1, len(atoms) - 1)
        first_indices = sorted(shuffled[:split])
        second_indices = sorted(shuffled[split:second_end])
        first = tuple(atoms[index] for index in first_indices)
        second = tuple(atoms[index] for index in second_indices)
        first_value = sum((weights[index] for index in first_indices), Fraction())
        second_value = sum((weights[index] for index in second_indices), Fraction())
        result = first_value + second_value
        prefix = (f"Outcomes Ω = {roster(atoms)}. Weights: "
                  f"{weight_text(atoms, weights)}. Disjoint events: "
                  f"A = {roster(first)}; B = {roster(second)}.")
        steps = weight_steps(atoms, weights)
        steps.extend([step("EVENT", "A", roster(first), len(first)),
                      step("EVENT", "B", roster(second), len(second)),
                      step("AXIOM", "additivity for disjoint events",
                           "P(A ∪ B) = P(A) + P(B)"),
                      step("A", prob_txt(first_value), prob_txt(second_value),
                           prob_txt(result)),
                      step("CHECK", "A ∩ B = ∅", "disjoint")])
        return prefix, steps, f"P(A ∪ B) = {prob_txt(result)}"

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        methods = {"missing_weight": self._missing,
                   "event_sum": self._event_sum,
                   "valid_assignment": self._validity,
                   "complement_from_weights": self._complement,
                   "disjoint_union": self._disjoint_union}
        prefix, steps, answer = methods[variant]()
        problem = f"{prefix} {random.choice(QUERIES[variant])}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"probability_axioms_finite_{variant}",
                "problem": problem, "steps": steps, "final_answer": answer}
