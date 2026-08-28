"""Critique quantitative claims by recomputing the underlying quantity.

Variants: ``magnitude``, ``units``, ``direction``, ``bounds``,
``monotonicity``, and ``control_plausible``. The first five variants emit both
plausible and implausible claims; the control is always plausible. Five
shared-context renderings and all four applied modifiers are supported.
Claims perturb an exact value, its unit, its direction, or a physical bound.
Op-codes: ``SELECT_RELEVANT``, ``ESTIMATE``, ``ESTIMATE_CHECK``,
``MODEL_EQ``, ``PERCENT_TO_DEC``, ``BOUND``, ``PLAUSIBLE``, ``M``, ``D``,
``S``, ``CHECK``, and ``Z``.
"""
import random
import re
from fractions import Fraction

from applied_common import (CONTEXTS, NAMES, estimate_first, exact, money,
                            select_relevant_step, unit)
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("magnitude", "units", "direction", "bounds", "monotonicity",
            "control_plausible")
CASE_FAMILIES = ("magnitude", "units", "direction", "bounds",
                 "monotonicity")
FRAMES = (
    "At {place}, {name} reviews a report. {facts} {question}",
    "{question} Here is the report {name} received at {place}: {facts}",
    "For {name} at {place}, the recorded situation is this: {facts} {question}",
    "At {place}, a note handed to {name} reads: {facts} {question}",
    "Consider the quantitative report from {place} that {name} is checking. "
    "{facts} {question}",
)
PLACES = tuple(
    setting
    for key in ("trip", "garden", "shop", "lab", "workshop", "business")
    for setting in CONTEXTS[key].settings
)
TIMES = (Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2),
         Fraction(3), Fraction(7, 2), Fraction(4))
PERCENTS = (10, 20, 25, 40, 50)


def _render(facts, question):
    return random.choice(FRAMES).format(
        facts=facts, question=question, place=random.choice(PLACES),
        name=random.choice(NAMES))


def _verdict(claim_correct):
    return "plausible" if claim_correct else "implausible"


def _answer(claim_correct, correct):
    return f"{_verdict(claim_correct)}; correct {correct}"


class PlausibilityCriticGenerator(ProblemGenerator):
    """Generate exact quantitative claim checks with positive controls."""

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant = variant
        self.modifier = modifier

    @staticmethod
    def _magnitude(force_correct=None):
        speed = random.randrange(30, 121, 5)
        travel_time = random.choice(TIMES)
        distance = speed * travel_time
        claim_correct = (random.randrange(3) == 0 if force_correct is None
                         else force_correct)
        if claim_correct:
            claim = Fraction(speed)
        else:
            factor = random.choice((Fraction(1, 2), Fraction(2), Fraction(3)))
            claim = speed * factor
        correct = unit(speed, "km/h")
        claim_text = unit(claim, "km/h")
        facts = (f"A van covers {exact(distance)} km in {exact(travel_time)} "
                 f"hours. {random.choice(NAMES)} says its speed over the trip "
                 f"is {claim_text}.")
        question = "Is that claim consistent with the recorded quantities?"
        model = (f"v = {exact(distance)}/{exact(travel_time)} = "
                 f"{correct}")
        steps = [step("D", exact(distance), exact(travel_time), speed),
                 step("PLAUSIBLE", "yes" if claim_correct else "no",
                      "claim matches distance per elapsed time" if claim_correct
                      else "claim differs from distance per elapsed time"),
                 step("CHECK", f"claim {claim_text}", f"correct {correct}",
                      _verdict(claim_correct))]
        used = [f"{exact(distance)} km", f"{exact(travel_time)} hours",
                f"claim {claim_text}"]
        work = (f"{exact(distance)} km divided by "
                f"{exact(travel_time)} hours")
        return (facts, question, steps, _answer(claim_correct, correct),
                Fraction(speed), model, used,
                lambda value: unit(value, "km/h"))

    @staticmethod
    def _units(force_correct=None):
        length, width = random.sample(range(3, 21), 2)
        covered = length * width
        claim_correct = (random.randrange(3) == 0 if force_correct is None
                         else force_correct)
        claim_unit = "m²" if claim_correct else "m"
        correct = unit(covered, "m²")
        claim_text = unit(covered, claim_unit)
        facts = (f"A rectangular floor is {length} m long and {width} m wide. "
                 f"{random.choice(NAMES)} says the amount of floor covered is "
                 f"{claim_text}.")
        question = "Is that claim consistent with the recorded quantities?"
        model = f"q = {length}*{width} = {correct}"
        steps = [step("M", length, width, covered),
                 step("PLAUSIBLE", "yes" if claim_correct else "no",
                      "covered surface uses square metres"),
                 step("CHECK", f"claim {claim_text}", f"correct {correct}",
                      _verdict(claim_correct))]
        used = [f"length {length} m", f"width {width} m",
                f"claim {claim_text}"]
        work = f"about {length} by {width} square metres"
        return (facts, question, steps, _answer(claim_correct, correct),
                Fraction(covered), model, used,
                lambda value: unit(value, "m²"))

    @staticmethod
    def _direction(force_correct=None):
        percent = random.choice(PERCENTS)
        price = random.randrange(20, 201, 5)
        discount = Fraction(price * percent, 100)
        sale = price - discount
        claim_correct = (random.randrange(3) == 0 if force_correct is None
                         else force_correct)
        claim = sale if claim_correct else price + discount
        correct = money(sale)
        claim_text = money(claim)
        facts = (f"An item is marked {money(price)} and then reduced by "
                 f"{percent}% of that marked price. {random.choice(NAMES)} "
                 f"says the new price is {claim_text}.")
        question = "Is that claim consistent with the recorded change?"
        model = f"s = {price}*(1 - {percent}/100) = {correct}"
        steps = [step("PERCENT_TO_DEC", f"{percent}%",
                      exact(Fraction(percent, 100))),
                 step("M", price, exact(Fraction(percent, 100)),
                      exact(discount)),
                 step("S", price, exact(discount), exact(sale)),
                 step("PLAUSIBLE", "yes" if claim_correct else "no",
                      "a reduction lowers the marked price"),
                 step("CHECK", f"claim {claim_text}", f"correct {correct}",
                      _verdict(claim_correct))]
        used = [f"marked price {money(price)}", f"reduction {percent}%",
                f"claim {claim_text}"]
        work = f"{money(price)} minus about {percent}%"
        return (facts, question, steps, _answer(claim_correct, correct),
                sale, model, used, money)

    @staticmethod
    def _bounds(force_correct=None):
        total = random.randint(8, 40)
        blue = random.randint(2, total - 2)
        correct_value = Fraction(blue, total)
        claim_correct = (random.randrange(3) == 0 if force_correct is None
                         else force_correct)
        claim = correct_value if claim_correct else Fraction(total + blue, total)
        correct = exact(correct_value)
        claim_text = exact(claim)
        facts = (f"A box holds {blue} blue beads among {total} beads in all. "
                 f"One bead will be chosen without looking. "
                 f"{random.choice(NAMES)} says the chance of blue is "
                 f"{claim_text}.")
        question = "Is that claim consistent with the recorded counts?"
        model = f"p = {blue}/{total} = {correct}"
        steps = [step("BOUND", f"0 ≤ chance ≤ 1", claim_text,
                      "a part cannot exceed the whole"),
                 step("D", blue, total, correct),
                 step("PLAUSIBLE", "yes" if claim_correct else "no",
                      "claim stays within the count-based bound" if claim_correct
                      else "claim exceeds the upper bound 1"),
                 step("CHECK", f"claim {claim_text}", f"correct {correct}",
                      _verdict(claim_correct))]
        used = [f"{blue} blue beads", f"{total} beads total",
                f"claim {claim_text}"]
        work = f"{blue} out of {total}, less than one"
        return (facts, question, steps, _answer(claim_correct, correct),
                correct_value, model, used, exact)

    @staticmethod
    def _monotonicity(force_correct=None):
        workers = random.randint(2, 8)
        factor = random.randint(2, 4)
        more_workers = workers * factor
        new_time = random.randint(1, 8)
        old_time = new_time * factor
        worker_hours = workers * old_time
        claim_correct = (random.randrange(3) == 0 if force_correct is None
                         else force_correct)
        claim = new_time if claim_correct else old_time * factor
        correct = unit(new_time, "hour")
        claim_text = unit(claim, "hour")
        facts = (f"A crew of {workers} identical workers completes a fixed job "
                 f"in {old_time} hours. A crew of {more_workers} workers at "
                 f"the same steady pace is assigned the same job. "
                 f"{random.choice(NAMES)} says it will take {claim_text}.")
        question = "Is that claim consistent with the change in crew size?"
        model = (f"t = {workers}*{old_time}/{more_workers} = "
                 f"{correct}")
        steps = [step("M", workers, old_time, worker_hours),
                 step("D", worker_hours, more_workers, new_time),
                 step("PLAUSIBLE", "yes" if claim_correct else "no",
                      "more equal workers shorten the fixed job"),
                 step("CHECK", f"claim {claim_text}", f"correct {correct}",
                      _verdict(claim_correct))]
        used = [f"{workers} workers", f"{old_time} hours",
                f"{more_workers} workers", f"claim {claim_text}"]
        work = f"crew size grows by {factor}, so time is about one-{factor}th"
        return (facts, question, steps, _answer(claim_correct, correct),
                Fraction(new_time), model, used,
                lambda value: unit(value, "hour"))

    @classmethod
    def _case(cls, family, force_correct=None):
        return getattr(cls, f"_{family}")(force_correct)

    def generate(self):
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)
        if variant == "control_plausible":
            family = random.choice(CASE_FAMILIES)
            force_correct = True
        else:
            family = variant
            force_correct = None
        facts, question, steps, answer, value, model, used, renderer = self._case(
            family, force_correct)
        problem = _render(facts, question)

        if modifier == "distractor":
            occupied = {int(token) for token in re.findall(r"\d+", problem)}
            extra = random.choice([number for number in range(101, 401)
                                   if number not in occupied])
            problem = f"A nearby notice lists {extra} storage lockers. {problem}"
            steps.insert(0, select_relevant_step(used,
                                                 f"{extra} storage lockers"))
        elif modifier == "estimate_first":
            steps = estimate_first(
                steps + [step("Z", answer)], value,
                "approximate the correct quantity before checking the claim",
                render=renderer)[:-1]
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model,
                                 "relationship among the recorded quantities"))
            answer = f"{model}; {answer}"

        steps.append(step("Z", answer))
        return {
            "problem_id": jid(),
            "operation": f"applied_plausibility_critic_{variant}_{modifier}",
            "problem": problem,
            "steps": steps,
            "final_answer": answer,
        }
