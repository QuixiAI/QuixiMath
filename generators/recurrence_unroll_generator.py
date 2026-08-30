"""Linear recurrences unrolled term by term mod m (depth strand).

Strand R of ``plans/depth_plan.md``. State is the pair of latest terms,
bounded below m <= 500 forever; each ``REC_STEP`` advances one term
(previous pair first, new pair last), so the chain length is the number
of terms unrolled.

Variants:

- ``term_n_mod_m``: x_{k+1} = (p*x_k + q*x_{k-1}) mod m for stated N
  terms; answer x_N.
- ``two_term_mod``: the Fibonacci rule (p = q = 1) from arbitrary
  seeds; answer x_N.
- ``pisano_period``: the Fibonacci pair walk from (0, 1) until the
  starting pair returns; m screened so the Pisano period lands in the
  tier window; answer the period.
- ``matrix_check``: as ``term_n_mod_m``, closed by a short
  square-and-multiply of [[p, q], [1, 0]]^N mod m and a ``CHECK`` that
  the matrix route agrees with the unrolled value.

Op-codes: ``REC_STEP`` / ``MAT_POW`` (new), ``CHECK`` (established),
``MILESTONE`` ((a + b) mod 9) at ``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "term_n_mod_m": (
        "Define x0 = {x0}, x1 = {x1}, and x(k+1) = ({p}*x(k) + {q}*x(k-1)) "
        "mod {m}. Unroll the recurrence for {n} terms. What is the final "
        "term?",
        "With x0 = {x0}, x1 = {x1}, iterate x(k+1) = ({p}*x(k) + "
        "{q}*x(k-1)) mod {m} term by term for {n} terms. Report the last "
        "value.",
        "Starting from x0 = {x0} and x1 = {x1}, apply x(k+1) = ({p}*x(k) "
        "+ {q}*x(k-1)) mod {m} for {n} terms. Give the final term.",
        "Unroll x(k+1) = ({p}*x(k) + {q}*x(k-1)) mod {m} from x0 = {x0}, "
        "x1 = {x1}, computing {n} terms in order. State the last one.",
    ),
    "two_term_mod": (
        "Define x0 = {x0}, x1 = {x1}, and x(k+1) = (x(k) + x(k-1)) mod "
        "{m}. Unroll the recurrence for {n} terms. What is the final "
        "term?",
        "With x0 = {x0}, x1 = {x1}, iterate the Fibonacci rule mod {m} "
        "term by term for {n} terms. Report the last value.",
        "Starting from x0 = {x0} and x1 = {x1}, add consecutive terms "
        "mod {m} for {n} terms. Give the final term.",
        "Unroll x(k+1) = (x(k) + x(k-1)) mod {m} from x0 = {x0}, x1 = "
        "{x1}, computing {n} terms in order. State the last one.",
    ),
    "pisano_period": (
        "Walk the Fibonacci pair (x(k-1), x(k)) mod {m} from (0, 1) "
        "until the starting pair returns (at most {cap} steps). What is "
        "the period?",
        "Iterate the Fibonacci rule mod {m} from the pair (0, 1) until "
        "that pair appears again (at most {cap} steps). Report the "
        "period length.",
        "Trace Fibonacci mod {m} pair by pair until (0, 1) recurs (at "
        "most {cap} steps). Give the period.",
        "The Fibonacci sequence mod {m} is periodic: walk it from "
        "(0, 1) to the first return (at most {cap} steps) and state the "
        "period.",
    ),
    "matrix_check": (
        "Define x0 = {x0}, x1 = {x1}, and x(k+1) = ({p}*x(k) + {q}*x(k-1)) "
        "mod {m}. Unroll the recurrence for {n} terms, then confirm the "
        "final term with the matrix power [[{p}, {q}], [1, 0]]^{n} mod "
        "{m}. What is the final term?",
        "With x0 = {x0}, x1 = {x1}, iterate x(k+1) = ({p}*x(k) + "
        "{q}*x(k-1)) mod {m} for {n} terms and verify the result by the "
        "matrix route. Report the final term.",
        "Starting from x0 = {x0} and x1 = {x1}, unroll x(k+1) = "
        "({p}*x(k) + {q}*x(k-1)) mod {m} for {n} terms; cross-check with "
        "[[{p}, {q}], [1, 0]]^{n}. Give the final term.",
        "Compute {n} terms of x(k+1) = ({p}*x(k) + {q}*x(k-1)) mod {m} "
        "from x0 = {x0}, x1 = {x1}, then check the last one against the "
        "companion-matrix power. State it.",
    ),
}


def _mat_mul(A, B, m):
    return (
        ((A[0][0] * B[0][0] + A[0][1] * B[1][0]) % m,
         (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % m),
        ((A[1][0] * B[0][0] + A[1][1] * B[1][0]) % m,
         (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % m),
    )


def _mat_pow_steps(p, q, n, m):
    """Square-and-multiply on the companion matrix, with MAT_POW rows."""
    steps = []
    result = ((1, 0), (0, 1))
    base = ((p, q), (1, 0))
    exponent = n
    while exponent:
        if exponent & 1:
            result = _mat_mul(result, base, m)
            steps.append(step("MAT_POW", "multiply",
                              f"[[{result[0][0]}, {result[0][1]}], "
                              f"[{result[1][0]}, {result[1][1]}]]"))
        exponent >>= 1
        if exponent:
            base = _mat_mul(base, base, m)
            steps.append(step("MAT_POW", "square",
                              f"[[{base[0][0]}, {base[0][1]}], "
                              f"[{base[1][0]}, {base[1][1]}]]"))
    return steps, result


def pisano(m, cap=2000):
    a, b, n = 0, 1, 0
    while True:
        a, b = b, (a + b) % m
        n += 1
        if (a, b) == (0, 1):
            return n
        if n > cap:
            return -1


class RecurrenceUnrollGenerator(ProblemGenerator):
    """Tier-length recurrence unrolls mod m (depth strand)."""

    VARIANTS = ("term_n_mod_m", "two_term_mod", "pisano_period",
                "matrix_check")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        self.variant = variant
        self.tier = tier

    #: pisano_period's text space is only (qualifying m) x templates, so
    #: it draws at reduced weight to keep the class over the capacity bar.
    VARIANT_WEIGHTS = (30, 30, 10, 30)

    def generate(self) -> dict:
        variant = self.variant or random.choices(
            self.VARIANTS, weights=self.VARIANT_WEIGHTS, k=1)[0]
        tier = self.tier or pick_tier()
        target = tier_target(tier)

        if variant == "pisano_period":
            lo, hi = TIER_FLOORS[tier], target + 15
            for _ in range(5000):
                m = random.randint(3, 4000)
                period = pisano(m, cap=hi + 1)
                if lo <= period <= hi:
                    break
            else:  # pragma: no cover - every window has ~120 moduli
                raise ValueError("no Pisano period found for the tier")
            p = q = 1
            x0, x1, n = 0, 1, period
        else:
            m = random.randint(10, 499)
            x0, x1 = random.randrange(m), random.randrange(m)
            if variant == "two_term_mod":
                p = q = 1
            else:
                p, q = random.randint(1, 9), random.randint(1, 9)
            n = target

        chain = Chain((x0, x1), render=lambda ab: f"({ab[0]}, {ab[1]})",
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant("(a + b) mod 9",
                            lambda ab, k: (ab[0] + ab[1]) % 9)
        for k in range(1, n + 1):
            a, b = chain.value
            chain.apply("REC_STEP", f"n={k}", (b, (p * b + q * a) % m))

        steps = list(chain.steps)
        if variant == "pisano_period":
            answer = str(n)
            cap = ((n + 24) // 25) * 25
            problem = random.choice(PROMPTS[variant]).format(m=m, cap=cap)
        else:
            final = chain.value[1]  # n applies from (x0, x1) -> x_{n+1}
            if variant == "matrix_check":
                # [x_{n+2}, x_{n+1}] = C^{n+1} [x1, x0], so the bottom row
                # of C^{n+1} recovers exactly the last unrolled term.
                mat_steps, matrix = _mat_pow_steps(p, q, n + 1, m)
                steps.extend(mat_steps)
                mat_value = (matrix[1][0] * x1 + matrix[1][1] * x0) % m
                steps.append(step("CHECK", "matrix route agrees",
                                  f"bottom row of C^{n + 1} on (x1, x0) = "
                                  f"{mat_value}",
                                  f"unrolled final term = {final}"))
            answer = str(final)
            problem = random.choice(PROMPTS[variant]).format(
                x0=x0, x1=x1, p=p, q=q, m=m, n=n)

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"recurrence_unroll_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
