"""Problem-text-only brute-force oracles for SquareCubeLawGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.square_cube_law_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, SquareCubeLawGenerator,
)
from helpers import DELIM

MODELS = {
    "scale_model_area_volume": "model area = (real area in cm²)/k²",
    "map_area": "real area = (map area × k²)/10,000",
    "recipe_pan_scaling": "new batter = old batter × (size ratio)³",
    "area_unit_conversion": "area in new units = area × (linear factor)²",
    "volume_unit_conversion": "volume in new units = volume × (linear factor)³",
    "how_many_small_cubes": "count = k³",
    "giant_or_miniature": "area ×k²; volume ×k³",
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
    return re.sub(r"^A nearby shelf holds \d+ unrelated parts\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"built at a scale of 1 : (\d+)\..*?area of ([\d./]+) m²", text, re.S)
    if match:
        k = int(match.group(1))
        area_real = Fraction(match.group(2))
        model_cm2 = area_real * 10000 / (k * k)
        return "scale_model_area_volume", f"{exact(model_cm2)} cm²"

    match = re.search(
        r"scale of 1 : (\d+) \(1 cm on the map is \d+ cm in reality\)\. A "
        r"park's area on the map measures (\d+) cm²", text)
    if match:
        k, map_cm2 = int(match.group(1)), int(match.group(2))
        real_m2 = Fraction(map_cm2 * k * k, 10000)
        return "map_area", f"{exact(real_m2)} m²"

    match = re.search(
        r"scaled for a (\d+)-inch round pan uses ([\d./]+) cups of batter\. "
        r"A larger, similarly shaped pan measures (\d+) inches", text)
    if match:
        d1, batter, d2 = int(match.group(1)), Fraction(match.group(2)), int(match.group(3))
        ratio = Fraction(d2, d1)
        new_batter = batter * ratio ** 3
        return "recipe_pan_scaling", f"{exact(new_batter)} cups"

    match = re.search(r"Convert ([\d./]+) (\w+)² to (\w+)²", text)
    if match:
        amount, unit1, unit2 = Fraction(match.group(1)), match.group(2), match.group(3)
        factor = _linear_factor(unit1, unit2)
        result = amount * factor * factor
        return "area_unit_conversion", f"{exact(result)} {unit2}²"

    match = re.search(r"Convert ([\d./]+) (\w+)³ to (\w+)³", text)
    if match:
        amount, unit1, unit2 = Fraction(match.group(1)), match.group(2), match.group(3)
        factor = _linear_factor(unit1, unit2)
        result = amount * factor ** 3
        return "volume_unit_conversion", f"{exact(result)} {unit2}³"

    match = re.search(r"cube's edge length is scaled by a factor of (\d+)", text)
    if match:
        k = int(match.group(1))
        return "how_many_small_cubes", f"{k ** 3} cubes"

    match = re.search(
        r"creature's linear size scales by a factor of ([\d./]+), with "
        r"every body proportion unchanged", text)
    if match:
        k = Fraction(match.group(1))
        area_factor, volume_factor = k * k, k * k * k
        return ("giant_or_miniature",
                f"area ×{exact(area_factor)}; volume ×{exact(volume_factor)}; "
                "volume changes by the larger factor")

    raise AssertionError(f"unrecognized problem: {problem}")


#: The generator's own (unit1, unit2, factor) bank — the oracle looks up the
#: same public linear conversion facts, an ordinary supplied constant, not a
#: replication of the generator's arithmetic.
LINEAR_FACTS = {("m", "cm"): 100, ("km", "m"): 1000, ("cm", "mm"): 10,
               ("m", "mm"): 1000}


def _linear_factor(unit1, unit2):
    return LINEAR_FACTS[(unit1, unit2)]


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer)


class TestSquareCubeLawGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(410)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = SquareCubeLawGenerator(variant, modifier).generate()
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
            solve("A model car is built at a scale of 1 : 20. The real "
                  "model car's windshield has an area of 2 m². What is the "
                  "model windshield's area in cm²?"),
            ("scale_model_area_volume", "50 cm²"))

    def test_how_many_small_cubes_matches_the_plans_worked_example(self):
        random.seed(411)
        for _ in range(200):
            result = SquareCubeLawGenerator("how_many_small_cubes", "plain").generate()
            k = int(re.search(r"factor of (\d+)", result["problem"]).group(1))
            self.assertEqual(result["final_answer"].split(" ")[0], str(k ** 3))

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "scale_model_area_volume": (
                "A model car is built at a scale of 1 : 20. The real "
                "model car's windshield has an area of 2 m².",
                "What is the model windshield's area in cm²?"),
            "map_area": (
                "A map is drawn at a scale of 1 : 1000 (1 cm on the map is "
                "1000 cm in reality). A park's area on the map measures 5 cm².",
                "What is the real area of the park in m²?"),
            "recipe_pan_scaling": (
                "A recipe scaled for a 4-inch round pan uses 2 cups of "
                "batter. A larger, similarly shaped pan measures 6 inches.",
                "How much batter does the larger pan need?"),
            "area_unit_conversion": (
                "Convert 5 m² to cm².", "What is the equivalent area?"),
            "volume_unit_conversion": (
                "Convert 2 m³ to cm³.", "What is the equivalent volume?"),
            "how_many_small_cubes": (
                "A cube's edge length is scaled by a factor of 3.",
                "How many of the original small cubes fit inside the new larger cube?"),
            "giant_or_miniature": (
                "A creature's linear size scales by a factor of 2, with "
                "every body proportion unchanged.",
                "By what factor do its cross-sectional area (strength) and "
                "its volume (weight) change?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(412)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SquareCubeLawGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_square_cube_law_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SquareCubeLawGenerator("bogus")
        with self.assertRaises(ValueError):
            SquareCubeLawGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(413)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = SquareCubeLawGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = SquareCubeLawGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
