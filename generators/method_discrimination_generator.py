"""Paired quantitative tasks that differ only in their structural cue.

Variants: ``combination_vs_permutation``, ``independent_vs_dependent``,
``area_vs_perimeter``, ``mean_vs_median``, ``linear_vs_exponential``,
``proportional_vs_not``, ``additive_vs_multiplicative``, and
``pythagoras_vs_similar``. Five shared-context renderings and all four applied
modifiers are supported. Problems never name the methods; composite answers
pair every label with a computed fact. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``DISCRIMINATE``, ``NCR``,
``NPR``, ``SORT``, ``RATIO_CHECK``, ``A``, ``M``, ``D``, ``E``, ``ROOT``,
``CHECK``, and ``Z``.
"""
import math
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("combination_vs_permutation", "independent_vs_dependent",
            "area_vs_perimeter", "mean_vs_median", "linear_vs_exponential",
            "proportional_vs_not", "additive_vs_multiplicative",
            "pythagoras_vs_similar")
FRAMES = (
    "At {place}, {name} compares two tasks. {facts} {question}",
    "{question} A note by {name} at {place} gives these tasks: {facts}",
    "For {name} at {place}: {facts} {question}",
    "At {place}, the paired record from {name} says: {facts} {question}",
    "Consider {name}'s paired report from {place}. {facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("classroom", "shop", "trip", "workshop", "business")
    for setting in CONTEXTS[key].settings
)
TRIPLES = ((3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17))


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def probability(value):
    return exact(Fraction(value))


class MethodDiscriminationGenerator(ProblemGenerator):
    """Generate exact contrast pairs with standard applied modifiers."""

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
    def _combination_permutation():
        n = random.randint(5, 10)
        r = random.randint(2, min(4, n - 1))
        choose = math.comb(n, r)
        arrange = math.prod(range(n - r + 1, n + 1))
        facts = (f"Task A selects {r} of {n} books for a trip, where changing "
                 f"their order does not create a new selection. Task B places "
                 f"{r} of the same {n} books in a row, where a different order "
                 "does create a new result.")
        question = "Name the structure of each task and give its number of outcomes."
        model = f"A=C({n},{r}); B=P({n},{r})"
        steps = [step("DISCRIMINATE", "A", "combination", "order irrelevant"),
                 step("NCR", f"C({n},{r})", choose),
                 step("DISCRIMINATE", "B", "permutation", "order matters"),
                 step("NPR", f"P({n},{r})", arrange),
                 step("CHECK", "paired counts", f"{choose}, {arrange}")]
        answer = f"A: combination, {choose}; B: permutation, {arrange}"
        used = [f"{r} of {n} books", "A order irrelevant", "B order matters"]
        return facts, question, steps, answer, Fraction(choose), model, used, exact

    @staticmethod
    def _independent_dependent():
        red = random.randint(2, 6)
        total = random.randint(red + 2, red + 8)
        with_replacement = Fraction(red, total) ** 2
        without_replacement = Fraction(red, total) * Fraction(red - 1, total - 1)
        facts = (f"A bag contains {red} red tokens among {total} tokens. Task A "
                 "draws a token, returns it, mixes, and draws again. Task B draws "
                 "twice from the same bag but does not return the first token.")
        question = "Classify how the two draws relate in each task and find the chance of two red draws."
        model = (f"A=({red}/{total})^2; B=({red}/{total})*"
                 f"({red - 1}/{total - 1})")
        steps = [step("DISCRIMINATE", "A", "independent", "first token returned"),
                 step("M", f"{red}/{total}", f"{red}/{total}",
                      probability(with_replacement)),
                 step("DISCRIMINATE", "B", "dependent", "bag composition changes"),
                 step("M", f"{red}/{total}", f"{red - 1}/{total - 1}",
                      probability(without_replacement)),
                 step("CHECK", "without-return chance is smaller",
                      f"{probability(without_replacement)} < {probability(with_replacement)}")]
        answer = (f"A: independent, {probability(with_replacement)}; B: dependent, "
                  f"{probability(without_replacement)}")
        used = [f"{red} red of {total}", "A returns first token", "B does not"]
        return (facts, question, steps, answer, with_replacement, model, used,
                probability)

    @staticmethod
    def _area_perimeter():
        length, width = random.sample(range(3, 16), 2)
        perimeter = 2 * (length + width)
        area = length * width
        facts = (f"The same rectangle is {length} cm long and {width} cm wide. "
                 "Task A asks for ribbon around its boundary. Task B asks for "
                 "paper covering its entire face.")
        question = "Name the quantity needed in each task and compute it."
        model = f"A=2({length}+{width}); B={length}*{width}"
        steps = [step("DISCRIMINATE", "A", "perimeter", "boundary length"),
                 step("A", length, width, length + width),
                 step("M", 2, length + width, perimeter),
                 step("DISCRIMINATE", "B", "area", "surface covered"),
                 step("M", length, width, area),
                 step("CHECK", "units differ", f"{perimeter} cm vs {area} cm²")]
        answer = f"A: perimeter, {perimeter} cm; B: area, {area} cm²"
        used = [f"length {length} cm", f"width {width} cm", "boundary vs face"]
        return (facts, question, steps, answer, Fraction(perimeter), model, used,
                lambda value: unit(value, "cm"))

    @staticmethod
    def _mean_median():
        start = random.randint(2, 15)
        gap = random.randint(1, 5)
        values = [start, start + gap, start + 2 * gap,
                  start + 3 * gap, start + 9 * gap]
        total = sum(values)
        mean = Fraction(total, 5)
        median = values[2]
        data = ", ".join(map(str, values))
        facts = (f"Both tasks use the data list {data}. Task A asks for the "
                 "equal-share value if the total were spread across all five "
                 "entries. Task B asks for the middle entry after ordering.")
        question = "Name the summary used by each task and give its value."
        model = f"A=({'+'.join(map(str, values))})/5; B=middle({data})"
        running = values[0]
        steps = [step("DISCRIMINATE", "A", "mean", "equal-share value")]
        for value in values[1:]:
            steps.append(step("A", running, value, running + value))
            running += value
        steps += [step("D", total, 5, exact(mean)),
                  step("DISCRIMINATE", "B", "median", "ordered middle"),
                  step("SORT", data, data),
                  step("CHECK", "third of five", median)]
        answer = f"A: mean, {exact(mean)}; B: median, {median}"
        used = [f"data {data}", "equal-share vs middle"]
        return facts, question, steps, answer, mean, model, used, exact

    @staticmethod
    def _linear_exponential():
        while True:
            start = random.randrange(50, 201, 10)
            change = random.choice((5, 10, 20, 25))
            years = random.randint(2, 4)
            linear = start + change * years
            exponential = Fraction(start) * Fraction(100 + change, 100) ** years
            if (exponential * 100).denominator == 1:
                break
        facts = (f"Two accounts each start with {money(start)}. Account A adds "
                 f"{money(change)} at the end of every year. Account B grows by "
                 f"{change}% of its current balance each year. Compare them after "
                 f"{years} years.")
        question = "Name each growth pattern and compute both balances."
        model = (f"A={start}+{change}*{years}; "
                 f"B={start}*(1+{change}/100)^{years}")
        steps = [step("DISCRIMINATE", "A", "linear", "same amount added"),
                 step("M", change, years, change * years),
                 step("A", start, change * years, linear),
                 step("DISCRIMINATE", "B", "exponential", "same percent of current"),
                 step("E", Fraction(100 + change, 100), years,
                      exact(Fraction(100 + change, 100) ** years)),
                 step("M", start, exact(Fraction(100 + change, 100) ** years),
                      exact(exponential)),
                 step("CHECK", "balances after years",
                      f"{money(linear)}, {money(exponential)}")]
        answer = (f"A: linear, {money(linear)}; B: exponential, "
                  f"{money(exponential)}")
        used = [f"start {money(start)}", f"change {change}", f"{years} years"]
        return facts, question, steps, answer, Fraction(linear), model, used, money

    @staticmethod
    def _proportional_not():
        rate = random.randint(2, 12)
        fixed = random.randint(2, 10)
        xs = (1, 2, 4)
        ys_a = tuple(rate * x for x in xs)
        ys_b = tuple(fixed + rate * x for x in xs)
        query = random.randint(5, 10)
        qa, qb = rate * query, fixed + rate * query
        rows_a = "; ".join(f"{x} to {y}" for x, y in zip(xs, ys_a))
        rows_b = "; ".join(f"{x} to {y}" for x, y in zip(xs, ys_b))
        facts = (f"Task A gives input-output records {rows_a}. Task B uses the "
                 f"same inputs but records {rows_b}.")
        question = (f"Which record keeps one output-to-input ratio, and what does "
                    f"each record give at input {query}?")
        model = f"A:y={rate}x; B:y={fixed}+{rate}x"
        steps = [step("D", ys_a[0], xs[0], rate),
                 step("D", ys_a[1], xs[1], rate),
                 step("RATIO_CHECK", "A", f"{rate}, {rate}, {rate}", "constant"),
                 step("D", ys_b[0], xs[0], exact(Fraction(ys_b[0], xs[0]))),
                 step("D", ys_b[1], xs[1], exact(Fraction(ys_b[1], xs[1]))),
                 step("RATIO_CHECK", "B", "ratios differ", "not constant"),
                 step("M", rate, query, qa),
                 step("A", fixed, qa, qb),
                 step("CHECK", f"input {query}", f"A {qa}, B {qb}")]
        answer = (f"A: proportional, y={qa}; B: not proportional, y={qb} at "
                  f"x={query}")
        used = [f"A records {rows_a}", f"B records {rows_b}", f"query {query}"]
        return facts, question, steps, answer, Fraction(qa), model, used, exact

    @staticmethod
    def _additive_multiplicative():
        start = random.randint(2, 12)
        change = random.choice((2, 3))
        rounds = random.randint(2, 5)
        additive = start + change * rounds
        multiplicative = start * change ** rounds
        facts = (f"Two machines start at {start} units and run for {rounds} "
                 f"rounds. Machine A adds {change} units each round. Machine B "
                 f"makes its current value {change} times as large each round.")
        question = "Name each update pattern and compute both final values."
        model = f"A={start}+{change}*{rounds}; B={start}*{change}^{rounds}"
        steps = [step("DISCRIMINATE", "A", "additive", "fixed amount each round"),
                 step("M", change, rounds, change * rounds),
                 step("A", start, change * rounds, additive),
                 step("DISCRIMINATE", "B", "multiplicative", "current value scaled"),
                 step("E", change, rounds, change ** rounds),
                 step("M", start, change ** rounds, multiplicative),
                 step("CHECK", "final values", f"{additive}, {multiplicative}")]
        answer = (f"A: additive, {additive} units; B: multiplicative, "
                  f"{multiplicative} units")
        used = [f"start {start}", f"change {change}", f"{rounds} rounds"]
        return facts, question, steps, answer, Fraction(additive), model, used, exact

    @staticmethod
    def _pythagoras_similar():
        first, second, hypotenuse = random.choice(TRIPLES)
        scale = random.randint(2, 5)
        scaled_first, scaled_second = scale * first, scale * second
        facts = (f"Task A has a right triangle with perpendicular sides {first} "
                 f"m and {second} m and asks for the side across from the right "
                 f"angle. Task B has a small triangle with sides {first} m and "
                 f"{second} m; a same-shape larger triangle has the corresponding "
                 f"first side {scaled_first} m and asks for its corresponding "
                 "second side.")
        question = "Name the relationship used in each task and compute both missing sides."
        model = (f"A:c^2={first}^2+{second}^2; "
                 f"B:{first}/{second}={scaled_first}/x")
        steps = [step("DISCRIMINATE", "A", "Pythagoras", "right-angle side relation"),
                 step("E", first, 2, first ** 2),
                 step("E", second, 2, second ** 2),
                 step("A", first ** 2, second ** 2, hypotenuse ** 2),
                 step("ROOT", hypotenuse ** 2, hypotenuse),
                 step("DISCRIMINATE", "B", "similar triangles", "corresponding scale"),
                 step("D", scaled_first, first, scale),
                 step("M", second, scale, scaled_second),
                 step("CHECK", "two missing sides",
                      f"{hypotenuse} m, {scaled_second} m")]
        answer = (f"A: Pythagoras, {hypotenuse} m; B: similar triangles, "
                  f"{scaled_second} m")
        used = [f"sides {first}, {second}", f"scaled side {scaled_first}"]
        return (facts, question, steps, answer, Fraction(hypotenuse), model, used,
                lambda value: unit(value, "m"))

    @classmethod
    def _case(cls, variant):
        methods = {
            "combination_vs_permutation": cls._combination_permutation,
            "independent_vs_dependent": cls._independent_dependent,
            "area_vs_perimeter": cls._area_perimeter,
            "mean_vs_median": cls._mean_median,
            "linear_vs_exponential": cls._linear_exponential,
            "proportional_vs_not": cls._proportional_not,
            "additive_vs_multiplicative": cls._additive_multiplicative,
            "pythagoras_vs_similar": cls._pythagoras_similar,
        }
        return methods[variant]()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(41, 100)
                                   if number not in occupied])
            problem = f"A shelf nearby holds {extra} blank cards. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} blank cards"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "estimate the first task before comparing structures",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "paired structures"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_method_discrimination_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
