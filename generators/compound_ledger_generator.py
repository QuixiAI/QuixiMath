"""A long account ledger with exact-cents interest (depth strand).

Strand F of ``plans/depth_plan.md``. N = tier events: deposits and
withdrawals in quarter multiples, plus periodic interest that stays
exact for *any* balance by crediting r% of the whole-dollar part only
(D dollars -> r*D cents — the floor a real bank applies), with the rate
stated once in the problem header.

Variants:

- ``final_balance``: the closing balance.
- ``interest_earned``: the sum of every interest credit.
- ``first_negative``: overdrafts allowed; which event first sends the
  balance below zero (screened to happen in the last quarter of the
  ledger, so the whole chain matters).
- ``statement_check``: the closing balance, re-derived in a ``CHECK``
  as start + deposits − withdrawals + interest.

Op-codes: ``A`` / ``S`` (established, money fields), ``INTEREST`` (new:
``INTEREST|<balance>|r% of $D = <c>¢|<balance'>``), ``CHECK``
(established), ``MILESTONE`` (balance cents mod 9) at ``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, cents_txt, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

RATES = (1, 2, 5)

PROMPTS = {
    "final_balance": (
        "An account opens at {start}. Interest events credit {r}% of the "
        "whole-dollar balance, in cents. Process the following {n} events "
        "in order: {events}. What is the closing balance?",
        "A ledger starts at {start}; each interest event credits {r}% of "
        "the whole-dollar balance in cents. Work through all {n} events "
        "in order: {events}. Report the closing balance.",
        "Starting from {start}, with interest events crediting {r}% of "
        "the whole-dollar balance, post these {n} events in order: "
        "{events}. Give the final balance.",
        "Open a statement at {start}. Interest credits {r}% of the "
        "whole-dollar balance in cents. Apply the {n} events in order "
        "({events}) and state the closing balance.",
    ),
    "interest_earned": (
        "An account opens at {start}. Interest events credit {r}% of the "
        "whole-dollar balance, in cents. Process the following {n} events "
        "in order: {events}. How much interest is credited in total?",
        "A ledger starts at {start}; each interest event credits {r}% of "
        "the whole-dollar balance in cents. Work through all {n} events "
        "in order: {events}. Report the total interest earned.",
        "Starting from {start}, with interest events crediting {r}% of "
        "the whole-dollar balance, post these {n} events in order: "
        "{events}. What do the interest credits sum to?",
        "Open a statement at {start}. Interest credits {r}% of the "
        "whole-dollar balance in cents. Apply the {n} events in order "
        "({events}) and total the interest.",
    ),
    "first_negative": (
        "An account opens at {start} with overdrafts permitted. Interest "
        "events credit {r}% of the whole-dollar balance, in cents. "
        "Process the following {n} events in order: {events}. After "
        "which event does the balance first go negative?",
        "A ledger starts at {start} (overdrafts allowed); each interest "
        "event credits {r}% of the whole-dollar balance in cents. Work "
        "through all {n} events in order: {events}. Identify the first "
        "event that overdraws the account.",
        "Starting from {start}, overdrafts permitted, with interest "
        "events crediting {r}% of the whole-dollar balance, post these "
        "{n} events in order: {events}. Which event first takes the "
        "balance below zero?",
        "Open a statement at {start}; overdrafts are allowed and "
        "interest credits {r}% of the whole-dollar balance in cents. "
        "Apply the {n} events in order ({events}) and report the first "
        "event that leaves a negative balance.",
    ),
    "statement_check": (
        "An account opens at {start}. Interest events credit {r}% of the "
        "whole-dollar balance, in cents. Process the following {n} events "
        "in order: {events}. State the closing balance and verify it as "
        "start plus deposits minus withdrawals plus interest.",
        "A ledger starts at {start}; each interest event credits {r}% of "
        "the whole-dollar balance in cents. Work through all {n} events "
        "in order: {events}. Report the closing balance, checked against "
        "the statement totals.",
        "Starting from {start}, with interest events crediting {r}% of "
        "the whole-dollar balance, post these {n} events in order: "
        "{events}. Give the final balance and confirm it from the "
        "column totals.",
        "Open a statement at {start}. Interest credits {r}% of the "
        "whole-dollar balance in cents. Apply the {n} events in order "
        "({events}), then reconcile the closing balance against start "
        "plus deposits minus withdrawals plus interest.",
    ),
}


def _events(n, rng):
    """[(kind, amount_or_None)] with interest roughly every 8-12 events."""
    out = []
    next_interest = rng.randint(4, 10)
    for index in range(n):
        if index == next_interest:
            out.append(("interest", None))
            next_interest += rng.randint(8, 12)
            continue
        kind = rng.choice(("deposit", "withdraw"))
        out.append((kind, rng.randrange(25, 15_001, 25)))
    return out


def _run(start, events, rate, tier, allow_negative):
    """(chain, interest_total, deposits, withdrawals, first_negative,
    peak)."""
    chain = Chain(start, render=cents_txt,
                  milestone_spacing=(True if tier != "d50" else None))
    chain.set_invariant("balance cents mod 9", lambda v, k: v % 9)
    interest_total = deposits = withdrawals = 0
    first_negative = None
    peak = start
    for index, (kind, amount) in enumerate(events, start=1):
        if kind == "interest":
            whole_dollars = max(chain.value, 0) // 100
            credit = rate * whole_dollars
            interest_total += credit
            chain.apply("INTEREST",
                        f"{rate}% of ${whole_dollars} = {credit} cents",
                        chain.value + credit)
        elif kind == "deposit":
            deposits += amount
            chain.apply("A", cents_txt(amount), chain.value + amount)
        else:
            withdrawals += amount
            chain.apply("S", cents_txt(amount), chain.value - amount)
        if first_negative is None and chain.value < 0:
            first_negative = index
        peak = max(peak, chain.value)
    return (chain, interest_total, deposits, withdrawals, first_negative,
            peak)


def _event_phrase(kind, amount):
    if kind == "interest":
        return "interest"
    verb = "deposit" if kind == "deposit" else "withdraw"
    return f"{verb} {cents_txt(amount)}"


class CompoundLedgerGenerator(ProblemGenerator):
    """Tier-length exact-cents ledgers (depth strand)."""

    VARIANTS = ("final_balance", "interest_earned", "first_negative",
                "statement_check")
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
        allow_negative = variant == "first_negative"

        for _ in range(2000):
            start = random.randrange(200_00, 900_01, 25)
            rate = random.choice(RATES)
            events = _events(n, random)
            (chain, interest_total, deposits, withdrawals,
             first_negative, peak) = _run(start, events, rate, tier,
                                          allow_negative)
            if peak > 5_000_00:
                continue
            if allow_negative:
                # The overdraft must land late so the whole chain matters.
                if (first_negative is not None
                        and first_negative >= (3 * n) // 4):
                    break
            else:
                if first_negative is None and chain.value <= 2_000_00:
                    break
        else:  # pragma: no cover - random walks satisfy this quickly
            raise ValueError("no ledger satisfied the variant's shape")

        event_list = "; ".join(_event_phrase(kind, amount)
                               for kind, amount in events)
        if variant == "final_balance":
            answer = cents_txt(chain.value)
        elif variant == "interest_earned":
            answer = cents_txt(interest_total)
        elif variant == "first_negative":
            answer = (f"event {first_negative}; "
                      f"balance {cents_txt(_balance_after(start, events, rate, first_negative))}")
        else:
            reconciled = start + deposits - withdrawals + interest_total
            chain.steps.append(step(
                "CHECK", "statement totals",
                f"{cents_txt(start)} + {cents_txt(deposits)} - "
                f"{cents_txt(withdrawals)} + {cents_txt(interest_total)}",
                cents_txt(reconciled)))
            answer = cents_txt(chain.value)
        problem = random.choice(PROMPTS[variant]).format(
            start=cents_txt(start), r=rate, n=n, events=event_list)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"compound_ledger_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )


def _balance_after(start, events, rate, count):
    balance = start
    for kind, amount in events[:count]:
        if kind == "interest":
            balance += rate * (max(balance, 0) // 100)
        elif kind == "deposit":
            balance += amount
        else:
            balance -= amount
    return balance
