import hashlib
import random
from math import gcd, isqrt

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

SQRT_PROMPTS = (
    "Expand sqrt({d}) as a periodic continued fraction using the (P, Q) "
    "recurrence, until the state repeats (at most {cap} steps). Report "
    "the period and a0.",
    "Run the (P, Q) recurrence for sqrt({d}) term by term until a state "
    "recurs (at most {cap} steps). What are the period and a0?",
    "Trace the continued fraction of sqrt({d}) with the standard (P, Q) "
    "updates until the pair repeats (at most {cap} steps). Give the "
    "period length and a0.",
    "The continued fraction of sqrt({d}) is periodic: walk the (P, Q) "
    "recurrence to the first repeat (at most {cap} steps) and state the "
    "period with a0.",
)


def sqrt_period_terms(d):
    """[(a, P', Q'), ...] for one full period of sqrt(d), or None."""
    a0 = isqrt(d)
    if a0 * a0 == d:
        return None
    terms = []
    P, Q = 0, 1
    first = None
    while True:
        a = (a0 + P) // Q
        P = a * Q - P
        Q = (d - P * P) // Q
        terms.append((a, P, Q))
        if first is None:
            first = (P, Q)
        elif (P, Q) == first:
            return terms[:-1]
        if len(terms) > 400:
            return None


def cf_text(partials):
    if len(partials) == 1:
        return f"[{partials[0]}]"
    return f"[{partials[0]}; {', '.join(str(v) for v in partials[1:])}]"


def frac_text(num, den):
    return f"{num}/{den}"


def convergent_text(convergents):
    return ", ".join(frac_text(num, den) for num, den in convergents)


def continued_fraction(num, den):
    partials = []
    x, y = num, den
    divisions = []
    while y:
        q = x // y
        r = x - q * y
        divisions.append((x, y, q, r))
        partials.append(q)
        x, y = y, r
    return partials, divisions


class ContinuedFractionGenerator(ProblemGenerator):
    """
    Simple continued fractions and convergents for positive rationals,
    plus the depth strand's ``sqrt_periodic`` retrofit — the (P, Q)
    recurrence for sqrt(d), whose state is bounded by 2*sqrt(d) forever,
    so it reaches every depth tier (plans/depth_plan.md Strand E; the
    rational expansion cannot go deep bounded — Euclid's phi^n wall).

    Op-codes used:
    - CF_SETUP / CF_PARTIAL / CF_RESULT: Euclidean quotient expansion
    - CONV_INIT / CONV_STEP / CONVERGENT: convergent recurrence
    - EUCLID_DIV / M / S / A (established/shared): arithmetic
    - SQRT_CF (new): one (P, Q) update, previous pair first, new last
    - MILESTONE: (P + Q) mod 9, at d100+
    - Z: continued fraction and all convergents / the period and a0
    """

    VARIANTS = ("legacy", "sqrt_periodic")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and (variant != "sqrt_periodic"
                                 or tier not in ("d50", "d100", "d200")):
            raise ValueError("tier applies to sqrt_periodic only")
        self.variant = variant
        self.tier = tier

    def _generate_sqrt_periodic(self) -> dict:
        tier = self.tier or pick_tier()
        target = tier_target(tier)
        lo, hi = TIER_FLOORS[tier], target + 15
        for _ in range(20_000):
            d = random.randint(50, 60_000)
            terms = sqrt_period_terms(d)
            if terms is not None and lo <= len(terms) <= hi:
                break
        else:  # pragma: no cover - thousands of d fit each window
            raise ValueError("no sqrt period found for the tier")
        a0 = isqrt(d)
        period = len(terms)
        chain = Chain((0, 1), render=lambda pq: f"(P={pq[0]}, Q={pq[1]})",
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant("(P + Q) mod 9",
                            lambda pq, k: (pq[0] + pq[1]) % 9)
        steps_prefix = [
            step("CF_SETUP", f"sqrt({d})", f"a0 = {a0}"),
            step("CHECK", "a0 is the integer part",
                 f"{a0}^2 = {a0 * a0} <= {d}",
                 f"{a0 + 1}^2 = {(a0 + 1) ** 2} > {d}"),
        ]
        for a, P, Q in terms:
            chain.apply("SQRT_CF", f"a = {a}", (P, Q))
        answer = f"period {period}; a0 = {a0}"
        cap = ((period + 24) // 25) * 25
        problem = random.choice(SQRT_PROMPTS).format(d=d, cap=cap)
        steps = steps_prefix + chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"continued_fraction_sqrt_periodic_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )

    def generate(self) -> dict:
        if self.variant == "sqrt_periodic":
            return self._generate_sqrt_periodic()
        if self.variant == "legacy":
            return self._generate_legacy()
        # Default: preserve legacy RNG advancement; swap in the tiered
        # face for roughly half of draws via a digest of the legacy
        # record (the house retrofit pattern).
        legacy = self._generate_legacy()
        post_state = random.getstate()
        digest = hashlib.sha256(
            legacy["problem"].encode("utf-8")
            + repr(post_state).encode("ascii")).digest()
        if digest[0] < 128:
            return legacy
        random.seed(int.from_bytes(digest[1:9], "big"))
        try:
            return self._generate_sqrt_periodic()
        finally:
            random.setstate(post_state)

    def _generate_legacy(self) -> dict:
        while True:
            den = random.randint(12, 160)
            num = random.randint(den + 1, 6 * den)
            if gcd(num, den) == 1:
                break

        partials, divisions = continued_fraction(num, den)
        steps = [
            step("CF_SETUP", frac_text(num, den)),
        ]
        for idx, (x, y, q, r) in enumerate(divisions):
            product = q * y
            steps.append(step("EUCLID_DIV", x, y, q, r))
            steps.append(step("M", q, y, product))
            steps.append(step("S", x, product, r))
            steps.append(step("CF_PARTIAL", f"a_{idx}", q))
        steps.append(step("CF_RESULT", cf_text(partials)))

        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0
        steps.append(step("CONV_INIT", "h_-2=0,h_-1=1",
                          "k_-2=1,k_-1=0"))
        convergents = []
        for idx, partial in enumerate(partials):
            h_prod = partial * h_prev1
            h = h_prod + h_prev2
            k_prod = partial * k_prev1
            k = k_prod + k_prev2
            steps.append(step("M", partial, h_prev1, h_prod))
            steps.append(step("A", h_prod, h_prev2, h))
            steps.append(step("M", partial, k_prev1, k_prod))
            steps.append(step("A", k_prod, k_prev2, k))
            steps.append(step("CONV_STEP", f"i={idx}", f"h={h}", f"k={k}"))
            steps.append(step("CONVERGENT", f"i={idx}", frac_text(h, k)))
            convergents.append((h, k))
            h_prev2, h_prev1 = h_prev1, h
            k_prev2, k_prev1 = k_prev1, k

        answer = (
            f"continued fraction = {cf_text(partials)}; "
            f"convergents = {convergent_text(convergents)}"
        )
        problem = (
            f"Find the simple continued fraction for {frac_text(num, den)} "
            f"and list all convergents."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="continued_fraction",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
