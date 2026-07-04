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

from generators.variation_parameters_generator import VariationParametersGenerator
from helpers import DELIM


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def ode_lhs(p, q):
    return fmt_terms([(1, "y''"), (p, "y'"), (q, "y")])


def char_poly(p, q):
    return fmt_terms([(1, "r^2"), (p, "r"), (q, "")])


def exp_text(rate):
    if rate == 0:
        return "1"
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_text(coeff, rate):
    if rate == 0:
        return str(coeff)
    if coeff == 1:
        return exp_text(rate)
    if coeff == -1:
        return f"-{exp_text(rate)}"
    return f"{coeff}{exp_text(rate)}"


def factor_text(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def signed_join(terms):
    return fmt_terms(terms)


def solution_text(r1, r2, A_part, k):
    return "y = " + signed_join([
        (1, f"C1{exp_text(r1)}"),
        (1, f"C2{exp_text(r2)}"),
        (A_part, exp_text(k)),
    ])


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_ode_lhs(lhs):
    coeffs = {"y''": 0, "y'": 0, "y": 0}
    for raw in split_terms(lhs):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        if raw == "y''":
            coeffs["y''"] += sign
        elif raw.endswith("y'"):
            prefix = raw[:-2]
            coeffs["y'"] += sign * (int(prefix) if prefix else 1)
        elif raw.endswith("y"):
            prefix = raw[:-1]
            coeffs["y"] += sign * (int(prefix) if prefix else 1)
        else:
            raise AssertionError(f"bad term {raw!r}")
    assert coeffs["y''"] == 1
    return coeffs["y'"], coeffs["y"]


def parse_coeff(text):
    if text == "":
        return 1
    if text == "-":
        return -1
    return int(text)


def parse_rate(text):
    if text == "x":
        return 1
    inner = text[1:-1].removesuffix("x")
    if inner == "-":
        return -1
    return int(inner)


def parse_rhs(rhs):
    match = re.fullmatch(r"(-?\d*)e\^(x|\(-?\d*x\))", rhs)
    assert match is not None, rhs
    return parse_coeff(match.group(1)), parse_rate(match.group(2))


def roots_from_coeffs(p, q):
    disc = p * p - 4 * q
    root = math.isqrt(disc)
    assert root * root == disc
    r1 = Fraction(-p - root, 2)
    r2 = Fraction(-p + root, 2)
    assert r1.denominator == 1 and r2.denominator == 1
    return sorted((r1.numerator, r2.numerator))


def parse_problem(problem):
    match = re.fullmatch(
        r"Solve (.+) = (.+) by variation of parameters\.",
        problem,
    )
    assert match is not None, problem
    lhs, rhs = match.groups()
    p, q = parse_ode_lhs(lhs)
    rhs_coeff, k = parse_rhs(rhs)
    return lhs, p, q, rhs, rhs_coeff, k


def oracle_parts(example):
    lhs, p, q, rhs, rhs_coeff, k = parse_problem(example["problem"])
    r1, r2 = roots_from_coeffs(p, q)
    d = r2 - r1
    denom = (k - r1) * (k - r2)
    A_part = Fraction(rhs_coeff, denom)
    assert A_part.denominator == 1
    A_part = A_part.numerator
    rate1 = k - r1
    rate2 = k - r2
    u1_prime_coeff = Fraction(-rhs_coeff, d)
    u2_prime_coeff = Fraction(rhs_coeff, d)
    u1_coeff = u1_prime_coeff / rate1
    u2_coeff = u2_prime_coeff / rate2
    for value in (u1_prime_coeff, u2_prime_coeff, u1_coeff, u2_coeff):
        assert value.denominator == 1
    return {
        "lhs": lhs,
        "p": p,
        "q": q,
        "rhs": rhs,
        "rhs_coeff": rhs_coeff,
        "k": k,
        "r1": r1,
        "r2": r2,
        "d": d,
        "rate1": rate1,
        "rate2": rate2,
        "A_part": A_part,
        "u1_prime_coeff": u1_prime_coeff.numerator,
        "u2_prime_coeff": u2_prime_coeff.numerator,
        "u1_coeff": u1_coeff.numerator,
        "u2_coeff": u2_coeff.numerator,
        "answer": solution_text(r1, r2, A_part, k),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def particular_satisfies_ode(example):
    parts = oracle_parts(example)
    x = 0.41
    A_part = parts["A_part"]
    k = parts["k"]
    expv = math.exp(k * x)
    y = A_part * expv
    yp = A_part * k * expv
    ypp = A_part * k * k * expv
    left = ypp + parts["p"] * yp + parts["q"] * y
    rhs = parts["rhs_coeff"] * expv
    return abs(left - rhs) < 1e-8


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            if fields[1:] != [f"{ode_lhs(parts['p'], parts['q'])} = "
                              f"{parts['rhs']}",
                              "variation of parameters"]:
                return False
        elif op == "CHAR_EQ":
            if fields[1:] != ["assume y=e^(rx)",
                              f"{char_poly(parts['p'], parts['q'])} = 0"]:
                return False
        elif op == "FACTOR":
            expected = f"{factor_text(parts['r1'])}{factor_text(parts['r2'])} = 0"
            if fields[1:] != [char_poly(parts["p"], parts["q"]), expected]:
                return False
        elif op == "WRONSKIAN":
            expected = coeff_exp_text(parts["d"], parts["r1"] + parts["r2"])
            if fields[1:] != ["y1*y2' - y1'*y2", expected]:
                return False
        elif op == "VOP_FORM" and fields[1] == "u1' = -y2*g/W":
            expected = (f"{-parts['rhs_coeff']}/{parts['d']} * "
                        f"{exp_text(parts['rate1'])}")
            if fields[2] != expected:
                return False
        elif op == "VOP_FORM" and fields[1] == "u2' = y1*g/W":
            expected = (f"{parts['rhs_coeff']}/{parts['d']} * "
                        f"{exp_text(parts['rate2'])}")
            if fields[2] != expected:
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
            if int(fields[3]) != parts["A_part"]:
                return False
        elif op == "PARTICULAR":
            expected = ["u1*y1 + u2*y2",
                        coeff_exp_text(parts["A_part"], parts["k"])]
            if fields[1:] != expected:
                return False
        elif op == "SOL_FORM":
            if fields[1:] != [parts["answer"]]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestVariationParametersGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = VariationParametersGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_particular_solution_satisfies_ode(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(particular_satisfies_ode(result),
                            result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_fixed_variant_constructor(self):
        gen = VariationParametersGenerator("exponential_forcing")
        result = gen.generate()
        self.assertEqual(result["operation"],
                         "variation_parameters_exponential_forcing")
        with self.assertRaises(ValueError):
            VariationParametersGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(
            r"(?<![A-Za-z0-9])1y|(?<![A-Za-z0-9])1r|"
            r"(?<![A-Za-z0-9])1e|1C|\+ -|--"
        )
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
