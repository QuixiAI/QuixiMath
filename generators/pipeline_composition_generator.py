"""Serial pipelines of catalog procedures with skills metadata
(depth strand).

Strand C of ``plans/depth_plan.md``. One quantity flows through
tier-many chained arithmetic links spread across dozens of small
stages; every stage is a procedure the catalog already teaches, the
output of stage k is the input of stage k+1, and a ``PIPE_STAGE``
annotation row marks each stage with the skill it reuses. The record
carries an ordered ``skills`` list exactly like ``ScenarioGenerator``,
so these rows feed the ``judgment_composition_eval`` config's serial
half. Following the applied strand's defining rule, the story sentences
never name the procedures — only the situation (enforced here by the
same ``applied_common.METHOD_WORDS`` scan, in this module's tests).

Stage bank (each stage is 1-2 chained links; the running count is kept
an exact integer in [5, 2,000,000] by per-stage divisibility and bound
screening):

- percent gain/loss via a reduced factor (x -> x * a/b): 2 links.
- ratio keep ("only a of every b pass"): 2 links.
- flat add/remove: 1 link.
- repack multiply / even split: 1 link.

Every stage guard also caps its OUTPUT at 100,000, so growth stages
reject themselves when the count is high and the pipeline
self-regulates; intermediate products (value x small factor) therefore
never exceed 1.2 million.

Variants: ``final_count``, ``stage_audit`` (milestones at every tier;
answer also states how many stages ran).

Op-codes: ``M`` / ``D`` / ``A`` / ``S`` (established, chained),
``PIPE_STAGE`` (new annotation row — listed with ``MILESTONE`` as
non-chain-breaking), ``MILESTONE``, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, MILESTONE_SPACING, TIER_FLOORS, pick_tier,
                          tier_difficulty, tier_target)

DEPTH = True

PROMPTS = {
    "final_count": (
        "A shipment starts at {v} items and passes through {k} stages in "
        "order: {stages}. How many items remain at the end?",
        "Starting from {v} items, work through the {k} stages in order "
        "({stages}). Report the final count.",
        "An order of {v} items goes through {k} stages, one after "
        "another: {stages}. What count comes out?",
        "Track {v} items through all {k} stages in sequence: {stages}. "
        "Give the final number of items.",
    ),
    "stage_audit": (
        "A shipment starts at {v} items and passes through {k} stages in "
        "order: {stages}. Report the final count and confirm the number "
        "of stages processed.",
        "Starting from {v} items, work through the {k} stages in order "
        "({stages}). Give the final count and the stage total.",
        "An order of {v} items goes through {k} stages, one after "
        "another: {stages}. State the resulting count and how many "
        "stages ran.",
        "Track {v} items through all {k} stages in sequence: {stages}. "
        "Report the final count together with the stage count.",
    ),
}

#: (skill, links, applicable?, apply, sentence) — sentences never name
#: the procedure.
PERCENTS = ((10, 11, 10), (20, 6, 5), (25, 5, 4), (50, 3, 2))
LOSSES = ((10, 9, 10), (20, 4, 5), (25, 3, 4), (50, 1, 2))
RATIOS = ((2, 3), (3, 4), (3, 5), (4, 5), (5, 6))


def _stage_bank(rng):
    """Draw one stage: (skill, sentence, [(op, operand_txt, fn)...])."""
    kind = rng.choice(("gain", "loss", "ratio", "add", "remove",
                       "repack", "split"))
    if kind == "gain":
        p, num, den = rng.choice(PERCENTS)
        return ("percent_change",
                f"demand grows the count by {p} for every 100",
                [("M", str(num), lambda v, num=num: v * num),
                 ("D", str(den), lambda v, den=den: v // den)],
                lambda v, num=num, den=den: (v % den == 0
                                             and v * num // den <= 100_000))
    if kind == "loss":
        p, num, den = rng.choice(LOSSES)
        return ("percent_change",
                f"spoilage removes {p} of every 100",
                [("M", str(num), lambda v, num=num: v * num),
                 ("D", str(den), lambda v, den=den: v // den)],
                lambda v, den=den: v % den == 0)
    if kind == "ratio":
        a, b = rng.choice(RATIOS)
        return ("ratio_split",
                f"only {a} of every {b} items pass inspection",
                [("M", str(a), lambda v, a=a: v * a),
                 ("D", str(b), lambda v, b=b: v // b)],
                lambda v, b=b: v % b == 0)
    if kind == "add":
        f = rng.randrange(5, 500, 5)
        return ("fixed_adjustment", f"a delivery adds {f} items",
                [("A", str(f), lambda v, f=f: v + f)],
                lambda v, f=f: v + f <= 100_000)
    if kind == "remove":
        f = rng.randrange(5, 500, 5)
        return ("fixed_adjustment", f"{f} items are set aside",
                [("S", str(f), lambda v, f=f: v - f)],
                lambda v, f=f: v - f >= 5)
    if kind == "repack":
        k = rng.choice((2, 3, 4, 6, 12))
        return ("unit_conversion",
                f"each item is repacked into {k} smaller packs",
                [("M", str(k), lambda v, k=k: v * k)],
                lambda v, k=k: v * k <= 100_000)
    k = rng.choice((2, 3, 4))
    return ("ratio_split",
            f"the lot is divided evenly {k} ways; keep one share",
            [("D", str(k), lambda v, k=k: v // k)],
            lambda v, k=k: v % k == 0 and v // k >= 5)


class PipelineCompositionGenerator(ProblemGenerator):
    """Serial skill pipelines with tier-length chains (depth strand)."""

    VARIANTS = ("final_count", "stage_audit")
    BASE_DIFFICULTY = 4

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
        lo, hi = TIER_FLOORS[tier], target + 15

        for _ in range(500):
            value = random.randrange(240, 4001, 60)  # rich in divisors
            milestone = True if (tier != "d50"
                                 or variant == "stage_audit") else None
            chain = Chain(value,
                          milestone_spacing=(MILESTONE_SPACING
                                             if milestone else None))
            chain.set_invariant("count mod 9", lambda v, k: v % 9)
            skills, sentences = [], []
            guard = 0
            while chain.links < lo and guard < 3000:
                guard += 1
                skill, sentence, ops, ok = _stage_bank(random)
                if not ok(chain.value):
                    continue
                if chain.links + len(ops) > hi:
                    break
                chain.steps.append(step("PIPE_STAGE", len(skills) + 1,
                                        skill))
                for op, operand, fn in ops:
                    chain.apply(op, operand, fn(chain.value))
                skills.append(skill)
                sentences.append(sentence)
            if lo <= chain.links <= hi and len(skills) >= 3:
                break
        else:  # pragma: no cover - stage mix always converges
            raise ValueError("no pipeline fit the tier")

        stage_list = "; ".join(f"{k}) {sentence}"
                               for k, sentence in enumerate(sentences,
                                                            start=1))
        if variant == "final_count":
            answer = str(chain.value)
        else:
            answer = f"{chain.value} items; {len(skills)} stages"
        problem = random.choice(PROMPTS[variant]).format(
            v=value, k=len(skills), stages=stage_list)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"pipeline_composition_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            skills=list(skills),
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
