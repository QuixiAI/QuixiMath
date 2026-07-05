import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.pollard_factorization_generator import PollardFactorizationGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def lcm(a, b):
    return a * b // math.gcd(a, b)


def parse_problem(problem):
    n = int(re.search(r"n=(\d+)", problem).group(1))
    if "rho" in problem:
        c = int(re.search(r"c=(\d+)", problem).group(1))
        x0 = int(re.search(r"x0=(\d+)", problem).group(1))
        return "rho", n, c, x0
    base = int(re.search(r"base=(\d+)", problem).group(1))
    bound = int(re.search(r"B=(\d+)", problem).group(1))
    return "p_minus_1", n, base, bound


def oracle(problem):
    parsed = parse_problem(problem)
    if parsed[0] == "rho":
        _, n, c, x0 = parsed
        x = x0
        y = x0
        while True:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if 1 < d < n:
                return f"factor = {d}; cofactor = {n // d}"
            if d == n:
                raise AssertionError("rho parameters failed")
    _, n, base, bound = parsed
    exponent = 1
    for value in range(2, bound + 1):
        exponent = lcm(exponent, value)
    residue = pow(base, exponent, n)
    d = math.gcd(residue - 1, n)
    return f"factor = {d}; cofactor = {n // d}"


class TestPollardFactorizationGenerator(unittest.TestCase):
    def test_contract_oracle_variants_and_arithmetic(self):
        random.seed(123)
        gen = PollardFactorizationGenerator()
        saw = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            self.assertEqual(result["final_answer"], oracle(result["problem"]))
            saw.add(result["operation"])
            factor, cofactor = map(int, re.search(
                r"factor = (\d+); cofactor = (\d+)",
                result["final_answer"],
            ).groups())
            n = int(re.search(r"n=(\d+)", result["problem"]).group(1))
            self.assertEqual(factor * cofactor, n)
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "MOD_POWER":
                    base, exp = map(int, fields[1].split("^"))
                    mod = int(fields[2].split()[1])
                    self.assertEqual(pow(base, exp, mod), int(fields[3]))
        self.assertEqual(saw, {"pollard_factorization_rho",
                               "pollard_factorization_p_minus_1"})

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            PollardFactorizationGenerator("bad")


if __name__ == "__main__":
    unittest.main()
