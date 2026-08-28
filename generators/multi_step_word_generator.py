"""Unstated-method multi-step arithmetic stories for elementary learners.

Variants: ``two_step_buy``, ``groups_then_remove``, ``change_from_bill``,
``time_elapsed``, ``compare_totals``, and ``three_step``.  Each combines exact
hand-friendly arithmetic with five phrasings and modifiers ``plain``,
``distractor``, ``estimate_first``, and ``with_model``.  Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``A``,
``S``, ``M``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import estimate_first, money, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
NAMES = ("Ada", "Ben", "Chi", "Dara", "Eli", "Fatima", "Gus", "Hana",
         "Ivan", "Jo", "Kofi", "Lena", "Mia", "Noor", "Omar", "Pia")
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
PROMPTS = {
    "two_step_buy": (
        "{name} buys {groups} packs with {each} pencils in each pack, then "
        "gives away {remove} pencils. How many pencils remain?",
        "How many pencils does {name} keep after giving away {remove} from "
        "{groups} packs of {each} pencils each?",
        "Pencil order — packs: {groups}; pencils per pack: {each}. {name} "
        "gives away {remove}. Find the number left.",
        "There are {each} pencils in a pack. {name} gets {groups} packs and "
        "hands {remove} pencils to a friend. What remains?",
        "After receiving {groups} equal packs of {each} pencils, {name} "
        "removes {remove} from the collection. Find the remaining pencils.",
    ),
    "groups_then_remove": (
        "A library places {each} books on each of {groups} shelves and later "
        "removes {remove} books. How many books stay on the shelves?",
        "How many books remain after {remove} are removed from {groups} "
        "shelves holding {each} books apiece?",
        "Shelf record — shelves: {groups}; books per shelf: {each}; books "
        "removed: {remove}. Find the books remaining.",
        "Each of {groups} shelves starts with {each} books. The librarian "
        "takes away {remove}. What is the new total?",
        "The library fills {groups} equal shelves with {each} books each, "
        "then checks out {remove}. How many are left?",
    ),
    "change_from_bill": (
        "{name} buys {groups} notebooks at {price} each and pays with {paid}. "
        "How much change should {name} receive?",
        "How much change comes from {paid} after {name} purchases {groups} "
        "notebooks costing {price} apiece?",
        "Purchase record — notebooks: {groups}; price each: {price}; payment: "
        "{paid}. Find the change.",
        "Each notebook costs {price}. {name} takes {groups} and hands the "
        "clerk {paid}. What change is due?",
        "From a payment of {paid}, subtract the cost of {groups} notebooks at "
        "{price} each. How much money remains?",
    ),
    "time_elapsed": (
        "A workshop starts at {start} and ends at {end}. How many minutes "
        "does it last?",
        "How many minutes pass from the workshop's {start} start to its "
        "{end} finish?",
        "Workshop clock record — start: {start}; end: {end}. Find the elapsed "
        "time in minutes.",
        "The clock reads {start} when a workshop begins and {end} when it "
        "finishes. What is its duration in minutes?",
        "From {start} until {end}, a class stays in session. Report the total "
        "number of minutes.",
    ),
    "compare_totals": (
        "Team Red scores {r1}, {r2}, and {r3} points in three rounds. Team "
        "Blue scores {b1}, {b2}, and {b3}. By how many points does Red win?",
        "By how many points is Red's total above Blue's if Red has {r1}, "
        "{r2}, {r3} and Blue has {b1}, {b2}, {b3}?",
        "Scoreboard — Red: {r1}, {r2}, {r3}; Blue: {b1}, {b2}, {b3}. Find "
        "Red's winning margin.",
        "Across three rounds Red earns {r1}, then {r2}, then {r3} points; "
        "Blue earns {b1}, then {b2}, then {b3}. What is the difference?",
        "Compare the totals for Red ({r1}, {r2}, {r3}) and Blue ({b1}, {b2}, "
        "{b3}). How many more points does Red have?",
    ),
    "three_step": (
        "A food drive receives {groups} boxes of {each} cans, plus {extra} "
        "loose cans, then donates {remove}. How many cans remain?",
        "How many cans remain after donating {remove} from {groups} boxes of "
        "{each} cans plus {extra} loose cans?",
        "Food-drive record — boxes: {groups}; cans per box: {each}; loose "
        "cans: {extra}; donated: {remove}. Find the final count.",
        "Volunteers collect {groups} equal boxes with {each} cans each and "
        "add {extra} loose cans. After {remove} leave, what remains?",
        "Start with {groups} boxes of {each} cans and {extra} separate cans. "
        "The drive gives away {remove}. Find the cans left.",
    ),
}


class MultiStepWordGenerator(ProblemGenerator):
    """Generate six exact multi-step story families with standard modifiers."""

    VARIANTS = tuple(PROMPTS)
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("pencil", "book", "$", "minute", "point", "can")

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _base_case(variant):
        name = random.choice(NAMES)
        if variant in ("two_step_buy", "groups_then_remove"):
            groups = random.randint(3, 12)
            each = random.randint(4, 15)
            product = groups * each
            remove = random.randint(1, product - 1)
            answer_value = product - remove
            noun = "pencils" if variant == "two_step_buy" else "books"
            fields = dict(name=name, groups=groups, each=each, remove=remove)
            steps = [step("M", groups, each, product),
                     step("S", product, remove, answer_value),
                     step("CHECK", "add back", f"{answer_value} + {remove}",
                          product)]
            answer = f"{answer_value} {noun}"
            model = f"x = {groups} * {each} - {remove}"
            used = [f"{groups} groups", f"{each} per group", f"{remove} removed"]
            return fields, steps, answer, Fraction(answer_value), model, used, None

        if variant == "change_from_bill":
            groups = random.randint(2, 8)
            price = Fraction(random.randint(4, 20), 4)
            cost = groups * price
            paid = Fraction((cost.numerator + cost.denominator - 1)
                            // cost.denominator + random.randint(2, 15))
            change = paid - cost
            fields = dict(name=name, groups=groups, price=money(price),
                          paid=money(paid))
            steps = [step("M", groups, str(price), str(cost)),
                     step("S", str(paid), str(cost), str(change)),
                     step("CHECK", "cost plus change",
                          f"{cost} + {change}", str(paid))]
            answer = money(change)
            model = f"x = {paid} - {groups} * {price}"
            used = [f"{groups} notebooks", money(price), money(paid)]
            return fields, steps, answer, change, model, used, money

        if variant == "time_elapsed":
            start_hour = random.randint(7, 15)
            start_minute = random.choice((0, 5, 10, 15, 20, 25, 30, 35, 40, 45))
            duration = random.randint(3, 24) * 5
            start_total = start_hour * 60 + start_minute
            end_total = start_total + duration
            end_hour, end_minute = divmod(end_total, 60)
            start = f"{start_hour}:{start_minute:02d}"
            end = f"{end_hour}:{end_minute:02d}"
            fields = dict(start=start, end=end)
            steps = [step("M", start_hour, 60, start_hour * 60),
                     step("A", start_hour * 60, start_minute, start_total),
                     step("M", end_hour, 60, end_hour * 60),
                     step("A", end_hour * 60, end_minute, end_total),
                     step("S", end_total, start_total, duration),
                     step("CHECK", "start plus elapsed",
                          f"{start_total} + {duration}", end_total)]
            answer = f"{duration} minutes"
            model = f"x = ({end_hour} * 60 + {end_minute}) - ({start_hour} * 60 + {start_minute})"
            used = [f"start {start}", f"end {end}"]
            return fields, steps, answer, Fraction(duration), model, used, None

        if variant == "compare_totals":
            blue = [random.randint(5, 30) for _ in range(3)]
            red = [value + random.randint(1, 8) for value in blue]
            red_total, blue_total = sum(red), sum(blue)
            margin = red_total - blue_total
            fields = dict(r1=red[0], r2=red[1], r3=red[2],
                          b1=blue[0], b2=blue[1], b3=blue[2])
            steps = [step("A", red[0], red[1], red[0] + red[1]),
                     step("A", red[0] + red[1], red[2], red_total),
                     step("A", blue[0], blue[1], blue[0] + blue[1]),
                     step("A", blue[0] + blue[1], blue[2], blue_total),
                     step("S", red_total, blue_total, margin),
                     step("CHECK", "round differences",
                          f"{red[0]-blue[0]} + {red[1]-blue[1]} + {red[2]-blue[2]}",
                          margin)]
            answer = f"Red by {margin} points"
            model = (f"Red = {red[0]} + {red[1]} + {red[2]}; "
                     f"Blue = {blue[0]} + {blue[1]} + {blue[2]}")
            used = [f"Red {','.join(map(str, red))}",
                    f"Blue {','.join(map(str, blue))}"]
            return fields, steps, answer, Fraction(margin), model, used, None

        groups = random.randint(3, 12)
        each = random.randint(4, 15)
        extra = random.randint(2, 30)
        subtotal = groups * each + extra
        remove = random.randint(1, subtotal - 1)
        answer_value = subtotal - remove
        fields = dict(groups=groups, each=each, extra=extra, remove=remove)
        steps = [step("M", groups, each, groups * each),
                 step("A", groups * each, extra, subtotal),
                 step("S", subtotal, remove, answer_value),
                 step("CHECK", "rebuild total",
                      f"{answer_value} + {remove}", subtotal)]
        answer = f"{answer_value} cans"
        model = f"x = {groups} * {each} + {extra} - {remove}"
        used = [f"{groups} boxes", f"{each} per box", f"{extra} loose",
                f"{remove} donated"]
        return fields, steps, answer, Fraction(answer_value), model, used, None

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        fields, steps, answer, value, model, used, renderer = self._base_case(variant)
        problem = random.choice(PROMPTS[variant]).format(**fields)

        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            distractor = random.choice([number for number in range(41, 100)
                                        if number not in occupied])
            problem = f"A nearby room has {distractor} chairs. {problem}"
            steps.insert(0, select_relevant_step(
                used, f"{distractor} chairs in a nearby room"))
        elif modifier == "estimate_first":
            base = steps + [step("Z", answer)]
            steps = estimate_first(base, value, "round the story quantities",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            answer = f"{model}; x = {answer}"
            steps.insert(0, step("MODEL_EQ", model, "quantities in the story"))

        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_multi_step_word_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
