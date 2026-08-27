"""Distinguish set membership, subset, equality, and cardinality.

Variants:
- ``membership`` checks whether one integer is an element of A.
- ``subset`` checks A ⊆ B and reports any missing elements.
- ``equality`` deduplicates two raw entry lists before comparing their sets.
- ``element_vs_subset`` contrasts n ∈ A, {n} ⊆ A, and {n} ∈ A.
- ``count`` deduplicates raw entries before finding card(A).

Raw entry collections use square brackets so duplicates and mixed input order
are visible without pretending they are canonical set rosters.  Five
phrasings and randomized rosters yield a problem space above 100,000.

Op-codes:
- ``ELEMENT_SCAN``: look for one candidate element in a set.
- ``SUBSET_CHECK``: check one prospective subset element against its superset.
- ``DEDUP``: turn raw entries into a canonical duplicate-free roster.
- ``COUNT``: record a set cardinality.
- ``Z``: exact composite answer.
"""
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import fmt_element, roster, sorted_elements


FOUNDATIONS = True


QUERIES = {
    "membership": (
        "Decide whether the focus value is an element of A.",
        "Scan A for the focus value and report membership.",
        "Is the stated integer in the set? Give the membership result.",
        "Check the roster and decide the element statement.",
        "Determine whether the focus value belongs to A.",
    ),
    "subset": (
        "Decide whether A is a subset of B and report missing elements.",
        "Check every element of A against B.",
        "Test A ⊆ B and list anything from A that is absent from B.",
        "Use an element-by-element scan to decide the subset claim.",
        "Determine the subset result together with its witness roster.",
    ),
    "equality": (
        "Remove repeated entries, then decide whether the resulting sets are equal.",
        "Deduplicate both raw lists and compare their sets.",
        "Convert each raw entry list to a set and test equality.",
        "Ignore repetition and input order; are A and B the same set?",
        "Write both reduced rosters and decide A = B.",
    ),
    "element_vs_subset": (
        "Decide n ∈ A, {n} ⊆ A, and {n} ∈ A separately.",
        "Distinguish the element and singleton-subset statements.",
        "Check all three claims about n and the singleton {n}.",
        "Report whether n and {n} occur as elements and whether {n} is a subset.",
        "Use the roster to evaluate the three membership/subset statements.",
    ),
    "count": (
        "Deduplicate the raw entries and find card(A).",
        "Count the distinct elements represented by the raw list.",
        "Convert the entries to a set, then report its cardinal number.",
        "Ignore repeated entries and determine card(A).",
        "Write the reduced roster and count its elements.",
    ),
}


def raw_list(values):
    return "[" + ", ".join(fmt_element(value) for value in values) + "]"


class SetMembershipSubsetGenerator(ProblemGenerator):
    """Generate explicit finite-set scans in the canonical set dialect."""

    VARIANTS = ("membership", "subset", "equality", "element_vs_subset",
                "count")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _integer_set(min_size=3, max_size=8):
        return sorted(random.sample(range(1, 100), random.randint(min_size,
                                                                  max_size)))

    def _membership(self):
        values = self._integer_set()
        focus = random.choice(values) if random.choice((True, False)) else random.choice(
            [value for value in range(1, 100) if value not in values]
        )
        present = focus in values
        problem = (
            f"Set A = {roster(values)}. Focus value: {focus}. "
            f"{random.choice(QUERIES['membership'])}"
        )
        steps = [step("ELEMENT_SCAN", focus, "A",
                      "found" if present else "not found")]
        answer = f"{focus} ∈ A: {'yes' if present else 'no'}; A = {roster(values)}"
        return problem, steps, answer

    def _subset(self):
        values_b = self._integer_set(4, 9)
        if random.choice((True, False)):
            values_a = sorted(random.sample(values_b,
                                            random.randint(1, len(values_b))))
        else:
            inside = random.sample(values_b, random.randint(1, len(values_b) - 1))
            outside = random.sample([value for value in range(1, 100)
                                     if value not in values_b],
                                    random.randint(1, 2))
            values_a = sorted(set(inside + outside))
        missing = sorted(set(values_a) - set(values_b))
        problem = (
            f"Set A = {roster(values_a)}. Set B = {roster(values_b)}. "
            f"{random.choice(QUERIES['subset'])}"
        )
        steps = [step("SUBSET_CHECK", value,
                      "in B?", "yes" if value in values_b else "no")
                 for value in values_a]
        answer = (f"A ⊆ B: {'yes' if not missing else 'no'}; "
                  f"missing = {roster(missing)}")
        return problem, steps, answer

    @staticmethod
    def _with_duplicates(values):
        raw = list(values)
        raw.extend(random.choices(values, k=random.randint(1, 3)))
        random.shuffle(raw)
        return raw

    def _equality(self):
        reduced_a = self._integer_set(3, 7)
        if random.choice((True, False)):
            reduced_b = list(reduced_a)
        else:
            reduced_b = list(reduced_a)
            reduced_b[random.randrange(len(reduced_b))] = random.choice(
                [value for value in range(1, 100) if value not in reduced_a]
            )
            reduced_b = sorted(set(reduced_b))
        raw_a = self._with_duplicates(reduced_a)
        raw_b = self._with_duplicates(reduced_b)
        equal = set(reduced_a) == set(reduced_b)
        problem = (
            f"Raw entries A = {raw_list(raw_a)}. Raw entries B = {raw_list(raw_b)}. "
            f"{random.choice(QUERIES['equality'])}"
        )
        steps = [step("DEDUP", f"A raw {raw_list(raw_a)}", roster(reduced_a)),
                 step("DEDUP", f"B raw {raw_list(raw_b)}", roster(reduced_b))]
        for value in sorted_elements(set(reduced_a) | set(reduced_b)):
            steps.append(step("ELEMENT_SCAN", value,
                              f"in A={'yes' if value in reduced_a else 'no'}",
                              f"in B={'yes' if value in reduced_b else 'no'}"))
        answer = (f"A = B: {'yes' if equal else 'no'}; "
                  f"reduced A = {roster(reduced_a)}; "
                  f"reduced B = {roster(reduced_b)}")
        return problem, steps, answer

    def _element_vs_subset(self):
        focus = random.randint(1, 30)
        values = set(random.sample([value for value in range(1, 50)
                                    if value != focus], random.randint(2, 5)))
        atom_present = random.choice((True, False))
        singleton_present = random.choice((True, False))
        if atom_present:
            values.add(focus)
        singleton = frozenset((focus,))
        if singleton_present:
            values.add(singleton)
        problem = (
            f"Set A = {roster(values)}. Focus value n = {focus}. "
            f"{random.choice(QUERIES['element_vs_subset'])}"
        )
        steps = [
            step("ELEMENT_SCAN", focus, "A",
                 "found" if atom_present else "not found"),
            step("SUBSET_CHECK", roster((focus,)), "subset of A?",
                 "yes" if atom_present else "no"),
            step("ELEMENT_SCAN", roster((focus,)), "A",
                 "found" if singleton_present else "not found"),
        ]
        answer = (
            f"{focus} ∈ A: {'yes' if atom_present else 'no'}; "
            f"{{{focus}}} ⊆ A: {'yes' if atom_present else 'no'}; "
            f"{{{focus}}} ∈ A: {'yes' if singleton_present else 'no'}"
        )
        return problem, steps, answer

    def _count(self):
        reduced = self._integer_set(3, 9)
        raw = self._with_duplicates(reduced)
        problem = (
            f"Raw entries A = {raw_list(raw)}. "
            f"{random.choice(QUERIES['count'])}"
        )
        steps = [step("DEDUP", f"A raw {raw_list(raw)}", roster(reduced)),
                 step("COUNT", "A", len(reduced))]
        answer = f"card(A) = {len(reduced)}; A = {roster(reduced)}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        builders = {
            "membership": self._membership,
            "subset": self._subset,
            "equality": self._equality,
            "element_vs_subset": self._element_vs_subset,
            "count": self._count,
        }
        problem, steps, answer = builders[variant]()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"set_membership_subset_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
