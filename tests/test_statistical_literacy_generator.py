"""Problem-text-only brute-force oracles for StatisticalLiteracyGenerator."""
import math
import random
import re
import unittest
from fractions import Fraction

from generators.statistical_literacy_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, StatisticalLiteracyGenerator,
)
from helpers import DELIM

MODELS = {
    "regression_to_mean": "predicted = mean + r × (score − mean)",
    "averaging_rates_wrong": "pooled = (count1 + count2)/(n1 + n2); naive = (rate1 + rate2)/2",
    "visual_ratio_truncated_axis": "visual = (bar2 − baseline)/(bar1 − baseline); true = bar2/bar1",
    "sampling_error_scale": "margin = 1/√n",
    "percent_of_what": "reverse = 100p/(100 + p)",
    "cherry_picked_interval": "window = (v3 − v2)/v2; full = (v4 − v1)/v1",
}


def dec(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    scaled, places = value, 0
    while scaled.denominator != 1 and places < 12:
        scaled *= 10
        places += 1
    if scaled.denominator != 1:
        raise AssertionError(f"does not terminate: {value}")
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    text = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return ("-" if value < 0 else "") + text


def exact(value):
    value = Fraction(value)
    try:
        return dec(value)
    except AssertionError:
        return str(value)


def clean(problem):
    return re.sub(r"^An unrelated log lists \d+ archived entries\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(r"mean is (\d+) and the [\w-]+ correlation is "
                      r"([\d.]+)\. A \w+ scored (\d+)", text)
    if match:
        mu, r, x = int(match.group(1)), Fraction(match.group(2)), int(match.group(3))
        predicted = mu + r * (x - mu)
        return "regression_to_mean", dec(predicted)

    match = re.search(r"([\d.]+)% of (\d+) \w+ passed in one group, and "
                      r"([\d.]+)% of (\d+) \w+ passed in another group", text)
    if match:
        pct1, n1, pct2, n2 = match.groups()
        n1, n2 = int(n1), int(n2)
        rate1, rate2 = Fraction(pct1) / 100, Fraction(pct2) / 100
        c1, c2 = rate1 * n1, rate2 * n2
        assert c1.denominator == 1 and c2.denominator == 1, text
        naive = (rate1 + rate2) / 2 * 100
        pooled = Fraction(int(c1) + int(c2), n1 + n2) * 100
        return ("averaging_rates_wrong",
                f"{dec(pooled)}%; averaging the two percents gives {dec(naive)}%, which is wrong")

    match = re.search(r"vertical axis starts at (\d+) instead of 0\. One "
                      r"bar reaches (\d+), and another reaches (\d+)", text)
    if match:
        base, h1, h2 = map(int, match.groups())
        d1, d2 = h1 - base, h2 - base
        visual, true = Fraction(d2, d1), Fraction(h2, h1)
        return "visual_ratio_truncated_axis", f"visual {exact(visual)}; true {exact(true)}"

    first = re.search(r"n = (\d+) people has a margin of error of about [\d.]+%", text)
    second = re.search(r"grows to n = (\d+) people", text)
    if first and second:
        n1, n2 = int(first.group(1)), int(second.group(1))
        m1, m2 = math.isqrt(n1), math.isqrt(n2)
        assert m1 * m1 == n1 and m2 * m2 == n2, text
        assert m2 % m1 == 0, text
        k = m2 // m1
        margin1, margin2 = Fraction(1, m1), Fraction(1, m2)
        return ("sampling_error_scale",
                f"factor of {k}; margin goes from {dec(margin1 * 100)}% "
                f"to {dec(margin2 * 100)}%")

    match = re.search(r"Quantity A is (\d+)% more than quantity B, and B "
                      r"is (\d+)", text)
    if match:
        p, B = int(match.group(1)), int(match.group(2))
        A = B * Fraction(100 + p, 100)
        assert A.denominator == 1, text
        A = int(A)
        reverse = Fraction(100 * p, 100 + p)
        return ("percent_of_what",
                f"{dec(reverse)}%; not {p}% (the base changed from {B} to {A})")

    match = re.search(r"measured (\d+) in year 1, (\d+) in year 2, (\d+) "
                      r"in year 3, and (\d+) in year 4", text)
    if match:
        v1, v2, v3, v4 = map(int, match.groups())
        window = Fraction(v3 - v2, v2) * 100
        full = Fraction(v4 - v1, v1) * 100
        return ("cherry_picked_interval",
                f"{dec(window)}%; {dec(full)}% (window: year 2 to 3, full: year 1 to 4)")

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestStatisticalLiteracyGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(380)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = StatisticalLiteracyGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "regression_to_mean": (
                "Class mean is 70 and the retest correlation is 0.5. A "
                "student scored 90.", "What retest score should be expected?"),
            "averaging_rates_wrong": (
                "50% of 20 items passed in one group, and 100% of 80 items "
                "passed in another group.",
                "What is the combined pass percent for both groups, and "
                "how does it compare to simply averaging the two percents?"),
            "visual_ratio_truncated_axis": (
                "A bar chart's vertical axis starts at 85 instead of 0. "
                "One bar reaches 90, and another reaches 95.",
                "What ratio does the chart visually suggest between the "
                "two bars, and what is the true ratio?"),
            "sampling_error_scale": (
                "Using the approximation that margin of error is about "
                "1/√n, a poll of n = 400 people has a margin of error of "
                "about 5%.",
                "If the poll grows to n = 1600 people, by what factor does "
                "the margin of error shrink, and what is the new margin of error?"),
            "percent_of_what": (
                "Quantity A is 25% more than quantity B, and B is 8.",
                "By what percent is B less than A?"),
            "cherry_picked_interval": (
                "A metric measured 100 in year 1, 100 in year 2, 175 in "
                "year 3, and 120 in year 4. A report highlights only the "
                "change from year 2 to year 3.",
                "What is the percent change from year 2 to year 3, and "
                "what is the percent change over the full period from "
                "year 1 to year 4?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_plans_worked_examples(self):
        self.assertEqual(
            solve("Class mean is 70 and the retest correlation is 0.5. A "
                  "student scored 90. What retest score should be expected?"),
            ("regression_to_mean", "80"))
        self.assertEqual(
            solve("50% of 20 items passed in one group, and 100% of 80 "
                  "items passed in another group. What is the combined "
                  "pass percent for both groups, and how does it compare "
                  "to simply averaging the two percents?"),
            ("averaging_rates_wrong",
             "90%; averaging the two percents gives 75%, which is wrong"))
        self.assertEqual(
            solve("A bar chart's vertical axis starts at 85 instead of 0. "
                  "One bar reaches 90, and another reaches 95. What ratio "
                  "does the chart visually suggest between the two bars, "
                  "and what is the true ratio?"),
            ("visual_ratio_truncated_axis", "visual 2; true 19/18"))

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(381)
        for _ in range(700):
            result = StatisticalLiteracyGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "PCT_MORE":
                    lhs, rhs = fields[1].split(" × ")
                    self.assertEqual(Fraction(lhs) * Fraction(rhs), Fraction(fields[2]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(382)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = StatisticalLiteracyGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_statistical_literacy_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            StatisticalLiteracyGenerator("bogus")
        with self.assertRaises(ValueError):
            StatisticalLiteracyGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(383)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = StatisticalLiteracyGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = StatisticalLiteracyGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
