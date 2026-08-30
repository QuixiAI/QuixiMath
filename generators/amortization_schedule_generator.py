"""Period-by-period amortization schedules in exact cents (depth strand).

Strand F of ``plans/depth_plan.md``. Interest stays exact for any
balance via the whole-dollar floor (interest = r% of the whole-dollar
balance, in cents — the header states the rule), so every period is one
chained ``AMORT_STEP``: previous balance first, the interest/principal
split in the middle, new balance last. The final period pays exactly
the remaining balance plus its interest.

Variants:

- ``balance_after_k``: a long loan truncated at tier-many periods;
  answer the balance then.
- ``payoff_period``: payment sized (by a float guide, then screened by
  exact simulation) so the loan retires inside the tier window; answer
  the period count.
- ``total_interest``: same schedule; answer the interest total.
- ``extra_payment``: one extra principal payment at a stated period;
  answer the new payoff period.

Op-codes: ``AMORT_STEP`` (new), ``MILESTONE`` (balance cents mod 9) at
``d100``+, ``Z``.
"""
import random

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, cents_txt, pick_tier,
                          tier_difficulty, tier_target)

DEPTH = True

RATES = (1, 2)  # percent per period, on the whole-dollar balance

PROMPTS = {
    "balance_after_k": (
        "A loan of {principal} charges {r}% per period on the "
        "whole-dollar balance (in cents) and is repaid at {payment} per "
        "period. Work the schedule for {n} periods. What is the balance "
        "then?",
        "Amortize {principal} at {r}% per period (interest on the "
        "whole-dollar balance, in cents) with payments of {payment}, "
        "period by period, for {n} periods. Report the remaining "
        "balance.",
        "A {principal} loan accrues {r}% per period on its whole-dollar "
        "balance and receives {payment} each period. After {n} periods "
        "of the schedule, what balance remains?",
        "Walk {n} periods of the schedule for a {principal} loan at {r}% "
        "per period (whole-dollar interest, in cents), payment "
        "{payment}. Give the balance at the end.",
    ),
    "payoff_period": (
        "A loan of {principal} charges {r}% per period on the "
        "whole-dollar balance (in cents) and is repaid at {payment} per "
        "period (at most {cap} periods). In which period is it paid "
        "off?",
        "Amortize {principal} at {r}% per period (whole-dollar interest, "
        "in cents) with payments of {payment} until the balance reaches "
        "zero (at most {cap} periods). Report the payoff period.",
        "A {principal} loan accrues {r}% per period on its whole-dollar "
        "balance; {payment} arrives each period (at most {cap} "
        "periods). When does the balance hit zero?",
        "Walk the schedule for a {principal} loan at {r}% per period "
        "(whole-dollar interest, in cents), payment {payment}, to "
        "payoff (at most {cap} periods). State the payoff period.",
    ),
    "total_interest": (
        "A loan of {principal} charges {r}% per period on the "
        "whole-dollar balance (in cents) and is repaid at {payment} per "
        "period (at most {cap} periods). How much interest is paid in "
        "total?",
        "Amortize {principal} at {r}% per period (whole-dollar interest, "
        "in cents) with payments of {payment} to payoff (at most {cap} "
        "periods). Report the total interest.",
        "A {principal} loan accrues {r}% per period on its whole-dollar "
        "balance; {payment} arrives each period until payoff (at most "
        "{cap} periods). Total the interest charges.",
        "Walk the schedule for a {principal} loan at {r}% per period "
        "(whole-dollar interest, in cents), payment {payment}, to "
        "payoff (at most {cap} periods). Give the interest total.",
    ),
    "extra_payment": (
        "A loan of {principal} charges {r}% per period on the "
        "whole-dollar balance (in cents) and is repaid at {payment} per "
        "period, with one extra {extra} principal payment in period "
        "{j} (at most {cap} periods). In which period is it paid off?",
        "Amortize {principal} at {r}% per period (whole-dollar interest, "
        "in cents), payment {payment}, plus an extra {extra} toward "
        "principal in period {j} (at most {cap} periods). Report the "
        "payoff period.",
        "A {principal} loan accrues {r}% per period on its whole-dollar "
        "balance; {payment} arrives each period and period {j} adds an "
        "extra {extra} to principal (at most {cap} periods). When does "
        "the balance reach zero?",
        "Walk the schedule for a {principal} loan at {r}% per period "
        "(whole-dollar interest, in cents), payment {payment}, extra "
        "{extra} in period {j}, to payoff (at most {cap} periods). "
        "State the payoff period.",
    ),
}


def _simulate(principal, rate, payment, extra_at=None, extra=0,
              stop_at=None, chain=None):
    """(periods, interest_total, final_balance) — exact simulation.

    With ``chain`` given, emits one AMORT_STEP per period.
    """
    balance = principal
    interest_total = 0
    period = 0
    while balance > 0:
        period += 1
        interest = rate * (balance // 100)
        pay = payment + (extra if extra_at == period else 0)
        if pay >= balance + interest:  # final period clears the loan
            pay = balance + interest
        principal_part = pay - interest
        interest_total += interest
        new_balance = balance - principal_part
        if chain is not None:
            chain.apply("AMORT_STEP",
                        f"k={period}, i={cents_txt(interest)}, "
                        f"p={cents_txt(principal_part)}", new_balance)
        balance = new_balance
        if stop_at is not None and period == stop_at:
            break
        if period > 1000:  # pragma: no cover - payments always amortize
            raise ValueError("schedule failed to terminate")
    return period, interest_total, balance


class AmortizationScheduleGenerator(ProblemGenerator):
    """Tier-length exact amortization schedules (depth strand)."""

    VARIANTS = ("balance_after_k", "payoff_period", "total_interest",
                "extra_payment")
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
        lo, hi = TIER_FLOORS[tier], n + 15

        for _ in range(8000):
            principal = random.randrange(5_000_00, 80_000_01, 100)
            rate = random.choice(RATES)
            if variant == "balance_after_k":
                # payment just above the initial interest: the balance
                # strictly DECREASES (never negative amortization, so the
                # state stays bounded by the principal) but payoff lies
                # far beyond the truncation point n
                initial_interest = rate * (principal // 100)
                payment = ((initial_interest
                            + random.randrange(25_00, 150_01, 25))
                           // 25 * 25)
                periods, _, _ = _simulate(principal, rate, payment,
                                          stop_at=n + 1)
                if periods > n:
                    extra_at = extra = None
                    break
            else:
                # float guide for the payment, exact screen on payoff;
                # clamp above the initial interest - at 2% and n ~ 260
                # the guide's margin is smaller than the $25 round-down,
                # which would make the schedule non-terminating
                r = rate / 100
                # extra_payment shortens payoff by up to ~45 periods; a
                # guide at n+20 keeps the shortened payoff inside the
                # window even when n is drawn at the tier floor
                n_guide = n + 20 if variant == "extra_payment" else n
                guide = principal * r / (1 - (1 + r) ** -n_guide)
                payment = max(int(guide // 25 * 25),
                              rate * (principal // 100) + 25_00)
                extra_at = extra = None
                if variant == "extra_payment":
                    extra_at = random.randint(max(2, n // 4), n // 2)
                    extra = random.randrange(500_00, 3_000_01, 25)
                try:
                    periods, _, _ = _simulate(principal, rate, payment,
                                              extra_at=extra_at,
                                              extra=extra)
                except ValueError:  # pragma: no cover - clamp prevents
                    continue
                if lo <= periods <= hi:
                    break
        else:  # pragma: no cover - the guide lands in-window quickly
            raise ValueError("no schedule shape found for the tier")

        chain = Chain(principal, render=cents_txt,
                      milestone_spacing=(True if tier != "d50" else None))
        chain.set_invariant("balance cents mod 9", lambda v, k: v % 9)
        stop = n if variant == "balance_after_k" else None
        periods, interest_total, balance = _simulate(
            principal, rate, payment, extra_at=extra_at, extra=extra or 0,
            stop_at=stop, chain=chain)

        fields = {"principal": cents_txt(principal), "r": rate,
                  "payment": cents_txt(payment)}
        if variant == "balance_after_k":
            answer = cents_txt(balance)
            fields["n"] = n
        else:
            fields["cap"] = ((periods + 24) // 25) * 25
            if variant == "payoff_period":
                answer = str(periods)
            elif variant == "total_interest":
                answer = cents_txt(interest_total)
            else:
                answer = str(periods)
                fields["j"] = extra_at
                fields["extra"] = cents_txt(extra)
        problem = random.choice(PROMPTS[variant]).format(**fields)
        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"amortization_schedule_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
