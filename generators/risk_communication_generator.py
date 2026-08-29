"""Relative vs. absolute risk, NNT, per-capita rates, and small-risk framing.

Variants: ``relative_vs_absolute``, ``percent_vs_percentage_points``, ``nnt``,
``per_capita_vs_raw``, ``rate_per_1000``, ``doubling_a_small_risk``. Five
context frames and all four applied modifiers are supported. Every rate is
built backward from integers so every percent is exact — either a clean
decimal or, for relative-risk fractions, a mixed number (``33 1/3%``).
Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``RISK``, ``DEC_TO_PERCENT``, ``PP_VS_PCT``, ``PP_CHANGE``, ``PCT_CHANGE``,
``NNT``, ``PER_1000``, ``CMP``, ``CHECK``, ``A``, ``S``, ``M``, ``D``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, dec, estimate_first, select_relevant_step, terminates
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("relative_vs_absolute", "percent_vs_percentage_points", "nnt",
            "per_capita_vs_raw", "rate_per_1000", "doubling_a_small_risk")
FRAMES = (
    "At {place}, {name} reviews a set of reported rates. {facts} {question}",
    "{question} A report reviewed by {name} at {place} states: {facts}",
    "For {name}'s summary at {place}: {facts} {question}",
    "A bulletin from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the figures {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)

#: Integers whose only prime factors are 2 and 5 — dividing by one of these
#: always yields a terminating decimal, whatever the numerator.
SMOOTH_K = (2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100)

MULTIPLIER_WORDS = {2: "doubles", 3: "triples", 4: "quadruples", 5: "increases fivefold"}


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


def frac_percent(fr):
    """Percent text for any positive ``Fraction``: a clean decimal when it
    terminates, else a mixed number (``Fraction(1, 3)`` -> ``'33 1/3%'``)."""
    pct_value = Fraction(fr) * 100
    whole, remainder = divmod(pct_value.numerator, pct_value.denominator)
    remainder = Fraction(remainder, pct_value.denominator)
    if remainder == 0:
        return f"{whole}%"
    if terminates(pct_value):
        return dec(pct_value) + "%"
    return f"{whole} {remainder.numerator}/{remainder.denominator}%"


class RiskCommunicationGenerator(ProblemGenerator):
    """Generate six exact risk-communication models without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _relative_vs_absolute():
        n = random.choice((100, 1000, 10000))
        a = random.randint(3, 30)
        b = random.randint(1, a - 1)
        rrr, arr_pp = Fraction(a - b, a), Fraction(a - b, n) * 100
        facts = (f"Without treatment the risk of a condition is {a} in {n}; "
                 f"with treatment it is {b} in {n}.")
        question = "State the relative risk reduction and the absolute risk reduction."
        model = "relative = (a − b)/a; absolute = (a − b)/n"
        steps = [step("RISK", "absolute", f"{a}/{n} − {b}/{n}", f"{a - b}/{n}"),
                 step("RISK", "relative", f"({a} − {b})/{a}", str(rrr)),
                 step("DEC_TO_PERCENT", str(rrr), frac_percent(rrr)),
                 step("PP_VS_PCT", f"{dec(arr_pp)} points", frac_percent(rrr))]
        answer = f"relative {frac_percent(rrr)}; absolute {dec(arr_pp)} percentage points"
        used = [f"baseline {a} in {n}", f"treatment {b} in {n}"]
        return facts, question, steps, answer, arr_pp, model, used, dec

    @staticmethod
    def _percent_vs_percentage_points():
        p1 = random.choice((4, 5, 8, 10, 16, 20, 25, 40, 50))
        delta = random.choice((1, 2, 3, 4, 5, 6, 8, 10))
        p2 = p1 + delta
        pct_change = dec(Fraction(delta, p1) * 100)
        facts = f"A reported rate rises from {p1}% to {p2}%."
        question = "State the change in percentage points and the percent change."
        model = "points = p2 − p1; percent = (p2 − p1)/p1"
        steps = [step("PP_CHANGE", f"{p2} − {p1}", f"{delta} points"),
                 step("PCT_CHANGE", f"({p2} − {p1})/{p1}", f"{pct_change}%"),
                 step("PP_VS_PCT", f"{delta} points", f"{pct_change}%")]
        answer = f"{delta} percentage points; {pct_change}% percent change"
        used = [f"from {p1}%", f"to {p2}%"]
        return facts, question, steps, answer, Fraction(delta), model, used, str

    @staticmethod
    def _nnt():
        k = random.choice((2, 4, 5, 10, 20, 25, 50, 100))
        arr_pct = Fraction(100, k)
        facts = (f"A treatment reduces absolute risk by {dec(arr_pct)}%.")
        question = ("How many patients must be treated to prevent one "
                    "additional bad outcome?")
        model = "NNT = 1/ARR"
        steps = [step("NNT", f"1/{dec(Fraction(arr_pct, 100))}", f"{k} people")]
        answer = f"{k} people"
        used = [f"absolute risk reduction {dec(arr_pct)}%"]
        return facts, question, steps, answer, Fraction(k), model, used, str

    @staticmethod
    def _per_capita_vs_raw():
        for _ in range(400):
            k1, k2 = random.sample(SMOOTH_K, 2)
            cases1, cases2 = random.randint(5, 90), random.randint(5, 150)
            if cases1 == cases2:
                continue
            rate1, rate2 = Fraction(cases1, k1), Fraction(cases2, k2)
            if rate1 == rate2:
                continue
            if (rate1 > rate2) != (cases1 > cases2):
                break
        else:
            raise AssertionError("no reversal found")
        pop1, pop2 = 1000 * k1, 1000 * k2
        higher = 1 if rate1 > rate2 else 2
        hi_rate, lo_rate = (rate1, rate2) if higher == 1 else (rate2, rate1)
        facts = (f"Place 1 recorded {cases1} cases among {pop1} people. "
                 f"Place 2 recorded {cases2} cases among {pop2} people.")
        question = "Which place has the higher case rate per 1000 people?"
        model = "rate = cases/(population/1000)"
        steps = [step("PER_1000", f"{cases1} × 1000/{pop1}", f"{dec(rate1)} per 1000"),
                 step("PER_1000", f"{cases2} × 1000/{pop2}", f"{dec(rate2)} per 1000"),
                 step("CMP", dec(rate1), dec(rate2), ">" if rate1 > rate2 else "<")]
        raw_note = ("despite fewer raw cases" if (cases1 if higher == 1 else cases2) <
                    (cases2 if higher == 1 else cases1) else "and more raw cases")
        answer = (f"place {higher} higher ({dec(hi_rate)} vs {dec(lo_rate)} "
                 f"per 1000) {raw_note}")
        used = [f"place 1: {cases1} in {pop1}", f"place 2: {cases2} in {pop2}"]
        return facts, question, steps, answer, hi_rate, model, used, dec

    @staticmethod
    def _rate_per_1000():
        k = random.choice(SMOOTH_K)
        pop = 1000 * k
        cases = random.randint(3, 20 * k)
        rate = Fraction(cases, k)
        facts = f"A community recorded {cases} cases among {pop} people."
        question = "What is the case rate per 1000 people?"
        model = "rate = cases × 1000/population"
        steps = [step("PER_1000", f"{cases} × 1000/{pop}", f"{dec(rate)} per 1000")]
        answer = f"{dec(rate)} per 1000"
        used = [f"cases {cases}", f"population {pop}"]
        return facts, question, steps, answer, rate, model, used, dec

    @staticmethod
    def _doubling_a_small_risk():
        n = random.choice((1000, 5000, 10000))
        a = random.randint(1, 9)
        k = random.choice((2, 3, 4, 5))
        new = a * k
        relative = (k - 1) * 100
        abs_pp = Fraction(new - a, n) * 100
        facts = (f"A rare condition's risk {MULTIPLIER_WORDS[k]} from {a} in "
                 f"{n} to {new} in {n}.")
        question = "State the relative risk change and the absolute risk change."
        model = "relative = (k − 1) × 100%; absolute = a(k − 1)/n × 100"
        steps = [step("RISK", "relative", f"({new} − {a})/{a}", f"+{relative}%"),
                 step("RISK", "absolute", f"({new} − {a})/{n}", f"+{dec(abs_pp)} points"),
                 step("PP_VS_PCT", f"{dec(abs_pp)} points", f"+{relative}%")]
        answer = f"relative +{relative}%; absolute +{dec(abs_pp)} percentage points"
        used = [f"baseline {a} in {n}", f"multiplier {k}"]
        return facts, question, steps, answer, abs_pp, model, used, dec

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
            extra = random.choice([n for n in range(601, 901) if n not in occupied])
            problem = f"An unrelated notice lists {extra} archived forms. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} archived forms"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the reported rate",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "risk-communication relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_risk_communication_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
