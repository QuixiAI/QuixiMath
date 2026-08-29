"""Problem-text-only brute-force oracles for SpatialPackingGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.spatial_packing_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, SpatialPackingGenerator,
)
from helpers import DELIM

MODELS = {
    "boxes_in_box_orientation": "count = floor(L/l) × floor(W/w) × floor(H/h), best orientation",
    "tiles_with_grout": "tiles per side = floor((length + grout)/(tile + grout))",
    "cans_in_case": "count = floor(L/d) × floor(W/d) × floor(H/h)",
    "wrapping_paper_overlap": "paper = surface area × (100 + extra%)/100",
    "leftover_material": "pieces = floor(L/l) × floor(W/w); leftover = sheet area − used area",
    "shelves_from_board": "count = floor((length + kerf)/(shelf + kerf))",
}


def exact(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        return str(value)
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def clean(problem):
    return re.sub(r"^A nearby rack holds \d+ unrelated items\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"box measures (\d+) cm × (\d+) cm × (\d+) cm\. Cartons measuring "
        r"(\d+) cm × (\d+) cm × (\d+) cm need to be packed inside", text)
    if match:
        L, W, H, l, w, h = map(int, match.groups())
        upright = (L // l) * (W // w) * (H // h)
        on_side = (L // l) * (W // h) * (H // w)
        assert upright != on_side, text
        if upright > on_side:
            best, wl, ww, wh = upright, L // l, W // w, H // h
        else:
            best, wl, ww, wh = on_side, L // l, W // h, H // w
        return "boxes_in_box_orientation", f"{best} cartons ({wl} × {ww} × {wh})"

    match = re.search(
        r"floor is (\d+) cm by (\d+) cm\. Square tiles (\d+) cm across are "
        r"laid with a (\d+) mm grout line", text)
    if match:
        L, W, t, g_mm = map(int, match.groups())
        g = Fraction(g_mm, 10)
        n_l, n_w = (L + g) // (t + g), (W + g) // (t + g)
        return "tiles_with_grout", f"{n_l} × {n_w} = {n_l * n_w} tiles"

    match = re.search(
        r"case measures (\d+) cm × (\d+) cm × (\d+) cm inside\. Cans are "
        r"(\d+) cm in diameter and (\d+) cm tall", text)
    if match:
        L, W, H, d, h = map(int, match.groups())
        n_l, n_w, layers = L // d, W // d, H // h
        return ("cans_in_case",
                f"{n_l * n_w * layers} cans ({n_l} × {n_w} × {layers})")

    match = re.search(
        r"gift box is (\d+) cm × (\d+) cm × (\d+) cm\. Wrapping paper must "
        r"cover the full surface area plus (\d+)% extra", text)
    if match:
        L, W, H, pct = map(int, match.groups())
        surface = 2 * (L * W + L * H + W * H)
        with_overlap = Fraction(surface * (100 + pct), 100)
        return "wrapping_paper_overlap", f"{exact(with_overlap)} cm²"

    match = re.search(
        r"sheet of material measures (\d+) cm × (\d+) cm\. Rectangular "
        r"pieces measuring (\d+) cm × (\d+) cm are cut from it in a grid, "
        r"without rotating", text)
    if match:
        L, W, l, w = map(int, match.groups())
        n_l, n_w = L // l, W // w
        pieces = n_l * n_w
        leftover = L * W - pieces * l * w
        return "leftover_material", f"{pieces} pieces; {leftover} cm² left over"

    match = re.search(
        r"board is (\d+) cm long\. Shelves (\d+) cm long are cut from it, "
        r"and each cut removes (\d+) mm of material as sawdust", text)
    if match:
        L, s, k_mm = map(int, match.groups())
        k = Fraction(k_mm, 10)
        n = (L + k) // (s + k)
        return "shelves_from_board", f"{n} shelves"

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer)


class TestSpatialPackingGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(420)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = SpatialPackingGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], MODELS[variant])
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_example(self):
        self.assertEqual(
            solve("A box measures 60 cm × 40 cm × 30 cm. Cartons measuring "
                  "20 cm × 20 cm × 15 cm need to be packed inside, all the "
                  "same way up. How many cartons fit?"),
            ("boxes_in_box_orientation", "12 cartons (3 × 2 × 2)"))

    def test_orientation_never_ties(self):
        random.seed(421)
        for _ in range(300):
            result = SpatialPackingGenerator("boxes_in_box_orientation").generate()
            fields = {raw.split(DELIM)[0]: raw.split(DELIM) for raw in result["steps"]}
            upright, on_side = int(fields["FIT"][-1]), int(fields["TRY"][-1])
            self.assertNotEqual(upright, on_side, result["problem"])
            self.assertEqual(int(fields["ORIENT"][-1]), max(upright, on_side))

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "boxes_in_box_orientation": (
                "A box measures 60 cm × 40 cm × 30 cm. Cartons measuring "
                "20 cm × 20 cm × 15 cm need to be packed inside, all the "
                "same way up.",
                "How many cartons fit?"),
            "tiles_with_grout": (
                "A floor is 300 cm by 400 cm. Square tiles 30 cm across "
                "are laid with a 5 mm grout line between each tile.",
                "How many whole tiles fit along each side, and how many "
                "tiles in total?"),
            "cans_in_case": (
                "A case measures 60 cm × 40 cm × 30 cm inside. Cans are "
                "8 cm in diameter and 10 cm tall, standing upright.",
                "How many cans fit inside the case?"),
            "wrapping_paper_overlap": (
                "A gift box is 30 cm × 20 cm × 10 cm. Wrapping paper must "
                "cover the full surface area plus 20% extra for overlaps "
                "and folds.",
                "How much paper is needed?"),
            "leftover_material": (
                "A sheet of material measures 100 cm × 150 cm. Rectangular "
                "pieces measuring 20 cm × 25 cm are cut from it in a grid, "
                "without rotating any piece.",
                "How many pieces fit, and how much material area is left over?"),
            "shelves_from_board": (
                "A board is 300 cm long. Shelves 40 cm long are cut from "
                "it, and each cut removes 3 mm of material as sawdust.",
                "How many whole shelves can be cut?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(422)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SpatialPackingGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_spatial_packing_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SpatialPackingGenerator("bogus")
        with self.assertRaises(ValueError):
            SpatialPackingGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(423)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = SpatialPackingGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = SpatialPackingGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
