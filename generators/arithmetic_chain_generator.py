"""One running value through a long chain of small exact operations.

The first depth-strand generator (``plans/depth_plan.md`` Strand A): the
procedure is elementary arithmetic, the difficulty is staying on track
for 40-260 dependent steps. Intermediates are bounded by construction —
integers stay inside (10, 500), fractions keep denominators dividing 12
and stay inside (0, 60), money stays inside [$0, $1000] in exact
quarter-cent-free whole cents. Variants:

- ``integer_chain``: add / subtract / double / halve on integers.
- ``fraction_chain``: add / subtract twelfths, double, halve (only when
  exact), on fractions with denominator dividing 12.
- ``money_chain``: a ledger of received / paid amounts in exact cents.
- ``missing_start``: the operations and the final value are given; the
  trace runs the inverse chain backward to recover the start.

Op-codes: ``A`` / ``S`` / ``M`` / ``D`` (established) emitted through the
strand's ``Chain`` (previous value first, new value last), ``MILESTONE``
at ``d100``+ (invariant: the integer value mod 9; for fractions, the
numerator of the value over 12 mod 9; for money, the cents mod 9), and
``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, cents_txt, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "integer_chain": (
        "Start with {start}. Apply the following {n} steps in order: {ops}. "
        "What is the final value?",
        "A counter begins at {start}. Carry out these {n} steps in order: "
        "{ops}. Report the final value.",
        "Beginning from {start}, work through all {n} steps in order: {ops}. "
        "What number results?",
        "Take {start} and apply, one at a time, the {n} steps: {ops}. "
        "Give the final value.",
    ),
    "fraction_chain": (
        "Start with {start}. Apply the following {n} steps in order: {ops}. "
        "Give the final value as an exact fraction.",
        "A running total begins at {start}. Carry out these {n} steps in "
        "order: {ops}. Report the exact final value.",
        "Beginning from {start}, work through all {n} steps in order: {ops}. "
        "What exact value results?",
        "Take {start} and apply, one at a time, the {n} steps: {ops}. "
        "Give the exact final value.",
    ),
    "money_chain": (
        "An account starts at {start} and records the following {n} events "
        "in order: {ops}. What is the final balance?",
        "A club fund begins at {start}. It then logs these {n} events in "
        "order: {ops}. Report the final balance.",
        "Starting from a balance of {start}, process all {n} events in "
        "order: {ops}. What balance results?",
        "A till opens at {start}. Working through the {n} events in order "
        "({ops}), find the closing balance.",
    ),
    "missing_start": (
        "After applying the following {n} steps in order ({ops}), the "
        "result is {end}. What was the starting value?",
        "A number was put through these {n} steps in order: {ops}. The "
        "final value is {end}. Find the starting value.",
        "Working through all {n} steps in order ({ops}) turned an unknown "
        "starting value into {end}. What was it?",
        "The {n} steps {ops}, applied in order, produced {end}. Recover "
        "the starting value.",
    ),
}


def _frac_txt(fr):
    """House fraction rendering: integers plain, otherwise ``a/b``."""
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


def _integer_ops(start, n, rng):
    """``[(kind, operand, result), ...]`` keeping every value in (10, 500)."""
    value = start
    ops = []
    for _ in range(n):
        choices = []
        if value <= 240:
            choices.append("double")
        if value % 2 == 0 and value >= 24:
            choices.append("halve")
        if value <= 440:
            choices.append("add")
        if value >= 72:
            choices.append("subtract")
        kind = rng.choice(choices)
        if kind == "add":
            operand = rng.randint(5, min(60, 495 - value))
            value += operand
        elif kind == "subtract":
            operand = rng.randint(5, min(60, value - 11))
            value -= operand
        elif kind == "double":
            operand = 2
            value *= 2
        else:
            operand = 2
            value //= 2
        ops.append((kind, operand, value))
    return ops


def _fraction_ops(start, n, rng):
    """Chain on fractions with denominator dividing 12, value in (0, 60)."""
    value = start
    ops = []
    for _ in range(n):
        choices = []
        if value <= 28:
            choices.append("double")
        if (value * 12).numerator % 2 == 0 and value >= 2:
            choices.append("halve")
        if value <= 55:
            choices.append("add")
        if value >= 5:
            choices.append("subtract")
        kind = rng.choice(choices)
        if kind == "add":
            operand = Fraction(rng.randint(1, 48), 12)
            value += operand
        elif kind == "subtract":
            operand = Fraction(rng.randint(1, min(48, int((value - 1) * 12))),
                               12)
            value -= operand
        elif kind == "double":
            operand = 2
            value *= 2
        else:
            operand = 2
            value /= 2
        ops.append((kind, operand, value))
    return ops


def _money_ops(start_cents, n, rng):
    """Ledger events in whole cents, balance kept inside [0, $1000]."""
    value = start_cents
    ops = []
    for _ in range(n):
        headroom = 100_000 - value
        floor_room = value
        choices = []
        if headroom >= 25:
            choices.append("receive")
        if floor_room >= 25:
            choices.append("pay")
        kind = rng.choice(choices)
        room = headroom if kind == "receive" else floor_room
        operand = rng.randrange(25, min(room, 15_000) + 1, 25)
        value += operand if kind == "receive" else -operand
        ops.append((kind, operand, value))
    return ops


def _op_phrase(kind, operand, render):
    if kind in ("add", "receive"):
        verb = "add" if kind == "add" else "receive"
        return f"{verb} {render(operand)}"
    if kind in ("subtract", "pay"):
        verb = "subtract" if kind == "subtract" else "pay"
        return f"{verb} {render(operand)}"
    return "double it" if kind == "double" else "halve it"


_STEP_OPS = {"add": "A", "receive": "A", "subtract": "S", "pay": "S",
             "double": "M", "halve": "D"}


class ArithmeticChainGenerator(ProblemGenerator):
    """Long bounded chains of elementary arithmetic (depth strand)."""

    VARIANTS = ("integer_chain", "fraction_chain", "money_chain",
                "missing_start")
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
        n = tier_target(tier)

        if variant == "money_chain":
            start = random.randrange(10_000, 60_001, 25)
            ops = _money_ops(start, n, random)
            render = cents_txt
            invariant = ("balance cents mod 9", lambda v, k: v % 9)
        elif variant == "fraction_chain":
            start = Fraction(random.randint(13, 300), 12)
            ops = _fraction_ops(start, n, random)
            render = _frac_txt
            invariant = ("numerator over 12 mod 9",
                         lambda v, k: (v * 12).numerator % 9)
        else:  # integer_chain and missing_start share the integer engine
            start = random.randint(20, 200)
            ops = _integer_ops(start, n, random)
            render = str
            invariant = ("value mod 9", lambda v, k: v % 9)

        op_list = "; ".join(_op_phrase(kind, operand, render)
                            for kind, operand, _ in ops)
        end = ops[-1][2]

        if variant == "missing_start":
            problem = random.choice(PROMPTS[variant]).format(
                n=n, ops=op_list, end=render(end))
            chain = Chain(end, render=render,
                          milestone_spacing=(True if tier != "d50" else None))
            chain.set_invariant(*invariant)
            # Run the inverse chain backward through the operations.
            for kind, operand, _ in reversed(ops):
                previous = chain.value
                if kind == "add":
                    chain.apply("S", render(operand), previous - operand,
                                extra="undo add")
                elif kind == "subtract":
                    chain.apply("A", render(operand), previous + operand,
                                extra="undo subtract")
                elif kind == "double":
                    chain.apply("D", "2", previous // 2, extra="undo double")
                else:
                    chain.apply("M", "2", previous * 2, extra="undo halve")
            answer = render(start)
        else:
            problem = random.choice(PROMPTS[variant]).format(
                n=n, start=render(start), ops=op_list)
            chain = Chain(start, render=render,
                          milestone_spacing=(True if tier != "d50" else None))
            chain.set_invariant(*invariant)
            for kind, operand, result in ops:
                chain.apply(_STEP_OPS[kind], render(operand), result)
            answer = render(end)

        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"arithmetic_chain_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
