"""Problem-text-only oracles for the applied percent-word extension."""
import random
import re
import unittest
from fractions import Fraction

from generators.percent_word_problem_generator import (
    APPLIED,
    MODIFIERS,
    MONEY_OPS,
    PHRASINGS,
    VARIANTS,
    PercentWordProblemGenerator,
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


def clean(problem):
    return re.sub(r"^A shelf nearby holds \d+ empty folders\. ", "", problem)


def solve(problem):
    """Infer the arithmetic variant and answer from the story alone."""
    text = clean(problem)
    pct = int(re.search(r"(\d+)%", text).group(1))
    base_match = (re.search(r"\$(\d+)\.00", text)
                  or re.search(r"(\d+)-dollar", text)
                  or re.search(r"(\d+)(?:-unit| units)", text))
    if not base_match:
        raise AssertionError(f"base not found: {problem}")
    base = int(base_match.group(1))
    lower = text.lower()
    if "tax" in lower:
        variant = "tax"
    elif "$" in text or "dollar" in lower:
        variant = ("discount" if any(word in lower for word in
                   ("discount", "% off", "reduces", "reduction", "cheaper"))
                   else "markup")
    elif any(word in lower for word in ("falls", "smaller", "drops",
                                         "reduction", "loses")):
        variant = "decrease"
    else:
        variant = "increase"
    additive = variant in ("increase", "markup", "tax")
    change = Fraction(base * pct, 100)
    total = base + change if additive else base - change
    answer = money_text(total) if variant in MONEY_OPS else f"{exact_text(total)} units"
    sign = "+" if additive else "-"
    model = f"x = {base}*(1{sign}{pct}/100)"
    return variant, answer, model


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; x = {answer}"
    return variant, answer


class TestPercentWordProblemGenerator(unittest.TestCase):
    def test_marker_contract_and_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(249)
        seen = set()
        for _ in range(1000):
            variant = random.choice(VARIANTS)
            modifier = random.choice(MODIFIERS)
            result = PercentWordProblemGenerator(modifier=modifier,
                                                 variant=variant).generate()
            self.assertEqual(result["steps"][-1],
                             f"Z{DELIM}{result['final_answer']}")
            parsed_variant, answer = expected(result["problem"], modifier)
            self.assertEqual(parsed_variant, variant)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_phrasings_are_invertible(self):
        for variant, phrasings in PHRASINGS.items():
            self.assertEqual(len(phrasings), 5)
            for index, phrasing in enumerate(phrasings):
                rendered = phrasing.format(base=80, pct=25)
                problem = f"At the corner shop, {rendered[:1].lower() + rendered[1:]}"
                with self.subTest(variant=variant, phrasing=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_arithmetic_steps(self):
        random.seed(250)
        for _ in range(600):
            result = PercentWordProblemGenerator(
                modifier=random.choice(MODIFIERS)).generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw)

    def test_modifier_shapes_and_legacy_constructor(self):
        random.seed(251)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = PercentWordProblemGenerator(
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
        self.assertEqual(PercentWordProblemGenerator().modifier, "plain")
        self.assertEqual(PercentWordProblemGenerator(distractor=True).modifier,
                         "distractor")
        with self.assertRaises(ValueError):
            PercentWordProblemGenerator(modifier="bogus")
        with self.assertRaises(ValueError):
            PercentWordProblemGenerator(variant="bogus")
        with self.assertRaises(ValueError):
            PercentWordProblemGenerator(distractor=True, modifier="plain")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(252)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(500):
            result = PercentWordProblemGenerator(
                modifier=random.choice(MODIFIERS)).generate()
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
