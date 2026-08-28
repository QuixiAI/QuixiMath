"""Exact unstated-method work, fill, and drain stories.

Variants: ``together``, ``one_alone_unknown``, ``one_leaves_early``,
``fill_and_drain``, ``three_workers``, and ``partial_job``. Five renderings,
shared contexts, and four applied modifiers yield broad capacity. Op-codes:
``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``, ``RATE``, ``RATE_SUM``,
``MODEL_EQ``, ``A``, ``S``, ``M``, ``D``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, WORK_RATE_PAIRS, estimate_first,
                            frac_txt, select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("together", "one_alone_unknown", "one_leaves_early",
            "fill_and_drain", "three_workers", "partial_job")
FRAMES = (
    "At {place} ({record}), {facts_lc} {question}",
    "{question} The {record} note from {place} says: {facts}",
    "Job {record} at {place} — {facts} {question}",
    "{place_cap}, record {record}: {facts_lc} {question}",
    "Consider the {record} report from {place}: {facts} {question}",
)


def _render(facts, question, place):
    facts_cap = facts[:1].upper() + facts[1:]
    return random.choice(FRAMES).format(
        facts=facts_cap, facts_lc=facts[:1].lower() + facts[1:],
        question=question, place=place,
        place_cap=place[:1].upper() + place[1:],
        record=f"{random.choice('ABCDEFGH')}{random.randint(10, 99)}")


def _half_friendly(value):
    return value > 0 and value.denominator in (1, 2)


def _fill_drain_cases():
    cases = []
    for fill in range(2, 25):
        for drain in range(fill + 1, 49):
            time = 1 / (Fraction(1, fill) - Fraction(1, drain))
            if _half_friendly(time):
                cases.append((fill, drain, time))
    return tuple(cases)


FILL_DRAIN_CASES = _fill_drain_cases()


class WorkRateGenerator(ProblemGenerator):
    """Generate exact work-composition stories with standard modifiers."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS
    ANSWER_UNIT = "hours"

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _scene():
        ctx = random.choice(tuple(CONTEXTS.values()))
        device, verb, job = ctx.fragment("work")
        return ctx.setting(), device, verb, job

    @staticmethod
    def _case(variant):
        place, device, verb, job = WorkRateGenerator._scene()
        first, second, third = f"{device} A", f"{device} B", f"{device} C"
        if variant in ("together", "one_alone_unknown"):
            a, b = random.choice(WORK_RATE_PAIRS)
            total_rate = Fraction(1, a) + Fraction(1, b)
            together = 1 / total_rate
            if variant == "together":
                facts = (f"{first} alone can {verb} one {job} in {a} hours. "
                         f"{second} alone can {verb} one {job} in {b} hours.")
                question = "How many hours do they need when both run at once?"
                model = f"1/{a} + 1/{b} = 1/t"
                answer_value = together
                answer = unit(together, "hour")
                steps = [step("RATE", first, f"1/{a} job per hour"),
                         step("RATE", second, f"1/{b} job per hour"),
                         step("A", f"1/{a}", f"1/{b}", frac_txt(total_rate)),
                         step("RATE_SUM", f"1/{a} + 1/{b}", frac_txt(total_rate)),
                         step("MODEL_EQ", f"({frac_txt(total_rate)})*t=1",
                              f"one {job}"),
                         step("D", 1, frac_txt(total_rate), frac_txt(together)),
                         step("CHECK", "work completed",
                              f"{frac_txt(together/a)} + {frac_txt(together/b)}", 1)]
                used = [f"{a} hours", f"{b} hours"]
            else:
                facts = (f"{first} alone can {verb} one {job} in {a} hours. "
                         f"Working with {second}, the same job takes "
                         f"{frac_txt(together)} hours.")
                question = f"How many hours would {second} need alone?"
                model = f"1/{a} + 1/b = 1/{frac_txt(together)}"
                answer_value = Fraction(b)
                answer = unit(b, "hour")
                unknown_rate = Fraction(1, together) - Fraction(1, a)
                steps = [step("RATE", "together", f"1/{frac_txt(together)} job per hour"),
                         step("RATE", first, f"1/{a} job per hour"),
                         step("S", frac_txt(1 / together), f"1/{a}",
                              frac_txt(unknown_rate)),
                         step("RATE", second, f"{frac_txt(unknown_rate)} job per hour"),
                         step("D", 1, frac_txt(unknown_rate), b),
                         step("CHECK", "combined time", frac_txt(together))]
                used = [f"{a} hours alone", f"{frac_txt(together)} hours together"]
            return place, facts, question, steps, answer, answer_value, model, used

        if variant == "one_leaves_early":
            while True:
                a, b = random.choice(WORK_RATE_PAIRS)
                rate_sum = Fraction(1, a) + Fraction(1, b)
                lead = random.randint(1, max(1, int(1 / rate_sum) - 1))
                completed_together = lead * rate_sum
                remaining = 1 - completed_together
                alone_after = remaining * a
                total_time = lead + alone_after
                if remaining > 0 and _half_friendly(total_time):
                    break
            facts = (f"{first} alone can {verb} one {job} in {a} hours, and "
                     f"{second} alone needs {b} hours. They start together, "
                     f"but {second} leaves after {lead} hours.")
            question = f"How many hours after the start is the {job} finished?"
            model = f"(1/{a} + 1/{b})*{lead} + (t-{lead})/{a} = 1"
            steps = [step("RATE", first, f"1/{a} job per hour"),
                     step("RATE", second, f"1/{b} job per hour"),
                     step("A", f"1/{a}", f"1/{b}", frac_txt(rate_sum)),
                     step("M", lead, frac_txt(rate_sum),
                          frac_txt(completed_together)),
                     step("S", 1, frac_txt(completed_together),
                          frac_txt(remaining)),
                     step("D", frac_txt(remaining), f"1/{a}",
                          frac_txt(alone_after)),
                     step("A", lead, frac_txt(alone_after), frac_txt(total_time)),
                     step("CHECK", "work completed",
                          f"{frac_txt(completed_together)} + {frac_txt(remaining)}", 1)]
            answer = unit(total_time, "hour")
            used = [f"{a} hours", f"{b} hours", f"{lead} hours alone first"]
            return place, facts, question, steps, answer, total_time, model, used

        if variant == "fill_and_drain":
            fill, drain, time = random.choice(FILL_DRAIN_CASES)
            facts = (f"A pump fills one tank in {fill} hours. An open valve "
                     f"drains a full tank in {drain} hours.")
            question = "With both operating, how many hours does filling take?"
            net = Fraction(1, fill) - Fraction(1, drain)
            model = f"1/{fill} - 1/{drain} = 1/t"
            steps = [step("RATE", "pump", f"1/{fill} tank per hour"),
                     step("RATE", "valve", f"-1/{drain} tank per hour"),
                     step("S", f"1/{fill}", f"1/{drain}", frac_txt(net)),
                     step("RATE_SUM", f"1/{fill} - 1/{drain}", frac_txt(net)),
                     step("D", 1, frac_txt(net), frac_txt(time)),
                     step("CHECK", "net tank change",
                          f"({frac_txt(time)})/{fill} - ({frac_txt(time)})/{drain}",
                          1)]
            answer = unit(time, "hour")
            return place, facts, question, steps, answer, time, model, [f"fill {fill} hours", f"drain {drain} hours"]

        if variant == "three_workers":
            while True:
                times = random.sample(range(3, 25), 3)
                rate = sum((Fraction(1, value) for value in times), Fraction())
                together = 1 / rate
                if _half_friendly(together):
                    break
            a, b, c = times
            facts = (f"{first}, {second}, and {third} alone can each {verb} one "
                     f"{job} in {a}, {b}, and {c} hours respectively.")
            question = "How many hours do all three need together?"
            model = f"1/{a} + 1/{b} + 1/{c} = 1/t"
            steps = [step("RATE", first, f"1/{a} job per hour"),
                     step("RATE", second, f"1/{b} job per hour"),
                     step("RATE", third, f"1/{c} job per hour"),
                     step("A", f"1/{a}", f"1/{b}", frac_txt(Fraction(1, a)+Fraction(1, b))),
                     step("A", frac_txt(Fraction(1, a)+Fraction(1, b)),
                          f"1/{c}", frac_txt(rate)),
                     step("RATE_SUM", model.split(" = ")[0], frac_txt(rate)),
                     step("D", 1, frac_txt(rate), frac_txt(together)),
                     step("CHECK", "three shares sum", frac_txt(together*rate), 1)]
            answer = unit(together, "hour")
            return place, facts, question, steps, answer, together, model, [f"{a}, {b}, {c} hours"]

        denominator = random.randint(3, 10)
        numerator = random.randint(1, denominator - 1)
        elapsed = random.randint(1, 8) * numerator
        total_time = Fraction(elapsed * denominator, numerator)
        remaining = total_time - elapsed
        facts = (f"A machine completes {numerator}/{denominator} of an order "
                 f"in {elapsed} hours at a steady pace.")
        question = "How many hours does the whole order take, and how many remain?"
        model = f"({numerator}/{denominator})/{elapsed} = 1/t"
        rate = Fraction(numerator, denominator * elapsed)
        steps = [step("RATE", "machine", f"({numerator}/{denominator})/{elapsed}",
                      frac_txt(rate)),
                 step("D", 1, frac_txt(rate), frac_txt(total_time)),
                 step("S", frac_txt(total_time), elapsed, frac_txt(remaining)),
                 step("CHECK", "completed fraction",
                      frac_txt(Fraction(elapsed, total_time)),
                      f"{numerator}/{denominator}")]
        answer = f"{unit(total_time, 'hour')} total; {unit(remaining, 'hour')} remaining"
        return place, facts, question, steps, answer, total_time, model, [f"{numerator}/{denominator} in {elapsed} hours"]

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        place, facts, question, steps, answer, value, model, used = self._case(variant)
        problem = _render(facts, question, place)
        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(41, 100)
                                   if number not in occupied])
            problem = f"A storage shelf holds {extra} labels. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} shelf labels"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], value,
                                   "round the completion times")[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "completion facts"))
            answer = f"{model}; t = {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(),
                "operation": f"applied_work_rate_{variant}_{modifier}",
                "problem": problem, "steps": steps, "final_answer": answer}
