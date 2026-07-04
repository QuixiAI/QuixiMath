import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec, money


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


class FinanceGenerator(ProblemGenerator):
    """
    Everyday financial arithmetic: simple interest, annual compounding, loan
    payment breakdowns, and budget percentage splits. Amounts are constructed
    so dollar-and-cent answers are exact.

    Variants:
    - simple_interest:   I = P*r*t, then A = P + I
    - compound_interest: A = P(1+r)^t, then interest = A - P
    - loan_payment:      interest, principal, and new balance for one payment
    - budget_split:      category amounts from percentages of income

    Op-codes used:
    - FIN_SETUP: financial context and goal
    - FIN_FORMULA: formula or payment rule
    - PERCENT_TO_DEC (established): percent as a decimal rate
    - RATE_MONTHLY: annual percent divided by 12
    - M / A / S / E (established): exact arithmetic
    - Z: exact money answer
    """

    VARIANTS = ["simple_interest", "compound_interest",
                "loan_payment", "budget_split"]
    BUDGET_SPLITS = [(50, 20, 30), (60, 20, 20), (70, 10, 20),
                     (40, 30, 30), (55, 15, 30)]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def _simple_interest(self):
        principal = random.choice([200, 300, 400, 500, 800, 1000, 1200])
        rate_pct = random.choice([3, 4, 5, 6, 8, 10, 12])
        years = random.randint(1, 5)
        rate = Fraction(rate_pct, 100)
        annual = principal * rate
        interest = annual * years
        balance = principal + interest
        answer = f"interest {money(interest)}; balance {money(balance)}"
        steps = [
            step("FIN_SETUP", f"simple interest P = {principal}",
                 f"r = {rate_pct}%, t = {years}", "interest and balance"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("FIN_FORMULA", "I = P*r*t; A = P + I"),
            step("M", principal, dec(rate), exact(annual)),
            step("M", exact(annual), years, exact(interest)),
            step("A", principal, exact(interest), exact(balance)),
            step("Z", answer),
        ]
        problem = (
            f"An account starts with ${principal} and earns simple interest "
            f"at {rate_pct}% per year for {years} year{'s' if years != 1 else ''}. Find the interest "
            "and ending balance."
        )
        return "simple_interest", problem, steps, answer

    def _compound_interest(self):
        while True:
            principal = random.choice([200, 400, 500, 800, 1000, 1200, 2000])
            rate_pct = random.choice([5, 10, 20, 25])
            years = random.randint(2, 4)
            rate = Fraction(rate_pct, 100)
            base = 1 + rate
            growth = base ** years
            balance = principal * growth
            if (balance * 100).denominator == 1:
                break
        interest = balance - principal
        answer = f"balance {money(balance)}; interest {money(interest)}"
        steps = [
            step("FIN_SETUP", f"compound interest P = {principal}",
                 f"r = {rate_pct}%, t = {years}", "ending balance"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("FIN_FORMULA", "A = P(1+r)^t"),
            step("A", 1, dec(rate), dec(base)),
            step("E", dec(base), years, exact(growth)),
            step("M", principal, exact(growth), exact(balance)),
            step("S", exact(balance), principal, exact(interest)),
            step("Z", answer),
        ]
        problem = (
            f"An account starts with ${principal} and earns {rate_pct}% "
            f"interest compounded once per year for {years} years. Find "
            "the ending balance and total interest."
        )
        return "compound_interest", problem, steps, answer

    def _loan_payment(self):
        balance = random.randrange(1000, 5001, 100)
        annual_pct = random.choice([6, 12, 18, 24])
        monthly_rate = Fraction(annual_pct, 1200)
        interest = balance * monthly_rate
        payment = int(interest) + random.choice([75, 100, 125, 150, 200])
        principal_paid = Fraction(payment) - interest
        new_balance = Fraction(balance) - principal_paid
        answer = (f"interest {money(interest)}; principal "
                  f"{money(principal_paid)}; balance {money(new_balance)}")
        steps = [
            step("FIN_SETUP", f"loan balance = {balance}",
                 f"payment = {payment}, annual rate = {annual_pct}%",
                 "one-payment breakdown"),
            step("RATE_MONTHLY", f"{annual_pct}% / 12",
                 exact(monthly_rate)),
            step("FIN_FORMULA",
                 "interest = balance*monthly rate; principal = payment - interest"),
            step("M", balance, exact(monthly_rate), exact(interest)),
            step("S", payment, exact(interest), exact(principal_paid)),
            step("S", balance, exact(principal_paid), exact(new_balance)),
            step("Z", answer),
        ]
        problem = (
            f"A loan has current balance ${balance}. The monthly payment is "
            f"${payment} and the annual interest rate is {annual_pct}%. "
            "For this month, find the interest paid, principal paid, and "
            "new balance."
        )
        return "loan_payment", problem, steps, answer

    def _budget_split(self):
        income = random.randrange(1200, 5001, 100)
        needs_pct, savings_pct, fun_pct = random.choice(self.BUDGET_SPLITS)
        needs = income * Fraction(needs_pct, 100)
        savings = income * Fraction(savings_pct, 100)
        fun = income * Fraction(fun_pct, 100)
        answer = (f"needs {money(needs)}; savings {money(savings)}; "
                  f"fun {money(fun)}")
        steps = [
            step("FIN_SETUP", f"income = {income}",
                 f"needs {needs_pct}%, savings {savings_pct}%, fun {fun_pct}%",
                 "budget amounts"),
            step("FIN_FORMULA", "category amount = income * category percent"),
            step("PERCENT_TO_DEC", f"{needs_pct}%", dec(Fraction(needs_pct, 100))),
            step("M", income, dec(Fraction(needs_pct, 100)), exact(needs)),
            step("PERCENT_TO_DEC", f"{savings_pct}%", dec(Fraction(savings_pct, 100))),
            step("M", income, dec(Fraction(savings_pct, 100)), exact(savings)),
            step("PERCENT_TO_DEC", f"{fun_pct}%", dec(Fraction(fun_pct, 100))),
            step("M", income, dec(Fraction(fun_pct, 100)), exact(fun)),
            step("A", exact(needs), exact(savings), exact(needs + savings)),
            step("A", exact(needs + savings), exact(fun), exact(income)),
            step("Z", answer),
        ]
        problem = (
            f"A monthly income of ${income} is split into needs {needs_pct}%, "
            f"savings {savings_pct}%, and fun {fun_pct}%. Find the dollar "
            "amount for each category."
        )
        return "budget_split", problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "simple_interest":
            op_suffix, problem, steps, answer = self._simple_interest()
        elif variant == "compound_interest":
            op_suffix, problem, steps, answer = self._compound_interest()
        elif variant == "loan_payment":
            op_suffix, problem, steps, answer = self._loan_payment()
        else:
            op_suffix, problem, steps, answer = self._budget_split()

        return dict(
            problem_id=jid(),
            operation=f"finance_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
