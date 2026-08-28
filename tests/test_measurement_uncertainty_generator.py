"""Problem-text-only oracles for MeasurementUncertaintyGenerator."""
import random
import re
import unittest
from fractions import Fraction

from generators.measurement_uncertainty_generator import (
    APPLIED, FRAMES, MODIFIERS, VARIANTS, MeasurementUncertaintyGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("%", "").rstrip("."))


def exact_text(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return str(value.numerator) if value.denominator == 1 else str(value)
    scaled, places = value, 0
    while scaled.denominator != 1:
        scaled *= 10
        places += 1
    if places == 0:
        return str(scaled.numerator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    rendered = (digits[:-places] + "." + digits[-places:]).rstrip("0").rstrip(".")
    return sign + rendered


def interval(low, high):
    return f"[{exact_text(low)}, {exact_text(high)}]"


def clean(problem):
    return re.sub(r"^A nearby cabinet holds \d+ spare clips\. ", "", problem)


def solve(problem):
    text = clean(problem)

    match = re.search(
        r"target is ([0-9.]+) ± ([0-9.]+) (cm|g|mL), and a part measures "
        r"([0-9.]+) \3", text, re.I)
    if match:
        nominal, tolerance = map(number, match.groups()[:2])
        unit_name, measured = match.group(3), number(match.group(4))
        difference = abs(measured - nominal)
        inside = difference <= tolerance
        symbol = "≤" if inside else ">"
        verdict = "within tolerance" if inside else "outside tolerance"
        answer = (f"{verdict}; difference {exact_text(difference)} {unit_name} "
                  f"{symbol} {exact_text(tolerance)} {unit_name}")
        model = (f"abs({exact_text(measured)} − {exact_text(nominal)}) = "
                 f"{exact_text(difference)} {symbol} {exact_text(tolerance)}")
        return "within_tolerance", answer, model, difference, verdict

    match = re.search(
        r"part is specified as ([0-9.]+) ± ([0-9.]+) (cm|g|mL)", text,
        re.I)
    if match:
        nominal, tolerance = map(number, match.groups()[:2])
        unit_name = match.group(3)
        low, high = nominal - tolerance, nominal + tolerance
        answer = f"{exact_text(low)} {unit_name} to {exact_text(high)} {unit_name}"
        model = f"x ∈ {interval(low, high)} {unit_name}"
        return "tolerance_interval", answer, model, nominal, unit_name

    match = re.search(
        r"rectangle measures ([0-9.]+) ± ([0-9.]+) cm by ([0-9.]+) ± "
        r"([0-9.]+) cm", text, re.I)
    if match:
        length, length_u, width, width_u = map(number, match.groups())
        ll, lh = length - length_u, length + length_u
        wl, wh = width - width_u, width + width_u
        low, high = ll * wl, lh * wh
        nominal = length * width
        answer = f"{exact_text(low)} cm² to {exact_text(high)} cm²"
        model = (f"A ∈ [{exact_text(ll)} × {exact_text(wl)}, "
                 f"{exact_text(lh)} × {exact_text(wh)}]")
        return "area_from_measured_sides", answer, model, nominal, None

    match = re.search(
        r"Two lengths are ([0-9.]+) ± ([0-9.]+) cm and ([0-9.]+) ± "
        r"([0-9.]+) cm\. The second is (added to|subtracted from) the first",
        text, re.I)
    if match:
        first, first_u, second, second_u = map(number, match.groups()[:4])
        action = match.group(5).lower()
        fl, fh = first - first_u, first + first_u
        sl, sh = second - second_u, second + second_u
        total_u = first_u + second_u
        if action == "added to":
            nominal, low, high = first + second, fl + sl, fh + sh
            symbol, category = "+", "sum"
        else:
            nominal, low, high = first - second, fl - sh, fh - sl
            symbol, category = "−", "difference"
        answer = (f"{exact_text(nominal)} ± {exact_text(total_u)} cm; "
                  f"{exact_text(low)} cm to {exact_text(high)} cm")
        model = (f"({exact_text(first)} ± {exact_text(first_u)}) {symbol} "
                 f"({exact_text(second)} ± {exact_text(second_u)})")
        return "sum_difference_propagation", answer, model, nominal, category

    match = re.search(
        r"reference value is ([0-9.]+) g, while a measurement gives "
        r"([0-9.]+) g", text, re.I)
    if match:
        true_value, measured = map(number, match.groups())
        percent = abs(measured - true_value) / true_value * 100
        answer = f"{exact_text(percent)}%"
        model = (f"abs({exact_text(measured)} − {exact_text(true_value)})/"
                 f"{exact_text(true_value)} × 100 = {exact_text(percent)}%")
        return "percent_error", answer, model, percent, None

    multiply = re.search(
        r"result uses (\d+) cm by (\d+) cm\. Their percentage uncertainties "
        r"are (\d+)% and (\d+)%", text, re.I)
    divide = re.search(
        r"result uses (\d+) m over (\d+) s\. Their percentage uncertainties "
        r"are (\d+)% and (\d+)%", text, re.I)
    if multiply or divide:
        match = multiply or divide
        first, second, first_pct, second_pct = map(int, match.groups())
        combined = first_pct + second_pct
        if multiply:
            value, symbol, unit_name, category = Fraction(first * second), "×", "cm²", "multiply"
        else:
            value, symbol, unit_name, category = Fraction(first, second), "÷", "m/s", "divide"
        absolute = value * Fraction(combined, 100)
        answer = (f"{exact_text(value)} ± {exact_text(absolute)} {unit_name} "
                  f"({combined}%)")
        model = (f"{first} {symbol} {second} = {exact_text(value)}; "
                 f"u = {combined}% × {exact_text(value)}")
        return "relative_uncertainty_rule", answer, model, value, category

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestMeasurementUncertaintyGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(308)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = MeasurementUncertaintyGenerator(variant, modifier).generate()
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
        examples = {
            "tolerance_interval": "A part is specified as 10 ± 0.5 cm.",
            "within_tolerance": "A target is 10 ± 0.5 cm, and a part measures 10.4 cm.",
            "sum_difference_propagation": (
                "Two lengths are 12 ± 0.2 cm and 3 ± 0.1 cm. The second is "
                "subtracted from the first."),
            "area_from_measured_sides": (
                "A rectangle measures 12.5 ± 0.2 cm by 8 ± 0.1 cm."),
            "percent_error": "A reference value is 10 g, while a measurement gives 9.8 g.",
            "relative_uncertainty_rule": (
                "A result uses 12 cm by 8 cm. Their percentage uncertainties "
                "are 2% and 3%. For this report, add the percentage uncertainties "
                "for multiplication or division."),
        }
        question = "Give the exact uncertainty result."
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_both_verdicts_and_operation_branches(self):
        random.seed(309)
        verdicts, propagation, relative = set(), set(), set()
        for _ in range(400):
            verdicts.add(solve(MeasurementUncertaintyGenerator(
                "within_tolerance", "plain").generate()["problem"])[4])
            propagation.add(solve(MeasurementUncertaintyGenerator(
                "sum_difference_propagation", "plain").generate()["problem"])[4])
            relative.add(solve(MeasurementUncertaintyGenerator(
                "relative_uncertainty_rule", "plain").generate()["problem"])[4])
        self.assertEqual(verdicts, {"within tolerance", "outside tolerance"})
        self.assertEqual(propagation, {"sum", "difference"})
        self.assertEqual(relative, {"multiply", "divide"})

    def test_arithmetic_steps(self):
        random.seed(310)
        for _ in range(1500):
            result = MeasurementUncertaintyGenerator().generate()
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

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(311)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MeasurementUncertaintyGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_measurement_uncertainty_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            MeasurementUncertaintyGenerator("bogus")
        with self.assertRaises(ValueError):
            MeasurementUncertaintyGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(312)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = MeasurementUncertaintyGenerator().generate()
            self.assertNotIn(DELIM, result["problem"])
            self.assertNotIn(DELIM, result["final_answer"])
            joined = " ".join((result["problem"], result["final_answer"], *result["steps"]))
            for fragment in banned:
                self.assertNotIn(fragment, joined.lower())
            for raw in result["steps"]:
                self.assertLessEqual(len(raw.split(DELIM)) - 1, 4, raw)


if __name__ == "__main__":
    unittest.main()
