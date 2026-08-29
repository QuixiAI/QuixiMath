"""How many rectangular/circular pieces fit, and what orientation wins.

Variants: ``boxes_in_box_orientation``, ``tiles_with_grout``, ``cans_in_case``,
``wrapping_paper_overlap``, ``leftover_material``, ``shelves_from_board``.
Five context frames and all four applied modifiers are supported. Every fit
count comes from an integer floor division; orientation ties are excluded by
construction. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``,
``MODEL_EQ``, ``FIT``, ``TRY``, ``REJECT``, ``ORIENT``, ``AREA``,
``EXTRA_MATERIAL``, ``A``, ``S``, ``M``, ``D``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, dec, estimate_first, exact,
                            reject_step, select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("boxes_in_box_orientation", "tiles_with_grout", "cans_in_case",
            "wrapping_paper_overlap", "leftover_material", "shelves_from_board")
FRAMES = (
    "At {place}, {name} works out the following packing problem. {facts} {question}",
    "{question} A task for {name} at {place} states: {facts}",
    "For {name}'s project at {place}: {facts} {question}",
    "A note from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the packing job {name} is doing at {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("workshop", "business", "garden", "shop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class SpatialPackingGenerator(ProblemGenerator):
    """Generate six exact packing/fit models without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _boxes_in_box_orientation():
        for _ in range(300):
            L, W, H = (5 * random.randint(6, 20) for _ in range(3))
            l, w, h = (5 * random.randint(1, 6) for _ in range(3))
            upright = (L // l) * (W // w) * (H // h)
            on_side = (L // l) * (W // h) * (H // w)
            if upright != on_side:
                break
        else:
            raise AssertionError("no non-tied orientation found")
        if upright > on_side:
            best, wl, ww, wh, label = upright, L // l, W // w, H // h, "upright"
            other = on_side
        else:
            best, wl, ww, wh, label = on_side, L // l, W // h, H // w, "on their side"
            other = upright
        facts = (f"A box measures {L} cm × {W} cm × {H} cm. Cartons "
                 f"measuring {l} cm × {w} cm × {h} cm need to be packed "
                 "inside, all the same way up.")
        question = "How many cartons fit?"
        model = "count = floor(L/l) × floor(W/w) × floor(H/h), best orientation"
        steps = [step("FIT", "upright", f"floor({L}/{l})·floor({W}/{w})·floor({H}/{h})", upright),
                step("TRY", "cartons on their side", f"floor({L}/{l})·floor({W}/{h})·floor({H}/{w})", on_side),
                reject_step(f"{other} cartons", f"{other} < {best}"),
                step("ORIENT", label, best)]
        answer = f"{best} cartons ({wl} × {ww} × {wh})"
        used = [f"box {L}×{W}×{H} cm", f"carton {l}×{w}×{h} cm"]
        return facts, question, steps, answer, Fraction(best), model, used, str

    @staticmethod
    def _tiles_with_grout():
        L, W = 10 * random.randint(15, 40), 10 * random.randint(15, 40)
        t = random.choice((20, 25, 30, 40, 50))
        g_mm = random.choice((2, 3, 4, 5))
        g = Fraction(g_mm, 10)
        n_l = (L + g) // (t + g)
        n_w = (W + g) // (t + g)
        total = n_l * n_w
        facts = (f"A floor is {L} cm by {W} cm. Square tiles {t} cm across "
                 f"are laid with a {g_mm} mm grout line between each tile.")
        question = "How many whole tiles fit along each side, and how many tiles in total?"
        model = "tiles per side = floor((length + grout)/(tile + grout))"
        steps = [step("FIT", "length", f"floor(({L}+{dec(g)})/({t}+{dec(g)}))", n_l),
                step("FIT", "width", f"floor(({W}+{dec(g)})/({t}+{dec(g)}))", n_w),
                step("M", n_l, n_w, total)]
        answer = f"{n_l} × {n_w} = {total} tiles"
        used = [f"floor {L}×{W} cm", f"tile {t} cm", f"grout {g_mm} mm"]
        return facts, question, steps, answer, Fraction(total), model, used, str

    @staticmethod
    def _cans_in_case():
        L, W, H = 10 * random.randint(4, 12), 10 * random.randint(4, 12), 10 * random.randint(2, 8)
        d = random.choice((5, 6, 7, 8, 9, 10))
        h = random.choice((8, 10, 12, 15))
        n_l, n_w, layers = L // d, W // d, H // h
        total = n_l * n_w * layers
        facts = (f"A case measures {L} cm × {W} cm × {H} cm inside. Cans "
                 f"are {d} cm in diameter and {h} cm tall, standing upright.")
        question = "How many cans fit inside the case?"
        model = "count = floor(L/d) × floor(W/d) × floor(H/h)"
        steps = [step("FIT", "length", f"floor({L}/{d})", n_l),
                step("FIT", "width", f"floor({W}/{d})", n_w),
                step("FIT", "height", f"floor({H}/{h})", layers),
                step("M", f"{n_l}·{n_w}·{layers}", total)]
        answer = f"{total} cans ({n_l} × {n_w} × {layers})"
        used = [f"case {L}×{W}×{H} cm", f"can {d} cm across, {h} cm tall"]
        return facts, question, steps, answer, Fraction(total), model, used, str

    @staticmethod
    def _wrapping_paper_overlap():
        L, W, H = (5 * random.randint(4, 20) for _ in range(3))
        pct = random.choice((10, 20, 25, 50))
        surface = 2 * (L * W + L * H + W * H)
        with_overlap = Fraction(surface * (100 + pct), 100)
        facts = (f"A gift box is {L} cm × {W} cm × {H} cm. Wrapping paper "
                 f"must cover the full surface area plus {pct}% extra for "
                 "overlaps and folds.")
        question = "How much paper is needed?"
        model = "paper = surface area × (100 + extra%)/100"
        steps = [step("AREA", f"2×({L}×{W}+{L}×{H}+{W}×{H})", surface),
                step("EXTRA_MATERIAL", f"{pct}%", surface, exact(with_overlap))]
        answer = f"{exact(with_overlap)} cm²"
        used = [f"box {L}×{W}×{H} cm", f"extra {pct}%"]
        return facts, question, steps, answer, with_overlap, model, used, exact

    @staticmethod
    def _leftover_material():
        L, W = 5 * random.randint(10, 40), 5 * random.randint(10, 40)
        for _ in range(200):
            l, w = 5 * random.randint(1, 8), 5 * random.randint(1, 8)
            n_l, n_w = L // l, W // w
            if n_l > 0 and n_w > 0:
                break
        else:
            raise AssertionError("no piece size fits")
        pieces = n_l * n_w
        used_area = pieces * l * w
        leftover = L * W - used_area
        facts = (f"A sheet of material measures {L} cm × {W} cm. "
                 f"Rectangular pieces measuring {l} cm × {w} cm are cut "
                 "from it in a grid, without rotating any piece.")
        question = "How many pieces fit, and how much material area is left over?"
        model = "pieces = floor(L/l) × floor(W/w); leftover = sheet area − used area"
        steps = [step("FIT", "length", f"floor({L}/{l})", n_l),
                step("FIT", "width", f"floor({W}/{w})", n_w),
                step("M", n_l, n_w, pieces),
                step("AREA", f"{L}×{W}", L * W),
                step("AREA", f"{pieces}×{l}×{w}", used_area),
                step("S", L * W, used_area, leftover)]
        answer = f"{pieces} pieces; {leftover} cm² left over"
        used = [f"sheet {L}×{W} cm", f"piece {l}×{w} cm"]
        return facts, question, steps, answer, Fraction(leftover), model, used, str

    @staticmethod
    def _shelves_from_board():
        L = 5 * random.randint(30, 100)
        s = random.choice((30, 40, 45, 50, 60, 75))
        k_mm = random.choice((2, 3, 4, 5))
        k = Fraction(k_mm, 10)
        n = (L + k) // (s + k)
        facts = (f"A board is {L} cm long. Shelves {s} cm long are cut from "
                 f"it, and each cut removes {k_mm} mm of material as sawdust.")
        question = "How many whole shelves can be cut?"
        model = "count = floor((length + kerf)/(shelf + kerf))"
        steps = [step("FIT", "shelves", f"floor(({L}+{dec(k)})/({s}+{dec(k)}))", n)]
        answer = f"{n} shelves"
        used = [f"board {L} cm", f"shelf {s} cm", f"kerf {k_mm} mm"]
        return facts, question, steps, answer, Fraction(n), model, used, str

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
            extra = random.choice([n for n in range(401, 701) if n not in occupied])
            problem = f"A nearby rack holds {extra} unrelated items. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} unrelated items"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the fitting count",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "packing relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_spatial_packing_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
