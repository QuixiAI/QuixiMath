"""Compound growth, decay, half-life, and continuous compounding, kept exact.

Variants: ``growth``, ``decay``, ``half_life``, ``continuous``. Six phrasings
per variant over forty names and dozens of contexts, plus all four applied
modifiers (``plain``, ``distractor``, ``estimate_first``, ``with_model``).
Op-codes: ``MODEL``, ``MODEL_APPLY``, ``PERCENT_TO_DEC``, ``SELECT_RELEVANT``,
``ESTIMATE``, ``ESTIMATE_CHECK``, ``A``, ``S``, ``E``, ``M``, ``D``, ``Z``.
"""
import random
import re
from fractions import Fraction
from math import gcd

from applied_common import estimate_first, select_relevant_step
from base_generator import ProblemGenerator
from helpers import step, jid


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")


def dec(fr):
    """Exact decimal string for a Fraction whose denominator is
    2^a·5^b: 33/10 -> '3.3', 1331/1000 -> '1.331'."""
    num, den = fr.numerator, fr.denominator
    p10 = 0
    while den % 2 == 0:
        den //= 2
        num *= 5
        p10 += 1
    while den % 5 == 0:
        den //= 5
        num *= 2
        p10 += 1
    assert den == 1, fr
    if p10 == 0:
        return str(num)
    s = str(abs(num)).rjust(p10 + 1, "0")
    out = f"{s[:-p10]}.{s[-p10:]}".rstrip("0").rstrip(".")
    return ("-" if num < 0 else "") + out


def money(fr):
    """Fraction dollars -> '$665.50'."""
    cents = fr * 100
    assert cents.denominator == 1
    c = cents.numerator
    return f"${c // 100}.{c % 100:02d}"


def _places(fr):
    """Decimal places in the exact decimal render of ``fr``."""
    s = dec(fr)
    return len(s.split(".")[1]) if "." in s else 0


def _rate_time_options(sign):
    """(rate percent, years) pairs whose accumulation factor still has at
    most four decimal places, so the closing multiplication stays short."""
    out = []
    for r in range(1, 96):
        base = 1 + sign * Fraction(r, 100)
        if base <= 0:
            continue
        for t in range(2, 7):
            if _places(base ** t) <= 4:
                out.append((r, t))
    return out


GROWTH_RATES = _rate_time_options(1)
DECAY_RATES = _rate_time_options(-1)

NAMES = [
    "Alina", "Bo", "Cyrus", "Daniela", "Eli", "Fatou", "Gideon", "Hina",
    "Ivan", "Jamila", "Kofi", "Lena", "Mateo", "Nia", "Oleg", "Paloma",
    "Quinn", "Rania", "Soren", "Talia", "Umar", "Valeria", "Wren", "Xiulan",
    "Yara", "Zeke", "Amara", "Bertil", "Chiara", "Dolores", "Emeka", "Freya",
    "Goran", "Hilde", "Ilya", "Josefa", "Kwame", "Leif", "Marisol", "Nadir",
]

GROWTH_THINGS = [
    "a savings account", "a bond fund", "an index fund",
    "a certificate of deposit", "an art collection", "a vintage guitar",
    "a rare coin set", "a small vineyard", "a stamp album",
    "a share of a startup", "a timber lot", "a classic motorcycle",
    "a jewellery box", "a fine violin", "a plot of farmland",
]

DECAY_THINGS = [
    "a delivery van", "a laser cutter", "a printing press", "a tractor",
    "a fishing boat", "a laptop", "a coffee roaster", "a snow plough",
    "a camera body", "a milling machine", "a hot air balloon",
    "a food truck", "a sewing machine", "an excavator", "a tour bus",
]

CONT_THINGS = [
    "a money market account", "a college fund", "a retirement account",
    "a brokerage account", "a savings bond", "a trust account",
    "a business reserve", "a rainy day fund",
]

SUBSTANCES = [
    "iodine", "radium", "polonium", "technetium", "a medical tracer",
    "a radioactive dye", "a laboratory isotope", "cobalt", "caesium",
    "strontium", "a fluorescent marker", "the sample isotope",
    "a decaying catalyst", "a shipment isotope", "thorium",
]

MASS_UNITS = ["g", "mg", "kg"]
TIME_UNITS = ["years", "days", "hours"]

GROWTH_TEMPLATES = [
    "An investment of ${P} grows {r}% per year. What is it worth after "
    "{t} years?",
    "{name} puts ${P} into {thing} that grows {r}% each year. What is it "
    "worth after {t} years?",
    "{Thing} bought for ${P} appreciates {r}% per year. Give its value "
    "after {t} years.",
    "A fund holding ${P} increases {r}% annually. How much is in it after "
    "{t} years?",
    "{name} invests ${P} in {thing}; its value rises {r}% per year. What is "
    "it worth after {t} years?",
    "{Thing} is worth ${P} today and gains {r}% of its value every year. "
    "What is it worth after {t} years?",
]

DECAY_TEMPLATES = [
    "A machine worth ${P} loses {r}% of its value each year. What is it "
    "worth after {t} years?",
    "{name} owns {thing} worth ${P} that loses {r}% of its value each "
    "year. What is it worth after {t} years?",
    "{Thing} bought for ${P} depreciates {r}% per year. Give its value "
    "after {t} years.",
    "The book value of {thing} is ${P} and declines {r}% annually. What is "
    "the book value after {t} years?",
    "{name} bought {thing} for ${P}; its resale value drops {r}% each "
    "year. What is it worth after {t} years?",
    "{Thing} valued at ${P} falls {r}% in value every year. What is its "
    "value after {t} years?",
]

HALF_LIFE_TEMPLATES = [
    "A sample of {m0} {u} has a half-life of {h} {tu}. How much remains "
    "after {t} {tu}?",
    "{name} measures {m0} {u} of {sub}, whose half-life is {h} {tu}. How "
    "much is left after {t} {tu}?",
    "{Sub} decays with a half-life of {h} {tu}. Starting from {m0} {u}, "
    "how much remains after {t} {tu}?",
    "A {m0} {u} sample of {sub} is stored for {t} {tu}. If its half-life "
    "is {h} {tu}, how much remains?",
    "The half-life of {sub} is {h} {tu}. How much of a {m0} {u} sample is "
    "left after {t} {tu}?",
]

CONTINUOUS_TEMPLATES = [
    "An investment of ${P} earns {r}% interest compounded continuously. "
    "Give its exact value in dollars after {t} years.",
    "{name} deposits ${P} at {r}% compounded continuously. Write the exact "
    "value in dollars after {t} years.",
    "${P} is placed in an account paying {r}% continuously compounded "
    "interest. Give the exact value in dollars after {t} years.",
    "A trust holds ${P} earning {r}% compounded continuously. Give its "
    "exact value in dollars after {t} years.",
    "{name} opens {thing} with ${P} at {r}% compounded continuously. Give "
    "the exact value in dollars after {t} years.",
]

#: What the distractor sentence names, chosen not to collide with any digit
#: pattern the oracle scans for (dollars, percents, years, mass/time units).
DISTRACTOR_RANGE = range(151, 551)


def _cap(phrase):
    return phrase[0].upper() + phrase[1:]


class ExponentialModelGenerator(ProblemGenerator):
    """
    Exponential models kept exact by hand: compound growth and decay
    with terminating-decimal bases, half-life as literal repeated
    halving, and continuous compounding left in exact Pe^rt form.

    Variants:
    - growth:     A = P(1 + r)^t on an investment
    - decay:      A = P(1 - r)^t on a depreciating value
    - half_life:  A = P·(1/2)^(t/h), the sample halved step by step
    - continuous: A = Pe^(rt); the answer stays exact, e.g. 500e^0.3

    Widened axes: every rate 1..95% whose accumulation factor stays within
    four decimal places, terms of 2..6 periods, principals drawn from the
    whole exact-cents lattice, half-lives and sample masses built backward
    from an exact remainder, three mass units and three time units, and
    six phrasings per variant over forty names and dozens of contexts.

    Modifiers (``plain``, ``distractor``, ``estimate_first``,
    ``with_model``): ``distractor`` names an irrelevant count and flags it
    with ``SELECT_RELEVANT``; ``estimate_first`` predicts the answer's scale
    (``ESTIMATE`` / ``ESTIMATE_CHECK``) before the exact steps run;
    ``with_model`` puts the named formula in front of the answer.

    Op-codes used:
    - MODEL: the model formula (formula)
    - MODEL_APPLY: the formula with values substituted (instantiation)
    - PERCENT_TO_DEC: rate conversion (established)
    - SELECT_RELEVANT / ESTIMATE / ESTIMATE_CHECK: shared applied modifiers
    - A / S / E / M / D: exact decimal arithmetic (established)
    - Z: money, mass with unit, or exact exponential form
    """

    VARIANTS = ["growth", "decay", "half_life", "continuous"]
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    @staticmethod
    def _principal(factor):
        """A principal that keeps P·factor exact to the cent, drawn from as
        round a lattice as the factor allows."""
        need = factor.denominator // gcd(factor.numerator * 100,
                                         factor.denominator)
        for grid in (100, 25, 5, 1):
            stride = need * grid // gcd(need, grid)
            if stride <= 2000:
                break
        top = 40000 // stride
        low = max(1, (100 + stride - 1) // stride)
        return stride * random.randint(low, max(low, top))

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        modifier = self.modifier or random.choice(self.MODIFIERS)

        if variant in ("growth", "decay"):
            grow = variant == "growth"
            r, t = random.choice(GROWTH_RATES if grow else DECAY_RATES)
            base = 1 + Fraction(r, 100) * (1 if grow else -1)
            P = self._principal(base ** t)
            value = P * base ** t
            rate_dec = dec(Fraction(r, 100))
            base_txt = dec(base)
            name = random.choice(NAMES)
            thing = random.choice(GROWTH_THINGS if grow else DECAY_THINGS)
            template = random.choice(GROWTH_TEMPLATES if grow
                                     else DECAY_TEMPLATES)
            problem = template.format(P=P, r=r, t=t, name=name, thing=thing,
                                      Thing=_cap(thing))
            if grow:
                formula = "A = P(1 + r)^t"
                combine = step("A", 1, rate_dec, base_txt)
            else:
                formula = "A = P(1 - r)^t"
                combine = step("S", 1, rate_dec, base_txt)
            answer = money(value)
            steps = [
                step("MODEL", formula),
                step("MODEL_APPLY", f"A = {P} · (1 "
                     f"{'+' if grow else '-'} "
                     f"{rate_dec})^{t}"),
                step("PERCENT_TO_DEC", f"{r}%", rate_dec),
                combine,
                step("E", base_txt, t, dec(base ** t)),
                step("M", P, dec(base ** t), dec(value)),
            ]
            used = [f"principal ${P}", f"rate {r}%", f"years {t}"]
            est_value, renderer = value, money
            est_work = "predict the compounded value's scale"
        elif variant == "half_life":
            k = random.randint(2, 6)
            h = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18,
                               20, 24, 25, 28, 30, 36, 40, 45, 50, 60, 75,
                               80, 90, 100, 120])
            remaining = random.choice([n for n in range(1, 100)
                                       if n % 2 == 1])
            m0 = remaining * 2 ** k
            t = k * h
            unit = random.choice(MASS_UNITS)
            tu = random.choice(TIME_UNITS)
            sub = random.choice(SUBSTANCES)
            formula = "A = P · (1/2)^(t/h)"
            answer = f"{remaining} {unit}"
            steps = [
                step("MODEL", formula),
                step("MODEL_APPLY", f"A = {m0} · (1/2)^({t}/{h})"),
                step("D", t, h, k),
            ]
            cur = m0
            for _ in range(k):
                steps.append(step("D", cur, 2, cur // 2))
                cur //= 2
            problem = random.choice(HALF_LIFE_TEMPLATES).format(
                m0=m0, h=h, t=t, u=unit, tu=tu, sub=sub, Sub=_cap(sub),
                name=random.choice(NAMES))
            used = [f"initial {m0} {unit}", f"half-life {h} {tu}",
                    f"elapsed {t} {tu}"]
            est_value, renderer = Fraction(remaining), (lambda v, u=unit: f"{v} {u}")
            est_work = "predict the remaining amount after repeated halving"
        else:
            P = 25 * random.randint(4, 2000)
            r = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14,
                               15, 16, 18, 20, 24, 25])
            t = random.randint(2, 20)
            rt = dec(Fraction(r * t, 100))
            formula = "A = Pe^(rt)"
            answer = f"{P}e^{rt}"
            steps = [
                step("MODEL", formula),
                step("PERCENT_TO_DEC", f"{r}%", dec(Fraction(r, 100))),
                step("M", dec(Fraction(r, 100)), t, rt),
                step("MODEL_APPLY", f"A = {P}e^{rt}"),
            ]
            problem = random.choice(CONTINUOUS_TEMPLATES).format(
                P=P, r=r, t=t, name=random.choice(NAMES),
                thing=random.choice(CONT_THINGS))
            used = [f"principal ${P}", f"rate {r}%", f"years {t}"]
            est_value, renderer = Fraction(P), money
            est_work = "predict the principal's scale in the exact answer"

        if modifier == "distractor":
            occupied = {int(x) for x in re.findall(r"\d+", problem)}
            extra = random.choice([n for n in DISTRACTOR_RANGE if n not in occupied])
            problem = f"A nearby ledger lists {extra} unrelated entries. {problem}"
            steps.insert(0, select_relevant_step(used, f"{extra} unrelated entries"))
        elif modifier == "estimate_first":
            steps = estimate_first(steps + [step("Z", answer)], est_value,
                                   est_work, render=renderer)[:-1]
        elif modifier == "with_model":
            answer = f"{formula}; {answer}"

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"applied_exponential_model_{variant}_{modifier}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
