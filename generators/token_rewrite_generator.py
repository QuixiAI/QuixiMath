"""String rewriting to a normal form, one rule application per step
(depth strand).

Strand S of ``plans/depth_plan.md``. Systems come from a bank of
terminating, confluent sorting rules over a small alphabet:

- ``sort2``: the single rule ``ba -> ab`` — every application removes
  exactly one (b, a) inversion, so the step count IS the inversion
  count and the normal form is the sorted string.
- ``sort3``: the full sorting system ``ba -> ab``, ``ca -> ac``,
  ``cb -> bc`` — every application removes exactly one out-of-order
  pair, so the step count is the total inversion count and per-rule
  usage is the per-letter-pair inversion count.

Start strings are built as blocks (``c^i b^j a^k``, whose inversion
count is exactly ij + ik + jk) then scrambled by a few random adjacent
transpositions for capacity, and screened by simulation into the tier
window — uniform random strings of bounded length cannot reach d200.

Application order is leftmost match, first rule first — stated in the
problem. Each application is one chained ``RW_STEP`` (previous string
first, ``rule@position`` in the middle, new string last); the string
length never changes, so state is bounded by construction, and letter
counts are conserved — the MILESTONE invariant is the count of ``a``.

Variants: ``normal_form``, ``step_count``, ``rule_usage_count``
(``sort3`` only; answer ``ba: 120; cb: 45``).

Op-codes: ``RW_STEP`` (new — the established ``REWRITE`` code carries
algebraic-expression fields and is not reused), ``MILESTONE``, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

SYSTEMS = {
    "sort2": ("ba -> ab",),
    "sort3": ("ba -> ab", "ca -> ac", "cb -> bc"),
}

PROMPTS = {
    "normal_form": (
        "Rewrite the string {start} with the rule(s) {rules}, always "
        "applying the leftmost match of the first applicable rule, until "
        "no rule applies (at most {cap} steps). What is the final "
        "string?",
        "Apply {rules} to {start} — leftmost match, first rule first — "
        "until nothing matches (at most {cap} steps). Report the normal "
        "form.",
        "Reduce {start} step by step under {rules} (leftmost match, "
        "first listed rule first) to its normal form (at most {cap} "
        "steps). Give the final string.",
        "Drive {start} to a fixed point under {rules}, one leftmost "
        "application at a time (at most {cap} steps). State the "
        "resulting string.",
    ),
    "step_count": (
        "Rewrite the string {start} with the rule(s) {rules}, always "
        "applying the leftmost match of the first applicable rule, until "
        "no rule applies (at most {cap} steps). How many applications "
        "does this take?",
        "Apply {rules} to {start} — leftmost match, first rule first — "
        "until nothing matches (at most {cap} steps). Count the "
        "applications.",
        "Reduce {start} under {rules} (leftmost match, first listed rule "
        "first) to its normal form (at most {cap} steps). How many "
        "steps are needed?",
        "Drive {start} to a fixed point under {rules}, one leftmost "
        "application at a time (at most {cap} steps). Report the number "
        "of applications.",
    ),
    "rule_usage_count": (
        "Rewrite the string {start} with the rules {rules}, always "
        "applying the leftmost match of the first applicable rule, until "
        "no rule applies (at most {cap} steps). How many times is each "
        "rule used?",
        "Apply {rules} to {start} — leftmost match, first rule first — "
        "until nothing matches (at most {cap} steps). Report each "
        "rule's usage count.",
        "Reduce {start} under {rules} (leftmost match, first listed rule "
        "first) to its normal form (at most {cap} steps). Count the "
        "uses of each rule.",
        "Drive {start} to a fixed point under {rules}, one leftmost "
        "application at a time (at most {cap} steps). Give the per-rule "
        "usage counts.",
    ),
}


def rewrite(start, rules, chain=None, limit=1500):
    """(applications, usage dict, normal form); optionally emits steps."""
    value = start
    usage = {rule: 0 for rule in rules}
    applications = 0
    while True:
        for rule in rules:
            lhs, rhs = rule.split(" -> ")
            position = value.find(lhs)
            if position != -1:
                new_value = (value[:position] + rhs
                             + value[position + len(lhs):])
                usage[rule] += 1
                applications += 1
                if chain is not None:
                    chain.apply("RW_STEP", f"{lhs}@{position}", new_value)
                value = new_value
                break
        else:
            return applications, usage, value
        if applications > limit:  # pragma: no cover - sorting terminates
            raise ValueError("rewriting failed to terminate")


class TokenRewriteGenerator(ProblemGenerator):
    """Tier-length rewriting chains to a normal form (depth strand)."""

    VARIANTS = ("normal_form", "step_count", "rule_usage_count")
    BASE_DIFFICULTY = 3

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
        if tier == "d200":
            target = min(target, 180)  # ~74-char rows keep the 16k cap
        lo, hi = TIER_FLOORS[tier], target + 15

        system = ("sort3" if variant == "rule_usage_count"
                  else random.choice(sorted(SYSTEMS)))
        rules = SYSTEMS[system]
        for _ in range(4000):
            if system == "sort2":
                j = random.randint(4, 18)
                k = max(1, target // j + random.randint(-4, 4))
                blocks = "b" * j + "a" * k
            else:
                base = max(2, int((target / 3) ** 0.5))
                i, j, k = (max(1, base + random.randint(-3, 4))
                           for _ in range(3))
                blocks = "c" * i + "b" * j + "a" * k
            chars = list(blocks)
            # a wide scramble spreads the start-string space (capacity);
            # the window screen below keeps the count on-tier anyway
            for _ in range(random.randint(len(chars), 5 * len(chars))):
                p_swap = random.randrange(len(chars) - 1)
                chars[p_swap], chars[p_swap + 1] = (chars[p_swap + 1],
                                                    chars[p_swap])
            start = "".join(chars)
            if len(start) > 28:
                continue
            applications, usage, normal = rewrite(start, rules)
            if lo <= applications <= hi:
                break
        else:  # pragma: no cover - block sizing lands in-window
            raise ValueError("no start string fit the tier")

        chain = Chain(start,
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant("count of a (letters are conserved)",
                            lambda v, k: v.count("a"))
        rewrite(start, rules, chain=chain)

        cap = ((applications + 24) // 25) * 25
        rules_txt = "; ".join(rules)
        if variant == "normal_form":
            answer = normal
        elif variant == "step_count":
            answer = str(applications)
        else:
            answer = "; ".join(f"{rule.split(' ')[0]}: {usage[rule]}"
                               for rule in rules)
        problem = random.choice(PROMPTS[variant]).format(
            start=start, rules=rules_txt, cap=cap)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"token_rewrite_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
