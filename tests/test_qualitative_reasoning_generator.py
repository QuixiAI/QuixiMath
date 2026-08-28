"""Problem-text-only oracles for :class:`QualitativeReasoningGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.qualitative_reasoning_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    QualitativeReasoningGenerator,
)
from helpers import DELIM


def number(token):
    return Fraction(token.replace("$", "").replace("%", "").rstrip("."))


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


def money_text(value):
    cents = Fraction(value) * 100
    if cents.denominator != 1:
        raise AssertionError(f"not exact cents: {value}")
    return f"${cents.numerator // 100}.{cents.numerator % 100:02d}"


def unit_text(value, name):
    value = Fraction(value)
    text = exact_text(value)
    if name in ("m²", "m³") or "/" in name:
        return f"{text} {name}"
    return f"{text} {name if abs(value) == 1 else name + 's'}"


def clean(problem):
    return re.sub(r"^A nearby cabinet contains \d+ old folders\. ", "", problem)


def solve(problem):
    """Infer the qualitative result and verify it by exact evaluation."""
    text = clean(problem)

    match = re.search(r"outputs at input n are n² and (\d+)n", text, re.I)
    if match:
        coefficient = int(match.group(1))
        check_n = 2 * coefficient
        square = check_n ** 2
        multiple = coefficient * check_n
        answer = (f"n²; larger for n > {coefficient} (at n = {check_n}: "
                  f"{square} vs {multiple})")
        model = f"n² > {coefficient}n when n > {coefficient}"
        return "dominant_term", answer, model, Fraction(coefficient), None

    match = re.search(
        r"ratio is \((\d+)n \+ (\d+)\)/\(n \+ (\d+)\).*?check uses n = "
        r"(\d+)", text, re.I)
    if match:
        leading, offset, denominator_offset, check_n = map(int, match.groups())
        numerator = leading * check_n + offset
        denominator = check_n + denominator_offset
        value = Fraction(numerator, denominator)
        approximation = f"{float(value):.3f}"
        expression = f"({leading}n + {offset})/(n + {denominator_offset})"
        answer = (f"{leading}; at n = {check_n}, {numerator}/{denominator} "
                  f"≈ {approximation}")
        model = f"{expression} → {leading} as n grows"
        return "limiting_value", answer, model, Fraction(leading), None

    match = re.search(
        r"account starts with (\$[0-9.]+).*?Over (\d+) years, the annual "
        r"change shifts from (\d+)% to (\d+)%", text, re.I)
    if match:
        principal = number(match.group(1))
        years, first_rate, second_rate = map(int, match.groups()[1:])
        first = principal * Fraction(100 + first_rate, 100) ** years
        second = principal * Fraction(100 + second_rate, 100) ** years
        direction = "increases" if second > first else "decreases"
        answer = (f"{direction}; {money_text(first)} → {money_text(second)} "
                  f"when the annual change goes {first_rate}% → {second_rate}%")
        model = (f"A1={exact_text(principal)}*(1+{first_rate}/100)^{years}; "
                 f"A2={exact_text(principal)}*(1+{second_rate}/100)^{years}")
        return "direction_of_change", answer, model, second, direction

    match = re.search(
        r"square garden changes from side length (\d+) m to side length (\d+) m",
        text, re.I)
    if match:
        old, new = map(int, match.groups())
        old_value, new_value = old ** 2, new ** 2
        factor = Fraction(new_value, old_value)
        effect = f"multiplies by {exact_text(factor)}"
        answer = (f"{effect}; {unit_text(old_value, 'm²')} → "
                  f"{unit_text(new_value, 'm²')}")
        model = f"q1={old}²={old_value}; q2={new}²={new_value}"
        return "doubling_effect_in_formula", answer, model, Fraction(new_value), "square"

    match = re.search(
        r"cube-shaped tank changes from edge length (\d+) m to edge length "
        r"(\d+) m", text, re.I)
    if match:
        old, new = map(int, match.groups())
        old_value, new_value = old ** 3, new ** 3
        factor = Fraction(new_value, old_value)
        effect = f"multiplies by {exact_text(factor)}"
        answer = (f"{effect}; {unit_text(old_value, 'm³')} → "
                  f"{unit_text(new_value, 'm³')}")
        model = f"q1={old}³={old_value}; q2={new}³={new_value}"
        return "doubling_effect_in_formula", answer, model, Fraction(new_value), "cube"

    match = re.search(
        r"vehicle covers a fixed (\d+) km route.*?speed changes from (\d+) "
        r"km/h to (\d+) km/h", text, re.I)
    if match:
        distance, old, new = map(int, match.groups())
        old_value, new_value = Fraction(distance, old), Fraction(distance, new)
        factor = new_value / old_value
        effect = "multiplies by 1/2"
        answer = (f"{effect}; {unit_text(old_value, 'hour')} → "
                  f"{unit_text(new_value, 'hour')}")
        model = (f"t1={distance}/{old}={exact_text(old_value)}; "
                 f"t2={distance}/{new}={exact_text(new_value)}")
        return "doubling_effect_in_formula", answer, model, new_value, "inverse"

    match = re.search(
        r"integer inputs n from 1 through (\d+), two sequences give (\d+)\^n "
        r"and (\d+)n\^(\d+)", text, re.I)
    if match:
        upper, base, coefficient, power = map(int, match.groups())
        comparisons = [base ** n > coefficient * n ** power
                       for n in range(1, upper + 1)]
        thresholds = [n for n in range(1, upper + 1)
                      if all(comparisons[n - 1:])]
        if not thresholds:
            raise AssertionError("no crossover in stated range")
        threshold = thresholds[0]
        first_value = base ** threshold
        second_value = coefficient * threshold ** power
        answer = (f"{base}^n; from n = {threshold} through {upper} "
                  f"(at n = {threshold}: {first_value} vs {second_value})")
        model = (f"{base}^n > {coefficient}n^{power} for "
                 f"{threshold} ≤ n ≤ {upper}")
        return "compare_growth_rates", answer, model, Fraction(threshold), None

    match = re.search(r"recorded product is (.+?)\.(?:\s|$)", text, re.I)
    if match:
        expression = match.group(1)
        factors = [int(token) for token in re.findall(r"-?\d+", expression)]
        product = 1
        for factor in factors:
            product *= factor
        negative_count = sum(factor < 0 for factor in factors)
        label = "positive" if product > 0 else "negative"
        answer = f"{label}; {expression} = {product}"
        sign_value = -1 if negative_count % 2 else 1
        model = f"negative-factor count = {negative_count}; sign = {sign_value}"
        return "sign_without_computing", answer, model, Fraction(product), label

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestQualitativeReasoningGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(283)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = QualitativeReasoningGenerator(variant, modifier).generate()
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
            "dominant_term": (
                "Two outputs at input n are n² and 100n. Kai wants to know which "
                "is larger once n passes their positive meeting point."),
            "limiting_value": (
                "A changing ratio is (3n + 1)/(n + 2). The input n keeps growing "
                "while the constants stay fixed, and a check uses n = 1000."),
            "direction_of_change": (
                "An account starts with $100.00 and changes each year by the same "
                "percentage of its current balance. Over 2 years, the annual "
                "change shifts from 10% to 20%."),
            "doubling_effect_in_formula": (
                "A square garden changes from side length 4 m to side length 8 m."),
            "compare_growth_rates": (
                "For integer inputs n from 1 through 30, two sequences give 2^n "
                "and 2n^2."),
            "sign_without_computing": (
                "A recorded product is (-7) × 4 × (-2) × (-3)."),
        }
        question = "What qualitative result and exact check follow?"
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_direction_sign_and_doubling_subfamilies_are_reachable(self):
        random.seed(284)
        directions, signs, doubling = set(), set(), set()
        for _ in range(500):
            directions.add(solve(QualitativeReasoningGenerator(
                "direction_of_change", "plain").generate()["problem"])[4])
            signs.add(solve(QualitativeReasoningGenerator(
                "sign_without_computing", "plain").generate()["problem"])[4])
            doubling.add(solve(QualitativeReasoningGenerator(
                "doubling_effect_in_formula", "plain").generate()["problem"])[4])
        self.assertEqual(directions, {"increases", "decreases"})
        self.assertEqual(signs, {"positive", "negative"})
        self.assertEqual(doubling, {"square", "cube", "inverse"})

    def test_arithmetic_steps(self):
        random.seed(285)
        for _ in range(1400):
            result = QualitativeReasoningGenerator().generate()
            for raw in result["steps"]:
                fields = raw.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(number(fields[1]) + number(fields[2]),
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
                elif fields[0] == "PERCENT_TO_DEC":
                    self.assertEqual(number(fields[1]) / 100,
                                     number(fields[2]), raw)

    def test_modifier_shapes_operation_and_invalid_inputs(self):
        random.seed(286)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = QualitativeReasoningGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(
                    result["operation"],
                    f"applied_qualitative_reasoning_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
        with self.assertRaises(ValueError):
            QualitativeReasoningGenerator("bogus")
        with self.assertRaises(ValueError):
            QualitativeReasoningGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(287)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = QualitativeReasoningGenerator().generate()
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
