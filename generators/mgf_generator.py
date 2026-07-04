import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def exp_term(coefficient, power):
    coefficient = Fraction(coefficient)
    coef_text = "" if coefficient == 1 else f"{fraction_text(coefficient)}*"
    if power == 0:
        return fraction_text(coefficient)
    if power == 1:
        return f"{coef_text}e^t"
    return f"{coef_text}e^({power}t)"


def formula(terms):
    return " + ".join(terms)


class MGFGenerator(ProblemGenerator):
    """
    Derive a discrete moment generating function and differentiate for moments.

    Op-codes used:
    - MGF_SETUP: probability mass function
    - MGF_TERM: each p(x)e^(tx) contribution
    - DERIVATIVE: first and second MGF derivatives
    - EVAL_AT_ZERO: substitute t=0 in exponentials
    - REWRITE: assembled MGF formula
    - A / S / M / E (established/shared): exact moment arithmetic
    - Z: M(t), E[X], E[X^2], and Var(X)
    """

    def generate(self) -> dict:
        total = random.randint(8, 48)
        c0 = random.randint(1, total - 2)
        c1 = random.randint(1, total - c0 - 1)
        c2 = total - c0 - c1
        p0 = Fraction(c0, total)
        p1 = Fraction(c1, total)
        p2 = Fraction(c2, total)

        mgf = formula([exp_term(p0, 0), exp_term(p1, 1), exp_term(p2, 2)])
        first_derivative = formula([exp_term(p1, 1), exp_term(2 * p2, 2)])
        second_derivative = formula([exp_term(p1, 1), exp_term(4 * p2, 2)])

        two_p2 = 2 * p2
        mean = p1 + two_p2
        four = 2 ** 2
        four_p2 = four * p2
        second_moment = p1 + four_p2
        mean_sq = mean * mean
        variance = second_moment - mean_sq

        steps = [
            step("MGF_SETUP", f"P(X=0)={fraction_text(p0)}",
                 f"P(X=1)={fraction_text(p1)}",
                 f"P(X=2)={fraction_text(p2)}"),
            step("MGF_TERM", "x=0", "p0*e^(0t)", fraction_text(p0)),
            step("MGF_TERM", "x=1", "p1*e^t", exp_term(p1, 1)),
            step("MGF_TERM", "x=2", "p2*e^(2t)", exp_term(p2, 2)),
            step("REWRITE", f"M(t)={mgf}"),
            step("DERIVATIVE", f"M'(t)={first_derivative}"),
            step("DERIVATIVE", f"M''(t)={second_derivative}"),
            step("EVAL_AT_ZERO", "e^0=1", "e^(2*0)=1"),
            step("M", 2, fraction_text(p2), fraction_text(two_p2)),
            step("A", fraction_text(p1), fraction_text(two_p2),
                 fraction_text(mean)),
            step("E", 2, 2, four),
            step("M", four, fraction_text(p2), fraction_text(four_p2)),
            step("A", fraction_text(p1), fraction_text(four_p2),
                 fraction_text(second_moment)),
            step("M", fraction_text(mean), fraction_text(mean),
                 fraction_text(mean_sq)),
            step("S", fraction_text(second_moment), fraction_text(mean_sq),
                 fraction_text(variance)),
        ]
        answer = (
            f"M(t)={mgf}; E[X]={fraction_text(mean)}; "
            f"E[X^2]={fraction_text(second_moment)}; "
            f"Var(X)={fraction_text(variance)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"A discrete random variable has P(X=0)={fraction_text(p0)}, "
            f"P(X=1)={fraction_text(p1)}, and "
            f"P(X=2)={fraction_text(p2)}. Derive M(t), then use M'(0) "
            "and M''(0) to find E[X], E[X^2], and Var(X)."
        )
        return dict(
            problem_id=jid(),
            operation="mgf_discrete_three_point",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
