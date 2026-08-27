"""Solve finite knights-and-knaves puzzles by exhaustive case checking.

Variants:
- ``two_islanders`` uses two named speakers.
- ``three_islanders`` uses three named speakers and the full statement grammar.
- ``one_statement_each`` uses three speakers with exactly one statement apiece.

The generator chooses a target assignment, samples only statements consistent
with that target, and brute-forces all assignments until exactly one survives.
Names, statement grammar, and five phrasings provide over 100,000 puzzles.

Op-codes:
- ``CASE``: state one knight/knave assignment in canonical order.
- ``STATEMENT_EVAL``: evaluate a speaker's claim and its consistency.
- ``REJECT`` / ``ACCEPT``: close or retain the case.
- ``CHECK``: verify the unique surviving assignment.
- ``Z``: exact composite type assignment.
"""
import itertools
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


NAMES = (
    "Ada", "Bea", "Cleo", "Dara", "Eli", "Finn", "Gia", "Hugo", "Iris",
    "Jae", "Kira", "Luca", "Mara", "Nico", "Oona", "Pia", "Quin", "Ravi",
    "Suri", "Theo",
)

QUERIES = (
    "Determine who is a knight and who is a knave.",
    "Check the possible assignments and identify each person's type.",
    "Find the unique assignment consistent with every statement.",
    "Decide each islander's type by testing the cases in the stated order.",
    "Use truthfulness and lying to solve for all speakers.",
)


def assignment_text(names, assignment):
    return ", ".join(
        f"{name}={'knight' if assignment[name] else 'knave'}" for name in names
    )


def answer_text(names, assignment):
    return ", ".join(
        f"{name} {'knight' if assignment[name] else 'knave'}" for name in names
    )


def statement_bank(names):
    bank = []
    for name in names:
        bank.append((f"{name} is a knight",
                     lambda assignment, name=name: assignment[name]))
        bank.append((f"{name} is a knave",
                     lambda assignment, name=name: not assignment[name]))
    for first, second in itertools.combinations(names, 2):
        bank.extend((
            (f"{first} and {second} are the same type",
             lambda assignment, first=first, second=second:
             assignment[first] == assignment[second]),
            (f"{first} and {second} are different types",
             lambda assignment, first=first, second=second:
             assignment[first] != assignment[second]),
            (f"at least one of {first} and {second} is a knight",
             lambda assignment, first=first, second=second:
             assignment[first] or assignment[second]),
            (f"both {first} and {second} are knaves",
             lambda assignment, first=first, second=second:
             not assignment[first] and not assignment[second]),
        ))
    return bank


class KnightsKnavesGenerator(ProblemGenerator):
    """Generate uniquely solvable cases from a reusable statement grammar."""

    VARIANTS = ("two_islanders", "three_islanders", "one_statement_each")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _assignments(names):
        return [dict(zip(names, values))
                for values in itertools.product((True, False), repeat=len(names))]

    @staticmethod
    def _consistent(assignment, statements):
        return all(bool(evaluator(assignment)) == assignment[speaker]
                   for speaker, _, evaluator in statements)

    def _puzzle(self, names):
        candidates = self._assignments(names)
        bank = statement_bank(names)
        for _ in range(2000):
            target = random.choice(candidates)
            statements = []
            for speaker in names:
                valid = [(text, evaluator) for text, evaluator in bank
                         if bool(evaluator(target)) == target[speaker]]
                text, evaluator = random.choice(valid)
                statements.append((speaker, text, evaluator))
            survivors = [assignment for assignment in candidates
                         if self._consistent(assignment, statements)]
            if len(survivors) == 1:
                return statements, survivors[0], candidates
        raise RuntimeError("could not construct a unique knights-and-knaves puzzle")

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        count = 2 if variant == "two_islanders" else 3
        names = tuple(random.sample(NAMES, count))
        statements, solution, candidates = self._puzzle(names)
        format_label = variant.replace("_", " ")
        claims = " ".join(f'{speaker} says "{text}."'
                          for speaker, text, _ in statements)
        problem = (
            f"Puzzle format: {format_label}. Each person is either a knight who "
            f"always tells the truth or a knave who always lies. {claims} "
            f"Check assignments with names in listed order and knight before knave. "
            f"{random.choice(QUERIES)}"
        )
        steps = []
        for assignment in candidates:
            case = assignment_text(names, assignment)
            steps.append(step("CASE", case))
            consistent = True
            for speaker, text, evaluator in statements:
                truth = bool(evaluator(assignment))
                statement_consistent = truth == assignment[speaker]
                steps.append(step("STATEMENT_EVAL", f"{speaker} says {text}",
                                  "T" if truth else "F",
                                  "consistent" if statement_consistent else
                                  "contradiction"))
                if not statement_consistent:
                    consistent = False
                    break
            steps.append(step("ACCEPT" if consistent else "REJECT", case,
                              "all statements fit" if consistent else "contradiction"))
        answer = answer_text(names, solution)
        steps.append(step("CHECK", "unique surviving case", answer))
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"knights_knaves_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
