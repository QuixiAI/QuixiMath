import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money
from generators.finance_generator import exact


VARIANTS = ["future_value", "present_value", "amortization"]


def cents_exact(value):
    return (value * 100).denominator == 1


class AnnuityGenerator(ProblemGenerator):
    """
    Annuity present/future value and short amortization schedules.

    Variants:
    - future_value: ordinary annuity FV = PMT((1+r)^n - 1)/r
    - present_value: ordinary annuity PV = PMT(1 - (1+r)^(-n))/r
    - amortization: three payment rows with interest/principal/balance

    Op-codes used:
    - ANNUITY_SETUP / ANNUITY_FORMULA / AMORT_ROW
    - PERCENT_TO_DEC (established)
    - A / S / M / D / E (established/shared): exact annuity arithmetic
    - Z: exact money answer
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "future_value":
            op, problem, steps, answer = self._future_value()
        elif variant == "present_value":
            op, problem, steps, answer = self._present_value()
        else:
            op, problem, steps, answer = self._amortization()
        return dict(
            problem_id=jid(),
            operation=f"annuity_{op}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _future_value(self):
        while True:
            payment = random.randrange(100, 1001, 50)
            rate_pct = random.choice([10, 20, 25, 50])
            periods = random.randint(2, 5)
            rate = Fraction(rate_pct, 100)
            base = 1 + rate
            growth = base ** periods
            numerator = growth - 1
            factor = numerator / rate
            value = payment * factor
            if cents_exact(value):
                break
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
            step("Z", answer),
        ]
        problem = (
            f"An ordinary annuity pays ${payment} at the end of each period "
            f"for {periods} periods at {rate_pct}% per period. Find the "
            "future value."
        )
        return "future_value", problem, steps, answer

    def _present_value(self):
        while True:
            payment = random.randrange(100, 1001, 50)
            rate_pct = random.choice([10, 20, 25, 50])
            periods = random.randint(2, 5)
            rate = Fraction(rate_pct, 100)
            base = 1 + rate
            growth = base ** periods
            discount = Fraction(1, 1) / growth
            numerator = 1 - discount
            factor = numerator / rate
            value = payment * factor
            if cents_exact(value):
                break
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
            step("Z", answer),
        ]
        problem = (
            f"An ordinary annuity pays ${payment} at the end of each period "
            f"for {periods} periods at {rate_pct}% per period. Find the "
            "present value."
        )
        return "present_value", problem, steps, answer

    def _amortization(self):
        original_balance = random.randrange(1024, 8193, 512)
        balance = Fraction(original_balance)
        rate_pct = 50
        rate = Fraction(rate_pct, 100)
        payment = int(balance * Fraction(5, 8))
        periods = 3
        steps = [
            step("ANNUITY_SETUP", "amortization schedule",
                 f"balance={int(balance)},payment={payment},r={rate_pct}%",
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
        answer = (
            f"total_interest {money(total_interest)}; "
            f"final_balance {money(balance)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Build a {periods}-payment amortization schedule for a loan with "
            f"starting balance ${original_balance}, "
            f"payment ${payment}, and period rate {rate_pct}%. Find total "
            "interest and final balance."
        )
        return "amortization", problem, steps, answer
