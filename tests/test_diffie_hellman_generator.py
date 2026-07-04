import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.diffie_hellman_generator import DiffieHellmanGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For Diffie-Hellman with prime p=(\d+), generator g=(\d+), "
    r"Alice secret a=(\d+), and Bob secret b=(\d+), compute both public "
    r"keys and the shared secret\."
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


def factor_distinct(n):
    factors = []
    d = 2
    remaining = n
    while d * d <= remaining:
        if remaining % d == 0:
            factors.append(d)
            while remaining % d == 0:
                remaining //= d
        d += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def is_primitive_root(g, p):
    return all(pow(g, (p - 1) // factor, p) != 1
               for factor in factor_distinct(p - 1))


def expected_flow(p, g, alice_secret, bob_secret):
    alice_public = pow(g, alice_secret, p)
    bob_public = pow(g, bob_secret, p)
    alice_shared = pow(bob_public, alice_secret, p)
    bob_shared = pow(alice_public, bob_secret, p)
    steps = [
        make_step("DH_SETUP", f"p={p}", f"g={g}"),
        make_step("DH_SECRET", "Alice", alice_secret),
        make_step("DH_SECRET", "Bob", bob_secret),
        make_step("MOD_POWER", f"{g}^{alice_secret}", f"mod {p}",
                  alice_public),
        make_step("DH_PUBLIC", "Alice", alice_public),
        make_step("MOD_POWER", f"{g}^{bob_secret}", f"mod {p}",
                  bob_public),
        make_step("DH_PUBLIC", "Bob", bob_public),
        make_step("MOD_POWER", f"{bob_public}^{alice_secret}", f"mod {p}",
                  alice_shared),
        make_step("DH_SHARED", "Alice", alice_shared),
        make_step("MOD_POWER", f"{alice_public}^{bob_secret}", f"mod {p}",
                  bob_shared),
        make_step("DH_SHARED", "Bob", bob_shared),
        make_step("CHECK", "shared secrets match", alice_shared),
    ]
    answer = (
        f"Alice public = {alice_public}; Bob public = {bob_public}; "
        f"shared secret = {alice_shared}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestDiffieHellmanGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DiffieHellmanGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "diffie_hellman")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            p, g, alice_secret, bob_secret = parse_problem(result["problem"])
            expected_steps, answer = expected_flow(
                p, g, alice_secret, bob_secret
            )
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_key_exchange_conditions(self):
        for _ in range(300):
            result = self.gen.generate()
            p, g, alice_secret, bob_secret = parse_problem(result["problem"])
            self.assertTrue(is_prime(p))
            self.assertTrue(is_primitive_root(g, p))
            self.assertGreaterEqual(alice_secret, 2)
            self.assertLessEqual(alice_secret, p - 2)
            self.assertGreaterEqual(bob_secret, 2)
            self.assertLessEqual(bob_secret, p - 2)
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "MOD_POWER":
                    base, exponent = map(int, fields[1].split("^"))
                    mod = int(fields[2].split()[1])
                    self.assertEqual(pow(base, exponent, mod),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
