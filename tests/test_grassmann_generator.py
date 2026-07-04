import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.grassmann_generator import GrassmannGenerator
from helpers import DELIM


MULTIPLY_RE = re.compile(
    r"Let theta\^2=0\. Multiply x=(.+) by y=(.+)\."
)
EXP_RE = re.compile(
    r"Let theta\^2=0\. Expand exp\((.+)\) as a finite Grassmann series\."
)
INTEGRATE_RE = re.compile(
    r"Using Berezin rules int dtheta 1=0 and int dtheta theta=1, "
    r"compute int dtheta \((.+)\)\."
)
MULTIPLY_INTEGRATE_RE = re.compile(
    r"Let theta\^2=0 with Berezin rules int dtheta 1=0 and "
    r"int dtheta theta=1\. Compute int dtheta \[\(x\)\*\(y\)\] for "
    r"x=(.+) and y=(.+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def coeff_text(value):
    if value == 1:
        return ""
    if value == -1:
        return "-"
    return str(value)


def theta_term(coeff):
    if coeff == 0:
        return ""
    return f"{coeff_text(coeff)}theta"


def grass_expr(constant, theta_coeff):
    parts = []
    if constant != 0:
        parts.append(str(constant))
    if theta_coeff != 0:
        body = theta_term(abs(theta_coeff))
        if not parts:
            parts.append(theta_term(theta_coeff))
        elif theta_coeff > 0:
            parts.append(f"+ {body}")
        else:
            parts.append(f"- {body}")
    return " ".join(parts) if parts else "0"


def parse_expr(expr):
    if expr == "0":
        return 0, 0
    normalized = expr.replace(" - ", " + -")
    constant = 0
    theta_coeff = 0
    for term in normalized.split(" + "):
        if term.endswith("theta"):
            raw = term[:-5]
            if raw == "":
                theta_coeff += 1
            elif raw == "-":
                theta_coeff -= 1
            else:
                theta_coeff += int(raw)
        else:
            constant += int(term)
    return constant, theta_coeff


def parse_theta_arg(arg):
    constant, theta_coeff = parse_expr(arg)
    assert constant == 0
    return theta_coeff


def parse_problem(problem):
    match = MULTIPLY_RE.fullmatch(problem)
    if match:
        return {
            "variant": "multiply",
            "x": parse_expr(match.group(1)),
            "y": parse_expr(match.group(2)),
        }
    match = EXP_RE.fullmatch(problem)
    if match:
        return {"variant": "exponential", "k": parse_theta_arg(match.group(1))}
    match = INTEGRATE_RE.fullmatch(problem)
    if match:
        return {"variant": "integrate", "expr": parse_expr(match.group(1))}
    match = MULTIPLY_INTEGRATE_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "multiply_integrate",
        "x": parse_expr(match.group(1)),
        "y": parse_expr(match.group(2)),
    }


def multiply_steps(steps, a, b, c, d):
    constant = a * c
    ad = a * d
    bc = b * c
    bd = b * d
    theta_coeff = ad + bc
    result = grass_expr(constant, theta_coeff)
    steps.extend([
        make_step("M", a, c, constant),
        make_step("M", a, d, ad),
        make_step("M", b, c, bc),
        make_step("M", b, d, bd),
        make_step("NILPOTENT", "theta^2=0", f"{bd}theta^2", 0),
        make_step("A", ad, bc, theta_coeff),
        make_step("GRASSMANN_RESULT", f"constant={constant}",
                  f"theta={theta_coeff}", result),
    ])
    return constant, theta_coeff, result


def expected_multiply(parts):
    a, b = parts["x"]
    c, d = parts["y"]
    x = grass_expr(a, b)
    y = grass_expr(c, d)
    steps = [make_step("GRASSMANN_SETUP", "multiply", f"x={x}", f"y={y}")]
    _, _, result = multiply_steps(steps, a, b, c, d)
    answer = f"x*y = {result}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_exponential(parts):
    k = parts["k"]
    argument = theta_term(k)
    result = grass_expr(1, k)
    steps = [
        make_step("GRASSMANN_SETUP", "exponential", f"arg={argument}",
                  "theta^2=0"),
        make_step("SERIES_TERM", "n=0", 1, 1),
        make_step("SERIES_TERM", "n=1", argument, argument),
        make_step("NILPOTENT", "n>=2", "theta^2=0", 0),
        make_step("GRASSMANN_RESULT", "constant=1", f"theta={k}", result),
    ]
    answer = f"exp({argument}) = {result}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_integrate(parts):
    a, b = parts["expr"]
    expr = grass_expr(a, b)
    const_part = a * 0
    theta_part = b * 1
    integral = const_part + theta_part
    steps = [
        make_step("GRASSMANN_SETUP", "integrate", f"expr={expr}",
                  "int1=0,inttheta=1"),
        make_step("BEREZIN_RULE", "int dtheta 1", 0),
        make_step("BEREZIN_RULE", "int dtheta theta", 1),
        make_step("M", a, 0, const_part),
        make_step("M", b, 1, theta_part),
        make_step("A", const_part, theta_part, integral),
    ]
    answer = f"integral = {integral}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_multiply_integrate(parts):
    a, b = parts["x"]
    c, d = parts["y"]
    x = grass_expr(a, b)
    y = grass_expr(c, d)
    steps = [
        make_step("GRASSMANN_SETUP", "multiply_integrate",
                  f"x={x}", f"y={y}"),
    ]
    constant, theta_coeff, _ = multiply_steps(steps, a, b, c, d)
    const_part = constant * 0
    theta_part = theta_coeff * 1
    integral = const_part + theta_part
    steps.extend([
        make_step("BEREZIN_RULE", "int dtheta 1", 0),
        make_step("BEREZIN_RULE", "int dtheta theta", 1),
        make_step("M", constant, 0, const_part),
        make_step("M", theta_coeff, 1, theta_part),
        make_step("A", const_part, theta_part, integral),
    ])
    answer = f"integral = {integral}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "multiply":
        return expected_multiply(parts)
    if parts["variant"] == "exponential":
        return expected_exponential(parts)
    if parts["variant"] == "integrate":
        return expected_integrate(parts)
    return expected_multiply_integrate(parts)


class TestGrassmannGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GrassmannGenerator()

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
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in GrassmannGenerator.VARIANTS:
            result = GrassmannGenerator(variant).generate()
            self.assertEqual(result["operation"], f"grassmann_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GrassmannGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_rendering_avoids_degenerate_terms(self):
        bad = re.compile(r"(?<!\d)1theta|\+ -|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]), result["problem"])
            self.assertIsNone(bad.search(result["final_answer"]),
                              result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(200)}
        self.assertEqual(
            seen,
            {"grassmann_multiply", "grassmann_exponential",
             "grassmann_integrate", "grassmann_multiply_integrate"},
        )


if __name__ == "__main__":
    unittest.main()
