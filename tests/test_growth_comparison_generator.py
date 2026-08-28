"""Problem-text-only brute-force oracles for GrowthComparisonGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.growth_comparison_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, GrowthComparisonGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace(",", "").replace("%", "").rstrip("."))


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
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def money(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    cents = int(cents)
    return f"${cents // 100}.{cents % 100:02d}"


def clean(problem):
    return re.sub(r"^An unrelated memo lists \d+ archive boxes\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"value starts at (\$[0-9.]+)\. Plan L adds (\$[0-9.]+) each year, "
        r"while plan E grows by (\d+)% each year", text, re.I)
    year_match = re.search(r"end of year (\d+)", text, re.I)
    if match and year_match:
        start, increment = number(match.group(1)), number(match.group(2))
        rate, years = int(match.group(3)), int(year_match.group(1))
        linear = start + increment * years
        exponential = start * (1 + Fraction(rate, 100)) ** years
        winner = "exponential" if exponential > linear else "linear"
        difference = abs(exponential - linear)
        model = f"L(n) = {start} + {increment}n; E(n) = {start}({exact_text(1 + Fraction(rate, 100))})^n"
        return "linear_vs_exponential_table", f"{winner}; difference {money(difference)}", model

    match = re.search(
        r"Offer A starts at (\$[0-9.]+) and adds (\$[0-9.]+) each year\. "
        r"Offer B starts at (\$[0-9.]+) and grows (\d+)% each year", text, re.I)
    if match:
        start, increment, start_b = map(number, match.groups()[:3])
        rate = int(match.group(4))
        if start != start_b:
            raise AssertionError("offer starts differ")
        factor = 1 + Fraction(rate, 100)
        crossing = next(year for year in range(1, 101)
                        if start * factor ** year > start + increment * year)
        linear, exponential = start + increment * crossing, start * factor ** crossing
        model = f"A(n) = {start} + {increment}n; B(n) = {start}({exact_text(factor)})^n"
        return "crossover_year", f"year {crossing}; {money(exponential)} vs {money(linear)}", model

    match = re.search(
        r"account grows at (\d+)% per year\. For this estimate, use the rule "
        r"of 70", text, re.I)
    if match:
        rate = int(match.group(1))
        years = Fraction(70, rate)
        word = "year" if years == 1 else "years"
        return "rule_of_70_doubling", f"{years} {word}", f"doubling time ≈ 70/{rate}"

    match = re.search(
        r"machine is worth (\$[0-9.]+) and loses (\d+)% of its value each "
        r"year\. A replacement is required once its value is below (\$[0-9.]+)", text, re.I)
    if match:
        start, threshold = number(match.group(1)), number(match.group(3))
        rate = int(match.group(2))
        factor = 1 - Fraction(rate, 100)
        year, value = 0, start
        while value >= threshold:
            year += 1
            value *= factor
        model = f"V(n) = {start}({exact_text(factor)})^n"
        return "depreciation_below_threshold", f"year {year}; value {money(value)}", model

    match = re.search(
        r"culture starts with (\d+) cells and doubles once per hour", text, re.I)
    target_match = re.search(r"reach (\d+) cells", text, re.I)
    if match and target_match:
        start, target = int(match.group(1)), int(target_match.group(1))
        current, hours = start, 0
        while current < target:
            current *= 2
            hours += 1
        word = "hour" if hours == 1 else "hours"
        return "repeated_doubling_count", f"{hours} {word}", f"{start} × 2^h = {target}"

    match = re.search(
        r"For (\d+) years, offer A pays (\$[0-9.]+) initially plus "
        r"(\$[0-9.]+) more each year\. Offer B starts at (\$[0-9.]+) and "
        r"grows (\d+)% per year", text, re.I)
    if match:
        years = int(match.group(1))
        start, increment, start_b = map(number, match.groups()[1:4])
        rate = int(match.group(5))
        if start != start_b:
            raise AssertionError("offer starts differ")
        factor = 1 + Fraction(rate, 100)
        linear = start + increment * years
        exponential = start * factor ** years
        winner = "offer B" if exponential > linear else "offer A"
        model = f"A = {start} + {increment}({years}); B = {start}({exact_text(factor)})^{years}"
        return "which_offer", f"{winner}; A {money(linear)}; B {money(exponential)}", model

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model = solve(problem)
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestGrowthComparisonGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(350)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = GrowthComparisonGenerator(variant, modifier).generate()
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
            "linear_vs_exponential_table": ("A value starts at $100.00. Plan L adds "
                                            "$10.00 each year, while plan E grows by 10% "
                                            "each year.", "At the end of year 3, which "
                                            "plan is larger and by how much?"),
            "crossover_year": ("Offer A starts at $100.00 and adds $10.00 each year. "
                               "Offer B starts at $100.00 and grows 10% each year.",
                               "What is the first whole year when offer B is worth more than offer A?"),
            "rule_of_70_doubling": ("An account grows at 7% per year. For this estimate, "
                                    "use the rule of 70: divide 70 by the annual percent rate.",
                                    "About how many years will doubling take?"),
            "depreciation_below_threshold": ("A machine is worth $8000.00 and loses 25% "
                                             "of its value each year. A replacement is "
                                             "required once its value is below $4000.00.",
                                             "What is the first whole year when replacement is required?"),
            "repeated_doubling_count": ("A culture starts with 5 cells and doubles once "
                                        "per hour.", "How many complete hours does it take "
                                        "to reach 160 cells?"),
            "which_offer": ("For 3 years, offer A pays $100.00 initially plus $10.00 more "
                            "each year. Offer B starts at $100.00 and grows 20% per year.",
                            "Which offer has the larger value at the end, and what are both values?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(351)
        for _ in range(900):
            result = GrowthComparisonGenerator().generate()
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

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(352)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = GrowthComparisonGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"], f"applied_growth_comparison_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            GrowthComparisonGenerator("bogus")
        with self.assertRaises(ValueError):
            GrowthComparisonGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(353)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = GrowthComparisonGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
