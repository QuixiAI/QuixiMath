"""Exact proportional stories across rates, scales, recipes, and shadows.

Variants: ``speed``, ``recipe``, ``cost``, ``ratio_table``,
``scale_drawing``, ``map_scale``, ``recipe_scaling``,
``shadow_similar_triangles``, and ``speed_from_map``. Each has five phrasings
through shared contexts and supports all four applied modifiers. The
historical ``distractor=True`` constructor remains supported. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``PROP_SETUP``, ``EQ_SETUP``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("speed", "recipe", "cost", "ratio_table", "scale_drawing",
            "map_scale", "recipe_scaling", "shadow_similar_triangles",
            "speed_from_map")
PHRASINGS = {
    "speed": (
        "A car travels {k1} miles in {k2} hours. How far will it travel in {q} hours?",
        "A car covers {k1} miles during {k2} hours at a steady pace. What distance does it cover in {q} hours?",
        "In {k2} hours, a van travels {k1} miles. How many miles does it travel in {q} hours at the same pace?",
        "A {k1}-mile trip takes {k2} hours. What distance takes {q} hours at that pace?",
        "A driver logs {k1} miles over {k2} hours and continues steadily. What is the distance after {q} hours?",
    ),
    "recipe": (
        "A recipe uses {k1} cups of flour for {k2} servings. How many cups are needed for {q} servings?",
        "Making {k2} servings needs {k1} cups of flour. What amount is needed for {q} servings?",
        "For {k2} servings, a cook measures {k1} cups of flour. How many cups go into {q} servings?",
        "A {k2}-serving batch contains {k1} cups of flour. What does a {q}-serving batch contain?",
        "The flour amount is {k1} cups when the yield is {k2} servings. What is it for {q} servings?",
    ),
    "cost": (
        "If {k2} pounds of apples cost ${k1}.00, how much do {q} pounds cost?",
        "A shopper pays ${k1}.00 for {k2} pounds of apples. What is the cost of {q} pounds?",
        "The price for {k2} pounds of apples is ${k1}.00. How much are {q} pounds?",
        "A {k2}-pound bag of apples costs ${k1}.00. What would {q} pounds cost at that pace?",
        "Apples total ${k1}.00 for {k2} pounds. Find the total for {q} pounds.",
    ),
    "ratio_table": (
        "A data table pairs input {k2} units with output {k1} units. What output goes with input {q} units?",
        "An input of {k2} units maps to {k1} output units. What maps from {q} input units?",
        "The table shows {k2} input units and {k1} output units together. What output matches {q} input units?",
        "When the input is {k2} units, the output is {k1} units. What is the output for {q} input units?",
        "A machine turns {k2} input units into {k1} output units. How many output units come from {q} input units?",
    ),
    "scale_drawing": (
        "On a building drawing, 1 cm represents {factor} m. A wall measures {q} cm on the drawing. How long is the wall?",
        "A drawing shows each centimetre as {factor} m. What real length is shown by {q} cm?",
        "One centimetre in a plan corresponds to {factor} m. How many metres correspond to {q} cm?",
        "A {q} cm line represents a wall when every centimetre stands for {factor} m. What is the wall's length?",
        "The plan labels 1 cm as {factor} m, and a room edge spans {q} cm. What is its actual length?",
    ),
    "map_scale": (
        "On a map, 1 cm represents {factor} km. A route measures {q} cm. How long is the route?",
        "Each centimetre on a map stands for {factor} km. What distance is shown by {q} cm?",
        "A map key pairs 1 cm with {factor} km. How many kilometres does {q} cm represent?",
        "A route is {q} cm on a map where each centimetre means {factor} km. What is the real distance?",
        "The map marks 1 cm as {factor} km, and a trail spans {q} cm. How long is the trail?",
    ),
    "recipe_scaling": (
        "One batch uses {amount} cup of oil. How many cups are needed for {q} batches?",
        "A cook needs {amount} cup of oil per batch. What amount is needed for {q} batches?",
        "Each batch contains {amount} cup of oil. How many cups go into {q} batches?",
        "Oil is measured at {amount} cup for one batch. What is the amount for {q} batches?",
        "The single-batch oil amount is {amount} cup. Find the oil for {q} batches.",
    ),
    "shadow_similar_triangles": (
        "A {height} m pole casts a {shadow} m shadow. At the same time, a tree casts a {q} m shadow. How tall is the tree?",
        "A pole {height} m tall has a {shadow} m shadow while a tree's shadow is {q} m. What is the tree's height?",
        "A {shadow} m shadow belongs to a {height} m pole. Nearby, a tree's shadow is {q} m. How tall is the tree?",
        "At one moment, a {height} m marker has a {shadow} m shadow and a tree has a {q} m shadow. Find the tree height.",
        "The sun gives a {height} m pole a {shadow} m shadow. A tree's shadow then measures {q} m. What height is the tree?",
    ),
    "speed_from_map": (
        "On a map, 1 cm represents {factor} km. A trip measures {draw} cm and takes {hours} hours. What is the average speed?",
        "A {draw} cm route uses a map key of 1 cm to {factor} km. The trip lasts {hours} hours. What is the average speed?",
        "Each map centimetre means {factor} km; a journey spans {draw} cm in {hours} hours. What is its average speed?",
        "A map route is {draw} cm where 1 cm stands for {factor} km. Travel time is {hours} hours. What speed is averaged?",
        "The map marks 1 cm as {factor} km. A {draw} cm trip takes {hours} hours. What is the trip's average speed?",
    ),
}
PLACE_KEYS = {
    "speed": ("trip",),
    "recipe": ("recipe",),
    "cost": ("shop",),
    "ratio_table": ("classroom", "workshop"),
    "scale_drawing": ("classroom", "workshop"),
    "map_scale": ("trip", "classroom"),
    "recipe_scaling": ("recipe",),
    "shadow_similar_triangles": ("garden", "sports"),
    "speed_from_map": ("trip", "classroom"),
}


def _at_place(text, variant):
    places = tuple(
        setting
        for key in PLACE_KEYS[variant]
        for setting in CONTEXTS[key].settings
    )
    return (f"At {random.choice(places)}, {random.choice(NAMES)} records this: "
            f"{text}")


class ProportionWordProblemGenerator(ProblemGenerator):
    """Generate exact proportional applications with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = ("mi", "cups", "$", "units", "m", "km", "km/h")

    def __init__(self, distractor=False, modifier=None, variant=None):
        if modifier is None:
            modifier = "distractor" if distractor else "plain"
        elif distractor and modifier != "distractor":
            raise ValueError("distractor=True requires modifier='distractor'")
        if modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS}")
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.modifier = modifier
        self.variant = variant
        self.distractor = modifier == "distractor"

    @staticmethod
    def _classic(kind):
        rate = random.randint(1, 12)
        k2 = random.randint(2, 6)
        k1 = rate * k2
        q = random.choice([value for value in range(2, 16) if value != k2])
        answer_value = rate * q
        problem = random.choice(PHRASINGS[kind]).format(k1=k1, k2=k2, q=q)
        model = f"{k1}/{k2} = x/{q}"
        cross = k1 * q
        steps = [step("PROP_SETUP", model),
                 step("M", k1, q, cross),
                 step("EQ_SETUP", f"x = {cross}/{k2}"),
                 step("D", cross, k2, answer_value),
                 step("CHECK", "constant ratio", exact(Fraction(k1, k2)))]
        if kind == "cost":
            answer, renderer = money(answer_value), money
        elif kind == "speed":
            answer = f"{exact(answer_value)} mi"
            renderer = lambda value: f"{exact(value)} mi"
        elif kind == "recipe":
            answer = unit(answer_value, "cup")
            renderer = lambda value: unit(value, "cup")
        else:
            answer = unit(answer_value, "output unit")
            renderer = lambda value: unit(value, "output unit")
        used = [f"known pair {k1} to {k2}", f"query {q}"]
        return problem, steps, answer, Fraction(answer_value), model, used, renderer

    @staticmethod
    def _scale(kind):
        factor = random.randint(2, 30 if kind == "map_scale" else 15)
        q = random.randint(2, 20)
        answer_value = factor * q
        problem = random.choice(PHRASINGS[kind]).format(factor=factor, q=q)
        model = f"1/{factor} = {q}/x"
        steps = [step("PROP_SETUP", model),
                 step("M", factor, q, answer_value),
                 step("EQ_SETUP", f"x = {factor}*{q}"),
                 step("D", answer_value, 1, answer_value),
                 step("CHECK", "drawing length times key", answer_value)]
        unit_name = "km" if kind == "map_scale" else "m"
        answer = unit(answer_value, unit_name)
        used = [f"1 cm represents {factor} {unit_name}", f"drawing {q} cm"]
        renderer = lambda value: unit(value, unit_name)
        return problem, steps, answer, Fraction(answer_value), model, used, renderer

    @staticmethod
    def _recipe_scaling():
        denominator = random.choice((2, 3, 4, 5))
        numerator = random.randint(1, denominator - 1)
        amount = Fraction(numerator, denominator)
        q = random.randint(2, 12)
        answer_value = amount * q
        problem = random.choice(PHRASINGS["recipe_scaling"]).format(
            amount=exact(amount), q=q)
        model = f"{exact(amount)}/1 = x/{q}"
        cross = numerator * q
        steps = [step("PROP_SETUP", model),
                 step("M", numerator, q, cross),
                 step("EQ_SETUP", f"x = {cross}/{denominator}"),
                 step("D", cross, denominator, exact(answer_value)),
                 step("CHECK", "per-batch amount times batches", exact(answer_value))]
        answer = unit(answer_value, "cup")
        used = [f"{exact(amount)} cup per batch", f"{q} batches"]
        return (problem, steps, answer, answer_value, model, used,
                lambda value: unit(value, "cup"))

    @staticmethod
    def _shadow():
        ratio = random.randint(1, 5)
        shadow = random.randint(1, 6)
        height = ratio * shadow
        q = random.randint(2, 15)
        answer_value = ratio * q
        problem = random.choice(PHRASINGS["shadow_similar_triangles"]).format(
            height=height, shadow=shadow, q=q)
        model = f"{height}/{shadow} = x/{q}"
        cross = height * q
        steps = [step("PROP_SETUP", model),
                 step("M", height, q, cross),
                 step("EQ_SETUP", f"x = {cross}/{shadow}"),
                 step("D", cross, shadow, answer_value),
                 step("CHECK", "height-to-shadow ratio", ratio)]
        answer = unit(answer_value, "m")
        used = [f"pole {height} m", f"pole shadow {shadow} m",
                f"tree shadow {q} m"]
        return (problem, steps, answer, Fraction(answer_value), model, used,
                lambda value: unit(value, "m"))

    @staticmethod
    def _speed_from_map():
        while True:
            factor = random.randint(2, 20)
            draw = random.randint(2, 15)
            hours = random.randint(2, 6)
            distance_value = factor * draw
            answer_value = Fraction(distance_value, hours)
            if answer_value.denominator in (1, 2):
                break
        problem = random.choice(PHRASINGS["speed_from_map"]).format(
            factor=factor, draw=draw, hours=hours)
        model = f"x = {factor}*{draw}/{hours}"
        steps = [step("M", factor, draw, distance_value),
                 step("D", distance_value, hours, exact(answer_value)),
                 step("CHECK", "map distance over travel time",
                      unit(answer_value, "km/h"))]
        answer = unit(answer_value, "km/h")
        used = [f"1 cm represents {factor} km", f"route {draw} cm",
                f"time {hours} hours"]
        return (problem, steps, answer, answer_value, model, used,
                lambda value: unit(value, "km/h"))

    @classmethod
    def _case(cls, variant):
        if variant in ("speed", "recipe", "cost", "ratio_table"):
            return cls._classic(variant)
        if variant in ("scale_drawing", "map_scale"):
            return cls._scale(variant)
        if variant == "recipe_scaling":
            return cls._recipe_scaling()
        if variant == "shadow_similar_triangles":
            return cls._shadow()
        return cls._speed_from_map()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        problem, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _at_place(problem, variant)
        if self.modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([value for value in range(41, 100)
                                   if value not in occupied])
            problem = f"A notice nearby lists {extra} lockers. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} lockers"))
        elif self.modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "round the known pair before scaling", render=renderer)[:-1]
        elif self.modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "constant relationship"))
            answer = f"{model}; x = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_proportion_word_{variant}_{self.modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
