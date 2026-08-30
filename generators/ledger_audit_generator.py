"""Audit a long claimed trace and find the one bad row (depth strand).

Strand V of ``plans/depth_plan.md`` — the long-form critic record. The
problem presents a CLAIMED table of tier-many rows with exactly one
corrupted result; every later claimed row propagates consistently from
the corrupted value (the classic single-error ledger), so only genuine
row-by-row verification finds it. One record in five is an error-free
control.

The trace re-derives the true running value at every row: a chained
``AUDIT_ROW`` per correct row (previous true value first, the row's
operation and verdict in the middle, new true value last) and one
``AUDIT_FLAG`` at the bad row stating the claim and the truth — so the
whole audit is one unbroken dependency chain regardless of where the
error sits. (The established ``VERIFY``/``FLAG`` codes carry
index-first fields and are not reused.)

Variants (the underlying trace types):

- ``money_ledger``: deposits/withdrawals in exact cents.
- ``running_sum``: signed integer additions.
- ``affine_table``: x -> (a*x + b) mod m rows.

Answers: ``first error at row 73; correct final balance $418.20`` (or
value), and ``no errors; final balance $973.25 confirmed`` for the
control.

Op-codes: ``AUDIT_ROW`` / ``AUDIT_FLAG`` (new), ``MILESTONE``, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, cents_txt, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "money_ledger": (
        "An account starts at {start}. A clerk posted the following {n} "
        "rows, but at most one result may be wrong (every later row was "
        "computed from it consistently): {rows}. Audit the ledger row by "
        "row. Identify the first wrong row, or confirm there is none, "
        "and give the correct final balance.",
        "A ledger opens at {start} and lists {n} rows ({rows}); at most "
        "one posted result is wrong, with all later rows propagated from "
        "it. Check every row in order and report the first error (if "
        "any) and the correct closing balance.",
        "Starting from {start}, the {n} rows as posted are: {rows}. At most "
        "one result was mis-copied and everything after follows from it. "
        "Verify each row and state the first bad row, or that all are "
        "fine, with the correct final balance.",
        "Audit this statement: opening balance {start}, then {n} rows "
        "({rows}). No more than one result is wrong; later rows build on "
        "it. Find the first error, or confirm none, and give the true "
        "closing balance.",
    ),
    "running_sum": (
        "A tally starts at {start}. The following {n} rows were posted, "
        "but at most one result may be wrong (later rows were computed "
        "from it): {rows}. Audit the tally row by row. Identify the "
        "first wrong row, or confirm there is none, and give the "
        "correct final value.",
        "A running total opens at {start} and lists {n} rows ({rows}); "
        "at most one posted result is wrong, with all later rows "
        "propagated from it. Check each row in order and report the "
        "first error (if any) and the correct final value.",
        "Starting from {start}, the {n} rows as posted are: {rows}. At most "
        "one result was mis-copied and everything after follows from it. "
        "Verify each row and state the first bad row, or that all are "
        "fine, with the correct final value.",
        "Audit this tally: opening value {start}, then {n} rows "
        "({rows}). No more than one result is wrong; later rows build on "
        "it. Find the first error, or confirm none, and give the true "
        "final value.",
    ),
    "affine_table": (
        "An iteration table for x -> ({a}x + {b}) mod {m} starts at "
        "x = {start}. The following {n} rows were posted, but at most "
        "one result may be wrong (later rows were computed from it): "
        "{rows}. Audit the table row by row. Identify the first wrong "
        "row, or confirm there is none, and give the correct final "
        "value.",
        "A table of x -> ({a}x + {b}) mod {m} from x = {start} lists {n} "
        "rows ({rows}); at most one posted result is wrong, with later "
        "rows propagated from it. Check each row in order and report "
        "the first error (if any) and the correct final value.",
        "Starting from x = {start}, the {n} rows as posted for x -> ({a}x + "
        "{b}) mod {m} are: {rows}. At most one result was mis-copied and "
        "everything after follows from it. Verify each row and state "
        "the first bad row, or that all are fine, with the correct "
        "final value.",
        "Audit this iteration table for x -> ({a}x + {b}) mod {m}: "
        "start x = {start}, then {n} rows ({rows}). No more than one "
        "result is wrong; later rows build on it. Find the first error, "
        "or confirm none, and give the true final value.",
    ),
}


class LedgerAuditGenerator(ProblemGenerator):
    """Find the one bad row in a tier-length claimed trace."""

    VARIANTS = ("money_ledger", "running_sum", "affine_table")
    BASE_DIFFICULTY = 3
    CONTROL_WEIGHT = 0.2  # error-free records

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
        if tier == "d200":
            # claimed rows + audit rows both scale with n; money rows are
            # the widest (~90 chars combined), so the cap is per-variant
            n = min(n, {"money_ledger": 190, "running_sum": 235,
                        "affine_table": 215}[variant])
        clean = random.random() < self.CONTROL_WEIGHT

        if variant == "money_ledger":
            start = random.randrange(200_00, 900_01, 25)
            deltas = []
            value = start
            for _ in range(n):
                headroom, floor_room = 1_500_00 - value, value
                sign = 1 if (floor_room < 25 or
                             (headroom >= 25 and random.random() < 0.5)) else -1
                amount = random.randrange(
                    25, min(120_00, headroom if sign > 0 else floor_room) + 1,
                    25)
                deltas.append(sign * amount)
                value += sign * amount
            apply = lambda v, d: v + d
            op_txt = lambda d: (f"+{cents_txt(d)}" if d > 0
                                else f"-{cents_txt(-d)}")
            render = cents_txt
            corrupt = lambda v: v + random.choice((-1, 1)) * random.randrange(
                25, 20_01, 25)
            unit = "balance"
            fields = {}
        elif variant == "running_sum":
            start = random.randint(20, 90)
            deltas = [random.choice((-1, 1)) * random.randint(3, 40)
                      for _ in range(n)]
            apply = lambda v, d: v + d
            op_txt = lambda d: f"+{d}" if d > 0 else str(d)
            render = str
            corrupt = lambda v: v + random.choice((-1, 1)) * random.randint(
                1, 9)
            unit = "value"
            fields = {}
        else:
            m = random.randint(53, 997)
            a = random.randint(2, min(m - 1, 12))
            b = random.randint(0, m - 1)
            start = random.randrange(m)
            deltas = [None] * n
            apply = lambda v, d: (a * v + b) % m
            op_txt = lambda d: "iterate"
            render = str
            corrupt = lambda v: (v + random.randint(1, m - 1)) % m
            unit = "value"
            fields = {"a": a, "b": b, "m": m}

        true_values = [start]
        for d in deltas:
            true_values.append(apply(true_values[-1], d))

        if clean:
            error_row = None
            claimed = true_values[1:]
        else:
            error_row = random.randint(max(2, n // 5), n - 2)
            bad = corrupt(true_values[error_row])
            while bad == true_values[error_row]:  # pragma: no cover
                bad = corrupt(true_values[error_row])
            claimed = list(true_values[1:])
            claimed[error_row - 1] = bad
            value = bad
            for index in range(error_row, n):
                value = apply(value, deltas[index])
                claimed[index] = value

        rows = "; ".join(f"{k}: {op_txt(d)} = {render(c)}"
                         for k, (d, c) in enumerate(zip(deltas, claimed),
                                                    start=1))

        chain = Chain(start, render=render,
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant(
            f"true {unit} mod 9",
            (lambda v, k: v % 9))
        for k, (d, c) in enumerate(zip(deltas, claimed), start=1):
            true_next = apply(chain.value, d)
            if error_row is not None and k == error_row:
                chain.apply("AUDIT_FLAG",
                            f"row {k} claims {render(c)}; truth", true_next)
            else:
                verdict = "ok" if c == true_next else "consistent"
                chain.apply("AUDIT_ROW", f"row {k}: {op_txt(d)} {verdict}",
                            true_next)

        final = render(chain.value)
        if clean:
            answer = f"no errors; final {unit} {final} confirmed"
        else:
            answer = f"first error at row {error_row}; correct final {unit} {final}"
        fields.update(start=render(start) if variant != "affine_table"
                      else start, n=n, rows=rows)
        problem = random.choice(PROMPTS[variant]).format(**fields)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"ledger_audit_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
