"""Enumerate finite integer set-builder expressions by explicit trials.

Variants:
- ``integer_range`` lists a bounded integer interval.
- ``parity_divisibility`` adds an even/odd or divisibility predicate.
- ``squares_primes`` filters for primes or perfect squares.
- ``compound_condition`` combines two predicates with ``and`` or ``or``.
- ``cardinality`` reports the size of a generated roster.

Every expression has a hand-sized range, five query phrasings, and
parameterized bounds/predicates, producing more than 100,000 problem texts.

Op-codes:
- ``DOMAIN``: display the complete finite candidate roster.
- ``DIV_CHECK`` / ``M`` / ``CMP``: expose predicate arithmetic.
- ``TRY`` / ``ACCEPT`` / ``REJECT``: test each candidate in order.
- ``ROSTER``: record the canonical result roster.
- ``COUNT``: record its cardinality.
- ``Z``: exact roster or cardinality answer.
"""
import math
import random

from base_generator import ProblemGenerator
from helpers import jid, step
from set_common import fmt_int, roster


FOUNDATIONS = True


QUERIES = {
    "list": (
        "List the elements described by the set-builder expression.",
        "Enumerate the bounded domain and write the resulting roster.",
        "Test each integer in the range and give the set in roster form.",
        "Convert this finite set-builder description to a roster.",
        "Find every integer satisfying the stated condition.",
    ),
    "cardinality": (
        "Count the elements described by the set-builder expression.",
        "Enumerate the set, then report its cardinal number.",
        "Find card(S) for this bounded set-builder description.",
        "Test the candidate integers and give the number accepted.",
        "Determine the cardinality of the finite set S.",
    ),
}


def is_prime(value):
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def atom_text(atom):
    kind, parameter = atom
    if kind in ("even", "odd", "prime", "square"):
        word = "perfect square" if kind == "square" else kind
        return f"x is {word}"
    return f"{parameter} divides x"


def atom_value(value, atom):
    kind, parameter = atom
    if kind == "even":
        return value % 2 == 0
    if kind == "odd":
        return value % 2 != 0
    if kind == "divides":
        return value % parameter == 0
    if kind == "prime":
        return is_prime(value)
    if kind == "square":
        return value >= 0 and math.isqrt(value) ** 2 == value
    raise ValueError(kind)


class SetBuilderRosterGenerator(ProblemGenerator):
    """Generate finite set-builder scans with no hidden predicate arithmetic."""

    VARIANTS = ("integer_range", "parity_divisibility", "squares_primes",
                "compound_condition", "cardinality")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _bounds(nonnegative=False):
        low = random.randint(0 if nonnegative else -50, 45)
        width = random.randint(8, 16)
        return low, low + width

    @staticmethod
    def _simple_atom(allow_square_prime=True):
        choices = [("even", None), ("odd", None),
                   ("divides", random.randint(3, 10))]
        if allow_square_prime:
            choices.extend((("prime", None), ("square", None)))
        return random.choice(choices)

    @staticmethod
    def _predicate_steps(value, atom):
        kind, parameter = atom
        if kind in ("even", "odd"):
            return [step("DIV_CHECK", value, 2, f"remainder {value % 2}")]
        if kind == "divides":
            return [step("DIV_CHECK", value, parameter,
                         f"quotient {value // parameter}, remainder {value % parameter}")]
        if kind == "prime":
            if value < 2:
                return [step("CMP", value, 2, "<")]
            checks = []
            for divisor in range(2, math.isqrt(value) + 1):
                checks.append(step("DIV_CHECK", value, divisor,
                                   f"remainder {value % divisor}"))
                if value % divisor == 0:
                    break
            return checks or [step("CMP", value, 2, "≥")]
        if value < 0:
            return [step("CMP", value, 0, "<")]
        root = math.isqrt(value)
        square = root * root
        relation = "=" if square == value else "<"
        return [step("M", root, root, square),
                step("CMP", square, value, relation)]

    def _specification(self, variant):
        if variant == "integer_range":
            low, high = self._bounds()
            atoms, joiner = [], ""
        elif variant == "parity_divisibility":
            low, high = self._bounds()
            atoms = [self._simple_atom(False)]
            joiner = ""
        elif variant == "squares_primes":
            atom = random.choice((("prime", None), ("square", None)))
            low, high = self._bounds(nonnegative=atom[0] == "square")
            atoms, joiner = [atom], ""
        else:
            low, high = self._bounds()
            first = self._simple_atom(False)
            second_choices = [("prime", None), ("square", None),
                              ("divides", random.randint(3, 10)),
                              ("even", None), ("odd", None)]
            second = random.choice([item for item in second_choices
                                    if item != first])
            atoms = [first, second]
            joiner = random.choice(("and", "or"))
        return low, high, atoms, joiner

    @staticmethod
    def _condition(low, high, atoms, joiner, bound_style):
        bound_forms = (
            f"{fmt_int(low, True)} ≤ x ≤ {fmt_int(high, True)}",
            f"{fmt_int(low - 1, True)} < x ≤ {fmt_int(high, True)}",
            f"{fmt_int(low, True)} ≤ x < {fmt_int(high + 1, True)}",
            f"{fmt_int(low - 1, True)} < x < {fmt_int(high + 1, True)}",
        )
        bounds = bound_forms[bound_style]
        if not atoms:
            return bounds
        atom_condition = (atom_text(atoms[0]) if len(atoms) == 1 else
                          f"({atom_text(atoms[0])} {joiner} {atom_text(atoms[1])})")
        return f"{bounds} and {atom_condition}"

    @staticmethod
    def _accepts(value, atoms, joiner):
        if not atoms:
            return True
        results = [atom_value(value, atom) for atom in atoms]
        return results[0] if len(results) == 1 else (
            all(results) if joiner == "and" else any(results)
        )

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        spec_variant = (random.choice(("parity_divisibility", "squares_primes",
                                       "compound_condition"))
                        if variant == "cardinality" else variant)
        low, high, atoms, joiner = self._specification(spec_variant)
        candidates = list(range(low, high + 1))
        accepted = [value for value in candidates
                    if self._accepts(value, atoms, joiner)]
        condition = self._condition(low, high, atoms, joiner,
                                    random.randrange(4))
        expression = f"{{x ∈ ℤ : {condition}}}"
        query_kind = "cardinality" if variant == "cardinality" else "list"
        problem = (
            f"Set S = {expression}. {random.choice(QUERIES[query_kind])}"
        )
        steps = [step("DOMAIN", f"x = {fmt_int(low, True)}..{fmt_int(high, True)}",
                      roster(candidates, unicode_minus=True))]
        for value in candidates:
            for atom in atoms:
                steps.extend(self._predicate_steps(value, atom))
            result = self._accepts(value, atoms, joiner)
            steps.append(step("TRY", f"x = {fmt_int(value, True)}", condition,
                              "true" if result else "false"))
            steps.append(step("ACCEPT" if result else "REJECT",
                              f"x = {fmt_int(value, True)}"))
        result_roster = roster(accepted, unicode_minus=True)
        steps.append(step("ROSTER", "S", result_roster))
        if variant == "cardinality":
            steps.append(step("COUNT", "S", len(accepted)))
            answer = f"card(S) = {len(accepted)}; S = {result_roster}"
        else:
            answer = result_roster
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"set_builder_roster_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
