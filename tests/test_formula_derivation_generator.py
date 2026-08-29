"""Problem-text-only exact oracles for FormulaDerivationGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.formula_derivation_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, FormulaDerivationGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("−", "-").rstrip("."))


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
        return str(value)
    scaled, places = value, 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def money(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^An unrelated cabinet holds \d+ index cards\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(r"sum is 1 \+ 2 \+ \.\.\. \+ (\d+)", text, re.I)
    if match:
        n = int(match.group(1))
        total = sum(range(1, n + 1))
        model = "S = n(n + 1)/2"
        return "arithmetic_series_pairing", f"{model}; S_{n} = {total}", model

    match = re.search(r"convex polygon has (\d+) sides", text, re.I)
    if match:
        sides = int(match.group(1))
        total = sum(180 for _ in range(sides - 2))
        model = "interior total = (n − 2)·180°"
        return "interior_angle_sum_triangulation", f"{model}; {total}°", model

    match = re.search(
        r"triangle has base (\d+) cm and perpendicular height (\d+) cm", text, re.I)
    if match:
        base, height = map(int, match.groups())
        area = Fraction(base * height, 2)
        model = "A = bh/2"
        return "triangle_area_from_rectangle", f"{model}; {exact_text(area)} cm²", model

    match = re.search(
        r"trapezoid has parallel sides (\d+) cm and (\d+) cm and perpendicular "
        r"height (\d+) cm", text, re.I)
    if match:
        base1, base2, height = map(int, match.groups())
        area = Fraction((base1 + base2) * height, 2)
        model = "A = (b1 + b2)h/2"
        return "trapezoid_from_triangles", f"{model}; {exact_text(area)} cm²", model

    match = re.search(
        r"Two points are \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\)", text, re.I)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
        distance = math.isqrt(squared)
        if distance ** 2 != squared:
            raise AssertionError("distance is not integral")
        model = "d = sqrt((x2 − x1)^2 + (y2 − y1)^2)"
        return "distance_formula_from_pythagoras", f"{model}; d = {distance}", model

    match = re.search(r"exact calculation is ([0-9/]+) ÷ ([0-9/]+)", text, re.I)
    if match:
        first, second = map(Fraction, match.groups())
        result = first / second
        model = "a/b ÷ c/d = ad/bc"
        answer = f"{model}; {first} ÷ {second} = {result}"
        return "divide_by_fraction_reciprocal", answer, model

    match = re.search(
        r"account starts with (\$[0-9.]+) and grows (\d+)% once per year for "
        r"(\d+) years", text, re.I)
    if match:
        principal, rate, years = number(match.group(1)), int(match.group(2)), int(match.group(3))
        value = principal
        for _ in range(years):
            value *= 1 + Fraction(rate, 100)
        model = "A = P(1 + r)^t"
        return "compound_interest_repeated_multiplication", f"{model}; after {years} years {money(value)}", model

    match = re.search(
        r"equation is x² ([+−]) (\d+)x ([+−]) (\d+) = 0", text, re.I)
    if match:
        b = int(match.group(2)) * (1 if match.group(1) == "+" else -1)
        c = int(match.group(4)) * (1 if match.group(3) == "+" else -1)
        discriminant = b * b - 4 * c
        root_disc = math.isqrt(discriminant)
        if root_disc ** 2 != discriminant:
            raise AssertionError("non-square discriminant")
        roots = sorted({Fraction(-b + sign * root_disc, 2) for sign in (-1, 1)})
        model = "x = (−b ± sqrt(b² − 4ac))/(2a)"
        answer = f"{model}; x = {roots[0]} or x = {roots[1]}"
        return "quadratic_formula_complete_square_concrete", answer, model

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestFormulaDerivationGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(390)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(16):
                    result = FormulaDerivationGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "arithmetic_series_pairing": ("The sum is 1 + 2 + ... + 20.",
                                          "Show a general expression for 1 + 2 + ... + n, then evaluate this sum."),
            "interior_angle_sum_triangulation": ("A convex polygon has 6 sides.",
                                                 "Build a general expression for its interior-angle total, then evaluate it."),
            "triangle_area_from_rectangle": ("A triangle has base 8 cm and perpendicular "
                                             "height 5 cm.", "Relate it to a matching rectangle, "
                                             "state the general area relationship, and find its area."),
            "trapezoid_from_triangles": ("A trapezoid has parallel sides 12 cm and 6 cm "
                                         "and perpendicular height 8 cm.", "Split it into two "
                                         "triangles, state the general area relationship, and find its area."),
            "distance_formula_from_pythagoras": ("Two points are (1, 2) and (4, 6).",
                                                 "Use their horizontal and vertical changes to "
                                                 "state the general distance relationship and find this distance."),
            "divide_by_fraction_reciprocal": ("The exact calculation is 3/4 ÷ 2/5.",
                                              "Rewrite both quantities with one denominator, then "
                                              "state the general multiplication relationship and evaluate."),
            "compound_interest_repeated_multiplication": ("An account starts with $1000.00 "
                                                          "and grows 10% once per year for 2 years.",
                                                          "Show the repeated yearly multiplication, state the "
                                                          "general relationship, and find the final balance."),
            "quadratic_formula_complete_square_concrete": ("The equation is x² − 5x + 6 = 0.",
                                                           "Rearrange it into a square, state the corresponding "
                                                           "general relationship, and give both exact solutions."),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the classroom", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(391)
        for _ in range(1000):
            result = FormulaDerivationGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]), number(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(number(fields[1]) ** int(fields[2]), number(fields[3]), raw)
                elif fields[0] == "ROOT":
                    self.assertEqual(number(fields[2]) ** 2, number(fields[1]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(392)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = FormulaDerivationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_formula_derivation_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            FormulaDerivationGenerator("bogus")
        with self.assertRaises(ValueError):
            FormulaDerivationGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(393)
        banned = ("^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = FormulaDerivationGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)-?1x\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
