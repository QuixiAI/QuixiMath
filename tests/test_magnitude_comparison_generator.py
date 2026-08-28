"""Problem-text-only oracles for :class:`MagnitudeComparisonGenerator`."""
import random
import re
import unittest
from fractions import Fraction

from generators.magnitude_comparison_generator import (
    APPLIED,
    FRAMES,
    MODIFIERS,
    VARIANTS,
    MagnitudeComparisonGenerator,
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
    if name in ("km", "m²") or "/" in name:
        return f"{text} {name}"
    return f"{text} {name if abs(value) == 1 else name + 's'}"


def relation(left, right):
    return "<" if left < right else ">" if left > right else "="


def clean(problem):
    return re.sub(r"^A nearby display lists \d+ archived tickets\. ", "",
                  problem)


def solve(problem):
    """Recompute each comparison from the quantitative story alone."""
    text = clean(problem)

    match = re.search(
        r"tank contains (\d+) filled sections out of (\d+) equal sections\. "
        r"Compare that share with ([0-9./]+)", text, re.I)
    if match:
        numerator, denominator = map(int, match.groups()[:2])
        benchmark = number(match.group(3))
        value = Fraction(numerator, denominator)
        symbol = relation(value, benchmark)
        words = {"<": "less than", ">": "greater than", "=": "equal to"}[symbol]
        left_cross = numerator * benchmark.denominator
        right_cross = benchmark.numerator * denominator
        benchmark_text = f"{benchmark.numerator}/{benchmark.denominator}"
        fraction_text = f"{numerator}/{denominator}"
        answer = (f"{words} {benchmark_text}; {left_cross} {symbol} "
                  f"{right_cross}")
        model = f"{fraction_text} {symbol} {benchmark_text}"
        return "benchmark_fraction", answer, model, value, symbol

    match = re.search(
        r"two expressions are ([0-9./]+) × (\d+) and (\d+) ÷ (\d+)", text,
        re.I)
    if match:
        factor = number(match.group(1))
        first_base, second_base, divisor = map(int, match.groups()[1:])
        if first_base != second_base:
            raise AssertionError("expressions do not share a base")
        left, right = factor * first_base, Fraction(second_base, divisor)
        left_expr = f"{exact_text(factor)} × {first_base}"
        right_expr = f"{second_base} ÷ {divisor}"
        symbol = relation(left, right)
        if left > right:
            larger_expr, larger, smaller = left_expr, left, right
        else:
            larger_expr, larger, smaller = right_expr, right, left
        answer = f"{larger_expr}; {exact_text(larger)} > {exact_text(smaller)}"
        model = f"{left_expr} {symbol} {right_expr}"
        return "compare_without_computing", answer, model, larger, symbol

    match = re.search(
        r"about ([0-9.]+) × 10\^(\d+) residents.*?costs ([0-9.]+) × "
        r"10\^(\d+) dollars per resident", text, re.I)
    if match:
        first_mantissa = number(match.group(1))
        first_exp = int(match.group(2))
        second_mantissa = number(match.group(3))
        second_exp = int(match.group(4))
        total = (first_mantissa * 10 ** first_exp *
                 second_mantissa * 10 ** second_exp)
        digits = len(str(total.numerator // total.denominator)) - 1
        normalized = total / 10 ** digits
        answer = f"10^{digits} dollars; exact {money_text(total)}"
        model = (f"({exact_text(first_mantissa)} × 10^{first_exp})"
                 f"({exact_text(second_mantissa)} × 10^{second_exp}) = "
                 f"{exact_text(normalized)} × 10^{digits}")
        return "order_of_magnitude", answer, model, total, None

    match = re.search(
        r"shopper buys (\d+) identical notebooks at (\$[0-9.]+) each\. "
        r"A report gives the total as (\$[0-9.]+)", text, re.I)
    if match:
        count = int(match.group(1))
        price, claim = number(match.group(2)), number(match.group(3))
        value = count * price
        correct = money_text(value)
        model = f"c = {count} × {exact_text(price)} = {correct}"
        family = "cost"
    else:
        match = re.search(
            r"bus travels at (\d+) km/h for (\d+) hours?\. A report gives "
            r"the distance as ([0-9.]+) km", text, re.I)
        if match:
            speed, elapsed = map(int, match.groups()[:2])
            claim = number(match.group(3))
            value = Fraction(speed * elapsed)
            correct = unit_text(value, "km")
            model = f"d = {speed} × {elapsed} = {correct}"
            family = "travel"
        else:
            match = re.search(
                r"rectangular floor is (\d+) m by (\d+) m\. A report gives "
                r"the covered surface as ([0-9.]+) m²", text, re.I)
            if match:
                length, width = map(int, match.groups()[:2])
                claim = number(match.group(3))
                value = Fraction(length * width)
                correct = unit_text(value, "m²")
                model = f"q = {length} × {width} = {correct}"
                family = "area"
    if match and "A report gives" in match.string[match.start():]:
        claim_correct = claim == value
        verdict = "reasonable" if claim_correct else "unreasonable"
        answer = f"{verdict}; correct {correct}"
        return "reasonable_answer", answer, model, value, (family, verdict)

    match = re.search(
        r"same positive number (\d+) is multiplied by ([0-9./]+).*?divided "
        r"by ([0-9./]+)", text, re.I)
    if match:
        base = int(match.group(1))
        factor, second_factor = map(number, match.groups()[1:])
        if factor != second_factor:
            raise AssertionError("product and quotient factors differ")
        product, quotient = base * factor, base / factor
        factor_text = exact_text(factor)
        product_expr = f"{base} × {factor_text}"
        quotient_expr = f"{base} ÷ {factor_text}"
        symbol = relation(product, quotient)
        if product > quotient:
            larger_expr, larger, smaller = product_expr, product, quotient
        else:
            larger_expr, larger, smaller = quotient_expr, quotient, product
        answer = f"{larger_expr}; {exact_text(larger)} > {exact_text(smaller)}"
        model = f"{product_expr} {symbol} {quotient_expr}"
        return "bigger_product_or_quotient", answer, model, larger, symbol

    match = re.search(
        r"size check is needed for (\d+) × (\d+)\. Round each factor", text,
        re.I)
    if match:
        first, second = map(int, match.groups())
        first_rounded = 10 * ((first + 5) // 10)
        second_rounded = 10 * ((second + 5) // 10)
        estimate, value = first_rounded * second_rounded, first * second
        answer = f"about {estimate}; exact {value}"
        model = f"{first} × {second} ≈ {first_rounded} × {second_rounded} = {estimate}"
        return "estimate_then_verify", answer, model, Fraction(value), None

    raise AssertionError(f"unrecognized problem: {problem}")


def expected(problem, modifier):
    variant, answer, model, value, category = solve(problem)
    if modifier == "with_model":
        answer = f"{model}; {answer}"
    return variant, answer, model, value, category


class TestMagnitudeComparisonGenerator(unittest.TestCase):
    def test_marker_contract_and_500_sample_problem_only_oracle(self):
        self.assertIs(APPLIED, True)
        random.seed(293)
        seen = set()
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                for _ in range(24):
                    result = MagnitudeComparisonGenerator(variant, modifier).generate()
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
            "benchmark_fraction": (
                "A tank contains 7 filled sections out of 15 equal sections. "
                "Compare that share with 1/2 of the tank."),
            "compare_without_computing": (
                "The two expressions are 0.3 × 45 and 45 ÷ 3."),
            "order_of_magnitude": (
                "A region has about 4.8 × 10^3 residents, and a program costs "
                "2.1 × 10^2 dollars per resident."),
            "reasonable_answer": (
                "A bus travels at 60 km/h for 3 hours. A report gives the "
                "distance as 18 km."),
            "bigger_product_or_quotient": (
                "The same positive number 80 is multiplied by 0.5 in one "
                "expression and divided by 0.5 in another."),
            "estimate_then_verify": (
                "A size check is needed for 47 × 62. Round each factor to the "
                "nearest ten before finding the exact product."),
        }
        question = "Give the comparison and exact check."
        self.assertEqual(len(FRAMES), 5)
        for variant, facts in examples.items():
            for index, frame in enumerate(FRAMES):
                problem = frame.format(facts=facts, question=question,
                                       place="the science room", name="Ada")
                with self.subTest(variant=variant, rendering=index):
                    self.assertEqual(solve(problem)[0], variant)

    def test_comparison_directions_reasonable_families_and_verdicts(self):
        random.seed(294)
        benchmark, expression, product_quotient = set(), set(), set()
        reasonable_families, reasonable_verdicts = set(), set()
        for _ in range(600):
            benchmark.add(solve(MagnitudeComparisonGenerator(
                "benchmark_fraction", "plain").generate()["problem"])[4])
            expression.add(solve(MagnitudeComparisonGenerator(
                "compare_without_computing", "plain").generate()["problem"])[4])
            product_quotient.add(solve(MagnitudeComparisonGenerator(
                "bigger_product_or_quotient", "plain").generate()["problem"])[4])
            family, verdict = solve(MagnitudeComparisonGenerator(
                "reasonable_answer", "plain").generate()["problem"])[4]
            reasonable_families.add(family)
            reasonable_verdicts.add(verdict)
        self.assertTrue({"<", ">"}.issubset(benchmark))
        self.assertEqual(expression, {"<", ">"})
        self.assertEqual(product_quotient, {"<", ">"})
        self.assertEqual(reasonable_families, {"cost", "travel", "area"})
        self.assertEqual(reasonable_verdicts, {"reasonable", "unreasonable"})

    def test_arithmetic_steps(self):
        random.seed(295)
        for _ in range(1500):
            result = MagnitudeComparisonGenerator().generate()
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

    def test_modifier_shapes_and_estimate_variant(self):
        random.seed(296)
        for variant in VARIANTS:
            for modifier in MODIFIERS:
                result = MagnitudeComparisonGenerator(variant, modifier).generate()
                codes = [raw.split(DELIM)[0] for raw in result["steps"]]
                self.assertEqual(
                    result["operation"],
                    f"applied_magnitude_comparison_{variant}_{modifier}")
                if modifier == "distractor":
                    self.assertEqual(codes[0], "SELECT_RELEVANT")
                elif modifier == "estimate_first":
                    self.assertEqual(codes[0], "ESTIMATE")
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
                elif modifier == "with_model":
                    self.assertEqual(codes[0], "MODEL_EQ")
                if variant == "estimate_then_verify":
                    self.assertIn("ESTIMATE", codes)
                    self.assertEqual(codes[-2], "ESTIMATE_CHECK")
        with self.assertRaises(ValueError):
            MagnitudeComparisonGenerator("bogus")
        with self.assertRaises(ValueError):
            MagnitudeComparisonGenerator(modifier="bogus")

    def test_pipe_safety_and_render_sanity(self):
        random.seed(297)
        banned = ("1x", "-1x", "^1", "+ 0", "--", "the the", "e+")
        for _ in range(700):
            result = MagnitudeComparisonGenerator().generate()
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
