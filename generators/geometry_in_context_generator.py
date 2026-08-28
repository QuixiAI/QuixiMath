"""Solve practical geometry from unstated structural cues.

Variants: ``fence_against_wall``, ``tiles_with_waste``, ``paint_coverage``,
``packaging_cost``, ``border_area``, ``ladder_or_shadow``, and
``garden_path``. Five shared-context renderings and all four applied
modifiers are supported. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``FENCE_SIDES``, ``AREA``, ``WASTE``,
``CEIL``, ``E``, ``ROOT``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, ``Z``.
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
VARIANTS = ("fence_against_wall", "tiles_with_waste", "paint_coverage",
            "packaging_cost", "border_area", "ladder_or_shadow",
            "garden_path")
FRAMES = (
    "At {place}, {name} plans a practical layout. {facts} {question}",
    "{question} A project given to {name} at {place} states: {facts}",
    "For {name} at {place}, the dimensions are described this way: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the layout from {place} that {name} is checking. {facts} {question}",
)
PLACES = tuple(setting for key in ("garden", "workshop", "business", "classroom")
               for setting in CONTEXTS[key].settings)
TRIPLES = ((3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17))


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class GeometryInContextGenerator(ProblemGenerator):
    """Solve seven practical geometry models without naming the method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _fence_against_wall():
        width, length = random.randint(3, 15), random.randint(8, 30)
        fence, area = 2 * width + length, width * length
        facts = (f"A rectangular garden uses a wall as one long side. The other "
                 f"three sides use {fence} m of fencing, and each short side is "
                 f"{width} m.")
        question = "What covered area does the garden have?"
        model = f"2 × {width} + L = {fence}; A = {width} × L"
        steps = [step("FENCE_SIDES", "two widths + one length",
                      f"2 × {width} + L = {fence}"),
                 step("M", 2, width, 2 * width),
                 step("S", fence, 2 * width, length),
                 step("AREA", f"{width} × {length}", area),
                 step("CHECK", "three fenced sides", fence)]
        return facts, question, steps, unit(area, "m²"), Fraction(area), model, [f"fence {fence} m", f"width {width} m"], lambda x: unit(x, "m²")

    @staticmethod
    def _tiles_with_waste():
        length, width = random.randint(3, 15), random.randint(3, 12)
        tile_area = random.choice((Fraction(1, 4), Fraction(1, 2), Fraction(1)))
        waste = random.choice((5, 10, 15, 20))
        area = length * width
        base_tiles = Fraction(area, 1) / tile_area
        with_waste = base_tiles * Fraction(100 + waste, 100)
        tiles = math.ceil(with_waste)
        facts = (f"A floor is {length} m by {width} m. Each tile covers "
                 f"{exact(tile_area)} m², and {waste}% extra tiles are allowed "
                 "for cuts and breakage.")
        question = "What whole number of tiles should be ordered?"
        model = f"tiles = ceil(({length} × {width})/{exact(tile_area)} × {100 + waste}/100)"
        steps = [step("M", length, width, area),
                 step("D", area, exact(tile_area), exact(base_tiles)),
                 step("M", exact(base_tiles), exact(Fraction(100 + waste, 100)), exact(with_waste)),
                 step("WASTE", f"{waste}%", f"{exact(base_tiles)} → {exact(with_waste)}", tiles),
                 step("CEIL", exact(with_waste), tiles),
                 step("CHECK", "whole tiles", tiles)]
        return facts, question, steps, unit(tiles, "tile"), Fraction(tiles), model, [f"floor {length} by {width} m", f"tile {exact(tile_area)} m²", f"waste {waste}%"], lambda x: unit(x, "tile")

    @staticmethod
    def _paint_coverage():
        length, height = random.randint(4, 15), random.randint(2, 6)
        coats = random.choice((1, 2, 3))
        coverage = random.choice((6, 8, 10, 12))
        area, coated = length * height, length * height * coats
        raw = Fraction(coated, coverage)
        cans = math.ceil(raw)
        facts = (f"A wall is {length} m long and {height} m high. It needs "
                 f"{coats} {'coat' if coats == 1 else 'coats'}, and one paint "
                 f"can covers {coverage} m².")
        question = "How many whole paint cans are needed?"
        model = f"cans = ceil({length} × {height} × {coats}/{coverage})"
        steps = [step("M", length, height, area), step("M", area, coats, coated),
                 step("D", coated, coverage, exact(raw)), step("CEIL", exact(raw), cans),
                 step("CHECK", "whole cans", cans)]
        return facts, question, steps, unit(cans, "can"), Fraction(cans), model, [f"wall {length} by {height} m", f"coats {coats}", f"coverage {coverage} m²"], lambda x: unit(x, "can")

    @staticmethod
    def _packaging_cost():
        length, width, height = random.randint(10, 40), random.randint(6, 25), random.randint(4, 20)
        cents = random.choice((1, 2, 3, 4, 5))
        lw, lh, wh = length * width, length * height, width * height
        pair_sum, surface = lw + lh + wh, 2 * (lw + lh + wh)
        cost = Fraction(surface * cents, 100)
        facts = (f"A closed rectangular package is {length} cm by {width} cm by "
                 f"{height} cm. Covering material costs ${cents / 100:.2f} per cm².")
        question = "What does the material for all six faces cost?"
        model = f"cost = 2({length}×{width}+{length}×{height}+{width}×{height}) × {cents}/100"
        steps = [step("M", length, width, lw), step("M", length, height, lh),
                 step("M", width, height, wh), step("A", lw, lh, lw + lh),
                 step("A", lw + lh, wh, pair_sum), step("M", 2, pair_sum, surface),
                 step("M", surface, exact(Fraction(cents, 100)), exact(cost)),
                 step("CHECK", "six faces", surface)]
        return facts, question, steps, money(cost), cost, model, [f"dimensions {length}, {width}, {height} cm", f"cost ${cents / 100:.2f}/cm²"], money

    @staticmethod
    def _border_area():
        inner_l, inner_w = random.randint(6, 24), random.randint(4, 18)
        border = random.randint(1, 5)
        outer_l, outer_w = inner_l + 2 * border, inner_w + 2 * border
        inner, outer = inner_l * inner_w, outer_l * outer_w
        area = outer - inner
        facts = (f"A rectangular picture is {inner_l} cm by {inner_w} cm and has "
                 f"a uniform {border} cm frame around every edge.")
        question = "What area is occupied by the frame alone?"
        model = f"frame = ({outer_l} × {outer_w}) − ({inner_l} × {inner_w})"
        steps = [step("M", 2, border, 2 * border), step("A", inner_l, 2 * border, outer_l),
                 step("A", inner_w, 2 * border, outer_w), step("AREA", f"{outer_l} × {outer_w}", outer),
                 step("AREA", f"{inner_l} × {inner_w}", inner), step("S", outer, inner, area)]
        return facts, question, steps, unit(area, "cm²"), Fraction(area), model, [f"picture {inner_l} by {inner_w} cm", f"frame {border} cm"], lambda x: unit(x, "cm²")

    @staticmethod
    def _ladder_or_shadow():
        ladder = random.choice((True, False))
        if ladder:
            base, height, length = random.choice(TRIPLES)
            facts = (f"A ladder reaches {height} m up a wall while its foot is "
                     f"{base} m from the wall; the wall and ground meet at a right angle.")
            question = "How long is the ladder?"
            model = f"L² = {base}² + {height}²"
            steps = [step("E", base, 2, base ** 2), step("E", height, 2, height ** 2),
                     step("A", base ** 2, height ** 2, length ** 2), step("ROOT", length ** 2, length)]
            used, category = [f"base {base} m", f"height {height} m"], "ladder"
        else:
            object_height = random.randint(2, 12)
            object_shadow = random.randint(2, 10)
            scale = random.randint(2, 8)
            shadow, length = object_shadow * scale, object_height * scale
            facts = (f"At the same moment, a {object_height} m post casts a "
                     f"{object_shadow} m shadow, while a tree casts a {shadow} m shadow.")
            question = "How tall is the tree?"
            model = f"h/{shadow} = {object_height}/{object_shadow}"
            steps = [step("D", shadow, object_shadow, scale), step("M", object_height, scale, length)]
            used, category = [f"post {object_height} m", f"shadows {object_shadow}, {shadow} m"], "shadow"
        steps.append(step("CHECK", category, unit(length, "m")))
        return facts, question, steps, unit(length, "m"), Fraction(length), model, used, lambda x: unit(x, "m")

    @staticmethod
    def _garden_path():
        length, width, path = random.randint(8, 30), random.randint(6, 20), random.randint(1, 4)
        outer_l, outer_w = length + 2 * path, width + 2 * path
        garden, outer, area = length * width, outer_l * outer_w, outer_l * outer_w - length * width
        facts = (f"A {length} m by {width} m garden has a {path} m wide path "
                 "running outside all four edges.")
        question = "What area does the path cover?"
        model = f"path = ({outer_l} × {outer_w}) − ({length} × {width})"
        steps = [step("M", 2, path, 2 * path), step("A", length, 2 * path, outer_l),
                 step("A", width, 2 * path, outer_w), step("AREA", f"{outer_l} × {outer_w}", outer),
                 step("AREA", f"{length} × {width}", garden), step("S", outer, garden, area)]
        return facts, question, steps, unit(area, "m²"), Fraction(area), model, [f"garden {length} by {width} m", f"path {path} m"], lambda x: unit(x, "m²")

    @classmethod
    def _case(cls, variant): return getattr(cls, f"_{variant}")()

    def generate(self):
        variant, modifier = self.variant or random.choice(self.VARIANTS), self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(x) for x in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(191, 491) if n not in occupied])
            problem = f"A nearby sign lists {extra} reserved spaces. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} reserved spaces"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the geometric scale before computing",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "geometry from the situation"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"applied_geometry_in_context_{variant}_{modifier}", "problem": problem, "steps": steps, "final_answer": answer}
