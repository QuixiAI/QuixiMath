import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mod_exp_generator import ModExpGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use square-and-multiply to compute (\d+)\^(\d+) modulo (\d+)\."
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


def expected_flow(base, exponent, modulus):
    base_mod = base % modulus
    bits = bin(exponent)[2:]
    steps = [
        make_step("MODEXP_SETUP", f"base {base}",
                  f"exponent {exponent}", f"modulus {modulus}"),
        make_step("MOD_REDUCE", base, f"mod {modulus}", base_mod),
        make_step("BINARY_EXPONENT", exponent, bits),
    ]
    result = 1
    for idx, bit in enumerate(bits, start=1):
        squared = result * result
        reduced_square = squared % modulus
        steps.append(make_step("M", result, result, squared))
        steps.append(make_step("MOD_REDUCE", squared, f"mod {modulus}",
                               reduced_square))
        steps.append(make_step("MODEXP_SQUARE", f"bit {idx}={bit}",
                               reduced_square))
        result = reduced_square
        if bit == "1":
            product = result * base_mod
            reduced_product = product % modulus
            steps.append(make_step("M", result, base_mod, product))
            steps.append(make_step("MOD_REDUCE", product, f"mod {modulus}",
                                   reduced_product))
            steps.append(make_step("MODEXP_MULTIPLY", f"bit {idx}=1",
                                   reduced_product))
            result = reduced_product
        else:
            steps.append(make_step("MODEXP_MULTIPLY", f"bit {idx}=0",
                                   "skip"))
        steps.append(make_step("MODEXP_STATE", f"after bit {idx}", result))
    answer = f"{base}^{exponent} mod {modulus} = {result}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestModExpGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ModExpGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "mod_exp")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            base, exponent, modulus = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(base, exponent, modulus)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_and_residue(self):
        for _ in range(300):
            result = self.gen.generate()
            base, exponent, modulus = parse_problem(result["problem"])
            expected = pow(base, exponent, modulus)
            self.assertTrue(result["final_answer"].endswith(f" = {expected}"))
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
