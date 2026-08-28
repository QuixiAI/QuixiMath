"""Supplied-factor scale estimates with bounds and paired comparisons.

Variants: ``water_use``, ``stadium``, ``cafeteria``, ``household_water``,
``city_buses``, ``school_lunches``, ``book_pages``, ``road_trip_fuel``,
``waste_bags``, ``bound_check``, and ``compare_two_estimates``. Five
renderings and all four applied modifiers are supported. Op-codes:
``FERMI_SETUP``, ``FERMI_FACTOR``, ``SIGFIG_ROUND``, ``ESTIMATE``,
``ESTIMATE_CHECK``, ``BOUND``, ``PLAUSIBLE``, ``CMP``, ``M``, ``D``, ``Z``.
"""
import random
import re

from applied_common import CONTEXTS, NAMES, select_relevant_step
from base_generator import ProblemGenerator
from helpers import jid, step


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")
VARIANTS = ("water_use", "stadium", "cafeteria", "household_water",
            "city_buses", "school_lunches", "book_pages", "road_trip_fuel",
            "waste_bags", "bound_check", "compare_two_estimates")
FRAMES = (
    "At {place}, {name} builds a scale estimate. {facts} {question}",
    "{question} Supplied factors given to {name} at {place} state: {facts}",
    "For {name} at {place}, the estimate is described this way: {facts} {question}",
    "At {place}, a note reviewed by {name} reads: {facts} {question}",
    "Consider the supplied-factor estimate from {place} that {name} checks. {facts} {question}",
)
PLACES = tuple(setting for key in ("business", "classroom", "trip", "shop", "workshop")
               for setting in CONTEXTS[key].settings)


def sig2(n):
    """Round a positive integer to two significant digits in scientific text."""
    assert n > 0
    exponent = len(str(n)) - 1
    if exponent <= 1:
        return str(n)
    place = 10 ** (exponent - 1)
    q, remainder = divmod(n, place)
    if remainder * 2 >= place:
        q += 1
    if q == 100:
        q, exponent = 10, exponent + 1
    mantissa = str(q // 10) if q % 10 == 0 else f"{q // 10}.{q % 10}"
    return f"{mantissa} × 10^{exponent}"


def _render(facts, question):
    return random.choice(FRAMES).format(facts=facts, question=question,
                                        place=random.choice(PLACES),
                                        name=random.choice(NAMES))


class FermiEstimationGenerator(ProblemGenerator):
    VARIANTS, MODIFIERS = VARIANTS, MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _product(target, units, factors, facts, question):
        steps, product, used, parts = [step("FERMI_SETUP", target, units)], 1, [], []
        for label, value in factors:
            steps.append(step("FERMI_FACTOR", label, value))
            used.append(f"{label} {value}")
            parts.append(str(value))
            old, product = product, product * value
            if old != 1:
                steps.append(step("M", old, value, product))
        rounded = sig2(product)
        steps += [step("SIGFIG_ROUND", product, "2 significant figures", rounded),
                  step("ESTIMATE_CHECK", rounded, product, "rounded estimate")]
        return (facts, question, steps, f"{rounded} {units}", product,
                f"{' × '.join(parts)} = {product} {units}", used)

    @classmethod
    def _standard(cls, variant):
        if variant == "water_use":
            a, b = random.choice((12000, 18000, 24000, 36000, 52000, 75000)), random.choice((60, 75, 80, 90, 110, 125))
            return cls._product("town water", "gallons/day", (("people", a), ("gallons/person/day", b)), f"A town has {a} people using {b} gallons per person each day.", "Estimate daily water and round to two significant figures.")
        if variant == "stadium":
            a, b, c = random.choice((18, 24, 32, 40, 48)), random.choice((18, 24, 28, 32, 36)), random.choice((14, 16, 18, 20, 22))
            return cls._product("stadium seats", "seats", (("sections", a), ("rows/section", b), ("seats/row", c)), f"A stadium has {a} sections, {b} rows per section, and {c} seats per row.", "Estimate all seats and round to two significant figures.")
        if variant == "cafeteria":
            a, b, c = random.choice((450, 600, 750, 900, 1200, 1500)), random.choice((1, 2, 3, 4)), random.choice((30, 32, 36, 40))
            return cls._product("pizza slices", "slices/year", (("students", a), ("slices/student/week", b), ("weeks", c)), f"A school has {a} students eating {b} pizza slices per week for {c} weeks.", "Estimate yearly slices and round to two significant figures.")
        if variant == "household_water":
            a, b, c = random.randint(2, 7), random.choice((80, 100, 120, 150, 180, 200)), random.choice((28, 30, 31))
            return cls._product("household water", "liters/month", (("people", a), ("liters/person/day", b), ("days", c)), f"A household has {a} people using {b} liters per person per day for {c} days.", "Estimate monthly water and round to two significant figures.")
        if variant == "city_buses":
            a, b, c = random.choice((40, 60, 80, 100, 120, 150)), random.choice((6, 8, 10, 12, 14)), random.choice((20, 25, 30, 35, 40, 45))
            return cls._product("bus rides", "rides/day", (("buses", a), ("trips/bus", b), ("riders/trip", c)), f"A city runs {a} buses making {b} trips per day with {c} riders per trip.", "Estimate daily rides and round to two significant figures.")
        if variant == "school_lunches":
            a, b, c = random.choice((300, 450, 600, 750, 900, 1200)), random.choice((160, 170, 175, 180)), random.choice((1, 2))
            lunch_word = "lunch" if c == 1 else "lunches"
            return cls._product("school lunches", "lunches/year", (("students", a), ("days", b), ("lunches/student/day", c)), f"A district serves {a} students for {b} days at {c} {lunch_word} per student per day.", "Estimate yearly lunches and round to two significant figures.")
        if variant == "book_pages":
            a, b, c = random.choice((120, 180, 240, 300, 450, 600)), random.choice((180, 220, 250, 300, 360, 400)), random.choice((1, 2, 3, 4))
            copy_word = "copy" if c == 1 else "copies"
            return cls._product("printed pages", "pages", (("titles", a), ("pages/title", b), ("copies", c)), f"A print run has {a} titles, {b} pages per title, and {c} {copy_word} of each.", "Estimate printed pages and round to two significant figures.")
        if variant == "waste_bags":
            a, b, c = random.choice((1200, 1800, 2400, 3600, 5000, 7500)), random.choice((1, 2, 3, 4)), random.choice((48, 50, 52))
            return cls._product("waste bags", "bags/year", (("households", a), ("bags/household/week", b), ("weeks", c)), f"A community has {a} households producing {b} waste bags each week for {c} weeks.", "Estimate yearly bags and round to two significant figures.")
        raise AssertionError(variant)

    @staticmethod
    def _road_trip_fuel():
        rate, liters = random.choice((8, 10, 12, 15, 20)), random.choice((20, 30, 40, 50, 60, 75))
        distance, rounded = rate * liters, sig2(liters)
        steps = [step("FERMI_SETUP", "trip fuel", "liters"), step("FERMI_FACTOR", "distance", distance), step("FERMI_FACTOR", "km/liter", rate), step("D", distance, rate, liters), step("SIGFIG_ROUND", liters, "2 significant figures", rounded), step("ESTIMATE_CHECK", rounded, liters, "rounded estimate")]
        return (f"A trip covers {distance} km at {rate} km per liter.", "Estimate fuel and round to two significant figures.", steps, f"{rounded} liters", liters, f"{distance} ÷ {rate} = {liters} liters", [f"distance {distance}", f"rate {rate}"])

    @staticmethod
    def _bound_check():
        h, bags, weeks = random.choice((10000, 20000, 30000, 50000, 80000)), random.choice((2, 3, 4, 5)), 52
        partial, upper = h * bags, h * bags * weeks
        power = len(str(upper)) - 1
        plausible = random.choice((True, False))
        claim_power = power if plausible else min(9, power + 2)
        claim, rounded = 10 ** claim_power, sig2(upper)
        verdict = "plausible" if plausible else "implausible"
        facts = f"A region has at most {h} households, {bags} bags per household each week, and {weeks} weeks. A claim gives 10^{claim_power} bags per year."
        steps = [step("FERMI_SETUP", "bag upper bound", "bags/year"), step("M", h, bags, partial), step("M", partial, weeks, upper), step("BOUND", f"claim 10^{claim_power}", f"upper {upper}", "within" if plausible else "exceeds"), step("PLAUSIBLE", "yes" if plausible else "no", verdict), step("SIGFIG_ROUND", upper, "2 significant figures", rounded), step("CHECK", claim, upper, verdict)]
        return (facts, "Is that scale plausible under the supplied bounds?", steps, f"{verdict}; claim 10^{claim_power}; upper bound {rounded} bags/year", upper, f"upper = {h} × {bags} × {weeks} = {upper}", [f"households {h}", f"bags {bags}", f"weeks {weeks}", f"claim 10^{claim_power}"])

    @staticmethod
    def _compare_two_estimates():
        a, b = random.choice((8, 12, 16, 20, 24, 30)), random.choice((300, 400, 500, 600, 750))
        c, d, e = random.choice((20, 30, 40, 50, 60)), random.choice((80, 100, 120, 150, 200)), random.choice((2, 3, 4))
        first, partial, second = a * b, c * d, c * d * e
        if first == second:
            e, second = e + 1, partial * (e + 1)
        choice, ra, rb = ("estimate A" if first > second else "estimate B"), sig2(first), sig2(second)
        facts = f"Estimate A uses {a} schools with {b} people each. Estimate B uses {c} neighborhoods with {d} households each and {e} people per household."
        steps = [step("FERMI_SETUP", "two estimates", "people"), step("M", a, b, first), step("M", c, d, partial), step("M", partial, e, second), step("SIGFIG_ROUND", first, "2 significant figures", ra), step("SIGFIG_ROUND", second, "2 significant figures", rb), step("CMP", f"A {first}", f"B {second}", ">" if first > second else "<"), step("CHECK", "larger", choice)]
        return (facts, "Which estimate is larger, and what are both rounded values?", steps, f"{choice}; A {ra} people; B {rb} people", max(first, second), f"A={a} × {b}; B={c} × {d} × {e}", [f"A {a} by {b}", f"B {c} by {d} by {e}"])

    @classmethod
    def _case(cls, variant):
        if variant == "road_trip_fuel": return cls._road_trip_fuel()
        if variant == "bound_check": return cls._bound_check()
        if variant == "compare_two_estimates": return cls._compare_two_estimates()
        return cls._standard(variant)

    def generate(self):
        variant, modifier = self.variant or random.choice(self.VARIANTS), self.modifier or random.choice(self.MODIFIERS)
        facts, question, steps, answer, value, model, used = self._case(variant)
        problem = _render(facts, question)
        if modifier == "distractor":
            occupied = {int(x) for x in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in range(181, 481) if n not in occupied])
            problem = f"A nearby notice lists {extra} empty bins. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} empty bins"))
        elif modifier == "estimate_first":
            estimate = sig2(int(value))
            steps.insert(0, step("ESTIMATE", "combine supplied factor scales", estimate))
            if steps[-1].split("|", 1)[0] != "ESTIMATE_CHECK":
                steps.append(step("ESTIMATE_CHECK", estimate, value, "same scale"))
        elif modifier == "with_model":
            steps.insert(0, step("MODEL_EQ", model, "supplied-factor model"))
            answer = f"{model}; {answer}"
        steps.append(step("Z", answer))
        return {"problem_id": jid(), "operation": f"applied_fermi_estimation_{variant}_{modifier}", "problem": problem, "steps": steps, "final_answer": answer}
