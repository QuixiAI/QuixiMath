"""Derive reusable relationships through concrete exact examples.

Variants: ``arithmetic_series_pairing``,
``interior_angle_sum_triangulation``, ``triangle_area_from_rectangle``,
``trapezoid_from_triangles``, ``distance_formula_from_pythagoras``,
``divide_by_fraction_reciprocal``,
``compound_interest_repeated_multiplication``, and
``quadratic_formula_complete_square_concrete``. Five context frames and all
four applied modifiers are supported. Each variant follows one fixed,
explicit canonical route. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``DERIVE``, ``GENERALIZE``, ``SERIES_PAIR``,
``TRIANGULATE``, ``COMMON_DEN``, ``REWRITE``, ``ROOT``, ``A``, ``S``, ``M``,
``D``, ``E``, ``CHECK``, and ``Z``.
"""
import math
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, exact, money, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("arithmetic_series_pairing", "interior_angle_sum_triangulation",
            "triangle_area_from_rectangle", "trapezoid_from_triangles",
            "distance_formula_from_pythagoras", "divide_by_fraction_reciprocal",
            "compound_interest_repeated_multiplication",
            "quadratic_formula_complete_square_concrete")
FRAMES = (
    "At {place}, {name} develops a general relationship. {facts} {question}",
    "{question} A derivation task for {name} at {place} states: {facts}",
    "For {name}'s work at {place}: {facts} {question}",
    "A note from {place}, checked by {name}, gives: {facts} {question}",
    "Consider the exact example {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("classroom", "workshop", "garden", "business")
               for setting in CONTEXTS[key].settings)
TRIPLES = ((3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15))


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class FormulaDerivationGenerator(ProblemGenerator):
    """Generate eight concrete-to-general exact derivations."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _arithmetic_series_pairing():
        n = 2 * random.randint(5, 60)
        pair_sum, pairs, total = n + 1, n // 2, n * (n + 1) // 2
        facts = f"The sum is 1 + 2 + ... + {n}."
        question = "Show a general expression for 1 + 2 + ... + n, then evaluate this sum."
        model = "S = n(n + 1)/2"
        steps = [step("SERIES_PAIR", f"1 + {n}", pair_sum),
                 step("SERIES_PAIR", f"2 + {n - 1}", pair_sum),
                 step("D", n, 2, pairs),
                 step("DERIVE", f"{pairs} pairs", f"each sums to {pair_sum}"),
                 step("M", pairs, pair_sum, total),
                 step("GENERALIZE", "n/2 pairs of (n + 1)", model),
                 step("CHECK", f"n = {n}", f"{n}·{n + 1}/2 = {total}")]
        answer = f"{model}; S_{n} = {total}"
        used = [f"sum through {n}"]
        return facts, question, steps, answer, Fraction(total), model, used, str

    @staticmethod
    def _interior_angle_sum_triangulation():
        sides = random.randint(4, 15)
        triangles, total = sides - 2, (sides - 2) * 180
        facts = f"A convex polygon has {sides} sides."
        question = "Build a general expression for its interior-angle total, then evaluate it."
        model = "interior total = (n − 2)·180°"
        steps = [step("TRIANGULATE", f"{sides}-gon", triangles),
                 step("S", sides, 2, triangles),
                 step("DERIVE", f"{triangles} triangles", "180° each"),
                 step("M", triangles, 180, total),
                 step("GENERALIZE", "n-sided polygon", model),
                 step("CHECK", f"n = {sides}", unit(total, "°"))]
        answer = f"{model}; {total}°"
        used = [f"convex polygon {sides} sides"]
        return facts, question, steps, answer, Fraction(total), model, used, lambda v: unit(v, "°")

    @staticmethod
    def _triangle_area_from_rectangle():
        base, height = random.randint(3, 30), random.randint(2, 20)
        rectangle, area = base * height, Fraction(base * height, 2)
        facts = f"A triangle has base {base} cm and perpendicular height {height} cm."
        question = "Relate it to a matching rectangle, state the general area relationship, and find its area."
        model = "A = bh/2"
        steps = [step("DERIVE", "two matching triangles", "one b by h rectangle"),
                 step("M", base, height, rectangle), step("D", rectangle, 2, exact(area)),
                 step("GENERALIZE", "half of bh", model),
                 step("CHECK", f"2 × {exact(area)}", rectangle)]
        answer = f"{model}; {exact(area)} cm²"
        used = [f"base {base} cm", f"height {height} cm"]
        return facts, question, steps, answer, area, model, used, lambda v: unit(v, "cm²")

    @staticmethod
    def _trapezoid_from_triangles():
        base1, base2 = random.randint(8, 30), random.randint(3, 7)
        height = 2 * random.randint(2, 10)
        area1, area2 = Fraction(base1 * height, 2), Fraction(base2 * height, 2)
        area = area1 + area2
        facts = (f"A trapezoid has parallel sides {base1} cm and {base2} cm and "
                 f"perpendicular height {height} cm.")
        question = "Split it into two triangles, state the general area relationship, and find its area."
        model = "A = (b1 + b2)h/2"
        steps = [step("DERIVE", "triangle 1", f"{base1}·{height}/2"),
                 step("M", base1, height, base1 * height),
                 step("D", base1 * height, 2, exact(area1)),
                 step("DERIVE", "triangle 2", f"{base2}·{height}/2"),
                 step("M", base2, height, base2 * height),
                 step("D", base2 * height, 2, exact(area2)),
                 step("A", exact(area1), exact(area2), exact(area)),
                 step("GENERALIZE", "sum the two triangle areas", model),
                 step("CHECK", f"({base1}+{base2})·{height}/2", exact(area))]
        answer = f"{model}; {exact(area)} cm²"
        used = [f"parallel sides {base1}, {base2} cm", f"height {height} cm"]
        return facts, question, steps, answer, area, model, used, lambda v: unit(v, "cm²")

    @staticmethod
    def _distance_formula_from_pythagoras():
        dx, dy, distance = random.choice(TRIPLES)
        x1, y1 = random.randint(-20, 20), random.randint(-20, 20)
        x2 = x1 + dx * random.choice((-1, 1))
        y2 = y1 + dy * random.choice((-1, 1))
        actual_dx, actual_dy = x2 - x1, y2 - y1
        model = "d = sqrt((x2 − x1)^2 + (y2 − y1)^2)"
        facts = f"Two points are ({x1}, {y1}) and ({x2}, {y2})."
        question = "Use their horizontal and vertical changes to state the general distance relationship and find this distance."
        steps = [step("S", x2, x1, actual_dx), step("S", y2, y1, actual_dy),
                 step("E", actual_dx, 2, actual_dx ** 2),
                 step("E", actual_dy, 2, actual_dy ** 2),
                 step("A", actual_dx ** 2, actual_dy ** 2, distance ** 2),
                 step("ROOT", distance ** 2, distance),
                 step("GENERALIZE", "right-triangle legs Δx and Δy", model),
                 step("CHECK", f"{distance}²", distance ** 2)]
        answer = f"{model}; d = {distance}"
        used = [f"points ({x1}, {y1}), ({x2}, {y2})"]
        return facts, question, steps, answer, Fraction(distance), model, used, str

    @staticmethod
    def _divide_by_fraction_reciprocal():
        first = Fraction(random.randint(2, 12), random.randint(2, 12))
        second = Fraction(random.randint(2, 12), random.randint(2, 12))
        while first.denominator == 1 or second.denominator == 1:
            first = Fraction(random.randint(2, 12), random.randint(2, 12))
            second = Fraction(random.randint(2, 12), random.randint(2, 12))
        common = math.lcm(first.denominator, second.denominator)
        scaled_first = first.numerator * (common // first.denominator)
        scaled_second = second.numerator * (common // second.denominator)
        result = first / second
        model = "a/b ÷ c/d = ad/bc"
        facts = f"The exact calculation is {first} ÷ {second}."
        question = "Rewrite both quantities with one denominator, then state the general multiplication relationship and evaluate."
        steps = [step("COMMON_DEN", common),
                 step("M", first.numerator, common // first.denominator, scaled_first),
                 step("M", second.numerator, common // second.denominator, scaled_second),
                 step("REWRITE", f"{scaled_first}/{common} ÷ {scaled_second}/{common}"),
                 step("D", scaled_first, scaled_second, exact(result)),
                 step("DERIVE", "equal-sized parts", f"{scaled_first}/{scaled_second}"),
                 step("GENERALIZE", "multiply by d/c", model),
                 step("CHECK", f"{first} × {second.denominator}/{second.numerator}", exact(result))]
        answer = f"{model}; {first} ÷ {second} = {result}"
        used = [f"fractions {first}, {second}"]
        return facts, question, steps, answer, result, model, used, exact

    @staticmethod
    def _compound_interest_repeated_multiplication():
        rate = random.choice((10, 20, 25, 50))
        years = random.randint(2, 4)
        factor = 1 + Fraction(rate, 100)
        stride = factor.denominator ** years
        principal = stride * random.randint(20, 300)
        value = Fraction(principal) * factor ** years
        model = "A = P(1 + r)^t"
        facts = (f"An account starts with {money(principal)} and grows {rate}% "
                 f"once per year for {years} years.")
        question = "Show the repeated yearly multiplication, state the general relationship, and find the final balance."
        steps = [step("A", 1, exact(Fraction(rate, 100)), exact(factor))]
        current = Fraction(principal)
        for year in range(1, years + 1):
            next_value = current * factor
            steps += [step("M", exact(current), exact(factor), exact(next_value)),
                      step("DERIVE", f"year {year}", money(next_value))]
            current = next_value
        steps += [step("GENERALIZE", "same factor t times", model),
                  step("CHECK", f"P({exact(factor)})^{years}", money(value))]
        answer = f"{model}; after {years} years {money(value)}"
        used = [f"principal {money(principal)}", f"rate {rate}%", f"years {years}"]
        return facts, question, steps, answer, value, model, used, money

    @staticmethod
    def _quadratic_formula_complete_square_concrete():
        roots = tuple(value for value in range(-12, 13) if value != 0)
        root1, root2 = sorted(random.sample(roots, 2))
        while root1 + root2 == 0 or abs(root1 + root2) == 1:
            root1, root2 = sorted(random.sample(roots, 2))
        b, c = -(root1 + root2), root1 * root2
        half_b = Fraction(b, 2)
        square = half_b ** 2
        right = square - c
        root_right = abs(Fraction(root2 - root1, 2))
        equation = f"x² {'+' if b >= 0 else '−'} {abs(b)}x {'+' if c >= 0 else '−'} {abs(c)} = 0"
        binomial = f"x + {exact(half_b)}" if half_b >= 0 else f"x − {exact(-half_b)}"
        model = "x = (−b ± sqrt(b² − 4ac))/(2a)"
        facts = f"The equation is {equation}."
        question = "Rearrange it into a square, state the corresponding general relationship, and give both exact solutions."
        steps = [step("S", 0, c, -c),
                 step("REWRITE", f"x² {'+' if b >= 0 else '−'} {abs(b)}x = {-c}"),
                 step("D", b, 2, exact(half_b)),
                 step("E", exact(half_b), 2, exact(square)),
                 step("A", -c, exact(square), exact(right)),
                 step("REWRITE", f"({binomial})² = {exact(right)}"),
                 step("ROOT", exact(right), exact(root_right)),
                 step("S", exact(root_right), exact(half_b), root2),
                 step("S", exact(-root_right), exact(half_b), root1),
                 step("GENERALIZE", "complete the square for ax² + bx + c", model),
                 step("CHECK", f"roots {root1}, {root2}", f"sum {-b}, product {c}")]
        answer = f"{model}; x = {root1} or x = {root2}"
        used = [equation]
        return facts, question, steps, answer, Fraction(max(abs(root1), abs(root2))), model, used, str

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
            extra = random.choice([value for value in range(901, 1301) if value not in occupied])
            problem = f"An unrelated cabinet holds {extra} index cards. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} index cards"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the applied value before generalizing",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "general relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_formula_derivation_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
