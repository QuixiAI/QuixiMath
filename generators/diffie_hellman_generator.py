import random

from base_generator import ProblemGenerator
from helpers import step, jid


PRIMES = [17, 19, 23, 29, 31, 37, 41, 43]


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
    for factor in factor_distinct(p - 1):
        if pow(g, (p - 1) // factor, p) == 1:
            return False
    return True


def primitive_root(p):
    roots = [g for g in range(2, p) if is_primitive_root(g, p)]
    return random.choice(roots)


class DiffieHellmanGenerator(ProblemGenerator):
    """
    Diffie-Hellman key exchange over a small prime field.

    Op-codes used:
    - DH_SETUP / DH_SECRET: public parameters and private exponents
    - MOD_POWER / DH_PUBLIC / DH_SHARED: public keys and shared secrets
    - CHECK: both parties agree
    - Z: public keys and shared secret
    """

    def generate(self) -> dict:
        p = random.choice(PRIMES)
        g = primitive_root(p)
        alice_secret = random.randint(2, p - 2)
        bob_secret = random.randint(2, p - 2)

        alice_public = pow(g, alice_secret, p)
        bob_public = pow(g, bob_secret, p)
        alice_shared = pow(bob_public, alice_secret, p)
        bob_shared = pow(alice_public, bob_secret, p)

        steps = [
            step("DH_SETUP", f"p={p}", f"g={g}"),
            step("DH_SECRET", "Alice", alice_secret),
            step("DH_SECRET", "Bob", bob_secret),
            step("MOD_POWER", f"{g}^{alice_secret}", f"mod {p}",
                 alice_public),
            step("DH_PUBLIC", "Alice", alice_public),
            step("MOD_POWER", f"{g}^{bob_secret}", f"mod {p}",
                 bob_public),
            step("DH_PUBLIC", "Bob", bob_public),
            step("MOD_POWER", f"{bob_public}^{alice_secret}", f"mod {p}",
                 alice_shared),
            step("DH_SHARED", "Alice", alice_shared),
            step("MOD_POWER", f"{alice_public}^{bob_secret}", f"mod {p}",
                 bob_shared),
            step("DH_SHARED", "Bob", bob_shared),
            step("CHECK", "shared secrets match", alice_shared),
        ]
        answer = (
            f"Alice public = {alice_public}; Bob public = {bob_public}; "
            f"shared secret = {alice_shared}"
        )
        problem = (
            f"For Diffie-Hellman with prime p={p}, generator g={g}, "
            f"Alice secret a={alice_secret}, and Bob secret b={bob_secret}, "
            f"compute both public keys and the shared secret."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="diffie_hellman",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
