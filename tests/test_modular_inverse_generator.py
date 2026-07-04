import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.modular_inverse_generator import ModularInverseGenerator
from helpers import DELIM


INVERSE_RE = re.compile(
    r"Find the modular inverse of (\d+) modulo (\d+)\."
)
LINEAR_RE = re.compile(
    r"Solve the linear congruence (\d+)x congruent to (\d+) modulo (\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def list_text(values):
    return ", ".join(str(value) for value in values)


def parse_problem(problem):
    match = INVERSE_RE.fullmatch(problem)
    if match:
        a, modulus = map(int, match.groups())
        return {"variant": "inverse", "a": a, "modulus": modulus}
    match = LINEAR_RE.fullmatch(problem)
    assert match is not None, problem
    a, b, modulus = map(int, match.groups())
    return {"variant": "linear_congruence", "a": a, "b": b,
            "modulus": modulus}


def extended_trace(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    steps = [
        make_step("EXT_GCD_SETUP", a, b),
        make_step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
        make_step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
    ]
    while r != 0:
        q = old_r // r
        product = q * r
        new_r = old_r - product
        steps.append(make_step("EUCLID_DIV", old_r, r, q, new_r))
        steps.append(make_step("M", q, r, product))
        steps.append(make_step("S", old_r, product, new_r))

        qx = q * x
        new_x = old_x - qx
        steps.append(make_step("M", q, x, qx))
        steps.append(make_step("S", old_x, qx, new_x))

        qy = q * y
        new_y = old_y - qy
        steps.append(make_step("M", q, y, qy))
        steps.append(make_step("S", old_y, qy, new_y))
        steps.append(make_step("BACK_SUB_ROW", f"r={new_r}",
                               f"x={new_x}", f"y={new_y}"))

        old_r, r = r, new_r
        old_x, x = x, new_x
        old_y, y = y, new_y
    return steps, old_r, old_x, old_y


def expected_inverse(parts):
    a = parts["a"]
    modulus = parts["modulus"]
    steps = [
        make_step("MOD_SETUP", "inverse", f"a={a}", f"modulus={modulus}"),
    ]
    euclid_steps, g, x, _ = extended_trace(a, modulus)
    steps.extend(euclid_steps)
    steps.extend([
        make_step("GCD_RESULT", f"gcd({a},{modulus})", g),
        make_step("CHECK", "gcd = 1", "inverse exists"),
    ])
    inverse = x % modulus
    product = a * inverse
    reduced = product % modulus
    steps.extend([
        make_step("MOD_NORMALIZE", x, f"mod {modulus}", inverse),
        make_step("MOD_INVERSE", f"{a} mod {modulus}", inverse),
        make_step("M", a, inverse, product),
        make_step("MOD_REDUCE", product, f"mod {modulus}", reduced),
        make_step("CHECK", "a*inverse mod m", reduced),
    ])
    answer = f"{a}^-1 mod {modulus} = {inverse}"
    return steps, answer


def expected_linear(parts):
    a = parts["a"]
    b = parts["b"]
    modulus = parts["modulus"]
    d = gcd(a, modulus)
    reduced_a = a // d
    reduced_b = b // d
    reduced_modulus = modulus // d
    steps = [
        make_step("MOD_SETUP", "linear congruence", f"a={a}",
                  f"b={b}", f"modulus={modulus}"),
        make_step("GCD_RESULT", f"gcd({a},{modulus})", d),
        make_step("CHECK", f"{d} divides {b}", "solutions exist"),
        make_step("D", a, d, reduced_a),
        make_step("D", b, d, reduced_b),
        make_step("D", modulus, d, reduced_modulus),
        make_step("CONGRUENCE_REDUCE",
                  f"{reduced_a}x congruent to {reduced_b}",
                  f"mod {reduced_modulus}"),
    ]
    euclid_steps, g, x, _ = extended_trace(reduced_a, reduced_modulus)
    steps.extend(euclid_steps)
    inverse = x % reduced_modulus
    product = inverse * reduced_b
    base = product % reduced_modulus
    solutions = [base + k * reduced_modulus for k in range(d)]
    steps.extend([
        make_step("GCD_RESULT", f"gcd({reduced_a},{reduced_modulus})", g),
        make_step("MOD_NORMALIZE", x, f"mod {reduced_modulus}", inverse),
        make_step("MOD_INVERSE", f"{reduced_a} mod {reduced_modulus}",
                  inverse),
        make_step("M", inverse, reduced_b, product),
        make_step("MOD_REDUCE", product, f"mod {reduced_modulus}", base),
        make_step("CONGRUENCE_SOLUTIONS", f"base {base}",
                  f"step {reduced_modulus}", list_text(solutions)),
    ])
    answer = f"solutions mod {modulus} = {list_text(solutions)}"
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "inverse":
        steps, answer = expected_inverse(parts)
    else:
        steps, answer = expected_linear(parts)
    return steps + [make_step("Z", answer)], answer


class TestModularInverseGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ModularInverseGenerator()

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

    def test_arithmetic_and_solution_validity(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "EUCLID_DIV":
                    dividend, divisor, quotient, remainder = map(
                        int, fields[1:]
                    )
                    self.assertEqual(dividend, quotient * divisor + remainder)
                    self.assertGreaterEqual(remainder, 0)
                    self.assertLess(remainder, divisor)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "MOD_REDUCE":
                    modulus = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % modulus,
                                     int(fields[3]), raw_step)

            if parts["variant"] == "inverse":
                inv = int(result["final_answer"].rsplit(" = ", 1)[1])
                self.assertEqual((parts["a"] * inv) % parts["modulus"], 1)
            else:
                solution_text = result["final_answer"].split(" = ", 1)[1]
                solutions = [int(value) for value in solution_text.split(", ")]
                for solution in solutions:
                    self.assertEqual((parts["a"] * solution - parts["b"])
                                     % parts["modulus"], 0)
                self.assertEqual(len(solutions), gcd(parts["a"],
                                                     parts["modulus"]))

    def test_variants_are_available(self):
        expected_ops = {
            "inverse": "modular_inverse",
            "linear_congruence": "linear_congruence",
        }
        for variant in ("inverse", "linear_congruence"):
            gen = ModularInverseGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], expected_ops[variant])
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ModularInverseGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
