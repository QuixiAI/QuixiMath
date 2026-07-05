import random

from base_generator import ProblemGenerator
from helpers import step, jid


CASES = {
    "unit_refutation": [
        ("A",),
        ("not A",),
    ],
    "chain_refutation": [
        ("A",),
        ("not A", "B"),
        ("not B",),
    ],
    "binary_refutation": [
        ("A", "B"),
        ("not A",),
        ("not B",),
    ],
}


PROBLEM_TEMPLATES = [
    ("Use propositional resolution on CNF {formula}. Resolve the earliest "
     "available complementary literal that gives a new clause, alphabetically, "
     "until the empty clause appears."),
    ("Give a resolution refutation for clauses {formula}, using the stated "
     "clause order and alphabetical complementary literals, skipping duplicate "
     "resolvents."),
    ("Derive the empty clause by resolution from {formula}."),
]


def clause_key(clause):
    return tuple(sorted(clause, key=lambda x: x.replace("not ", "")))


def clause_text(clause):
    if not clause:
        return "{}"
    return "(" + " OR ".join(clause) + ")"


def formula_text(clauses):
    return ", ".join(f"C{i + 1}={clause_text(c)}"
                     for i, c in enumerate(clauses))


def complement(lit):
    return lit[4:] if lit.startswith("not ") else f"not {lit}"


def resolve(c1, c2, lit):
    comp = complement(lit)
    out = [x for x in c1 if x != lit] + [x for x in c2 if x != comp]
    seen = []
    for item in out:
        if item not in seen:
            seen.append(item)
    return tuple(sorted(seen, key=lambda x: x.replace("not ", "")))


class ResolutionProofGenerator(ProblemGenerator):
    """
    Propositional resolution refutations for tiny unsatisfiable CNFs.

    Op-codes used:
    - RES_SETUP / CLAUSE / RESOLVE / DERIVED / RES_EMPTY
    - CHECK
    - Z: unsatisfiable verdict and empty-clause index
    """

    VARIANTS = ["unit_refutation", "chain_refutation", "binary_refutation"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        clauses = list(CASES[variant])
        steps = [step("RES_SETUP", formula_text(clauses))]
        for i, clause in enumerate(clauses, start=1):
            steps.append(step("CLAUSE", f"C{i}", clause_text(clause)))

        while clauses[-1]:
            seen = set(clauses)
            found = None
            for i, c1 in enumerate(clauses):
                for j, c2 in enumerate(clauses):
                    if i >= j:
                        continue
                    for lit in sorted(c1, key=lambda x: x.replace("not ", "")):
                        if complement(lit) in c2:
                            resolvent = resolve(c1, c2, lit)
                            if resolvent not in seen:
                                found = (i, j, lit, resolvent)
                                break
                            steps.append(step("RES_SKIP", f"C{i + 1}",
                                              f"C{j + 1}",
                                              clause_text(resolvent)))
                            break
                    if found:
                        break
                if found:
                    break
            if found is None:
                raise RuntimeError("resolution trace could not derive a new clause")
            i, j, lit, resolvent = found
            clauses.append(resolvent)
            new_name = f"C{len(clauses)}"
            steps.append(step("RESOLVE", f"C{i + 1}", f"C{j + 1}", lit))
            steps.append(step("DERIVED", new_name, clause_text(resolvent)))

        steps.append(step("RES_EMPTY", f"C{len(clauses)}"))
        steps.append(step("CHECK", "empty clause", "unsatisfiable"))
        answer = f"unsatisfiable; empty clause = C{len(clauses)}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            formula=formula_text(CASES[variant])
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"resolution_proof_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
