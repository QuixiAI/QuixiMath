import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


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

    Op-codes used:
    - MODEL: the model formula (formula)
    - MODEL_APPLY: the formula with values substituted (instantiation)
    - PERCENT_TO_DEC: rate conversion (established)
    - A / S / E / M / D: exact decimal arithmetic (established)
    - Z: money, mass with unit, or exact exponential form
    """

    VARIANTS = ["growth", "decay", "half_life", "continuous"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant in ("growth", "decay"):
            while True:
                P = random.choice([200, 400, 500, 800, 1000, 2000, 4000,
                                   5000, 8000])
                r = random.choice([10, 20, 25, 50])
                t = random.randint(2, 4)
                base = 1 + Fraction(r, 100) * (1 if variant == "growth"
                                               else -1)
                value = P * base ** t
                if (value * 100).denominator == 1:
                    break
            rate_dec = dec(Fraction(r, 100))
            base_txt = dec(base)
            if variant == "growth":
                formula = "A = P(1 + r)^t"
                combine = step("A", 1, rate_dec, base_txt)
                problem = (f"An investment of ${P} grows {r}% per year. "
                           f"What is it worth after {t} years?")
            else:
                formula = "A = P(1 - r)^t"
                combine = step("S", 1, rate_dec, base_txt)
                problem = (f"A machine worth ${P} loses {r}% of its value "
                           f"each year. What is it worth after {t} years?")
            answer = money(value)
            steps = [
                step("MODEL", formula),
                step("MODEL_APPLY", f"A = {P} · (1 "
                     f"{'+' if variant == 'growth' else '-'} "
                     f"{rate_dec})^{t}"),
                step("PERCENT_TO_DEC", f"{r}%", rate_dec),
                combine,
                step("E", base_txt, t, dec(base ** t)),
                step("M", P, dec(base ** t), dec(value)),
                step("Z", answer),
            ]
            op = f"exponential_{variant}"
        elif variant == "half_life":
            k = random.randint(2, 4)
            h = random.choice([3, 5, 10, 12, 20, 25])
            m0 = random.choice([1, 3, 5, 6, 7]) * 2 ** k
            t = k * h
            remaining = m0 >> k
            answer = f"{remaining} g"
            steps = [
                step("MODEL", "A = P · (1/2)^(t/h)"),
                step("MODEL_APPLY", f"A = {m0} · (1/2)^({t}/{h})"),
                step("D", t, h, k),
            ]
            cur = m0
            for _ in range(k):
                steps.append(step("D", cur, 2, cur // 2))
                cur //= 2
            steps.append(step("Z", answer))
            problem = (f"A sample of {m0} g has a half-life of {h} years. "
                       f"How much remains after {t} years?")
            op = "exponential_half_life"
        else:
            P = random.choice([200, 300, 500, 750, 1000, 1500, 2000])
            r = random.choice([2, 3, 4, 5, 6, 8])
            t = random.randint(2, 12)
            rt = dec(Fraction(r * t, 100))
            answer = f"{P}e^{rt}"
            steps = [
                step("MODEL", "A = Pe^(rt)"),
                step("PERCENT_TO_DEC", f"{r}%", dec(Fraction(r, 100))),
                step("M", dec(Fraction(r, 100)), t, rt),
                step("MODEL_APPLY", f"A = {P}e^{rt}"),
                step("Z", answer),
            ]
            problem = (f"An investment of ${P} earns {r}% interest "
                       f"compounded continuously. Give its exact value "
                       f"in dollars after {t} years.")
            op = "exponential_continuous"

        return dict(
            problem_id=jid(),
            operation=op,
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
