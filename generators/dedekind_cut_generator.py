"""Exact finite exercises with Dedekind cuts of rational numbers."""
from fractions import Fraction
import random

from base_generator import ProblemGenerator
from helpers import jid, step


FOUNDATIONS = True


QUERIES = {
    "membership": (
        "Classify each listed rational as a member or nonmember of the cut.",
        "Determine which listed rationals belong to L(√2).",
        "Test both rationals against the defining condition.",
        "State the membership status of each listed value.",
        "Use exact squares to classify the two rationals.",
    ),
    "largest_of_list": (
        "Find the largest listed member of L(√2).",
        "Which listed cut member is greatest?",
        "Select the greatest rational in the list that belongs to the cut.",
        "Identify the maximum among the listed members of L(√2).",
        "Test the list and report its largest member of the cut.",
    ),
    "compare_cuts": (
        "Find the unique listed rational that separates the two cuts.",
        "Which listed value belongs to L(3/2) but not to L(√2)?",
        "Identify the unique listed witness that the two cuts differ.",
        "Select the listed rational lying in L(3/2) outside L(√2).",
        "Use exact comparisons to find the separator in the list.",
    ),
    "rational_cut": (
        "exhibit a larger member above q and conclude whether the cut has a largest element.",
        "use the midpoint of q and r to show that q is not largest.",
        "find a cut member strictly between q and r, then state the conclusion.",
        "construct the midpoint witness and decide whether L(r) has a largest element.",
        "show with an exact intermediate rational that the lower cut has no maximum.",
    ),
}


def int_text(value):
    return str(value).replace("-", "−")


def fraction_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return int_text(value.numerator)
    return f"{int_text(value.numerator)}/{value.denominator}"


def in_sqrt2_cut(value):
    value = Fraction(value)
    return value < 0 or value * value < 2


def random_fraction(low=-200, high=200, max_denominator=120):
    return Fraction(random.randint(low, high),
                    random.randint(1, max_denominator))


def positive_sqrt2_member():
    while True:
        denominator = random.randint(2, 60)
        value = Fraction(random.randint(1, 2 * denominator), denominator)
        if in_sqrt2_cut(value):
            return value


def positive_sqrt2_nonmember():
    while True:
        denominator = random.randint(2, 60)
        value = Fraction(random.randint(1, 2 * denominator), denominator)
        if not in_sqrt2_cut(value):
            return value


def separator_fraction():
    """Return a rational in [sqrt(2), 3/2)."""
    while True:
        denominator = random.randint(5, 80)
        value = Fraction(random.randint(1, 2 * denominator), denominator)
        if not in_sqrt2_cut(value) and value < Fraction(3, 2):
            return value


def membership_evidence(value):
    if value < 0:
        return f"{fraction_text(value)} < 0"
    square = value * value
    relation = "<" if square < 2 else ">"
    return f"{fraction_text(square)} {relation} 2"


def classification_steps(value):
    rendered = fraction_text(value)
    if value < 0:
        steps = [step("CMP", rendered, 0, "<")]
    else:
        square = value * value
        relation = "<" if square < 2 else ">"
        steps = [step("E", rendered, 2, fraction_text(square)),
                 step("CMP", fraction_text(square), 2, relation)]
    symbol = "∈" if in_sqrt2_cut(value) else "∉"
    steps.append(step("MEMBER", f"{rendered} {symbol} L(√2)"))
    return steps


class DedekindCutGenerator(ProblemGenerator):
    """Generate exact exercises using lower Dedekind cuts."""

    VARIANTS = ("membership", "largest_of_list", "compare_cuts",
                "rational_cut")

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _membership(self):
        member = (positive_sqrt2_member() if random.randrange(4) else
                  -random_fraction(1, 80, 60))
        values = [member, positive_sqrt2_nonmember()]
        random.shuffle(values)
        rendered = ", ".join(fraction_text(value) for value in values)
        problem = ("Define L(√2) by q ∈ L(√2) iff q < 0 or q² < 2. "
                   f"Listed rationals: [{rendered}]. "
                   f"{random.choice(QUERIES['membership'])}")
        steps = [step("CUT_RULE", "L(√2)", "q < 0 or q² < 2")]
        answer_parts = []
        for value in values:
            steps.extend(classification_steps(value))
            symbol = "∈" if in_sqrt2_cut(value) else "∉"
            answer_parts.append(
                f"{fraction_text(value)} {symbol} L(√2) "
                f"({membership_evidence(value)})")
        answer = "; ".join(answer_parts)
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def _largest_of_list(self):
        members = {positive_sqrt2_member() for _ in range(3)}
        while len(members) < 3:
            members.add(positive_sqrt2_member())
        nonmembers = {positive_sqrt2_nonmember() for _ in range(2)}
        while len(nonmembers) < 2 or members & nonmembers:
            nonmembers.add(positive_sqrt2_nonmember())
        values = list(members | nonmembers)
        random.shuffle(values)
        largest = max(value for value in values if in_sqrt2_cut(value))
        rendered = ", ".join(fraction_text(value) for value in values)
        problem = ("Define L(√2) by q ∈ L(√2) iff q < 0 or q² < 2. "
                   f"Candidate list: [{rendered}]. "
                   f"{random.choice(QUERIES['largest_of_list'])}")
        steps = [step("CUT_RULE", "L(√2)", "q < 0 or q² < 2")]
        for value in values:
            steps.extend(classification_steps(value))
        member_text = ", ".join(
            fraction_text(value) for value in sorted(values)
            if in_sqrt2_cut(value))
        steps.append(step("LIST_MAX", member_text, fraction_text(largest)))
        answer = (f"largest listed member: {fraction_text(largest)} "
                  f"({membership_evidence(largest)})")
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def _compare_cuts(self):
        separator = separator_fraction()
        below = {positive_sqrt2_member() for _ in range(2)}
        while len(below) < 2:
            below.add(positive_sqrt2_member())
        above = {positive_sqrt2_nonmember() for _ in range(2)}
        above = {value for value in above if value >= Fraction(3, 2)}
        while len(above) < 2:
            value = positive_sqrt2_nonmember()
            if value >= Fraction(3, 2):
                above.add(value)
        values = list(below | above | {separator})
        if len(values) != 5:
            return self._compare_cuts()
        random.shuffle(values)
        rendered = ", ".join(fraction_text(value) for value in values)
        problem = ("Define L(√2) by q ∈ L(√2) iff q < 0 or q² < 2, and "
                   "define L(3/2) by q ∈ L(3/2) iff q < 3/2. "
                   f"Candidate list: [{rendered}]. "
                   f"{random.choice(QUERIES['compare_cuts'])}")
        steps = [step("CUT_RULE", "L(√2)", "q < 0 or q² < 2"),
                 step("CUT_RULE", "L(3/2)", "q < 3/2")]
        for value in values:
            rendered_value = fraction_text(value)
            if value >= 0:
                square = value * value
                relation = "<" if square < 2 else ">"
                steps.append(step("E", rendered_value, 2,
                                  fraction_text(square)))
                steps.append(step("CMP", fraction_text(square), 2, relation))
            else:
                steps.append(step("CMP", rendered_value, 0, "<"))
            relation = ("<" if value < Fraction(3, 2) else
                        "=" if value == Fraction(3, 2) else ">")
            steps.append(step("CMP", rendered_value, "3/2", relation))
            if value == separator:
                steps.append(step("SEPARATOR", rendered_value,
                                  "in L(3/2)", "not in L(√2)"))
        answer = (f"separator: {fraction_text(separator)} "
                  f"({fraction_text(separator)} ∈ L(3/2), "
                  f"{fraction_text(separator)} ∉ L(√2))")
        steps.append(step("CHECK", answer))
        return problem, steps, answer

    def _rational_cut(self):
        denominator = random.randint(2, 20)
        numerator = random.randint(-50, 50)
        rational = Fraction(numerator, denominator)
        lower = Fraction(numerator - random.randint(1, 24), denominator)
        midpoint = (lower + rational) / 2
        total = lower + rational
        q_text = fraction_text(lower)
        r_text = fraction_text(rational)
        midpoint_text = fraction_text(midpoint)
        problem = (f"Define L({r_text}) by x ∈ L({r_text}) iff x < {r_text}. "
                   f"Given q = {q_text} in L({r_text}), "
                   f"{random.choice(QUERIES['rational_cut'])}")
        steps = [step("CUT_RULE", f"L({r_text})", f"x < {r_text}"),
                 step("CMP", q_text, r_text, "<"),
                 step("A", q_text, r_text, fraction_text(total)),
                 step("D", fraction_text(total), 2, midpoint_text),
                 step("CMP", q_text, midpoint_text, "<"),
                 step("CMP", midpoint_text, r_text, "<"),
                 step("MEMBER", f"{midpoint_text} ∈ L({r_text})"),
                 step("CHECK", "every listed q has a larger midpoint member")]
        answer = f"no largest; {q_text} < {midpoint_text} < {r_text}"
        return problem, steps, answer

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "membership":
            problem, steps, answer = self._membership()
        elif variant == "largest_of_list":
            problem, steps, answer = self._largest_of_list()
        elif variant == "compare_cuts":
            problem, steps, answer = self._compare_cuts()
        else:
            problem, steps, answer = self._rational_cut()
        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"dedekind_cut_{variant}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
