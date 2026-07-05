import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.elliptic_curve_finite_field_generator import (
    EllipticCurveFiniteFieldGenerator,
)
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def point_text(point):
    return "O" if point is None else f"({point[0]},{point[1]})"


def parse_point(text):
    if text == "O":
        return None
    x, y = re.fullmatch(r"\((\d+),(\d+)\)", text).groups()
    return int(x), int(y)


def inv_mod(value, p):
    return pow(value % p, -1, p)


def add(P, Q, p, a):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        slope = ((3 * x1 * x1 + a) * inv_mod(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * inv_mod(x2 - x1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def parse_problem(problem):
    p = int(re.search(r"F_(\d+)", problem).group(1))
    a, b = map(int, re.search(r"x\^3 \+ (\d+)x \+ (\d+)", problem).groups())
    if "P + Q" in problem:
        P, Q = re.search(r"P=(\(\d+,\d+\)) and Q=(\(\d+,\d+\))",
                         problem).groups()
        return "add", p, a, b, parse_point(P), parse_point(Q), None
    if re.search(r"compute 2P", problem, re.IGNORECASE):
        P = re.search(r"P=(\(\d+,\d+\))", problem).group(1)
        return "double", p, a, b, parse_point(P), parse_point(P), None
    k, P = re.search(r"compute (\d+)P for P=(\(\d+,\d+\))",
                     problem, re.IGNORECASE).groups()
    return "scalar", p, a, b, parse_point(P), None, int(k)


def oracle(problem):
    variant, p, a, _, P, Q, k = parse_problem(problem)
    if variant == "add":
        return f"P+Q = {point_text(add(P, Q, p, a))}"
    if variant == "double":
        return f"2P = {point_text(add(P, P, p, a))}"
    acc = None
    for _ in range(k):
        acc = add(acc, P, p, a)
    return f"{k}P = {point_text(acc)}"


class TestEllipticCurveFiniteFieldGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_arithmetic(self):
        random.seed(123)
        gen = EllipticCurveFiniteFieldGenerator()
        saw = set()
        openings = set()
        for _ in range(200):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            openings.add(result["problem"].split(" ", 2)[0])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]))
        self.assertEqual(saw, {f"elliptic_curve_finite_field_{v}"
                               for v in EllipticCurveFiniteFieldGenerator.VARIANTS})
        self.assertGreaterEqual(len(openings), 2)

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            EllipticCurveFiniteFieldGenerator("bad")


if __name__ == "__main__":
    unittest.main()
