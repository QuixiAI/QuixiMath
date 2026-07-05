import random

from base_generator import ProblemGenerator
from helpers import step, jid


PRIMES = [17, 41, 73]


def roots_mod(a, p):
    return sorted(x for x in range(p) if (x * x) % p == a % p)


def nonresidue(p):
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            return z
    raise ValueError(p)


class TonelliShanksGenerator(ProblemGenerator):
    """
    Tonelli-Shanks modular square roots for odd primes.

    Op-codes used:
    - TS_SETUP / TS_FACTOR / TS_NONRESIDUE / TS_INIT / TS_LOOP
    - MOD_POWER / M / MOD_REDUCE / CHECK
    - Z: both square roots modulo p
    """

    def generate(self) -> dict:
        p = random.choice(PRIMES)
        root = random.randint(2, p - 2)
        a = (root * root) % p
        steps = [step("TS_SETUP", f"a={a}", f"p={p}")]
        q = p - 1
        s = 0
        while q % 2 == 0:
            q //= 2
            s += 1
        z = nonresidue(p)
        steps.append(step("TS_FACTOR", f"p-1={p - 1}", f"q={q}", f"s={s}"))
        steps.append(step("TS_NONRESIDUE", z))
        m = s
        c = pow(z, q, p)
        t = pow(a, q, p)
        r = pow(a, (q + 1) // 2, p)
        steps.extend([
            step("MOD_POWER", f"{z}^{q}", f"mod {p}", c),
            step("MOD_POWER", f"{a}^{q}", f"mod {p}", t),
            step("MOD_POWER", f"{a}^{(q + 1) // 2}", f"mod {p}", r),
            step("TS_INIT", f"m={m}", f"c={c}", f"t={t}", f"r={r}"),
        ])
        while t != 1:
            i = 1
            value = (t * t) % p
            while value != 1:
                value = (value * value) % p
                i += 1
            b = pow(c, 2 ** (m - i - 1), p)
            steps.append(step("TS_LOOP", f"i={i}", f"b={b}"))
            r = (r * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i
            steps.append(step("TS_INIT", f"m={m}", f"c={c}", f"t={t}",
                              f"r={r}"))
        roots = sorted([r, (-r) % p])
        steps.append(step("CHECK", f"{roots[0]}^2 mod {p}", a))
        steps.append(step("CHECK", f"{roots[1]}^2 mod {p}", a))
        answer = f"roots = {roots[0]}, {roots[1]} mod {p}"
        problem = (
            f"Use Tonelli-Shanks to solve x^2 congruent to {a} modulo prime {p}."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="tonelli_shanks",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
