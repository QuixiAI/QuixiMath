"""Term-by-term partial sums with bounded running state (depth strand).

Strand R of ``plans/depth_plan.md``. Families are chosen so the running
sum stays small forever: arithmetic series (integers, Gauss closed
form), and the telescoping series sum of 1/(k(k+1)), whose running sum
from k = s always reduces to the two-small-integer fraction
1/s - 1/(s+k). Every accumulation is one chained ``A`` step; a final
``CHECK`` re-derives the total from the closed form.

Variants:

- ``arithmetic``: N stated terms of a + kd; answer the partial sum.
- ``telescoping``: N stated terms of 1/(k(k+1)) from k = s; answer the
  exact fraction.
- ``first_exceed``: the smallest N with the arithmetic partial sum
  above a stated bound (crossing screened into the tier window).

Op-codes: ``A`` (established, chained), ``CHECK`` (established),
``MILESTONE`` at ``d100``+, ``Z``.
"""
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from depth_common import (Chain, TIER_FLOORS, pick_tier, tier_difficulty,
                          tier_target)

DEPTH = True

PROMPTS = {
    "arithmetic": (
        "Accumulate {n} terms of the sequence {a}, {a_plus_d}, "
        "{a_plus_2d}, ... (each term {d} more than the last), adding one "
        "term at a time. What is the total?",
        "Add up the first {n} terms of the arithmetic sequence starting "
        "at {a} with common difference {d}, one term at a time. Report "
        "the sum.",
        "Sum {n} terms of the sequence that begins {a}, {a_plus_d}, "
        "{a_plus_2d}, ..., term by term. Give the running total's final "
        "value.",
        "Work through {n} terms of the arithmetic sequence (first term "
        "{a}, difference {d}), keeping a running sum. State the total.",
    ),
    "telescoping": (
        "Accumulate {n} terms of 1/(k(k+1)) starting at k = {s}, adding "
        "one term at a time and reducing the running sum. What exact "
        "fraction results?",
        "Add up {n} terms of the series 1/(k(k+1)) from k = {s}, term by "
        "term. Report the exact total.",
        "Sum {n} terms of 1/(k(k+1)) beginning at k = {s}, keeping the "
        "running sum reduced. Give the exact fraction.",
        "Work through {n} terms of 1/(k(k+1)) from k = {s} with a "
        "running total. State the exact sum.",
    ),
    "first_exceed": (
        "Keep adding terms of the sequence {a}, {a_plus_d}, {a_plus_2d}, "
        "... (difference {d}) until the running sum first exceeds "
        "{bound} (at most {cap} terms). How many terms does that take?",
        "Accumulate the arithmetic sequence starting at {a} with "
        "difference {d} until the total passes {bound} (at most {cap} "
        "terms). Report the term count.",
        "Sum terms of {a}, {a_plus_d}, {a_plus_2d}, ... one at a time "
        "until the running total is above {bound} (at most {cap} "
        "terms). How many terms are needed?",
        "Adding term by term, when does the arithmetic series (first "
        "term {a}, difference {d}) first exceed {bound}? Use at most "
        "{cap} terms and give the count.",
    ),
}


def _frac_txt(fr):
    return str(fr.numerator) if fr.denominator == 1 else str(fr)


class PartialSumMarathonGenerator(ProblemGenerator):
    """Tier-length running sums with closed-form checks (depth strand)."""

    VARIANTS = ("arithmetic", "telescoping", "first_exceed")
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
        milestones = True if tier != "d50" else None

        if variant == "telescoping":
            s = random.randint(1, 200)
            chain = Chain(Fraction(0), render=_frac_txt,
                          milestone_spacing=milestones)
            chain.set_invariant(
                "numerator + denominator mod 9",
                lambda v, k: (v.numerator + v.denominator) % 9)
            for k in range(s, s + n):
                term = Fraction(1, k * (k + 1))
                chain.apply("A", f"1/({k}*{k + 1}) = {term}",
                            chain.value + term)
            total = chain.value
            closed = Fraction(1, s) - Fraction(1, s + n)
            chain.steps.append(step(
                "CHECK", "telescoped closed form",
                f"1/{s} - 1/{s + n} = {_frac_txt(closed)}",
                f"accumulated = {_frac_txt(total)}"))
            answer = _frac_txt(total)
            problem = random.choice(PROMPTS[variant]).format(n=n, s=s)
        else:
            a = random.randint(1, 40)
            d = random.randint(1, 12)
            if variant == "first_exceed":
                # place the crossing exactly at the drawn n: any bound in
                # [S_{n-1}, S_n - 1] is first exceeded by S_n
                s_n = n * a + d * (n * (n - 1)) // 2
                s_prev = s_n - (a + (n - 1) * d)
                bound = random.randint(s_prev, s_n - 1)
                count = n
            terms = n
            chain = Chain(0, milestone_spacing=milestones)
            chain.set_invariant("running sum mod 9", lambda v, k: v % 9)
            for k in range(terms):
                term = a + k * d
                chain.apply("A", str(term), chain.value + term)
            total = chain.value
            closed = terms * (2 * a + (terms - 1) * d) // 2
            chain.steps.append(step(
                "CHECK", "closed form n(2a + (n-1)d)/2",
                f"{terms}*(2*{a} + {terms - 1}*{d})/2 = {closed}",
                f"accumulated = {total}"))
            fields = {"n": n, "a": a, "d": d, "a_plus_d": a + d,
                      "a_plus_2d": a + 2 * d}
            if variant == "first_exceed":
                answer = str(count)
                fields["bound"] = bound
                fields["cap"] = ((n + 24) // 25) * 25
            else:
                answer = str(total)
            problem = random.choice(PROMPTS[variant]).format(**fields)

        steps = chain.steps + [step("Z", answer)]
        return dict(
            problem_id=jid(),
            operation=f"partial_sum_marathon_{variant}_{tier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
            difficulty=tier_difficulty(self.BASE_DIFFICULTY, tier),
        )
