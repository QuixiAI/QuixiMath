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

from generators.second_order_ode_generator import SecondOrderODEGenerator
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
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def factor_text(root):
    return f"(r - {root})" if root > 0 else f"(r + {abs(root)})"


def signed_join(terms):
    return fmt_terms(terms)


def distinct_solution(c1, r1, c2, r2):
    return "y = " + signed_join([(c1, exp_text(r1)),
                                  (c2, exp_text(r2))])


def linear_x(c1, c2):
    return signed_join([(c1, ""), (c2, "x")])


def repeated_solution(c1, c2, r):
    return f"y = ({linear_x(c1, c2)}){exp_text(r)}"


def trig_arg(beta):
    return "x" if beta == 1 else f"{beta}x"


def trig_combo(c1, c2, beta):
    arg = trig_arg(beta)
    return signed_join([(c1, f"cos({arg})"), (c2, f"sin({arg})")])


def complex_solution(c1, c2, alpha, beta):
    return f"y = {exp_text(alpha)}({trig_combo(c1, c2, beta)})"


def derivative_exp_terms(r1, r2):
    return signed_join([
        (r1, f"C1{exp_text(r1)}"),
        (r2, f"C2{exp_text(r2)}"),
    ])


def constant_equation_terms(a, b):
    return signed_join([(a, "C1"), (b, "C2")])


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


def parse_problem(problem):
    match = re.fullmatch(
        r"Solve (.+) = 0 with y\(0\) = (-?\d+) and y'\(0\) = (-?\d+)\.",
        problem,
    )
    assert match is not None, problem
    lhs, y0, v0 = match.groups()
    p, q = parse_ode_lhs(lhs)
    return lhs, p, q, int(y0), int(v0)


def oracle_parts(example):
    lhs, p, q, y0, v0 = parse_problem(example["problem"])
    disc = p * p - 4 * q
    if disc > 0:
        root = math.isqrt(disc)
        assert root * root == disc
        r1 = Fraction(-p - root, 2)
        r2 = Fraction(-p + root, 2)
        assert r1.denominator == 1 and r2.denominator == 1
        r1, r2 = sorted((r1.numerator, r2.numerator))
        c1 = Fraction(v0 - r2 * y0, r1 - r2)
        c2 = Fraction(y0) - c1
        assert c1.denominator == 1 and c2.denominator == 1
        c1, c2 = c1.numerator, c2.numerator
        return {
            "variant": "distinct_real",
            "lhs": lhs,
            "p": p,
            "q": q,
            "y0": y0,
            "v0": v0,
            "r1": r1,
            "r2": r2,
            "c1": c1,
            "c2": c2,
            "answer": distinct_solution(c1, r1, c2, r2),
        }
    if disc == 0:
        r = Fraction(-p, 2)
        assert r.denominator == 1
        r = r.numerator
        c1 = y0
        c2 = v0 - r * c1
        return {
            "variant": "repeated_root",
            "lhs": lhs,
            "p": p,
            "q": q,
            "y0": y0,
            "v0": v0,
            "r": r,
            "c1": c1,
            "c2": c2,
            "answer": repeated_solution(c1, c2, r),
        }
    root = math.isqrt(-disc)
    assert root * root == -disc
    alpha = Fraction(-p, 2)
    beta = Fraction(root, 2)
    assert alpha.denominator == 1 and beta.denominator == 1
    alpha, beta = alpha.numerator, beta.numerator
    c1 = y0
    c2 = Fraction(v0 - alpha * c1, beta)
    assert c2.denominator == 1
    c2 = c2.numerator
    return {
        "variant": "complex_roots",
        "lhs": lhs,
        "p": p,
        "q": q,
        "y0": y0,
        "v0": v0,
        "alpha": alpha,
        "beta": beta,
        "c1": c1,
        "c2": c2,
        "answer": complex_solution(c1, c2, alpha, beta),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def solution_values(parts, x):
    if parts["variant"] == "distinct_real":
        c1, c2 = parts["c1"], parts["c2"]
        r1, r2 = parts["r1"], parts["r2"]
        e1 = math.exp(r1 * x)
        e2 = math.exp(r2 * x)
        y = c1 * e1 + c2 * e2
        yp = c1 * r1 * e1 + c2 * r2 * e2
        ypp = c1 * r1 * r1 * e1 + c2 * r2 * r2 * e2
        return y, yp, ypp
    if parts["variant"] == "repeated_root":
        c1, c2, r = parts["c1"], parts["c2"], parts["r"]
        e = math.exp(r * x)
        inner = c1 + c2 * x
        y = inner * e
        yp = (c2 + r * inner) * e
        ypp = (2 * r * c2 + r * r * inner) * e
        return y, yp, ypp
    c1, c2 = parts["c1"], parts["c2"]
    alpha, beta = parts["alpha"], parts["beta"]
    e = math.exp(alpha * x)
    cosv = math.cos(beta * x)
    sinv = math.sin(beta * x)
    f = c1 * cosv + c2 * sinv
    fp = -c1 * beta * sinv + c2 * beta * cosv
    fpp = -beta * beta * f
    y = e * f
    yp = e * (alpha * f + fp)
    ypp = e * (alpha * alpha * f + 2 * alpha * fp + fpp)
    return y, yp, ypp


def solution_satisfies_ode(example):
    parts = oracle_parts(example)
    y, yp, ypp = solution_values(parts, 0.31)
    residual = ypp + parts["p"] * yp + parts["q"] * y
    y0, v0, _ = solution_values(parts, 0)
    return (abs(residual) < 1e-8 and
            abs(y0 - parts["y0"]) < 1e-9 and
            abs(v0 - parts["v0"]) < 1e-9)


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            expected = [
                f"{ode_lhs(parts['p'], parts['q'])} = 0",
                f"y(0) = {parts['y0']}, y'(0) = {parts['v0']}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "CHAR_EQ":
            if fields[1:] != ["assume y=e^(rx)",
                              f"{char_poly(parts['p'], parts['q'])} = 0"]:
                return False
        elif op == "FACTOR":
            if parts["variant"] == "distinct_real":
                expected = (
                    f"{factor_text(parts['r1'])}{factor_text(parts['r2'])} = 0"
                )
            elif parts["variant"] == "repeated_root":
                expected = f"{factor_text(parts['r'])}^2 = 0"
            else:
                continue
            if fields[1:] != [char_poly(parts["p"], parts["q"]), expected]:
                return False
        elif op == "CHAR_ROOTS":
            if parts["variant"] == "distinct_real":
                expected = [f"r1 = {parts['r1']}, r2 = {parts['r2']}",
                            "distinct real"]
            elif parts["variant"] == "repeated_root":
                expected = [f"r = {parts['r']}", "repeated"]
            else:
                expected = [f"r = {parts['alpha']} ± {parts['beta']}i",
                            "complex conjugates"]
            if fields[1:] != expected:
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "SOLVE_CONST":
            if fields[1:] != [f"C1 = {parts['c1']}",
                              f"C2 = {parts['c2']}"]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestSecondOrderODEGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SecondOrderODEGenerator()

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

    def test_solution_satisfies_ode_and_initial_conditions(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(solution_satisfies_ode(result), result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("distinct_real", "repeated_root", "complex_roots"):
            gen = SecondOrderODEGenerator(variant)
            for _ in range(80):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"second_order_ode_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SecondOrderODEGenerator("bogus")

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
