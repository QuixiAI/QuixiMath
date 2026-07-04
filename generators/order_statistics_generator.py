import math
import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class OrderStatisticsGenerator(ProblemGenerator):
    """
    Uniform(0,1) order statistic pdf, moments, and exact pdf evaluation.

    Op-codes used:
    - ORDER_SETUP: sample size, order index, and evaluation point
    - ORDER_PDF: symbolic pdf formula for X_(k)
    - FACT: factorial arithmetic for the coefficient
    - A / S / M / D / E (established/shared): exact arithmetic
    - Z: pdf, mean, variance, and f(q)
    """

    def generate(self) -> dict:
        n = random.randint(2, 9)
        k = random.randint(1, n)
        den = random.randint(3, 15)
        num = random.randint(1, den - 1)
        q = Fraction(num, den)

        n_fact = math.factorial(n)
        k_minus = k - 1
        n_minus = n - k
        k_minus_fact = math.factorial(k_minus)
        n_minus_fact = math.factorial(n_minus)
        denom_fact = k_minus_fact * n_minus_fact
        coef = Fraction(n_fact, denom_fact)

        one_minus_q = 1 - q
        q_power = q ** k_minus
        one_minus_power = one_minus_q ** n_minus
        pdf_partial = coef * q_power
        pdf_value = pdf_partial * one_minus_power

        n_plus_one = n + 1
        mean = Fraction(k, n_plus_one)
        n_plus_one_minus_k = n_plus_one - k
        var_num = k * n_plus_one_minus_k
        n_plus_one_sq = n_plus_one ** 2
        n_plus_two = n_plus_one + 1
        var_den = n_plus_one_sq * n_plus_two
        variance = Fraction(var_num, var_den)

        pdf_formula = f"{fraction_text(coef)}*x^{k_minus}*(1-x)^{n_minus}"
        steps = [
            step("ORDER_SETUP", f"n={n}", f"k={k}",
                 f"q={fraction_text(q)}"),
            step("FACT", n, n_fact),
            step("S", k, 1, k_minus),
            step("S", n, k, n_minus),
            step("FACT", k_minus, k_minus_fact),
            step("FACT", n_minus, n_minus_fact),
            step("M", k_minus_fact, n_minus_fact, denom_fact),
            step("D", n_fact, denom_fact, fraction_text(coef)),
            step("ORDER_PDF", f"f_{{{k}:{n}}}(x)={pdf_formula}"),
            step("S", 1, fraction_text(q), fraction_text(one_minus_q)),
            step("E", fraction_text(q), k_minus, fraction_text(q_power)),
            step("E", fraction_text(one_minus_q), n_minus,
                 fraction_text(one_minus_power)),
            step("M", fraction_text(coef), fraction_text(q_power),
                 fraction_text(pdf_partial)),
            step("M", fraction_text(pdf_partial),
                 fraction_text(one_minus_power), fraction_text(pdf_value)),
            step("A", n, 1, n_plus_one),
            step("D", k, n_plus_one, fraction_text(mean)),
            step("S", n_plus_one, k, n_plus_one_minus_k),
            step("M", k, n_plus_one_minus_k, var_num),
            step("E", n_plus_one, 2, n_plus_one_sq),
            step("A", n_plus_one, 1, n_plus_two),
            step("M", n_plus_one_sq, n_plus_two, var_den),
            step("D", var_num, var_den, fraction_text(variance)),
        ]
        answer = (
            f"f_{{{k}:{n}}}(x)={pdf_formula}; "
            f"E[X_({k})]={fraction_text(mean)}; "
            f"Var(X_({k}))={fraction_text(variance)}; "
            f"f_{{{k}:{n}}}({fraction_text(q)})={fraction_text(pdf_value)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For {n} iid Uniform(0,1) samples, find the pdf, mean, "
            f"variance, and f({fraction_text(q)}) for the {k}-th order "
            f"statistic X_({k})."
        )
        return dict(
            problem_id=jid(),
            operation="order_statistics_uniform_pdf_moments",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
