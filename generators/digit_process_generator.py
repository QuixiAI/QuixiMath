"""Iterated digit processes on many-digit seeds (depth strand).

Strand I of ``plans/depth_plan.md``: repeatedly collapse a number via a
digit rule until a fixed point (or a repeat), with every single-digit
addition shown. The seed's digit count is sized so the measured serial
chain lands in the tier window; the running total is bounded by
``9 * digits`` throughout, so intermediates never grow.

Variants:

- ``fixed_point``: repeated digit sums down to the digital root.
- ``step_count``: the same trace; the answer is the number of passes
  (the additive persistence).
- ``happy_classification``: sum of squared digits, iterated until 1 or
  a repeated value; squares are shown inline in the operand field.

Pass boundaries stay on-chain via ``DIGIT_SPLIT|<total>|digits a,b,c|
<carry>``: the previous total first, the new pass's starting value last
(the first digit, or its square for the happy rule), so the dependency
chain runs unbroken through every pass.

Op-codes: ``A`` (established), ``DIGIT_SPLIT`` (new), ``MILESTONE``
(running total mod 9 at ``d100``+), ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "fixed_point": (
        "Take the number with {L} digits: {seed}. Repeatedly replace it "
        "with the sum of its digits until one digit remains. What is that "
        "digit?",
        "A number with {L} digits is given: {seed}. Keep adding its digits, "
        "then the digits of each result, until a single digit is left. "
        "Report it.",
        "Starting from the number with {L} digits ({seed}), collapse it by "
        "digit sums until a single digit remains. Which digit results?",
        "Reduce {seed} — a number with {L} digits — by repeated digit sums "
        "to a single digit. Give that digit.",
    ),
    "step_count": (
        "Take the number with {L} digits: {seed}. Repeatedly replace it "
        "with the sum of its digits until one digit remains. How many "
        "passes does this take?",
        "A number with {L} digits is given: {seed}. Keep adding its digits "
        "until a single digit is left. How many digit-sum passes are "
        "needed?",
        "Starting from the number with {L} digits ({seed}), collapse it by "
        "digit sums to a single digit. Count the passes required.",
        "Reduce {seed} — a number with {L} digits — by repeated digit sums "
        "to a single digit. Report the number of passes.",
    ),
    "happy_classification": (
        "Take the number with {L} digits: {seed}. Repeatedly replace it "
        "with the sum of the squares of its digits. Does the process reach "
        "1, or does it repeat a value first?",
        "A number with {L} digits is given: {seed}. Iterate the "
        "sum-of-squared-digits rule. Say whether it reaches 1 or repeats "
        "an earlier value, and after how many passes.",
        "Starting from the number with {L} digits ({seed}), keep replacing "
        "it with the sum of its digits' squares. Classify the outcome.",
        "Iterate the squared-digit sum on {seed}, a number with {L} "
        "digits. Does it settle at 1 or cycle? Report the outcome.",
    ),
}


def _digit_sum_trace(digits, milestones=False):
    """(chain, passes) for repeated digit sums, all on one Chain."""
    chain = Chain(digits[0], milestone_spacing=(True if milestones else None))
    chain.set_invariant("running total mod 9", lambda v, k: v % 9)
    passes = 1
    while True:
        for d in digits[1:]:
            chain.apply("A", str(d), chain.value + d)
        total = chain.value
        if total < 10:
            break
        digits = [int(c) for c in str(total)]
        passes += 1
        chain.apply("DIGIT_SPLIT",
                    "digits " + ",".join(str(d) for d in digits), digits[0])
    return chain, passes


def _happy_trace(digits, milestones=False):
    """(chain, verdict) for the squared-digit rule with repeat detection."""
    chain = Chain(digits[0] * digits[0],
                  milestone_spacing=(True if milestones else None))
    chain.set_invariant("running total mod 9", lambda v, k: v % 9)
    seen = []
    passes = 1
    while True:
        for d in digits[1:]:
            chain.apply("A", f"{d}^2 = {d * d}", chain.value + d * d)
        total = chain.value
        if total == 1:
            return chain, f"happy; reaches 1 after {passes} passes"
        if total in seen:
            return chain, (f"unhappy; repeats {total} after {passes} passes")
        seen.append(total)
        digits = [int(c) for c in str(total)]
        passes += 1
        chain.apply("DIGIT_SPLIT",
                    "digits " + ",".join(str(d) for d in digits),
                    digits[0] * digits[0])


def _seed_digits(length, rng):
    return [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(length - 1)]


class DigitProcessGenerator(ProblemGenerator):
    """Long digit-collapse chains on many-digit seeds (depth strand)."""

    VARIANTS = ("fixed_point", "step_count", "happy_classification")
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

        # Size the seed so the measured chain lands in the tier window,
        # then redraw on the rare miss (later passes add a few steps).
        milestones = tier != "d50"
        for _ in range(200):
            length = max(2, target - random.randint(3, 8))
            digits = _seed_digits(length, random)
            if variant == "happy_classification":
                chain, verdict = _happy_trace(list(digits), milestones)
            else:
                chain, passes = _digit_sum_trace(list(digits), milestones)
            lo = max(target - 12, TIER_FLOORS[tier])
            if lo <= chain.links <= target + 12:
                break
        else:  # pragma: no cover - the window is generous
            raise ValueError("could not size a digit chain for the tier")

        seed_txt = "".join(str(d) for d in digits)
        if variant == "fixed_point":
            answer = str(chain.value)
        elif variant == "step_count":
            answer = str(passes)
        else:
            answer = verdict
        problem = random.choice(PROMPTS[variant]).format(L=len(digits),
                                                         seed=seed_txt)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"digit_process_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
