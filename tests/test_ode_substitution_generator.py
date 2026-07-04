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

from generators.ode_substitution_generator import ODESubstitutionGenerator
from helpers import DELIM


def exp_text(rate):
    if rate == 1:
        return "e^x"
    if rate == -1:
        return "e^(-x)"
    return f"e^({rate}x)"


def coeff_exp_text(coeff, rate):
    if coeff == 1:
        return exp_text(rate)
    if coeff == -1:
        return f"-{exp_text(rate)}"
    return f"{coeff}{exp_text(rate)}"


def bernoulli_left(a):
    return "dy/dx + y" if a == 1 else f"dy/dx + {a}y"


def y_squared_text(coeff):
    return "y^2" if coeff == 1 else f"{coeff}y^2"


def exp_term(coeff, rate):
    body = exp_text(rate)
    return body if abs(coeff) == 1 else f"{abs(coeff)}{body}"


def denominator_text(m, C, rate):
    body = exp_term(C, rate)
    return f"{m} + {body}" if C > 0 else f"{m} - {body}"


def signed_const(c):
    return f"+ {c}" if c > 0 else f"- {abs(c)}"


def add_term(coeff, var):
    return f"+ {var}" if coeff == 1 else f"+ {coeff}{var}"


def subtract_term(coeff, var):
    return f"- {var}" if coeff == 1 else f"- {coeff}{var}"


def ln_term(coeff):
    if coeff == 1:
        return "ln(x)"
    if coeff == -1:
        return "-ln(x)"
    return f"{coeff} ln(x)"


def ln_combo(coeff, const):
    pieces = [ln_term(coeff)]
    if const > 0:
        pieces.append(f"+ {const}")
    elif const < 0:
        pieces.append(f"- {abs(const)}")
    return " ".join(pieces)


def dx_over_x(coeff):
    if coeff == 1:
        return "dx/x"
    if coeff == -1:
        return "-dx/x"
    return f"{coeff} dx/x"


def if_left_text(a):
    if a == 1:
        return f"{exp_text(-a)}u' - {exp_text(-a)}u"
    return f"{exp_text(-a)}u' - {a}{exp_text(-a)}u"


def parse_problem(problem):
    bernoulli = re.fullmatch(
        r"Solve (dy/dx \+ (?:(\d+)y|y)) = (?:(\d+)y\^2|y\^2) "
        r"with y\(0\) = 1/(\d+) using the Bernoulli substitution "
        r"u = y\^\(-1\)\.",
        problem,
    )
    if bernoulli:
        left, a_txt, b_txt, q_txt = bernoulli.groups()
        a = int(a_txt or 1)
        b = int(b_txt or 1)
        return {"variant": "bernoulli", "left": left, "a": a,
                "b": b, "q": int(q_txt)}

    homogeneous = re.fullmatch(
        r"Solve dy/dx = y/x ([+-]) (\d+) with y\(1\) = (-?\d+) "
        r"using y = vx \(x > 0\)\.",
        problem,
    )
    assert homogeneous is not None, problem
    sign, mag, y1 = homogeneous.groups()
    c = int(mag) if sign == "+" else -int(mag)
    return {"variant": "homogeneous", "c": c, "y1": int(y1)}


def oracle_parts(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "bernoulli":
        m = Fraction(parts["b"], parts["a"])
        assert m.denominator == 1
        m = m.numerator
        C = parts["q"] - m
        answer = f"y = 1/({denominator_text(m, C, parts['a'])})"
        return {**parts, "m": m, "C": C, "answer": answer}

    combo = ln_combo(parts["c"], parts["y1"])
    answer = f"y = x({combo})"
    return {**parts, "combo": combo, "answer": answer}


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def solution_satisfies_ode(example):
    parts = oracle_parts(example)
    if parts["variant"] == "bernoulli":
        a, b, m, C = parts["a"], parts["b"], parts["m"], parts["C"]
        x = 0.23
        denom = m + C * math.exp(a * x)
        y = 1 / denom
        y_prime = -C * a * math.exp(a * x) / (denom * denom)
        return abs(y_prime + a * y - b * y * y) < 1e-9

    c, y1 = parts["c"], parts["y1"]
    x = 1.7
    inner = c * math.log(x) + y1
    y = x * inner
    y_prime = inner + c
    return abs(y_prime - (y / x + c)) < 1e-9 and y1 == y1


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ODE_SETUP":
            if parts["variant"] == "bernoulli":
                expected = [
                    f"{bernoulli_left(parts['a'])} = "
                    f"{y_squared_text(parts['b'])}, y(0) = 1/{parts['q']}",
                    "Bernoulli n=2",
                ]
            else:
                expected = [
                    f"dy/dx = y/x {signed_const(parts['c'])}, "
                    f"y(1) = {parts['y1']}",
                    "homogeneous substitution",
                ]
            if fields[1:] != expected:
                return False
        elif op == "DIVIDE_EQ":
            expected = [
                "divide by y^2",
                f"y^(-2)dy/dx {add_term(parts['a'], 'y^(-1)')} = "
                f"{parts['b']}",
            ]
            if fields[1:] != expected:
                return False
        elif op == "IFACTOR":
            if fields[1:] != [f"mu = e^(∫ {-parts['a']} dx)",
                              exp_text(-parts["a"])]:
                return False
        elif op == "MULTIPLY_IF":
            expected = [if_left_text(parts["a"]),
                        coeff_exp_text(-parts["b"], -parts["a"])]
            if fields[1:] != expected:
                return False
        elif op == "D":
            if Fraction(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "SEPARATE":
            if fields[1:] != [f"dv = {dx_over_x(parts['c'])}"]:
                return False
        elif op == "ANTIDERIV" and fields[1] == dx_over_x(parts.get("c", 2)):
            if fields[2] != f"{ln_term(parts['c'])} + C":
                return False
        elif op == "EVAL":
            if fields[1:] != ["ln(1)", "0"]:
                return False
        elif op == "SOLVE_Y" and parts["variant"] == "homogeneous":
            if fields[1:] != [f"y/x = {parts['combo']}", parts["answer"]]:
                return False
        elif op == "BACK_SUB" and fields[1] == "u = 1/y":
            if fields[2] != parts["answer"]:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestODESubstitutionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ODESubstitutionGenerator()

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

    def test_solutions_satisfy_odes(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(solution_satisfies_ode(result), result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("bernoulli", "homogeneous"):
            gen = ODESubstitutionGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"ode_substitution_{variant}")
                self.assertEqual(oracle_parts(result)["variant"], variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ODESubstitutionGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1y|(?<!\d)1u|(?<!\d)1e|1 ln|\+ -|--")
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
