"""Chained base conversions, fully on-chain (depth strand).

Strand A of ``plans/depth_plan.md``. A value in [10^8, 10^9) is
decomposed digit by digit (``RADIX_STEP``: divide by the base, record
the remainder digit, carry the quotient) down to 0, then recomposed by
Horner (``HORNER``: times base plus digit) from that same 0 — so
decompose → recompose → next decompose chains unbroken through every
base, and the state never exceeds the starting value.

Variants (per-variant tier latitude — bounded values cap what a single
trip can reach):

- ``round_trip_check``: one base there-and-back with a ``CHECK`` that
  the recomposition equals the start; ``d50`` only.
- ``chain_two``: base a, back to decimal, then base b (a, b in 2..16);
  ``d50``/``d100``.
- ``base_tour``: a screened sequence of bases; all tiers.

Answers are the final representation, rendered with digits above 9 as
letters (e.g. ``2B7F (base 16)``).

Op-codes: ``RADIX_STEP`` / ``HORNER`` (new), ``CHECK`` (established),
``MILESTONE`` (value mod 9) at ``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

DIGITS = "0123456789ABCDEF"
VARIANT_TIERS = {
    "round_trip_check": ("d50",),
    "chain_two": ("d50", "d100"),
    "base_tour": ("d50", "d100", "d200"),
}

PROMPTS = {
    "round_trip_check": (
        "Convert {v} to base {b0} digit by digit, then rebuild the value "
        "from those digits ({k} conversions in all). Confirm the round "
        "trip and report the base-{b0} representation.",
        "Write {v} in base {b0} by repeated division, then recompose it "
        "back to decimal ({k} conversions in all). Give the base-{b0} "
        "form.",
        "Decompose {v} into base {b0} and recombine the digits to check "
        "the value returns ({k} conversions in all). What is the "
        "base-{b0} representation?",
        "Take {v} to base {b0} and back ({k} conversions in all). Report "
        "the base-{b0} representation once the check passes.",
    ),
    "chain_two": (
        "Convert {v} to base {b0}, rebuild it in decimal, then convert it "
        "to base {b1} ({k} conversions in all). Report the base-{b1} "
        "representation.",
        "Take {v} through base {b0} and back, then into base {b1} ({k} "
        "conversions in all). What is the base-{b1} form?",
        "Write {v} in base {b0}, recompose to decimal, and re-express it "
        "in base {b1} ({k} conversions in all). Give the final "
        "representation.",
        "Push {v} through the bases {b0} then {b1}, digit by digit ({k} "
        "conversions in all). Report the base-{b1} representation.",
    ),
    "base_tour": (
        "Convert {v} through the bases {tour} in order, rebuilding the "
        "value between bases ({k} conversions in all). Report the final "
        "base-{last} representation.",
        "Take {v} on a tour of the bases {tour}, decomposing and "
        "recomposing at each stop ({k} conversions in all). What is the "
        "final base-{last} form?",
        "Push {v} through each of the bases {tour} in turn ({k} "
        "conversions in all). Give the representation in the last base, "
        "{last}.",
        "Carry {v} through the base sequence {tour}, one digit at a time "
        "({k} conversions in all). Report the base-{last} result.",
    ),
}


def _rep(value, base):
    digits = []
    while value:
        digits.append(DIGITS[value % base])
        value //= base
    return "".join(reversed(digits)) or "0"


def _digit_count(value, base):
    count = 0
    while value:
        count += 1
        value //= base
    return count


def _tour_links(value, bases):
    return sum(2 * _digit_count(value, b) for b in bases)


def _emit_tour(v, bases, tier):
    chain = Chain(v, milestone_spacing=(True if tier != "d50" else None))
    chain.set_invariant("value mod 9", lambda x, k: x % 9)
    for base in bases:
        collected = []
        while chain.value:
            digit = chain.value % base
            collected.append(digit)
            chain.apply("RADIX_STEP", f"div {base} rem {DIGITS[digit]}",
                        chain.value // base)
        for digit in reversed(collected):
            chain.apply("HORNER", f"x {base} + {DIGITS[digit]}",
                        chain.value * base + digit)
    return chain


class RadixMarathonGenerator(ProblemGenerator):
    """Base-conversion marathons with unbroken chains (depth strand)."""

    VARIANTS = ("round_trip_check", "chain_two", "base_tour")
    BASE_DIFFICULTY = 3

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        if (variant is not None and tier is not None
                and tier not in VARIANT_TIERS[variant]):
            raise ValueError(f"{variant} supports {VARIANT_TIERS[variant]}")
        self.variant = variant
        self.tier = tier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        allowed = VARIANT_TIERS[variant]
        tier = self.tier if self.tier in allowed else random.choice(allowed)
        target = tier_target(tier)
        lo, hi = TIER_FLOORS[tier], target + 15

        for _ in range(5000):
            v = random.randint(10 ** 8, 10 ** 9 - 1)
            if variant == "round_trip_check":
                bases = [random.randint(2, 16)]
            elif variant == "chain_two":
                bases = random.sample(range(2, 17), 2)
            else:
                bases = [random.randint(2, 16)
                         for _ in range(random.randint(2, 9))]
            if lo <= _tour_links(v, bases) <= hi:
                break
        else:  # pragma: no cover - windows are reachable
            raise ValueError("no base tour found for the tier")

        chain = _emit_tour(v, bases, tier)
        if variant == "round_trip_check":
            chain.steps.append(step("CHECK", "round trip returns the start",
                                    v, chain.value))
        answer = f"{_rep(v, bases[-1])} (base {bases[-1]})"
        fields = {"v": v, "k": len(bases), "b0": bases[0],
                  "last": bases[-1],
                  "tour": ", ".join(str(b) for b in bases)}
        if variant == "chain_two":
            fields["b1"] = bases[1]
        problem = random.choice(PROMPTS[variant]).format(**fields)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"radix_marathon_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
