import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.series_solution_generator import SeriesSolutionGenerator
from helpers import DELIM


def term_text(coeff, power):
    if power == 0:
        return str(abs(coeff))
    body = "x" if power == 1 else f"x^{power}"
    return body if abs(coeff) == 1 else f"{abs(coeff)}{body}"


def poly_text(coeffs):
    pieces = []
    for power, coeff in enumerate(coeffs):
        if coeff == 0:
            continue
        body = term_text(coeff, power)
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def left_text(k):
    if k == 1:
        return "y' = y"
    if k == -1:
        return "y' = -y"
    return f"y' = {k}y"


def coeff_var_text(k, var):
    if k == 1:
        return var
    if k == -1:
        return f"-{var}"
    return f"{k}{var}"


def parse_problem(problem):
    match = re.fullmatch(
        r"Find the power-series solution through x\^5 for (y' = .+) "
        r"with y\(0\) = (\d+)\.",
        problem,
    )
    assert match is not None, problem
    left = match.group(1)
    if left == "y' = y":
        k = 1
    elif left == "y' = -y":
        k = -1
    else:
        coeff = re.fullmatch(r"y' = (-?\d+)y", left)
        assert coeff is not None, left
        k = int(coeff.group(1))
    return k, int(match.group(2))


def coeffs_for(k, a0):
    coeffs = [a0]
    for n in range(5):
        coeffs.append(coeffs[n] * k // (n + 1))
    return coeffs


def oracle_parts(example):
    k, a0 = parse_problem(example["problem"])
    coeffs = coeffs_for(k, a0)
    return {
        "k": k,
        "a0": a0,
        "coeffs": coeffs,
        "answer": f"y = {poly_text(coeffs)} + O(x^6)",
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    coeff_index = 0
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            if fields[1:] != [f"{left_text(parts['k'])}, "
                              f"y(0) = {parts['a0']}",
                              "power series through x^5"]:
                return False
        elif op == "RECURRENCE":
            if fields[1:] != ["a_(n+1)",
                              f"{coeff_var_text(parts['k'], 'a_n')}/(n+1)"]:
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "COEFF":
            coeff_index += 1
            if fields[1:] != [f"a_{coeff_index}",
                              str(parts["coeffs"][coeff_index])]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return coeff_index == 5


def truncated_series_matches_exponential(example):
    parts = oracle_parts(example)
    x = 0.05
    approx = sum(coeff * (x ** power)
                 for power, coeff in enumerate(parts["coeffs"]))
    exact = parts["a0"] * math.exp(parts["k"] * x)
    return abs(approx - exact) < 0.05


class TestSeriesSolutionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SeriesSolutionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_series_matches_exponential_locally(self):
        for _ in range(100):
            result = self.gen.generate()
            self.assertTrue(truncated_series_matches_exponential(result),
                            result["problem"])

    def test_fixed_variant_constructor(self):
        gen = SeriesSolutionGenerator("first_order_exp")
        result = gen.generate()
        self.assertEqual(result["operation"], "series_solution_first_order_exp")
        with self.assertRaises(ValueError):
            SeriesSolutionGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<![A-Za-z0-9])1y|(?<!\d)1x|\+ -|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)


if __name__ == "__main__":
    unittest.main()
