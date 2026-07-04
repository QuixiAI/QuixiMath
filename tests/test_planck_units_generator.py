import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.planck_units_generator import PlanckUnitsGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given hbar=(\d+), G=(\d+), and c=(\d+), compute the Planck "
    r"(length|time|mass) "
    r"(sqrt\(hbar\*G/c\^[35]\)|sqrt\(hbar\*c/G\))\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "hbar": int(match.group(1)),
        "G": int(match.group(2)),
        "c": int(match.group(3)),
        "variant": match.group(4),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    hbar = parts["hbar"]
    G = parts["G"]
    c = parts["c"]
    variant = parts["variant"]
    if variant == "length":
        power = 3
        answer_name = "l_P"
        numerator = hbar * G
        denominator = c ** power
    elif variant == "time":
        power = 5
        answer_name = "t_P"
        numerator = hbar * G
        denominator = c ** power
    else:
        power = 1
        answer_name = "m_P"
        numerator = hbar * c
        denominator = G
    radicand = Fraction(numerator, denominator)
    root_value = sqrt_fraction(radicand)
    steps = [
        make_step("PLANCK_SETUP", variant, f"hbar={hbar}", f"G={G}",
                  f"c={c}"),
        make_step("M", hbar, G if variant != "mass" else c, numerator),
        make_step("E", c if variant != "mass" else G, power,
                  (c if variant != "mass" else G) ** power),
        make_step("D", numerator, denominator, fraction_text(radicand)),
        make_step("ROOT", f"sqrt({fraction_text(radicand)})",
                  fraction_text(root_value)),
    ]
    answer = f"{answer_name} = {fraction_text(root_value)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def sqrt_fraction(value):
    num = int(value.numerator ** 0.5)
    den = int(value.denominator ** 0.5)
    assert num * num == value.numerator
    assert den * den == value.denominator
    return Fraction(num, den)


class TestPlanckUnitsGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PlanckUnitsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    inside = Fraction(fields[1].removeprefix("sqrt(").rstrip(")"))
                    root = Fraction(fields[2])
                    self.assertEqual(root * root, inside, raw_step)

    def test_variants_are_available(self):
        for variant in PlanckUnitsGenerator.VARIANTS:
            result = PlanckUnitsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"planck_units_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PlanckUnitsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
