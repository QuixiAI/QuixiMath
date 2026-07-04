import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.legendre_construction_generator import LegendreConstructionGenerator
from helpers import DELIM


P2_RE = re.compile(
    r"Use Gram-Schmidt on \{1, x, x\^2\} over \[-1,1\] to construct "
    r"the Legendre polynomial P_2 with leading coefficient 3/2\."
)
P3_RE = re.compile(
    r"Use Gram-Schmidt on \{1, x, x\^2, x\^3\} over \[-1,1\] to "
    r"construct the Legendre polynomial P_3 with leading coefficient 5/2\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    if P2_RE.fullmatch(problem):
        return "p2"
    assert P3_RE.fullmatch(problem), problem
    return "p3"


def expected_flow(example):
    variant = parse_problem(example["problem"])
    if variant == "p2":
        numerator = Fraction(2, 3)
        denominator = Fraction(2)
        projection = numerator / denominator
        answer = "P_2(x) = (3x^2 - 1)/2"
        steps = [
            make_step("LEGENDRE_SETUP", "target=P_2",
                      "inner product integral_-1^1 f(x)g(x) dx"),
            make_step("INTEGRAL", "<1,1>", denominator),
            make_step("INTEGRAL", "<x^2,1>", numerator),
            make_step("D", numerator, denominator, projection),
            make_step("PROJECTION", "x^2 onto 1", projection),
            make_step("POLY_SUB", "x^2", projection, "x^2 - 1/3"),
            make_step("POLY_SCALE", "x^2 - 1/3", "3/2",
                      "(3x^2 - 1)/2"),
            make_step("Z", answer),
        ]
    else:
        numerator = Fraction(2, 5)
        denominator = Fraction(2, 3)
        projection = numerator / denominator
        answer = "P_3(x) = (5x^3 - 3x)/2"
        steps = [
            make_step("LEGENDRE_SETUP", "target=P_3",
                      "inner product integral_-1^1 f(x)g(x) dx"),
            make_step("INTEGRAL", "<x,x>", denominator),
            make_step("INTEGRAL", "<x^3,x>", numerator),
            make_step("D", numerator, denominator, projection),
            make_step("PROJECTION", "x^3 onto x", projection),
            make_step("POLY_SUB", "x^3", "3x/5", "x^3 - 3x/5"),
            make_step("POLY_SCALE", "x^3 - 3x/5", "5/2",
                      "(5x^3 - 3x)/2"),
            make_step("Z", answer),
        ]
    return steps, answer


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

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(100):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_projection_arithmetic(self):
        for variant in ("p2", "p3"):
            result = LegendreConstructionGenerator(variant).generate()
            div = [s for s in result["steps"] if s.startswith(f"D{DELIM}")][0]
            fields = div.split(DELIM)
            self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                             Fraction(fields[3]))

    def test_variants_are_available(self):
        for variant in ("p2", "p3"):
            gen = LegendreConstructionGenerator(variant)
            result = gen.generate()
            self.assertEqual(result["operation"],
                             f"legendre_construction_{variant}")
            self.assertEqual(parse_problem(result["problem"]), variant)

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
