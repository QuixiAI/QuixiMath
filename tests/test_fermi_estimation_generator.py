"""Problem-text-only oracles for the extended Fermi estimate generator."""
import random
import re
import unittest

from generators.fermi_estimation_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, FermiEstimationGenerator,
)
from helpers import DELIM


def sig2(n):
    exponent = len(str(n)) - 1
    if exponent <= 1:
        return str(n)
    place = 10 ** (exponent - 1)
    q, remainder = divmod(n, place)
    q += remainder * 2 >= place
    if q == 100:
        q, exponent = 10, exponent + 1
    mantissa = str(q // 10) if q % 10 == 0 else f"{q // 10}.{q % 10}"
    return f"{mantissa} × 10^{exponent}"


def clean(problem):
    return re.sub(r"^A nearby notice lists \d+ empty bins\. ", "", problem)


def solved(variant, product, units, model):
    return variant, f"{sig2(product)} {units}", model, product, None


def solve(problem):
    text = clean(problem)
    patterns = (
        ("water_use", r"town has (\d+) people using (\d+) gallons", "gallons/day"),
        ("stadium", r"stadium has (\d+) sections, (\d+) rows per section, and (\d+) seats", "seats"),
        ("cafeteria", r"school has (\d+) students eating (\d+) pizza slices per week for (\d+) weeks", "slices/year"),
        ("household_water", r"household has (\d+) people using (\d+) liters per person per day for (\d+) days", "liters/month"),
        ("city_buses", r"city runs (\d+) buses making (\d+) trips per day with (\d+) riders", "rides/day"),
        ("school_lunches", r"district serves (\d+) students for (\d+) days at (\d+) lunch(?:es)?", "lunches/year"),
        ("book_pages", r"print run has (\d+) titles, (\d+) pages per title, and (\d+) cop(?:y|ies)", "pages"),
        ("waste_bags", r"community has (\d+) households producing (\d+) waste bags each week for (\d+) weeks", "bags/year"),
    )
    for variant, pattern, units in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            values = list(map(int, match.groups()))
            product = 1
            for value in values:
                product *= value
            return solved(variant, product, units,
                          f"{' × '.join(map(str, values))} = {product} {units}")

    match = re.search(r"trip covers (\d+) km at (\d+) km per liter", text, re.I)
    if match:
        distance, rate = map(int, match.groups())
        liters = distance // rate
        return solved("road_trip_fuel", liters, "liters",
                      f"{distance} ÷ {rate} = {liters} liters")

    match = re.search(
        r"at most (\d+) households, (\d+) bags per household each week, and "
        r"(\d+) weeks\. A claim gives 10\^(\d+)", text, re.I)
    if match:
        households, bags, weeks, claim_power = map(int, match.groups())
        upper = households * bags * weeks
        claim = 10 ** claim_power
        plausible = claim <= upper
        verdict = "plausible" if plausible else "implausible"
        answer = (f"{verdict}; claim 10^{claim_power}; upper bound "
                  f"{sig2(upper)} bags/year")
        model = f"upper = {households} × {bags} × {weeks} = {upper}"
        return "bound_check", answer, model, upper, verdict

    match = re.search(
        r"Estimate A uses (\d+) schools with (\d+) people each\. Estimate B "
        r"uses (\d+) neighborhoods with (\d+) households each and (\d+) people",
        text, re.I)
    if match:
        a, b, c, d, e = map(int, match.groups())
        first, second = a * b, c * d * e
        choice = "estimate A" if first > second else "estimate B"
        answer = f"{choice}; A {sig2(first)} people; B {sig2(second)} people"
        model = f"A={a} × {b}; B={c} × {d} × {e}"
        return "compare_two_estimates", answer, model, max(first, second), choice
    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestFermiEstimationGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(313)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(14):
                    result = FermiEstimationGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model, _, _ = expected(result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer, result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1], model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        facts = {
            "water_use": "A town has 12000 people using 80 gallons per person each day.",
            "stadium": "A stadium has 24 sections, 20 rows per section, and 18 seats per row.",
            "cafeteria": "A school has 600 students eating 2 pizza slices per week for 40 weeks.",
            "household_water": "A household has 4 people using 100 liters per person per day for 30 days.",
            "city_buses": "A city runs 80 buses making 10 trips per day with 30 riders per trip.",
            "school_lunches": "A district serves 600 students for 180 days at 1 lunch per student per day.",
            "book_pages": "A print run has 240 titles, 300 pages per title, and 2 copies of each.",
            "road_trip_fuel": "A trip covers 600 km at 12 km per liter.",
            "waste_bags": "A community has 2400 households producing 3 waste bags each week for 52 weeks.",
            "bound_check": "A region has at most 20000 households, 3 bags per household each week, and 52 weeks. A claim gives 10^9 bags per year.",
            "compare_two_estimates": "Estimate A uses 20 schools with 500 people each. Estimate B uses 40 neighborhoods with 100 households each and 3 people per household.",
        }
        for variant, text in facts.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=text, question="Give the estimate.",
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_bound_verdicts_and_comparison_choices(self):
        random.seed(314)
        verdicts, choices = set(), set()
        for _ in range(400):
            verdicts.add(solve(FermiEstimationGenerator(
                "bound_check", "plain").generate()["problem"])[4])
            choices.add(solve(FermiEstimationGenerator(
                "compare_two_estimates", "plain").generate()["problem"])[4])
        self.assertEqual(verdicts, {"plausible", "implausible"})
        self.assertEqual(choices, {"estimate A", "estimate B"})

    def test_arithmetic_and_rounding_steps(self):
        random.seed(315)
        for _ in range(1600):
            result = FermiEstimationGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]), int(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]), int(fields[3]), raw)
                elif fields[0] == "SIGFIG_ROUND":
                    self.assertEqual(sig2(int(fields[1])), fields[3], raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(316)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = FermiEstimationGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_fermi_estimation_{variant}_{modifier}")
                if modifier == "distractor": self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model": self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError): FermiEstimationGenerator("bogus")
        with self.assertRaises(ValueError): FermiEstimationGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(317)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(800):
            result = FermiEstimationGenerator().generate()
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            self.assertNotIn(DELIM, result["problem"])
            for fragment in banned: self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]: self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
