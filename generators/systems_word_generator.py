"""Recover two unknown quantities from paired real-world constraints.

Variants: ``tickets``, ``two_item_purchase``, ``investment_two_rates``,
``mixture_as_system``, ``perimeter_and_relation``, and ``from_table``. Five
context frames and the four applied modifiers are supported. All values are
constructed backward from integral solutions. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``DEFINE_VAR``, ``MODEL_EQ``, ``SUBST``,
``REWRITE``, ``COMB_X``, ``DIV_COEFF``, ``TABLE_ROW``, ``A``, ``S``, ``M``,
``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, money, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("tickets", "two_item_purchase", "investment_two_rates",
            "mixture_as_system", "perimeter_and_relation", "from_table")
FRAMES = (
    "At {place}, {name} reviews this record. {facts} {question}",
    "{question} The record for {name} at {place} says: {facts}",
    "For {name}'s project at {place}: {facts} {question}",
    "A report from {place}, checked by {name}, states: {facts} {question}",
    "Consider the following record that {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


def _two_total_steps(x_name, x_desc, y_name, y_desc, total, high, low,
                     combined, label):
    """Solve x+y=total and high*x+low*y=combined by substitution."""
    low_total = low * total
    difference = high - low
    remainder = combined - low_total
    x_value = remainder // difference
    y_value = total - x_value
    model = f"{x_name} + {y_name} = {total}; {high}{x_name} + {low}{y_name} = {combined}"
    steps = [step("DEFINE_VAR", x_name, x_desc),
             step("DEFINE_VAR", y_name, y_desc),
             step("MODEL_EQ", f"{x_name} + {y_name} = {total}", "total quantity"),
             step("MODEL_EQ", f"{high}{x_name} + {low}{y_name} = {combined}", label),
             step("SUBST", y_name, f"{total} − {x_name}"),
             step("REWRITE", f"{high}{x_name} + {low}({total} − {x_name}) = {combined}"),
             step("M", low, total, low_total),
             step("S", high, low, difference),
             step("S", combined, low_total, remainder),
             step("COMB_X", f"{high}{x_name}", f"−{low}{x_name}",
                  f"{difference}{x_name}"),
             step("MODEL_EQ", f"{difference}{x_name} = {remainder}",
                  "combined equation"),
             step("D", remainder, difference, x_value),
             step("DIV_COEFF", remainder, difference, f"{x_name} = {x_value}"),
             step("S", total, x_value, y_value),
             step("SUBST", y_name, f"{total} − {x_value}", y_value),
             step("M", high, x_value, high * x_value),
             step("M", low, y_value, low * y_value),
             step("A", high * x_value, low * y_value, combined),
             step("CHECK", label, combined)]
    return steps, model


class SystemsWordGenerator(ProblemGenerator):
    """Generate six exact paired-constraint stories without method cues."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _tickets():
        adults, children = random.randint(20, 180), random.randint(15, 160)
        adult_price = random.randint(8, 20)
        child_price = random.randint(3, adult_price - 2)
        total, revenue = adults + children, adult_price * adults + child_price * children
        facts = (f"A theater sold {total} tickets for ${revenue}. Adult tickets "
                 f"cost ${adult_price} and child tickets cost ${child_price}.")
        question = "How many adult tickets and child tickets were sold?"
        steps, model = _two_total_steps("a", "adult tickets", "c", "child tickets",
                                        total, adult_price, child_price, revenue, "revenue")
        answer = f"adults {adults}; children {children}"
        used = [f"{total} tickets", f"${revenue}", f"prices ${adult_price}, ${child_price}"]
        return facts, question, steps, answer, Fraction(adults), model, used, lambda v: unit(v, "ticket")

    @staticmethod
    def _two_item_purchase():
        notebooks, pens = random.randint(4, 45), random.randint(5, 60)
        notebook_price = random.randint(4, 15)
        pen_price = random.randint(1, notebook_price - 1)
        total = notebooks + pens
        cost = notebook_price * notebooks + pen_price * pens
        facts = (f"A supply order contains {total} items and costs ${cost}. Each "
                 f"notebook costs ${notebook_price}, and each pen costs ${pen_price}.")
        question = "How many notebooks and pens are in the order?"
        steps, model = _two_total_steps("n", "notebooks", "p", "pens", total,
                                        notebook_price, pen_price, cost, "order cost")
        answer = f"notebooks {notebooks}; pens {pens}"
        used = [f"{total} items", f"${cost}", f"prices ${notebook_price}, ${pen_price}"]
        return facts, question, steps, answer, Fraction(notebooks), model, used, lambda v: unit(v, "item")

    @staticmethod
    def _investment_two_rates():
        high_amount = 100 * random.randint(10, 90)
        low_amount = 100 * random.randint(10, 90)
        high_rate = random.choice((6, 7, 8, 9, 10, 12))
        low_rate = random.randint(2, high_rate - 2)
        total = high_amount + low_amount
        interest = high_rate * high_amount + low_rate * low_amount
        facts = (f"A total of ${total} is split between accounts paying {high_rate}% "
                 f"and {low_rate}% simple annual interest. After one year, the "
                 f"interest is ${interest // 100}.")
        question = "How much was placed in each account?"
        steps, model = _two_total_steps("h", "dollars at the higher rate", "l",
                                        "dollars at the lower rate", total,
                                        high_rate, low_rate, interest, "interest in cent-percent units")
        answer = f"{high_rate}% account {money(high_amount)}; {low_rate}% account {money(low_amount)}"
        used = [f"total ${total}", f"rates {high_rate}%, {low_rate}%", f"interest ${interest // 100}"]
        return facts, question, steps, answer, Fraction(high_amount), model, used, money

    @staticmethod
    def _mixture_as_system():
        high_volume, low_volume = random.randint(2, 24), random.randint(2, 24)
        high_pct = random.choice((50, 60, 70, 80, 90))
        low_pct = random.choice(tuple(range(5, high_pct - 4, 5)))
        total = high_volume + low_volume
        solute_units = high_pct * high_volume + low_pct * low_volume
        target = Fraction(solute_units, total)
        facts = (f"A blend uses solutions that are {high_pct}% and {low_pct}% "
                 f"concentrated. The final {total} L blend is {target}% concentrated.")
        question = "How many liters of each solution were used?"
        steps, model = _two_total_steps("h", "liters of higher concentration", "l",
                                        "liters of lower concentration", total,
                                        high_pct, low_pct, solute_units, "solute percent-liters")
        answer = f"{high_pct}% solution {high_volume} L; {low_pct}% solution {low_volume} L"
        used = [f"{total} L", f"concentrations {high_pct}%, {low_pct}%, {target}%"]
        return facts, question, steps, answer, Fraction(high_volume), model, used, lambda v: unit(v, "L")

    @staticmethod
    def _perimeter_and_relation():
        width = random.randint(3, 30)
        difference = random.randint(2, 20)
        length = width + difference
        perimeter, half = 2 * (length + width), length + width
        facts = (f"A rectangle has perimeter {perimeter} m. Its length is "
                 f"{difference} m greater than its width.")
        question = "What are the rectangle's length and width?"
        model = f"L + W = {half}; L − W = {difference}"
        steps = [step("DEFINE_VAR", "L", "length in meters"),
                 step("DEFINE_VAR", "W", "width in meters"),
                 step("D", perimeter, 2, half),
                 step("MODEL_EQ", f"L + W = {half}", "half the perimeter"),
                 step("MODEL_EQ", f"L − W = {difference}", "length-width relation"),
                 step("A", half, difference, 2 * length),
                 step("D", 2 * length, 2, length),
                 step("S", half, length, width),
                 step("CHECK", f"2({length} + {width})", perimeter)]
        answer = f"length {length} m; width {width} m"
        used = [f"perimeter {perimeter} m", f"difference {difference} m"]
        return facts, question, steps, answer, Fraction(length), model, used, lambda v: unit(v, "m")

    @staticmethod
    def _from_table():
        first_price, second_price = random.randint(2, 18), random.randint(2, 18)
        while second_price == first_price:
            second_price = random.randint(2, 18)
        a1, b1 = random.randint(1, 9), random.randint(1, 9)
        a2, b2 = random.randint(1, 9), random.randint(1, 9)
        while a1 * b2 == a2 * b1:
            a2, b2 = random.randint(1, 9), random.randint(1, 9)
        total1, total2 = a1 * first_price + b1 * second_price, a2 * first_price + b2 * second_price
        det = a1 * b2 - a2 * b1
        numerator = total1 * b2 - total2 * b1
        remainder = total1 - a1 * first_price
        marker1 = "marker" if a1 == 1 else "markers"
        marker2 = "marker" if a2 == 1 else "markers"
        folder1 = "folder" if b1 == 1 else "folders"
        folder2 = "folder" if b2 == 1 else "folders"
        facts = (f"Two supply orders are listed — order A: {a1} {marker1} and "
                 f"{b1} {folder1} cost ${total1}; order B: {a2} {marker2} and "
                 f"{b2} {folder2} cost ${total2}.")
        question = "What is the price of one marker and one folder?"
        model = f"{a1}m + {b1}f = {total1}; {a2}m + {b2}f = {total2}"
        steps = [step("DEFINE_VAR", "m", "marker price"),
                 step("DEFINE_VAR", "f", "folder price"),
                 step("TABLE_ROW", "order A", f"{a1} markers, {b1} folders", money(total1)),
                 step("TABLE_ROW", "order B", f"{a2} markers, {b2} folders", money(total2)),
                 step("MODEL_EQ", f"{a1}m + {b1}f = {total1}", "order A"),
                 step("MODEL_EQ", f"{a2}m + {b2}f = {total2}", "order B"),
                 step("M", a1, b2, a1 * b2), step("M", a2, b1, a2 * b1),
                 step("S", a1 * b2, a2 * b1, det),
                 step("M", total1, b2, total1 * b2),
                 step("M", total2, b1, total2 * b1),
                 step("S", total1 * b2, total2 * b1, numerator),
                 step("D", numerator, det, first_price),
                 step("M", a1, first_price, a1 * first_price),
                 step("S", total1, a1 * first_price, remainder),
                 step("D", remainder, b1, second_price),
                 step("CHECK", "order B", total2)]
        answer = f"marker {money(first_price)}; folder {money(second_price)}"
        used = [f"order A {a1}, {b1}, ${total1}", f"order B {a2}, {b2}, ${total2}"]
        return facts, question, steps, answer, Fraction(first_price), model, used, money

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(301, 701) if value not in occupied])
            problem = f"An unrelated inventory lists {extra} shipping labels. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} shipping labels"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "estimate one unknown from the paired totals",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "paired constraints"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_systems_word_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
