"""Problem-text-only oracles for :class:`SignificantFiguresGenerator`."""
import random
import re
import unittest
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from generators.significant_figures_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    SignificantFiguresGenerator,
)
from helpers import DELIM


def number(token):
    text = token.replace("$", "").rstrip(".")
    return Fraction(text) if "/" in text else Fraction(Decimal(text))


def exact_text(value):
    value = Fraction(value)
    denominator = value.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    if denominator != 1:
        return (str(value.numerator) if value.denominator == 1 else
                f"{value.numerator}/{value.denominator}")
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


def sig_count(token):
    text = token.strip().lstrip("+-")
    if "×" in text:
        text = text.split("×", 1)[0].strip()
    if "." in text:
        return len(text.replace(".", "").lstrip("0"))
    return len(text.lstrip("0").rstrip("0"))


def round_sig(value, count):
    value = Decimal(value)
    exponent = value.adjusted() - count + 1
    quantum = Decimal(f"1e{exponent}")
    rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
    places = max(0, count - rounded.adjusted() - 1)
    return f"{rounded:.{places}f}"


def clean(problem):
    return re.sub(r"^A nearby shelf holds \d+ sealed vials\. ", "", problem)


def solve(problem):
    """Parse the displayed precision rule and recompute its exact answer."""
    text = clean(problem)

    match = re.search(
        r"measurement is written as ([0-9.]+) × 10\^(-\d+) (m|g|L)", text,
        re.I)
    if match:
        mantissa, exponent_token, unit_name = match.groups()
        exponent = int(exponent_token)
        count = sig_count(mantissa)
        ordinary_decimal = Decimal(mantissa) * (Decimal(10) ** exponent)
        ordinary = format(ordinary_decimal, "f")
        answer = f"{count} significant figures; {ordinary} {unit_name}"
        model = f"{mantissa} × 10^{exponent} = {ordinary} {unit_name}"
        return "scientific_notation_measurement", answer, model, Fraction(ordinary_decimal), (count, unit_name)

    match = re.search(r"measurement is written as ([0-9.]+)\.", text, re.I)
    if match:
        token = match.group(1)
        count = sig_count(token)
        answer = str(count)
        model = f"significant-digit count({token}) = {count}"
        if token.startswith("0."):
            family = "leading"
        elif re.fullmatch(r"\d+\.0+", token):
            family = "whole_decimal"
        else:
            family = "decimal"
        return "count_sig_figs", answer, model, Fraction(count), family

    value_match = re.search(r"measured value is ([0-9.]+) cm", text, re.I)
    target_match = re.search(r"Report it to (\d+) significant", text, re.I)
    if value_match and target_match:
        token, count_token = value_match.group(1), target_match.group(1)
        count = int(count_token)
        rounded = round_sig(Decimal(token), count)
        answer = f"{rounded} cm"
        model = f"{token} cm → {rounded} cm ({count} significant figures)"
        return "round_to_sig_figs", answer, model, number(rounded), None

    multiply_match = re.search(
        r"measurements give ([0-9.]+) cm × ([0-9.]+) cm\. When "
        r"multiplying measurements", text, re.I)
    divide_match = re.search(
        r"measurements give ([0-9.]+) m ÷ ([0-9.]+) s\. When "
        r"dividing measurements", text, re.I)
    if multiply_match or divide_match:
        match = multiply_match or divide_match
        first, second = match.groups()
        symbol = "×" if multiply_match else "÷"
        first_value, second_value = Decimal(first), Decimal(second)
        if symbol == "×":
            raw = first_value * second_value
            unit_name = "cm²"
        else:
            raw = first_value / second_value
            unit_name = "m/s"
        target = min(sig_count(first), sig_count(second))
        rounded = round_sig(raw, target)
        answer = f"{rounded} {unit_name}"
        model = f"{first} {symbol} {second} → {rounded} {unit_name}"
        return "multiply_divide_rule", answer, model, number(rounded), symbol

    match = re.search(
        r"measurements give ([0-9.]+) ([+−]) ([0-9.]+) g\. When "
        r"(adding|subtracting) measurements", text, re.I)
    if match:
        first, symbol, second, verb = match.groups()
        first_value, second_value = Decimal(first), Decimal(second)
        if symbol == "+":
            raw, expected_verb = first_value + second_value, "adding"
        else:
            raw, expected_verb = first_value - second_value, "subtracting"
        if verb.lower() != expected_verb:
            raise AssertionError("stated decimal rule mismatches operation")
        places = min(len(first.split(".")[1]), len(second.split(".")[1]))
        quantum = Decimal(1).scaleb(-places)
        rounded = raw.quantize(quantum, rounding=ROUND_HALF_UP)
        rounded_text = f"{rounded:.{places}f}"
        answer = f"{rounded_text} g"
        model = f"{first} {symbol} {second} → {rounded_text} g"
        return "add_subtract_rule", answer, model, number(rounded_text), symbol

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestSignificantFiguresGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(303)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(28):
                    result = SignificantFiguresGenerator(variant, modifier).generate()
                    self.assertEqual(result["steps"][-1],
                                     f"Z{DELIM}{result['final_answer']}")
                    parsed, answer, model, _, _ = expected(
                        result["problem"], modifier)
                    self.assertEqual(parsed, variant)
                    self.assertEqual(result["final_answer"], answer,
                                     result["problem"])
                    if modifier == "with_model":
                        self.assertEqual(result["steps"][0].split(DELIM)[1],
                                         model)
                    seen.add((variant, modifier))
        self.assertEqual(seen, {(v, m) for v in VARIANTS for m in MODIFIERS})

    def test_all_five_renderings_invert_every_variant(self):
        examples = {
            "count_sig_figs": "A measurement is written as 0.004500.",
            "round_to_sig_figs": "A measured value is 8.55 cm.",
            "multiply_divide_rule": (
                "Two measurements give 2.5 cm × 3.42 cm. When multiplying "
                "measurements, report the result to the fewer significant "
                "figures shown by either input."),
            "add_subtract_rule": (
                "Two measurements give 3.70 + 6.9 g. When adding measurements, "
                "report to the fewest decimal places shown by either input."),
            "scientific_notation_measurement": (
                "A measurement is written as 4.500 × 10^-3 m."),
        }
        questions = {
            "count_sig_figs": "How many significant figures are displayed?",
            "round_to_sig_figs": "Report it to 2 significant figures.",
            "multiply_divide_rule": "What reported result follows?",
            "add_subtract_rule": "What reported result follows?",
            "scientific_notation_measurement": (
                "How many significant figures are shown, and what is the "
                "ordinary decimal form?"),
        }
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=questions[variant],
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_all_rule_families_and_scientific_shapes_reachable(self):
        random.seed(304)
        count_families, mult_div, add_sub, units, counts = (set() for _ in range(5))
        for _ in range(500):
            count_families.add(solve(SignificantFiguresGenerator(
                "count_sig_figs", "plain").generate()["problem"])[4])
            mult_div.add(solve(SignificantFiguresGenerator(
                "multiply_divide_rule", "plain").generate()["problem"])[4])
            add_sub.add(solve(SignificantFiguresGenerator(
                "add_subtract_rule", "plain").generate()["problem"])[4])
            count, unit_name = solve(SignificantFiguresGenerator(
                "scientific_notation_measurement", "plain").generate()["problem"])[4]
            counts.add(count)
            units.add(unit_name)
        self.assertEqual(count_families, {"leading", "decimal", "whole_decimal"})
        self.assertEqual(mult_div, {"×", "÷"})
        self.assertEqual(add_sub, {"+", "−"})
        self.assertEqual(units, {"m", "g", "L"})
        self.assertEqual(counts, {3, 4, 5, 6})

    def test_arithmetic_and_precision_steps(self):
        random.seed(305)
        for _ in range(1400):
            result = SignificantFiguresGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "S":
                    self.assertEqual(number(fields[1]) - number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "M":
                    self.assertEqual(number(fields[1]) * number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "D":
                    self.assertEqual(number(fields[1]) / number(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "E":
                    self.assertEqual(number(fields[1]) ** int(fields[2]),
                                     number(fields[3]), raw)
                elif fields[0] == "ROUND_SF":
                    raw_value = number(fields[1])
                    raw_decimal = (Decimal(raw_value.numerator) /
                                   Decimal(raw_value.denominator))
                    self.assertEqual(round_sig(raw_decimal, int(fields[2])),
                                     fields[3], raw)
                elif fields[0] == "SIGFIG":
                    self.assertEqual(sig_count(fields[1]), int(fields[2]), raw)

    def test_modifier_shapes_and_invalid_inputs(self):
        random.seed(306)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = SignificantFiguresGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(result["operation"],
                                 f"applied_significant_figures_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            SignificantFiguresGenerator("bogus")
        with self.assertRaises(ValueError):
            SignificantFiguresGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(307)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = SignificantFiguresGenerator().generate()
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
