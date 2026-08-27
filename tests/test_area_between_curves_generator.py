import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.area_between_curves_generator import (
    AreaBetweenCurvesGenerator,
)
from helpers import DELIM


def oracle_answer(example):
    first, second = curves_from_problem(example["problem"])
    f, g = parse_quadratic(first), parse_quadratic(second)
    difference = tuple(a - b for a, b in zip(f, g))
    roots = sorted(t for t in range(-30, 31)
                   if eval_poly(difference, Fraction(t)) == 0)
    assert len(roots) == 2
    p, q = map(Fraction, roots)
    midpoint = Fraction(p + q, 2)
    if eval_poly(difference, midpoint) < 0:
        difference = tuple(-value for value in difference)
    # Integrate the upper-minus-lower quadratic exactly over [p, q].
    c2, c1, c0 = difference
    def antiderivative(x):
        return c2 * x ** 3 / 3 + c1 * x ** 2 / 2 + c0 * x
    return str(antiderivative(q) - antiderivative(p))


CURVE_PATTERNS = (
    r"Find the area between y = (?P<f>.+) and y = (?P<g>.+)\.",
    r"Find the area of the region bounded by the curves y = (?P<f>.+) and "
    r"y = (?P<g>.+)\.",
    r"The curves y = (?P<f>.+) and y = (?P<g>.+) enclose a region\. "
    r"Find its area\.",
    r"Compute the exact area of the region between y = (?P<f>.+) and "
    r"y = (?P<g>.+)\.",
    r"Find the area enclosed by the graphs of y = (?P<f>.+) and "
    r"y = (?P<g>.+)\.",
    r"Two curves, y = (?P<f>.+) and y = (?P<g>.+), intersect at two "
    r"points\. Find the area of the region between them\.",
)


def curves_from_problem(problem):
    for pattern in CURVE_PATTERNS:
        match = re.fullmatch(pattern, problem)
        if match:
            return match.group("f"), match.group("g")
    raise AssertionError(problem)


def parse_quadratic(text):
    """Return coefficients of x^2, x, 1 from the printed curve."""
    coefficients = {2: 0, 1: 0, 0: 0}
    for raw in text.replace(" - ", " + -").split(" + "):
        term = raw.strip()
        match = re.fullmatch(r"(-?\d*)x(?:\^(2))?|(-?\d+)", term)
        assert match, text
        if match.group(3) is not None:
            coefficients[0] += int(match.group(3))
            continue
        raw_coefficient = match.group(1)
        if raw_coefficient == "":
            coefficient = 1
        elif raw_coefficient == "-":
            coefficient = -1
        else:
            coefficient = int(raw_coefficient)
        power = 2 if match.group(2) else 1
        coefficients[power] += coefficient
    return coefficients[2], coefficients[1], coefficients[0]


def eval_poly(coefficients, x):
    c2, c1, c0 = coefficients
    return c2 * x * x + c1 * x + c0


class TestAreaBetweenCurvesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = AreaBetweenCurvesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: (q - p)³/6 for secants; (8/3)k³ for the pair."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_area_is_positive(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertGreater(Fraction(result["final_answer"]), 0)

    def test_top_curve_checked(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"CHECK{DELIM}midpoint")
                                for s in result["steps"]))

    def test_both_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            AreaBetweenCurvesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
