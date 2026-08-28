"""Problem-text-only oracles for the applied proportion extension."""
import random
import re
import unittest
from fractions import Fraction

from generators.proportion_word_problem_generator import (
    APPLIED,
    MODIFIERS,
    PHRASINGS,
    VARIANTS,
    ProportionWordProblemGenerator,
)
from helpers import DELIM


def exact_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + rendered


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def plural(value, singular):
    return singular if Fraction(value) == 1 else singular + "s"


def clean(problem):
    return re.sub(r"^A notice nearby lists \d+ lockers\. ", "", problem)


def _shadow_values(text):
    patterns = (
        r"A (\d+) m pole casts a (\d+) m shadow.*tree casts a (\d+) m shadow",
        r"pole (\d+) m tall has a (\d+) m shadow.*shadow is (\d+) m",
        r"A (\d+) m shadow belongs to a (\d+) m pole.*shadow is (\d+) m",
        r"a (\d+) m marker has a (\d+) m shadow.*tree has a (\d+) m shadow",
        r"a (\d+) m pole a (\d+) m shadow.*measures (\d+) m",
    )
    for index, pattern in enumerate(patterns):
        match = re.search(pattern, text, re.I)
        if match:
            values = tuple(map(int, match.groups()))
            if index == 2:
                shadow, height, query = values
                return height, shadow, query
            return values
    return None


def solve(problem):
    """Infer every operand from its printed unit and recompute exactly."""
    text = clean(problem)

    if "shadow" in text.lower():
        values = _shadow_values(text)
        if not values:
            raise AssertionError(f"shadow grammar not recognized: {problem}")
        height, shadow, query = values
        value = Fraction(height * query, shadow)
        model = f"{height}/{shadow} = x/{query}"
        return "shadow_similar_triangles", f"{exact_text(value)} m", model

    if "map" in text.lower() and " km" in text and "hours" in text.lower():
        factor = int(re.search(r"(\d+) km", text).group(1))
        draw = next(v for v in map(int, re.findall(r"(\d+) cm", text)) if v != 1)
        elapsed = int(re.search(r"(\d+) hours", text).group(1))
        value = Fraction(factor * draw, elapsed)
        model = f"x = {factor}*{draw}/{elapsed}"
        return "speed_from_map", f"{exact_text(value)} km/h", model

    if "map" in text.lower() and " km" in text:
        factor = int(re.search(r"(\d+) km", text).group(1))
        query = next(v for v in map(int, re.findall(r"(\d+) cm", text)) if v != 1)
        value = factor * query
        model = f"1/{factor} = {query}/x"
        return "map_scale", f"{value} km", model

    if " cm" in text and " m" in text:
        factor = int(re.search(r"(\d+) m", text).group(1))
        query = next(v for v in map(int, re.findall(r"(\d+) cm", text)) if v != 1)
        value = factor * query
        model = f"1/{factor} = {query}/x"
        return "scale_drawing", f"{value} m", model

    if "batch" in text.lower() and "oil" in text.lower():
        amount = Fraction(re.search(r"([0-9]+(?:\.[0-9]+|/[0-9]+)?) cup",
                                    text).group(1))
        query = int(re.search(r"(\d+) batches", text).group(1))
        value = amount * query
        model = f"{exact_text(amount)}/1 = x/{query}"
        return "recipe_scaling", f"{exact_text(value)} {plural(value, 'cup')}", model

    if "miles" in text.lower() or "mile trip" in text.lower():
        known = int(re.search(r"(\d+)(?:-mile| miles)", text).group(1))
        times = list(map(int, re.findall(r"(\d+) hours", text)))
        denominator, query = times[0], times[-1]
        value = Fraction(known * query, denominator)
        model = f"{known}/{denominator} = x/{query}"
        return "speed", f"{exact_text(value)} mi", model

    if "flour" in text.lower():
        known = int(re.search(r"(\d+) cups?", text).group(1))
        servings = list(map(int, re.findall(r"(\d+)(?:-serving| servings)", text)))
        denominator, query = servings[0], servings[-1]
        value = Fraction(known * query, denominator)
        model = f"{known}/{denominator} = x/{query}"
        return "recipe", f"{exact_text(value)} {plural(value, 'cup')}", model

    if "apples" in text.lower():
        cost = Fraction(re.search(r"\$(\d+)\.00", text).group(1))
        pounds = list(map(int, re.findall(r"(\d+)(?:-pound| pounds)", text)))
        denominator, query = pounds[0], pounds[-1]
        value = cost * query / denominator
        model = f"{int(cost)}/{denominator} = x/{query}"
        return "cost", money_text(value), model

    if any(word in text.lower() for word in ("data table", "maps to",
                                              "the table", "machine turns",
                                              "input is")):
        values = list(map(int, re.findall(r"\d+", text)))
        denominator, known, query = values[-3:]
        value = Fraction(known * query, denominator)
        model = f"{known}/{denominator} = x/{query}"
        return "ratio_table", f"{exact_text(value)} output units", model
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; x = {answer}"
    return variant, answer


class TestProportionWordProblemGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(253)
        seen = set()
        for _ in range(1400):
            variant = random.choice(VARIANTS)
            modifier = random.choice(MODIFIERS)
            result = ProportionWordProblemGenerator(
                modifier=modifier, variant=variant).generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_phrasings_are_invertible(self):
        fields = {
            "speed": dict(k1=60, k2=3, q=5),
            "recipe": dict(k1=6, k2=4, q=10),
            "cost": dict(k1=12, k2=3, q=5),
            "ratio_table": dict(k1=12, k2=3, q=5),
            "scale_drawing": dict(factor=4, q=7),
            "map_scale": dict(factor=5, q=8),
            "recipe_scaling": dict(amount="3/4", q=6),
            "shadow_similar_triangles": dict(height=6, shadow=2, q=8),
            "speed_from_map": dict(factor=5, draw=8, hours=2),
        }
        for variant, phrasings in PHRASINGS.items():
            self.assertEqual(len(phrasings), 5)
            for index, phrasing in enumerate(phrasings):
                rendered = phrasing.format(**fields[variant])
                problem = f"At the market stand, {rendered[:1].lower() + rendered[1:]}"
                with self.subTest(variant=variant, phrasing=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(254)
        for _ in range(700):
            result = ProportionWordProblemGenerator(
                modifier=random.choice(MODIFIERS)).generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_modifier_shapes_and_legacy_constructor(self):
        random.seed(255)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = ProportionWordProblemGenerator(
                    modifier=modifier, variant=variant).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["final_answer"],
                                 expected(result["problem"], modifier)[1])
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        self.assertEqual(ProportionWordProblemGenerator().modifier, "plain")
        self.assertEqual(ProportionWordProblemGenerator(distractor=True).modifier,
                         "distractor")
        with self.assertRaises(ValueError):
            ProportionWordProblemGenerator(modifier="bogus")
        with self.assertRaises(ValueError):
            ProportionWordProblemGenerator(variant="bogus")
        with self.assertRaises(ValueError):
            ProportionWordProblemGenerator(distractor=True, modifier="plain")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(256)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = ProportionWordProblemGenerator(
                modifier=random.choice(MODIFIERS)).generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"],
                               *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            self.assertIsNone(re.search(r"(?<!\d)1 (?:hours|servings|pounds)\b",
                                        joined.lower()))
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
