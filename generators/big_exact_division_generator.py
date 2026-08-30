"""Long division marathons, one DIV_STEP per digit (depth strand).

Strand A of ``plans/depth_plan.md``. The dividend has tier-many digits
but is never manipulated whole: the chain state is the running
sub-divisor remainder (always below the two-digit divisor), and each
``DIV_STEP`` brings down one digit, divides, and carries the new
remainder. Every individual step is hand-small; the marathon is the
point.

Variants:

- ``remainder_only``: divide a tier-digit dividend by a two-digit
  divisor; answer just the remainder (the whole chain is still needed).
- ``quotient_digit_sum``: the sum of every quotient digit — a checksum
  that is wrong if any single step drifts.
- ``repetend_length``: the decimal period of p/q for a prime q screened
  so ord_q(10) lands in the tier window; the chain runs one full period
  of the expansion until the starting remainder returns.

Op-codes: ``DIV_STEP`` (new: ``DIV_STEP|<r_prev>|d=<digit>, q=<qdigit>|
<r_next>`` — previous remainder first, new remainder last),
``MILESTONE`` (remainder mod 9) at ``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "remainder_only": (
        "Divide the number with {L} digits ({dividend}) by {divisor} using "
        "long division, one digit at a time. What is the remainder?",
        "Work the long division of {dividend} — a number with {L} digits — "
        "by {divisor}, digit by digit. Report the remainder.",
        "Using long division, take {dividend} (a number with {L} digits) "
        "over {divisor}. What remainder is left?",
        "Carry {dividend}, which has {L} digits, through long division by "
        "{divisor}. Give the final remainder.",
    ),
    "quotient_digit_sum": (
        "Divide the number with {L} digits ({dividend}) by {divisor} using "
        "long division, one digit at a time. What is the sum of the "
        "quotient's digits?",
        "Work the long division of {dividend} — a number with {L} digits — "
        "by {divisor}, digit by digit. Report the sum of the digits of the "
        "quotient.",
        "Using long division, take {dividend} (a number with {L} digits) "
        "over {divisor}. Add up all the digits of the quotient.",
        "Carry {dividend}, which has {L} digits, through long division by "
        "{divisor}. Give the quotient's digit sum.",
    ),
    "repetend_length": (
        "Expand {p}/{q} as a decimal, one digit at a time, until the "
        "remainder repeats (at most {cap} steps). How long is the "
        "repeating block?",
        "Carry out the decimal expansion of {p}/{q} digit by digit until "
        "a remainder returns (at most {cap} steps). Report the period "
        "length.",
        "Divide {p} by {q} in decimal, step by step, until the expansion "
        "starts repeating (at most {cap} steps). What is the length of "
        "the repetend?",
        "The decimal expansion of {p}/{q} eventually repeats; trace it "
        "(at most {cap} steps) and give the period length.",
    ),
}


def _order_bank():
    """(q, ord_q(10)) for primes q < 1000 coprime to 10."""
    bank = []
    for q in range(7, 1000):
        if q % 2 == 0 or q % 5 == 0:
            continue
        if any(q % d == 0 for d in range(3, int(q ** 0.5) + 1, 2)):
            continue
        order, power = 1, 10 % q
        while power != 1:
            power = (power * 10) % q
            order += 1
        bank.append((q, order))
    return bank


ORDER_BANK = _order_bank()


def _division_chain(digits, divisor, tier):
    """The digit-by-digit chain; returns (chain, quotient_digits)."""
    chain = Chain(0, milestone_spacing=(True if tier != "d50" else None))
    chain.set_invariant("remainder mod 9", lambda v, k: v % 9)
    quotient_digits = []
    for d in digits:
        widened = chain.value * 10 + d
        q_digit = widened // divisor
        quotient_digits.append(q_digit)
        chain.apply("DIV_STEP", f"d={d}, q={q_digit}", widened % divisor)
    return chain, quotient_digits


class BigExactDivisionGenerator(ProblemGenerator):
    """Tier-length long-division chains (depth strand)."""

    VARIANTS = ("remainder_only", "quotient_digit_sum", "repetend_length")
    BASE_DIFFICULTY = 2

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        self.variant = variant
        self.tier = tier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        tier = self.tier or pick_tier()
        target = tier_target(tier)

        if variant == "repetend_length":
            lo, hi = TIER_FLOORS[tier], target + 15
            q, period = random.choice(
                [(q, o) for q, o in ORDER_BANK if lo <= o <= hi])
            p = random.randint(1, q - 1)
            chain = Chain(p, milestone_spacing=(True if tier != "d50"
                                                else None))
            chain.set_invariant("remainder mod 9", lambda v, k: v % 9)
            for _ in range(period):
                widened = chain.value * 10
                chain.apply("DIV_STEP", f"d=0, q={widened // q}", widened % q)
            answer = str(period)
            cap = ((period + 24) // 25) * 25
            problem = random.choice(PROMPTS[variant]).format(p=p, q=q,
                                                             cap=cap)
        else:
            length = target
            divisor = random.randint(11, 97)
            digits = ([random.randint(1, 9)]
                      + [random.randint(0, 9) for _ in range(length - 1)])
            chain, quotient_digits = _division_chain(digits, divisor, tier)
            if variant == "remainder_only":
                answer = str(chain.value)
            else:
                answer = str(sum(quotient_digits))
            dividend = "".join(str(d) for d in digits)
            problem = random.choice(PROMPTS[variant]).format(
                L=length, dividend=dividend, divisor=divisor)

        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"big_exact_division_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
