import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mobius_transform_generator import MobiusTransformGenerator
from helpers import DELIM


IMAGE_RE = re.compile(
    r"For T\(z\) = \(([^()]*)\)/\(([^()]*)\), compute T\((-?\d+)\)\."
)
FIXED_RE = re.compile(
    r"For T\(z\) = \(([^()]*)\)/\(([^()]*)\), find the fixed points\."
)
CROSS_RE = re.compile(
    r"Compute the cross-ratio \[z1,z2;z3,z4\] for z1=(-?\d+), "
    r"z2=(-?\d+), z3=(-?\d+), z4=(-?\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def frac_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def linear_text(coef, const):
    parts = []
    if coef != 0:
        if coef == 1:
            parts.append("z")
        elif coef == -1:
            parts.append("-z")
        else:
            parts.append(f"{coef}z")
    if const != 0:
        if not parts:
            parts.append(str(const))
        else:
            parts.append(f"+ {const}" if const > 0 else f"- {-const}")
    return " ".join(parts) if parts else "0"


def transform_text(a, b, c, d):
    return f"({linear_text(a, b)})/({linear_text(c, d)})"


def parse_linear(text):
    coef = 0
    const = 0
    for term in text.replace(" - ", " + -").split(" + "):
        if term == "z":
            coef += 1
        elif term == "-z":
            coef -= 1
        elif term.endswith("z"):
            coef += int(term[:-1])
        elif term:
            const += int(term)
    return coef, const


def parse_problem(problem):
    match = IMAGE_RE.fullmatch(problem)
    if match:
        a, b = parse_linear(match.group(1))
        c, d = parse_linear(match.group(2))
        z0 = int(match.group(3))
        return {"variant": "image", "a": a, "b": b, "c": c, "d": d,
                "z0": z0}
    match = FIXED_RE.fullmatch(problem)
    if match:
        a, b = parse_linear(match.group(1))
        c, d = parse_linear(match.group(2))
        return {"variant": "fixed_points", "a": a, "b": b, "c": c,
                "d": d}
    match = CROSS_RE.fullmatch(problem)
    assert match is not None, problem
    z1, z2, z3, z4 = map(int, match.groups())
    return {"variant": "cross_ratio", "z1": z1, "z2": z2, "z3": z3,
            "z4": z4}


def expected_image(a, b, c, d, z0):
    az = a * z0
    numerator = az + b
    cz = c * z0
    denominator = cz + d
    value = Fraction(numerator, denominator)
    steps = [
        make_step("MOBIUS_SETUP", f"T(z)={transform_text(a, b, c, d)}",
                  f"z0={z0}"),
        make_step("M", a, z0, az),
        make_step("A", az, b, numerator),
        make_step("M", c, z0, cz),
        make_step("A", cz, d, denominator),
        make_step("F", numerator, denominator, frac_text(value)),
        make_step("IMAGE", f"T({z0})", frac_text(value)),
    ]
    return steps, f"T({z0}) = {frac_text(value)}"


def expected_fixed(a, b, c, d):
    middle = d - a
    const = -b
    disc = middle * middle - 4 * c * const
    sqrt_disc = int(disc ** 0.5)
    roots = sorted([
        Fraction(-middle - sqrt_disc, 2 * c),
        Fraction(-middle + sqrt_disc, 2 * c),
    ])
    steps = [
        make_step("MOBIUS_SETUP", f"T(z)={transform_text(a, b, c, d)}",
                  "fixed points"),
        make_step("FIXED_EQ", "z=(az+b)/(cz+d)"),
        make_step("EXPAND", "c z^2 + (d-a)z - b = 0"),
        make_step("S", d, a, middle),
        make_step("S", 0, b, const),
        make_step("QUADRATIC", c, middle, const),
    ]
    for root in roots:
        square = root * root
        term1 = c * square
        term2 = middle * root
        partial = term1 + term2
        total = partial + const
        steps.extend([
            make_step("E", root, 2, square),
            make_step("M", c, square, term1),
            make_step("M", middle, root, term2),
            make_step("A", term1, term2, partial),
            make_step("A", partial, const, total),
            make_step("CHECK", f"root {frac_text(root)}", total),
            make_step("FIXED_POINT", frac_text(root)),
        ])
    answer_roots = ", ".join(frac_text(root) for root in roots)
    return steps, f"fixed points = {{{answer_roots}}}"


def expected_cross_ratio(z1, z2, z3, z4):
    a = z1 - z3
    b = z2 - z4
    c = z1 - z4
    d = z2 - z3
    numerator = a * b
    denominator = c * d
    value = Fraction(numerator, denominator)
    steps = [
        make_step("CROSS_RATIO_SETUP", f"z1={z1}", f"z2={z2}",
                  f"z3={z3}", f"z4={z4}"),
        make_step("S", z1, z3, a),
        make_step("S", z2, z4, b),
        make_step("M", a, b, numerator),
        make_step("S", z1, z4, c),
        make_step("S", z2, z3, d),
        make_step("M", c, d, denominator),
        make_step("F", numerator, denominator, frac_text(value)),
        make_step("CROSS_RATIO", frac_text(value)),
    ]
    return steps, f"cross_ratio = {frac_text(value)}"


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "image":
        steps, answer = expected_image(parts["a"], parts["b"], parts["c"],
                                       parts["d"], parts["z0"])
    elif parts["variant"] == "fixed_points":
        steps, answer = expected_fixed(parts["a"], parts["b"], parts["c"],
                                       parts["d"])
    else:
        steps, answer = expected_cross_ratio(parts["z1"], parts["z2"],
                                             parts["z3"], parts["z4"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMobiusTransformGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = MobiusTransformGenerator()

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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "F":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("image", "fixed_points", "cross_ratio"):
            gen = MobiusTransformGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"mobius_transform_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MobiusTransformGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
