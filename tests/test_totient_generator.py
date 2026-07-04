import os
import random
import re
import sys
import unittest
from math import gcd

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.totient_generator import TotientGenerator
from helpers import DELIM


TOTIENT_RE = re.compile(r"Compute Euler's totient phi\((\d+)\)\.")
EULER_RE = re.compile(
    r"Use Euler's theorem to reduce (\d+)\^(\d+) modulo (\d+)\."
)
FERMAT_RE = re.compile(
    r"Use Fermat's little theorem to reduce (\d+)\^(\d+) modulo (\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def factorization(n):
    out = []
    d = 2
    remaining = n
    while d * d <= remaining:
        if remaining % d == 0:
            count = 0
            while remaining % d == 0:
                remaining //= d
                count += 1
            out.append((d, count))
        d += 1 if d == 2 else 2
    if remaining > 1:
        out.append((remaining, 1))
    return out


def factor_text(factors):
    return " * ".join(
        f"{prime}^{exp}" if exp > 1 else str(prime)
        for prime, exp in factors
    )


def parse_problem(problem):
    match = TOTIENT_RE.fullmatch(problem)
    if match:
        return {"variant": "totient", "n": int(match.group(1))}
    match = EULER_RE.fullmatch(problem)
    if match:
        base, exponent, n = map(int, match.groups())
        return {"variant": "euler_power", "base": base,
                "exponent": exponent, "n": n}
    match = FERMAT_RE.fullmatch(problem)
    assert match is not None, problem
    base, exponent, prime = map(int, match.groups())
    return {"variant": "fermat_power", "base": base,
            "exponent": exponent, "prime": prime}


def totient_steps(n):
    factors = factorization(n)
    steps = [
        make_step("FACTOR_SETUP", n),
    ]
    for prime, exp in factors:
        steps.append(make_step("FACTOR_FOUND", prime, exp))
    steps.append(make_step("FACTOR_FORM", n, factor_text(factors)))

    result = n
    for prime, _ in factors:
        quotient = result // prime
        prime_minus_one = prime - 1
        new_result = quotient * prime_minus_one
        steps.append(make_step("D", result, prime, quotient))
        steps.append(make_step("S", prime, 1, prime_minus_one))
        steps.append(make_step("M", quotient, prime_minus_one, new_result))
        steps.append(make_step("PHI_STEP", f"p={prime}", new_result))
        result = new_result
    steps.append(make_step("TOTIENT_RESULT", f"phi({n})", result))
    return steps, result


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "totient":
        steps, phi = totient_steps(parts["n"])
        answer = f"phi({parts['n']}) = {phi}"
    elif parts["variant"] == "euler_power":
        n = parts["n"]
        base = parts["base"]
        exponent = parts["exponent"]
        steps, phi = totient_steps(n)
        g = gcd(base, n)
        reduced_exp = exponent % phi
        value = pow(base, reduced_exp, n)
        steps.extend([
            make_step("GCD_RESULT", f"gcd({base},{n})", g),
            make_step("CHECK", "gcd = 1", "Euler applies"),
            make_step("MOD_REDUCE", exponent, f"mod {phi}", reduced_exp),
            make_step("POWER_REDUCE", f"{base}^{exponent}",
                      f"{base}^{reduced_exp} mod {n}"),
            make_step("MOD_POWER", f"{base}^{reduced_exp}", f"mod {n}",
                      value),
        ])
        answer = f"{base}^{exponent} mod {n} = {value}"
    else:
        prime = parts["prime"]
        base = parts["base"]
        exponent = parts["exponent"]
        phi = prime - 1
        reduced_exp = exponent % phi
        value = pow(base, reduced_exp, prime)
        steps = [
            make_step("FERMAT_SETUP", f"prime {prime}", f"base {base}",
                      f"exponent {exponent}"),
            make_step("S", prime, 1, phi),
            make_step("TOTIENT_RESULT", f"phi({prime})", phi),
            make_step("CHECK", f"{prime} does not divide {base}",
                      "Fermat applies"),
            make_step("MOD_REDUCE", exponent, f"mod {phi}", reduced_exp),
            make_step("POWER_REDUCE", f"{base}^{exponent}",
                      f"{base}^{reduced_exp} mod {prime}"),
            make_step("MOD_POWER", f"{base}^{reduced_exp}",
                      f"mod {prime}", value),
        ]
        answer = f"{base}^{exponent} mod {prime} = {value}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestTotientGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TotientGenerator()

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

    def test_arithmetic_and_theorem_conditions(self):
        for _ in range(300):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "euler_power":
                self.assertEqual(gcd(parts["base"], parts["n"]), 1)
            elif parts["variant"] == "fermat_power":
                self.assertNotEqual(parts["base"] % parts["prime"], 0)

            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "D":
                    self.assertEqual(int(fields[1]) // int(fields[2]),
                                     int(fields[3]), raw_step)
                    self.assertEqual(int(fields[1]) % int(fields[2]), 0)
                elif fields[0] == "S":
                    self.assertEqual(int(fields[1]) - int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "MOD_REDUCE":
                    mod = int(fields[2].split()[1])
                    self.assertEqual(int(fields[1]) % mod, int(fields[3]),
                                     raw_step)
                elif fields[0] == "MOD_POWER":
                    base_exp = fields[1].split("^")
                    base, exponent = map(int, base_exp)
                    mod = int(fields[2].split()[1])
                    self.assertEqual(pow(base, exponent, mod),
                                     int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("totient", "euler_power", "fermat_power"):
            gen = TotientGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"], f"totient_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TotientGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
