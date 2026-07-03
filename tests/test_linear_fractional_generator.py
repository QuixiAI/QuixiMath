import os
import random
import re
import sys
import unittest
from fractions import Fraction
from math import lcm

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.linear_fractional_generator import LinearFractionalGenerator
from helpers import DELIM

FLIP = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}

FRAC_RE = re.compile(
    r"Solve (?:for x|the inequality): "
    r"\((-?\d+/\d+)\)x ([+-]) (\d+(?:/\d+)?) (=|<|>|≤|≥) (-?\d+(?:/\d+)?)$")
DEC_RE = re.compile(
    r"Solve (?:for x|the inequality): "
    r"(-?\d+\.\d)x ([+-]) (\d+\.\d) (=|<|>|≤|≥) (-?\d+\.\d)$")


def parse_problem(problem):
    """Returns (a, b, rel, rhs) as exact Fractions from the problem text."""
    m = FRAC_RE.match(problem) or DEC_RE.match(problem)
    assert m, f"Unparseable problem: {problem}"
    a = Fraction(m.group(1))
    b = Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1)
    return a, b, m.group(4), Fraction(m.group(5))


def oracle_answer(example):
    """Independently solves the problem from its text alone."""
    a, b, rel, rhs = parse_problem(example["problem"])
    x = (rhs - b) / a
    assert x.denominator == 1, "solution not integer"
    x = int(x)
    if rel == "=":
        return str(x)
    rel_out = FLIP[rel] if a < 0 else rel
    return f"x {rel_out} {x}"


class TestLinearFractionalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LinearFractionalGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_all_variants_reachable(self):
        seen = {self.gen.generate()["operation"] for _ in range(120)}
        self.assertEqual(seen, {"linear_eq_fractions", "linear_ineq_fractions",
                                "linear_eq_decimals", "linear_ineq_decimals"})

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: re-solve from the problem text with exact arithmetic."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_inequality_direction_semantically(self):
        """Beyond the flip rule: a test point must actually satisfy/violate."""
        checked = 0
        for _ in range(300):
            result = self.gen.generate()
            if "ineq" not in result["operation"]:
                continue
            a, b, rel, rhs = parse_problem(result["problem"])
            m = re.fullmatch(r"x (<|>|≤|≥) (-?\d+)", result["final_answer"])
            self.assertIsNotNone(m, result["final_answer"])
            rel_out, boundary = m.group(1), int(m.group(2))
            for xt in (boundary + 1, boundary - 1):
                lhs = a * xt + b
                satisfies_original = {
                    '<': lhs < rhs, '>': lhs > rhs,
                    '≤': lhs <= rhs, '≥': lhs >= rhs}[rel]
                satisfies_answer = {
                    '<': xt < boundary, '>': xt > boundary,
                    '≤': xt <= boundary, '≥': xt >= boundary}[rel_out]
                self.assertEqual(satisfies_original, satisfies_answer,
                                 f"{result['problem']} -> {result['final_answer']}")
            checked += 1
        self.assertGreater(checked, 50)

    def test_step_arithmetic(self):
        """L, MUL_TERM, and CHECK steps must be independently true."""
        for _ in range(300):
            result = self.gen.generate()
            factor = None
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "L":
                    self.assertEqual(lcm(int(f[1]), int(f[2])), int(f[3]), s)
                elif f[0] == "MUL_TERM":
                    factor = Fraction(f[1])
                    term, res = f[2], f[3]
                    if term.endswith("x"):
                        coef = term[:-1]
                        coef = Fraction(coef.strip("()"))
                        self.assertEqual(coef * factor,
                                         Fraction(res[:-1]), s)
                    else:
                        val = Fraction(term.replace("- ", "-"))
                        self.assertEqual(val * factor, Fraction(res), s)
                elif f[0] == "CHECK":
                    self.assertIn(f[1], ("substitute", "boundary_equality"), s)
                    work, rhs_field = f[2], f[3]
                    tail = work.rsplit("= ", 1)[1]
                    self.assertEqual(Fraction(tail), Fraction(rhs_field), s)

    def test_flip_only_on_negative_divide(self):
        for _ in range(300):
            result = self.gen.generate()
            if "ineq" not in result["operation"]:
                continue
            a, _, rel, _ = parse_problem(result["problem"])
            flipped = any(s.startswith(f"INEQ_FLIP{DELIM}")
                          for s in result["steps"])
            self.assertEqual(flipped, a < 0, result["problem"])
            m = re.fullmatch(r"x (<|>|≤|≥) -?\d+", result["final_answer"])
            expected_rel = FLIP[rel] if a < 0 else rel
            self.assertEqual(m.group(1), expected_rel, result["problem"])

    def test_fixed_variant_constructor(self):
        for ptype, ops in (("fractions", {"linear_eq_fractions",
                                          "linear_ineq_fractions"}),
                           ("decimals", {"linear_eq_decimals",
                                         "linear_ineq_decimals"})):
            gen = LinearFractionalGenerator(ptype)
            seen = {gen.generate()["operation"] for _ in range(40)}
            self.assertEqual(seen, ops)
        with self.assertRaises(ValueError):
            LinearFractionalGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
