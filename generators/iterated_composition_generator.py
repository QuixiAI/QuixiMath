"""Alternating Möbius maps from the anharmonic group (depth strand).

Strand I of ``plans/depth_plan.md``. The six maps

    x,  1-x,  1/x,  1/(1-x),  (x-1)/x,  x/(x-1)

form a group closed under composition (isomorphic to S3), so an
alternating sequence g, f, g, f, ... keeps every value inside the at
most six rationals of x0's orbit — bounded forever, exact forever.
The alternating sequence is eventually periodic with period dividing
2 * ord(g∘f) (1, 2, 3, 4, or 6 steps).

Variants:

- ``final_value``: apply the alternation for N stated steps; answer
  the exact value.
- ``cycle_length``: walk until the (value, next-map) state repeats (at
  most a stated cap); answer the period of the alternation.
- ``shortcut_check``: as ``final_value``, plus a ``CHECK`` that
  reducing N mod the period predicts the same value; composite answer
  ``period P; value v``.

Op-codes: ``MAP_APPLY`` (new: previous value first, the map applied in
the middle, new value last), ``CHECK``, ``MILESTONE``
((numerator + denominator) mod 9) at ``d100``+, ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, pick_tier, tier_difficulty, tier_target)

DEPTH = True

#: name -> (callable, printable rule). All six anharmonic maps.
MAPS = {
    "one_minus": (lambda x: 1 - x, "x -> 1 - x"),
    "reciprocal": (lambda x: 1 / x, "x -> 1/x"),
    "recip_complement": (lambda x: 1 / (1 - x), "x -> 1/(1 - x)"),
    "shifted_ratio": (lambda x: (x - 1) / x, "x -> (x - 1)/x"),
    "ratio_shift": (lambda x: x / (x - 1), "x -> x/(x - 1)"),
}

PROMPTS = {
    "final_value": (
        "Let x = {x0}. Alternately apply f: {f} and g: {g} (f first), "
        "for {n} applications in total. What exact value results?",
        "Starting from x = {x0}, apply f: {f}, then g: {g}, then f "
        "again, and so on, for {n} applications. Report the exact "
        "final value.",
        "Alternate the maps f: {f} and g: {g} on x = {x0}, beginning "
        "with f, for {n} applications. Give the exact result.",
        "Take x = {x0} through {n} applications that alternate f: {f} "
        "with g: {g}, starting with f. State the exact final value.",
    ),
    "cycle_length": (
        "Let x = {x0}. Alternately apply f: {f} and g: {g} (f first) "
        "until the value-and-turn state repeats (at most {cap} steps). "
        "What is the period of the alternation?",
        "Starting from x = {x0}, alternate f: {f} with g: {g} until the "
        "sequence starts repeating (at most {cap} steps). Report the "
        "period.",
        "Alternate f: {f} and g: {g} on x = {x0} until a full cycle "
        "closes (at most {cap} steps). Give the period length.",
        "Take x = {x0} through the alternation of f: {f} and g: {g} to "
        "its first full repeat (at most {cap} steps). State the period.",
    ),
    "shortcut_check": (
        "Let x = {x0}. Alternately apply f: {f} and g: {g} (f first) "
        "for {n} applications, then confirm the result by reducing the "
        "count modulo the alternation's period. Report the period and "
        "the exact value.",
        "Starting from x = {x0}, run {n} applications alternating "
        "f: {f} with g: {g}; verify via the period shortcut. Give the "
        "period and the value.",
        "Alternate f: {f} and g: {g} on x = {x0} for {n} applications "
        "and cross-check against the cycle structure. State the period "
        "and the exact result.",
        "Take x = {x0} through {n} applications, alternating f: {f} "
        "and g: {g}, and check the answer with the period. Report both.",
    ),
}


def _txt(fr):
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


def _orbit_ok(x0, f, g, length=16):
    """The alternation never hits a pole (0 or 1) in a full period."""
    value = x0
    for turn in range(length):
        if value in (0, 1):
            return False
        value = (f if turn % 2 == 0 else g)(value)
    return value not in (0, 1)


def _alternation_period(x0, f, g):
    """Smallest even p with the alternation returning to (x0, f's turn)."""
    value = x0
    for steps_taken in range(1, 13):
        value = (f if (steps_taken - 1) % 2 == 0 else g)(value)
        if steps_taken % 2 == 0 and value == x0:
            return steps_taken
    return 12  # pragma: no cover - group order bounds the period by 12


class IteratedCompositionGenerator(ProblemGenerator):
    """Long alternating-map chains with tiny bounded orbits."""

    VARIANTS = ("final_value", "cycle_length", "shortcut_check")
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
        n = tier_target(tier)

        for _ in range(500):
            f_name, g_name = random.sample(sorted(MAPS), 2)
            f, f_txt = MAPS[f_name]
            g, g_txt = MAPS[g_name]
            x0 = Fraction(random.randint(2, 12),
                          random.randint(2, 12))
            if x0 in (0, 1) or not _orbit_ok(x0, f, g):
                continue
            break
        else:  # pragma: no cover - most draws are pole-free
            raise ValueError("no pole-free alternation found")
        period = _alternation_period(x0, f, g)

        chain = Chain(x0, render=_txt,
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant(
            "numerator + denominator mod 9",
            lambda v, k: (v.numerator + v.denominator) % 9)

        if variant == "cycle_length":
            # whole cycles, rounded UP so the walk never dips below the
            # tier floor (period 6 truncating 40 -> 36 would)
            walk = period * ((n + period - 1) // period)
            cap = ((walk + 24) // 25) * 25
        else:
            walk = n
        for k in range(walk):
            mapping, rule = (f, f_txt) if k % 2 == 0 else (g, g_txt)
            chain.apply("MAP_APPLY", rule, mapping(chain.value))

        steps = list(chain.steps)
        if variant == "cycle_length":
            answer = str(period)
            problem = random.choice(PROMPTS[variant]).format(
                x0=_txt(x0), f=f_txt, g=g_txt, cap=cap)
        else:
            value = chain.value
            if variant == "shortcut_check":
                reduced = n % period
                shortcut = x0
                for k in range(reduced):
                    shortcut = (f if k % 2 == 0 else g)(shortcut)
                steps.append(step(
                    "CHECK", "period shortcut",
                    f"{n} mod {period} = {reduced} steps give "
                    f"{_txt(shortcut)}",
                    f"full walk gives {_txt(value)}"))
                answer = f"period {period}; value {_txt(value)}"
            else:
                answer = _txt(value)
            problem = random.choice(PROMPTS[variant]).format(
                x0=_txt(x0), f=f_txt, g=g_txt, n=n)

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"iterated_composition_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
