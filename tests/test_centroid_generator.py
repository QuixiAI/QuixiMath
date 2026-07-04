import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.centroid_generator import CentroidGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_y(text):
    if text == "x":
        return 1, 1
    if text == "x^2":
        return 1, 2
    coeff, body = text.split("*")
    return int(coeff), 2 if body == "x^2" else 1


def oracle_answer(example):
    y_txt, width = re.fullmatch(
        r"Find the centroid of the region under y = (.+) from x = 0 "
        r"to x = (\d+) using moments\.",
        example["problem"],
    ).groups()
    coeff, power = parse_y(y_txt)
    width = int(width)
    if power == 1:
        area = Fraction(coeff * width * width, 2)
        moment_y = Fraction(coeff * width ** 3, 3)
        moment_x = Fraction(coeff * coeff * width ** 3, 6)
    else:
        area = Fraction(coeff * width ** 3, 3)
        moment_y = Fraction(coeff * width ** 4, 4)
        moment_x = Fraction(coeff * coeff * width ** 5, 10)
    return (f"centroid ({fmt_frac(moment_y / area)}, "
            f"{fmt_frac(moment_x / area)})")


def eval_fraction_expr(expr):
    expr = expr.replace("^", "**")
    expr = re.sub(r"\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"AREA_INT", "MOMENT_Y", "MOMENT_X",
                        "CENTROID_COORD"}:
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
    return True


class TestCentroidGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CentroidGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_outputs(self):
        for variant in ("line_region", "parabola_region"):
            gen = CentroidGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(result["final_answer"].startswith("centroid "))

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)
                self.assertNotIn(f"{DELIM}{DELIM}", s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            CentroidGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
