import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quaternion_generator import QuaternionGenerator
from helpers import DELIM


ARITH_RE = re.compile(
    r"Let p=(\([^)]*\)) and q=(\([^)]*\)) represent coefficients of "
    r"1,i,j,k\. With i\^2=j\^2=k\^2=ijk=-1, compute p\*q, q\*p, "
    r"conjugate\(p\), norm\^2\(p\), and p\^-1\."
)
ROT_RE = re.compile(
    r"Let q=(\([^)]*\)) and v=(\([^)]*\)) represent a unit quaternion "
    r"and a pure-vector quaternion\. Rotate v by q\*v\*q\^-1\."
)

COMPONENTS = ["real", "i", "j", "k"]


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_number(text):
    return Fraction(text)


def number_text(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def parse_quat(text):
    body = text.strip("()")
    return tuple(parse_number(part) for part in body.split(","))


def parse_int_quat(text):
    return tuple(int(value) for value in parse_quat(text))


def quat_text(q):
    return "(" + ",".join(number_text(value) for value in q) + ")"


def vector_text(v):
    return "(" + ",".join(str(value) for value in v) + ")"


def conjugate(q):
    a, b, c, d = q
    return (a, -b, -c, -d)


def norm_squared(q):
    return sum(value * value for value in q)


def multiply(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (
        a * e - b * f - c * g - d * h,
        a * f + b * e + c * h - d * g,
        a * g - b * h + c * e + d * f,
        a * h + b * g - c * f + d * e,
    )


def inverse(q):
    n = norm_squared(q)
    return tuple(Fraction(value, n) for value in conjugate(q))


def hamilton_steps():
    return [
        make_step("HAMILTON", "i*i", "-1"),
        make_step("HAMILTON", "j*j", "-1"),
        make_step("HAMILTON", "k*k", "-1"),
        make_step("HAMILTON", "i*j", "k"),
        make_step("HAMILTON", "j*i", "-k"),
    ]


def trace_multiply(steps, left_name, left, right_name, right, result_name):
    steps.append(make_step("QUAT_MUL_START", result_name, left_name,
                           right_name))
    a, b, c, d = left
    e, f, g, h = right
    terms = [
        [(1, a, e), (-1, b, f), (-1, c, g), (-1, d, h)],
        [(1, a, f), (1, b, e), (1, c, h), (-1, d, g)],
        [(1, a, g), (-1, b, h), (1, c, e), (1, d, f)],
        [(1, a, h), (1, b, g), (-1, c, f), (1, d, e)],
    ]
    result = []
    for component, component_terms in zip(COMPONENTS, terms):
        running = Fraction(0)
        for sign, left_value, right_value in component_terms:
            product = left_value * right_value
            steps.append(make_step("M", left_value, right_value, product))
            signed = product
            if sign < 0:
                signed = -product
                steps.append(make_step("S", 0, product, signed))
            total = running + signed
            steps.append(make_step("A", running, signed, total))
            running = total
        steps.append(make_step("QUAT_COMPONENT", result_name, component,
                               running))
        result.append(running)
    steps.append(make_step("QUAT_RESULT", result_name, quat_text(result)))
    return tuple(result)


def trace_norm(steps, name, q):
    running = Fraction(0)
    for value in q:
        square = value * value
        steps.append(make_step("M", value, value, square))
        total = running + square
        steps.append(make_step("A", running, square, total))
        running = total
    steps.append(make_step("NORM_SQUARED", name, running))
    return running


def trace_inverse(steps, name, q_conj, q_norm):
    steps.append(make_step("CONJUGATE", name, quat_text(q_conj)))
    fractions = []
    for value in q_conj:
        fraction = Fraction(value, q_norm)
        steps.append(make_step("F", value, q_norm, number_text(fraction)))
        fractions.append(fraction)
    steps.append(make_step("QUAT_INVERSE", name, quat_text(fractions)))
    return tuple(fractions)


def parse_problem(problem):
    match = ARITH_RE.fullmatch(problem)
    if match:
        return {
            "variant": "arithmetic",
            "p": parse_int_quat(match.group(1)),
            "q": parse_int_quat(match.group(2)),
        }
    match = ROT_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "rotation",
        "q": parse_int_quat(match.group(1)),
        "v": parse_int_quat(match.group(2)),
    }


def expected_arithmetic(p, q):
    p = tuple(Fraction(value) for value in p)
    q = tuple(Fraction(value) for value in q)
    steps = [
        make_step("QUAT_SETUP", f"p={quat_text(p)}", f"q={quat_text(q)}"),
    ]
    steps.extend(hamilton_steps())
    pq = trace_multiply(steps, "p", p, "q", q, "p*q")
    qp = trace_multiply(steps, "q", q, "p", p, "q*p")
    p_conj = conjugate(p)
    p_norm = trace_norm(steps, "p", p)
    p_inv = trace_inverse(steps, "p", p_conj, p_norm)
    steps.append(make_step("CHECK", "p*q differs from q*p", "yes"))
    answer = (
        f"p*q = {quat_text(pq)}; q*p = {quat_text(qp)}; "
        f"conjugate(p) = {quat_text(p_conj)}; "
        f"norm^2(p) = {number_text(p_norm)}; p^-1 = {quat_text(p_inv)}"
    )
    return steps, answer


def expected_rotation(q, v):
    q = tuple(Fraction(value) for value in q)
    v = tuple(Fraction(value) for value in v)
    q_conj = conjugate(q)
    q_norm = norm_squared(q)
    q_inv = inverse(q)
    first = multiply(q, v)
    rotated = multiply(first, q_inv)
    rotated_int = tuple(int(value) for value in rotated)
    steps = [
        make_step("QUAT_SETUP", f"q={quat_text(q)}", f"v={quat_text(v)}"),
    ]
    steps.extend(hamilton_steps())
    traced_norm = trace_norm(steps, "q", q)
    steps.append(make_step("CHECK", "unit norm",
                           "yes" if traced_norm == 1 else "no"))
    steps.append(make_step("CONJUGATE", "q", quat_text(q_conj)))
    for value in q_conj:
        steps.append(make_step("F", value, q_norm,
                               number_text(Fraction(value, q_norm))))
    steps.append(make_step("QUAT_INVERSE", "q", quat_text(q_inv)))
    trace_multiply(steps, "q", q, "v", v, "q*v")
    trace_multiply(steps, "q*v", first, "q^-1", q_inv, "q*v*q^-1")
    steps.append(make_step("ROTATED_VECTOR", vector_text(rotated_int[1:])))
    answer = (
        f"qvq^-1 = {quat_text(rotated_int)}; "
        f"vector = {vector_text(rotated_int[1:])}"
    )
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "arithmetic":
        steps, answer = expected_arithmetic(parts["p"], parts["q"])
    else:
        steps, answer = expected_rotation(parts["q"], parts["v"])
    steps.append(make_step("Z", answer))
    return steps, answer


class TestQuaternionGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuaternionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(400):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_independent_quaternion_identities(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "arithmetic":
                p = tuple(Fraction(value) for value in parts["p"])
                p_inv = inverse(p)
                self.assertEqual(multiply(p, p_inv), (1, 0, 0, 0),
                                 result["problem"])
                self.assertNotEqual(multiply(p, parts["q"]),
                                    multiply(parts["q"], p),
                                    result["problem"])
            else:
                q = tuple(Fraction(value) for value in parts["q"])
                v = tuple(Fraction(value) for value in parts["v"])
                rotated = multiply(multiply(q, v), inverse(q))
                self.assertEqual(rotated[0], 0, result["problem"])
                self.assertIn(f"qvq^-1 = {quat_text(rotated)}",
                              result["final_answer"])

    def test_arithmetic_steps(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(parse_number(fields[1]) +
                                     parse_number(fields[2]),
                                     parse_number(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(parse_number(fields[1]) *
                                     parse_number(fields[2]),
                                     parse_number(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(parse_number(fields[1]) -
                                     parse_number(fields[2]),
                                     parse_number(fields[3]), raw_step)
                elif fields[0] == "F":
                    self.assertEqual(Fraction(parse_number(fields[1]),
                                              parse_number(fields[2])),
                                     parse_number(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("arithmetic", "rotation"):
            gen = QuaternionGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"quaternion_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            QuaternionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
