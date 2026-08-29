import random
from fractions import Fraction
from itertools import accumulate
from math import gcd

from applied_common import apply_applied_modifier
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money
from generators.finance_generator import exact


APPLIED = True
MODIFIERS = ("plain", "distractor", "estimate_first", "with_model")

VARIANTS = ["future_value", "present_value", "amortization", "due",
            "perpetuity"]

NAMES = [
    "Amara", "Bennett", "Camila", "Devon", "Elena", "Farhan", "Greta",
    "Hollis", "Imani", "Jonas", "Keiko", "Lucia", "Marcus", "Nadia",
    "Omar", "Priya", "Quentin", "Rosa", "Silas", "Tamar", "Ulises",
    "Vera", "Wesley", "Ximena", "Yusuf", "Zara", "Adele", "Boris",
    "Corinne", "Dmitri", "Esme", "Felix", "Gwen", "Hugo", "Ingrid",
    "Javier", "Katya", "Leonel", "Mira", "Noor", "Oscar", "Petra",
    "Rashid", "Sonia", "Teodoro", "Ursula", "Viktor", "Willa",
]

FUNDS = [
    "savings plan", "retirement account", "college fund",
    "brokerage account", "money market account", "pension fund",
    "sinking fund", "reserve account", "investment account",
    "trust account", "credit union account", "endowment fund",
]

LOANS = [
    "car loan", "home improvement loan", "student loan",
    "equipment loan", "business loan", "personal loan", "boat loan",
    "renovation loan", "tuition loan", "furniture loan",
    "solar panel loan", "tractor loan",
]

RATES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 18, 20, 24, 25, 50]

PAY_LO = 50
PAY_HI = 9995
MAX_LEN = 12  # longest exact() rendering allowed for growth / factor


def cents_exact(value):
    return (value * 100).denominator == 1


def units_for(rate_pct):
    """Period words that read naturally for a per-period rate."""
    if rate_pct <= 5:
        return ["month", "quarter", "year", "period"]
    if rate_pct <= 12:
        return ["quarter", "year", "period"]
    if rate_pct <= 25:
        return ["year", "period"]
    return ["period"]


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def payment_multiple(factor):
    """Smallest m with m*factor exact to the cent."""
    d = factor.denominator
    return d // gcd(d, 100 * factor.numerator)


def multiples(m, lo=PAY_LO, hi=PAY_HI, round_to=5):
    """Hand-friendly multiples of ``m`` between lo and hi."""
    if m > hi:
        return []
    stride = round_to if round_to % m == 0 else m
    if stride < round_to:
        stride = m * ((round_to + m - 1) // m)
    first = ((lo + stride - 1) // stride) * stride
    return list(range(first, hi + 1, stride))


def _readable(*values):
    return all(len(exact(v)) <= MAX_LEN for v in values)


def _build_table(factor_of):
    """(rate_pct, periods, payments) triples whose answers stay exact."""
    table = []
    for rate_pct in RATES:
        rate = Fraction(rate_pct, 100)
        for periods in range(2, 8):
            growth = (1 + rate) ** periods
            factor = factor_of(rate, periods, growth)
            if not _readable(growth, factor):
                continue
            pays = multiples(payment_multiple(factor))
            if pays:
                table.append((rate_pct, periods, pays))
    return table


def _weights(table):
    """Cumulative weights so every (rate, n, payment) triple is equally likely."""
    return list(accumulate(len(row[-1]) for row in table))


def _pick(table, cum):
    row = random.choices(table, cum_weights=cum)[0]
    return row[:-1] + (random.choice(row[-1]),)


FV_TABLE = _build_table(lambda r, n, g: (g - 1) / r)
PV_TABLE = _build_table(lambda r, n, g: (1 - 1 / g) / r)
DUE_TABLE = _build_table(lambda r, n, g: (g - 1) / r * (1 + r))
PERP_TABLE = [
    (rate_pct, multiples(payment_multiple(Fraction(100, rate_pct))))
    for rate_pct in RATES if rate_pct <= 25
]

FV_WEIGHTS = _weights(FV_TABLE)
PV_WEIGHTS = _weights(PV_TABLE)
DUE_WEIGHTS = _weights(DUE_TABLE)
PERP_WEIGHTS = _weights(PERP_TABLE)

FV_TEMPLATES = [
    ("An ordinary annuity pays ${pmt} at the end of each {unit} for {n} "
     "{units} at {rate}% per {unit}. Find the future value."),
    ("{name} deposits ${pmt} into a {fund} at the end of each {unit} for "
     "{n} {units}. The account earns {rate}% per {unit}. What is the "
     "future value of the annuity?"),
    ("At the end of every {unit}, {name} adds ${pmt} to a {fund} that "
     "earns {rate}% per {unit}. How much is in the {fund} right after the "
     "{nth} deposit?"),
    ("A {fund} receives an end-of-{unit} payment of ${pmt} for {n} {units} "
     "and grows at {rate}% per {unit}. Find the accumulated value of the "
     "annuity."),
    ("{name} makes {n} end-of-{unit} deposits of ${pmt} each into a {fund} "
     "paying {rate}% per {unit}. Find the future value of the annuity."),
]

PV_TEMPLATES = [
    ("An ordinary annuity pays ${pmt} at the end of each {unit} for {n} "
     "{units} at {rate}% per {unit}. Find the present value."),
    ("{name} will receive ${pmt} at the end of each {unit} for {n} {units} "
     "from a {fund} earning {rate}% per {unit}. What is the present value "
     "of the annuity?"),
    ("How much must be deposited now in a {fund} earning {rate}% per "
     "{unit} so that it can pay out ${pmt} at the end of each {unit} for "
     "{n} {units}?"),
    ("A {loan} is repaid with {n} end-of-{unit} payments of ${pmt} at "
     "{rate}% per {unit}. Find the present value of the payment stream."),
    ("{name} is offered ${pmt} at the end of each {unit} for the next {n} "
     "{units}. At {rate}% per {unit}, what single amount today is worth "
     "the same?"),
]

DUE_TEMPLATES = [
    ("An annuity due pays ${pmt} at the beginning of each {unit} for {n} "
     "{units} at {rate}% per {unit}. Find the future value."),
    ("{name} deposits ${pmt} at the beginning of every {unit} into a "
     "{fund} earning {rate}% per {unit}. What is the value of the {fund} "
     "at the end of {n} {units}?"),
    ("Each {unit} opens with a ${pmt} deposit into a {fund} that pays "
     "{rate}% per {unit}. Find the future value of the annuity due after "
     "{n} {units}."),
    ("{name} makes {n} beginning-of-{unit} payments of ${pmt} into a "
     "{fund} at {rate}% per {unit}. Find the future value of the annuity "
     "due."),
]

PERP_TEMPLATES = [
    ("A perpetuity pays ${pmt} at the end of each {unit} forever. At "
     "{rate}% per {unit}, find its present value."),
    ("{name} wants a {fund} that pays ${pmt} at the end of each {unit} "
     "forever. If the {fund} earns {rate}% per {unit}, how much must be "
     "deposited today?"),
    ("The {fund} at {name} College must pay ${pmt} every {unit} forever "
     "out of interest alone. At {rate}% per {unit}, what principal is "
     "required?"),
    ("Find the present value of a perpetuity of ${pmt} per {unit} at "
     "{rate}% per {unit}."),
    ("{name} deposits a lump sum into a {fund} paying {rate}% per {unit}. "
     "If only the interest is withdrawn, the {fund} can pay ${pmt} every "
     "{unit} forever. How large is the lump sum?"),
]

AMORT_TEMPLATES = [
    ("Build a {n}-payment amortization schedule for a loan with starting "
     "balance ${bal}, payment ${pmt}, and period rate {rate}%. Find total "
     "interest and final balance."),
    ("{name} owes ${bal} on a {loan} charged {rate}% per {unit}. The "
     "payment is ${pmt} per {unit}. After {n} payments, find the total "
     "interest paid and the balance that remains."),
    ("A {loan} of ${bal} charges {rate}% interest per {unit}. With ${pmt} "
     "paid each {unit}, amortize the first {n} payments and give the "
     "total interest and the remaining balance."),
    ("The balance on {name}'s {loan} is ${bal}, the rate is {rate}% per "
     "{unit}, and the payment due each {unit} is ${pmt}. Fill in {n} rows "
     "of the amortization schedule, then report the total interest and "
     "the ending balance."),
]


def _context(rate_pct):
    unit = random.choice(units_for(rate_pct))
    return {
        "name": random.choice(NAMES),
        "fund": random.choice(FUNDS),
        "loan": random.choice(LOANS),
        "unit": unit,
        "units": unit + "s",
    }


class AnnuityGenerator(ProblemGenerator):
    """
    Annuity present/future value and short amortization schedules.

    Variants:
    - future_value: ordinary annuity FV = PMT((1+r)^n - 1)/r
    - present_value: ordinary annuity PV = PMT(1 - (1+r)^(-n))/r
    - amortization: an n-row schedule with interest/principal/balance
    - due: annuity due FV = PMT((1+r)^n - 1)/r * (1+r)
    - perpetuity: PV = PMT/r for a payment stream with no end

    Op-codes used:
    - ANNUITY_SETUP / ANNUITY_FORMULA / AMORT_ROW
    - PERCENT_TO_DEC (established)
    - A / S / M / D / E (established/shared): exact annuity arithmetic
    - CHECK (established): multiply_back / split verification
    - Z: exact money answer
    """

    VARIANTS = VARIANTS
    MODIFIERS = MODIFIERS

    def __init__(self, variant=None, modifier=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        if modifier is not None and modifier not in self.MODIFIERS:
            raise ValueError(f"modifier must be one of {self.MODIFIERS} or None")
        self.variant, self.modifier = variant, modifier

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "future_value":
            op, problem, steps, answer, used, value, model = self._future_value()
        elif variant == "present_value":
            op, problem, steps, answer, used, value, model = self._present_value()
        elif variant == "due":
            op, problem, steps, answer, used, value, model = self._due()
        elif variant == "perpetuity":
            op, problem, steps, answer, used, value, model = self._perpetuity()
        else:
            op, problem, steps, answer, used, value, model = self._amortization()
        modifier = self.modifier or random.choice(self.MODIFIERS)
        result = dict(
            problem_id=jid(),
            operation=f"annuity_{op}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
        return apply_applied_modifier(result, modifier, used, value, model, renderer=money)

    def _future_value(self):
        rate_pct, periods, payment = _pick(FV_TABLE, FV_WEIGHTS)
        rate = Fraction(rate_pct, 100)
        base = 1 + rate
        growth = base ** periods
        numerator = growth - 1
        factor = numerator / rate
        value = payment * factor
        assert cents_exact(value)
        answer = f"future_value {money(value)}"
        steps = [
            step("ANNUITY_SETUP", "ordinary annuity future value",
                 f"PMT={payment},r={rate_pct}%,n={periods}"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("ANNUITY_FORMULA", "FV = PMT*((1+r)^n - 1)/r"),
            step("A", 1, dec(rate), exact(base)),
            step("E", exact(base), periods, exact(growth)),
            step("S", exact(growth), 1, exact(numerator)),
            step("D", exact(numerator), dec(rate), exact(factor)),
            step("M", payment, exact(factor), exact(value)),
        ]
        if random.random() < 0.5:
            steps.append(step(
                "CHECK", "multiply_back",
                f"{exact(factor)}×{dec(rate)}+1={exact(growth)}",
                f"(1+r)^n={exact(growth)}"))
        steps.append(step("Z", answer))
        ctx = _context(rate_pct)
        problem = random.choice(FV_TEMPLATES).format(
            pmt=payment, n=periods, nth=ordinal(periods), rate=rate_pct,
            **ctx)
        used = [f"payment ${payment}", f"rate {rate_pct}%", f"periods {periods}"]
        return ("future_value", problem, steps, answer, used, value,
                "FV = PMT × ((1 + r)^n − 1)/r")

    def _present_value(self):
        rate_pct, periods, payment = _pick(PV_TABLE, PV_WEIGHTS)
        rate = Fraction(rate_pct, 100)
        base = 1 + rate
        growth = base ** periods
        discount = Fraction(1, 1) / growth
        numerator = 1 - discount
        factor = numerator / rate
        value = payment * factor
        assert cents_exact(value)
        answer = f"present_value {money(value)}"
        steps = [
            step("ANNUITY_SETUP", "ordinary annuity present value",
                 f"PMT={payment},r={rate_pct}%,n={periods}"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("ANNUITY_FORMULA", "PV = PMT*(1 - (1+r)^(-n))/r"),
            step("A", 1, dec(rate), exact(base)),
            step("E", exact(base), periods, exact(growth)),
            step("D", 1, exact(growth), exact(discount)),
            step("S", 1, exact(discount), exact(numerator)),
            step("D", exact(numerator), dec(rate), exact(factor)),
            step("M", payment, exact(factor), exact(value)),
        ]
        if random.random() < 0.5:
            steps.append(step(
                "CHECK", "multiply_back",
                f"{exact(factor)}×{dec(rate)}={exact(numerator)}",
                f"1-{exact(discount)}={exact(numerator)}"))
        steps.append(step("Z", answer))
        ctx = _context(rate_pct)
        problem = random.choice(PV_TEMPLATES).format(
            pmt=payment, n=periods, nth=ordinal(periods), rate=rate_pct,
            **ctx)
        used = [f"payment ${payment}", f"rate {rate_pct}%", f"periods {periods}"]
        return ("present_value", problem, steps, answer, used, value,
                "PV = PMT × (1 − (1 + r)^(−n))/r")

    def _due(self):
        rate_pct, periods, payment = _pick(DUE_TABLE, DUE_WEIGHTS)
        rate = Fraction(rate_pct, 100)
        base = 1 + rate
        growth = base ** periods
        numerator = growth - 1
        factor = numerator / rate
        ordinary = payment * factor
        value = ordinary * base
        assert cents_exact(value)
        answer = f"future_value_due {money(value)}"
        steps = [
            step("ANNUITY_SETUP", "annuity due future value",
                 f"PMT={payment},r={rate_pct}%,n={periods}"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("ANNUITY_FORMULA", "FV(due) = PMT*((1+r)^n - 1)/r*(1+r)"),
            step("A", 1, dec(rate), exact(base)),
            step("E", exact(base), periods, exact(growth)),
            step("S", exact(growth), 1, exact(numerator)),
            step("D", exact(numerator), dec(rate), exact(factor)),
            step("M", payment, exact(factor), exact(ordinary)),
            step("M", exact(ordinary), exact(base), exact(value)),
        ]
        if random.random() < 0.5:
            steps.append(step(
                "CHECK", "multiply_back",
                f"{exact(factor)}×{dec(rate)}+1={exact(growth)}",
                f"(1+r)^n={exact(growth)}"))
        steps.append(step("Z", answer))
        ctx = _context(rate_pct)
        problem = random.choice(DUE_TEMPLATES).format(
            pmt=payment, n=periods, nth=ordinal(periods), rate=rate_pct,
            **ctx)
        used = [f"payment ${payment}", f"rate {rate_pct}%", f"periods {periods}"]
        return ("due", problem, steps, answer, used, value,
                "FV(due) = PMT × ((1 + r)^n − 1)/r × (1 + r)")

    def _perpetuity(self):
        rate_pct, payment = _pick(PERP_TABLE, PERP_WEIGHTS)
        rate = Fraction(rate_pct, 100)
        value = payment / rate
        assert cents_exact(value)
        answer = f"present_value {money(value)}"
        steps = [
            step("ANNUITY_SETUP", "perpetuity present value",
                 f"PMT={payment},r={rate_pct}%"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("ANNUITY_FORMULA", "PV = PMT/r"),
            step("D", payment, dec(rate), exact(value)),
            step("CHECK", "multiply_back",
                 f"{exact(value)}×{dec(rate)}={payment}",
                 f"PMT={payment}"),
            step("Z", answer),
        ]
        ctx = _context(rate_pct)
        problem = random.choice(PERP_TEMPLATES).format(
            pmt=payment, rate=rate_pct, **ctx)
        used = [f"payment ${payment}", f"rate {rate_pct}%"]
        return "perpetuity", problem, steps, answer, used, value, "PV = PMT/r"

    def _amortization(self):
        while True:
            rate_pct = random.choice([2, 4, 5, 8, 10, 12, 15, 20, 24, 25, 50])
            periods = random.randint(2, 5)
            rate = Fraction(rate_pct, 100)
            base = 1 + rate
            den = 100 // gcd(rate_pct, 100)
            bal_mod = den ** periods // gcd(den ** periods, 100)
            pay_mod = den ** (periods - 1) // gcd(den ** (periods - 1), 100)
            bal_step = bal_mod if bal_mod >= 100 else bal_mod * (
                (100 + bal_mod - 1) // bal_mod)
            if bal_step > 500:
                continue
            balances = list(range(
                ((1000 + bal_step - 1) // bal_step) * bal_step,
                99001, bal_step))
            if not balances:
                continue
            original_balance = random.choice(balances)
            start = Fraction(original_balance)
            growth = base ** periods
            series = (growth - 1) / rate
            pay_low = start * rate
            pay_high = start * growth / series
            pay_step = pay_mod if pay_mod >= 25 else pay_mod * (
                (25 + pay_mod - 1) // pay_mod)
            first = (int(pay_low) // pay_step + 1) * pay_step
            last = pay_step * ((int(pay_high) - 1) // pay_step)
            if first > last:
                continue
            payment = random.randrange(first, last + 1, pay_step)
            if payment <= pay_low or payment >= pay_high:
                continue
            break

        balance = start
        steps = [
            step("ANNUITY_SETUP", "amortization schedule",
                 f"balance={original_balance},payment={payment},"
                 f"r={rate_pct}%",
                 f"periods={periods}"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("ANNUITY_FORMULA",
                 "interest=balance*r; principal=payment-interest"),
        ]
        total_interest = Fraction(0)
        for period in range(1, periods + 1):
            interest = balance * rate
            principal = payment - interest
            new_balance = balance - principal
            new_total = total_interest + interest
            steps.extend([
                step("M", exact(balance), dec(rate), exact(interest)),
                step("S", payment, exact(interest), exact(principal)),
                step("S", exact(balance), exact(principal), exact(new_balance)),
                step("A", exact(total_interest), exact(interest),
                     exact(new_total)),
                step("AMORT_ROW", period, f"interest={money(interest)}",
                     f"principal={money(principal)},balance={money(new_balance)}"),
            ])
            balance = new_balance
            total_interest = new_total
        paid_down = start - balance
        steps.append(step(
            "CHECK", "split",
            f"{periods}×{payment}-{exact(total_interest)}={exact(paid_down)}",
            f"{original_balance}-{exact(balance)}={exact(paid_down)}"))
        answer = (
            f"total_interest {money(total_interest)}; "
            f"final_balance {money(balance)}"
        )
        steps.append(step("Z", answer))
        ctx = _context(rate_pct)
        problem = random.choice(AMORT_TEMPLATES).format(
            bal=original_balance, pmt=payment, n=periods, rate=rate_pct,
            **ctx)
        used = [f"balance ${original_balance}", f"payment ${payment}",
                f"rate {rate_pct}%", f"periods {periods}"]
        return ("amortization", problem, steps, answer, used, balance,
                "interest = balance × r; principal = payment − interest")
