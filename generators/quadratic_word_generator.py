"""Solve exact quadratic models embedded in practical stories.

Variants: ``projectile_ground_time``, ``projectile_max_height``,
``area_with_border``, ``revenue_linear_demand``,
``rectangle_from_area_perimeter``, and ``consecutive_product``. Five context
frames and all four applied modifiers are supported. Problems are constructed
backward from integral roots or vertices. Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``REWRITE``, ``ZERO_PRODUCT``,
``REVENUE``, ``TRY``, ``REJECT``, ``ACCEPT``, ``A``, ``S``, ``M``, ``D``,
``E``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, estimate_first, money, select_relevant_step, unit
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("projectile_ground_time", "projectile_max_height",
            "area_with_border", "revenue_linear_demand",
            "rectangle_from_area_perimeter", "consecutive_product")
FRAMES = (
    "At {place}, {name} studies this situation. {facts} {question}",
    "{question} A report for {name} from {place} states: {facts}",
    "For a project at {place}, {name} is given: {facts} {question}",
    "A note reviewed by {name} at {place} reads: {facts} {question}",
    "Consider the situation {name} recorded at {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("sports", "garden", "business", "classroom")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


def _signed(value):
    return f"+ {value}" if value >= 0 else f"− {abs(value)}"


def _poly(a, b, c, variable="t"):
    first = f"{a}{variable}²" if a != -1 else f"−{variable}²"
    if a == 1:
        first = f"{variable}²"
    if b == 0:
        middle = ""
    elif abs(b) == 1:
        middle = f" {'+' if b > 0 else '−'} {variable}"
    else:
        middle = f" {_signed(b)}{variable}"
    constant = "" if c == 0 else f" {_signed(c)}"
    return first + middle + constant


class QuadraticWordGenerator(ProblemGenerator):
    """Generate six exact contextual quadratic problems without method cues."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _projectile_ground_time():
        positive, negative = random.randint(2, 10), random.randint(1, 6)
        while negative == positive:
            negative = random.randint(1, 6)
        scale = random.randint(2, 5)
        a = -scale
        b = scale * (positive - negative)
        c = scale * positive * negative
        expression = _poly(a, b, c)
        normalized_b, normalized_c = negative - positive, -positive * negative
        normalized = _poly(1, normalized_b, normalized_c)
        facts = f"A ball's height in meters after t seconds is h(t) = {expression}."
        question = "When does the ball reach the ground?"
        model = f"{expression} = 0"
        steps = [step("MODEL_EQ", model, "height is zero"),
                 step("D", a, a, 1), step("D", b, a, normalized_b),
                 step("D", c, a, normalized_c), step("REWRITE", f"{normalized} = 0"),
                 step("ZERO_PRODUCT", f"(t − {positive})(t + {negative}) = 0"),
                 step("TRY", f"t = −{negative}"),
                 step("REJECT", f"t = −{negative}", "negative time"),
                 step("TRY", f"t = {positive}"), step("ACCEPT", f"t = {positive}"),
                 step("E", positive, 2, positive ** 2),
                 step("M", a, positive ** 2, a * positive ** 2),
                 step("M", b, positive, b * positive),
                 step("A", a * positive ** 2, b * positive, a * positive ** 2 + b * positive),
                 step("A", a * positive ** 2 + b * positive, c, 0),
                 step("CHECK", f"h({positive})", 0)]
        answer = unit(positive, "second")
        used = [expression, "height 0 m"]
        return facts, question, steps, answer, Fraction(positive), model, used, lambda v: unit(v, "second")

    @staticmethod
    def _projectile_max_height():
        vertex_time = random.randint(2, 9)
        scale = random.randint(2, 5)
        initial = random.randint(1, 30)
        maximum = initial + scale * vertex_time ** 2
        a, b, c = -scale, 2 * scale * vertex_time, initial
        expression = _poly(a, b, c)
        facts = f"A launched object's height in meters after t seconds is h(t) = {expression}."
        question = "At what time is it highest, and what is that height?"
        model = f"h(t) = {expression}"
        before = maximum - scale
        steps = [step("MODEL_EQ", model, "height over time"),
                 step("M", 2, a, 2 * a), step("D", -b, 2 * a, vertex_time),
                 step("E", vertex_time, 2, vertex_time ** 2),
                 step("M", a, vertex_time ** 2, a * vertex_time ** 2),
                 step("M", b, vertex_time, b * vertex_time),
                 step("A", a * vertex_time ** 2, b * vertex_time,
                      a * vertex_time ** 2 + b * vertex_time),
                 step("A", a * vertex_time ** 2 + b * vertex_time, c, maximum),
                 step("TRY", f"t = {vertex_time - 1}", unit(before, "m")),
                 step("TRY", f"t = {vertex_time + 1}", unit(before, "m")),
                 step("ACCEPT", f"t = {vertex_time}", unit(maximum, "m")),
                 step("CHECK", "neighboring times are lower", f"{before} < {maximum}")]
        answer = f"at {vertex_time} seconds; {maximum} m"
        used = [expression, "time t in seconds", "height in meters"]
        return facts, question, steps, answer, Fraction(maximum), model, used, lambda v: unit(v, "m")

    @staticmethod
    def _area_with_border():
        inner_l = 2 * random.randint(3, 12)
        inner_w = 2 * random.randint(2, 10)
        border = random.randint(1, 8)
        outer_l, outer_w = inner_l + 2 * border, inner_w + 2 * border
        outer_area = outer_l * outer_w
        other_root = -Fraction(inner_l + inner_w, 2) - border
        facts = (f"A {inner_l} cm by {inner_w} cm picture has a uniform border. "
                 f"The outside rectangle has area {outer_area} cm².")
        question = "How wide is the border?"
        model = f"({inner_l} + 2x)({inner_w} + 2x) = {outer_area}"
        steps = [step("MODEL_EQ", model, "outside area"),
                 step("REWRITE", f"roots x = {border}, {other_root}"),
                 step("TRY", f"x = {other_root}"),
                 step("REJECT", f"x = {other_root}", "negative width"),
                 step("TRY", f"x = {border}"), step("ACCEPT", f"x = {border}"),
                 step("M", 2, border, 2 * border),
                 step("A", inner_l, 2 * border, outer_l),
                 step("A", inner_w, 2 * border, outer_w),
                 step("M", outer_l, outer_w, outer_area),
                 step("CHECK", "outside area", unit(outer_area, "cm²"))]
        answer = unit(border, "cm")
        used = [f"picture {inner_l} by {inner_w} cm", f"outside area {outer_area} cm²"]
        return facts, question, steps, answer, Fraction(border), model, used, lambda v: unit(v, "cm")

    @staticmethod
    def _revenue_linear_demand():
        slope = random.randint(2, 5)
        price = random.randint(4, 30)
        intercept = 2 * slope * price
        quantity = intercept - slope * price
        revenue = price * quantity
        facts = (f"At price p dollars, a seller can sell q = {intercept} − {slope}p items. "
                 "Revenue is the price times the number sold.")
        question = "What price gives the greatest revenue, and what is that revenue?"
        model = f"R = p({intercept} − {slope}p)"
        steps = [step("MODEL_EQ", f"q = {intercept} − {slope}p", "items sold"),
                 step("REVENUE", model),
                 step("REWRITE", f"R = −{slope}p² + {intercept}p"),
                 step("M", 2, -slope, -2 * slope),
                 step("D", -intercept, -2 * slope, price),
                 step("M", slope, price, slope * price),
                 step("S", intercept, slope * price, quantity),
                 step("M", price, quantity, revenue),
                 step("TRY", f"p = {price - 1}", (price - 1) * (intercept - slope * (price - 1))),
                 step("TRY", f"p = {price + 1}", (price + 1) * (intercept - slope * (price + 1))),
                 step("ACCEPT", f"p = {price}", revenue),
                 step("CHECK", "neighboring integer prices are lower", revenue)]
        answer = f"{money(price)}; revenue {money(revenue)}"
        used = [f"q = {intercept} − {slope}p", "revenue is price times quantity"]
        return facts, question, steps, answer, Fraction(revenue), model, used, money

    @staticmethod
    def _rectangle_from_area_perimeter():
        length = random.randint(8, 35)
        width = random.randint(2, length - 2)
        area, perimeter, half = length * width, 2 * (length + width), length + width
        facts = f"A rectangular lot has area {area} m² and perimeter {perimeter} m."
        question = "What are its dimensions?"
        model = f"x({half} − x) = {area}"
        steps = [step("D", perimeter, 2, half),
                 step("MODEL_EQ", model, "area with dimensions x and half-perimeter minus x"),
                 step("REWRITE", f"x² − {half}x + {area} = 0"),
                 step("ZERO_PRODUCT", f"(x − {length})(x − {width}) = 0"),
                 step("ACCEPT", f"x = {length}"), step("ACCEPT", f"x = {width}"),
                 step("A", length, width, half), step("M", length, width, area),
                 step("CHECK", f"2({length} + {width})", perimeter)]
        answer = f"{length} m by {width} m"
        used = [f"area {area} m²", f"perimeter {perimeter} m"]
        return facts, question, steps, answer, Fraction(area), model, used, lambda v: unit(v, "m²")

    @staticmethod
    def _consecutive_product():
        first = random.randint(2, 50)
        second, product = first + 1, first * (first + 1)
        negative = -first - 1
        facts = f"The product of two consecutive positive integers is {product}."
        question = "What are the two integers?"
        model = f"n(n + 1) = {product}"
        steps = [step("MODEL_EQ", model, "consecutive integers"),
                 step("REWRITE", f"n² + n − {product} = 0"),
                 step("ZERO_PRODUCT", f"(n − {first})(n + {second}) = 0"),
                 step("TRY", f"n = {negative}"),
                 step("REJECT", f"n = {negative}", "not positive"),
                 step("TRY", f"n = {first}"), step("ACCEPT", f"n = {first}"),
                 step("A", first, 1, second), step("M", first, second, product),
                 step("CHECK", "consecutive product", product)]
        answer = f"{first} and {second}"
        used = [f"product {product}", "consecutive positive integers"]
        return facts, question, steps, answer, Fraction(first), model, used, str

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
            extra = random.choice([value for value in range(401, 801) if value not in occupied])
            problem = f"An unrelated notice mentions {extra} storage bins. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} storage bins"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict a reasonable positive solution",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "quadratic model from the situation"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_quadratic_word_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
