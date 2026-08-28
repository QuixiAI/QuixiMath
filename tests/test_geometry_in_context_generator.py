"""Problem-text-only oracles for GeometryInContextGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.geometry_in_context_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, GeometryInContextGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    scaled, places = value, 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + rendered


def quantity(value, unit_name):
    text = exact_text(value)
    if unit_name in {"m", "m²", "cm²"}:
        return f"{text} {unit_name}"
    return f"{text} {unit_name}" if Fraction(value) == 1 else f"{text} {unit_name}s"


def money(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^A nearby sign lists \d+ reserved spaces\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"three sides use (\d+) m of fencing, and each short side is (\d+) m",
        text, re.I)
    if match:
        fence, width = map(int, match.groups())
        length = fence - 2 * width
        area = width * length
        model = f"2 × {width} + L = {fence}; A = {width} × L"
        return "fence_against_wall", quantity(area, "m²"), model, Fraction(area), "fence"

    match = re.search(
        r"floor is (\d+) m by (\d+) m\. Each tile covers ([0-9./]+) m², "
        r"and (\d+)% extra tiles", text, re.I)
    if match:
        length, width = map(int, match.groups()[:2])
        tile_area, waste = number(match.group(3)), int(match.group(4))
        raw = Fraction(length * width, 1) / tile_area * Fraction(100 + waste, 100)
        count = math.ceil(raw)
        model = (f"tiles = ceil(({length} × {width})/{exact_text(tile_area)} × "
                 f"{100 + waste}/100)")
        return "tiles_with_waste", quantity(count, "tile"), model, Fraction(count), "tiles"

    match = re.search(
        r"wall is (\d+) m long and (\d+) m high\. It needs (\d+) coats?, "
        r"and one paint can covers (\d+) m²", text, re.I)
    if match:
        length, height, coats, coverage = map(int, match.groups())
        count = math.ceil(Fraction(length * height * coats, coverage))
        model = f"cans = ceil({length} × {height} × {coats}/{coverage})"
        return "paint_coverage", quantity(count, "can"), model, Fraction(count), "paint"

    match = re.search(
        r"closed rectangular package is (\d+) cm by (\d+) cm by (\d+) cm\. "
        r"Covering material costs \$([0-9.]+) per cm²", text, re.I)
    if match:
        length, width, height = map(int, match.groups()[:3])
        rate = number(match.group(4))
        surface = 2 * (length * width + length * height + width * height)
        cost = surface * rate
        cents = int(rate * 100)
        model = (f"cost = 2({length}×{width}+{length}×{height}+{width}×{height}) "
                 f"× {cents}/100")
        return "packaging_cost", money(cost), model, cost, "package"

    match = re.search(
        r"picture is (\d+) cm by (\d+) cm and has a uniform (\d+) cm frame",
        text, re.I)
    if match:
        length, width, border = map(int, match.groups())
        outer_l, outer_w = length + 2 * border, width + 2 * border
        area = outer_l * outer_w - length * width
        model = f"frame = ({outer_l} × {outer_w}) − ({length} × {width})"
        return "border_area", quantity(area, "cm²"), model, Fraction(area), "border"

    match = re.search(
        r"ladder reaches (\d+) m up a wall while its foot is (\d+) m from",
        text, re.I)
    if match:
        height, base = map(int, match.groups())
        length = math.isqrt(base * base + height * height)
        model = f"L² = {base}² + {height}²"
        return "ladder_or_shadow", quantity(length, "m"), model, Fraction(length), "ladder"

    match = re.search(
        r"a (\d+) m post casts a (\d+) m shadow, while a tree casts a (\d+) m shadow",
        text, re.I)
    if match:
        post, post_shadow, tree_shadow = map(int, match.groups())
        height = Fraction(post * tree_shadow, post_shadow)
        model = f"h/{tree_shadow} = {post}/{post_shadow}"
        return "ladder_or_shadow", quantity(height, "m"), model, height, "shadow"

    match = re.search(
        r"A (\d+) m by (\d+) m garden has a (\d+) m wide path", text, re.I)
    if match:
        length, width, path = map(int, match.groups())
        outer_l, outer_w = length + 2 * path, width + 2 * path
        area = outer_l * outer_w - length * width
        model = f"path = ({outer_l} × {outer_w}) − ({length} × {width})"
        return "garden_path", quantity(area, "m²"), model, Fraction(area), "path"

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestGeometryInContextGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(320)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(20):
                    result = GeometryInContextGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model, _, category = expected(
                        result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier, category))
        self.assertEqual({(v, m) for v, m, _ in seen},
                         {(v, m) for v in VARIANTS for m in MODIFIERS})
        ladder_kinds = {category for variant, _, category in seen
                        if variant == "ladder_or_shadow"}
        self.assertEqual(ladder_kinds, {"ladder", "shadow"})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "fence_against_wall": (
                "A rectangular garden uses a wall as one long side. The other "
                "three sides use 30 m of fencing, and each short side is 8 m.",
                "What covered area does the garden have?"),
            "tiles_with_waste": (
                "A floor is 4 m by 3 m. Each tile covers 0.25 m², and 10% extra "
                "tiles are allowed for cuts and breakage.",
                "What whole number of tiles should be ordered?"),
            "paint_coverage": (
                "A wall is 8 m long and 3 m high. It needs 2 coats, and one paint "
                "can covers 10 m².", "How many whole paint cans are needed?"),
            "packaging_cost": (
                "A closed rectangular package is 10 cm by 8 cm by 5 cm. Covering "
                "material costs $0.03 per cm².",
                "What does the material for all six faces cost?"),
            "border_area": (
                "A rectangular picture is 12 cm by 8 cm and has a uniform 2 cm "
                "frame around every edge.", "What area is occupied by the frame alone?"),
            "ladder_or_shadow": (
                "A ladder reaches 4 m up a wall while its foot is 3 m from the wall; "
                "the wall and ground meet at a right angle.", "How long is the ladder?"),
            "garden_path": (
                "A 12 m by 8 m garden has a 2 m wide path running outside all four "
                "edges.", "What area does the path cover?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the school garden", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(321)
        for _ in range(900):
            result = GeometryInContextGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(number(fields[1]) ** int(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(math.isqrt(int(fields[1])), int(fields[2]), raw)
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]), raw)
                elif fields[0] == "AREA":
                    left, right = fields[1].split(" × ")
                    self.assertEqual(number(left) * number(right), number(fields[2]), raw)
                elif fields[0] == "CEIL":
                    self.assertEqual(math.ceil(number(fields[1])), int(fields[2]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(322)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = GeometryInContextGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(
                    result["operation"],
                    f"applied_geometry_in_context_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            GeometryInContextGenerator("bogus")
        with self.assertRaises(ValueError):
            GeometryInContextGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(323)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = GeometryInContextGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
