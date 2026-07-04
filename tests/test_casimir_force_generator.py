import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.casimir_force_generator import CasimirForceGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given hbar=(\d+), c=(\d+), and plate separation d=(\d+), "
    r"compute the Casimir force per area "
    r"F/A=-π\^2\*hbar\*c/\(240\*d\^4\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def pi_squared_text(value):
    coeff = Fraction(value)
    sign = "-" if coeff < 0 else ""
    coeff = abs(coeff)
    if coeff == 1:
        body = "π^2"
    elif coeff.denominator == 1:
        body = f"{coeff.numerator}π^2"
    elif coeff.numerator == 1:
        body = f"π^2/{coeff.denominator}"
    else:
        body = f"{coeff.numerator}π^2/{coeff.denominator}"
    return sign + body


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "hbar": int(match.group(1)),
        "c": int(match.group(2)),
        "d": int(match.group(3)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    hbar = parts["hbar"]
    c = parts["c"]
    d = parts["d"]
    d_fourth = d ** 4
    denominator = 240 * d_fourth
    numerator = hbar * c
    coeff = Fraction(numerator, denominator)
    signed_coeff = -coeff
    value = pi_squared_text(signed_coeff)
    constants = f"hbar={hbar},c={c},d={d}"
    steps = [
        make_step("CASIMIR_FORCE_SETUP",
                  "F/A=-π^2*hbar*c/(240*d^4)", constants),
        make_step("E", d, 4, d_fourth),
        make_step("M", 240, d_fourth, denominator),
        make_step("M", hbar, c, numerator),
        make_step("D", numerator, denominator, fraction_text(coeff)),
        make_step("S", 0, fraction_text(coeff), fraction_text(signed_coeff)),
        make_step("PI2_NUM", fraction_text(signed_coeff), "π^2", value),
    ]
    answer = f"F/A = {value}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCasimirForceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CasimirForceGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "PI2_NUM":
                    self.assertEqual(fields[2], "π^2", raw_step)
                    self.assertEqual(pi_squared_text(Fraction(fields[1])),
                                     fields[3], raw_step)

    def test_variant_is_available(self):
        result = CasimirForceGenerator("pressure").generate()
        self.assertEqual(result["operation"], "casimir_force_pressure")
        parts = parse_problem(result["problem"])
        self.assertGreaterEqual(parts["d"], 1)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CasimirForceGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_force_is_attractive(self):
        for _ in range(100):
            result = self.gen.generate()
            self.assertIn("F/A = -", result["final_answer"])


if __name__ == "__main__":
    unittest.main()
