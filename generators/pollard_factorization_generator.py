import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


COMPOSITES = [91, 143, 187, 221, 299, 323, 341, 391, 437, 493, 589]

PROBLEM_TEMPLATES = [
    "Use {method} to factor n={n} with the supplied parameters {params}.",
    "Factor n={n} by {method}; use parameters {params} and show the trace.",
    "Run {method} on n={n} using {params}. Report the nontrivial factor and cofactor.",
]


def lcm(a, b):
    return a * b // gcd(a, b)


class PollardFactorizationGenerator(ProblemGenerator):
    """
    Pollard rho and Pollard p-1 factorization traces for small composites.

    Op-codes used:
    - POLLARD_RHO_SETUP / RHO_ITER / POLLARD_PM1_SETUP / LCM_STEP
    - MOD_POWER / S / GCD / CHECK / POLLARD_FACTOR
    - Z: nontrivial factor and cofactor
    """

    VARIANTS = ["rho", "p_minus_1"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "rho":
            n, c, x0, steps, factor = self._rho_case()
            method = "Pollard rho with f(x)=x^2+c"
            params = f"c={c}, x0={x0}"
        else:
            n, base, bound, steps, factor = self._pminus1_case()
            method = "Pollard p-1"
            params = f"base={base}, B={bound}"
        cofactor = n // factor
        steps.append(step("POLLARD_FACTOR", factor, cofactor))
        steps.append(step("CHECK", f"{factor}*{cofactor}", n))
        answer = f"factor = {factor}; cofactor = {cofactor}"
        problem = random.choice(PROBLEM_TEMPLATES).format(
            method=method,
            n=n,
            params=params,
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"pollard_factorization_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _rho_case(self):
        while True:
            n = random.choice(COMPOSITES)
            c = random.randint(1, 5)
            x0 = random.randint(2, 9)
            x = x0
            y = x0
            steps = [
                step("POLLARD_RHO_SETUP", f"n={n}", f"c={c}", f"x0={x0}"),
            ]
            for i in range(1, 15):
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
                diff = abs(x - y)
                d = gcd(diff, n)
                steps.append(step("RHO_ITER", i, f"x={x}, y={y}",
                                  f"abs(r)={diff}", f"gcd={d}"))
                if 1 < d < n:
                    return n, c, x0, steps, d
                if d == n:
                    break

    def _pminus1_case(self):
        while True:
            n = random.choice(COMPOSITES)
            base = random.choice([2, 3, 5])
            if gcd(base, n) != 1:
                continue
            bound = random.choice([4, 5, 6, 7])
            exponent = 1
            steps = [
                step("POLLARD_PM1_SETUP", f"n={n}", f"base={base}",
                     f"B={bound}"),
            ]
            for value in range(2, bound + 1):
                before = exponent
                exponent = lcm(exponent, value)
                steps.append(step("LCM_STEP", before, value, exponent))
            residue = pow(base, exponent, n)
            diff = residue - 1
            factor = gcd(diff, n)
            steps.extend([
                step("MOD_POWER", f"{base}^{exponent}", f"mod {n}",
                     residue),
                step("S", residue, 1, diff),
                step("GCD", f"gcd({diff},{n})", factor),
            ])
            if 1 < factor < n:
                return n, base, bound, steps, factor
