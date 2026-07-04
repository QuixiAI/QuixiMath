import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.finance_generator import exact


class BlackScholesGenerator(ProblemGenerator):
    """
    Black-Scholes call and put evaluation with normal CDF values supplied.

    Op-codes used:
    - BS_SETUP / BS_FORMULA / NORMAL_SYMMETRY / BS_RESULT
    - M / S (established/shared): exact formula arithmetic
    - Z: call and put prices
    """

    N_PAIRS = [
        (Fraction(3, 5), Fraction(11, 20)),
        (Fraction(13, 20), Fraction(3, 5)),
        (Fraction(7, 10), Fraction(13, 20)),
        (Fraction(3, 4), Fraction(7, 10)),
        (Fraction(4, 5), Fraction(3, 4)),
        (Fraction(9, 10), Fraction(17, 20)),
    ]

    def generate(self) -> dict:
        while True:
            stock = random.choice([80, 90, 100, 110, 120, 150])
            strike = random.choice([80, 90, 100, 110, 120, 150])
            discount = random.choice([
                Fraction(9, 10), Fraction(19, 20), Fraction(39, 40)
            ])
            n_d1, n_d2 = random.choice(self.N_PAIRS)
            stock_call_term = stock * n_d1
            discounted_strike = strike * discount
            strike_call_term = discounted_strike * n_d2
            call_price = stock_call_term - strike_call_term
            n_neg_d1 = 1 - n_d1
            n_neg_d2 = 1 - n_d2
            put_strike_term = discounted_strike * n_neg_d2
            put_stock_term = stock * n_neg_d1
            put_price = put_strike_term - put_stock_term
            if call_price > 0 and put_price > 0:
                break

        answer = f"call={exact(call_price)}; put={exact(put_price)}"
        steps = [
            step("BS_SETUP", f"S={stock},K={strike}",
                 f"df={exact(discount)}",
                 f"N_d1={exact(n_d1)},N_d2={exact(n_d2)}"),
            step("BS_FORMULA", "C=S*N(d1)-K*df*N(d2)",
                 "P=K*df*N(-d2)-S*N(-d1)"),
            step("M", stock, exact(n_d1), exact(stock_call_term)),
            step("M", strike, exact(discount), exact(discounted_strike)),
            step("M", exact(discounted_strike), exact(n_d2),
                 exact(strike_call_term)),
            step("S", exact(stock_call_term), exact(strike_call_term),
                 exact(call_price)),
            step("S", 1, exact(n_d1), exact(n_neg_d1)),
            step("S", 1, exact(n_d2), exact(n_neg_d2)),
            step("NORMAL_SYMMETRY", f"N_neg_d1={exact(n_neg_d1)}",
                 f"N_neg_d2={exact(n_neg_d2)}"),
            step("M", exact(discounted_strike), exact(n_neg_d2),
                 exact(put_strike_term)),
            step("M", stock, exact(n_neg_d1), exact(put_stock_term)),
            step("S", exact(put_strike_term), exact(put_stock_term),
                 exact(put_price)),
            step("BS_RESULT", f"call={exact(call_price)}",
                 f"put={exact(put_price)}"),
            step("Z", answer),
        ]
        problem = (
            f"Evaluate Black-Scholes option prices with S={stock}, "
            f"K={strike}, discount_factor={exact(discount)}, "
            f"N(d1)={exact(n_d1)}, and N(d2)={exact(n_d2)}. "
            "Use N(-d)=1-N(d). Compute the call and put prices."
        )
        return dict(
            problem_id=jid(),
            operation="black_scholes_call_put",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
