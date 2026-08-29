"""Six statistical-literacy traps, computed exactly from clean constructions.

Variants: ``regression_to_mean``, ``averaging_rates_wrong``,
``visual_ratio_truncated_axis``, ``sampling_error_scale``, ``percent_of_what``,
``cherry_picked_interval``. Five context frames and all four applied
modifiers are supported. Every quantity is built backward so its rendering
is exact — correlations are tenths, group sizes are 2,5-smooth, sample sizes
are perfect squares. Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``MODEL_EQ``, ``REGRESS_MEAN``, ``AVG``, ``POOLED_RATE``,
``VISUAL_RATIO``, ``TRUE_RATIO``, ``MOE``, ``SHRINK_FACTOR``, ``PCT_MORE``,
``PCT_LESS``, ``WINDOW_CHANGE``, ``FULL_CHANGE``, ``CHECK``, ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, banded_count, dec, estimate_first,
                            exact, select_relevant_step)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("regression_to_mean", "averaging_rates_wrong",
            "visual_ratio_truncated_axis", "sampling_error_scale",
            "percent_of_what", "cherry_picked_interval")
FRAMES = (
    "At {place}, {name} reviews the following figures. {facts} {question}",
    "{question} A report reviewed by {name} at {place} states: {facts}",
    "For {name}'s summary at {place}: {facts} {question}",
    "A bulletin from {place}, checked by {name}, reads: {facts} {question}",
    "Consider the figures {name} received from {place}. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "shop", "classroom", "workshop")
               for setting in CONTEXTS[key].settings)

#: (small, large) group-size splits that sum to 100, so every pooled rate is
#: an exact whole percent.
SIZE_PAIRS = ((10, 90), (20, 80), (25, 75), (30, 70), (40, 60))

REGRESSION_CONTEXTS = (
    dict(group="Class", metric="retest", subject="student"),
    dict(group="Team", metric="second-round", subject="golfer"),
    dict(group="Group", metric="follow-up", subject="participant"),
    dict(group="League", metric="next-season", subject="player"),
)

RATE_ITEMS = ("items", "components", "applications", "trials", "submissions")

#: Sample-size base ``m`` values (giving perfect square ``m**2``) and growth
#: multipliers, both 2,5-smooth, so every ``1/(m·k)`` margin renders exactly.
MARGIN_BASES = (4, 5, 8, 10, 16, 20, 25, 40, 50)
MARGIN_MULTIPLIERS = (2, 4, 5)

#: "p% more" values whose base-100 sum stays 2,5-smooth, so the reverse
#: percent always renders as a clean decimal.
BASE_CONFUSION_RATES = (25, 100, 150, 400)


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class StatisticalLiteracyGenerator(ProblemGenerator):
    """Generate six exact statistical-literacy traps without naming a method."""

    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _regression_to_mean():
        ctx = random.choice(REGRESSION_CONTEXTS)
        mu = random.randint(50, 90)
        r = Fraction(random.randint(1, 9), 10)
        x = random.choice([v for v in range(0, 101) if v != mu])
        predicted = mu + r * (x - mu)
        facts = (f"{ctx['group']} mean is {mu} and the {ctx['metric']} "
                 f"correlation is {dec(r)}. A {ctx['subject']} scored {x}.")
        question = f"What {ctx['metric']} score should be expected?"
        model = "predicted = mean + r × (score − mean)"
        steps = [step("REGRESS_MEAN", f"{mu} + {dec(r)}·({x} − {mu})", dec(predicted))]
        answer = dec(predicted)
        used = [f"mean {mu}", f"correlation {dec(r)}", f"score {x}"]
        return facts, question, steps, answer, predicted, model, used, dec

    @staticmethod
    def _averaging_rates_wrong():
        n1, n2 = random.choice(SIZE_PAIRS)
        for _ in range(300):
            c1, c2 = banded_count(n1, 0.05, 0.95), banded_count(n2, 0.05, 0.95)
            rate1, rate2 = Fraction(c1, n1), Fraction(c2, n2)
            if rate1 != rate2:
                break
        else:
            raise AssertionError("no distinct rates found")
        naive = (rate1 + rate2) / 2 * 100
        pooled = Fraction(c1 + c2, n1 + n2) * 100
        item = random.choice(RATE_ITEMS)
        pct1, pct2 = dec(rate1 * 100), dec(rate2 * 100)
        facts = (f"{pct1}% of {n1} {item} passed in one group, and {pct2}% "
                 f"of {n2} {item} passed in another group.")
        question = ("What is the combined pass percent for both groups, and "
                    "how does it compare to simply averaging the two percents?")
        model = "pooled = (count1 + count2)/(n1 + n2); naive = (rate1 + rate2)/2"
        steps = [step("AVG", f"({pct1}% + {pct2}%)/2", f"{dec(naive)}%"),
                step("POOLED_RATE", f"{c1 + c2}/{n1 + n2}", f"{dec(pooled)}%")]
        answer = f"{dec(pooled)}%; averaging the two percents gives {dec(naive)}%, which is wrong"
        used = [f"group 1: {pct1}% of {n1}", f"group 2: {pct2}% of {n2}"]
        return facts, question, steps, answer, pooled, model, used, dec

    @staticmethod
    def _visual_ratio_truncated_axis():
        base = random.randint(50, 90)
        h1 = random.randint(base + 2, base + 20)
        h2 = random.randint(h1 + 2, h1 + 20)
        d1, d2 = h1 - base, h2 - base
        visual, true = Fraction(d2, d1), Fraction(h2, h1)
        visual_txt, true_txt = exact(visual), exact(true)
        facts = (f"A bar chart's vertical axis starts at {base} instead of 0. "
                 f"One bar reaches {h1}, and another reaches {h2}.")
        question = "What ratio does the chart visually suggest between the two bars, and what is the true ratio?"
        model = "visual = (bar2 − baseline)/(bar1 − baseline); true = bar2/bar1"
        steps = [step("VISUAL_RATIO", f"{d2} : {d1}", visual_txt),
                step("TRUE_RATIO", f"{h2} : {h1}", true_txt)]
        answer = f"visual {visual_txt}; true {true_txt}"
        used = [f"baseline {base}", f"bars {h1}, {h2}"]
        return facts, question, steps, answer, true, model, used, str

    @staticmethod
    def _sampling_error_scale():
        m = random.choice(MARGIN_BASES)
        k = random.choice(MARGIN_MULTIPLIERS)
        n1, n2 = m * m, (m * k) * (m * k)
        margin1, margin2 = Fraction(1, m), Fraction(1, m * k)
        facts = (f"Using the approximation that margin of error is about "
                 f"1/√n, a poll of n = {n1} people has a margin of error of "
                 f"about {dec(margin1 * 100)}%.")
        question = f"If the poll grows to n = {n2} people, by what factor does the margin of error shrink, and what is the new margin of error?"
        model = "margin = 1/√n"
        steps = [step("MOE", f"1/√{n2}", f"{dec(margin2 * 100)}%"),
                step("SHRINK_FACTOR", f"{dec(margin1 * 100)}%/{dec(margin2 * 100)}%", str(k))]
        answer = f"factor of {k}; margin goes from {dec(margin1 * 100)}% to {dec(margin2 * 100)}%"
        used = [f"n1 {n1}", f"n2 {n2}"]
        return facts, question, steps, answer, margin2 * 100, model, used, dec

    @staticmethod
    def _percent_of_what():
        p = random.choice(BASE_CONFUSION_RATES)
        # Choose B as a multiple that keeps A = B*(100+p)/100 an integer.
        factor = Fraction(100 + p, 100)
        stride = factor.denominator
        B = stride * random.randint(2, 40)
        A = int(B * factor)
        reverse_pct = Fraction(100 * p, 100 + p)
        facts = f"Quantity A is {p}% more than quantity B, and B is {B}."
        question = "By what percent is B less than A?"
        model = "reverse = 100p/(100 + p)"
        steps = [step("PCT_MORE", f"{B} × {dec(factor)}", A),
                step("PCT_LESS", f"({A} − {B})/{A}", f"{dec(reverse_pct)}%")]
        answer = f"{dec(reverse_pct)}%; not {p}% (the base changed from {B} to {A})"
        used = [f"A is {p}% more than B", f"B = {B}"]
        return facts, question, steps, answer, reverse_pct, model, used, dec

    @staticmethod
    def _cherry_picked_interval():
        scale1, scale2 = random.randint(1, 5), random.randint(1, 9)
        p_full = random.choice((10, 15, 20, 25, 30))
        p_window = random.choice((50, 60, 75, 80, 100))
        v1 = 100 * scale1
        v4 = v1 + scale1 * p_full
        v2 = 100 * scale2
        v3 = v2 + scale2 * p_window
        facts = (f"A metric measured {v1} in year 1, {v2} in year 2, {v3} "
                 f"in year 3, and {v4} in year 4. A report highlights only "
                 "the change from year 2 to year 3.")
        question = "What is the percent change from year 2 to year 3, and what is the percent change over the full period from year 1 to year 4?"
        model = "window = (v3 − v2)/v2; full = (v4 − v1)/v1"
        steps = [step("WINDOW_CHANGE", f"({v3} − {v2})/{v2}", f"{p_window}%"),
                step("FULL_CHANGE", f"({v4} − {v1})/{v1}", f"{p_full}%")]
        answer = f"{p_window}%; {p_full}% (window: year 2 to 3, full: year 1 to 4)"
        used = [f"year 1: {v1}", f"year 2: {v2}", f"year 3: {v3}", f"year 4: {v4}"]
        return facts, question, steps, answer, Fraction(p_full), model, used, dec

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
            extra = random.choice([n for n in range(701, 1001) if n not in occupied])
            problem = f"An unrelated log lists {extra} archived entries. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} archived entries"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "predict the scale of the reported figure",
                                   render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "statistical-literacy relationship"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_statistical_literacy_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
