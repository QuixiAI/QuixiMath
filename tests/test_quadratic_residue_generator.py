import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quadratic_residue_generator import QuadraticResidueGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Euler's criterion to compute Legendre\((\d+),(\d+)\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(map(int, match.groups()))


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def expected_flow(a, prime):
    exponent = (prime - 1) // 2
    a_mod = a % prime
    bits = bin(exponent)[2:]
    steps = [
        make_step("LEGENDRE_SETUP", f"a={a}", f"p={prime}"),
        make_step("S", prime, 1, prime - 1),
        make_step("D", prime - 1, 2, exponent),
        make_step("MOD_REDUCE", a, f"mod {prime}", a_mod),
        make_step("BINARY_EXPONENT", exponent, bits),
    ]
    result = 1
    for idx, bit in enumerate(bits, start=1):
        squared = result * result
        reduced_square = squared % prime
        steps.append(make_step("M", result, result, squared))
        steps.append(make_step("MOD_REDUCE", squared, f"mod {prime}",
                               reduced_square))
        steps.append(make_step("MODEXP_SQUARE", f"bit {idx}={bit}",
                               reduced_square))
        result = reduced_square
        if bit == "1":
            product = result * a_mod
            reduced_product = product % prime
            steps.append(make_step("M", result, a_mod, product))
            steps.append(make_step("MOD_REDUCE", product, f"mod {prime}",
                                   reduced_product))
            steps.append(make_step("MODEXP_MULTIPLY", f"bit {idx}=1",
                                   reduced_product))
            result = reduced_product
        else:
            steps.append(make_step("MODEXP_MULTIPLY", f"bit {idx}=0",
                                   "skip"))
        steps.append(make_step("MODEXP_STATE", f"after bit {idx}", result))

    if result == 1:
        symbol = 1
        meaning = "quadratic residue"
    else:
        symbol = -1
        meaning = "quadratic nonresidue"
    steps.extend([
        make_step("EULER_CRITERION", f"{a}^{exponent} mod {prime}", result),
        make_step("LEGENDRE_RESULT", result, symbol, meaning),
    ])
    answer = f"Legendre({a},{prime}) = {symbol}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestQuadraticResidueGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuadraticResidueGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "quadratic_residue_legendre")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            a, prime = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(a, prime)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_and_legendre_value(self):
        saw = set()
        for _ in range(500):
            result = self.gen.generate()
            a, prime = parse_problem(result["problem"])
            self.assertTrue(is_prime(prime))
            expected_residue = pow(a, (prime - 1) // 2, prime)
            expected_symbol = 1 if expected_residue == 1 else -1
            saw.add(expected_symbol)
            self.assertEqual(result["final_answer"],
                             f"Legendre({a},{prime}) = {expected_symbol}")
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])
        self.assertEqual(saw, {-1, 1})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
