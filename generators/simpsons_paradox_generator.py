"""Subgroup rates that reverse when pooled, built backward from clean counts.

Variants: ``compute_and_state_reversal``, ``which_is_better_overall``,
``which_is_better_in_each_group``, ``weights_explain``,
``no_reversal_control``. Four contexts (hospitals, admissions, batting,
sales) and all four applied modifiers are supported. Every subgroup and
pooled rate is an exact percent by construction (counts are multiples of the
group size's 2,5-smooth remainder). Op-codes: ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``, ``SUBGROUP_RATE``,
``POOLED_RATE``, ``WEIGHT``, ``REVERSAL``, ``CMP``, ``CHECK``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, banded_count, dec, estimate_first,
                            lower_count, select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("compute_and_state_reversal", "which_is_better_overall",
            "which_is_better_in_each_group", "weights_explain",
            "no_reversal_control")
FRAMES = (
    "At {place}, {name} reviews the following report. {facts} {question}",
    "{question} A report reviewed by {name} at {place} states: {facts}",
    "For {name}'s review at {place}: {facts} {question}",
    "A bulletin from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the figures {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))

#: (small, large) case-count splits that sum to 100, so every pooled rate is
#: an exact whole percent.
SIZE_PAIRS = ((10, 90), (20, 80), (25, 75), (30, 70), (40, 60))

#: Subgroup rates are drawn from these two disjoint bands (as a fraction of
#: the subgroup size) so "subgroup 1" always outperforms "subgroup 2" for
#: both entities — the realistic condition that makes the pooled reversal
#: possible when the group sizes are swapped between entities.
HIGH_BAND = (0.55, 0.95)
LOW_BAND = (0.05, 0.45)

SP_CONTEXTS = (
    dict(label_a="Hospital A", label_b="Hospital B", entity="hospital",
        rate_noun="recovery", subgroup1="easy cases", subgroup2="hard cases",
        short1="easy", short2="hard", metric="recovered"),
    dict(label_a="University A", label_b="University B", entity="university",
        rate_noun="admission", subgroup1="in-state applicants",
        subgroup2="out-of-state applicants", short1="in-state",
        short2="out-of-state", metric="were admitted"),
    dict(label_a="Player A", label_b="Player B", entity="player",
        rate_noun="batting", subgroup1="day at-bats", subgroup2="night at-bats",
        short1="day", short2="night", metric="were hits"),
    dict(label_a="Rep A", label_b="Rep B", entity="sales rep",
        rate_noun="closing", subgroup1="new-client pitches",
        subgroup2="repeat-client pitches", short1="new-client",
        short2="repeat-client", metric="closed"),
)


def _pct(fr):
    return dec(fr * 100)


def _draw_reversal(small, large):
    """Counts where entity A wins subgroup 1 and subgroup 2, but entity B
    wins pooled, because A's cases skew to the low-rate subgroup and B's
    skew to the high-rate one."""
    for _ in range(2000):
        a1, a2 = banded_count(small, *HIGH_BAND), banded_count(large, *LOW_BAND)
        b1, b2 = banded_count(large, *HIGH_BAND), banded_count(small, *LOW_BAND)
        rate_a1, rate_a2 = Fraction(a1, small), Fraction(a2, large)
        rate_b1, rate_b2 = Fraction(b1, large), Fraction(b2, small)
        if rate_a1 <= rate_b1 or rate_a2 <= rate_b2:
            continue
        pooled_a, pooled_b = Fraction(a1 + a2, 100), Fraction(b1 + b2, 100)
        if pooled_b > pooled_a:
            return dict(a1=a1, a2=a2, b1=b1, b2=b2, small=small, large=large,
                       rate_a1=rate_a1, rate_a2=rate_a2, rate_b1=rate_b1,
                       rate_b2=rate_b2, pooled_a=pooled_a, pooled_b=pooled_b)
    raise AssertionError(f"no reversal found for sizes {small}, {large}")


def _draw_control(size1, size2):
    """Counts where both entities split cases the same way between the two
    subgroups, so A winning both subgroups forces A to win pooled too — no
    reversal is possible."""
    a1 = banded_count(size1, *HIGH_BAND)
    b1 = lower_count(size1, a1)
    a2 = banded_count(size2, *HIGH_BAND)
    b2 = lower_count(size2, a2)
    rate_a1, rate_b1 = Fraction(a1, size1), Fraction(b1, size1)
    rate_a2, rate_b2 = Fraction(a2, size2), Fraction(b2, size2)
    pooled_a = Fraction(a1 + a2, size1 + size2)
    pooled_b = Fraction(b1 + b2, size1 + size2)
    return dict(a1=a1, a2=a2, b1=b1, b2=b2, small=size1, large=size2,
               rate_a1=rate_a1, rate_a2=rate_a2, rate_b1=rate_b1,
               rate_b2=rate_b2, pooled_a=pooled_a, pooled_b=pooled_b)


def _facts(ctx, case, swapped_sizes=False):
    """The two-entity report. ``swapped_sizes`` is True for the paradox
    variants (A's subgroup sizes are (small, large); B's are (large,
    small)); False for the control (both use (small, large))."""
    small, large = case["small"], case["large"]
    b_size1, b_size2 = (large, small) if swapped_sizes else (small, large)
    a = (f"{ctx['label_a']}: {case['a1']} of {small} {ctx['subgroup1']} "
         f"{ctx['metric']}, {case['a2']} of {large} {ctx['subgroup2']} {ctx['metric']}.")
    b = (f"{ctx['label_b']}: {case['b1']} of {b_size1} {ctx['subgroup1']} "
         f"{ctx['metric']}, {case['b2']} of {b_size2} {ctx['subgroup2']} {ctx['metric']}.")
    order = [a, b]
    random.shuffle(order)
    return " ".join(order)


class SimpsonsParadoxGenerator(ProblemGenerator):
    """Generate five exact subgroup-vs-pooled-rate models without naming
    the phenomenon."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _rate_steps(ctx, case, swapped=True):
        """``swapped`` matches :func:`_facts`: True when B's subgroup sizes
        are (large, small) — the paradox variants; False when B uses the
        same (small, large) split as A — the control."""
        small, large = case["small"], case["large"]
        b1_denom, b2_denom = (large, small) if swapped else (small, large)
        return [
            step("SUBGROUP_RATE", ctx["short1"], "A", f"{case['a1']}/{small} = {_pct(case['rate_a1'])}%"),
            step("SUBGROUP_RATE", ctx["short1"], "B", f"{case['b1']}/{b1_denom} = {_pct(case['rate_b1'])}%"),
            step("SUBGROUP_RATE", ctx["short2"], "A", f"{case['a2']}/{large} = {_pct(case['rate_a2'])}%"),
            step("SUBGROUP_RATE", ctx["short2"], "B", f"{case['b2']}/{b2_denom} = {_pct(case['rate_b2'])}%"),
        ]

    @classmethod
    def _compute_and_state_reversal(cls):
        small, large = random.choice(SIZE_PAIRS)
        ctx, case = random.choice(SP_CONTEXTS), _draw_reversal(small, large)
        facts = _facts(ctx, case, swapped_sizes=True)
        question = f"Compare the {ctx['rate_noun']} rates within {ctx['subgroup1']} and {ctx['subgroup2']}, and overall."
        model = "pooled = (subgroup 1 count + subgroup 2 count)/100"
        total_a, total_b = case["a1"] + case["a2"], case["b1"] + case["b2"]
        steps = cls._rate_steps(ctx, case) + [
            step("POOLED_RATE", "A", f"{total_a}/100 = {_pct(case['pooled_a'])}%"),
            step("POOLED_RATE", "B", f"{total_b}/100 = {_pct(case['pooled_b'])}%"),
            step("REVERSAL", "A wins each group, B wins overall"),
            step("CHECK", f"A's cases are {large}% {ctx['short2']}; "
                 f"B's cases are {large}% {ctx['short1']}"),
        ]
        answer = (f"A better in both groups ({_pct(case['rate_a1'])}% > {_pct(case['rate_b1'])}%, "
                 f"{_pct(case['rate_a2'])}% > {_pct(case['rate_b2'])}%); "
                 f"B better overall ({_pct(case['pooled_b'])}% > {_pct(case['pooled_a'])}%)")
        used = [f"A: {case['a1']} of {small}, {case['a2']} of {large}",
                f"B: {case['b1']} of {large}, {case['b2']} of {small}"]
        return facts, question, steps, answer, case["pooled_b"], model, used, dec

    @classmethod
    def _which_is_better_overall(cls):
        small, large = random.choice(SIZE_PAIRS)
        ctx, case = random.choice(SP_CONTEXTS), _draw_reversal(small, large)
        facts = _facts(ctx, case, swapped_sizes=True)
        question = f"Which {ctx['entity']} has the better overall {ctx['rate_noun']} rate, and what are the two overall rates?"
        model = "pooled = (subgroup 1 count + subgroup 2 count)/100"
        total_a, total_b = case["a1"] + case["a2"], case["b1"] + case["b2"]
        steps = [step("POOLED_RATE", "A", f"{total_a}/100 = {_pct(case['pooled_a'])}%"),
                step("POOLED_RATE", "B", f"{total_b}/100 = {_pct(case['pooled_b'])}%"),
                step("CMP", _pct(case["pooled_b"]), _pct(case["pooled_a"]), ">")]
        answer = f"B; {_pct(case['pooled_b'])}% vs {_pct(case['pooled_a'])}%"
        used = [f"A: {case['a1']} of {small}, {case['a2']} of {large}",
                f"B: {case['b1']} of {large}, {case['b2']} of {small}"]
        return facts, question, steps, answer, case["pooled_b"], model, used, dec

    @classmethod
    def _which_is_better_in_each_group(cls):
        small, large = random.choice(SIZE_PAIRS)
        ctx, case = random.choice(SP_CONTEXTS), _draw_reversal(small, large)
        facts = _facts(ctx, case, swapped_sizes=True)
        question = f"Which {ctx['entity']} has the better rate in {ctx['subgroup1']}, and which has the better rate in {ctx['subgroup2']}?"
        model = "rate = count/subgroup size"
        steps = cls._rate_steps(ctx, case) + [
            step("CMP", _pct(case["rate_a1"]), _pct(case["rate_b1"]), ">"),
            step("CMP", _pct(case["rate_a2"]), _pct(case["rate_b2"]), ">"),
        ]
        answer = (f"{ctx['subgroup1']}: A ({_pct(case['rate_a1'])}% > {_pct(case['rate_b1'])}%); "
                 f"{ctx['subgroup2']}: A ({_pct(case['rate_a2'])}% > {_pct(case['rate_b2'])}%)")
        used = [f"A: {case['a1']} of {small}, {case['a2']} of {large}",
                f"B: {case['b1']} of {large}, {case['b2']} of {small}"]
        return facts, question, steps, answer, case["rate_a1"] * 100, model, used, dec

    @classmethod
    def _weights_explain(cls):
        small, large = random.choice(SIZE_PAIRS)
        ctx, case = random.choice(SP_CONTEXTS), _draw_reversal(small, large)
        facts = _facts(ctx, case, swapped_sizes=True)
        question = (f"{ctx['label_a']} has the better rate in both {ctx['subgroup1']} and "
                   f"{ctx['subgroup2']}, yet {ctx['label_b']} has the better overall rate. "
                   "What do the two group sizes show?")
        model = "composition = subgroup size/total"
        steps = [step("WEIGHT", "A", f"{large}% {ctx['short2']}"),
                step("WEIGHT", "B", f"{large}% {ctx['short1']}"),
                step("CHECK", f"A's cases are {large}% {ctx['short2']}; "
                     f"B's cases are {large}% {ctx['short1']}")]
        answer = f"A's cases are {large}% {ctx['short2']}; B's cases are {large}% {ctx['short1']}"
        used = [f"A: {case['a1']} of {small}, {case['a2']} of {large}",
                f"B: {case['b1']} of {large}, {case['b2']} of {small}"]
        return facts, question, steps, answer, Fraction(large), model, used, str

    @classmethod
    def _no_reversal_control(cls):
        size1, size2 = random.choice(SIZE_PAIRS)
        ctx, case = random.choice(SP_CONTEXTS), _draw_control(size1, size2)
        facts = _facts(ctx, case, swapped_sizes=False)
        question = f"Compare the {ctx['rate_noun']} rates within {ctx['subgroup1']} and {ctx['subgroup2']}, and overall."
        model = "pooled = (subgroup 1 count + subgroup 2 count)/total"
        total_a, total_b = case["a1"] + case["a2"], case["b1"] + case["b2"]
        total = size1 + size2
        steps = cls._rate_steps(ctx, case, swapped=False) + [
            step("POOLED_RATE", "A", f"{total_a}/{total} = {_pct(case['pooled_a'])}%"),
            step("POOLED_RATE", "B", f"{total_b}/{total} = {_pct(case['pooled_b'])}%"),
            step("REVERSAL", "no reversal; A wins each group and overall"),
        ]
        answer = (f"A better in both groups ({_pct(case['rate_a1'])}% > {_pct(case['rate_b1'])}%, "
                 f"{_pct(case['rate_a2'])}% > {_pct(case['rate_b2'])}%) and overall "
                 f"({_pct(case['pooled_a'])}% > {_pct(case['pooled_b'])}%); no reversal")
        used = [f"A: {case['a1']} of {size1}, {case['a2']} of {size2}",
                f"B: {case['b1']} of {size1}, {case['b2']} of {size2}"]
        return facts, question, steps, answer, case["pooled_a"], model, used, dec

    @classmethod
    def _case(cls, variant):
        return getattr(cls, f"_{variant}")()

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used, renderer = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(301, 601) if n not in occupied])
            problem = f"An unrelated memo lists {extra} filed reports. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} filed reports"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict which side's overall rate will be higher",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "pooled-rate relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_simpsons_paradox_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
