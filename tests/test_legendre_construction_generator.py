import os
import random
import re
import sys
import unittest
from fractions import Fraction
from math import factorial, gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.legendre_construction_generator import LegendreConstructionGenerator
from helpers import DELIM


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    if "{1, x, x^2, x^3}" in problem:
        variant, degree = "p3", 3
    elif "{1, x, x^2}" in problem:
        variant, degree = "p2", 2
    else:
        match = re.search(r"\bn = (\d+)\b", problem)
        assert match, problem
        variant, degree = "recurrence", int(match.group(1)) + 1
    point = re.search(r"x = (-?\d+(?:/\d+)?)(?: exactly)?\.?$", problem)
    assert point, problem
    series = re.search(r"(S\(x\) = .*?)(?: exactly)? at x = ", problem)
    assert series, problem
    coefficients = [0] * (degree + 1)
    for sign, magnitude, index in re.findall(
            r"(?:(?P<sign>[+-])\s*)?(?P<mag>\d*)P_(?P<i>\d+)\(x\)",
            series.group(1).split("=", 1)[1]):
        value = int(magnitude or 1)
        coefficients[int(index)] = -value if sign == "-" else value
    return variant, degree, Fraction(point.group(1)), coefficients


def legendre_coeffs(n):
    """Independent closed form from Rodrigues' formula, ascending powers."""
    coefficients = [Fraction(0)] * (n + 1)
    for k in range(n // 2 + 1):
        power = n - 2 * k
        numerator = (-1) ** k * factorial(2 * n - 2 * k)
        denominator = (2 ** n * factorial(k) * factorial(n - k)
                       * factorial(power))
        coefficients[power] = Fraction(numerator, denominator)
    return coefficients


def poly_eval(coefficients, x):
    total = Fraction(0)
    for coefficient in reversed(coefficients):
        total = total * x + coefficient
    return total


def poly_text(coefficients):
    denominator = 1
    for coefficient in coefficients:
        denominator = (denominator * coefficient.denominator
                       // gcd(denominator, coefficient.denominator))
    integers = [int(coefficient * denominator)
                for coefficient in coefficients]
    pieces = []
    for power in range(len(integers) - 1, -1, -1):
        coefficient = integers[power]
        if coefficient == 0:
            continue
        magnitude = abs(coefficient)
        if power == 0:
            body = str(magnitude)
        else:
            variable = "x" if power == 1 else f"x^{power}"
            body = variable if magnitude == 1 else f"{magnitude}{variable}"
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append(("- " if coefficient < 0 else "+ ") + body)
    body = " ".join(pieces) or "0"
    return body if denominator == 1 else f"({body})/{denominator}"


def expected_flow(example):
    variant, degree, x0, series = parse_problem(example["problem"])
    values = [poly_eval(legendre_coeffs(index), x0)
              for index in range(degree + 1)]
    total = sum((coefficient * values[index]
                 for index, coefficient in enumerate(series)), Fraction(0))
    answer = (f"P_{degree}(x) = {poly_text(legendre_coeffs(degree))}; "
              f"S({x0}) = {total}")
    return variant, degree, x0, series, values, total, answer


class TestLegendreConstructionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LegendreConstructionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_answer_and_series_trace_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            _, degree, x0, series, values, total, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"][-1], make_step("Z", answer))
            eval_steps = {fields[1]: Fraction(fields[2])
                          for fields in (step.split(DELIM)
                                         for step in result["steps"])
                          if fields[0] == "EVAL"}
            for index, coefficient in enumerate(series):
                if coefficient:
                    self.assertEqual(eval_steps[f"P_{index}({x0})"],
                                     values[index])
            self.assertEqual(eval_steps[f"S({x0})"], total)
            products = [fields for fields in
                        (step.split(DELIM) for step in result["steps"])
                        if fields[0] == "M" and fields[1].lstrip("-").isdigit()]
            expected_products = [coefficient * values[index]
                                 for index, coefficient in enumerate(series)
                                 if coefficient]
            self.assertEqual([Fraction(fields[3]) for fields in products],
                             expected_products)

    def test_projection_arithmetic(self):
        for variant in ("p2", "p3"):
            result = LegendreConstructionGenerator(variant).generate()
            div = [s for s in result["steps"] if s.startswith(f"D{DELIM}")][0]
            fields = div.split(DELIM)
            self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                             Fraction(fields[3]))

    def test_variants_are_available(self):
        for variant in LegendreConstructionGenerator.VARIANTS:
            gen = LegendreConstructionGenerator(variant)
            result = gen.generate()
            self.assertEqual(result["operation"],
                             f"legendre_construction_{variant}")
            self.assertEqual(parse_problem(result["problem"])[0], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LegendreConstructionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(100):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
