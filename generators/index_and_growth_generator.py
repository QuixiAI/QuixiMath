"""Index numbers, CAGR, inflation adjustment, and log-scale reading.

Variants: ``index_number``, ``percent_change_vs_points``,
``cagr_perfect_power``, ``real_vs_nominal_supplied_cpi``,
``log_scale_reading``, ``repeated_doubling``. Five context frames and all
four applied modifiers are supported. Every ratio is built backward from a
2,5-smooth denominator, and CAGR problems are constructed from an exact root
rather than computed — the growth rate is known before the end value is.
Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``MODEL_EQ``,
``INDEX_NUMBER``, ``DEC_TO_PERCENT``, ``PP_CHANGE``, ``PCT_CHANGE``, ``CAGR``,
``REAL_RATE``, ``LOG_TICKS``, ``D``, ``E``, ``CHECK``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import CONTEXTS, NAMES, dec, estimate_first, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("index_number", "percent_change_vs_points", "cagr_perfect_power",
            "real_vs_nominal_supplied_cpi", "log_scale_reading",
            "repeated_doubling")
FRAMES = (
    "At {place}, {name} reviews the following figures. {facts} {question}",
    "{question} A report reviewed by {name} at {place} states: {facts}",
    "For {name}'s summary at {place}: {facts} {question}",
    "A bulletin from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the figures {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)

#: Index values whose only prime factors are 2 and 5, so dividing any later
#: integer index by one of these always terminates.
SMOOTH_INDEX_VALUES = (50, 64, 80, 100, 125, 160, 200, 250, 320, 400)

#: (ratio, years) pairs built from a small-denominator ratio so
#: ``ratio ** years`` keeps a 2,5-smooth denominator.
CAGR_RATIOS = (
    (Fraction(11, 10), (2, 3, 4)), (Fraction(21, 20), (2, 3)),
    (Fraction(6, 5), (2, 3)), (Fraction(5, 4), (2, 3, 4)),
    (Fraction(3, 2), (2, 3)), (Fraction(9, 5), (2, 3)),
    (Fraction(2, 1), (2, 3, 4)), (Fraction(13, 10), (2, 3)),
)

#: Nominal-vs-real: inflation percents whose ``100 + inflation`` stays
#: 2,5-smooth, so the exact real rate always terminates.
INFLATION_RATES = (0, 25, 150, 300, 400)

GROWTH_SUBJECTS = ("a population", "a customer base", "a subscriber count",
                   "an account balance", "a colony's size")

DOUBLING_PERIODS = (5, 10, 20, 25)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class IndexAndGrowthGenerator(ProblemGenerator):
    """Generate six exact index/growth models without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _index_number():
        i0 = 100
        i1 = random.choice(SMOOTH_INDEX_VALUES)
        i2 = max(1, i1 + random.randint(-i1 // 2, i1))
        pct1 = Fraction(i1 - i0, i0) * 100
        pct2 = Fraction(i2 - i1, i1) * 100
        facts = f"A price index changes from {i0} to {i1}, then to {i2}."
        question = "What is the percent change in each step?"
        model = "step percent = (new − old)/old"
        steps = [step("INDEX_NUMBER", f"{i1}/{i0}", dec(Fraction(i1, i0))),
                step("DEC_TO_PERCENT", dec(Fraction(i1 - i0, i0)), f"{dec(pct1)}%"),
                step("INDEX_NUMBER", f"{i2}/{i1}", dec(Fraction(i2, i1))),
                step("DEC_TO_PERCENT", dec(Fraction(i2 - i1, i1)), f"{dec(pct2)}%")]
        answer = f"{dec(pct1)}%; {dec(pct2)}%"
        used = [f"index {i0}, {i1}, {i2}"]
        return facts, question, steps, answer, pct2, model, used, dec

    @staticmethod
    def _percent_change_vs_points():
        p1 = random.choice((4, 5, 8, 10, 16, 20, 25, 40, 50))
        delta = random.choice((1, 2, 3, 4, 5, 6, 8, 10))
        sign = random.choice((1, -1))
        p2 = p1 + sign * delta
        pct_change = dec(Fraction(sign * delta, p1) * 100)
        facts = f"An inflation rate goes from {p1}% to {p2}% year over year."
        question = "What is the change in percentage points, and what is the percent change in the rate itself?"
        model = "points = p2 − p1; percent = (p2 − p1)/p1"
        steps = [step("PP_CHANGE", f"{p2} − {p1}", f"{sign * delta} points"),
                step("PCT_CHANGE", f"({p2} − {p1})/{p1}", f"{pct_change}%")]
        answer = f"{sign * delta} percentage points; {pct_change}% percent change"
        used = [f"from {p1}%", f"to {p2}%"]
        return facts, question, steps, answer, Fraction(delta), model, used, str

    @staticmethod
    def _cagr_perfect_power():
        ratio, years_bank = random.choice(CAGR_RATIOS)
        t = random.choice(years_bank)
        factor = ratio ** t
        v0 = factor.denominator * random.randint(1, 5)
        v1 = int(v0 * factor)
        subject = random.choice(GROWTH_SUBJECTS)
        facts = f"{subject.capitalize()} grows from {v0} to {v1} over {t} years."
        question = "What is the annual growth rate?"
        model = "rate = (end/start)^(1/years) − 1"
        steps = [step("CAGR", f"({v1}/{v0})^(1/{t})", dec(ratio))]
        answer = f"{dec((ratio - 1) * 100)}% per year"
        used = [f"start {v0}", f"end {v1}", f"years {t}"]
        return facts, question, steps, answer, (ratio - 1) * 100, model, used, dec

    @staticmethod
    def _real_vs_nominal_supplied_cpi():
        inflation = random.choice(INFLATION_RATES)
        nominal = random.randint(-20, 80)
        real_pct = Fraction(100 * (100 + nominal), 100 + inflation) - 100
        facts = (f"A wage rises {nominal}% nominally while inflation (CPI) "
                 f"for the year is {inflation}%.")
        question = "What is the exact real (inflation-adjusted) percent change?"
        model = "real = 100(100 + nominal)/(100 + inflation) − 100"
        steps = [step("REAL_RATE", f"100·(100 + {nominal})/(100 + {inflation}) − 100",
                     f"{dec(real_pct)}%")]
        answer = f"{dec(real_pct)}%"
        used = [f"nominal {nominal}%", f"inflation {inflation}%"]
        return facts, question, steps, answer, real_pct, model, used, dec

    @staticmethod
    def _log_scale_reading():
        n = random.randint(1, 4)
        rises = random.choice((True, False))
        multiplier = 10 ** n
        direction, arrow = ("rises", f"×{multiplier}") if rises else ("falls", f"÷{multiplier}")
        tick = "major tick" if n == 1 else "major ticks"
        facts = f"A curve on a log-10 axis {direction} {n} {tick}."
        question = "By what factor did the underlying value change?"
        model = "factor = 10^(number of major ticks)"
        steps = [step("LOG_TICKS", n, arrow)]
        answer = arrow
        used = [f"{n} {tick}", direction]
        return facts, question, steps, answer, Fraction(multiplier), model, used, str

    @staticmethod
    def _repeated_doubling():
        period = random.choice(DOUBLING_PERIODS)
        k = random.randint(2, 6)
        years = period * k
        subject = random.choice(GROWTH_SUBJECTS)
        factor = 2 ** k
        facts = f"{subject.capitalize()} doubles every {period} years."
        question = f"Over {years} years, how many times does it double, and what is the total growth factor?"
        model = "doublings = years/period; factor = 2^doublings"
        steps = [step("D", years, period, k), step("E", 2, k, factor)]
        answer = f"{k} times; ×{factor}"
        used = [f"doubling period {period}", f"span {years} years"]
        return facts, question, steps, answer, Fraction(factor), model, used, str

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
            problem = f"An unrelated ledger lists {extra} filed reports. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} filed reports"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the reported change",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "index/growth relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_index_and_growth_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
