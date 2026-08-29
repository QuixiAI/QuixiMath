"""Problem-text-only brute-force oracles for IndexAndGrowthGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.index_and_growth_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, IndexAndGrowthGenerator,
)
from helpers import DELIM

MODELS = {
    "index_number": "step percent = (new − old)/old",
    "percent_change_vs_points": "points = p2 − p1; percent = (p2 − p1)/p1",
    "cagr_perfect_power": "rate = (end/start)^(1/years) − 1",
    "real_vs_nominal_supplied_cpi": "real = 100(100 + nominal)/(100 + inflation) − 100",
    "log_scale_reading": "factor = 10^(number of major ticks)",
    "repeated_doubling": "doublings = years/period; factor = 2^doublings",
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


def clean(problem):
    return re.sub(r"^An unrelated ledger lists \d+ filed reports\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(r"price index changes from (-?\d+) to (-?\d+), then "
                      r"to (-?\d+)", text)
    if match:
        i0, i1, i2 = map(int, match.groups())
        pct1 = Fraction(i1 - i0, i0) * 100
        pct2 = Fraction(i2 - i1, i1) * 100
        return "index_number", f"{dec(pct1)}%; {dec(pct2)}%"

    match = re.search(r"inflation rate goes from (\d+)% to (-?\d+)% year over year", text)
    if match:
        p1, p2 = map(int, match.groups())
        delta = p2 - p1
        pct_change = dec(Fraction(delta, p1) * 100)
        return ("percent_change_vs_points",
                f"{delta} percentage points; {pct_change}% percent change")

    match = re.search(r"grows from (\d+) to (\d+) over (\d+) years", text)
    if match:
        v0, v1, t = map(int, match.groups())
        ratio = Fraction(v1, v0)
        root = _integer_root(ratio, t)
        return "cagr_perfect_power", f"{dec((root - 1) * 100)}% per year"

    match = re.search(r"wage rises (-?\d+)% nominally while inflation "
                      r"\(CPI\) for the year is (-?\d+)%", text)
    if match:
        nominal, inflation = map(int, match.groups())
        real_pct = Fraction(100 * (100 + nominal), 100 + inflation) - 100
        return "real_vs_nominal_supplied_cpi", f"{dec(real_pct)}%"

    match = re.search(r"log-10 axis (rises|falls) (\d+) major tick", text)
    if match:
        direction, n = match.group(1), int(match.group(2))
        multiplier = 10 ** n
        arrow = f"×{multiplier}" if direction == "rises" else f"÷{multiplier}"
        return "log_scale_reading", arrow

    period_match = re.search(r"doubles every (\d+) years", text)
    years_match = re.search(r"Over (\d+) years", text)
    if period_match and years_match:
        period, years = int(period_match.group(1)), int(years_match.group(1))
        assert years % period == 0, text
        k = years // period
        return "repeated_doubling", f"{k} times; ×{2 ** k}"

    raise AssertionError(f"unrecognized problem: {problem}")


def _iroot(x, t):
    """Exact integer t-th root of ``x`` via binary search (0 if it is not
    a perfect t-th power — callers verify)."""
    if x == 0:
        return 0
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** t <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def _integer_root(ratio, t):
    """The unique positive rational r with r**t == ratio (the generator
    only ever constructs perfect t-th powers, numerator and denominator
    each a perfect t-th power in lowest terms)."""
    p, q = _iroot(ratio.numerator, t), _iroot(ratio.denominator, t)
    assert p ** t == ratio.numerator and q ** t == ratio.denominator, (ratio, t)
    return Fraction(p, q)


def expected(problem, variant, modifier):
    parsed_variant, answer = solve(problem)
    model = MODELS[variant]
    return parsed_variant, (f"{model}; {answer}" if modifier == "with_model" else answer)


class TestIndexAndGrowthGenerator(unittest.TestCase):
    def test_marker_contract_and_full_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(390)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = IndexAndGrowthGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1], f"Z{DELIM}{result['final_answer']}")
                    parsed, answer = expected(result["problem"], variant, modifier)
                    self.assertEqual(parsed, variant, result["problem"])
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], MODELS[variant])
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_plans_worked_examples(self):
        self.assertEqual(
            solve("A price index changes from 100 to 125, then to 150. "
                  "What is the percent change in each step?"),
            ("index_number", "25%; 20%"))
        self.assertEqual(
            solve("A subscriber count grows from 100 to 144 over 2 years. "
                  "What is the annual growth rate?"),
            ("cagr_perfect_power", "20% per year"))
        self.assertEqual(
            solve("A curve on a log-10 axis rises 2 major ticks. By what "
                  "factor did the underlying value change?"),
            ("log_scale_reading", "×100"))

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "index_number": (
                "A price index changes from 100 to 125, then to 150.",
                "What is the percent change in each step?"),
            "percent_change_vs_points": (
                "An inflation rate goes from 4% to 6% year over year.",
                "What is the change in percentage points, and what is the "
                "percent change in the rate itself?"),
            "cagr_perfect_power": (
                "A population grows from 100 to 144 over 2 years.",
                "What is the annual growth rate?"),
            "real_vs_nominal_supplied_cpi": (
                "A wage rises 5% nominally while inflation (CPI) for the "
                "year is 25%.",
                "What is the exact real (inflation-adjusted) percent change?"),
            "log_scale_reading": (
                "A curve on a log-10 axis rises 2 major ticks.",
                "By what factor did the underlying value change?"),
            "repeated_doubling": (
                "A population doubles every 10 years.",
                "Over 30 years, how many times does it double, and what "
                "is the total growth factor?"),
        }
        for variant, (facts, question) in examples.items():
            for frame in FRAMES:
                problem = frame.format(place="the market stand", name="Ari",
                                       facts=facts, question=question)
                self.assertEqual(solve(problem)[0], variant, problem)

    def test_arithmetic_inside_emitted_steps(self):
        random.seed(391)
        for _ in range(700):
            result = IndexAndGrowthGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]), int(fields[3]), raw)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0, raw)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]), int(fields[3]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(392)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = IndexAndGrowthGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_index_and_growth_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            IndexAndGrowthGenerator("bogus")
        with self.assertRaises(ValueError):
            IndexAndGrowthGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(393)
        banned = ("1x", "-1x", "^1", "--", "the the", "e+")
        for _ in range(700):
            result = IndexAndGrowthGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)

    def test_determinism_under_seed(self):
        random.seed(23)
        gen = IndexAndGrowthGenerator()
        first = [gen.generate()["problem"] for _ in range(30)]
        random.seed(23)
        second = [gen.generate()["problem"] for _ in range(30)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
