import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
from generators.finance_generator import exact


VARIANTS = ["npv", "irr_newton"]


def fraction_text(value):
    return str(Fraction(value))


class NPVIRRGenerator(ProblemGenerator):
    """
    Net present value and IRR via Newton iterations.

    Variants:
    - npv: discount a short cash-flow stream at a given rate.
    - irr_newton: estimate one-period IRR with two exact Newton iterations.

    Op-codes used:
    - NPV_SETUP / NPV_TERM / IRR_SETUP / IRR_VALUE / NEWTON_STEP
    - PERCENT_TO_DEC (established)
    - A / S / M / D / E (established/shared): discounting and Newton update
    - Z: exact NPV or Newton IRR estimate
    """

    VARIANTS = VARIANTS

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "npv":
            problem, steps, answer = self._generate_npv()
        else:
            problem, steps, answer = self._generate_irr()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"npv_irr_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_npv(self):
        c0 = -random.randrange(500, 3001, 100)
        cashflows = [random.randrange(100, 2001, 50) for _ in range(3)]
        rate_pct = random.choice([5, 10, 20, 25])
        rate = Fraction(rate_pct, 100)
        base = 1 + rate
        total = Fraction(c0)
        steps = [
            step("NPV_SETUP", f"c0={c0},c1={cashflows[0]},c2={cashflows[1]},c3={cashflows[2]}",
                 f"rate={rate_pct}%"),
            step("PERCENT_TO_DEC", f"{rate_pct}%", dec(rate)),
            step("A", 1, dec(rate), exact(base)),
            step("NPV_TERM", "t=0", exact(total)),
        ]
        for t, cashflow in enumerate(cashflows, start=1):
            discount = base ** t
            pv = Fraction(cashflow, 1) / discount
            new_total = total + pv
            steps.extend([
                step("E", exact(base), t, exact(discount)),
                step("D", cashflow, exact(discount), exact(pv)),
                step("NPV_TERM", f"t={t}", exact(pv)),
                step("A", exact(total), exact(pv), exact(new_total)),
            ])
            total = new_total
        answer = f"NPV={exact(total)}"
        problem = (
            f"Compute NPV for cash flows c0={c0}, c1={cashflows[0]}, "
            f"c2={cashflows[1]}, c3={cashflows[2]} at discount rate "
            f"{rate_pct}%."
        )
        return problem, steps, answer

    def _generate_irr(self):
        investment = random.randrange(500, 3001, 100)
        payoff_multiplier = random.choice([
            Fraction(6, 5), Fraction(3, 2), Fraction(2), Fraction(5, 2)
        ])
        payoff = int(investment * payoff_multiplier)
        c0 = -investment
        r = random.choice([Fraction(0), Fraction(1, 10), Fraction(1, 5)])
        initial_r = r
        iterations = 2
        steps = [
            step("IRR_SETUP", f"c0={c0},c1={payoff}",
                 f"r0={fraction_text(initial_r)},iterations={iterations}"),
        ]
        for iteration in range(1, iterations + 1):
            base = 1 + r
            pv = Fraction(payoff, 1) / base
            f_value = c0 + pv
            base_sq = base ** 2
            deriv_abs = Fraction(payoff, 1) / base_sq
            derivative = -deriv_abs
            correction = f_value / derivative
            next_r = r - correction
            steps.extend([
                step("A", 1, fraction_text(r), fraction_text(base)),
                step("D", payoff, fraction_text(base), fraction_text(pv)),
                step("A", c0, fraction_text(pv), fraction_text(f_value)),
                step("IRR_VALUE", f"f{iteration}", fraction_text(f_value)),
                step("E", fraction_text(base), 2, fraction_text(base_sq)),
                step("D", payoff, fraction_text(base_sq),
                     fraction_text(deriv_abs)),
                step("M", -1, fraction_text(deriv_abs),
                     fraction_text(derivative)),
                step("IRR_VALUE", f"fprime{iteration}",
                     fraction_text(derivative)),
                step("D", fraction_text(f_value), fraction_text(derivative),
                     fraction_text(correction)),
                step("S", fraction_text(r), fraction_text(correction),
                     fraction_text(next_r)),
                step("NEWTON_STEP", iteration, fraction_text(next_r)),
            ])
            r = next_r
        answer = f"IRR_estimate={fraction_text(r)}"
        problem = (
            f"Estimate IRR for cash flows c0={c0}, c1={payoff} using "
            f"Newton's method from r0={fraction_text(initial_r)} "
            f"for {iterations} iterations."
        )
        return problem, steps, answer
