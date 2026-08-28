"""Problem-text-only exact oracles for QuadraticWordGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.quadratic_word_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, QuadraticWordGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("−", "-").rstrip("."))


def money(value):
    cents = int(Fraction(value) * 100)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^An unrelated notice mentions \d+ storage bins\. ", "", problem)


def polynomial_coefficients(expression, variable="t"):
    text = expression.replace("−", "-").replace(" ", "")
    match = re.fullmatch(
        rf"([+-]?\d*){variable}²([+-]\d*){variable}([+-]\d+)", text)
    if not match:
        raise AssertionError(f"cannot parse polynomial: {expression}")
    lead = match.group(1)
    a = -1 if lead == "-" else 1 if lead in ("", "+") else int(lead)
    middle = match.group(2)
    b = -1 if middle == "-" else 1 if middle == "+" else int(middle)
    return a, b, int(match.group(3))


def integral_roots(a, b, c):
    discriminant = b * b - 4 * a * c
    root = math.isqrt(discriminant)
    if root * root != discriminant:
        raise AssertionError(f"non-square discriminant {discriminant}")
    roots = {Fraction(-b + sign * root, 2 * a) for sign in (-1, 1)}
    if any(value.denominator != 1 for value in roots):
        raise AssertionError(f"non-integral roots {roots}")
    return sorted(int(value) for value in roots)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"ball's height in meters after t seconds is h\(t\) = ([^.]+)\.",
        text, re.I)
    if match:
        expression = match.group(1)
        roots = integral_roots(*polynomial_coefficients(expression))
        positive = [root for root in roots if root >= 0]
        if len(positive) != 1:
            raise AssertionError(f"physical root not unique: {roots}")
        answer = f"{positive[0]} seconds" if positive[0] != 1 else "1 second"
        return "projectile_ground_time", answer, f"{expression} = 0"

    match = re.search(
        r"object's height in meters after t seconds is h\(t\) = ([^.]+)\.",
        text, re.I)
    if match:
        expression = match.group(1)
        a, b, c = polynomial_coefficients(expression)
        vertex = Fraction(-b, 2 * a)
        height = a * vertex * vertex + b * vertex + c
        answer = f"at {vertex} seconds; {height} m"
        return "projectile_max_height", answer, f"h(t) = {expression}"

    match = re.search(
        r"A (\d+) cm by (\d+) cm picture has a uniform border\. The outside "
        r"rectangle has area (\d+) cm²", text, re.I)
    if match:
        length, width, outer_area = map(int, match.groups())
        # Expand independently and solve with the discriminant.
        roots = integral_roots(4, 2 * (length + width), length * width - outer_area)
        positive = [root for root in roots if root > 0]
        if len(positive) != 1:
            raise AssertionError(f"border root not unique: {roots}")
        border = positive[0]
        model = f"({length} + 2x)({width} + 2x) = {outer_area}"
        return "area_with_border", f"{border} cm", model

    match = re.search(
        r"price p dollars, a seller can sell q = (\d+) − (\d+)p items", text, re.I)
    if match:
        intercept, slope = map(int, match.groups())
        candidates = [(p * (intercept - slope * p), p)
                      for p in range(intercept // slope + 1)]
        revenue, price = max(candidates)
        model = f"R = p({intercept} − {slope}p)"
        return "revenue_linear_demand", f"{money(price)}; revenue {money(revenue)}", model

    match = re.search(
        r"rectangular lot has area (\d+) m² and perimeter (\d+) m", text, re.I)
    if match:
        area, perimeter = map(int, match.groups())
        pairs = [(length, width) for length in range(1, perimeter)
                 for width in range(1, length)
                 if length * width == area and 2 * (length + width) == perimeter]
        if len(pairs) != 1:
            raise AssertionError(f"dimensions not unique: {pairs}")
        length, width = pairs[0]
        half = perimeter // 2
        return "rectangle_from_area_perimeter", f"{length} m by {width} m", f"x({half} − x) = {area}"

    match = re.search(
        r"product of two consecutive positive integers is (\d+)", text, re.I)
    if match:
        product = int(match.group(1))
        first = (math.isqrt(1 + 4 * product) - 1) // 2
        if first * (first + 1) != product:
            raise AssertionError(f"not a consecutive product: {product}")
        return "consecutive_product", f"{first} and {first + 1}", f"n(n + 1) = {product}"

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestQuadraticWordGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(340)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = QuadraticWordGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "projectile_ground_time": ("A ball's height in meters after t seconds "
                                       "is h(t) = −5t² + 20t + 25.",
                                       "When does the ball reach the ground?"),
            "projectile_max_height": ("A launched object's height in meters after t "
                                      "seconds is h(t) = −2t² + 12t + 5.",
                                      "At what time is it highest, and what is that height?"),
            "area_with_border": ("A 8 cm by 6 cm picture has a uniform border. The "
                                 "outside rectangle has area 120 cm².",
                                 "How wide is the border?"),
            "revenue_linear_demand": ("At price p dollars, a seller can sell q = 40 − "
                                      "2p items. Revenue is the price times the number sold.",
                                      "What price gives the greatest revenue, and what is that revenue?"),
            "rectangle_from_area_perimeter": ("A rectangular lot has area 96 m² and "
                                              "perimeter 40 m.", "What are its dimensions?"),
            "consecutive_product": ("The product of two consecutive positive integers "
                                    "is 156.", "What are the two integers?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the recreation center", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_and_physical_root_steps(self):
        random.seed(341)
        rejected = {"projectile_ground_time": False, "area_with_border": False,
                    "consecutive_product": False}
        for _ in range(1000):
            result = QuadraticWordGenerator().generate()
            variant = next(v for v in VARIANTS if f"_{v}_" in result["operation"])
            codes = [raw.split(DELIM)[0] for raw in result["steps"]]
            if variant in rejected and "REJECT" in codes:
                rejected[variant] = True
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
        self.assertTrue(all(rejected.values()), rejected)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(342)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = QuadraticWordGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_quadratic_word_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            QuadraticWordGenerator("bogus")
        with self.assertRaises(ValueError):
            QuadraticWordGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(343)
        banned = ("^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = QuadraticWordGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)[−-]?1[xt](?:²)?\b", joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
