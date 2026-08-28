"""Unstated-method integer relationship stories solved exactly.

Variants cover present/future ages, consecutive integers, even/odd runs,
coin counts, affine number relationships, and digit reversal.  Each variant
uses five surface renderings and the four applied modifiers.  Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``DEFINE_VAR``,
``PUZZLE_REL``, ``MODEL_EQ``, ``COMB_X``, ``MOVE_TERM``, ``DIV_COEFF``,
``SUBST``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import estimate_first, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("age_now", "age_future", "consecutive_integers",
            "consecutive_even_odd", "coins_count_value",
            "number_relationship", "digit_reversal")
NAMES = (("Ann", "Ben"), ("Mia", "Leo"), ("Noor", "Omar"),
         ("Pia", "Sam"), ("Rosa", "Theo"), ("Uma", "Vik"))
SETTINGS = ("community center", "classroom challenge", "library club",
            "family game", "school fair")
FRAMES = (
    "At the {setting} ({record}), {facts_lc} {question}",
    "{question} The {setting} record {record} gives these details: {facts}",
    "Case {record} at the {setting} — {facts} {question}",
    "At the {setting}, note {record}: {facts_lc} {question}",
    "Consider the {record} report from the {setting}: {facts} {question}",
)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, setting=random.choice(SETTINGS),
        facts_lc=facts[:1].lower() + facts[1:],
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def _sum_work(values):
    return " + ".join(map(str, values)).replace("+ -", "- ")


class IntegerPuzzleWordGenerator(ProblemGenerator):
    """Generate seven exact integer-story families with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _case(variant):
        first, second = random.choice(NAMES)
        if variant == "age_now":
            younger = random.randint(5, 30)
            offset = random.randint(1, 9)
            older = 2 * younger + offset
            total = older + younger
            facts = (f"{first} is {offset} years older than twice {second}'s "
                     f"age. Together their ages total {total} years.")
            question = f"How old are {first} and {second}?"
            model = f"b + (2b + {offset}) = {total}"
            steps = [step("DEFINE_VAR", "b", f"{second}'s age"),
                     step("PUZZLE_REL", f"{offset} older than twice",
                          f"a = 2b + {offset}"),
                     step("MODEL_EQ", model, "ages total"),
                     step("COMB_X", f"3b + {offset} = {total}"),
                     step("MOVE_TERM", f"3b = {total - offset}"),
                     step("DIV_COEFF", f"b = {younger}"),
                     step("SUBST", "a", f"2*{younger} + {offset}", older),
                     step("CHECK", f"{older} + {younger}", total)]
            answer = f"{first} {older} years; {second} {younger} years"
            used = [f"{offset} years", f"total {total} years"]
            return facts, question, steps, answer, Fraction(younger), model, used

        if variant == "age_future":
            younger = random.randint(5, 35)
            gap = random.randint(1, 12)
            years = random.randint(2, 10)
            older = younger + gap
            future_total = older + younger + 2 * years
            facts = (f"{first} is {gap} years older than {second}. In {years} "
                     f"years their ages will total {future_total} years.")
            question = f"What are {first}'s and {second}'s ages now?"
            model = f"b + (b + {gap}) + 2*{years} = {future_total}"
            steps = [step("DEFINE_VAR", "b", f"{second}'s current age"),
                     step("PUZZLE_REL", f"{gap} years older", f"a=b+{gap}"),
                     step("MODEL_EQ", model, "future ages total"),
                     step("S", future_total, 2 * years, older + younger),
                     step("S", older + younger, gap, 2 * younger),
                     step("D", 2 * younger, 2, younger),
                     step("SUBST", "a", f"{younger}+{gap}", older),
                     step("CHECK", f"{older+years} + {younger+years}",
                          future_total)]
            answer = f"{first} {older} years; {second} {younger} years"
            used = [f"gap {gap} years", f"in {years} years",
                    f"total {future_total} years"]
            return facts, question, steps, answer, Fraction(younger), model, used

        if variant == "consecutive_integers":
            first_value = random.randint(-30, 60)
            values = [first_value, first_value + 1, first_value + 2]
            total = sum(values)
            facts = f"Three consecutive integers have sum {total}."
            question = "What are the three integers?"
            model = f"x + (x + 1) + (x + 2) = {total}"
            steps = [step("DEFINE_VAR", "x", "smallest integer"),
                     step("PUZZLE_REL", "consecutive", "x, x+1, x+2"),
                     step("MODEL_EQ", model, "sum stated"),
                     step("COMB_X", f"3x + 3 = {total}"),
                     step("MOVE_TERM", f"3x = {total - 3}"),
                     step("DIV_COEFF", f"x = {first_value}"),
                     step("CHECK", _sum_work(values), total)]
            answer = ", ".join(map(str, values))
            return facts, question, steps, answer, Fraction(first_value), model, [f"sum {total}"]

        if variant == "consecutive_even_odd":
            parity = random.choice((0, 1))
            first_value = random.randint(-15, 30) * 2 + parity
            values = [first_value, first_value + 2, first_value + 4]
            total = sum(values)
            kind = "even" if parity == 0 else "odd"
            facts = f"Three consecutive {kind} integers have sum {total}."
            question = f"What are the three {kind} integers?"
            model = f"x + (x + 2) + (x + 4) = {total}"
            steps = [step("DEFINE_VAR", "x", f"smallest {kind} integer"),
                     step("PUZZLE_REL", f"consecutive {kind}", "x, x+2, x+4"),
                     step("MODEL_EQ", model, "sum stated"),
                     step("COMB_X", f"3x + 6 = {total}"),
                     step("MOVE_TERM", f"3x = {total - 6}"),
                     step("DIV_COEFF", f"x = {first_value}"),
                     step("CHECK", _sum_work(values), total)]
            answer = ", ".join(map(str, values))
            return facts, question, steps, answer, Fraction(first_value), model, [f"sum {total}"]

        if variant == "coins_count_value":
            nickels = random.randint(2, 30)
            dimes = random.randint(2, 30)
            count = nickels + dimes
            cents = 5 * nickels + 10 * dimes
            facts = (f"A jar contains {count} nickels and dimes worth "
                     f"{cents} cents altogether.")
            question = "How many nickels and how many dimes are in the jar?"
            model = f"n + d = {count}; 5n + 10d = {cents}"
            steps = [step("DEFINE_VAR", "n", "number of nickels"),
                     step("DEFINE_VAR", "d", "number of dimes"),
                     step("MODEL_EQ", f"n + d = {count}", "coin count"),
                     step("MODEL_EQ", f"5n + 10d = {cents}", "total cents"),
                     step("M", count, 5, 5 * count),
                     step("S", cents, 5 * count, 5 * dimes),
                     step("D", 5 * dimes, 5, dimes),
                     step("S", count, dimes, nickels),
                     step("CHECK", f"5*{nickels} + 10*{dimes}", cents)]
            answer = f"nickels {nickels}; dimes {dimes}"
            return facts, question, steps, answer, Fraction(nickels), model, [f"{count} coins", f"{cents} cents"]

        if variant == "number_relationship":
            smaller = random.randint(-10, 30)
            multiplier = random.randint(2, 6)
            offset = random.randint(1, 12)
            larger = multiplier * smaller + offset
            if larger <= smaller:
                return IntegerPuzzleWordGenerator._case(variant)
            total = smaller + larger
            facts = (f"The larger of two integers is {offset} more than "
                     f"{multiplier} times the smaller. Their sum is {total}.")
            question = "What are the two integers?"
            model = f"x + ({multiplier}x + {offset}) = {total}"
            coefficient = multiplier + 1
            steps = [step("DEFINE_VAR", "x", "smaller integer"),
                     step("PUZZLE_REL", f"{offset} more than {multiplier} times",
                          f"y={multiplier}x+{offset}"),
                     step("MODEL_EQ", model, "integers sum"),
                     step("COMB_X", f"{coefficient}x + {offset} = {total}"),
                     step("MOVE_TERM", f"{coefficient}x = {total-offset}"),
                     step("DIV_COEFF", f"x = {smaller}"),
                     step("SUBST", "y", f"{multiplier}*{smaller}+{offset}", larger),
                     step("CHECK", f"{smaller} + {larger}", total)]
            answer = f"smaller {smaller}; larger {larger}"
            used = [f"multiplier {multiplier}", f"offset {offset}", f"sum {total}"]
            return facts, question, steps, answer, Fraction(smaller), model, used

        tens = random.randint(2, 9)
        ones = random.randint(0, tens - 1)
        digit_sum = tens + ones
        difference = 9 * (tens - ones)
        number, reverse = 10 * tens + ones, 10 * ones + tens
        facts = (f"A two-digit number has digit sum {digit_sum}. It is "
                 f"{difference} greater than the number made by reversing "
                 "its digits.")
        question = "What is the number and its reversal?"
        model = f"a + b = {digit_sum}; (10a+b) - (10b+a) = {difference}"
        gap = tens - ones
        steps = [step("DEFINE_VAR", "a", "tens digit"),
                 step("DEFINE_VAR", "b", "ones digit"),
                 step("MODEL_EQ", f"a + b = {digit_sum}", "digit sum"),
                 step("MODEL_EQ", f"9(a - b) = {difference}", "reversal gap"),
                 step("D", difference, 9, gap),
                 step("A", digit_sum, gap, 2 * tens),
                 step("D", 2 * tens, 2, tens),
                 step("S", digit_sum, tens, ones),
                 step("CHECK", f"{number} - {reverse}", difference)]
        answer = f"number {number}; reversed {reverse}"
        return facts, question, steps, answer, Fraction(number), model, [f"digit sum {digit_sum}", f"gap {difference}"]

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, estimate_value, model, used = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A notice board lists {extra} events. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                  f"{extra} listed events"))
        elif modifier == "estimate_first":
            wrapped = estimate_first(steps + [step("Z", answer)],
                                     estimate_value,
                                     "round the stated totals")
            steps = wrapped[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "relationships in the story"))
            answer = f"{model}; x = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_integer_puzzle_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
