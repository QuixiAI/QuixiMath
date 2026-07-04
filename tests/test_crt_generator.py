import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.crt_generator import CRTGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Solve the CRT system (.+)\. Give the least nonnegative solution "
    r"modulo the product\."
)
CLAUSE_RE = re.compile(r"x congruent to (\d+) modulo (\d+)")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def product(values):
    out = 1
    for value in values:
        out *= value
    return out


def inverse_mod(a, modulus):
    residue = a % modulus
    for candidate in range(modulus):
        if (residue * candidate) % modulus == 1:
            return candidate
    raise AssertionError("inverse does not exist")


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    residues = []
    moduli = []
    for clause in match.group(1).split("; "):
        clause_match = CLAUSE_RE.fullmatch(clause)
        assert clause_match is not None, clause
        residue, modulus = map(int, clause_match.groups())
        residues.append(residue)
        moduli.append(modulus)
    return residues, moduli


def expected_flow(residues, moduli):
    count = len(moduli)
    total_modulus = product(moduli)
    steps = [
        make_step("CRT_SETUP", f"{count} congruences"),
        make_step("CRT_TOTAL_MODULUS", list_text(moduli), total_modulus),
    ]
    for idx, (residue, modulus) in enumerate(zip(residues, moduli), start=1):
        steps.append(make_step("CRT_CONGRUENCE", f"i={idx}",
                               f"x={residue}", f"mod {modulus}"))

    running_sum = 0
    for idx, (residue, modulus) in enumerate(zip(residues, moduli), start=1):
        partial = total_modulus // modulus
        inverse = inverse_mod(partial, modulus)
        steps.append(make_step("D", total_modulus, modulus, partial))
        steps.append(make_step("CRT_FACTOR", f"i={idx}",
                               f"M_i={partial}", f"mod {modulus}"))
        steps.append(make_step("MOD_INVERSE", f"{partial} mod {modulus}",
                               inverse))
        first_product = residue * partial
        term = first_product * inverse
        steps.append(make_step("M", residue, partial, first_product))
        steps.append(make_step("M", first_product, inverse, term))
        steps.append(make_step("CRT_TERM", f"i={idx}", term))
        new_sum = running_sum + term
        steps.append(make_step("A", running_sum, term, new_sum))
        running_sum = new_sum

    solution = running_sum % total_modulus
    steps.append(make_step("MOD_REDUCE", running_sum,
                           f"mod {total_modulus}", solution))
    for idx, (residue, modulus) in enumerate(zip(residues, moduli), start=1):
        check = solution % modulus
        steps.append(make_step("MOD_REDUCE", solution, f"mod {modulus}",
                               check))
        steps.append(make_step("CRT_CHECK", f"i={idx}", check, residue))

    answer = f"x = {solution} mod {total_modulus}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCRTGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = CRTGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "crt")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            residues, moduli = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(residues, moduli)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_solution_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            residues, moduli = parse_problem(result["problem"])
            self.assertTrue(all(gcd(a, b) == 1
                                for i, a in enumerate(moduli)
                                for b in moduli[i + 1:]))
            answer_match = re.fullmatch(r"x = (\d+) mod (\d+)",
                                        result["final_answer"])
            self.assertIsNotNone(answer_match)
            solution, modulus = map(int, answer_match.groups())
            self.assertEqual(modulus, product(moduli))
            for residue, mod in zip(residues, moduli):
                self.assertEqual(solution % mod, residue)

            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
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
