import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.jacobi_symbol_generator import JacobiSymbolGenerator
from helpers import DELIM
from tests.new_generator_test_utils import assert_contract, assert_pipe_safe


def parse_problem(problem):
    patterns = [
        r"\((\d+)/(\d+)\)",
        r"Jacobi\((\d+),(\d+)\)",
        r"a=(\d+) and odd modulus n=(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, problem)
        if match:
            return int(match.group(1)), int(match.group(2))
    raise AssertionError(problem)


def factor(n):
    out = []
    d = 2
    while d * d <= n:
        count = 0
        while n % d == 0:
            count += 1
            n //= d
        if count:
            out.append((d, count))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return 1 if value == 1 else -1


def jacobi(a, n):
    if math.gcd(a, n) != 1:
        return 0
    result = 1
    for p, exp in factor(n):
        result *= legendre(a, p) ** exp
    return result


class TestJacobiSymbolGenerator(unittest.TestCase):
    def test_contract_oracle_arithmetic_and_phrasing(self):
        random.seed(123)
        gen = JacobiSymbolGenerator()
        openings = set()
        for _ in range(300):
            result = gen.generate()
            assert_contract(self, result)
            assert_pipe_safe(self, result)
            a, n = parse_problem(result["problem"])
            self.assertEqual(result["final_answer"],
                             f"Jacobi({a},{n}) = {jacobi(a, n)}")
            openings.add(result["problem"].split(" ", 2)[0])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]))
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]))
        self.assertGreaterEqual(len(openings), 2)


if __name__ == "__main__":
    unittest.main()
