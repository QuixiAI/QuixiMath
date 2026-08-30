"""Extended Euclidean algorithm, with depth-strand tiered variants.

The legacy ``extended_euclid`` operation (small coprime pairs, full
coefficient table, every product and subtraction shown) is unchanged.
The depth retrofit (``plans/depth_plan.md`` Strand E) adds two tiered
variants at **d50 only** — a mathematical bound, not a scoping choice:
a Euclid chain of length n needs inputs of size ~phi^n, so the strand's
bounded-intermediates rule caps chained gcd work near n = 70 (16-digit
values, quotients mostly 1).

- ``bezout``: a quotient sequence of mostly-1s is built backward
  through continuants into a pair (a, b); the trace is a chained
  remainder-pair walk ``EUCLID_PAIR|(a, b)|q=<q>|(b, a-qb)`` of exactly
  that length. Bezout coefficients are computed and spot-verified mod
  97 in a single ``CHECK`` (no tier-length product ever appears).
- ``crt_chain``: fifteen pairwise-coprime moduli folded sequentially
  into a running solution, three chained links per fold
  (``CRT_RES`` / ``CRT_T`` / ``A``), answer ``x = <x> (mod <M>)``.

The default wrapper preserves the legacy call's exact global-RNG
advancement (this class sits mid-registry): the legacy record is drawn
first, and a digest of it decides — without consuming RNG — whether a
tiered record is generated on a locally re-seeded stream instead.
"""
import hashlib
import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import Chain, tier_difficulty, tier_target

DEPTH = True

#: Pairwise-coprime fold moduli for ``crt_chain`` (15 needed: three
#: chained links per fold and fourteen folds give the 42-link chain).
CRT_MODULI = (4, 9, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)

BEZOUT_PROMPTS = (
    "Run the Euclidean algorithm on ({a}, {b}) — a pair built to need "
    "{n} steps of division — and give the gcd with Bezout coefficients.",
    "The pair ({a}, {b}) takes {n} steps of the Euclidean algorithm. "
    "Walk them all and report gcd, x, and y with ax + by = gcd.",
    "Carry ({a}, {b}) through all {n} steps of the Euclidean algorithm "
    "and state the gcd and one pair of Bezout coefficients.",
    "Apply the Euclidean algorithm to ({a}, {b}) for the full {n} steps "
    "it requires; give gcd, x, and y.",
)

CRT_PROMPTS = (
    "Solve the system of {k} congruences, folding them in one at a "
    "time: {congruences}. Give x mod the product of the moduli.",
    "Fold the {k} congruences {congruences} into a single solution, one "
    "modulus at a time. Report x modulo the full product.",
    "Combine the {k} congruences ({congruences}) sequentially into one "
    "running solution. What is x mod the product?",
    "Work through the {k} congruences {congruences} in order, updating "
    "the solution at each fold. State x modulo the product.",
)


def coprime_pair():
    while True:
        m = random.randint(12, 90)
        n = random.randint(10, 85)
        if m != n and gcd(m, n) == 1:
            return m, n


def _pair_from_quotients(quotients, g):
    """Reconstruct (a, b) whose Euclid quotient sequence is exactly this."""
    r_next, r = 0, g
    for q in reversed(quotients):
        r_next, r = r, q * r + r_next
    return r, r_next


def _bezout(a, b):
    old_r, r, old_x, x, old_y, y = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y


class ExtendedEuclidGenerator(ProblemGenerator):
    """Extended Euclid: legacy face plus d50 depth variants."""

    VARIANTS = ("legacy", "bezout", "crt_chain")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and (variant in (None, "legacy")
                                 or tier != "d50"):
            raise ValueError("tiered variants support d50 only")
        self.variant = variant
        self.tier = tier

    # ------------------------------------------------------------------
    # Legacy face — byte-identical to the original generator.
    # ------------------------------------------------------------------
    def _generate_legacy(self) -> dict:
        scale = random.choice([1, 1, 2, 3, 4, 5, 6, 7])
        m, n = coprime_pair()
        a, b = sorted((scale * m, scale * n), reverse=True)

        old_r, r = a, b
        old_x, x = 1, 0
        old_y, y = 0, 1
        steps = [
            step("EXT_GCD_SETUP", a, b),
            step("BACK_SUB_ROW", f"r={old_r}", f"x={old_x}", f"y={old_y}"),
            step("BACK_SUB_ROW", f"r={r}", f"x={x}", f"y={y}"),
        ]

        while r != 0:
            q = old_r // r
            product = q * r
            new_r = old_r - product
            steps.append(step("EUCLID_DIV", old_r, r, q, new_r))
            steps.append(step("M", q, r, product))
            steps.append(step("S", old_r, product, new_r))

            qx = q * x
            new_x = old_x - qx
            steps.append(step("M", q, x, qx))
            steps.append(step("S", old_x, qx, new_x))

            qy = q * y
            new_y = old_y - qy
            steps.append(step("M", q, y, qy))
            steps.append(step("S", old_y, qy, new_y))
            steps.append(step("BACK_SUB_ROW", f"r={new_r}",
                              f"x={new_x}", f"y={new_y}"))

            old_r, r = r, new_r
            old_x, x = x, new_x
            old_y, y = y, new_y

        ax = a * old_x
        by = b * old_y
        steps.extend([
            step("M", a, old_x, ax),
            step("M", b, old_y, by),
            step("A", ax, by, old_r),
            step("BEZOUT_CHECK", f"{a}*{old_x} + {b}*{old_y}", old_r),
            step("CHECK", "gcd is last nonzero remainder", old_r),
        ])
        answer = f"gcd = {old_r}; x = {old_x}; y = {old_y}"
        problem = (
            f"Use the extended Euclidean algorithm to find gcd({a}, {b}) "
            f"and coefficients x,y with {a}x + {b}y = gcd."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="extended_euclid",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    # ------------------------------------------------------------------
    # Depth variants (d50 only)
    # ------------------------------------------------------------------
    def _generate_bezout(self) -> dict:
        for _ in range(200):
            n = tier_target("d50")
            quotients = [random.choice((1, 1, 1, 1, 1, 1, 1, 2))
                         for _ in range(n)]
            quotients[-1] = max(quotients[-1], 2)  # last quotient >= 2
            g = random.randint(1, 3)
            a, b = _pair_from_quotients(quotients, g)
            if a <= 2 * 10 ** 16:
                break
        chain = Chain((a, b), render=lambda p: f"({p[0]}, {p[1]})")
        # EUCLID_PAIR, not EUCLID_DIV: the legacy code's fields are four
        # scalars (old, r, q, new) and may not be reused with pair fields.
        for q in quotients:
            r0, r1 = chain.value
            chain.apply("EUCLID_PAIR", f"q={q}", (r1, r0 - q * r1))
        g_out, x, y = _bezout(a, b)
        check_value = (a % 97 * (x % 97) + b % 97 * (y % 97)) % 97
        chain.steps.append(step(
            "CHECK", "bezout identity mod 97",
            f"({a % 97}*{x % 97} + {b % 97}*{y % 97}) mod 97 = "
            f"{check_value}",
            f"gcd mod 97 = {g_out % 97}"))
        answer = f"gcd = {g_out}; x = {x}; y = {y}"
        problem = random.choice(BEZOUT_PROMPTS).format(a=a, b=b, n=n)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation="extended_euclid_bezout_d50",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, "d50"),
        )

    def _generate_crt(self) -> dict:
        moduli = list(CRT_MODULI)
        random.shuffle(moduli)
        residues = [random.randrange(m) for m in moduli]
        congruences = "; ".join(
            f"x = {r} (mod {m})" for m, r in zip(moduli, residues))
        chain = Chain(residues[0])
        running_modulus = moduli[0]
        for m, target in zip(moduli[1:], residues[1:]):
            r = chain.value % m
            m_inv = pow(running_modulus, -1, m)
            t = ((target - r) * m_inv) % m
            chain.apply("CRT_RES", f"x mod {m} = {r}", chain.value)
            chain.apply("CRT_T",
                        f"t = ({target} - {r})*{m_inv} mod {m} = {t}",
                        chain.value)
            chain.apply("A", f"t*M = {t * running_modulus}",
                        chain.value + t * running_modulus)
            running_modulus *= m
        answer = f"x = {chain.value} (mod {running_modulus})"
        problem = random.choice(CRT_PROMPTS).format(
            k=len(moduli), congruences=congruences)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation="extended_euclid_crt_chain_d50",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, "d50"),
        )

    def generate(self) -> dict:
        if self.variant == "legacy":
            return self._generate_legacy()
        if self.variant == "bezout":
            return self._generate_bezout()
        if self.variant == "crt_chain":
            return self._generate_crt()

        # Default: preserve the legacy call's exact RNG advancement, then
        # swap in a tiered record for roughly half of draws via a digest
        # of the legacy output (no extra RNG consumed on the shared
        # stream; the tiered path runs on a locally re-seeded stream).
        legacy = self._generate_legacy()
        post_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_state).encode("ascii")).digest()
        if digest[0] < 128:
            return legacy
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            if digest[0] % 2:
                return self._generate_bezout()
            return self._generate_crt()
        finally:
            random.setstate(post_state)
