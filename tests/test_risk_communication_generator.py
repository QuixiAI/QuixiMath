"""Problem-text-only brute-force oracles for RiskCommunicationGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.risk_communication_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, RiskCommunicationGenerator,
)
from helpers import DELIM

MULTIPLIER_WORD_TO_K = {"doubles": 2, "triples": 3, "quadruples": 4,
                        "increases fivefold": 5}

MODELS = {
    "relative_vs_absolute": "relative = (a − b)/a; absolute = (a − b)/n",
    "percent_vs_percentage_points": "points = p2 − p1; percent = (p2 − p1)/p1",
    "nnt": "NNT = 1/ARR",
    "per_capita_vs_raw": "rate = cases/(population/1000)",
    "rate_per_1000": "rate = cases × 1000/population",
    "doubling_a_small_risk": "relative = (k − 1) × 100%; absolute = a(k − 1)/n × 100",
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


def frac_percent(fr):
    pct_value = Fraction(fr) * 100
    whole, remainder = divmod(pct_value.numerator, pct_value.denominator)
    remainder = Fraction(remainder, pct_value.denominator)
    if remainder == 0:
        return f"{whole}%"
    try:
        return dec(pct_value) + "%"
    except AssertionError:
        return f"{whole} {remainder.numerator}/{remainder.denominator}%"


def clean(problem):
    return re.sub(r"^An unrelated notice lists \d+ archived forms\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"Without treatment the risk of a condition is (\d+) in (\d+); "
        r"with treatment it is (\d+) in (\d+)", text)
    if match:
        a, n, b, n2 = map(int, match.groups())
        assert n == n2, text
        rrr, arr_pp = Fraction(a - b, a), Fraction(a - b, n) * 100
        answer = (f"relative {frac_percent(rrr)}; absolute {dec(arr_pp)} "
                 "percentage points")
        return "relative_vs_absolute", answer

    match = re.search(r"A reported rate rises from (\d+)% to (\d+)%", text)
    if match:
        p1, p2 = map(int, match.groups())
        delta = p2 - p1
        pct_change = dec(Fraction(delta, p1) * 100)
        return ("percent_vs_percentage_points",
                f"{delta} percentage points; {pct_change}% percent change")

    match = re.search(r"A treatment reduces absolute risk by (\d+)%", text)
    if match:
        arr_pct = int(match.group(1))
        assert 100 % arr_pct == 0, text
        return "nnt", f"{100 // arr_pct} people"

    match = re.search(
        r"Place 1 recorded (\d+) cases among (\d+) people\. Place 2 recorded "
        r"(\d+) cases among (\d+) people", text)
    if match:
        cases1, pop1, cases2, pop2 = map(int, match.groups())
        rate1, rate2 = Fraction(cases1 * 1000, pop1), Fraction(cases2 * 1000, pop2)
        higher = 1 if rate1 > rate2 else 2
        hi_rate, lo_rate = (rate1, rate2) if higher == 1 else (rate2, rate1)
        hi_cases = cases1 if higher == 1 else cases2
        lo_cases = cases2 if higher == 1 else cases1
        note = "despite fewer raw cases" if hi_cases < lo_cases else "and more raw cases"
        answer = (f"place {higher} higher ({dec(hi_rate)} vs {dec(lo_rate)} "
                 f"per 1000) {note}")
        return "per_capita_vs_raw", answer

    match = re.search(
        r"A community recorded (\d+) cases among (\d+) people", text)
    if match:
        cases, pop = map(int, match.groups())
        rate = Fraction(cases * 1000, pop)
        return "rate_per_1000", f"{dec(rate)} per 1000"

    match = re.search(
        r"A rare condition's risk (doubles|triples|quadruples|"
        r"increases fivefold) from (\d+) in (\d+) to (\d+) in (\d+)", text)
    if match:
        word, a, n, new, n2 = match.groups()
        a, n, new, n2 = int(a), int(n), int(new), int(n2)
        assert n == n2, text
        k = MULTIPLIER_WORD_TO_K[word]
        assert new == a * k, text
        relative = (k - 1) * 100
        abs_pp = Fraction(new - a, n) * 100
        answer = f"relative +{relative}%; absolute +{dec(abs_pp)} percentage points"
        return "doubling_a_small_risk", answer

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer = solve(problem)
    model = MODELS[variant]
    return variant, (f"{model}; {answer}" if modifier == "with_model" else answer), model


class TestRiskCommunicationGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(360)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = RiskCommunicationGenerator(variant, modifier).generate()
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
            "relative_vs_absolute": (
                "Without treatment the risk of a condition is 3 in 1000; "
                "with treatment it is 2 in 1000.",
                "State the relative risk reduction and the absolute risk reduction."),
            "percent_vs_percentage_points": (
                "A reported rate rises from 8% to 10%.",
                "State the change in percentage points and the percent change."),
            "nnt": (
                "A treatment reduces absolute risk by 5%.",
                "How many patients must be treated to prevent one additional "
                "bad outcome?"),
            "per_capita_vs_raw": (
                "Place 1 recorded 30 cases among 12000 people. Place 2 "
                "recorded 50 cases among 25000 people.",
                "Which place has the higher case rate per 1000 people?"),
            "rate_per_1000": (
                "A community recorded 45 cases among 9000 people.",
                "What is the case rate per 1000 people?"),
            "doubling_a_small_risk": (
                "A rare condition's risk doubles from 1 in 5000 to 2 in 5000.",
                "State the relative risk change and the absolute risk change."),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_relative_vs_absolute_matches_the_plans_worked_example(self):
        self.assertEqual(
            solve("Without treatment the risk of a condition is 3 in 1000; "
                  "with treatment it is 2 in 1000. State the relative risk "
                  "reduction and the absolute risk reduction."),
            ("relative_vs_absolute",
             "relative 33 1/3%; absolute 0.1 percentage points"))

    def test_nnt_matches_the_plans_worked_example(self):
        self.assertEqual(
            solve("A treatment reduces absolute risk by 5%. How many "
                  "patients must be treated to prevent one additional bad "
                  "outcome?"),
            ("nnt", "20 people"))

    def test_per_capita_vs_raw_matches_the_plans_worked_example(self):
        self.assertEqual(
            solve("Place 1 recorded 30 cases among 12000 people. Place 2 "
                  "recorded 50 cases among 25000 people. Which place has "
                  "the higher case rate per 1000 people?"),
            ("per_capita_vs_raw",
             "place 1 higher (2.5 vs 2 per 1000) despite fewer raw cases"))

    def test_per_capita_vs_raw_always_reverses(self):
        random.seed(361)
        for _ in range(200):
            result = RiskCommunicationGenerator("per_capita_vs_raw").generate()
            self.assertIn("despite fewer raw cases", result["final_answer"])

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(362)
        for _ in range(700):
            result = RiskCommunicationGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "CMP":
                    x, y = Fraction(fields[1]), Fraction(fields[2])
                    self.assertEqual(fields[3], ">" if x > y else "<", raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(363)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = RiskCommunicationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_risk_communication_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            RiskCommunicationGenerator("bogus")
        with self.assertRaises(ValueError):
            RiskCommunicationGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(364)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = RiskCommunicationGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = RiskCommunicationGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
