import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec
from generators.finance_generator import exact


def pct(pct_value):
    return Fraction(pct_value, 100)


class PortfolioGenerator(ProblemGenerator):
    """
    Two-asset portfolio expected return and variance with covariance.

    Op-codes used:
    - PORT_SETUP / PORT_FORMULA / PORT_RESULT
    - PERCENT_TO_DEC (established)
    - A / M / E (established/shared): exact weighted sums and variance terms
    - Z: expected return and variance
    """

    def generate(self) -> dict:
        w_a = random.choice([
            Fraction(1, 4), Fraction(1, 3), Fraction(2, 5),
            Fraction(1, 2), Fraction(3, 5), Fraction(2, 3),
            Fraction(3, 4),
        ])
        w_b = 1 - w_a
        r_a_pct = random.choice([4, 6, 8, 10, 12, 15])
        r_b_pct = random.choice([5, 7, 9, 11, 14, 18])
        vol_a = pct(random.choice([10, 15, 20, 25, 30]))
        vol_b = pct(random.choice([10, 15, 20, 25, 30]))
        rho = random.choice([
            Fraction(-1, 2), Fraction(-1, 4), Fraction(0),
            Fraction(1, 4), Fraction(1, 2),
        ])

        r_a = pct(r_a_pct)
        r_b = pct(r_b_pct)
        var_a = vol_a ** 2
        var_b = vol_b ** 2
        cov = rho * vol_a * vol_b

        er_a = w_a * r_a
        er_b = w_b * r_b
        expected_return = er_a + er_b

        w_a_sq = w_a ** 2
        w_b_sq = w_b ** 2
        var_term_a = w_a_sq * var_a
        var_term_b = w_b_sq * var_b
        two_w_a = 2 * w_a
        two_w_aw_b = two_w_a * w_b
        cov_term = two_w_aw_b * cov
        variance_without_cov = var_term_a + var_term_b
        variance = variance_without_cov + cov_term

        answer = (
            f"expected_return={exact(expected_return)}; "
            f"variance={exact(variance)}"
        )
        steps = [
            step("PORT_SETUP", f"wA={exact(w_a)},wB={exact(w_b)}",
                 f"rA={r_a_pct}%,rB={r_b_pct}%",
                 f"varA={exact(var_a)},varB={exact(var_b)},cov={exact(cov)}"),
            step("PERCENT_TO_DEC", f"{r_a_pct}%", dec(r_a)),
            step("PERCENT_TO_DEC", f"{r_b_pct}%", dec(r_b)),
            step("PORT_FORMULA", "E=wA*rA+wB*rB",
                 "Var=wA^2*varA+wB^2*varB+2*wA*wB*cov"),
            step("M", exact(w_a), dec(r_a), exact(er_a)),
            step("M", exact(w_b), dec(r_b), exact(er_b)),
            step("A", exact(er_a), exact(er_b), exact(expected_return)),
            step("E", exact(w_a), 2, exact(w_a_sq)),
            step("M", exact(w_a_sq), exact(var_a), exact(var_term_a)),
            step("E", exact(w_b), 2, exact(w_b_sq)),
            step("M", exact(w_b_sq), exact(var_b), exact(var_term_b)),
            step("M", 2, exact(w_a), exact(two_w_a)),
            step("M", exact(two_w_a), exact(w_b), exact(two_w_aw_b)),
            step("M", exact(two_w_aw_b), exact(cov), exact(cov_term)),
            step("A", exact(var_term_a), exact(var_term_b),
                 exact(variance_without_cov)),
            step("A", exact(variance_without_cov), exact(cov_term),
                 exact(variance)),
            step("PORT_RESULT", f"expected_return={exact(expected_return)}",
                 f"variance={exact(variance)}"),
            step("Z", answer),
        ]
        problem = (
            f"A portfolio invests weight wA={exact(w_a)} in asset A and "
            f"wB={exact(w_b)} in asset B. Asset A has expected return "
            f"{r_a_pct}% and variance {exact(var_a)}; asset B has expected "
            f"return {r_b_pct}% and variance {exact(var_b)}; covariance is "
            f"{exact(cov)}. Compute portfolio expected return and variance."
        )
        return dict(
            problem_id=jid(),
            operation="portfolio_two_asset",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
