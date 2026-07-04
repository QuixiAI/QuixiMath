import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.spherical_triangle_generator import SphericalTriangleGenerator
from helpers import DELIM


COS_RE = re.compile(
    r"In a spherical triangle, sides b=(\d+) deg and c=(\d+) deg "
    r"enclose angle A=(\d+) deg\. Given cos\(b\)=([^,]+), "
    r"cos\(c\)=([^,]+), sin\(b\)=([^,]+), sin\(c\)=([^,]+), "
    r"and cos\(A\)=([^,]+), use the spherical law of cosines to "
    r"find cos\(a\)\."
)
SIN_RE = re.compile(
    r"In a spherical triangle, side a=(\d+) deg, side b=(\d+) deg, "
    r"and angle A=(\d+) deg\. Given sin\(a\)=([^,]+), "
    r"sin\(b\)=([^,]+), and sin\(A\)=([^,]+), use the spherical "
    r"law of sines to find sin\(B\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def simplify_sqrt(radicand):
    outside = 1
    factor = 2
    while factor * factor <= radicand:
        square = factor * factor
        while radicand % square == 0:
            outside *= factor
            radicand //= square
        factor += 1
    return outside, radicand


def exact_term(radicand, coefficient):
    coefficient = Fraction(coefficient)
    if coefficient == 0:
        return {}
    outside, squarefree = simplify_sqrt(radicand)
    return {squarefree: coefficient * outside}


def exact_add(left, right):
    result = dict(left)
    for radicand, coefficient in right.items():
        result[radicand] = result.get(radicand, Fraction(0)) + coefficient
        if result[radicand] == 0:
            del result[radicand]
    return result


def exact_mul(left, right):
    result = {}
    for left_rad, left_coef in left.items():
        for right_rad, right_coef in right.items():
            outside, squarefree = simplify_sqrt(left_rad * right_rad)
            coefficient = left_coef * right_coef * outside
            result[squarefree] = result.get(squarefree, Fraction(0)) + \
                coefficient
            if result[squarefree] == 0:
                del result[squarefree]
    return result


def exact_div_monomial(numerator, denominator):
    if len(numerator) != 1 or len(denominator) != 1:
        raise AssertionError((numerator, denominator))
    num_rad, num_coef = next(iter(numerator.items()))
    den_rad, den_coef = next(iter(denominator.items()))
    outside, squarefree = simplify_sqrt(num_rad * den_rad)
    coefficient = num_coef * outside / (den_coef * den_rad)
    return exact_term(squarefree, coefficient)


def radical_term_text(radicand, coefficient):
    coefficient = Fraction(coefficient)
    sign = "-" if coefficient < 0 else ""
    coefficient = abs(coefficient)
    if radicand == 1:
        return sign + str(coefficient)
    root = f"sqrt({radicand})"
    if coefficient == 1:
        body = root
    elif coefficient.denominator == 1:
        body = f"{coefficient.numerator}{root}"
    elif coefficient.numerator == 1:
        body = f"{root}/{coefficient.denominator}"
    else:
        body = f"{coefficient.numerator}{root}/{coefficient.denominator}"
    return sign + body


def exact_text(value):
    if not value:
        return "0"
    parts = []
    for radicand in sorted(value):
        text = radical_term_text(radicand, value[radicand])
        if not parts:
            parts.append(text)
        elif text.startswith("-"):
            parts.append(f"- {text[1:]}")
        else:
            parts.append(f"+ {text}")
    return " ".join(parts)


def parse_term(text):
    text = text.strip()
    sign = -1 if text.startswith("-") else 1
    if text.startswith(("-", "+")):
        text = text[1:].strip()
    root_match = re.fullmatch(r"(?:(\d+))?sqrt\((\d+)\)(?:/(\d+))?", text)
    if root_match:
        numerator = int(root_match.group(1) or 1)
        radicand = int(root_match.group(2))
        denominator = int(root_match.group(3) or 1)
        return exact_term(radicand, Fraction(sign * numerator, denominator))
    frac_match = re.fullmatch(r"(\d+)(?:/(\d+))?", text)
    assert frac_match is not None, text
    numerator = int(frac_match.group(1))
    denominator = int(frac_match.group(2) or 1)
    return exact_term(1, Fraction(sign * numerator, denominator))


def parse_exact(text):
    if text == "0":
        return {}
    normalized = text.replace(" - ", " + -")
    result = {}
    for raw_term in normalized.split(" + "):
        result = exact_add(result, parse_term(raw_term))
    return result


def parse_problem(problem):
    match = COS_RE.fullmatch(problem)
    if match:
        return {
            "variant": "cosines",
            "b": int(match.group(1)),
            "c": int(match.group(2)),
            "angle_a": int(match.group(3)),
            "cos_b": match.group(4),
            "cos_c": match.group(5),
            "sin_b": match.group(6),
            "sin_c": match.group(7),
            "cos_angle_a": match.group(8),
        }
    match = SIN_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "sines",
        "side_a": int(match.group(1)),
        "side_b": int(match.group(2)),
        "angle_a": int(match.group(3)),
        "sin_a": match.group(4),
        "sin_b": match.group(5),
        "sin_angle_a": match.group(6),
    }


def expected_cosines(parts):
    cos_product = exact_mul(parse_exact(parts["cos_b"]),
                            parse_exact(parts["cos_c"]))
    sin_product = exact_mul(parse_exact(parts["sin_b"]),
                            parse_exact(parts["sin_c"]))
    mixed_product = exact_mul(sin_product,
                              parse_exact(parts["cos_angle_a"]))
    target = exact_add(cos_product, mixed_product)
    steps = [
        make_step("SPHERICAL_TRIANGLE_SETUP",
                  f"b={parts['b']} deg, c={parts['c']} deg, "
                  f"A={parts['angle_a']} deg", "find cos(a)"),
        make_step("SPHERICAL_COSINE_LAW",
                  "cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)"),
        make_step("TRIG_VALUE", f"cos(b)={parts['cos_b']}",
                  f"cos(c)={parts['cos_c']}",
                  f"cos(A)={parts['cos_angle_a']}"),
        make_step("TRIG_VALUE", f"sin(b)={parts['sin_b']}",
                  f"sin(c)={parts['sin_c']}"),
        make_step("M", parts["cos_b"], parts["cos_c"],
                  exact_text(cos_product)),
        make_step("M", parts["sin_b"], parts["sin_c"],
                  exact_text(sin_product)),
        make_step("M", exact_text(sin_product), parts["cos_angle_a"],
                  exact_text(mixed_product)),
        make_step("A", exact_text(cos_product),
                  exact_text(mixed_product), exact_text(target)),
    ]
    answer = f"cos(a) = {exact_text(target)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_sines(parts):
    product = exact_mul(parse_exact(parts["sin_b"]),
                        parse_exact(parts["sin_angle_a"]))
    target = exact_div_monomial(product, parse_exact(parts["sin_a"]))
    steps = [
        make_step("SPHERICAL_TRIANGLE_SETUP",
                  f"a={parts['side_a']} deg, b={parts['side_b']} deg, "
                  f"A={parts['angle_a']} deg", "find sin(B)"),
        make_step("SPHERICAL_SINE_LAW",
                  "sin(A)/sin(a)=sin(B)/sin(b)"),
        make_step("TRIG_VALUE", f"sin(a)={parts['sin_a']}",
                  f"sin(b)={parts['sin_b']}",
                  f"sin(A)={parts['sin_angle_a']}"),
        make_step("M", parts["sin_b"], parts["sin_angle_a"],
                  exact_text(product)),
        make_step("D", exact_text(product), parts["sin_a"],
                  exact_text(target)),
    ]
    answer = f"sin(B) = {exact_text(target)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "cosines":
        return expected_cosines(parts)
    return expected_sines(parts)


class TestSphericalTriangleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SphericalTriangleGenerator()

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
                    self.assertEqual(
                        exact_text(exact_mul(parse_exact(fields[1]),
                                             parse_exact(fields[2]))),
                        fields[3], raw_step)
                elif fields[0] == "A":
                    self.assertEqual(
                        exact_text(exact_add(parse_exact(fields[1]),
                                             parse_exact(fields[2]))),
                        fields[3], raw_step)
                elif fields[0] == "D":
                    self.assertEqual(
                        exact_text(exact_div_monomial(
                            parse_exact(fields[1]), parse_exact(fields[2]))),
                        fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in ("cosines", "sines"):
            gen = SphericalTriangleGenerator(variant)
            for _ in range(30):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"spherical_triangle_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            SphericalTriangleGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
