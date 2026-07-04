import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_set(values):
    return "{" + ", ".join(str(v) for v in values) + "}"


def fmt_pair(pair):
    return f"({pair[0]}, {pair[1]})"


def fmt_relation(pairs):
    ordered = sorted(pairs)
    return "{" + ", ".join(fmt_pair(pair) for pair in ordered) + "}" if ordered else "{}"


def yes_no(value):
    return "yes" if value else "no"


def properties(A, R):
    Rset = set(R)
    reflexive = all((a, a) in Rset for a in A)
    symmetric = all((b, a) in Rset for a, b in Rset)
    antisymmetric = all(a == b or (b, a) not in Rset for a, b in Rset)
    transitive = True
    for a, b in Rset:
        for c, d in Rset:
            if b == c and (a, d) not in Rset:
                transitive = False
    return reflexive, symmetric, antisymmetric, transitive


def answer_txt(props):
    names = ["reflexive", "symmetric", "antisymmetric", "transitive"]
    return "; ".join(f"{name} {yes_no(value)}"
                     for name, value in zip(names, props))


class RelationCheckGenerator(ProblemGenerator):
    """
    Relation property checks on small finite sets.

    Variant:
    - property_check: reflexive, symmetric, antisymmetric, transitive

    Op-codes used:
    - REL_SETUP: finite set and relation
    - REFLEXIVE_CHECK / SYMMETRIC_CHECK / ANTISYM_CHECK / TRANSITIVE_CHECK
    - PROPERTY_RESULT: yes/no result for one property
    - Z: composite property classification
    """

    VARIANTS = ["property_check"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        n = random.choice([3, 4])
        A = list(range(1, n + 1))
        all_pairs = [(a, b) for a in A for b in A]
        R = [pair for pair in all_pairs if random.random() < 0.38]
        props = properties(A, R)
        Rset = set(R)
        steps = [step("REL_SETUP", f"A = {fmt_set(A)}", f"R = {fmt_relation(R)}")]

        reflexive_ok = True
        for a in A:
            present = (a, a) in Rset
            reflexive_ok = reflexive_ok and present
            steps.append(step("REFLEXIVE_CHECK", fmt_pair((a, a)),
                              "present" if present else "missing"))
        steps.append(step("PROPERTY_RESULT", "reflexive", yes_no(reflexive_ok)))

        symmetric_ok = True
        for pair in sorted(Rset):
            reverse = (pair[1], pair[0])
            present = reverse in Rset
            symmetric_ok = symmetric_ok and present
            steps.append(step("SYMMETRIC_CHECK", fmt_pair(pair),
                              f"reverse {fmt_pair(reverse)}",
                              "present" if present else "missing"))
        steps.append(step("PROPERTY_RESULT", "symmetric", yes_no(symmetric_ok)))

        antisym_ok = True
        for pair in sorted(p for p in Rset if p[0] != p[1]):
            reverse = (pair[1], pair[0])
            violation = reverse in Rset
            antisym_ok = antisym_ok and not violation
            steps.append(step("ANTISYM_CHECK", fmt_pair(pair),
                              f"reverse {fmt_pair(reverse)}",
                              "violation" if violation else "ok"))
        steps.append(step("PROPERTY_RESULT", "antisymmetric", yes_no(antisym_ok)))

        transitive_ok = True
        for a, b in sorted(Rset):
            for c, d in sorted(Rset):
                if b != c:
                    continue
                needed = (a, d)
                present = needed in Rset
                transitive_ok = transitive_ok and present
                steps.append(step("TRANSITIVE_CHECK",
                                  f"{fmt_pair((a, b))} and {fmt_pair((c, d))}",
                                  f"need {fmt_pair(needed)}",
                                  "present" if present else "missing"))
        steps.append(step("PROPERTY_RESULT", "transitive", yes_no(transitive_ok)))

        answer = answer_txt(props)
        steps.append(step("Z", answer))
        problem = (
            f"For A = {fmt_set(A)} and R = {fmt_relation(R)}, determine "
            f"whether R is reflexive, symmetric, antisymmetric, and transitive."
        )
        return dict(
            problem_id=jid(),
            operation="relation_check_property_check",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
