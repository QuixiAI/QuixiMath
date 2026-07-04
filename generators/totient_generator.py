import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


COMPOSITES = [12, 15, 18, 20, 21, 24, 28, 30, 35, 36, 40, 42,
              45, 48, 54, 56, 60, 63, 70, 72, 84, 90]
PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


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


class TotientGenerator(ProblemGenerator):
    """
    Euler totient computation and Fermat/Euler power reductions.

    Variants:
    - totient: compute phi(n) from the prime factorization
    - euler_power: reduce a^k modulo composite n using Euler's theorem
    - fermat_power: reduce a^k modulo prime p using Fermat's little theorem

    Op-codes used:
    - FACTOR_SETUP / FACTOR_FOUND: prime factorization context
    - PHI_STEP / TOTIENT_RESULT: totient product updates
    - FERMAT_SETUP / POWER_REDUCE / MOD_POWER: theorem reduction
    - D / S / M / MOD_REDUCE / GCD_RESULT / CHECK (established/shared)
    - Z: final totient or residue
    """

    VARIANTS = ["totient", "euler_power", "fermat_power"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "totient":
            problem, steps, answer = self._generate_totient()
        elif variant == "euler_power":
            problem, steps, answer = self._generate_euler_power()
        else:
            problem, steps, answer = self._generate_fermat_power()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"totient_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _totient_steps(self, n):
        factors = factorization(n)
        steps = [
            step("FACTOR_SETUP", n),
        ]
        for prime, exp in factors:
            steps.append(step("FACTOR_FOUND", prime, exp))
        steps.append(step("FACTOR_FORM", n, factor_text(factors)))

        result = n
        for prime, _ in factors:
            quotient = result // prime
            prime_minus_one = prime - 1
            new_result = quotient * prime_minus_one
            steps.append(step("D", result, prime, quotient))
            steps.append(step("S", prime, 1, prime_minus_one))
            steps.append(step("M", quotient, prime_minus_one, new_result))
            steps.append(step("PHI_STEP", f"p={prime}", new_result))
            result = new_result
        steps.append(step("TOTIENT_RESULT", f"phi({n})", result))
        return steps, result

    def _generate_totient(self):
        n = random.choice(COMPOSITES + PRIMES)
        steps, phi = self._totient_steps(n)
        answer = f"phi({n}) = {phi}"
        problem = f"Compute Euler's totient phi({n})."
        return problem, steps, answer

    def _generate_euler_power(self):
        n = random.choice(COMPOSITES)
        while True:
            base = random.randint(2, 80)
            if gcd(base, n) == 1:
                break
        exponent = random.randint(30, 250)
        steps, phi = self._totient_steps(n)
        g = gcd(base, n)
        reduced_exp = exponent % phi
        value = pow(base, reduced_exp, n)
        steps.extend([
            step("GCD_RESULT", f"gcd({base},{n})", g),
            step("CHECK", "gcd = 1", "Euler applies"),
            step("MOD_REDUCE", exponent, f"mod {phi}", reduced_exp),
            step("POWER_REDUCE", f"{base}^{exponent}",
                 f"{base}^{reduced_exp} mod {n}"),
            step("MOD_POWER", f"{base}^{reduced_exp}", f"mod {n}", value),
        ])
        answer = f"{base}^{exponent} mod {n} = {value}"
        problem = (
            f"Use Euler's theorem to reduce {base}^{exponent} modulo {n}."
        )
        return problem, steps, answer

    def _generate_fermat_power(self):
        prime = random.choice(PRIMES)
        while True:
            base = random.randint(2, 80)
            if base % prime != 0:
                break
        exponent = random.randint(30, 250)
        phi = prime - 1
        reduced_exp = exponent % phi
        value = pow(base, reduced_exp, prime)
        steps = [
            step("FERMAT_SETUP", f"prime {prime}", f"base {base}",
                 f"exponent {exponent}"),
            step("S", prime, 1, phi),
            step("TOTIENT_RESULT", f"phi({prime})", phi),
            step("CHECK", f"{prime} does not divide {base}",
                 "Fermat applies"),
            step("MOD_REDUCE", exponent, f"mod {phi}", reduced_exp),
            step("POWER_REDUCE", f"{base}^{exponent}",
                 f"{base}^{reduced_exp} mod {prime}"),
            step("MOD_POWER", f"{base}^{reduced_exp}", f"mod {prime}",
                 value),
        ]
        answer = f"{base}^{exponent} mod {prime} = {value}"
        problem = (
            f"Use Fermat's little theorem to reduce {base}^{exponent} "
            f"modulo {prime}."
        )
        return problem, steps, answer
