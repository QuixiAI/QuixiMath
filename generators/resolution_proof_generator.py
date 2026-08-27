"""Construct canonical propositional-resolution refutations.

Variants:
- ``unit_refutation``, ``chain_refutation``, and ``binary_refutation`` retain
  the three original named refutation cores for compatibility.
- ``random_unsatisfiable`` builds a random 3–5-clause CNF over exactly 3–4
  variables and verifies unsatisfiability by brute force before tracing it.

The canonical policy scans clause pairs by increasing indices and candidate
pivots alphabetically, appends the first new non-tautological resolvent, and
restarts. Variable names, clause sets, orderings, and five phrasings provide
well over 100,000 problem texts.

Op-codes:
- ``RES_SETUP`` / ``CLAUSE``: state the ordered initial CNF.
- ``RESOLVE`` / ``DERIVED``: show a parent pair, pivot, and new resolvent.
- ``RES_SKIP``: record a duplicate or tautological resolvent.
- ``RES_EMPTY``: identify the derived empty clause.
- ``CHECK``: state the unsatisfiability certificate.
- ``Z``: verdict and exact empty-clause index.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = (
    "Derive the empty clause by canonical resolution.",
    "Give the complete resolution refutation in the stated order.",
    "Apply the pair-and-pivot scan until contradiction is explicit.",
    "Refute the clause set without changing the canonical scan policy.",
    "Complete the deterministic derivation of the empty clause.",
)


def literal_name(literal):
    return literal[4:] if literal.startswith("not ") else literal


def literal_text(literal):
    return f"¬{literal[4:]}" if literal.startswith("not ") else literal


def literal_key(literal):
    return literal_name(literal), literal.startswith("not ")


def normalize_clause(clause):
    return tuple(sorted(set(clause), key=literal_key))


def clause_text(clause):
    if not clause:
        return "□"
    return "(" + " ∨ ".join(literal_text(value) for value in clause) + ")"


def formula_text(clauses):
    return ", ".join(f"C{index}={clause_text(clause)}"
                     for index, clause in enumerate(clauses, 1))


def complement(literal):
    return literal[4:] if literal.startswith("not ") else f"not {literal}"


def resolve(first, second, pivot):
    opposite = complement(pivot)
    values = [value for value in first if value != pivot]
    values.extend(value for value in second if value != opposite)
    return normalize_clause(values)


def tautological(clause):
    values = set(clause)
    return any(complement(value) in values for value in values)


def satisfies(clauses, assignment):
    return all(any((not assignment[literal_name(value)])
                       if value.startswith("not ")
                       else assignment[value]
                   for value in clause)
               for clause in clauses)


def is_unsatisfiable(clauses):
    names = sorted({literal_name(value) for clause in clauses for value in clause})
    return not any(satisfies(clauses, dict(zip(names, values)))
                   for values in itertools.product((False, True), repeat=len(names)))


def random_clause(names, minimum=1):
    size = random.randint(minimum, min(3, len(names)))
    chosen = random.sample(names, size)
    return normalize_clause(
        f"not {name}" if random.choice((True, False)) else name
        for name in chosen)


def original_clauses(variant):
    """Retain the original three named cores with alpha-varied symbols."""
    names = [f"P{value}" for value in random.sample(range(1, 100000), 5)]
    first, second = names[:2]
    if variant == "unit_refutation":
        clauses = [(first,), (f"not {first}",)]
        unused = names[1:]
    elif variant == "chain_refutation":
        clauses = [(first,), (f"not {first}", second), (f"not {second}",)]
        unused = names[2:]
    else:
        clauses = [(first, second), (f"not {first}",), (f"not {second}",)]
        unused = names[2:]
    random.shuffle(clauses)
    distractor_size = random.randint(1, len(unused))
    clauses.append(tuple(unused[:distractor_size]))
    return [normalize_clause(clause) for clause in clauses]


def random_unsatisfiable_clauses():
    """Build and brute-force-check a random small unsatisfiable clause set."""
    count = random.choice((3, 4))
    names = [f"P{value}" for value in random.sample(range(1, 100000), count)]
    first, second = names[:2]
    core_type = random.choice(("unit", "chain", "binary", "four_corners"))
    if core_type == "unit":
        clauses = [(first,), (f"not {first}",)]
    elif core_type == "chain":
        clauses = [(first,), (f"not {first}", second), (f"not {second}",)]
    elif core_type == "binary":
        clauses = [(first, second), (f"not {first}",), (f"not {second}",)]
    else:
        clauses = [
            (first, second), (first, f"not {second}"),
            (f"not {first}", second),
            (f"not {first}", f"not {second}"),
        ]
    clauses = [normalize_clause(clause) for clause in clauses]
    unused = [name for name in names
              if all(name != literal_name(value)
                     for clause in clauses for value in clause)]
    if unused:
        clauses.append(normalize_clause(
            f"not {name}" if random.choice((True, False)) else name
            for name in unused))
    target = random.randint(len(clauses), 5)
    while len(clauses) < target:
        candidate = random_clause(names)
        if candidate not in clauses:
            clauses.append(candidate)
    random.shuffle(clauses)
    used = {literal_name(value) for clause in clauses for value in clause}
    assert 3 <= len(clauses) <= 5
    assert used == set(names)
    assert is_unsatisfiable(clauses)
    return clauses


def resolution_trace(initial_clauses):
    clauses = list(initial_clauses)
    steps = [step("RES_SETUP", formula_text(clauses))]
    for index, clause in enumerate(clauses, 1):
        steps.append(step("CLAUSE", f"C{index}", clause_text(clause)))
    while clauses[-1]:
        seen = set(clauses)
        selected = None
        for first_index, first in enumerate(clauses):
            for second_index in range(first_index + 1, len(clauses)):
                second = clauses[second_index]
                for pivot in sorted(first, key=literal_key):
                    if complement(pivot) not in second:
                        continue
                    resolvent = resolve(first, second, pivot)
                    if tautological(resolvent) or resolvent in seen:
                        steps.append(step("RES_SKIP", f"C{first_index + 1}",
                                          f"C{second_index + 1}",
                                          clause_text(resolvent)))
                        continue
                    selected = (first_index, second_index, pivot, resolvent)
                    break
                if selected:
                    break
            if selected:
                break
        if selected is None:
            raise RuntimeError("resolution trace could not derive a new clause")
        first_index, second_index, pivot, resolvent = selected
        clauses.append(resolvent)
        new_name = f"C{len(clauses)}"
        steps.append(step("RESOLVE", f"C{first_index + 1}",
                          f"C{second_index + 1}", literal_text(pivot)))
        steps.append(step("DERIVED", new_name, clause_text(resolvent)))
    steps.append(step("RES_EMPTY", f"C{len(clauses)}"))
    steps.append(step("CHECK", "empty clause", "unsatisfiable"))
    return clauses, steps


class ResolutionProofGenerator(ProblemGenerator):
    """Generate exact canonical resolution refutations."""

    VARIANTS = ("unit_refutation", "chain_refutation", "binary_refutation",
                "random_unsatisfiable")
    WEIGHTS = (0.05, 0.05, 0.05, 0.85)

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self):
        variant = self.variant or random.choices(
            self.VARIANTS, weights=self.WEIGHTS, k=1)[0]
        initial = (random_unsatisfiable_clauses()
                   if variant == "random_unsatisfiable"
                   else original_clauses(variant))
        clauses, steps = resolution_trace(initial)
        policy = ("scan clause pairs by increasing indices; within a pair scan "
                  "complementary variables alphabetically; append the first new "
                  "non-tautological resolvent and restart; skip duplicates")
        problem = (f"CNF clauses: {formula_text(initial)}. Policy: {policy}. "
                   f"{random.choice(QUERIES)}")
        answer = f"unsatisfiable; empty clause = C{len(clauses)}"
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"resolution_proof_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
