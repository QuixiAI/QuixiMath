import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.finite_field_generator import FiniteFieldGenerator
from helpers import DELIM


ZP_RE = re.compile(
    r"Over Z_(\d+), compute \(f \+ g\) and \(f \* g\) for "
    r"f\(x\) = (.+) and g\(x\) = (.+)\."
)
GF2_RE = re.compile(
    r"Over GF\(2\), divide (.+) by (.+)\. "
    r"Use XOR for coefficient arithmetic\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def trim(poly):
    poly = poly[:]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def degree(poly):
    return len(trim(poly)) - 1


def degree_text(power):
    if power == 0:
        return "x^0"
    if power == 1:
        return "x"
    return f"x^{power}"


def term_text(coef, power):
    if coef == 0:
        return ""
    if power == 0:
        return str(coef)
    variable = "x" if power == 1 else f"x^{power}"
    if coef == 1:
        return variable
    return f"{coef}{variable}"


def poly_text(poly):
    poly = trim(poly)
    terms = []
    for power in range(len(poly) - 1, -1, -1):
        text = term_text(poly[power], power)
        if text:
            terms.append(text)
    return " + ".join(terms) if terms else "0"


def parse_poly(text):
    if text == "0":
        return [0]
    coefs = {}
    for term in text.split(" + "):
        if "x" not in term:
            power = 0
            coef = int(term)
        else:
            match = re.fullmatch(r"(\d*)x(?:\^(\d+))?", term)
            assert match is not None, term
            coef = int(match.group(1)) if match.group(1) else 1
            power = int(match.group(2)) if match.group(2) else 1
        coefs[power] = coefs.get(power, 0) + coef
    poly = [0] * (max(coefs) + 1)
    for power, coef in coefs.items():
        poly[power] = coef
    return trim(poly)


def add_mod(f, g, modulus):
    size = max(len(f), len(g))
    result = []
    for idx in range(size):
        result.append(((f[idx] if idx < len(f) else 0) +
                       (g[idx] if idx < len(g) else 0)) % modulus)
    return trim(result)


def multiply_mod(f, g, modulus):
    raw = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            raw[i + j] += a * b
    return trim([value % modulus for value in raw])


def parse_problem(problem):
    match = ZP_RE.fullmatch(problem)
    if match:
        modulus = int(match.group(1))
        return {
            "variant": "zp",
            "modulus": modulus,
            "f": parse_poly(match.group(2)),
            "g": parse_poly(match.group(3)),
        }
    match = GF2_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "gf2_division",
        "dividend": parse_poly(match.group(1)),
        "divisor": parse_poly(match.group(2)),
    }


def expected_zp(modulus, f, g):
    steps = [
        make_step("FIELD_SETUP", f"Z_{modulus}[x]", f"mod {modulus}"),
        make_step("POLY_INPUT", "f(x)", poly_text(f)),
        make_step("POLY_INPUT", "g(x)", poly_text(g)),
        make_step("POLY_ADD_START",
                  f"max degree {max(degree(f), degree(g))}"),
    ]
    sum_coeffs = []
    for power in range(max(len(f), len(g))):
        a = f[power] if power < len(f) else 0
        b = g[power] if power < len(g) else 0
        raw = a + b
        reduced = raw % modulus
        steps.append(make_step("A", a, b, raw))
        steps.append(make_step("MOD_REDUCE", raw, f"mod {modulus}",
                               reduced))
        steps.append(make_step("POLY_COEFF", "sum", degree_text(power),
                               reduced))
        sum_coeffs.append(reduced)
    sum_coeffs = trim(sum_coeffs)

    raw_product = [0] * (len(f) + len(g) - 1)
    steps.append(make_step("POLY_MUL_START", f"degree {degree(f)}",
                           f"degree {degree(g)}"))
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            product = a * b
            power = i + j
            previous = raw_product[power]
            total = previous + product
            steps.append(make_step("M", a, b, product))
            steps.append(make_step("A", previous, product, total))
            raw_product[power] = total
            steps.append(make_step("POLY_ACCUM", degree_text(power), total))

    product_coeffs = []
    for power, value in enumerate(raw_product):
        reduced = value % modulus
        steps.append(make_step("MOD_REDUCE", value, f"mod {modulus}",
                               reduced))
        steps.append(make_step("POLY_COEFF", "product", degree_text(power),
                               reduced))
        product_coeffs.append(reduced)
    product_coeffs = trim(product_coeffs)
    answer = (
        f"sum = {poly_text(sum_coeffs)}; "
        f"product = {poly_text(product_coeffs)}"
    )
    return steps, answer


def expected_gf2_division(dividend, divisor):
    steps = [
        make_step("FIELD_SETUP", "GF(2)[x]", "addition is XOR"),
        make_step("POLYDIV_SETUP", poly_text(dividend), poly_text(divisor)),
    ]
    remainder = trim(dividend)
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    div_degree = degree(divisor)
    while not (len(remainder) == 1 and remainder[0] == 0):
        rem_degree = degree(remainder)
        if rem_degree < div_degree:
            break
        shift = rem_degree - div_degree
        steps.append(make_step("DIV_TERM", degree_text(rem_degree),
                               degree_text(div_degree), degree_text(shift)))
        before_q = quotient[shift]
        quotient[shift] ^= 1
        steps.append(make_step("GF2_XOR", f"quotient {degree_text(shift)}",
                               f"{before_q} xor 1", quotient[shift]))
        for idx, coeff in enumerate(divisor):
            if coeff == 0:
                continue
            power = idx + shift
            before = remainder[power]
            after = before ^ coeff
            steps.append(make_step("GF2_XOR", f"remainder {degree_text(power)}",
                                   f"{before} xor {coeff}", after))
            remainder[power] = after
        remainder = trim(remainder)
        steps.append(make_step("POLY_REMAINDER", poly_text(remainder)))

    quotient = trim(quotient)
    remainder = trim(remainder)
    quotient_text = poly_text(quotient)
    remainder_text = poly_text(remainder)
    steps.extend([
        make_step("QUOTIENT", quotient_text),
        make_step("R", remainder_text),
    ])
    answer = f"quotient = {quotient_text}; remainder = {remainder_text}"
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "zp":
        steps, answer = expected_zp(parts["modulus"], parts["f"],
                                    parts["g"])
    else:
        steps, answer = expected_gf2_division(parts["dividend"],
                                              parts["divisor"])
    steps.append(make_step("Z", answer))
    return steps, answer


def gf2_add(f, g):
    size = max(len(f), len(g))
    result = []
    for idx in range(size):
        result.append((f[idx] if idx < len(f) else 0) ^
                      (g[idx] if idx < len(g) else 0))
    return trim(result)


def gf2_multiply(f, g):
    raw = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            raw[i + j] ^= (a & b)
    return trim(raw)


class TestFiniteFieldGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FiniteFieldGenerator()

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

    def test_independent_polynomial_identities(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "zp":
                expected_sum = add_mod(parts["f"], parts["g"],
                                       parts["modulus"])
                expected_product = multiply_mod(parts["f"], parts["g"],
                                                parts["modulus"])
                self.assertIn(f"sum = {poly_text(expected_sum)}",
                              result["final_answer"])
                self.assertIn(f"product = {poly_text(expected_product)}",
                              result["final_answer"])
            else:
                q_part, r_part = result["final_answer"].split("; ")
                quotient = parse_poly(q_part.removeprefix("quotient = "))
                remainder = parse_poly(r_part.removeprefix("remainder = "))
                rebuilt = gf2_add(gf2_multiply(quotient, parts["divisor"]),
                                  remainder)
                self.assertEqual(rebuilt, parts["dividend"],
                                 result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    modulus = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % modulus,
                                     int(fields[3]), raw_step)
                elif fields[0] == "GF2_XOR":
                    left, right = fields[2].split(" xor ")
                    self.assertEqual(int(left) ^ int(right), int(fields[3]),
                                     raw_step)

    def test_variants_are_available(self):
        for variant in ("zp", "gf2_division"):
            gen = FiniteFieldGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"finite_field_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            FiniteFieldGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
