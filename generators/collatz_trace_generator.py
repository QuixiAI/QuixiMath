"""Full Collatz traces with every halving and 3n+1 shown (depth strand).

Strand I of ``plans/depth_plan.md``. Each even step is one ``D`` and
each odd step is an ``M`` then an ``A`` (both chained), so the measured
serial chain is ``evens + 2*odds``; seeds are screened per tier so that
length lands in the window, and rejected when the trajectory ever
exceeds 99,999 (keeping every multiplication hand-small).

Variants:

- ``stopping_time``: applications of the rule until the value is 1.
- ``max_value``: the trajectory's peak.
- ``steps_to_below_seed``: applications until the value first drops
  below the (odd) seed. Long below-seed prefixes are intrinsically
  rare (they are the classic record-setters), so this variant is
  ``d50``-only, drawn from a wider seed range with its own value
  allowance.
- ``parity_checksum``: how many applications hit an odd value — a count
  that is wrong if any single step is skipped or misread.

Op-codes: ``D`` / ``M`` / ``A`` (established, chained), ``MILESTONE``
(value mod 9) at ``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

VALUE_CAP = 99_999
#: steps_to_below_seed draws bigger (odd) seeds and tolerates larger
#: peaks: each step is still one small-multiplier operation.
BELOW_SEED_MAX = 999_999
BELOW_SEED_VALUE_CAP = 2_999_999

PROMPTS = {
    "stopping_time": (
        "Start at {seed}. Repeatedly halve even values and send odd values "
        "to 3n+1, until the value reaches 1 (at most {cap} steps). How "
        "many applications of the rule does this take?",
        "Apply the rule (even: divide by 2; odd: triple and add 1) to "
        "{seed} until it reaches 1 (at most {cap} steps). Count the "
        "applications.",
        "Iterate n -> n/2 for even n and n -> 3n+1 for odd n, starting at "
        "{seed}, until 1 appears (at most {cap} steps). How many steps "
        "does that take?",
        "From {seed}, keep halving evens and tripling-plus-one odds until "
        "the value is 1 (at most {cap} steps). Report the number of "
        "applications.",
    ),
    "max_value": (
        "Start at {seed}. Repeatedly halve even values and send odd values "
        "to 3n+1, until the value reaches 1 (at most {cap} steps). What "
        "is the largest value the trajectory reaches?",
        "Apply the rule (even: divide by 2; odd: triple and add 1) to "
        "{seed} until it reaches 1 (at most {cap} steps). Report the "
        "trajectory's peak value.",
        "Iterate n -> n/2 for even n and n -> 3n+1 for odd n, starting at "
        "{seed}, until 1 appears (at most {cap} steps). What is the "
        "highest value seen?",
        "From {seed}, keep halving evens and tripling-plus-one odds until "
        "the value is 1 (at most {cap} steps). Give the maximum value "
        "reached.",
    ),
    "steps_to_below_seed": (
        "Start at {seed}. Repeatedly halve even values and send odd values "
        "to 3n+1 (at most {cap} steps). After how many applications does "
        "the value first drop below {seed}?",
        "Apply the rule (even: divide by 2; odd: triple and add 1) to "
        "{seed} (at most {cap} steps). Count the applications until the "
        "value first falls below the start.",
        "Iterate n -> n/2 for even n and n -> 3n+1 for odd n from {seed} "
        "(at most {cap} steps). When does the value first dip below "
        "{seed}?",
        "From {seed}, keep halving evens and tripling-plus-one odds (at "
        "most {cap} steps). Report how many applications it takes to "
        "first go below {seed}.",
    ),
    "parity_checksum": (
        "Start at {seed}. Repeatedly halve even values and send odd values "
        "to 3n+1, until the value reaches 1 (at most {cap} steps). How "
        "many of the values along the way (the start included, 1 "
        "excluded) are odd?",
        "Apply the rule (even: divide by 2; odd: triple and add 1) to "
        "{seed} until it reaches 1 (at most {cap} steps). Count how many "
        "odd values the rule is applied to.",
        "Iterate n -> n/2 for even n and n -> 3n+1 for odd n, starting at "
        "{seed}, until 1 appears (at most {cap} steps). How many of the "
        "iterated values are odd?",
        "From {seed}, keep halving evens and tripling-plus-one odds until "
        "the value is 1 (at most {cap} steps). Report the count of odd "
        "values the rule acts on.",
    ),
}


def _profile(seed, stop_below=None):
    """(applications, chain_links, peak, odds, capped) without emitting."""
    value = seed
    applications = links = odds = 0
    peak = seed
    while value != 1:
        if stop_below is not None and value < stop_below:
            break
        if value % 2 == 0:
            value //= 2
            links += 1
        else:
            value = 3 * value + 1
            links += 2
            odds += 1
        applications += 1
        peak = max(peak, value)
        if peak > (BELOW_SEED_VALUE_CAP if stop_below is not None
                   else VALUE_CAP):
            return applications, links, peak, odds, True
    return applications, links, peak, odds, False


def _emit(seed, tier, stop_below=None):
    """The Chain for a screened seed (mirrors ``_profile`` exactly)."""
    chain = Chain(seed, milestone_spacing=(True if tier != "d50" else None))
    chain.set_invariant("value mod 9", lambda v, k: v % 9)
    while chain.value != 1:
        if stop_below is not None and chain.value < stop_below:
            break
        if chain.value % 2 == 0:
            chain.apply("D", "2", chain.value // 2)
        else:
            tripled = 3 * chain.value
            chain.apply("M", "3", tripled)
            chain.apply("A", "1", tripled + 1)
    return chain


class CollatzTraceGenerator(ProblemGenerator):
    """Long Collatz trajectories, every arithmetic step shown."""

    VARIANTS = ("stopping_time", "max_value", "steps_to_below_seed",
                "parity_checksum")
    BASE_DIFFICULTY = 2

    def __init__(self, variant=None, tier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if tier is not None and tier not in ("d50", "d100", "d200"):
            raise ValueError("tier must be d50, d100, d200, or None")
        if variant == "steps_to_below_seed" and tier not in (None, "d50"):
            raise ValueError("steps_to_below_seed supports d50 only")
        self.variant = variant
        self.tier = tier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "steps_to_below_seed":
            tier = "d50"
        else:
            tier = self.tier or pick_tier()
        target = tier_target(tier)
        lo, hi = max(target - 15, TIER_FLOORS[tier]), target + 15

        for _ in range(20_000):
            if variant == "steps_to_below_seed":
                seed = random.randrange(3, BELOW_SEED_MAX, 2)  # odd seeds
                stop_below = seed
            else:
                seed = random.randint(7, 100_000)
                stop_below = None
            applications, links, peak, odds, capped = _profile(
                seed, stop_below)
            if not capped and lo <= links <= hi:
                break
        else:  # pragma: no cover - windows are well populated
            raise ValueError("no Collatz seed found for the tier")

        chain = _emit(seed, tier, stop_below)
        cap = ((applications + 24) // 25) * 25
        if variant == "stopping_time":
            answer = str(applications)
        elif variant == "max_value":
            answer = str(peak)
        elif variant == "steps_to_below_seed":
            answer = str(applications)
        else:
            answer = str(odds)
        problem = random.choice(PROMPTS[variant]).format(seed=seed, cap=cap)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"collatz_trace_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
